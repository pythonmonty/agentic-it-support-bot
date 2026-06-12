"""Embedding-based retriever: numpy cosine similarity with an on-disk cache.

The corpus of KB articles is small (~175 section chunks), so brute-force search is one matrix
multiplication against the pre-normalized corpus matrix. This is simpler and faster than a
vector database would be at this scale. However, it's worth mentioning that it would make sense
to implement a vector database in case the corpus grows.

Embeddings are cached on disk, so re-runs do not generate extra cost nothing since they
are only re-embedded if they changed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from ..llm.base import EmbeddingProvider
from .base import Chunk, Retriever, SearchResult


class VectorRetriever(Retriever):
    def __init__(
        self,
        chunks: list[Chunk],
        provider: EmbeddingProvider,
        cache_dir: Path | None = None,
    ) -> None:
        self._chunks = chunks
        self._provider = provider

        # Where the embeddings are cached on disk. Add model_id since vectors generated
        # by different models are incompatible.
        self._cache_path = (
            cache_dir / f"embeddings-{_rename_filesystem_safe(provider.model_id)}.json"
            if cache_dir
            else None
        )

        vectors = self._embed_corpus([c.display_text for c in chunks])
        self._corpus_matrix = _normalize_rows(np.asarray(vectors, dtype=np.float32))

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        query_vector = np.asarray(self._provider.embed([query]), dtype=np.float32)
        # Since the corpus and the query are L2-normalized, the dot product is cosine similarity.
        scores = self._corpus_matrix @ _normalize_rows(query_vector)[0]
        best = np.argsort(scores)[::-1][:top_k]
        return [SearchResult(chunk=self._chunks[i], score=float(scores[i])) for i in best]

    def _embed_corpus(self, texts: list[str]) -> list[list[float]]:
        cache = self._load_cache()
        keys = [_content_key(t) for t in texts]
        missing = [(key, text) for key, text in zip(keys, texts, strict=True) if key not in cache]
        if missing:
            vectors = self._provider.embed([text for _, text in missing])
            cache.update({key: vector for (key, _), vector in zip(missing, vectors, strict=True)})
            self._save_cache(cache)
        return [cache[key] for key in keys]

    def _load_cache(self) -> dict[str, list[float]]:
        if self._cache_path and self._cache_path.exists():
            return json.loads(self._cache_path.read_text())
        return {}

    def _save_cache(self, cache: dict[str, list[float]]) -> None:
        if self._cache_path:
            self._cache_path.parent.mkdir(parents=True, exist_ok=True)
            self._cache_path.write_text(json.dumps(cache))


def _content_key(text: str) -> str:
    """SHA-256 hash of the text chunk. Hashing the content means the cache gets invalidated if
    a KB article and its chunks gets edited since they hash differently. So exactly those chunks
    and nothing more, gets re-embedded.
    """
    return hashlib.sha256(text.encode()).hexdigest()


def _rename_filesystem_safe(model_id: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in model_id)


def _normalize_rows(matrix: np.ndarray) -> np.ndarray:
    """L2-normalize each row; zero vectors stay zero instead of dividing by 0."""
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.maximum(norms, np.finfo(matrix.dtype).tiny)
