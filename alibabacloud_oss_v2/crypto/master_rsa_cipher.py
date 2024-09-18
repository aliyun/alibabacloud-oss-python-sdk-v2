import json
from typing import Optional,  Dict
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from .types import MasterCipher

class MasterRsaCipher(MasterCipher):
    """MasterRsaCipher implements rsa master key interface
    """
    def __init__(
        self,
        mat_desc: Optional[Dict] = None,
        public_key: Optional[str] = None,
        private_key: Optional[str] = None,
    ):
        self._public_key = public_key
        self._private_key = private_key
        self._mat_desc = None
        if mat_desc is not None and len(mat_desc.items()) > 0:
            self._mat_desc = json.dumps(mat_desc)

        self._encrypt_obj = None
        if public_key is not None:
            self._encrypt_obj = PKCS1_v1_5.new(RSA.importKey(public_key))

        self._decrypt_obj = None
        if private_key is not None:
            self._decrypt_obj = PKCS1_v1_5.new(RSA.importKey(private_key))


    def get_wrap_algorithm(self) -> str:
        return 'RSA/NONE/PKCS1Padding'

    def get_mat_desc(self) -> str:
        return self._mat_desc or ''

    def encrypt(self, data: bytes) -> bytes:
        if self._encrypt_obj is None:
            raise ValueError('RSA public key is none or invalid.')

        return self._encrypt_obj.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        if self._decrypt_obj is None:
            raise ValueError('RSA private key is none or invalid.')
        decrypted_data =  self._decrypt_obj.decrypt(data, object)
        if decrypted_data == object:
            raise ValueError('Decrypted data error, please check RSA private key!')
        return decrypted_data
