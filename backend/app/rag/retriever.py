from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import TranscriptChunk
from app.rag.embeddings import embed_text


DEFAULT_TOP_K = 5
DEFAULT_SIMILARITY_THRESHOLD = 0.65


async def retrieve_relevant_chunks(
    session: AsyncSession,
    query: str,
    top_k: int = DEFAULT_TOP_K,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
) -> list[dict]:
    """
    Retrieve the most relevant transcript chunks for a user query.

    Steps:
    1. Convert the user query into an embedding.
    2. Search transcript chunks using pgvector cosine similarity.
    3. Return the top relevant chunks above the similarity threshold.
    """

    # 1. Create embedding for the user's question
    query_embedding = embed_text(query)

    # 2. Calculate cosine distance
    distance = TranscriptChunk.embedding.cosine_distance(
        query_embedding
    )

    # Convert cosine distance into similarity.
    # similarity = 1 - cosine_distance
    similarity = 1 - distance

    # 3. Search PostgreSQL using pgvector
    statement = (
        select(
            TranscriptChunk,
            similarity.label("similarity"),
        )
        .where(similarity >= threshold)
        .order_by(distance)
        .limit(top_k)
    )

    result = await session.execute(statement)

    rows = result.all()

    # 4. Convert database results into a simple structure
    chunks = []

    for chunk, score in rows:
        chunks.append(
            {
                "id": str(chunk.id),
                "episode": chunk.episode,
                "guest": chunk.guest,
                "title": chunk.title,
                "timestamp": chunk.timestamp,
                "topic": chunk.topic,
                "content": chunk.content,
                "similarity": float(score),
            }
        )

    return chunks