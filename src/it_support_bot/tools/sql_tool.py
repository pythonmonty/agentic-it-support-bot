"""Tool exposing the ticket database through read-only SQL."""

from __future__ import annotations

import json

from ..data.database import SCHEMA_DOC, TicketDatabase
from .base import Tool


class QueryTicketsTool(Tool):
    name = "query_tickets"
    description = (
        "Run a read-only SQL (SQLite) SELECT query against the historical support "
        "ticket database. Use it for counts, trends over time, filtering by "
        "department/product/priority, finding similar past tickets and how they "
        "were resolved.\n\nSchema:\n" + SCHEMA_DOC
    )
    parameters = {
        "type": "object",
        "properties": {
            "sql": {
                "type": "string",
                "description": "A single SQLite SELECT statement.",
            }
        },
        "required": ["sql"],
    }

    def __init__(self, database: TicketDatabase) -> None:
        self._database = database

    def run(self, sql: str) -> str:
        columns, rows, truncated = self._database.query(sql)
        if not rows:
            return "Query returned no rows."
        result = {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
        }
        if truncated:
            result["note"] = (
                f"Output truncated to {self._database.MAX_ROWS} rows; "
                "use aggregation or a WHERE clause to narrow down."
            )
        return json.dumps(result, default=str)
