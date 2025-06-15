"""
Sigil processor module.

This module provides functionality to process text files by adding invisible characters
as a signature based on a given input text.
"""

import math
from collections.abc import Generator
from contextlib import suppress

from src.base_converter import custom_base
from src.config import Config
from src.logger import logger


def get_max_signature_len(text: str, *, base: int = Config.BASE) -> int:
    """
    Calculate the maximum length of a signature that can be embedded in the text.

    The maximum length is determined by the length of the text and the base used for
    encoding.

    Args:
        text: The text in which the signature will be embedded.
        base: The base used for encoding (default is Config.BASE).

    Returns:
        The maximum length of the signature that can be embedded in the text.

    """
    return math.floor(len(text) * math.log2(base) / 8)


def get_number_from_text(text: str) -> int:
    """
    Convert text to a number using UTF-8 encoding.

    Args:
        text: The text to convert.

    Returns:
        The integer value of the text encoded in UTF-8.

    """
    return int.from_bytes(text.encode("utf-8"), "big")


def get_invisible_char_from_number(number: int) -> str:
    """
    Get an invisible character corresponding to a number in the custom base.

    Args:
        number: The number to convert to an invisible character.

    Returns:
        The invisible character corresponding to the number.

    """
    return Config.INVISIBLE_CHARS[number]


def invisible_char_generator(custom_base_number: str) -> Generator[str]:
    """
    Yield invisible characters based on base representation.

    Args:
        custom_base_number: The representation of the number in the specified base.

    Yields:
        Invisible characters corresponding to base representation.

    """
    for custom_base_digit in custom_base_number:
        digit = custom_base.decode(custom_base_digit)
        yield get_invisible_char_from_number(digit)


def encode(text: str, signature: str) -> str | None:
    """
    Encode the text by embedding a signature using invisible characters.

    Args:
        text: The text to encode.
        signature: The signature to embed in the text.

    Returns:
        The encoded text with the signature embedded using invisible characters,
        or None if the signature is too long to be embedded.

    """
    if not signature:
        logger.error("❌ Signature is empty!")
        return None
    max_signature_len = get_max_signature_len(text)
    if len(signature) > max_signature_len:
        logger.error(
            f"❌ Signature is too long! Maximum length is {max_signature_len}."
        )
        return None

    number = get_number_from_text(signature)
    custom_base_number = custom_base.encode(number)
    invisible_chars = invisible_char_generator(custom_base_number)

    result = []
    for char in text:
        result.append(char)
        with suppress(StopIteration):
            result.append(next(invisible_chars))

    try:
        next(invisible_chars)
    except StopIteration:
        return "".join(result)
    else:
        logger.error("❌ Too long signature! Not all characters could be embedded.")
        return None
