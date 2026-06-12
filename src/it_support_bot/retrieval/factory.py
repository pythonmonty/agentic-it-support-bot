"""Retriever factory depending on configuration.

In "auto" mode the embedding endpoint is tried out once. If it is unreachable (e.g. no embedding
model pulled in Ollama), the system gracefully switches to BM25 instead of failing.
"""

from __future__ import annotations

import sys

from ..config import Settings
from ..llm.openai_client import OpenAIEmbeddingProvider
from .base import Chunk, Retriever
from .bm25_retriever import BM25Retriever
from .vector_retriever import VectorRetriever


def build_retriever(settings: Settings, chunks: list[Chunk]) -> Retriever:
    if settings.retriever == "bm25":
        return BM25Retriever(chunks)

    provider = OpenAIEmbeddingProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        model=settings.embedding_model,
    )
    try:
        return VectorRetriever(chunks, provider, cache_dir=settings.cache_dir)
    except Exception as error:
        if settings.retriever == "vector":
            raise
        print(
            f"embedding endpoint unavailable ({error.__class__.__name__}); "
            "falling back to BM25 keyword retrieval",
            file=sys.stderr,
        )
        return BM25Retriever(chunks)
