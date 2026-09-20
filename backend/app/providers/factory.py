from app.providers.ollama_provider import OllamaProvider
from app.providers.cloud_provider import OpenAIProvider


def get_provider(provider_name: str):

    if provider_name == "ollama":
        return OllamaProvider()

    if provider_name == "openai":
        return OpenAIProvider()

    raise ValueError(f"Unsupported provider: {provider_name}")