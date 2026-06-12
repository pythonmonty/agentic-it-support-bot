"""Tools exposing the unstructured Knowledge Base."""

from __future__ import annotations

from pathlib import Path

from ..retrieval.base import Retriever
from .base import Tool


class SearchKnowledgeBaseTool(Tool):
    name = "search_knowledge_base"
    description = (
        "Semantic search over internal IT knowledge base articles (procedures, "
        "troubleshooting guides, resolution steps, escalation guidance). Use it "
        "to find the documented procedure for a symptom or task. Returns the "
        "most relevant article sections with their source filenames."
    )
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Symptom, topic or task to search for.",
            },
            "top_k": {
                "type": "integer",
                "description": "Number of sections to return (default 5).",
            },
        },
        "required": ["query"],
    }

    def __init__(self, retriever: Retriever) -> None:
        self._retriever = retriever

    def run(self, query: str, top_k: int = 5) -> str:
        results = self._retriever.search(query, top_k=top_k)
        if not results:
            return "No relevant knowledge base sections found."
        return "\n\n---\n\n".join(
            f"(relevance {r.score:.3f})\n{r.chunk.display_text}" for r in results
        )


class ReadKBArticleTool(Tool):
    name = "read_kb_article"
    description = (
        "Read a complete knowledge base article by filename. Use after "
        "search_knowledge_base when you need the full procedure, not just the "
        "matching section."
    )

    def __init__(self, kb_dir: Path) -> None:
        self._kb_dir = kb_dir
        filenames = sorted(p.name for p in kb_dir.glob("*.md"))
        self.parameters = {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "enum": filenames,
                    "description": "KB article filename.",
                }
            },
            "required": ["filename"],
        }

    def run(self, filename: str) -> str:
        path = self._kb_dir / Path(filename).name
        if not path.exists():
            return f"Error: no KB article named '{filename}'."
        return path.read_text()
