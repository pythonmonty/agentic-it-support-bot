import pytest
from pydantic import ValidationError

from it_support_bot.config import Settings


def test_defaults_when_env_unset(monkeypatch):
    for var in ("RETRIEVER", "MAX_AGENT_STEPS", "LLM_CHAT_MODEL", "DATASET_DIR"):
        monkeypatch.delenv(var, raising=False)
    settings = Settings.from_env()
    assert settings.retriever == "auto"
    assert settings.max_agent_steps == 8
    assert settings.tickets_path.name == "tickets.json"


def test_env_overrides_are_applied(monkeypatch):
    monkeypatch.setenv("RETRIEVER", "bm25")
    monkeypatch.setenv("MAX_AGENT_STEPS", "3")
    settings = Settings.from_env()
    assert settings.retriever == "bm25"
    assert settings.max_agent_steps == 3


@pytest.mark.parametrize(
    "var,bad_value",
    [
        ("RETRIEVER", "vektor"),
        ("MAX_AGENT_STEPS", "abc"),
        ("MAX_AGENT_STEPS", "0"),
    ],
)
def test_invalid_env_values_fail_loudly(monkeypatch, var, bad_value):
    monkeypatch.setenv(var, bad_value)
    with pytest.raises(ValidationError):
        Settings.from_env()
