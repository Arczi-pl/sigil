"""Logger configuration for the sigil."""

import sys

from loguru import logger

__all__ = ["logger"]

logger.remove()
logger.add(sys.stderr, level="INFO", format="{message}")
