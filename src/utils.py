"""Utility functions for sigil."""

from src.config import Config


def number_to_base(n: int) -> str:
    """
    Convert a number to a string in a given base using the ALPHABET.

    Args:
        n: The number to convert.

    Returns:
        The string representation of the number in the specified base.

    """
    if len(Config.INVISIBLE_CHARS) < Config.BASE:
        message = "Base is too big."
        raise ValueError(message)
    if n == 0:
        return Config.ALPHABET[0]
    digits = []
    while n:
        digits.append(Config.ALPHABET[n % Config.BASE])
        n //= Config.BASE
    return "".join(digits[::-1])


def get_number_from_invisible_char_from_number(c: str) -> str:
    """
    Get the index of an invisible character in the list of invisible characters.

    Args:
        c: The invisible character.

    Returns:
        The index of the invisible character in the list of invisible characters.

    Raises:
        ValueError: If the character is not in the list of invisible characters.

    """
    if not isinstance(c, str) or len(c) != 1:
        message = "Input must be a single character string."

        raise ValueError(message)
    if c in Config.INVISIBLE_CHARS:
        index = Config.INVISIBLE_CHARS.index(c)
        return number_to_base(index)
    message = "Character is not in the list of invisible characters."
    raise ValueError(message)
