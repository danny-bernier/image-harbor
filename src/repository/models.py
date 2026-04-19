"""SQLAlchemy schema metadata for Image Harbor."""

from __future__ import annotations

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    Table,
    Text,
    text,
)

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)

files = Table(
    "files",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("path", Text, nullable=False, unique=True),
    Column("thumbnail_path", Text),
    Column("preview_path", Text),
    Column("mime_type", Text, nullable=False),
    Column("width", Integer),
    Column("height", Integer),
    Column("orientation", Text),
    Column("size", Integer, nullable=False),
    Column("hash", Text),
    Column("original_filename", Text),
    Column("original_size", Integer),
    Column("original_last_modified_ts", Text),
    Column("original_path", Text),
    Column("created_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("last_updated_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    CheckConstraint("width IS NULL OR width > 0", name="width_positive"),
    CheckConstraint("height IS NULL OR height > 0", name="height_positive"),
    CheckConstraint("size >= 0", name="size_non_negative"),
    CheckConstraint("original_size IS NULL OR original_size >= 0", name="original_size_non_negative"),
    CheckConstraint(
        "orientation IS NULL OR orientation IN ('portrait', 'landscape', 'square')", name="orientation_valid"
    ),
)

film_rolls = Table(
    "film_rolls",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("description", Text),
    Column("camera_make", Text),
    Column("camera_model", Text),
    Column("format", Text),
    Column("stock", Text),
    Column("lens", Text),
    Column("captured_year", Integer),
    Column("captured_month", Integer),
    Column("captured_day", Integer),
    Column("created_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("last_updated_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    CheckConstraint("captured_year IS NULL OR captured_year BETWEEN 1800 AND 9999", name="captured_year_valid"),
    CheckConstraint("captured_month IS NULL OR captured_month BETWEEN 1 AND 12", name="captured_month_valid"),
    CheckConstraint("captured_day IS NULL OR captured_day BETWEEN 1 AND 31", name="captured_day_valid"),
)

import_groups = Table(
    "import_groups",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("storage_dir", Text(collation="NOCASE"), nullable=False, unique=True),
)

image_assets = Table(
    "image_assets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("description", Text),
    Column("format", Text),
    Column("camera_make", Text),
    Column("camera_model", Text),
    Column("lens", Text),
    Column("captured_year", Integer),
    Column("captured_month", Integer),
    Column("captured_day", Integer),
    Column("rating", Integer, nullable=False, server_default=text("0")),
    Column("needs_editing", Integer, nullable=False, server_default=text("0")),
    Column("has_been_viewed", Integer, nullable=False, server_default=text("0")),
    Column("last_viewed_ts", Text),
    Column("file_id", Integer, ForeignKey("files.id", ondelete="RESTRICT"), nullable=False),
    Column("edited_from_id", Integer, ForeignKey("image_assets.id", ondelete="SET NULL")),
    Column("belongs_to_roll_id", Integer, ForeignKey("film_rolls.id", ondelete="SET NULL")),
    Column("imported_in_group_id", Integer, ForeignKey("import_groups.id", ondelete="SET NULL")),
    Column("created_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("last_updated_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    CheckConstraint("captured_year IS NULL OR captured_year BETWEEN 1800 AND 9999", name="captured_year_valid"),
    CheckConstraint("captured_month IS NULL OR captured_month BETWEEN 1 AND 12", name="captured_month_valid"),
    CheckConstraint("captured_day IS NULL OR captured_day BETWEEN 1 AND 31", name="captured_day_valid"),
    CheckConstraint("rating BETWEEN 0 AND 5", name="rating_valid"),
    CheckConstraint("needs_editing IN (0, 1)", name="needs_editing_boolean"),
    CheckConstraint("has_been_viewed IN (0, 1)", name="has_been_viewed_boolean"),
    CheckConstraint("edited_from_id IS NULL OR edited_from_id <> id", name="edited_from_not_self"),
)

user_collections = Table(
    "user_collections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("description", Text),
    Column("created_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("last_updated_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

user_collections_to_image_assets = Table(
    "user_collections_to_image_assets",
    metadata,
    Column("user_collection_id", Integer, ForeignKey("user_collections.id", ondelete="CASCADE"), primary_key=True),
    Column("image_asset_id", Integer, ForeignKey("image_assets.id", ondelete="CASCADE"), primary_key=True),
    Column("created_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

tags = Table(
    "tags",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text(collation="NOCASE"), nullable=False, unique=True),
    Column("created_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

tag_to_image_asset = Table(
    "tag_to_image_asset",
    metadata,
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    Column("image_asset_id", Integer, ForeignKey("image_assets.id", ondelete="CASCADE"), primary_key=True),
    Column("created_ts", Text, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

Index("idx_files_hash", files.c.hash)
Index("idx_image_assets_file_id", image_assets.c.file_id)
Index("idx_image_assets_roll_id", image_assets.c.belongs_to_roll_id)
Index("idx_image_assets_import_group_id", image_assets.c.imported_in_group_id)
Index("idx_image_assets_edited_from_id", image_assets.c.edited_from_id)
Index("idx_image_assets_rating", image_assets.c.rating)
Index("idx_image_assets_needs_editing", image_assets.c.needs_editing)
Index("idx_image_assets_last_viewed_ts", image_assets.c.last_viewed_ts)
Index("idx_film_rolls_name", film_rolls.c.name)
Index("idx_user_collections_name", user_collections.c.name)

__all__ = ["metadata"]
