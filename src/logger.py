"""Logger configuration for the sigil."""

import sys

from loguru import logger

__all__ = ["logger"]

logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/app.log", rotation="1 MB", retention="7 days", level="DEBUG")
