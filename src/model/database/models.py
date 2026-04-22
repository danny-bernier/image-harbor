"""Declarative SQLAlchemy ORM models mapped to the Image Harbor schema."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, relationship

from . import schema


class Base(DeclarativeBase):
    """Base ORM class bound to the shared schema metadata."""

    metadata = schema.metadata


class File(Base):
    """Represent a managed file and its derived preview metadata."""

    __table__ = schema.files

    image_assets: Mapped[list[ImageAsset]] = relationship(back_populates="file")


class FilmRoll(Base):
    """Represent a film roll and optional capture metadata."""

    __table__ = schema.film_rolls

    image_assets: Mapped[list[ImageAsset]] = relationship(back_populates="belongs_to_roll")


class ImportGroup(Base):
    """Represent a single import batch that writes to one storage directory."""

    __table__ = schema.import_groups

    image_assets: Mapped[list[ImageAsset]] = relationship(back_populates="imported_in_group")


class ImageAsset(Base):
    """Represent a cataloged image and its edit/review lifecycle state."""

    __table__ = schema.image_assets

    file: Mapped[File] = relationship(back_populates="image_assets")
    edited_from: Mapped[ImageAsset | None] = relationship(
        back_populates="derived_assets",
        remote_side=[__table__.c.id],
    )
    derived_assets: Mapped[list[ImageAsset]] = relationship(back_populates="edited_from")
    belongs_to_roll: Mapped[FilmRoll | None] = relationship(back_populates="image_assets")
    imported_in_group: Mapped[ImportGroup | None] = relationship(back_populates="image_assets")
    user_collection_links: Mapped[list[UserCollectionToImageAsset]] = relationship(back_populates="image_asset")
    tag_links: Mapped[list[TagToImageAsset]] = relationship(back_populates="image_asset")


class UserCollection(Base):
    """Represent a user-curated collection of image assets."""

    __table__ = schema.user_collections

    image_asset_links: Mapped[list[UserCollectionToImageAsset]] = relationship(back_populates="user_collection")


class UserCollectionToImageAsset(Base):
    """Represent a link between a user collection and an image asset."""

    __table__ = schema.user_collections_to_image_assets

    user_collection: Mapped[UserCollection] = relationship(back_populates="image_asset_links")
    image_asset: Mapped[ImageAsset] = relationship(back_populates="user_collection_links")


class Tag(Base):
    """Represent a normalized label that can be attached to assets."""

    __table__ = schema.tags

    image_asset_links: Mapped[list[TagToImageAsset]] = relationship(back_populates="tag")


class TagToImageAsset(Base):
    """Represent a link between a tag and an image asset."""

    __table__ = schema.tag_to_image_asset

    tag: Mapped[Tag] = relationship(back_populates="image_asset_links")
    image_asset: Mapped[ImageAsset] = relationship(back_populates="tag_links")


__all__ = [
    "Base",
    "File",
    "FilmRoll",
    "ImportGroup",
    "ImageAsset",
    "UserCollection",
    "UserCollectionToImageAsset",
    "Tag",
    "TagToImageAsset",
]
