
import abc
import copy
from typing import Optional, Any
from ..utils import safety_str

class MasterCipher(abc.ABC):
    """Base abstract base class to encrypt or decrpt CipherData"""

    @abc.abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        """encrypt data
        """

    @abc.abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        """decrypt data
        """

    @abc.abstractmethod
    def get_wrap_algorithm(self) -> str:
        """get wrap algorithm
        """

    @abc.abstractmethod
    def get_mat_desc(self) -> str:
        """get mat desc
        """

class ContentCipher(abc.ABC):
    """Base abstract base class to encrypt or decrpt object's data"""

    @abc.abstractmethod
    def encrypt_content(self, data: Any) -> Any:
        """encrypt content
        """

    @abc.abstractmethod
    def decrypt_content(self, data: Any) -> Any:
        """decrypt content
        """

    @abc.abstractmethod
    def clone(self, **kwargs) -> "ContentCipher":
        """clone
        """

    @abc.abstractmethod
    def get_encrypted_len(self, plain_text_len: int) -> int:
        """get encrypted len
        """

    @abc.abstractmethod
    def get_cipher_data(self) -> "CipherData":
        """get cipher data
        """

    @abc.abstractmethod
    def get_align_len(self) -> int:
        """get align len
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
        """is valid

        Returns:
            bool: _description_
        """
        return (len(self.iv or b'') > 0 and
                len(self.cipher_key or b'') > 0 and
                safety_str(self.wrap_algorithm) != '' and
                safety_str(self.cek_algorithm) != '')


    def random_key_iv(self):
        """random key iv
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
        """clone

        Returns:
            CipherData: _description_
        """
        return copy.deepcopy(self)

    def random_key_iv(self):
        """random key iv
        """


class ContentCipherBuilder(abc.ABC):
    """Base abstract base class to create ContentCipher"""

    @abc.abstractmethod
    def content_cipher(self) -> ContentCipher:
        """content cipher
        """

    @abc.abstractmethod
    def content_cipher_from_env(self, env: Envelope, **kwargs) -> ContentCipher:
        """content cipher from env
        """

    @abc.abstractmethod
    def get_mat_desc(self) -> str:
        """get mat desc
        """
