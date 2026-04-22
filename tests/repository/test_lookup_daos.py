"""Starter tests for DAO lookup helpers."""

from __future__ import annotations

from sqlalchemy.orm import Session

from model.database.models import File, ImportGroup, Tag
from repository.daos import FileDAO, ImportGroupDAO, TagDAO


def test_file_dao_get_by_path_returns_matching_row(session: Session) -> None:
    """Ensure file lookup by path returns the expected row."""

    dao = FileDAO(session)
    dao.add(
        File(
            path="/library/one.jpg",
            mime_type="image/jpeg",
            size=123,
        ),
        commit=True,
    )

    found = dao.get_by_path("/library/one.jpg")

    assert found is not None
    assert found.mime_type == "image/jpeg"


def test_import_group_dao_get_by_storage_dir_returns_matching_row(session: Session) -> None:
    """Ensure import-group lookup by storage_dir returns the expected row."""

    dao = ImportGroupDAO(session)
    dao.add(ImportGroup(storage_dir="/harbor/imports/001"), commit=True)

    found = dao.get_by_storage_dir("/harbor/imports/001")

    assert found is not None
    assert found.storage_dir == "/harbor/imports/001"


def test_tag_dao_get_by_name_returns_matching_row(session: Session) -> None:
    """Ensure tag lookup by name returns the expected row."""

    dao = TagDAO(session)
    dao.add(Tag(name="favorites"), commit=True)

    found = dao.get_by_name("favorites")

    assert found is not None
    assert found.name == "favorites"
