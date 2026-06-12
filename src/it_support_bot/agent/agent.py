"""Implements the agent: an LLM-driven agentic loop that integrates tools.

Each turn the model decides whether to call tools or to answer. Tool results are appended to the
conversation and the model is called again, so it can plan multi-step investigations,
e.g. search the Knowledge Base for a symptom, then query tickets for matching historical
resolutions, then cross-check a spike by month. Tool errors are given back as observations so
the model can correct itself (fix a SQL mistake, rephrase a search) instead of crashing.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from ..llm.base import ChatClient, ToolCall
from ..tools.base import Tool

# CLI progress callback: (event, detail) e.g. ("tool_call", "query_tickets ...")
EventHandler = Callable[[str, str], None]


@dataclass(frozen=True)
class ToolExecution:
    name: str
    arguments: dict
    result: str


class Agent:
    """Conversational agent with registered tools. Keeps chat history across turns."""

    def __init__(
        self,
        client: ChatClient,
        tools: list[Tool],
        system_prompt: str,
        max_steps: int = 8,
        on_event: EventHandler | None = None,
    ) -> None:
        self._client = client
        self._tools = {tool.name: tool for tool in tools}
        self._tool_specs = [tool.spec() for tool in tools]
        self._max_steps = max_steps
        self._on_event = on_event or (lambda event, detail: None)
        self._messages: list[dict] = [{"role": "system", "content": system_prompt}]

    def ask(self, question: str) -> str:
        """Answer one user question, use tools as needed."""
        self._messages.append({"role": "user", "content": question})
        for _ in range(self._max_steps):
            turn = self._client.run(self._messages, self._tool_specs)
            self._messages.append(turn.to_message())
            if not turn.tool_calls:
                return turn.content or "(no answer produced)"
            for call in turn.tool_calls:
                result = self._execute(call)
                self._messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
        return self._final_answer_without_tools()

    def _execute(self, call: ToolCall) -> str:
        tool = self._tools.get(call.name)
        if tool is None:
            return f"Error: unknown tool '{call.name}'. Available tools: {sorted(self._tools)}."
        self._on_event("tool_call", _describe(call))
        try:
            result = tool.run(**call.arguments)
        except Exception as error:
            result = f"Tool error ({error.__class__.__name__}): {error}"
        self._on_event("tool_result", result)
        return result

    def _final_answer_without_tools(self) -> str:
        self._messages.append(
            {
                "role": "user",
                "content": (
                    "Stop investigating. Give your best final answer now based on "
                    "the evidence gathered so far, and say what remains uncertain."
                ),
            }
        )
        turn = self._client.run(self._messages, tools=[])
        self._messages.append(turn.to_message())
        return turn.content or "(no answer produced)"


def _describe(call: ToolCall) -> str:
    args = ", ".join(f"{k}={v!r}" for k, v in call.arguments.items())
    return f"{call.name}({args})"
