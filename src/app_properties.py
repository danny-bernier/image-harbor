from pathlib import Path
from typing import Final

from platformdirs import PlatformDirs

_PLATFORM_DIRS: Final[PlatformDirs] = PlatformDirs("image-harbor", False)

APP_DATA_PATH: Final[Path] = _PLATFORM_DIRS.user_data_path
APP_CONFIG_PATH: Final[Path] = _PLATFORM_DIRS.user_config_path
APP_CACHE_PATH: Final[Path] = _PLATFORM_DIRS.user_cache_path

print(f"Using app data directory: {APP_DATA_PATH}")
print(f"Using app config directory: {APP_CONFIG_PATH}")
print(f"Using app cache directory: {APP_CACHE_PATH}")
