"""Application settings, sourced from environment variables (if set) or defaults (if environment
variables are not set).

Defaults target a locally running Ollama server, which exposes an OpenAI-compatible API
free of charge. Any OpenAI-compatible endpoint works.

Settings is a Pydantic model so misconfiguration fails at startup instead of silently.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

RetrieverKind = Literal["auto", "vector", "bm25"]


class Settings(BaseModel):
    model_config = ConfigDict(frozen=True)

    dataset_dir: Path = Path("it-support-dataset")
    cache_dir: Path = Path(".cache")
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = "ollama"
    chat_model: str = "llama3.1:8b"
    embedding_model: str = "nomic-embed-text"
    retriever: RetrieverKind = "auto"
    max_agent_steps: int = Field(default=8, ge=1)

    @classmethod
    def from_env(cls) -> Settings:
        env = {
            "dataset_dir": os.getenv("DATASET_DIR"),
            "cache_dir": os.getenv("CACHE_DIR"),
            "llm_base_url": os.getenv("LLM_BASE_URL"),
            "llm_api_key": os.getenv("LLM_API_KEY"),
            "chat_model": os.getenv("LLM_CHAT_MODEL"),
            "embedding_model": os.getenv("LLM_EMBEDDING_MODEL"),
            "retriever": os.getenv("RETRIEVER"),
            "max_agent_steps": os.getenv("MAX_AGENT_STEPS"),
        }
        # Unset variable values use default values.
        return cls.model_validate({k: v for k, v in env.items() if v is not None})

    @property
    def kb_dir(self) -> Path:
        return self.dataset_dir / "kb"

    @property
    def tickets_path(self) -> Path:
        return self.dataset_dir / "tickets.json"
