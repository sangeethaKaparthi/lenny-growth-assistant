import asyncio
import re
import sys
from pathlib import Path

from sqlalchemy import delete

ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
    
from app.database import AsyncSessionLocal, init_database
from app.models.db_models import TranscriptChunk
from app.rag.embeddings import embed_texts


TRANSCRIPTS_DIR = (
    ROOT_DIR / "data" / "episodes"
)


def extract_frontmatter(content: str) -> tuple[dict, str]:
    metadata = {}

    if not content.startswith("---"):
        return metadata, content

    parts = content.split("---", 2)

    if len(parts) < 3:
        return metadata, content

    frontmatter = parts[1]
    transcript = parts[2]

    for line in frontmatter.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip()
        value = value.strip().strip('"')

        metadata[key] = value

    return metadata, transcript


def clean_text(text: str) -> str:
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def extract_timestamp(text: str) -> str | None:
    match = re.search(
        r"\(?(\d{1,2}:\d{2}(?::\d{2})?)\)?",
        text,
    )

    if match:
        return match.group(1)

    return None


def chunk_text(
    text: str,
    chunk_words: int = 650,
    overlap_words: int = 100,
) -> list[str]:

    words = text.split()

    if not words:
        return []

    chunks = []

    start = 0

    while start < len(words):
        end = min(
            start + chunk_words,
            len(words),
        )

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap_words

    return chunks


def read_transcripts():
    files = list(
        TRANSCRIPTS_DIR.glob(
            "**/transcript.md"
        )
    )

    print(
        f"Found {len(files)} transcript files."
    )

    for filepath in files:

        raw = filepath.read_text(
            encoding="utf-8"
        )

        metadata, transcript = (
            extract_frontmatter(raw)
        )

        transcript = clean_text(transcript)

        chunks = chunk_text(transcript)

        guest = metadata.get(
            "guest",
            filepath.parent.name,
        )

        title = metadata.get(
            "title",
            guest,
        )

        episode = filepath.parent.name

        for chunk in chunks:

            timestamp = extract_timestamp(
                chunk
            )

            yield {
                "episode": episode,
                "guest": guest,
                "title": title,
                "timestamp": timestamp,
                "topic": None,
                "content": chunk,
            }


async def ingest():

    await init_database()

    records = list(read_transcripts())

    print(
        f"Created {len(records)} transcript chunks."
    )

    if not records:
        print("No transcript chunks found.")
        return

    texts = [
        record["content"]
        for record in records
    ]

    print("Generating embeddings...")

    embeddings = embed_texts(texts)

    print("Saving chunks to PostgreSQL...")

    async with AsyncSessionLocal() as session:

        await session.execute(
            delete(TranscriptChunk)
        )

        batch = []

        for record, embedding in zip(
            records,
            embeddings,
        ):
            batch.append(
                TranscriptChunk(
                    episode=record["episode"],
                    guest=record["guest"],
                    title=record["title"],
                    timestamp=record["timestamp"],
                    topic=record["topic"],
                    content=record["content"],
                    embedding=embedding,
                )
            )

            if len(batch) >= 100:

                session.add_all(batch)

                await session.commit()

                batch = []

                print(
                    "Inserted 100 chunks..."
                )

        if batch:
            session.add_all(batch)
            await session.commit()

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    asyncio.run(ingest())