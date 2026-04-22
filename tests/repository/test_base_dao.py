"""Starter tests for common BaseDAO behavior."""

from __future__ import annotations

from sqlalchemy.orm import Session

from model.database.models import FilmRoll
from repository.daos import FilmRollDAO


def test_base_dao_add_and_get_round_trip(session: Session) -> None:
    """Ensure add and get persist and fetch a row by primary key."""

    dao = FilmRollDAO(session)
    added = dao.add(FilmRoll(name="Test Roll"), commit=True)

    fetched = dao.get(added.id)

    assert fetched is not None
    assert fetched.id == added.id
    assert fetched.name == "Test Roll"


def test_base_dao_list_applies_limit_and_offset(session: Session) -> None:
    """Ensure list supports deterministic pagination controls."""

    dao = FilmRollDAO(session)
    dao.add(FilmRoll(name="Roll A"))
    dao.add(FilmRoll(name="Roll B"))
    dao.add(FilmRoll(name="Roll C"), commit=True)

    rows = dao.list(limit=2, offset=1)

    assert len(rows) == 2
    assert rows[0].name == "Roll B"
    assert rows[1].name == "Roll C"


def test_base_dao_delete_by_identity_returns_expected_bool(session: Session) -> None:
    """Ensure delete_by_identity reports whether a row was removed."""

    dao = FilmRollDAO(session)
    added = dao.add(FilmRoll(name="Delete Me"), commit=True)

    deleted = dao.delete_by_identity(added.id, commit=True)
    deleted_missing = dao.delete_by_identity(added.id, commit=True)

    assert deleted is True
    assert deleted_missing is False
