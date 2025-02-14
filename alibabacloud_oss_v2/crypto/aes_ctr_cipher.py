
from typing import Any
from .types import (
    ContentCipherBuilder,
    MasterCipher,
    ContentCipher,
    CipherData,
    Envelope
)
from .aes_ctr import _AesCtr

class _AESCtrCipher(ContentCipher):
    def __init__(
        self,
        cipher_data: CipherData,
        offset: int
    ):
        self._cipher_data = cipher_data
        self._cipher = _AesCtr(cipher_data, offset)

    def encrypt_content(self, data: Any) -> Any:
        """encrypt content
        """
        return self._cipher.encrypt(data)

    def decrypt_content(self, data: Any) -> Any:
        """decrypt content
        """
        reader = self._cipher.decrypt(data)
        return reader

    def clone(self, **kwargs) -> ContentCipher:
        """clone
        """
        return _AESCtrCipher(
            cipher_data=self._cipher_data,
            offset = kwargs.get("offset", 0)
        )

    def get_encrypted_len(self, plain_text_len: int) -> int:
        """AES CTR encryption mode does not change content length
        """
        return plain_text_len

    def get_cipher_data(self) -> CipherData:
        return self._cipher_data

    def get_align_len(self) -> int:
        return len(self._cipher_data.iv)


class AESCtrCipherBuilder(ContentCipherBuilder):
    """AES Ctr Cipher Builder

    Args:
        ContentCipherBuilder (_type_): _description_
    """
    def __init__(
        self,
        master_cipher: MasterCipher,
    ):
        self.master_cipher = master_cipher

    def content_cipher(self) -> ContentCipher:
        cd = self._create_cipher_data()
        return self._content_cipher_from_cd(cd, 0)

    def content_cipher_from_env(self, env: Envelope, **kwargs) -> ContentCipher:
        encrypted_key = env.cipher_key
        encrypted_iv = env.iv
        key = self.master_cipher.decrypt(encrypted_key)
        iv = self.master_cipher.decrypt(encrypted_iv)
        offset = kwargs.get("offset", 0)
        return self._content_cipher_from_cd(
            CipherData(
                key=key,
                iv=iv,
                encrypted_key=encrypted_key,
                encrypted_iv=encrypted_iv,
                wrap_algorithm=env.wrap_algorithm,
                cek_algorithm=env.cek_algorithm,
                mat_desc=env.mat_desc
            ),
            offset)

    def get_mat_desc(self) -> str:
        return self.master_cipher.get_mat_desc()

    def _create_cipher_data(self) -> CipherData:
        key = _AesCtr.random_key()
        iv = _AesCtr.random_iv()
        encrypted_key = self.master_cipher.encrypt(key)
        encrypted_iv = self.master_cipher.encrypt(iv)
        return CipherData(
            key=key,
            iv=iv,
            encrypted_key=encrypted_key,
            encrypted_iv=encrypted_iv,
            wrap_algorithm=self.master_cipher.get_wrap_algorithm(),
            cek_algorithm='AES/CTR/NoPadding',
            mat_desc=self.master_cipher.get_mat_desc()
        )

    def _content_cipher_from_cd(self, cd:CipherData, offset: int) -> ContentCipher:
        return _AESCtrCipher(cipher_data=cd, offset=offset)
