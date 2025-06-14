#!/usr/bin/env python

"""Sigil processor to display invisible characters and their digits in a text file."""

import argparse
from pathlib import Path

from src.config import Config
from src.logger import logger
from src.utils import get_number_from_invisible_char_from_number


def show_chars_in_sigiled_text(sigiled_text: str) -> str:
    """
    Show invisible characters in a sigiled text as Unicode escape sequences.

    Args:
        sigiled_text: The text containing invisible characters.

    Returns:
        A string representation of the sigiled text with invisible characters shown
        as Unicode escape sequences.

    """
    text_to_show = ""
    for char in sigiled_text:
        if char in Config.INVISIBLE_CHARS:
            char_unicode_str = f"[\\u{ord(char):04x}]"
            text_to_show += char_unicode_str
        else:
            text_to_show += char
    return text_to_show


def show_digits_in_sigiled_text(sigiled_text: str) -> str:
    """
    Show digits corresponding to invisible characters in a sigiled text.

    Args:
        sigiled_text: The text containing invisible characters.

    Returns:
        A string representation of the sigiled text with digits corresponding to
        invisible characters.

    """
    text_to_show = ""
    for char in sigiled_text:
        if char in Config.INVISIBLE_CHARS:
            char_digit = get_number_from_invisible_char_from_number(char)
            text_to_show += f"[{char_digit}]"
        else:
            text_to_show += char
    return text_to_show


def main() -> None:
    """Process arguments and display the sigiled text."""
    parser = argparse.ArgumentParser(description="Sigil processor")
    parser.add_argument("--file", required=True, help="File path")
    args = parser.parse_args()

    try:
        with Path.open(args.file, encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        return

    logger.info("INVISIBLE_CHARS")
    logger.info(show_chars_in_sigiled_text(file_content))

    logger.info("\nDigits")
    logger.info(show_digits_in_sigiled_text(file_content))


main()
