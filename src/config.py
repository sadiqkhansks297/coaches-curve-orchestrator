"""Central configuration — all settings from environment variables."""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass  # dotenv optional until pip install

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Config:
    # LLM
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Knowledge
    KNOWLEDGE_PROVIDER: str = os.getenv("KNOWLEDGE_PROVIDER", "local")
    BRAIN_DIR: Path = PROJECT_ROOT / os.getenv("BRAIN_DIR", "brain")

    # Telegram (Step 2)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    # Production placeholders
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    MANUS_API_KEY: str = os.getenv("MANUS_API_KEY", "")
    GBRAIN_URL: str = os.getenv("GBRAIN_URL", "")
    GBRAIN_TOKEN: str = os.getenv("GBRAIN_TOKEN", "")


config = Config()
