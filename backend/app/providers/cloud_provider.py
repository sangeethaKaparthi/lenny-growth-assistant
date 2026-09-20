import json
import httpx

from app.config import settings
from app.providers.base import LLMProviderInterface


class OpenAIProvider(LLMProviderInterface):

    def __init__(self):
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.url = "https://api.openai.com/v1/chat/completions"

    async def chat(self, messages: list[dict], stream: bool = False):
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                self.url,
                headers=headers,
                json=payload,
            )

        response.raise_for_status()
        return response.json()

    async def stream_chat(self, messages: list[dict]):
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST",
                self.url,
                headers=headers,
                json=payload,
            ) as response:

                response.raise_for_status()

                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue

                    data = line[6:]

                    if data == "[DONE]":
                        break

                    chunk = json.loads(data)

                    content = (
                        chunk.get("choices", [{}])[0]
                        .get("delta", {})
                        .get("content")
                    )

                    if content:
                        yield content