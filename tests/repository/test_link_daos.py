"""Starter tests for composite-key DAO link entities."""

from __future__ import annotations

from sqlalchemy.orm import Session

from model.database.models import File, ImageAsset, Tag, TagToImageAsset, UserCollection, UserCollectionToImageAsset
from repository.daos import TagToImageAssetDAO, UserCollectionToImageAssetDAO


def test_user_collection_to_image_asset_dao_get_link(session: Session) -> None:
    """Ensure collection-asset link lookup works with composite primary keys."""

    file_row = File(path="/library/two.jpg", mime_type="image/jpeg", size=456)
    session.add(file_row)
    session.flush()

    image_asset = ImageAsset(name="Asset Two", file_id=file_row.id)
    collection = UserCollection(name="Quick Picks")
    session.add_all([image_asset, collection])
    session.flush()

    link = UserCollectionToImageAsset(user_collection_id=collection.id, image_asset_id=image_asset.id)
    session.add(link)
    session.commit()

    dao = UserCollectionToImageAssetDAO(session)
    found = dao.get_link(collection.id, image_asset.id)

    assert found is not None
    assert found.user_collection_id == collection.id
    assert found.image_asset_id == image_asset.id


def test_tag_to_image_asset_dao_get_link(session: Session) -> None:
    """Ensure tag-asset link lookup works with composite primary keys."""

    file_row = File(path="/library/three.jpg", mime_type="image/jpeg", size=789)
    session.add(file_row)
    session.flush()

    image_asset = ImageAsset(name="Asset Three", file_id=file_row.id)
    tag = Tag(name="portfolio")
    session.add_all([image_asset, tag])
    session.flush()

    link = TagToImageAsset(tag_id=tag.id, image_asset_id=image_asset.id)
    session.add(link)
    session.commit()

    dao = TagToImageAssetDAO(session)
    found = dao.get_link(tag.id, image_asset.id)

    assert found is not None
    assert found.tag_id == tag.id
    assert found.image_asset_id == image_asset.id
