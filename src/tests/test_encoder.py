from unittest.mock import patch

import pytest

from src.config import Config
from src.encoder import (
    encode,
    get_invisible_char_from_number,
    get_number_from_text,
    invisible_char_generator,
)


@pytest.mark.parametrize(
    ("text", "expected_number"),
    [
        ("A", 65),
        ("AB", 16706),
    ],
)
def test_get_number_from_text(text: str, expected_number: int) -> None:
    assert get_number_from_text(text) == expected_number


def test_get_invisible_char_from_number__valid() -> None:
    for i in range(len(Config.INVISIBLE_CHARS)):
        assert get_invisible_char_from_number(i) == Config.INVISIBLE_CHARS[i]


def test_get_invisible_char_from_number__invalid() -> None:
    with pytest.raises(IndexError):
        get_invisible_char_from_number(len(Config.INVISIBLE_CHARS))


def test_invisible_char_generator() -> None:
    generator = invisible_char_generator("012")
    assert next(generator) == Config.INVISIBLE_CHARS[0]
    assert next(generator) == Config.INVISIBLE_CHARS[1]
    assert next(generator) == Config.INVISIBLE_CHARS[2]
    with pytest.raises(StopIteration):
        next(generator)


def test_encode__empty_signature() -> None:
    assert encode("Hello World", "") is None


def test_encode__valid() -> None:
    text = "Hello World! This is a test."
    signature = "AS"

    with (
        patch("src.encoder.get_number_from_text", return_value=65),
        patch("src.encoder.custom_base.encode", return_value="1"),
        patch(
            "src.encoder.invisible_char_generator",
            return_value=iter([Config.INVISIBLE_CHARS[1]]),
        ),
    ):
        encoded = encode(text, signature)

        assert encoded == f"H{Config.INVISIBLE_CHARS[1]}e{text[2:]}"


def test_encode__not_valid() -> None:
    text = "Hello World!"
    signature = "Very Long Signature."

    with (
        patch("src.encoder.get_number_from_text", return_value=65),
        patch(
            "src.encoder.custom_base.encode", return_value="0120012012210021120120120"
        ),
        patch(
            "src.encoder.logger.error",
        ) as logger_mock,
    ):
        encoded = encode(text, signature)

        assert encoded is None
        logger_mock.assert_called_once_with(
            "❌ Too long signature! Not all characters could be embedded."
        )
