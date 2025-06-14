import string

INVISIBLE_CHARS = [
    "\u200c" , "\u2062" , "\u2063",
]
BASE = len(INVISIBLE_CHARS)
ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
