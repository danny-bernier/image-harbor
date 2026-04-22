"""Constraint-focused tests for schema uniqueness, checks, and foreign keys."""

from __future__ import annotations

import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from model.database.models import File, FilmRoll, ImageAsset, ImportGroup, Tag, TagToImageAsset


def test_files_path_must_be_unique(session: Session) -> None:
    """Enforce unique file paths in the files table."""

    session.add(File(path="/library/dup.jpg", mime_type="image/jpeg", size=100))
    session.commit()

    session.add(File(path="/library/dup.jpg", mime_type="image/jpeg", size=200))

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_tags_name_unique_is_case_insensitive(session: Session) -> None:
    """Enforce NOCASE uniqueness for tag names."""

    session.add(Tag(name="Favorites"))
    session.commit()

    session.add(Tag(name="favorites"))

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_files_size_must_be_non_negative(session: Session) -> None:
    """Reject file rows that violate the size non-negative check constraint."""

    session.add(File(path="/library/negative.jpg", mime_type="image/jpeg", size=-1))

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_image_assets_rating_must_be_between_zero_and_five(session: Session) -> None:
    """Reject image assets with ratings outside the allowed range."""

    file_row = File(path="/library/rated.jpg", mime_type="image/jpeg", size=321)
    session.add(file_row)
    session.flush()

    session.add(ImageAsset(name="Bad Rating", file_id=file_row.id, rating=6))

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_image_assets_file_id_must_reference_existing_file(session: Session) -> None:
    """Reject image assets that reference a missing file row."""

    session.add(ImageAsset(name="Orphan", file_id=99999))

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_tag_link_is_deleted_when_parent_tag_is_deleted(session: Session) -> None:
    """Ensure tag-to-asset links are removed via CASCADE when the tag is deleted."""

    file_row = File(path="/library/cascade.jpg", mime_type="image/jpeg", size=123)
    tag = Tag(name="cascade")
    session.add_all([file_row, tag])
    session.flush()

    asset = ImageAsset(name="Cascade Asset", file_id=file_row.id)
    session.add(asset)
    session.flush()

    link = TagToImageAsset(tag_id=tag.id, image_asset_id=asset.id)
    session.add(link)
    session.commit()

    session.execute(delete(Tag).where(Tag.id == tag.id))
    session.commit()
    session.expunge_all()

    remaining_link = session.get(TagToImageAsset, (tag.id, asset.id))
    assert remaining_link is None


def test_files_delete_is_restricted_when_image_asset_references_file(session: Session) -> None:
    """Reject file deletion when image assets still reference the file."""

    file_row = File(path="/library/restrict.jpg", mime_type="image/jpeg", size=222)
    session.add(file_row)
    session.flush()

    session.add(ImageAsset(name="Uses File", file_id=file_row.id))
    session.commit()

    with pytest.raises(IntegrityError):
        session.execute(delete(File).where(File.id == file_row.id))
        session.commit()
    session.rollback()


def test_roll_delete_sets_image_asset_roll_to_null(session: Session) -> None:
    """Ensure deleting a roll nulls belongs_to_roll_id on related assets."""

    file_row = File(path="/library/roll-null.jpg", mime_type="image/jpeg", size=333)
    roll = FilmRoll(name="Summer Roll")
    session.add_all([file_row, roll])
    session.flush()

    asset = ImageAsset(name="Roll Linked", file_id=file_row.id, belongs_to_roll_id=roll.id)
    session.add(asset)
    session.commit()

    session.execute(delete(FilmRoll).where(FilmRoll.id == roll.id))
    session.commit()
    session.expunge_all()

    refreshed_asset = session.get(ImageAsset, asset.id)
    assert refreshed_asset is not None
    assert refreshed_asset.belongs_to_roll_id is None


def test_import_group_delete_sets_image_asset_group_to_null(session: Session) -> None:
    """Ensure deleting an import group nulls imported_in_group_id on related assets."""

    file_row = File(path="/library/group-null.jpg", mime_type="image/jpeg", size=444)
    import_group = ImportGroup(storage_dir="/harbor/imports/999")
    session.add_all([file_row, import_group])
    session.flush()

    asset = ImageAsset(name="Group Linked", file_id=file_row.id, imported_in_group_id=import_group.id)
    session.add(asset)
    session.commit()

    session.execute(delete(ImportGroup).where(ImportGroup.id == import_group.id))
    session.commit()
    session.expunge_all()

    refreshed_asset = session.get(ImageAsset, asset.id)
    assert refreshed_asset is not None
    assert refreshed_asset.imported_in_group_id is None


def test_edited_from_delete_sets_child_reference_to_null(session: Session) -> None:
    """Ensure deleting a source asset nulls edited_from_id on derived assets."""

    original_file = File(path="/library/original.jpg", mime_type="image/jpeg", size=555)
    derived_file = File(path="/library/derived.jpg", mime_type="image/jpeg", size=666)
    session.add_all([original_file, derived_file])
    session.flush()

    original_asset = ImageAsset(name="Original", file_id=original_file.id)
    session.add(original_asset)
    session.flush()

    derived_asset = ImageAsset(name="Derived", file_id=derived_file.id, edited_from_id=original_asset.id)
    session.add(derived_asset)
    session.commit()

    session.execute(delete(ImageAsset).where(ImageAsset.id == original_asset.id))
    session.commit()
    session.expunge_all()

    refreshed_derived_asset = session.get(ImageAsset, derived_asset.id)
    assert refreshed_derived_asset is not None
    assert refreshed_derived_asset.edited_from_id is None
