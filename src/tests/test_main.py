import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.main import (
    get_file_content,
    main,
    write_file_content,
)


def test_get_file_content__existing_file() -> None:
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write("Test content")
        temp_file_path = Path(temp_file.name)

    try:
        content = get_file_content(temp_file_path)
        assert content == "Test content"
    finally:
        Path.unlink(temp_file_path)


def test_get_file_content__nonexistent_file() -> None:
    non_existent_path = Path("/path/to/nonexistent/file")
    with pytest.raises(FileNotFoundError):
        get_file_content(non_existent_path)


def test_write_file_content() -> None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = Path(temp_file.name)

    try:
        write_file_content(temp_file_path, "New content")

        with Path.open(temp_file_path, encoding="utf-8") as file:
            content = file.read()

        assert content == "New content"
    finally:
        Path.unlink(temp_file_path)


def test_encode_mode() -> None:
    test_content = "Test content"
    test_signature = "Test signature"
    encoded_content = "Encoded content"

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = Path(temp_file.name)
        temp_file.write(test_content.encode())

    try:
        with (
            patch("sys.argv", ["sigil", str(temp_file_path), test_signature]),
            patch("src.main.get_file_content", return_value=test_content),
            patch("src.main.sigil_encoder.encode", return_value=encoded_content),
            patch("src.main.write_file_content") as mock_write,
        ):
            main()

            mock_write.assert_called_once()
            args, _ = mock_write.call_args

            assert "__sigiled" in str(args[0])
            assert args[1] == encoded_content

    finally:
        Path.unlink(temp_file_path)


def test_encode_mode__error() -> None:
    test_content = "Test content"
    test_signature = "Test signature"

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = Path(temp_file.name)
        temp_file.write(test_content.encode())

    try:
        with (
            patch("sys.argv", ["sigil", str(temp_file_path), test_signature]),
            patch("src.main.get_file_content", return_value=test_content),
            patch("src.main.sigil_encoder.encode", return_value=None),
            patch("sys.exit") as mock_exit,
        ):
            main()

            mock_exit.assert_called_once_with(1)

    finally:
        Path.unlink(temp_file_path)


def test_decode_mode() -> None:
    test_content = "Encoded content"
    decoded_content = "Decoded signature"

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = Path(temp_file.name)
        temp_file.write(test_content.encode())

    try:
        with (
            patch("sys.argv", ["sigil", str(temp_file_path)]),
            patch("src.main.get_file_content", return_value=test_content),
            patch("src.main.sigil_decoder.decode", return_value=decoded_content),
            patch("src.main.logger.info") as mock_logger,
        ):
            main()

            mock_logger.assert_called_once_with(decoded_content)

    finally:
        Path.unlink(temp_file_path)
