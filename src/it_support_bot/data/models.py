"""Pydantic models for the SQLite ticket schema.

`Ticket` is the validated form of a single record in `tickets.json`.

The `Ticket` model is used to generate the schema that is passed to the LLM, as well as
for the CREATE TABLE statements in database.py.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Category = Literal["access", "hardware", "software", "network", "account", "security"]
Priority = Literal["low", "medium", "high", "critical"]
ImpactLevel = Literal["single_user", "team", "department", "company_wide"]
ApplicationCriticality = Literal["low", "medium", "high", "regulatory"]
Status = Literal["open", "in_progress", "resolved", "closed", "reopened"]
Department = Literal[
    "Private Banking",
    "Investment Advisory",
    "Trading",
    "Operations",
    "Compliance",
    "Risk Management",
    "Technology",
    "Finance",
    "Executive Office",
    "Human Resources",
]
Product = Literal[
    "VPN",
    "MFA",
    "SSO",
    "Outlook",
    "Microsoft Teams",
    "Jira",
    "Azure AD",
    "Corporate WiFi",
    "Endpoint Management",
    "Trading Platform",
    "Portfolio Management System",
    "Client Reporting Portal",
    "Market Data Platform",
    "Core Banking Portal",
    "Document Management System",
    "Identity Governance Platform",
    "Privileged Access Management",
]


class WorkNote(BaseModel):
    """One row in `ticket_work_notes`."""

    model_config = ConfigDict(frozen=True)

    noted_at: datetime = Field(alias="at", description="ISO timestamp of the note")
    note: str = Field(description="free-text update by the support team")


class Ticket(BaseModel):
    """One row in `tickets`."""

    model_config = ConfigDict(frozen=True)

    ticket_id: str = Field(description="e.g. 'T-1001'")
    created_at: datetime = Field(description="ISO timestamp, data spans 2025-01 .. 2025-12")
    requester_user: str = Field(description="e.g. 'j.smith'")
    department: Department
    language: str = "en"
    category: Category
    product: Product
    priority: Priority
    impact_level: ImpactLevel
    application_criticality: ApplicationCriticality
    subject: str = Field(description="short symptom summary written by the user")
    description: str = Field(description="free text, symptoms only (typos, abbreviations)")
    status: Status
    root_cause: str | None = Field(default=None, description="NULL unless resolved/closed/reopened")
    resolution: str | None = Field(default=None, description="NULL unless resolved/closed/reopened")
    resolution_time_hours: float | None = Field(
        default=None, description="NULL unless resolved/closed/reopened"
    )
    assigned_team: str
    reopened_count: int = Field(default=0, description="0 for most tickets")
    tags: list[str] = []
    work_notes: list[WorkNote] = []

    @field_validator("root_cause", "resolution", mode="before")
    @classmethod
    def empty_string_is_null(cls, value: object) -> object:
        """Unresolved tickets use "" in the source JSON; store NULL instead."""
        return None if value == "" else value
