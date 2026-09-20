import asyncio
import sys
from pathlib import Path

# Add backend directory to Python path
BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.database import AsyncSessionLocal
from app.rag.retriever import retrieve_relevant_chunks


async def main():
    query = "How do successful companies find product market fit?"

    async with AsyncSessionLocal() as session:
        results = await retrieve_relevant_chunks(
            session=session,
            query=query,
        )

    print("\nRetrieved results:")
    print("=" * 80)

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print(f"Guest: {result['guest']}")
        print(f"Episode: {result['episode']}")
        print(f"Title: {result['title']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Content: {result['content'][:500]}...")
        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())