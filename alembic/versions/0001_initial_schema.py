"""Initial schema.

Revision ID: 0001
Revises:
Create Date: 2026-04-18 00:00:00
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def _create_last_updated_trigger(table_name: str) -> None:
    """Create an update trigger that refreshes last_updated_ts for a table.

    Args:
        table_name: Database table name that includes id and last_updated_ts columns.
    """

    op.execute(
        f"""
        CREATE TRIGGER trg_{table_name}_last_updated_ts
        AFTER UPDATE ON {table_name}
        FOR EACH ROW
        WHEN NEW.last_updated_ts = OLD.last_updated_ts
        BEGIN
            UPDATE {table_name}
            SET last_updated_ts = CURRENT_TIMESTAMP
            WHERE id = NEW.id;
        END;
        """
    )


def upgrade() -> None:
    """Apply the initial database schema and indexes."""

    op.execute("PRAGMA foreign_keys = ON")

    op.create_table(
        "files",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("thumbnail_path", sa.Text(), nullable=True),
        sa.Column("preview_path", sa.Text(), nullable=True),
        sa.Column("mime_type", sa.Text(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("orientation", sa.Text(), nullable=True),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("hash", sa.Text(), nullable=True),
        sa.Column("original_filename", sa.Text(), nullable=True),
        sa.Column("original_size", sa.Integer(), nullable=True),
        sa.Column("original_last_modified_ts", sa.Text(), nullable=True),
        sa.Column("original_path", sa.Text(), nullable=True),
        sa.Column(
            "created_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "last_updated_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint("width IS NULL OR width > 0", name="ck_files_width_positive"),
        sa.CheckConstraint("height IS NULL OR height > 0", name="ck_files_height_positive"),
        sa.CheckConstraint("size >= 0", name="ck_files_size_non_negative"),
        sa.CheckConstraint(
            "original_size IS NULL OR original_size >= 0",
            name="ck_files_original_size_non_negative",
        ),
        sa.CheckConstraint(
            "orientation IS NULL OR orientation IN ('portrait', 'landscape', 'square')",
            name="ck_files_orientation_valid",
        ),
        sa.UniqueConstraint("path", name="uq_files_path"),
    )

    op.create_table(
        "film_rolls",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("camera_make", sa.Text(), nullable=True),
        sa.Column("camera_model", sa.Text(), nullable=True),
        sa.Column("format", sa.Text(), nullable=True),
        sa.Column("stock", sa.Text(), nullable=True),
        sa.Column("lens", sa.Text(), nullable=True),
        sa.Column("captured_year", sa.Integer(), nullable=True),
        sa.Column("captured_month", sa.Integer(), nullable=True),
        sa.Column("captured_day", sa.Integer(), nullable=True),
        sa.Column(
            "created_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "last_updated_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "captured_year IS NULL OR captured_year BETWEEN 1800 AND 9999",
            name="ck_film_rolls_captured_year_valid",
        ),
        sa.CheckConstraint(
            "captured_month IS NULL OR captured_month BETWEEN 1 AND 12",
            name="ck_film_rolls_captured_month_valid",
        ),
        sa.CheckConstraint(
            "captured_day IS NULL OR captured_day BETWEEN 1 AND 31",
            name="ck_film_rolls_captured_day_valid",
        ),
    )

    op.create_table(
        "import_groups",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "created_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("storage_dir", sa.Text(collation="NOCASE"), nullable=False),
        sa.UniqueConstraint("storage_dir", name="uq_import_groups_storage_dir"),
    )

    op.create_table(
        "image_assets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("format", sa.Text(), nullable=True),
        sa.Column("camera_make", sa.Text(), nullable=True),
        sa.Column("camera_model", sa.Text(), nullable=True),
        sa.Column("lens", sa.Text(), nullable=True),
        sa.Column("captured_year", sa.Integer(), nullable=True),
        sa.Column("captured_month", sa.Integer(), nullable=True),
        sa.Column("captured_day", sa.Integer(), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("needs_editing", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("has_been_viewed", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("last_viewed_ts", sa.Text(), nullable=True),
        sa.Column("file_id", sa.Integer(), nullable=False),
        sa.Column("edited_from_id", sa.Integer(), nullable=True),
        sa.Column("belongs_to_roll_id", sa.Integer(), nullable=True),
        sa.Column("imported_in_group_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "last_updated_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "captured_year IS NULL OR captured_year BETWEEN 1800 AND 9999",
            name="ck_image_assets_captured_year_valid",
        ),
        sa.CheckConstraint(
            "captured_month IS NULL OR captured_month BETWEEN 1 AND 12",
            name="ck_image_assets_captured_month_valid",
        ),
        sa.CheckConstraint(
            "captured_day IS NULL OR captured_day BETWEEN 1 AND 31",
            name="ck_image_assets_captured_day_valid",
        ),
        sa.CheckConstraint("rating BETWEEN 0 AND 5", name="ck_image_assets_rating_valid"),
        sa.CheckConstraint("needs_editing IN (0, 1)", name="ck_image_assets_needs_editing_boolean"),
        sa.CheckConstraint("has_been_viewed IN (0, 1)", name="ck_image_assets_has_been_viewed_boolean"),
        sa.CheckConstraint(
            "edited_from_id IS NULL OR edited_from_id <> id",
            name="ck_image_assets_edited_from_not_self",
        ),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["files.id"],
            name="fk_image_assets_file_id_files",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["edited_from_id"],
            ["image_assets.id"],
            name="fk_image_assets_edited_from_id_image_assets",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["belongs_to_roll_id"],
            ["film_rolls.id"],
            name="fk_image_assets_belongs_to_roll_id_film_rolls",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["imported_in_group_id"],
            ["import_groups.id"],
            name="fk_image_assets_imported_in_group_id_import_groups",
            ondelete="SET NULL",
        ),
    )

    op.create_table(
        "user_collections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "last_updated_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.create_table(
        "user_collections_to_image_assets",
        sa.Column("user_collection_id", sa.Integer(), nullable=False),
        sa.Column("image_asset_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(
            ["user_collection_id"],
            ["user_collections.id"],
            name="fk_user_collections_to_image_assets_user_collection_id_user_collections",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["image_asset_id"],
            ["image_assets.id"],
            name="fk_user_collections_to_image_assets_image_asset_id_image_assets",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "user_collection_id",
            "image_asset_id",
            name="pk_user_collections_to_image_assets",
        ),
    )

    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.Text(collation="NOCASE"), nullable=False),
        sa.Column(
            "created_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.UniqueConstraint("name", name="uq_tags_name"),
    )

    op.create_table(
        "tag_to_image_asset",
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.Column("image_asset_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_ts",
            sa.Text(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
            name="fk_tag_to_image_asset_tag_id_tags",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["image_asset_id"],
            ["image_assets.id"],
            name="fk_tag_to_image_asset_image_asset_id_image_assets",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("tag_id", "image_asset_id", name="pk_tag_to_image_asset"),
    )

    op.create_index("idx_files_hash", "files", ["hash"])
    op.create_index("idx_image_assets_file_id", "image_assets", ["file_id"])
    op.create_index("idx_image_assets_roll_id", "image_assets", ["belongs_to_roll_id"])
    op.create_index("idx_image_assets_import_group_id", "image_assets", ["imported_in_group_id"])
    op.create_index("idx_image_assets_edited_from_id", "image_assets", ["edited_from_id"])
    op.create_index("idx_image_assets_rating", "image_assets", ["rating"])
    op.create_index("idx_image_assets_needs_editing", "image_assets", ["needs_editing"])
    op.create_index("idx_image_assets_last_viewed_ts", "image_assets", ["last_viewed_ts"])
    op.create_index("idx_film_rolls_name", "film_rolls", ["name"])
    op.create_index("idx_user_collections_name", "user_collections", ["name"])

    _create_last_updated_trigger("files")
    _create_last_updated_trigger("film_rolls")
    _create_last_updated_trigger("image_assets")
    _create_last_updated_trigger("user_collections")


def downgrade() -> None:
    """Revert the initial database schema and all related indexes/triggers."""

    op.execute("DROP TRIGGER IF EXISTS trg_user_collections_last_updated_ts")
    op.execute("DROP TRIGGER IF EXISTS trg_image_assets_last_updated_ts")
    op.execute("DROP TRIGGER IF EXISTS trg_film_rolls_last_updated_ts")
    op.execute("DROP TRIGGER IF EXISTS trg_files_last_updated_ts")

    op.drop_index("idx_user_collections_name", table_name="user_collections")
    op.drop_index("idx_film_rolls_name", table_name="film_rolls")
    op.drop_index("idx_image_assets_last_viewed_ts", table_name="image_assets")
    op.drop_index("idx_image_assets_needs_editing", table_name="image_assets")
    op.drop_index("idx_image_assets_rating", table_name="image_assets")
    op.drop_index("idx_image_assets_edited_from_id", table_name="image_assets")
    op.drop_index("idx_image_assets_import_group_id", table_name="image_assets")
    op.drop_index("idx_image_assets_roll_id", table_name="image_assets")
    op.drop_index("idx_image_assets_file_id", table_name="image_assets")
    op.drop_index("idx_files_hash", table_name="files")

    op.drop_table("tag_to_image_asset")
    op.drop_table("tags")
    op.drop_table("user_collections_to_image_assets")
    op.drop_table("user_collections")
    op.drop_table("image_assets")
    op.drop_table("import_groups")
    op.drop_table("film_rolls")
    op.drop_table("files")
