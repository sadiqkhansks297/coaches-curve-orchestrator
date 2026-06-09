"""
Local markdown knowledge store (prototype).

Production replacement: GBrainStore — see docs/PRODUCTION_MIGRATION.md
"""

import re
from pathlib import Path

from src.knowledge.base import KnowledgeStore


class LocalKnowledgeStore(KnowledgeStore):
    """Search markdown files in brain/ using keyword relevance scoring."""

    def __init__(self, brain_dir: Path):
        self.brain_dir = brain_dir
        self._documents: list[tuple[str, str]] = []
        self._load_documents()

    def _load_documents(self) -> None:
        if not self.brain_dir.exists():
            return
        for path in sorted(self.brain_dir.rglob("*.md")):
            rel = str(path.relative_to(self.brain_dir))
            self._documents.append((rel, path.read_text(encoding="utf-8")))

    def list_sources(self) -> list[str]:
        return [rel for rel, _ in self._documents]

    def search(self, query: str, max_results: int = 3) -> str:
        if not self._documents:
            return "No knowledge base content found."

        query_terms = set(re.findall(r"\w+", query.lower()))
        scored: list[tuple[float, str, str]] = []

        for rel, content in self._documents:
            content_lower = content.lower()
            score = sum(content_lower.count(term) for term in query_terms)
            # Boost title/filename matches
            score += sum(3 for term in query_terms if term in rel.lower())
            if score > 0:
                scored.append((score, rel, content))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:max_results]

        if not top:
            # Fallback: return first document
            rel, content = self._documents[0]
            return f"--- {rel} ---\n{content[:2000]}"

        parts = []
        for _, rel, content in top:
            parts.append(f"--- {rel} ---\n{content[:2000]}")
        return "\n\n".join(parts)
