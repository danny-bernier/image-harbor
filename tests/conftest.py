"""Shared pytest fixtures for repository and DAO tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from model.database.schema import metadata
from repository.daos import create_session_factory


@pytest.fixture(scope="session")
def engine() -> Engine:
    """Create a shared in-memory SQLite engine for repository tests.

    Returns:
        Engine: Shared SQLAlchemy engine backed by in-memory SQLite.
    """

    test_engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )

    @event.listens_for(test_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, _connection_record) -> None:  # type: ignore[no-untyped-def]
        """Enable SQLite foreign key constraints for each new DB-API connection."""

        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()

    return test_engine


@pytest.fixture()
def connection(engine: Engine) -> Generator[Connection]:
    """Provide a connection with a fresh schema lifecycle for each test.

    Args:
        engine: Shared SQLAlchemy engine fixture.

    Yields:
        Generator[Connection]: Connection with schema created before and dropped after test execution.
    """

    with engine.connect() as conn:
        metadata.create_all(conn)
        try:
            yield conn
        finally:
            metadata.drop_all(conn)


@pytest.fixture()
def session(connection: Connection) -> Generator[Session]:
    """Provide a SQLAlchemy session bound to the per-test connection.

    Args:
        connection: Per-test SQLAlchemy connection fixture.

    Yields:
        Generator[Session]: Session bound to the per-test connection.
    """

    SessionFactory = create_session_factory(connection.engine)
    db_session = SessionFactory(bind=connection)
    try:
        yield db_session
    finally:
        db_session.close()
