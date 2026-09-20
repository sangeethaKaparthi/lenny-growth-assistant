import json
import httpx

from app.config import settings
from app.providers.base import LLMProviderInterface


class OllamaProvider(LLMProviderInterface):

    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model

    async def chat(
        self,
        messages: list[dict],
        stream: bool = False,
    ):
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                url,
                json=payload,
            )

            response.raise_for_status()

            if stream:
                return response.aiter_lines()

            return response.json()

    async def stream_chat(
        self,
        messages: list[dict],
    ):
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST",
                url,
                json=payload,
            ) as response:

                response.raise_for_status()

                async for line in response.aiter_lines():

                    if not line:
                        continue

                    data = json.loads(line)

                    if data.get("done"):
                        break

                    message = data.get("message", {})

                    content = message.get("content", "")

                    if content:
                        yield content