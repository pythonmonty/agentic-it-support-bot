"""In-memory SQLite database built from the file tickets.json.

Tickets are loaded into a normalized schema (tags and work notes in child
tables) so the agent can answer aggregate and relational questions with plain
SQL. Queries from the agent run behind a SQLite authorizer that permits reads
only, so a hallucinated UPDATE/DROP can never mutate data.

The Pydantic models in models.py are the single source of truth for the
schema: the CREATE TABLE DDL, the INSERT statement, and the LLM-facing
SCHEMA_DOC are all generated from their fields (SQL types from annotations,
allowed values from Literal types, column comments from Field descriptions).
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .helpers import (
    _NON_COLUMN_FIELDS,
    _column_doc,
    _column_fields,
    _create_sql_tables_instructions,
    _insert_into_tickets_sql_instruction,
    _work_note_columns,
)
from .models import Ticket

# Usage guidance for the LLM, knowledge about the data.
_DOC_NOTES = """\
Notes:
- Timestamps are ISO strings; use strftime('%Y-%m', created_at) for monthly grouping.
- Descriptions state symptoms, not causes: the root cause is only visible in
  root_cause/resolution of resolved tickets. Use LIKE '%...%' for text matching."""


def build_schema_doc() -> str:
    """LLM-facing schema documentation, generated from the Pydantic models."""
    lines = ["Table: tickets"]
    for name, field in _column_fields().items():
        lines += _column_doc(name, field, primary_key=(name == "ticket_id"))
    lines += [
        "",
        "Table: ticket_tags",
        f"{'  ticket_id TEXT, tag TEXT':<34}-- one row per tag",
        "",
        "Table: ticket_work_notes",
        f"  {_work_note_columns()}  -- only complex tickets have notes",
        "",
        _DOC_NOTES,
    ]
    return "\n".join(lines)


# Schema is handed to the LLM so it can write correct SQL.
SCHEMA_DOC = build_schema_doc()

_READ_ACTIONS = {
    sqlite3.SQLITE_SELECT,
    sqlite3.SQLITE_READ,
    sqlite3.SQLITE_FUNCTION,
    sqlite3.SQLITE_RECURSIVE,
}


def _read_only_authorizer(action: int, *_args) -> int:
    return sqlite3.SQLITE_OK if action in _READ_ACTIONS else sqlite3.SQLITE_DENY


class TicketDatabase:
    """Owns the SQLite connection and enforces read-only access for queries."""

    MAX_ROWS = 50

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    @classmethod
    def from_json(cls, tickets_path: Path) -> TicketDatabase:
        tickets = [Ticket.model_validate(record) for record in json.loads(tickets_path.read_text())]
        connection = sqlite3.connect(":memory:", check_same_thread=False)
        connection.executescript(_create_sql_tables_instructions())
        for ticket in tickets:
            connection.execute(
                _insert_into_tickets_sql_instruction(),
                {
                    **ticket.model_dump(exclude=_NON_COLUMN_FIELDS),
                    "created_at": ticket.created_at.isoformat(),
                },
            )
            connection.executemany(
                "INSERT INTO ticket_tags VALUES (?, ?)",
                [(ticket.ticket_id, tag) for tag in ticket.tags],
            )
            connection.executemany(
                "INSERT INTO ticket_work_notes VALUES (?, ?, ?)",
                [
                    (ticket.ticket_id, note.noted_at.isoformat(), note.note)
                    for note in ticket.work_notes
                ],
            )
        connection.commit()
        connection.set_authorizer(_read_only_authorizer)
        return cls(connection)

    def query(self, sql: str) -> tuple[list[str | None], list[Any], bool]:
        """Execute a read-only query.

        Returns (column_names, rows, truncated).
        Raises sqlite3.Error for invalid or non-read SQL.
        """
        cursor = self._connection.execute(sql)
        columns = [d[0] for d in cursor.description or []]
        rows = cursor.fetchmany(self.MAX_ROWS + 1)
        truncated = len(rows) > self.MAX_ROWS
        return columns, rows[: self.MAX_ROWS], truncated
