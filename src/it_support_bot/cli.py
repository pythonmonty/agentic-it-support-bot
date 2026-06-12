"""Command-line interface for an interactive chat over tickets and Knowledge Base."""

from __future__ import annotations

import argparse
import sys

from pydantic import ValidationError

from .agent.agent import Agent
from .agent.prompts import build_system_prompt
from .config import Settings
from .data.database import TicketDatabase
from .llm.openai_client import OpenAIChatClient
from .retrieval.chunking import load_kb_catalog, load_kb_chunks
from .retrieval.factory import build_retriever
from .tools.kb_tools import ReadKBArticleTool, SearchKnowledgeBaseTool
from .tools.sql_tool import QueryTicketsTool

_DIM = "\033[2m"
_BOLD = "\033[1m"
_RESET = "\033[0m"


def build_agent(settings: Settings, verbose: bool = False) -> Agent:
    database = TicketDatabase.from_json(settings.tickets_path)
    chunks = load_kb_chunks(settings.kb_dir)
    retriever = build_retriever(settings, chunks)
    tools = [
        QueryTicketsTool(database),
        SearchKnowledgeBaseTool(retriever),
        ReadKBArticleTool(settings.kb_dir),
    ]
    client = OpenAIChatClient(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        model=settings.chat_model,
    )
    return Agent(
        client=client,
        tools=tools,
        system_prompt=build_system_prompt(load_kb_catalog(settings.kb_dir)),
        max_steps=settings.max_agent_steps,
        on_event=_make_event_printer(verbose),
    )


def _make_event_printer(verbose: bool):
    def on_event(event: str, detail: str) -> None:
        if event == "tool_call":
            print(f"{_DIM}  → {_truncate(detail, 160)}{_RESET}")
        elif event == "tool_result" and verbose:
            print(f"{_DIM}    {_truncate(detail, 500)}{_RESET}")

    return on_event


def _truncate(text: str, limit: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="it-support-bot",
        description="Chat with IT support tickets and Knowledge Base articles.",
    )
    parser.add_argument("-q", "--question", help="Ask a single question and exit")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print tool results, not just calls"
    )
    args = parser.parse_args()

    try:
        settings = Settings.from_env()
    except ValidationError as error:
        sys.exit(f"Invalid settings:\n{error}")
    if not settings.tickets_path.exists() or not settings.kb_dir.exists():
        sys.exit(f"Dataset not found at '{settings.dataset_dir}'.")

    print(f"{_DIM}Loading dataset and building indexes...{_RESET}")
    agent = build_agent(settings, verbose=args.verbose)
    print(f"{_DIM}Ready. Model: {settings.chat_model} via {settings.llm_base_url}{_RESET}")

    if args.question:
        _ask(agent, args.question)
        return

    print("Ask about tickets and KB articles in natural language. Ctrl-D or 'exit' to quit.\n")
    while True:
        try:
            question = input(f"{_BOLD}you>{_RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break
        _ask(agent, question)


def _ask(agent: Agent, question: str) -> None:
    try:
        answer = agent.ask(question)
    except Exception as error:
        print(f"\n[error] LLM call failed: {error}", file=sys.stderr)
        return
    print(f"\n{_BOLD}bot>{_RESET} {answer}\n")


if __name__ == "__main__":
    main()
