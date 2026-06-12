"""Concrete LLM chat client implementation backed by the OpenAI API, based off of ABC `ChatClient`.

Works against any OpenAI-compatible endpoint. The default configuration points at a local
Ollama server.
"""

from __future__ import annotations

import json

from openai import OpenAI

from .base import AssistantTurn, ChatClient, EmbeddingProvider, ToolCall


class OpenAIChatClient(ChatClient):
    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self._client = OpenAI(base_url=base_url, api_key=api_key)
        self._model = model

    def run(self, messages: list[dict], tools: list[dict]) -> AssistantTurn:
        kwargs: dict = {"model": self._model, "messages": messages}
        if tools:
            kwargs["tools"] = tools
        response = self._client.chat.completions.create(**kwargs)
        message = response.choices[0].message
        tool_calls = [
            ToolCall(
                id=call.id,
                name=call.function.name,
                arguments=_parse_arguments(call.function.arguments),
            )
            for call in (message.tool_calls or [])
        ]
        return AssistantTurn(content=message.content, tool_calls=tool_calls)


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self._client = OpenAI(base_url=base_url, api_key=api_key)
        self._model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self._client.embeddings.create(model=self._model, input=texts)
        # The API guarantees an index per item. Sort just in case.
        ordered = sorted(response.data, key=lambda item: item.index)
        return [item.embedding for item in ordered]

    @property
    def model_id(self) -> str:
        return self._model


def _parse_arguments(raw: str | None) -> dict:
    """Sometimes local models might return malformed JSONs. We send it to the tool layer
    instead of crashing so that the agent can retry.
    """
    try:
        parsed = json.loads(raw or "{}")
        return parsed if isinstance(parsed, dict) else {"value": parsed}
    except json.JSONDecodeError:
        return {"malformed_arguments": raw}
