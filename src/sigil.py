#!/usr/bin/env python

"""
Sigil processor module.

This module provides functionality to process text files by adding invisible characters
as a signature based on a given input text.
"""

import argparse
import sys
from collections.abc import Generator
from pathlib import Path

from src.config import Config
from src.logger import logger
from src.utils import number_to_base


def get_invisible_char_from_number(n: int) -> str:
    """
    Get invisible character from number.

    Args:
        n: Index of the invisible character.

    Returns:
        The invisible character corresponding to the index.

    Raises:
        ValueError: If the index is out of range.

    """
    if 0 <= n <= Config.BASE:
        return Config.INVISIBLE_CHARS[n]
    message = f"Index must be in 0..{len(Config.INVISIBLE_CHARS) - 1}"
    raise ValueError(message)


def text_to_base(text: str) -> str:
    """
    Convert text to a number in a given base using the ALPHABET.

    Args:
        text: The text to convert.

    Returns:
        The string representation of the text in the specified base.

    """
    number_from_text = int.from_bytes(text.encode("utf-8"), "big")
    return number_to_base(number_from_text)


def invisible_char_generator(int_in_base: str) -> Generator[str]:
    """
    Return invisible characters based on base representation.

    Args:
        int_in_base: The string representation of the number in the specified base.

    Yields:
        Invisible characters corresponding to base representation.

    """
    for digit in int_in_base:
        invisible_char = get_invisible_char_from_number(int(digit, Config.BASE))
        yield invisible_char


def sigil(text_to_sigil: str, signature: str) -> str | None:
    """
    Apply a sigil to the text by inserting invisible characters based on the signature.

    Args:
        text_to_sigil: The text to which the sigil will be applied.
        signature: The signature text that will determine the invisible characters.

    Returns:
        The sigiled text with invisible characters inserted, or None if the signature
        is too long.

    """
    int_in_base = text_to_base(signature)
    invisible_char_gen = invisible_char_generator(int_in_base)
    sigiled_text = ""
    for char in text_to_sigil:
        invisible_char = next(invisible_char_gen, None)
        sigiled_text += char
        if invisible_char is not None:
            sigiled_text += invisible_char
    invisible_char = next(invisible_char_gen, None)
    if invisible_char is not None:
        logger.info("❌ too long sigal!")
        return None
    return sigiled_text


def main() -> None:
    """Process command line arguments and apply the sigil."""
    parser = argparse.ArgumentParser(description="Sigil processor")
    parser.add_argument("--input", required=True, help="File path")
    parser.add_argument("--signature", required=True, help="Text to put in file")
    parser.add_argument("--output", required=True, help="Ścieżka do pliku wyjściowego")

    args = parser.parse_args()

    try:
        with Path.open(args.input, encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        logger.info(f"❌ No such file: {args.input}")
        return

    result = sigil(file_content, args.signature)

    if result is None:
        sys.exit(1)

    try:
        with Path.open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        logger.info("✅ Done")
    except Exception as e:  # noqa: BLE001
        logger.info(f"❌ Exception durring save to file: {e}")


if __name__ == "__main__":
    main()
