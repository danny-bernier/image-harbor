from alembic import command
from alembic.config import Config

import app_properties
from util.log_util import Logger, get_logger

log: Logger = get_logger(__name__)


_ALEMBIC_INI_PATH = app_properties.REPO_ROOT / "alembic.ini"
_ALEMBIC_SCRIPT_PATH = app_properties.REPO_ROOT / "alembic"


def init_app():
    init_filesystem()
    init_database()


def init_filesystem():
    app_properties.APP_DATA_PATH.mkdir(parents=True, exist_ok=True)
    app_properties.APP_CONFIG_PATH.mkdir(parents=True, exist_ok=True)
    app_properties.APP_CACHE_PATH.mkdir(parents=True, exist_ok=True)


def init_database():
    ignore_migrations = app_properties.get_from_env("IGNORE_MIGRATIONS", "0")
    if ignore_migrations.lower() in {"1", "true", "yes", "on"}:
        log.warning("Skipping Alembic migrations because IMAGE_HARBOR_IGNORE_MIGRATIONS is enabled.")
        return

    if not _ALEMBIC_INI_PATH.exists():
        raise FileNotFoundError(f"Alembic config file not found: {_ALEMBIC_INI_PATH}")

    target_revision = app_properties.get_from_env("DB_REVISION", "head")

    alembic_config = Config(str(_ALEMBIC_INI_PATH))
    alembic_config.set_main_option("script_location", str(_ALEMBIC_SCRIPT_PATH))

    log.info(f"Running Alembic migrations to revision: {target_revision}")
    command.upgrade(alembic_config, target_revision)
