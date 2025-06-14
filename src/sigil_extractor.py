
import argparse

from config import ALPHABET, BASE, INVISIBLE_CHARS
from utils import get_number_from_invisible_char_from_number


def get_digits_in_sigiled_text(sigiled_text):
    digits = ""
    for char in sigiled_text:
        if char in INVISIBLE_CHARS:
            char_digit = get_number_from_invisible_char_from_number(char)
            digits += str(char_digit)
    return digits

def base_to_int(s):
    val = 0
    for char in s:
        val = val * BASE + ALPHABET.index(char)
    return val

def text_from_int_in_base(base_string):
    num = base_to_int(base_string)
    byte_length = (num.bit_length() + 7) // 8
    return num.to_bytes(byte_length, "big").decode("utf-8")

def sigal(sigiled_text):
    int_in_base = get_digits_in_sigiled_text(sigiled_text)
    sigal = text_from_int_in_base(int_in_base)
    return sigal


def main():
    parser = argparse.ArgumentParser(description="Sigil processor")
    parser.add_argument("--input", required=True, help="File path")
    args = parser.parse_args()

    try:
        with open(args.input, encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"❌ no such file: {args.input}")
        return

    result = sigal(file_content)
    print(result)


if __name__ == "__main__":
    main()
