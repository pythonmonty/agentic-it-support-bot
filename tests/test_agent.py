from it_support_bot.agent.agent import Agent
from it_support_bot.llm.base import AssistantTurn, ChatClient, ToolCall
from it_support_bot.tools.base import Tool


class EchoTool(Tool):
    name = "echo"
    description = "Echo the input."
    parameters = {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"],
    }

    def __init__(self):
        self.calls = []

    def run(self, text: str) -> str:
        self.calls.append(text)
        return f"echo: {text}"


class ScriptedClient(ChatClient):
    """Replays a fixed sequence of assistant turns and records what it was sent."""

    def __init__(self, turns):
        self._turns = list(turns)
        self.seen_messages = []

    def run(self, messages, tools):
        self.seen_messages.append([dict(m) for m in messages])
        return self._turns.pop(0)


def test_agent_executes_tool_and_returns_final_answer():
    tool = EchoTool()
    client = ScriptedClient(
        [
            AssistantTurn(
                content=None,
                tool_calls=[ToolCall(id="c1", name="echo", arguments={"text": "hi"})],
            ),
            AssistantTurn(content="Final answer based on echo."),
        ]
    )
    agent = Agent(client, [tool], system_prompt="sys", max_steps=3)

    answer = agent.ask("question?")

    assert answer == "Final answer based on echo."
    assert tool.calls == ["hi"]
    # The second completion has to see the tool result message.
    tool_messages = [m for m in client.seen_messages[1] if m["role"] == "tool"]
    assert tool_messages == [{"role": "tool", "tool_call_id": "c1", "content": "echo: hi"}]


def test_agent_feeds_tool_errors_back_to_model():
    class FailingTool(EchoTool):
        def run(self, text: str) -> str:
            raise ValueError("boom")

    client = ScriptedClient(
        [
            AssistantTurn(
                content=None,
                tool_calls=[ToolCall(id="c1", name="echo", arguments={"text": "hi"})],
            ),
            AssistantTurn(content="Recovered."),
        ]
    )
    agent = Agent(client, [FailingTool()], system_prompt="sys", max_steps=3)

    assert agent.ask("question?") == "Recovered."
    tool_messages = [m for m in client.seen_messages[1] if m["role"] == "tool"]
    assert "boom" in tool_messages[0]["content"]


def test_agent_forces_answer_when_step_budget_exhausted():
    looping_call = AssistantTurn(
        content=None,
        tool_calls=[ToolCall(id="c1", name="echo", arguments={"text": "again"})],
    )
    client = ScriptedClient(
        [looping_call, looping_call, AssistantTurn(content="Best effort answer.")]
    )
    agent = Agent(client, [EchoTool()], system_prompt="sys", max_steps=2)

    assert agent.ask("question?") == "Best effort answer."
