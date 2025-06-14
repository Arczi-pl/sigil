"""Configuration module for the application."""

import string
from typing import ClassVar


class Config:
    """Configuration class for the application."""

    INVISIBLE_CHARS: ClassVar[list[str]] = [
        "\u200c",
        "\u2062",
        "\u2063",
    ]
    BASE: ClassVar[int] = len(INVISIBLE_CHARS)
    ALPHABET: ClassVar[str] = (
        string.digits + string.ascii_lowercase + string.ascii_uppercase
    )
