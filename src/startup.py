"""Application startup initialization for filesystem and database state."""

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

import app_properties
from repository.database import create_database_engine, get_database_path
from util.log_util import Logger, get_logger

log: Logger = get_logger(__name__)


_ALEMBIC_INI_PATH = app_properties.REPO_ROOT / "alembic.ini"
_ALEMBIC_SCRIPT_PATH = app_properties.REPO_ROOT / "alembic"


def init_app():
    """Initialize application-owned filesystem and database state."""

    init_filesystem()
    init_database()


def init_filesystem():
    """Create the application data, config, and cache directories."""

    app_properties.APP_DATA_PATH.mkdir(parents=True, exist_ok=True)
    app_properties.APP_CONFIG_PATH.mkdir(parents=True, exist_ok=True)
    app_properties.APP_CACHE_PATH.mkdir(parents=True, exist_ok=True)


def init_database():
    """Run Alembic migrations for the configured application database.

    If the database file already exists and is already at the requested revision,
    Alembic upgrade work is skipped.

    Raises:
        FileNotFoundError: If the Alembic configuration file cannot be found.
    """

    ignore_migrations = app_properties.get_from_env("IGNORE_MIGRATIONS", "0")
    if ignore_migrations.lower() in {"1", "true", "yes", "on"}:
        log.warning("Skipping Alembic migrations because IMAGE_HARBOR_IGNORE_MIGRATIONS is enabled.")
        return

    if not _ALEMBIC_INI_PATH.exists():
        raise FileNotFoundError(f"Alembic config file not found: {_ALEMBIC_INI_PATH}")

    target_revision = app_properties.get_from_env("DB_REVISION", "head")
    log.debug(f"Target database revision set to: {target_revision}")

    alembic_config = Config(str(_ALEMBIC_INI_PATH))
    alembic_config.set_main_option("script_location", str(_ALEMBIC_SCRIPT_PATH))

    database_path = get_database_path()
    if database_path.exists():
        log.debug(f"Database file found at: {database_path}")
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

        if current_revision_set == target_revision_set:
            log.debug(f"Database already at requested revision: {target_revision}")
            return
        else:
            log.debug(f"Database revision(s) current: {current_revision_set} target: {target_revision_set}")

    log.info(f"Running Alembic migrations to revision: {target_revision}...")
    command.upgrade(alembic_config, target_revision)
