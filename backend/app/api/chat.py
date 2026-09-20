import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.db_models import Message, Session, Artifact
from app.models.schemas import ChatRequest
from app.providers.factory import get_provider
from app.rag.retriever import retrieve_relevant_chunks
from app.skills.ship30_writer import (
    build_grounded_prompt,
    build_ship30_prompt,
)


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


INSUFFICIENT_INFORMATION = (
    "I do not have sufficient information in Lenny's podcast archive "
    "to answer this"
)


def build_citations(chunks: list[dict]) -> list[dict]:
    return [
        {
            "episode": chunk["title"],
            "guest": chunk["guest"],
            "timestamp": chunk["timestamp"],
            "similarity": chunk["similarity"],
        }
        for chunk in chunks
    ]


@router.post("")
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):

    # --------------------------------------------------
    # 1. Validate session
    # --------------------------------------------------

    if request.session_id is None:
        raise HTTPException(
            status_code=400,
            detail="session_id is required",
        )

    session_result = await db.execute(
        select(Session).where(Session.id == request.session_id)
    )

    chat_session = session_result.scalar_one_or_none()

    if chat_session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    # --------------------------------------------------
    # 2. Save user message
    # --------------------------------------------------

    user_message = Message(
        session_id=request.session_id,
        role="user",
        content=request.message,
        sources=[],
    )

    db.add(user_message)
    await db.commit()

    # --------------------------------------------------
    # 3. Retrieve relevant transcript chunks
    # --------------------------------------------------

    chunks = await retrieve_relevant_chunks(
        session=db,
        query=request.message,
        top_k=5,
        threshold=0.65,
    )

    sources = build_citations(chunks)

    # --------------------------------------------------
    # 4. Handle insufficient context
    # --------------------------------------------------

    if not chunks:

        assistant_content = INSUFFICIENT_INFORMATION

        assistant_message = Message(
            session_id=request.session_id,
            role="assistant",
            content=assistant_content,
            sources=[],
        )

        db.add(assistant_message)
        await db.commit()

        async def empty_generator():

            yield (
                "data: "
                + json.dumps(
                    {
                        "type": "status",
                        "content": "No relevant transcript context found.",
                    }
                )
                + "\n\n"
            )

            yield (
                "data: "
                + json.dumps(
                    {
                        "type": "sources",
                        "sources": [],
                    }
                )
                + "\n\n"
            )

            yield (
                "data: "
                + json.dumps(
                    {
                        "type": "token",
                        "content": assistant_content,
                    }
                )
                + "\n\n"
            )

            yield "data: [DONE]\n\n"

        return StreamingResponse(
            empty_generator(),
            media_type="text/event-stream",
        )

    # --------------------------------------------------
    # 5. Build prompt
    # --------------------------------------------------

    if request.mode == "ship30":

        prompt = build_ship30_prompt(
            user_query=request.message,
            retrieved_chunks=chunks,
        )

    else:

        prompt = build_grounded_prompt(
            user_query=request.message,
            retrieved_chunks=chunks,
        )

    # --------------------------------------------------
    # 6. Select provider
    # --------------------------------------------------

    provider_name = (
        request.provider
        or settings.default_llm_provider
    )

    provider = get_provider(provider_name)

    # --------------------------------------------------
    # 7. Stream response
    # --------------------------------------------------

    async def generate():

        # Send status

        yield (
            "data: "
            + json.dumps(
                {
                    "type": "status",
                    "content": "Retrieving transcripts...",
                }
            )
            + "\n\n"
        )

        # Send sources

        yield (
            "data: "
            + json.dumps(
                {
                    "type": "sources",
                    "sources": sources,
                }
            )
            + "\n\n"
        )

        # Send generation status

        yield (
            "data: "
            + json.dumps(
                {
                    "type": "status",
                    "content": "Generating answer...",
                }
            )
            + "\n\n"
        )

        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        full_response = ""

        # ----------------------------------------------
        # Stream tokens from Ollama/OpenAI
        # ----------------------------------------------

        async for token in provider.stream_chat(messages):

            full_response += token

            yield (
                "data: "
                + json.dumps(
                    {
                        "type": "token",
                        "content": token,
                    }
                )
                + "\n\n"
            )

        # ----------------------------------------------
        # 8. Save assistant response
        # ----------------------------------------------

        assistant_message = Message(
            session_id=request.session_id,
            role="assistant",
            content=full_response,
            sources=sources,
        )

        db.add(assistant_message)

        # ----------------------------------------------
        # 9. Create Ship30 artifact
        # ----------------------------------------------

        if request.mode == "ship30":

            artifact = Artifact(
                message_id=assistant_message.id,
                artifact_type="markdown",
                content=full_response,
            )

            db.add(artifact)

        # ----------------------------------------------
        # 10. Commit everything
        # ----------------------------------------------

        await db.commit()

        # ----------------------------------------------
        # 11. Send artifact to frontend
        # ----------------------------------------------

        if request.mode == "ship30":

            yield (
                "data: "
                + json.dumps(
                    {
                        "type": "artifact",
                        "artifact": {
                            "type": "markdown",
                            "title": "Ship30 Growth Essay",
                            "content": full_response,
                        },
                    }
                )
                + "\n\n"
            )

        # ----------------------------------------------
        # 12. Finish stream
        # ----------------------------------------------

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )