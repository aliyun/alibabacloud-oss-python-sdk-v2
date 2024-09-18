import abc
from typing import Any

class Encrypter(abc.ABC):
    """Encrypter is interface with only encrypt method"""

    @abc.abstractmethod
    def encrypt(self, reader: Any) -> Any:
        """_summary_
        """


class Decrypter(abc.ABC):
    """Decrypter is interface with only decrypt method"""

    @abc.abstractmethod
    def decrypt(self, reader: Any) -> Any:
        """_summary_
        """

class Cipher(Encrypter, Decrypter):
    """_summary_
    """
