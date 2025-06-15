"""Convert numbers between different bases using a custom alphabet."""

from src.config import Config
from src.logger import logger


class CustomBaseConverter:
    """Class to convert numbers between different bases using a custom alphabet."""

    def __init__(
        self, base: int = Config.BASE, alphabet: str = Config.ALPHABET
    ) -> None:
        if base > len(alphabet):
            message = "Alphabet must be at least as long as the base."
            logger.error(message)
            raise ValueError(message)

        self.base = base
        self.alphabet = alphabet

    def decode(
        self,
        number: str,
    ) -> int:
        """
        Convert a string in a given base to an integer number.

        Args:
            number: The string to convert.
            base: The base of the number system (default is Config.BASE).
            alpabet: The alphabet used for the base (default is Config.ALPHABET).

        Returns:
            The integer value of the string in the specified base.

        """
        return sum(
            self.alphabet.index(char) * (self.base**exp)
            for exp, char in enumerate(reversed(number))
        )

    def encode(
        self,
        number: int,
    ) -> str:
        """
        Convert a number to a string in a given base using the ALPHABET.

        Args:
            number: The number to convert.
            base: The base of the number system (default is Config.BASE).
            alphabet: The alphabet used for the base (default is Config.ALPHABET).

        Returns:
            The string representation of the number in the specified base.

        """

        def _to_custom_base(number: int) -> list[int]:
            digits = []
            while number:
                digits.append(number % self.base)
                number //= self.base
            return digits

        if number < 0:
            message = "Negative numbers are not supported."
            logger.error(message)
            raise ValueError(message)

        if number == 0:
            return self.alphabet[0]

        return "".join(self.alphabet[d] for d in reversed(_to_custom_base(number)))


custom_base = CustomBaseConverter(base=Config.BASE, alphabet=Config.ALPHABET)
