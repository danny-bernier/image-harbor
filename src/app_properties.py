import os
from pathlib import Path
from types import ModuleType

from platformdirs import PlatformDirs

# Private constants
_ENVIRONMENT_PREFIX: str = "IMAGE_HARBOR"
_PLATFORM_DIRS: PlatformDirs | None = None


def _get_platform_dirs() -> PlatformDirs:
    global _PLATFORM_DIRS
    if not _PLATFORM_DIRS:
        _PLATFORM_DIRS = PlatformDirs(APP_NAME, False)
    return _PLATFORM_DIRS


def _print_properties():
    print("Application properties:")
    for name, value in sorted(globals().items()):
        if name.startswith("_"):
            continue
        if isinstance(value, ModuleType) or callable(value):
            continue
        print(f"{name}: {value}")


def get_from_env(var_name: str, default: str = None) -> str:
    return os.getenv(f"{_ENVIRONMENT_PREFIX}_{var_name}", default)


# Application properties
APP_NAME: str = "Image Harbor"
REPO_ROOT = Path(__file__).resolve().parent.parent
APP_DATA_PATH: Path = Path(get_from_env("APP_DATA_PATH", _get_platform_dirs().user_data_dir))
APP_CONFIG_PATH: Path = Path(get_from_env("APP_CONFIG_PATH", _get_platform_dirs().user_config_dir))
APP_CACHE_PATH: Path = Path(get_from_env("APP_CACHE_PATH", _get_platform_dirs().user_cache_dir))

# Print application properties
_print_properties()
