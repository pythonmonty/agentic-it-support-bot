"""Retrieval ABCs shared by all retriever implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    """A retrievable chunk (unit) of text. In this case one section of a KB article."""

    doc_id: str  # KB filename
    title: str  # article title
    section: str  # section title in the article
    text: str

    @property
    def display_text(self) -> str:
        return f"[{self.doc_id}] {self.title} — {self.section}\n{self.text}"


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


class Retriever(ABC):
    """Semantic or keyword search over a fixed number of chunks."""

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        """Return the top_k most relevant chunks, best matches first."""
