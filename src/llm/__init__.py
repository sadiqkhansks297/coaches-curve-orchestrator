"""LLM provider factory."""

from src.config import config
from src.llm.base import LLMProvider
from src.llm.gemini import GeminiProvider
from src.llm.groq import GroqProvider


def get_llm_provider() -> LLMProvider:
    if config.LLM_PROVIDER == "gemini":
        return GeminiProvider()
    if config.LLM_PROVIDER == "groq":
        return GroqProvider()
    # Production: elif config.LLM_PROVIDER == "claude": return ClaudeProvider(...)
    raise ValueError(f"Unknown LLM_PROVIDER: {config.LLM_PROVIDER}")
