import argparse
import sys
from config import BASE, INVISIBLE_CHARS
from utils import number_to_base


def get_invisible_char_from_number(n: int) -> str:
    if 0 <= n <= len(INVISIBLE_CHARS):
        return INVISIBLE_CHARS[n]
    raise ValueError(f"Index must be in 0..{len(INVISIBLE_CHARS)-1}")


def text_to_base(text):
    number_from_text = int.from_bytes(text.encode("utf-8"), "big")
    return number_to_base(number_from_text)


def invisible_char_generator(int_in_base):
    for digit in int_in_base:
        invisible_char = get_invisible_char_from_number(int(digit, BASE))
        yield invisible_char


def sigil(text_to_sigil, sigal):
    int_in_base = text_to_base(sigal)
    invisible_char_gen = invisible_char_generator(int_in_base)
    sigiled_text = ""
    for char in text_to_sigil:
        invisible_char = next(invisible_char_gen, None)
        sigiled_text += char
        if invisible_char is not None:
            sigiled_text += invisible_char
    else:
        invisible_char = next(invisible_char_gen, None)
        if invisible_char is not None:
            print("❌ too long sigal!")
            return None
    return sigiled_text


def main():
    parser = argparse.ArgumentParser(description="Sigil processor")
    parser.add_argument("--input", required=True, help="File path")
    parser.add_argument("--signature", required=True, help="Text to put in file")
    parser.add_argument("--output", required=True, help="Ścieżka do pliku wyjściowego")

    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"❌ No such file: {args.input}")
        return

    result = sigil(file_content, args.signature)

    if result is None:
        sys.exit(1)

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✅ Done")
    except Exception as e:
        print(f"❌ Exception durring save to file: {e}")


if __name__ == "__main__":
    main()
