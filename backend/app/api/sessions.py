from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import Message, Session
from app.models.schemas import SessionCreate


router = APIRouter(
    prefix="/api/sessions",
    tags=["Sessions"],
)


@router.post("")
async def create_session(
    request: SessionCreate,
    db: AsyncSession = Depends(get_db),
):
    new_session = Session(
        title=request.title.strip() or "New conversation"
    )

    db.add(new_session)

    await db.commit()
    await db.refresh(new_session)

    return {
        "id": str(new_session.id),
        "title": new_session.title,
        "created_at": new_session.created_at,
        "updated_at": new_session.updated_at,
    }


@router.get("/{session_id}")
async def get_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Session).where(Session.id == session_id)
    )

    session = result.scalar_one_or_none()

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    message_result = await db.execute(
        select(Message)
        .where(Message.session_id == session.id)
        .order_by(Message.created_at.asc())
    )

    messages = message_result.scalars().all()

    return {
        "id": str(session.id),
        "title": session.title,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "messages": [
            {
                "id": str(message.id),
                "role": message.role,
                "content": message.content,
                "sources": message.sources or [],
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }