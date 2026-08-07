import pytest

from app.config import Settings


def test_settings_loads_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("WORK_ORDER_APP_NAME", "Test Work Order API")
    monkeypatch.setenv("WORK_ORDER_ENVIRONMENT", "test")

    settings = Settings(_env_file=None)  # pyright: ignore[reportCallIssue]

    assert settings.app_name == "Test Work Order API"
    assert settings.environment == "test"
