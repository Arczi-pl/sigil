#!/usr/bin/env python

"""Extracts a signature from a sigiled text containing invisible characters."""

import argparse
from pathlib import Path

from src.config import Config
from src.logger import logger
from src.utils import get_number_from_invisible_char_from_number


def get_digits_in_sigiled_text(sigiled_text: str) -> str:
    """
    Extract digits from a sigiled text.

    Args:
        sigiled_text: The text containing invisible characters.

    Returns:
        A string of digits corresponding to the invisible characters in the text.

    """
    digits = ""
    for char in sigiled_text:
        if char in Config.INVISIBLE_CHARS:
            char_digit = get_number_from_invisible_char_from_number(char)
            digits += str(char_digit)
    return digits


def base_to_int(s: str) -> int:
    """
    Convert a string in a given base (using Config.ALPHABET) to an integer.

    Args:
        s: The string to convert.

    Returns:
        The integer value of the string in the specified base.

    """
    val = 0
    for char in s:
        val = val * Config.BASE + Config.ALPHABET.index(char)
    return val


def text_from_int_in_base(base_string: str) -> str:
    """
    Convert a string in a given base (using Config.ALPHABET) to a UTF-8 string.

    Args:
        base_string: The string to convert.

    Returns:
        The UTF-8 string representation of the number in the specified base.

    """
    num = base_to_int(base_string)
    byte_length = (num.bit_length() + 7) // 8
    return num.to_bytes(byte_length, "big").decode("utf-8")


def extract_sigil(sigiled_text: str) -> str:
    """
    Convert a sigiled text to a signature (UTF-8 string).

    Args:
        sigiled_text: The text containing invisible characters.

    Returns:
        The UTF-8 string representation of the signature text.

    """
    int_in_base = get_digits_in_sigiled_text(sigiled_text)
    return text_from_int_in_base(int_in_base)


def main() -> None:
    """Process the input file and extract the sigil."""
    parser = argparse.ArgumentParser(description="Sigil processor")
    parser.add_argument("--input", required=True, help="File path")
    args = parser.parse_args()

    try:
        with Path.open(args.input, encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        logger.info(f"❌ no such file: {args.input}")
        return

    result = extract_sigil(file_content)
    logger.info(result)


if __name__ == "__main__":
    main()
