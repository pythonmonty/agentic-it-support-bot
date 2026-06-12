import pytest
from pydantic import ValidationError

from it_support_bot.data.models import Ticket

RECORD = {
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
    "status": "open",
    "assigned_team": "Network",
    "tags": ["vpn"],
}


def test_valid_record_parses_with_defaults():
    ticket = Ticket.model_validate(RECORD)
    assert ticket.created_at.year == 2025
    assert ticket.root_cause is None
    assert ticket.reopened_count == 0
    assert ticket.work_notes == []


def test_empty_string_root_cause_becomes_none():
    ticket = Ticket.model_validate({**RECORD, "root_cause": "", "resolution": ""})
    assert ticket.root_cause is None
    assert ticket.resolution is None


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("priority", "urgent"),
        ("status", "done"),
        ("department", "Unknown Dept"),
        ("created_at", "not-a-date"),
    ],
)
def test_invalid_values_are_rejected(field, bad_value):
    with pytest.raises(ValidationError):
        Ticket.model_validate({**RECORD, field: bad_value})
