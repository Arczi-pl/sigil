from unittest.mock import patch

from src.config import Config
from src.decoder import (
    decode,
    get_custom_base_number_from_invisible_chars,
    get_invisible_chars_from_sigiled_text,
    get_text_from_custom_base_number,
)


def test_get_invisible_chars_from_sigiled_text() -> None:
    text = (
        f"H{Config.INVISIBLE_CHARS[0]}e{Config.INVISIBLE_CHARS[1]}"
        f"l{Config.INVISIBLE_CHARS[2]}lo"
    )
    expected = [
        Config.INVISIBLE_CHARS[0],
        Config.INVISIBLE_CHARS[1],
        Config.INVISIBLE_CHARS[2],
    ]
    assert get_invisible_chars_from_sigiled_text(text) == expected


def test_get_custom_base_number_from_invisible_chars() -> None:
    with patch("src.decoder.custom_base.encode", side_effect=["A", "B", "C"]):
        result = get_custom_base_number_from_invisible_chars(
            [
                Config.INVISIBLE_CHARS[0],
                Config.INVISIBLE_CHARS[1],
                Config.INVISIBLE_CHARS[2],
            ]
        )
        assert result == "ABC"


def test_get_text_from_custom_base_number() -> None:
    with patch("src.decoder.custom_base.decode", return_value=14844588):
        assert get_text_from_custom_base_number("euro") == "€"


def test_decode__no_invisible_chars() -> None:
    with (
        patch("src.decoder.get_invisible_chars_from_sigiled_text", return_value=[]),
        patch(
            "src.decoder.get_custom_base_number_from_invisible_chars",
            return_value="",
        ),
        patch("src.decoder.get_text_from_custom_base_number", return_value=""),
    ):
        assert decode("Hello") == ""


def test_decode__valid() -> None:
    text = f"H{Config.INVISIBLE_CHARS[1]}ello"

    with (
        patch(
            "src.decoder.get_invisible_chars_from_sigiled_text",
            return_value=[Config.INVISIBLE_CHARS[1]],
        ),
        patch(
            "src.decoder.get_custom_base_number_from_invisible_chars",
            return_value="A",
        ),
        patch("src.decoder.get_text_from_custom_base_number", return_value="Test"),
    ):
        assert decode(text) == "Test"
