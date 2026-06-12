"""BM25 retriever backed by the rank-bm25 package.

Keyword search is used as fallback when no embedding endpoint is available, so the system
always runs. Retrieval quality using keyword search with BM25 should be good enough for this
case because KB articles share the same vocabulary as symptoms mentioned in the tickets.
"""

from __future__ import annotations

import re

from rank_bm25 import BM25Okapi

from .base import Chunk, Retriever, SearchResult

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class BM25Retriever(Retriever):
    def __init__(self, chunks: list[Chunk]) -> None:
        self._chunks = chunks
        self._bm25 = BM25Okapi([_tokenize(chunk.display_text) for chunk in chunks])

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        scores = self._bm25.get_scores(_tokenize(query))
        ranked = sorted(
            zip(self._chunks, scores, strict=True), key=lambda pair: pair[1], reverse=True
        )
        return [
            SearchResult(chunk=chunk, score=float(score))
            for chunk, score in ranked[:top_k]
            if score > 0
        ]
