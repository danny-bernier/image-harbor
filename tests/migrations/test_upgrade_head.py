"""Migration smoke tests for Alembic upgrade-to-head behavior."""

from __future__ import annotations

from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

from client import database_client
from model.database.schema import metadata

_REPO_ROOT = Path(__file__).resolve().parents[2]
_ALEMBIC_INI_PATH = _REPO_ROOT / "alembic.ini"
_ALEMBIC_SCRIPT_PATH = _REPO_ROOT / "alembic"


def _build_alembic_config() -> Config:
    """Build a test Alembic config pointing at this repository script location.

    Returns:
        Config: Alembic configuration for running repository migrations.
    """

    config = Config(str(_ALEMBIC_INI_PATH))
    config.set_main_option("script_location", str(_ALEMBIC_SCRIPT_PATH))
    return config


def test_upgrade_to_head_creates_expected_schema(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Apply migrations and verify expected tables and revision are present.

    Args:
        tmp_path: Per-test temporary filesystem root.
        monkeypatch: Pytest monkeypatch fixture.
    """

    app_data_path = tmp_path / "app-data"
    app_data_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(database_client, "APP_DATA_PATH", app_data_path)

    command.upgrade(_build_alembic_config(), "head")

    database_path = database_client.get_database_path()
    assert database_path.exists()

    engine = create_engine(f"sqlite+pysqlite:///{database_path.as_posix()}", future=True)
    with engine.connect() as connection:
        table_names = set(
            connection.execute(text("SELECT name FROM sqlite_master WHERE type = 'table'")).scalars().all()
        )
        expected_table_names = set(metadata.tables.keys()) | {"alembic_version"}
        assert expected_table_names.issubset(table_names)

        current_revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
        assert current_revision == "0001"


def test_upgrade_to_head_is_idempotent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Run upgrade-to-head twice and verify revision remains stable.

    Args:
        tmp_path: Per-test temporary filesystem root.
        monkeypatch: Pytest monkeypatch fixture.
    """

    app_data_path = tmp_path / "app-data"
    app_data_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(database_client, "APP_DATA_PATH", app_data_path)

    config = _build_alembic_config()
    command.upgrade(config, "head")
    command.upgrade(config, "head")

    database_path = database_client.get_database_path()
    engine = create_engine(f"sqlite+pysqlite:///{database_path.as_posix()}", future=True)
    with engine.connect() as connection:
        current_revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
        assert current_revision == "0001"
