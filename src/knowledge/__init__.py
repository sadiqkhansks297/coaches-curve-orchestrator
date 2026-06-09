"""Knowledge layer factory."""

from pathlib import Path

from src.config import config
from src.knowledge.base import KnowledgeStore
from src.knowledge.local_store import LocalKnowledgeStore


def get_knowledge_store() -> KnowledgeStore:
    if config.KNOWLEDGE_PROVIDER == "local":
        return LocalKnowledgeStore(config.BRAIN_DIR)
    # Production: elif config.KNOWLEDGE_PROVIDER == "gbrain": return GBrainStore(...)
    raise ValueError(f"Unknown KNOWLEDGE_PROVIDER: {config.KNOWLEDGE_PROVIDER}")
