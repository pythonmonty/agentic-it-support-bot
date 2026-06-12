import json
import sqlite3

import pytest

from it_support_bot.data.database import TicketDatabase

TICKETS = [
    {
        "ticket_id": "T-1",
        "created_at": "2025-03-01T09:00:00",
        "requester_user": "a.user",
        "department": "Trading",
        "language": "en",
        "category": "network",
        "product": "VPN",
        "priority": "high",
        "impact_level": "single_user",
        "application_criticality": "high",
        "subject": "VPN broken",
        "description": "vpn wont connect, cert error",
        "status": "resolved",
        "root_cause": "Expired VPN certificate",
        "resolution": "Renewed certificate.",
        "resolution_time_hours": 2.0,
        "assigned_team": "Network",
        "tags": ["vpn", "certificate"],
        "work_notes": [{"at": "2025-03-01T10:00:00", "note": "checked cert store"}],
    },
    {
        "ticket_id": "T-2",
        "created_at": "2025-06-10T10:00:00",
        "requester_user": "b.user",
        "department": "Compliance",
        "language": "en",
        "category": "access",
        "product": "MFA",
        "priority": "medium",
        "impact_level": "single_user",
        "application_criticality": "medium",
        "subject": "Cannot finish MFA setup",
        "description": "qr code does nothing",
        "status": "open",
        "assigned_team": "IAM",
        "tags": ["mfa"],
    },
]


@pytest.fixture()
def database(tmp_path):
    path = tmp_path / "tickets.json"
    path.write_text(json.dumps(TICKETS))
    return TicketDatabase.from_json(path)


def test_select_with_joins_and_aggregates(database):
    columns, rows, truncated = database.query(
        "SELECT t.ticket_id, COUNT(g.tag) AS n FROM tickets t "
        "JOIN ticket_tags g ON g.ticket_id = t.ticket_id "
        "WHERE t.product = 'VPN' GROUP BY t.ticket_id"
    )
    assert columns == ["ticket_id", "n"]
    assert rows == [("T-1", 2)]
    assert not truncated


def test_unresolved_ticket_has_null_root_cause(database):
    _, rows, _ = database.query(
        "SELECT root_cause, resolution_time_hours FROM tickets WHERE ticket_id = 'T-2'"
    )
    assert rows == [(None, None)]


@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO tickets (ticket_id) VALUES ('T-666')",
        "UPDATE tickets SET priority = 'low'",
        "DELETE FROM tickets",
        "DROP TABLE tickets",
    ],
)
def test_write_statements_are_rejected(database, sql):
    with pytest.raises(sqlite3.Error):
        database.query(sql)


def test_schema_doc_is_generated_from_the_model(database):
    from it_support_bot.data.database import SCHEMA_DOC
    from it_support_bot.data.models import Ticket

    # Check if every database column appears in the doc with its SQL type.
    assert "ticket_id TEXT PRIMARY KEY" in SCHEMA_DOC
    assert "resolution_time_hours REAL" in SCHEMA_DOC
    assert "reopened_count INTEGER" in SCHEMA_DOC
    for name in Ticket.model_fields:
        if name not in ("tags", "work_notes", "language"):
            assert name in SCHEMA_DOC

    assert "low | medium | high | critical" in SCHEMA_DOC
    assert "NULL unless resolved/closed/reopened" in SCHEMA_DOC

    columns, _, _ = database.query("SELECT * FROM tickets LIMIT 1")
    for column in columns:
        assert column in SCHEMA_DOC
