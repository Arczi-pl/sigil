import pytest

from src.base_converter import CustomBaseConverter
from src.config import Config


def test_init_default() -> None:
    converter = CustomBaseConverter()
    assert converter.base == Config.BASE
    assert converter.alphabet == Config.ALPHABET


def test_init_custom() -> None:
    custom_base = 4
    custom_alphabet = "0123"
    converter = CustomBaseConverter(base=custom_base, alphabet=custom_alphabet)
    assert converter.base == custom_base
    assert converter.alphabet == custom_alphabet


def test_init_invalid() -> None:
    with pytest.raises(
        ValueError, match="Alphabet must be at least as long as the base"
    ):
        CustomBaseConverter(base=5, alphabet="0123")


def test_encode_zero() -> None:
    converter = CustomBaseConverter(base=10, alphabet="0123456789")
    assert converter.encode(0) == "0"


def test_encode_positive() -> None:
    converter = CustomBaseConverter(base=10, alphabet="0123456789")
    assert converter.encode(123) == "123"

    converter = CustomBaseConverter(base=2, alphabet="01")
    assert converter.encode(5) == "101"
    assert converter.encode(8) == "1000"

    converter = CustomBaseConverter(base=16, alphabet="0123456789abcdef")
    assert converter.encode(255) == "ff"
    assert converter.encode(3735928559) == "deadbeef"


def test_encode_negative() -> None:
    converter = CustomBaseConverter()
    with pytest.raises(ValueError, match="Negative numbers are not supported"):
        converter.encode(-1)


@pytest.mark.parametrize(
    ("expected", "number", "base", "alphabet"),
    [
        (0, "0", 10, "0123456789"),
        (123, "123", 10, "0123456789"),
        (5, "101", 2, "01"),
        (8, "1000", 2, "01"),
        (255, "ff", 16, "0123456789abcdef"),
        (3735928559, "deadbeef", 16, "0123456789abcdef"),
    ],
)
def test_decode(expected: int, number: str, base: int, alphabet: str) -> None:
    converter = CustomBaseConverter(base=base, alphabet=alphabet)
    assert converter.decode(number) == expected


def test_encode_decode_roundtrip() -> None:
    converter = CustomBaseConverter()

    for number in [0, 1, 42, 12345, 999999]:
        encoded = converter.encode(number)
        decoded = converter.decode(encoded)
        assert decoded == number
