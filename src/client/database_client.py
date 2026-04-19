"""Database path and engine helpers."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app_properties import APP_DATA_PATH

_DATABASE_FILENAME = "image_harbor.db"


def get_database_path() -> Path:
    """Get the default SQLite database path for the application.

    Returns:
        Path: The filesystem path used for the application database.
    """

    return APP_DATA_PATH / _DATABASE_FILENAME


def get_database_url() -> str:
    """Get the configured SQLAlchemy database URL.

    Returns:
        str: The SQLAlchemy connection URL for the application database.
    """

    return f"sqlite+pysqlite:///{get_database_path().as_posix()}"


def create_database_engine(*, echo: bool = False) -> Engine:
    """Create a SQLAlchemy engine for the application database.

    Args:
        echo: Whether SQLAlchemy should echo executed SQL statements.

    Returns:
        Engine: A SQLAlchemy engine configured for the application database.
    """

    database_path = get_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(get_database_url(), echo=echo, future=True)
