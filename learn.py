import argparse
from config import INVISIBLE_CHARS
from utils import get_number_from_invisible_char_from_number


def show_chars_in_sigiled_text(sigiled_text):
    text_to_show = ""
    for char in sigiled_text:
        if char in INVISIBLE_CHARS:
            char_unicode_str = "[\\u{:04x}]".format(ord(char))
            text_to_show += char_unicode_str
        else:
            text_to_show += char
    return text_to_show


def show_digits_in_sigiled_text(sigiled_text):
    text_to_show = ""
    for char in sigiled_text:
        if char in INVISIBLE_CHARS:
            char_digit = get_number_from_invisible_char_from_number(char)
            text_to_show += f"[{char_digit}]"
        else:
            text_to_show += char
    return text_to_show


def main():
    parser = argparse.ArgumentParser(description="Sigil processor")
    parser.add_argument("--file", required=True, help="File path")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        return

    print("INVISIBLE_CHARS")
    print(show_chars_in_sigiled_text(file_content))

    print("\nDigits")
    print(show_digits_in_sigiled_text(file_content))


main()
