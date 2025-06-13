from config import ALPHABET, BASE, INVISIBLE_CHARS


def number_to_base(n):
    if BASE > len(ALPHABET):
        raise ValueError("Za duża podstawa - maksymalnie {}".format(len(ALPHABET)))
    if n == 0:
        return ALPHABET[0]
    digits = []
    while n:
        digits.append(ALPHABET[n % BASE])
        n //= BASE
    return "".join(digits[::-1])


def get_number_from_invisible_char_from_number(c: str) -> int:
    if c in INVISIBLE_CHARS:
        index = INVISIBLE_CHARS.index(c)
        return number_to_base(index)
    raise ValueError("Character is not in the list of invisible characters")
