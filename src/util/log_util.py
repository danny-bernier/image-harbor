import logging
import os
from logging import Logger

_DEFAULT_LOG_LEVEL = "INFO"
_LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
_ENVIRONMENT_LOG_LEVEL = "IMAGE_HARBOR_LOG_LEVEL"
_ENVIRONMENT_LOG_TIMESTAMP_FORMAT = "IMAGE_HARBOR_LOG_TIMESTAMP_FORMAT"


def get_logger(name: str) -> Logger:
    root_logger = logging.getLogger()

    if not root_logger.handlers:
        log_level_name = os.getenv(_ENVIRONMENT_LOG_LEVEL, _DEFAULT_LOG_LEVEL).upper()
        log_level = getattr(logging, log_level_name, logging.INFO)
        timestamp_format = os.getenv(_ENVIRONMENT_LOG_TIMESTAMP_FORMAT)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=timestamp_format))

        root_logger.addHandler(handler)
        root_logger.setLevel(log_level)

    return logging.getLogger(name)


def is_debug_enabled() -> bool:
    root_logger = logging.getLogger()
    return root_logger.isEnabledFor(logging.DEBUG)
