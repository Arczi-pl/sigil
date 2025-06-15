"""Extracts a signature from a sigiled text containing invisible characters."""

from src.base_converter import custom_base
from src.config import Config


def get_invisible_chars_from_sigiled_text(text: str) -> list[str]:
    """
    Extract invisible characters from the sigiled text.

    Args:
        text: The text containing invisible characters.

    Returns:
        A list of invisible characters found in the text.

    """
    return [char for char in text if char in Config.INVISIBLE_CHARS]


def get_custom_base_number_from_invisible_chars(invisible_chars: list[str]) -> str:
    """
    Convert a list of invisible characters to a custom base number.

    Args:
        invisible_chars: A list of invisible characters.

    Returns:
        A string representing the number in a custom base.

    """
    return "".join(
        custom_base.encode(Config.INVISIBLE_CHARS.index(char))
        for char in invisible_chars
    )


def get_text_from_custom_base_numbner(custom_base_number: str) -> str:
    """
    Convert a custom base number to a UTF-8 string.

    Args:
        custom_base_number: A string representing the number in a custom base.

    Returns:
        The UTF-8 string representation of the number.

    """
    number = custom_base.decode(custom_base_number)
    byte_length = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_length, "big").decode("utf-8")


def decode(text: str) -> str:
    """
    Decode a sigiled text to extract the original text.

    Args:
        text: The text containing invisible characters.

    Returns:
        The original text extracted from the sigiled text.

    """
    invisible_chars = get_invisible_chars_from_sigiled_text(text)
    custom_base_number = get_custom_base_number_from_invisible_chars(invisible_chars)
    return get_text_from_custom_base_numbner(custom_base_number)
