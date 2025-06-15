#!/usr/bin/env python

"""
Sigil processor module.

This module provides functionality to process text files by adding invisible characters
as a signature based on a given input text.
"""

import argparse
import sys
from pathlib import Path

import src.decoder as sigil_decoder
import src.encoder as sigil_encoder
from src.logger import logger


def get_file_content(path: Path) -> str:
    """
    Read the content of a file.

    Args:
        path: The path to the file to read.

    Returns:
        The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist.

    """
    try:
        with Path.open(path, encoding="utf-8") as file:
            file_content = file.read()
    except FileNotFoundError:
        logger.exception(f"❌ No such file: {path}")
        raise
    else:
        return file_content


def write_file_content(path: Path, content: str) -> None:
    """
    Write content to a file.

    Args:
        path: The path to the file to write.
        content: The content to write to the file.

    Raises:
        Exception: If there is an error writing to the file.

    """
    try:
        with Path.open(path, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as err:  # noqa: BLE001
        logger.exception(f"❌ Exception during save to file: {err}")


def main() -> None:
    """Process command line arguments and apply the sigil."""
    parser = argparse.ArgumentParser(description="Sigil processor")
    parser.add_argument("file_path", help="File path", type=Path)
    parser.add_argument("signature", help="Text to put in file", type=str, nargs="?")
    args = parser.parse_args()

    file_content = get_file_content(args.file_path)
    if args.signature:
        encoded_content = sigil_encoder.encode(file_content, args.signature)
        if encoded_content is None:
            sys.exit(1)
        write_file_content(
            args.file_path.with_name(
                args.file_path.stem + "__sigiled" + args.file_path.suffix
            ),
            encoded_content,
        )
    else:
        file_content = get_file_content(args.file_path)
        decoded_content = sigil_decoder.decode(file_content)
        logger.info(decoded_content)


if __name__ == "__main__":
    main()  # coverage: ignore
