from abc import ABC, abstractmethod
from typing import AsyncIterator


class LLMProviderInterface(ABC):

    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        stream: bool = False,
    ):
        pass

    @abstractmethod
    async def stream_chat(
        self,
        messages: list[dict],
    ) -> AsyncIterator[str]:
        pass