
import abc
import copy
from typing import Optional, Any
from ..utils import safety_str

class MasterCipher(abc.ABC):
    """Base abstract base class to encrypt or decrpt CipherData"""

    @abc.abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        """_summary_
        """

    @abc.abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        """_summary_
        """

    @abc.abstractmethod
    def get_wrap_algorithm(self) -> str:
        """_summary_
        """

    @abc.abstractmethod
    def get_mat_desc(self) -> str:
        """_summary_
        """

class ContentCipher(abc.ABC):
    """Base abstract base class to encrypt or decrpt object's data"""

    @abc.abstractmethod
    def encrypt_content(self, data: Any) -> Any:
        """_summary_
        """

    @abc.abstractmethod
    def decrypt_content(self, data: Any) -> Any:
        """_summary_
        """

    @abc.abstractmethod
    def clone(self, **kwargs) -> "ContentCipher":
        """_summary_
        """

    @abc.abstractmethod
    def get_encrypted_len(self, plain_text_len: int) -> int:
        """_summary_
        """

    @abc.abstractmethod
    def get_cipher_data(self) -> "CipherData":
        """_summary_
        """

    @abc.abstractmethod
    def get_align_len(self) -> int:
        """_summary_
        """


class Envelope:
    """Envelope is stored in object's meta"""

    def __init__(
        self,
        iv: Optional[bytes] = None,
        cipher_key: Optional[bytes] = None,
        mat_desc: Optional[str] = None,
        wrap_algorithm: Optional[str] = None,
        cek_algorithm: Optional[str] = None,
        unencrypted_md5: Optional[str] = None,
        unencrypted_content_length: Optional[str] = None,
    ):
        self.iv = iv
        self.cipher_key = cipher_key
        self.mat_desc = mat_desc
        self.wrap_algorithm = wrap_algorithm
        self.cek_algorithm = cek_algorithm
        self.unencrypted_md5 = unencrypted_md5
        self.unencrypted_content_length = unencrypted_content_length

    def is_valid(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return (len(self.iv or b'') > 0 and
                len(self.cipher_key or b'') > 0 and
                safety_str(self.wrap_algorithm) != '' and
                safety_str(self.cek_algorithm) != '')


    def random_key_iv(self):
        """_summary_
        """

class CipherData:
    """CipherData is secret key information."""

    def __init__(
        self,
        iv: bytes = None,
        key: bytes = None,
        encrypted_iv: bytes = None,
        encrypted_key: bytes = None,
        mat_desc: str = None,
        wrap_algorithm: str = None,
        cek_algorithm: str = None,
    ):
        self.iv = iv
        self.key = key
        self.encrypted_iv = encrypted_iv
        self.encrypted_key = encrypted_key
        self.mat_desc = mat_desc
        self.wrap_algorithm = wrap_algorithm
        self.cek_algorithm = cek_algorithm

    def clone(self) -> "CipherData":
        """_summary_

        Returns:
            CipherData: _description_
        """
        return copy.deepcopy(self)

    def random_key_iv(self):
        """_summary_
        """


class ContentCipherBuilder(abc.ABC):
    """Base abstract base class to create ContentCipher"""

    @abc.abstractmethod
    def content_cipher(self) -> ContentCipher:
        """_summary_
        """

    @abc.abstractmethod
    def content_cipher_from_env(self, env: Envelope, **kwargs) -> ContentCipher:
        """_summary_
        """

    @abc.abstractmethod
    def get_mat_desc(self) -> str:
        """_summary_
        """
