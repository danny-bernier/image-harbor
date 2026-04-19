"""Application entrypoint for local Image Harbor startup."""

from model.errors import StartupError
from startup import init_app
from util.log_util import Logger, get_logger

log: Logger = get_logger(__name__)

try:
    init_app()
except StartupError as exc:
    log.error(f"Application startup failed: {exc}")
    if exc.__cause__ is not None:
        log.debug(f"Startup failure cause: {exc.__cause__}")
    raise SystemExit(1) from None

print("God, not another one...")
