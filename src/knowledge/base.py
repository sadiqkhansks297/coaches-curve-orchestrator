"""Knowledge store interface — swap implementations via config."""

from abc import ABC, abstractmethod


class KnowledgeStore(ABC):
    @abstractmethod
    def search(self, query: str, max_results: int = 3) -> str:
        """Return relevant context as a single string for LLM injection."""

    @abstractmethod
    def list_sources(self) -> list[str]:
        """Return all available knowledge source paths."""
