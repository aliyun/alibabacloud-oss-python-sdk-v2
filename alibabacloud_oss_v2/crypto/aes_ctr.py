
import struct
from typing import Any, Iterator, Iterable, AnyStr
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
from ..types import StreamBody
from .types import CipherData

_KEY_LEN = 32
_BLOCK_SIZE_LEN = 16
_BLOCK_BITS_LEN = 8 * 16

def _iv_to_big_int(iv: bytes) -> int:
    iv_high_low_pair = struct.unpack(">QQ", iv)
    iv_big_int = iv_high_low_pair[0] << 64 | iv_high_low_pair[1]
    return iv_big_int
  
class IteratorEncryptor():
    """Iterator Encryptor
    """

    def __init__(
        self,
        iterator: Iterator,
        cipher_data: CipherData,
        counter: int
    ) -> None:
        self._iterator = iterator
        self._cipher_data = cipher_data
        self._counter = counter

        ctr = Counter.new(_BLOCK_BITS_LEN, initial_value=self._counter)
        self._cipher =  AES.new(self._cipher_data.key, AES.MODE_CTR, counter=ctr)
        self._finished = False
        self._remains_bytes = None

    def __iter__(self):
        return self

    def __next__(self):

        if self._finished:
            raise StopIteration

        data = self._remains_bytes or b''
        self._remains_bytes = None
        try:
            while True:
                d = next(self._iterator)
                if isinstance(d, int):
                    d = d.to_bytes()
                elif isinstance(d, str):
                    d = d.encode()
                if len(d) < _BLOCK_SIZE_LEN:
                    data += d
                else:
                    if len(data) > 0:
                        data += d
                    else:
                        data = d
                if len(data) >= _BLOCK_SIZE_LEN:
                    data_len = len(data)
                    align_len = (data_len // _BLOCK_SIZE_LEN) * _BLOCK_SIZE_LEN
                    edata = self._cipher.encrypt(data[:align_len])
                    if data_len > align_len:
                        self._remains_bytes = data[align_len:]
                    return edata
        except StopIteration as err:
            self._finished = True
            if len(data) > 0:
                return self._cipher.encrypt(data)
            raise err

class IterableEncryptor():
    """Iterable Encryptor
    """

    def __init__(
        self,
        iterable: Iterable,
        cipher_data: CipherData,
        counter: int
    ) -> None:
        self._iterable = iterable
        self._cipher_data = cipher_data
        self._counter = counter

    def __iter__(self):
        return IteratorEncryptor(
            iterator=iter(self._iterable),
            cipher_data=self._cipher_data,
            counter=self._counter)

class FileLikeEncryptor():
    """File Like Encryptor
    """
    def __init__(
        self,
        reader: Any,
        cipher_data: CipherData,
        offset: int
    ) -> None:
        self._reader = reader
        self._cipher_data = cipher_data
        self._cipher = None
        self._base = reader.tell()
        self._roffset = self._base
        self._offset = offset

    def read(self, n: int = -1) -> AnyStr:
        """read

        Args:
            n (int, optional): _description_. Defaults to -1.

        Returns:
            AnyStr: _description_
        """
        if self._cipher is None:
            reloffset = self._roffset - self._base
            if not 0 == reloffset % _BLOCK_SIZE_LEN:
                raise ValueError('relative offset is not align to encrypt block')
            counter = _iv_to_big_int(self._cipher_data.iv) + (self._offset + reloffset)//_BLOCK_SIZE_LEN
            ctr = Counter.new(_BLOCK_BITS_LEN, initial_value=counter)
            self._cipher = AES.new(self._cipher_data.key, AES.MODE_CTR, counter=ctr)

        if n >= 0 and  0 != n % _BLOCK_SIZE_LEN:
            raise ValueError('n is not align to encrypt block')

        return self._cipher.encrypt(self._reader.read(n))

    def seek(self, offset: int, whence: int = 0) -> int:
        """seek

        Args:
            offset (int): _description_
            whence (int, optional): _description_. Defaults to 0.

        Returns:
            int: _description_
        """
        offset = self._reader.seek(offset, whence)
        if offset < self._base:
            raise ValueError(f'Offset {offset} is less than base {self._base}, can not creates cipher.')

        self._roffset = offset
        self._cipher = None
        return offset

    def tell(self) -> int:
        """tell
        """
        return self._reader.tell()


class StreamBodyDecryptor(StreamBody):
    """Stream Body Decryptor
    """
    def __init__(
        self,
        stream: StreamBody,
        cipher_data: CipherData,
        counter: int
    ) -> None:
        self._stream = stream
        self._cipher_data = cipher_data
        self._counter = counter

    def __enter__(self) -> "StreamBodyDecryptor":
        self._stream.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self._stream.__exit__(*args)

    @property
    def is_closed(self) -> bool:
        return self._stream.is_closed

    @property
    def is_stream_consumed(self) -> bool:
        return self._stream.is_stream_consumed

    @property
    def content(self) -> bytes:
        if not self._stream.is_stream_consumed:
            self._stream.read()
        return self._get_cipher().decrypt(self._stream.content)

    def read(self) -> bytes:
        return self._get_cipher().decrypt(self._stream.read())

    def close(self) -> None:
        self._stream.close()

    def iter_bytes(self, **kwargs: Any) -> Iterator[bytes]:
        cipher = self._get_cipher()
        for d in self._stream.iter_bytes(**kwargs):
            yield cipher.decrypt(d)

    def _get_cipher(self):
        ctr = Counter.new(_BLOCK_BITS_LEN, initial_value=self._counter)
        return AES.new(self._cipher_data.key, AES.MODE_CTR, counter=ctr)


class _AesCtr:
    def __init__(
        self,
        cipher_data: CipherData,
        offset: int
    ):
        self.cipher_data = cipher_data
        self.offset = offset
        if not 0 == offset % _BLOCK_SIZE_LEN:
            raise ValueError('offset is not align to encrypt block')
        self.counter = _iv_to_big_int(cipher_data.iv) + offset//_BLOCK_SIZE_LEN
        self.no_bytes = False
        self.no_str = False

    def encrypt(self, src: Any) -> Any:
        """encrypt data
        """
        if not self.no_str and isinstance(src, str):
            return self._get_cipher().encrypt(src.encode())

        if not self.no_bytes and isinstance(src, bytes):
            return self._get_cipher().encrypt(src)

        # file-like object
        if hasattr(src, 'seek') and hasattr(src, 'read'):
            return FileLikeEncryptor(reader=src, cipher_data=self.cipher_data, offset=self.offset)

        if isinstance(src, Iterator):
            return IteratorEncryptor(iterator=src, cipher_data=self.cipher_data, counter=self.counter)

        if isinstance(src, Iterable):
            return IterableEncryptor(iterable=src, cipher_data=self.cipher_data, counter=self.counter)

        raise TypeError(f'src is not str/bytes/file-like/Iterable type, got {type(src)}')

    def decrypt(self, src: Any) -> Any:
        """decrypt data

        Args:
            src (Any): _description_

        Returns:
            Any: _description_
        """
        if isinstance(src, bytes):
            return self._get_cipher().decrypt(src)

        if not isinstance(src, StreamBody):
            raise TypeError(f'src is not StreamBody type, got {type(src)}')

        return StreamBodyDecryptor(src, self.cipher_data, self.counter)

    def _get_cipher(self):
        ctr = Counter.new(_BLOCK_BITS_LEN, initial_value=self.counter)
        return AES.new(self.cipher_data.key, AES.MODE_CTR, counter=ctr)

    @staticmethod
    def random_key() -> bytes:
        """random key

        Returns:
            bytes: _description_
        """
        return Random.new().read(_KEY_LEN)

    @staticmethod
    def random_iv() -> bytes:
        """random iv

        Returns:
            bytes: _description_
        """
        iv = Random.new().read(16)
        safe_iv = iv[0:8] + struct.pack(">L", 0) + iv[12:]
        return safe_iv
