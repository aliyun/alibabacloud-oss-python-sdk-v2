import abc
from typing import Any

class Encrypter(abc.ABC):
    """Encrypter is interface with only encrypt method"""

    @abc.abstractmethod
    def encrypt(self, reader: Any) -> Any:
        """encrypt
        """


class Decrypter(abc.ABC):
    """Decrypter is interface with only decrypt method"""

    @abc.abstractmethod
    def decrypt(self, reader: Any) -> Any:
        """decrypt
        """

class Cipher(Encrypter, Decrypter):
    """Cipher
    """
