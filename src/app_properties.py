import os
from pathlib import Path

from platformdirs import PlatformDirs

# Private constants
_ENVIRONMENT_PREFIX: str = "IMAGE_HARBOR"
_PLATFORM_DIRS: PlatformDirs = PlatformDirs("Image Harbor", False)

# Application properties
APP_DATA_PATH: Path = Path(os.getenv("APP_DATA_PATH", _PLATFORM_DIRS.user_data_dir))
APP_CONFIG_PATH: Path = Path(os.getenv("APP_CONFIG_PATH", _PLATFORM_DIRS.user_config_dir))
APP_CACHE_PATH: Path = Path(os.getenv("APP_CACHE_PATH", _PLATFORM_DIRS.user_cache_dir))

# Creating required directories if they do not exist
os.makedirs(APP_DATA_PATH, exist_ok=True)
os.makedirs(APP_CONFIG_PATH, exist_ok=True)
os.makedirs(APP_CACHE_PATH, exist_ok=True)

# Printing properties
print(f"Using app data directory: {APP_DATA_PATH}")
print(f"Using app config directory: {APP_CONFIG_PATH}")
print(f"Using app cache directory: {APP_CACHE_PATH}")


def get_from_env(var_name: str, default: str = None) -> str:
    return os.getenv(f"{_ENVIRONMENT_PREFIX}_{var_name}", default)
