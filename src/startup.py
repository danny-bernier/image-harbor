"""Application startup initialization for filesystem and database state."""

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

import app_properties
from client.database_client import create_database_engine, get_database_path
from model.errors import StartupError
from util.log_util import Logger, get_logger

log: Logger = get_logger(__name__)


_ALEMBIC_INI_PATH = app_properties.REPO_ROOT / "alembic.ini"
_ALEMBIC_SCRIPT_PATH = app_properties.REPO_ROOT / "alembic"


def init_app():
    """Initialize application-owned filesystem and database state.

    Raises:
        StartupError: If filesystem or database startup work fails.
    """

    init_filesystem()
    init_database()


def init_filesystem():
    """Create the application data, config, and cache directories.

    Raises:
        StartupError: If filesystem initialization fails.
    """

    try:
        app_properties.APP_DATA_PATH.mkdir(parents=True, exist_ok=True)
        app_properties.APP_CONFIG_PATH.mkdir(parents=True, exist_ok=True)
        app_properties.APP_CACHE_PATH.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise StartupError(
            "Failed to initialize application filesystem",
            context={
                "app_data_path": str(app_properties.APP_DATA_PATH),
                "app_config_path": str(app_properties.APP_CONFIG_PATH),
                "app_cache_path": str(app_properties.APP_CACHE_PATH),
            },
        ) from exc


def init_database():
    """Run Alembic migrations for the configured application database.

    If the database file already exists and is already at the requested revision,
    Alembic upgrade work is skipped.

    Raises:
        StartupError: If migration inspection or migration execution fails.
    """

    ignore_migrations = app_properties.get_from_env("IGNORE_MIGRATIONS", "0")
    if ignore_migrations.lower() in {"1", "true", "yes", "on"}:
        log.warning("Skipping Alembic migrations because IMAGE_HARBOR_IGNORE_MIGRATIONS is enabled.")
        return

    target_revision = app_properties.get_from_env("DB_REVISION", "head")
    log.debug(f"Target database revision set to: {target_revision}")

    if not _ALEMBIC_INI_PATH.exists():
        raise StartupError(
            "Alembic config file not found",
            context={
                "alembic_ini_path": str(_ALEMBIC_INI_PATH),
                "target_revision": target_revision,
            },
        )

    alembic_config = Config(str(_ALEMBIC_INI_PATH))
    alembic_config.set_main_option("script_location", str(_ALEMBIC_SCRIPT_PATH))

    database_path = get_database_path()
    if database_path.exists():
        log.debug(f"Database file found at: {database_path}")
        try:
            script_directory = ScriptDirectory.from_config(alembic_config)
            target_revisions = script_directory.as_revision_number(target_revision)

            if isinstance(target_revisions, str):
                target_revision_set = {target_revisions}
            elif target_revisions is None:
                target_revision_set = set()
            else:
                target_revision_set = set(target_revisions)

            with create_database_engine().connect() as connection:
                current_revision_set = set(MigrationContext.configure(connection).get_current_heads())
        except Exception as exc:
            raise StartupError(
                "Failed to inspect current database revision",
                context={
                    "database_path": str(database_path),
                    "target_revision": target_revision,
                },
            ) from exc

        if current_revision_set == target_revision_set:
            log.debug(f"Database already at requested revision: {target_revision}")
            return
        else:
            log.debug(f"Database revision(s) current: {current_revision_set} target: {target_revision_set}")

    log.info(f"Running Alembic migrations to revision: {target_revision}...")
    try:
        command.upgrade(alembic_config, target_revision)
    except Exception as exc:
        raise StartupError(
            "Failed to apply database migrations",
            context={
                "database_path": str(database_path),
                "target_revision": target_revision,
            },
        ) from exc
