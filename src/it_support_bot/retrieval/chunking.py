"""Markdown chunking for Knowledge Base (KB) articles.

Since articles are short and well-structured into sections (Summary, Symptoms, Resolution Steps,
etc.), we set one chunk per `##` section. This should already give us precise retrieval.

If the article sections were not so well-structured, we would need to opt for a different chunking
strategy, e.g. defining an overlap percentage for the chunks.
"""

from __future__ import annotations

import re
from pathlib import Path

from .base import Chunk

_SECTION_HEADING = re.compile(r"^## +(.+)$", re.MULTILINE)


def chunk_markdown(doc_id: str, text: str) -> list[Chunk]:
    title, body = _split_off_title(text)
    return [
        Chunk(doc_id=doc_id, title=title or doc_id, section=section, text=section_text)
        for section, section_text in _split_sections(body)
        if section_text
    ]


def _split_off_title(text: str) -> tuple[str | None, str]:
    """Return (article title, text without the title line). title is None if absent."""
    first_line, _, rest = text.partition("\n")
    if first_line.startswith("# "):
        return first_line[2:].strip(), rest
    return None, text


def _split_sections(text: str) -> list[tuple[str, str]]:
    """Split on `## ` headings into (section name, section text) pairs.

    Text before the first heading is reported as section "Header".
    """
    parts = _SECTION_HEADING.split(text)
    sections = [("Header", parts[0]), *zip(parts[1::2], parts[2::2], strict=True)]
    return [(section.strip(), body.strip()) for section, body in sections]


def load_kb_chunks(kb_dir: Path) -> list[Chunk]:
    """Return the chunks contained in the KB articles."""
    chunks: list[Chunk] = []
    for path in sorted(kb_dir.glob("*.md")):
        chunks.extend(chunk_markdown(path.name, path.read_text()))
    return chunks


def load_kb_catalog(kb_dir: Path) -> list[tuple[str, str]]:
    """(filename, article title) pairs for the system prompt."""
    catalog: list[tuple[str, str]] = []
    for path in sorted(kb_dir.glob("*.md")):
        first_line = path.read_text().splitlines()[0] if path.stat().st_size else ""
        title = first_line[2:].strip() if first_line.startswith("# ") else path.stem
        catalog.append((path.name, title))
    return catalog
