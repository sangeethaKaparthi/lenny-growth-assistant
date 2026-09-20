import asyncio
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.providers.ollama_provider import OllamaProvider


async def main():

    provider = OllamaProvider()

    messages = [
        {
            "role": "user",
            "content": "Explain product-market fit in two simple sentences.",
        }
    ]

    response = await provider.chat(
        messages=messages,
        stream=False,
    )

    print("\nOllama response:")
    print("=" * 80)

    print(response)


if __name__ == "__main__":
    asyncio.run(main())