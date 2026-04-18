"""Initial schema migration for image harbor."""

from sqlite3 import Connection

from repository.migrations import Migration


class V0001InitialSchema(Migration):
    version = 1
    description = "Initial SQLite schema for image harbor MVP"

    def upgrade(self, connection: Connection) -> None:
        connection.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                applied_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                path TEXT NOT NULL UNIQUE,
                thumbnail_path TEXT,
                preview_path TEXT,
                mime_type TEXT NOT NULL,
                width INTEGER,
                height INTEGER,
                orientation TEXT,
                size INTEGER NOT NULL,
                hash TEXT,
                original_filename TEXT,
                original_size INTEGER,
                original_last_modified_ts TEXT,
                original_path TEXT,
                created_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_updated_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CHECK (width IS NULL OR width > 0),
                CHECK (height IS NULL OR height > 0),
                CHECK (size >= 0),
                CHECK (original_size IS NULL OR original_size >= 0),
                CHECK (
                    orientation IS NULL
                    OR orientation IN ('portrait', 'landscape', 'square')
                )
            );

            CREATE TABLE IF NOT EXISTS film_rolls (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                camera_make TEXT,
                camera_model TEXT,
                format TEXT,
                stock TEXT,
                lens TEXT,
                captured_year INTEGER,
                captured_month INTEGER,
                captured_day INTEGER,
                created_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_updated_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CHECK (captured_year IS NULL OR captured_year BETWEEN 1800 AND 9999),
                CHECK (captured_month IS NULL OR captured_month BETWEEN 1 AND 12),
                CHECK (captured_day IS NULL OR captured_day BETWEEN 1 AND 31)
            );

            CREATE TABLE IF NOT EXISTS import_groups (
                id INTEGER PRIMARY KEY,
                import_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                source_path TEXT,
                created_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS image_assets (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                format TEXT,
                camera_make TEXT,
                camera_model TEXT,
                lens TEXT,
                captured_year INTEGER,
                captured_month INTEGER,
                captured_day INTEGER,
                rating INTEGER NOT NULL DEFAULT 0,
                needs_editing INTEGER NOT NULL DEFAULT 0,
                has_been_viewed INTEGER NOT NULL DEFAULT 0,
                last_viewed_ts TEXT,
                file_id INTEGER NOT NULL,
                edited_from_id INTEGER,
                belongs_to_roll_id INTEGER,
                imported_in_group_id INTEGER,
                created_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_updated_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CHECK (captured_year IS NULL OR captured_year BETWEEN 1800 AND 9999),
                CHECK (captured_month IS NULL OR captured_month BETWEEN 1 AND 12),
                CHECK (captured_day IS NULL OR captured_day BETWEEN 1 AND 31),
                CHECK (rating BETWEEN 0 AND 5),
                CHECK (needs_editing IN (0, 1)),
                CHECK (has_been_viewed IN (0, 1)),
                CHECK (edited_from_id IS NULL OR edited_from_id <> id),
                FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE RESTRICT,
                FOREIGN KEY (edited_from_id) REFERENCES image_assets(id) ON DELETE SET NULL,
                FOREIGN KEY (belongs_to_roll_id) REFERENCES film_rolls(id) ON DELETE SET NULL,
                FOREIGN KEY (imported_in_group_id) REFERENCES import_groups(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS user_collections (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_updated_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS user_collections_to_image_assets (
                user_collection_id INTEGER NOT NULL,
                image_asset_id INTEGER NOT NULL,
                created_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_collection_id, image_asset_id),
                FOREIGN KEY (user_collection_id) REFERENCES user_collections(id) ON DELETE CASCADE,
                FOREIGN KEY (image_asset_id) REFERENCES image_assets(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL COLLATE NOCASE UNIQUE,
                created_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS tag_to_image_asset (
                tag_id INTEGER NOT NULL,
                image_asset_id INTEGER NOT NULL,
                created_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (tag_id, image_asset_id),
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
                FOREIGN KEY (image_asset_id) REFERENCES image_assets(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_files_hash ON files(hash);
            CREATE INDEX IF NOT EXISTS idx_image_assets_file_id ON image_assets(file_id);
            CREATE INDEX IF NOT EXISTS idx_image_assets_roll_id ON image_assets(belongs_to_roll_id);
            CREATE INDEX IF NOT EXISTS idx_image_assets_import_group_id ON image_assets(imported_in_group_id);
            CREATE INDEX IF NOT EXISTS idx_image_assets_edited_from_id ON image_assets(edited_from_id);
            CREATE INDEX IF NOT EXISTS idx_image_assets_rating ON image_assets(rating);
            CREATE INDEX IF NOT EXISTS idx_image_assets_needs_editing ON image_assets(needs_editing);
            CREATE INDEX IF NOT EXISTS idx_image_assets_last_viewed_ts ON image_assets(last_viewed_ts);
            CREATE INDEX IF NOT EXISTS idx_film_rolls_name ON film_rolls(name);
            CREATE INDEX IF NOT EXISTS idx_user_collections_name ON user_collections(name);

            CREATE TRIGGER IF NOT EXISTS trg_files_last_updated_ts
            AFTER UPDATE ON files
            FOR EACH ROW
            WHEN NEW.last_updated_ts = OLD.last_updated_ts
            BEGIN
                UPDATE files
                SET last_updated_ts = CURRENT_TIMESTAMP
                WHERE id = NEW.id;
            END;

            CREATE TRIGGER IF NOT EXISTS trg_film_rolls_last_updated_ts
            AFTER UPDATE ON film_rolls
            FOR EACH ROW
            WHEN NEW.last_updated_ts = OLD.last_updated_ts
            BEGIN
                UPDATE film_rolls
                SET last_updated_ts = CURRENT_TIMESTAMP
                WHERE id = NEW.id;
            END;

            CREATE TRIGGER IF NOT EXISTS trg_image_assets_last_updated_ts
            AFTER UPDATE ON image_assets
            FOR EACH ROW
            WHEN NEW.last_updated_ts = OLD.last_updated_ts
            BEGIN
                UPDATE image_assets
                SET last_updated_ts = CURRENT_TIMESTAMP
                WHERE id = NEW.id;
            END;

            CREATE TRIGGER IF NOT EXISTS trg_user_collections_last_updated_ts
            AFTER UPDATE ON user_collections
            FOR EACH ROW
            WHEN NEW.last_updated_ts = OLD.last_updated_ts
            BEGIN
                UPDATE user_collections
                SET last_updated_ts = CURRENT_TIMESTAMP
                WHERE id = NEW.id;
            END;

            INSERT OR IGNORE INTO schema_migrations (version, description)
            VALUES (1, 'Initial SQLite schema for image harbor MVP');

            PRAGMA user_version = 1;
            """
        )

    def downgrade(self, connection: Connection) -> None:
        connection.executescript(
            """
            DROP TRIGGER IF EXISTS trg_user_collections_last_updated_ts;
            DROP TRIGGER IF EXISTS trg_image_assets_last_updated_ts;
            DROP TRIGGER IF EXISTS trg_film_rolls_last_updated_ts;
            DROP TRIGGER IF EXISTS trg_files_last_updated_ts;

            DROP INDEX IF EXISTS idx_user_collections_name;
            DROP INDEX IF EXISTS idx_film_rolls_name;
            DROP INDEX IF EXISTS idx_image_assets_last_viewed_ts;
            DROP INDEX IF EXISTS idx_image_assets_needs_editing;
            DROP INDEX IF EXISTS idx_image_assets_rating;
            DROP INDEX IF EXISTS idx_image_assets_edited_from_id;
            DROP INDEX IF EXISTS idx_image_assets_import_group_id;
            DROP INDEX IF EXISTS idx_image_assets_roll_id;
            DROP INDEX IF EXISTS idx_image_assets_file_id;
            DROP INDEX IF EXISTS idx_files_hash;

            DELETE FROM schema_migrations WHERE version = 1;

            DROP TABLE IF EXISTS tag_to_image_asset;
            DROP TABLE IF EXISTS tags;
            DROP TABLE IF EXISTS user_collections_to_image_assets;
            DROP TABLE IF EXISTS user_collections;
            DROP TABLE IF EXISTS image_assets;
            DROP TABLE IF EXISTS import_groups;
            DROP TABLE IF EXISTS film_rolls;
            DROP TABLE IF EXISTS files;
            DROP TABLE IF EXISTS schema_migrations;

            PRAGMA user_version = 0;
            """
        )


__all__ = ["V0001InitialSchema"]
