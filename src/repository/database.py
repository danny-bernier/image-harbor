"""Database path and engine helpers."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app_properties import APP_DATA_PATH

_DATABASE_FILENAME = "image_harbor.db"


def get_database_path() -> Path:
    """Return the default SQLite database path for the application."""

    return APP_DATA_PATH / _DATABASE_FILENAME


def get_database_url() -> str:
    """Return the configured SQLAlchemy database URL."""

    return f"sqlite+pysqlite:///{get_database_path().as_posix()}"


def create_database_engine(*, echo: bool = False) -> Engine:
    """Create an engine for the configured application database."""

    database_path = get_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(get_database_url(), echo=echo, future=True)
