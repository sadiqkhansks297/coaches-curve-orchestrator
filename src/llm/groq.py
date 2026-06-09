"""Groq provider — free tier, fast inference."""

from groq import Groq

from src.config import config
from src.llm.base import LLMProvider


class GroqProvider(LLMProvider):
    def __init__(self):
        if not config.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not set. Get one free at https://console.groq.com/keys"
            )
        self.client = Groq(api_key=config.GROQ_API_KEY)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=2048,
        )
        return response.choices[0].message.content or ""
