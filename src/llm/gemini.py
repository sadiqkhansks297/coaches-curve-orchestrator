"""Google Gemini provider — free tier via AI Studio."""

import google.generativeai as genai

from src.config import config
from src.llm.base import LLMProvider


class GeminiProvider(LLMProvider):
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not set. Get one free at https://aistudio.google.com/apikey"
            )
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"
        response = self.model.generate_content(prompt)
        return response.text
