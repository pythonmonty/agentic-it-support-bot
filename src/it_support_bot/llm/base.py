"""Abstract interfaces for LLM chat completion and text embedding providers.

The agent depends only on these abstractions, so the concrete provider is easily configurable
without touching the `Agent` class.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ToolCall:
    """A tool invocation requested by the model."""

    id: str
    name: str
    arguments: dict


@dataclass(frozen=True)
class AssistantTurn:
    """One assistant turn (response): free text, tool-call requests, or both."""

    content: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)

    def to_message(self) -> dict:
        """Render message as an OpenAI-style assistant message for the conversation history."""
        message: dict = {"role": "assistant", "content": self.content or ""}

        if self.tool_calls:
            message["tool_calls"] = [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.name,
                        "arguments": json.dumps(call.arguments),
                    },
                }
                for call in self.tool_calls
            ]
        return message


class ChatClient(ABC):
    """A chat client model capable of tool calling."""

    @abstractmethod
    def run(self, messages: list[dict], tools: list[dict]) -> AssistantTurn:
        """Run chat client with OpenAI-style messages and tools."""


class EmbeddingProvider(ABC):
    """A model that embeds text into dense vector space."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of text, preserving its order."""

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Model identifier for the on-disk embedding cache."""
