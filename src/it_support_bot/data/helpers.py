"""Helper functions that bridge the `Tickets` Pydantic model with the SQL commands
and SQL schema"""

from __future__ import annotations

import textwrap
import typing
from datetime import datetime
from types import NoneType, UnionType
from typing import Literal, get_args, get_origin

from pydantic.fields import FieldInfo

from .models import Ticket, WorkNote

# Ticket fields that are not columns of the `tickets` table.
# tags and work_notes live in separate tables and language is constant ('en')
_NON_COLUMN_FIELDS = {"tags", "work_notes", "language"}


def _create_sql_tables_instructions() -> str:
    ticket_columns = ",\n    ".join(
        f"{name} {_sql_type(field.annotation)}" + (" PRIMARY KEY" if name == "ticket_id" else "")
        for name, field in _column_fields().items()
    )
    return (
        f"CREATE TABLE tickets (\n    {ticket_columns}\n);\n"
        "CREATE TABLE ticket_tags (ticket_id TEXT, tag TEXT);\n"
        f"CREATE TABLE ticket_work_notes ({_work_note_columns()});"
    )


def _insert_into_tickets_sql_instruction() -> str:
    return "INSERT INTO tickets VALUES (" + ", ".join(f":{name}" for name in _column_fields()) + ")"


def _column_doc(name: str, field: FieldInfo, *, primary_key: bool = False) -> list[str]:
    declaration = f"  {name} {_sql_type(field.annotation)}{' PRIMARY KEY' if primary_key else ''}"
    base = _base_type(field.annotation)
    comments = []
    if get_origin(base) is Literal:
        comments.append(" | ".join(get_args(base)))
    if field.description:
        comments.append(field.description)
    if not comments:
        return [declaration]
    wrapped = textwrap.wrap("; ".join(comments), width=62)
    lines = [f"{declaration:<34}-- {wrapped[0]}"]
    lines += [f"{'':<34}-- {continuation}" for continuation in wrapped[1:]]
    return lines


def _column_fields() -> dict[str, FieldInfo]:
    return {
        name: field for name, field in Ticket.model_fields.items() if name not in _NON_COLUMN_FIELDS
    }


def _base_type(annotation: object) -> object:
    """Unwrap `X | None` to X."""
    if get_origin(annotation) in (UnionType, typing.Union):
        return next(a for a in get_args(annotation) if a is not NoneType)
    return annotation


def _sql_type(annotation: object) -> str:
    base = _base_type(annotation)
    if get_origin(base) is Literal:
        return "TEXT"
    return {str: "TEXT", datetime: "TEXT", int: "INTEGER", float: "REAL"}[base]


def _work_note_columns() -> str:
    columns = ", ".join(
        f"{name} {_sql_type(field.annotation)}" for name, field in WorkNote.model_fields.items()
    )
    return f"ticket_id TEXT, {columns}"
