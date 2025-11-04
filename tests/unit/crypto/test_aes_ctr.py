# pylint: skip-file
import unittest
import io
import sys
import base64
from typing import cast, Any, Iterator
from alibabacloud_oss_v2.types import StreamBody
import alibabacloud_oss_v2.crypto.master_rsa_cipher as  rsa_cipher
import alibabacloud_oss_v2.crypto.aes_ctr as  aes_ctr
from alibabacloud_oss_v2.crypto.types import CipherData


rsa_private = """-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCokfiAVXXf5ImFzKDw+XO/UByW6mse2QsIgz3ZwBtMNu59fR5z
ttSx+8fB7vR4CN3bTztrP9A6bjoN0FFnhlQ3vNJC5MFO1PByrE/MNd5AAfSVba93
I6sx8NSk5MzUCA4NJzAUqYOEWGtGBcom6kEF6MmR1EKib1Id8hpooY5xaQIDAQAB
AoGAOPUZgkNeEMinrw31U3b2JS5sepG6oDG2CKpPu8OtdZMaAkzEfVTJiVoJpP2Y
nPZiADhFW3e0ZAnak9BPsSsySRaSNmR465cG9tbqpXFKh9Rp/sCPo4Jq2n65yood
JBrnGr6/xhYvNa14sQ6xjjfSgRNBSXD1XXNF4kALwgZyCAECQQDV7t4bTx9FbEs5
36nAxPsPM6aACXaOkv6d9LXI7A0J8Zf42FeBV6RK0q7QG5iNNd1WJHSXIITUizVF
6aX5NnvFAkEAybeXNOwUvYtkgxF4s28s6gn11c5HZw4/a8vZm2tXXK/QfTQrJVXp
VwxmSr0FAajWAlcYN/fGkX1pWA041CKFVQJAG08ozzekeEpAuByTIOaEXgZr5MBQ
gBbHpgZNBl8Lsw9CJSQI15wGfv6yDiLXsH8FyC9TKs+d5Tv4Cvquk0efOQJAd9OC
lCKFs48hdyaiz9yEDsc57PdrvRFepVdj/gpGzD14mVerJbOiOF6aSV19ot27u4on
Td/3aifYs0CveHzFPQJAWb4LCDwqLctfzziG7/S7Z74gyq5qZF4FUElOAZkz718E
yZvADwuz/4aK0od0lX9c4Jp7Mo5vQ4TvdoBnPuGoyw==
-----END RSA PRIVATE KEY-----"""


class StubStreamBody(StreamBody):
    def __init__(
        self,
        data: bytes,
    ) -> None:
        self._data = data
    def __enter__(self) -> "StubStreamBody":
        return self

    def __exit__(self, *args: Any) -> None:
        pass

    @property
    def is_closed(self) -> bool:
        return False

    @property
    def is_stream_consumed(self) -> bool:
        return False

    @property
    def content(self) -> bytes:
        return self._data


    def read(self) -> bytes:
        return self._data

    def close(self) -> None:
        pass

    def iter_bytes(self, **kwargs: Any) -> Iterator[bytes]:
        block_size = kwargs.get("block_size", 4 * 1024)
        for d in range(0, len(self._data), block_size):
            end = d + block_size
            if end > len(self._data):
                end = len(self._data)
            yield self._data[d:end]

class TestAesCtr(unittest.TestCase):
    def test_constructor(self):
        cipher = rsa_cipher.MasterRsaCipher(None, None, rsa_private)
        encrypted_key = "nyXOp7delQ/MQLjKQMhHLaT0w7u2yQoDLkSnK8MFg/MwYdh4na4/LS8LLbLcM18m8I/ObWUHU775I50sJCpdv+f4e0jLeVRRiDFWe+uo7Puc9j4xHj8YB3QlcIOFQiTxHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg="
        encrypted_iv = "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwox4WhLGng5DK2vNXxULmulMUUpYkdc9umqmDilgSy5Z3Foafw+v4JJThfw68T/9G2gxZLrQTbAlvFPFfPM9Ehk6cY4+8WpY32uN8w5vrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw="
        key = cipher.decrypt(base64.b64decode(encrypted_key))
        iv = cipher.decrypt(base64.b64decode(encrypted_iv))
        cipher_data = CipherData(
            iv = iv,
            key=key,
            encrypted_iv=base64.b64decode(encrypted_iv),
            encrypted_key=base64.b64decode(encrypted_key),
            mat_desc='{"key": "value"}',
            wrap_algorithm='RSA/NONE/PKCS1Padding',
            cek_algorithm='AES/CTR/NoPadding'
        )

        cipher = aes_ctr._AesCtr(
            cipher_data=cipher_data,
            offset=0
        )

        self.assertEqual(iv, cipher.cipher_data.iv)
        self.assertEqual(key, cipher.cipher_data.key)
        self.assertEqual('{"key": "value"}', cipher.cipher_data.mat_desc)
        self.assertEqual('RSA/NONE/PKCS1Padding', cipher.cipher_data.wrap_algorithm)
        self.assertEqual('AES/CTR/NoPadding', cipher.cipher_data.cek_algorithm)
        self.assertEqual(0, cipher.offset)


        try:
            cipher = aes_ctr._AesCtr(
                cipher_data=cipher_data,
                offset=11
            )
            self.fail('should not here')
        except ValueError as err:
            self.assertIn("offset is not align to encrypt block", str(err))

    def test_encrypt(self):
        cipher = rsa_cipher.MasterRsaCipher(None, None, rsa_private)
        encrypted_key = "nyXOp7delQ/MQLjKQMhHLaT0w7u2yQoDLkSnK8MFg/MwYdh4na4/LS8LLbLcM18m8I/ObWUHU775I50sJCpdv+f4e0jLeVRRiDFWe+uo7Puc9j4xHj8YB3QlcIOFQiTxHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg="
        encrypted_iv = "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwox4WhLGng5DK2vNXxULmulMUUpYkdc9umqmDilgSy5Z3Foafw+v4JJThfw68T/9G2gxZLrQTbAlvFPFfPM9Ehk6cY4+8WpY32uN8w5vrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw="
        key = cipher.decrypt(base64.b64decode(encrypted_key))
        iv = cipher.decrypt(base64.b64decode(encrypted_iv))
        cipher_data = CipherData(
            iv = iv,
            key=key,
            encrypted_iv=base64.b64decode(encrypted_iv),
            encrypted_key=base64.b64decode(encrypted_key),
            mat_desc='',
            wrap_algorithm='RSA/NONE/PKCS1Padding',
            cek_algorithm='AES/CTR/NoPadding'
        )

        print(sys.version)

        cipher = aes_ctr._AesCtr(
            cipher_data=cipher_data,
            offset=0
        )

        example_data = b''
        with open("./tests/data/example.jpg", 'rb') as f:
            example_data = f.read()
        self.assertTrue(len(example_data) > 0)

        enc_example_data = b''
        with open("./tests/data/enc-example.jpg", 'rb') as f:
            enc_example_data = f.read()

        # encrypt bytes
        edata = cipher.encrypt(example_data)
        self.assertIsInstance(edata, bytes)
        self.assertEqual(enc_example_data, edata)

        # encrypt str
        edata = cipher.encrypt('hello world')
        self.assertIsInstance(edata, bytes)
        self.assertNotEqual('hello world'.encode(), edata)
        eedata = cipher.decrypt(edata)
        self.assertEqual('hello world'.encode(), eedata)

        # file-like
        edata = b''
        with open("./tests/data/example.jpg", 'rb') as f:
            encf = cipher.encrypt(f)
            self.assertIsInstance(encf, aes_ctr.FileLikeEncryptor)
            encf = cast(aes_ctr.FileLikeEncryptor, encf)
            self.assertEqual(0, len(edata))
            while True:
                d = encf.read(8*1024)
                edata += d
                if len(d) < 8*1024:
                    break
            self.assertEqual(enc_example_data, edata)

            #seek
            self.assertEqual(len(enc_example_data), encf.tell())
            encf.seek(16, io.SEEK_SET)
            self.assertEqual(16, encf.tell())
            rlen = 8*1024
            edata = encf.read(8*1024)
            self.assertEqual(enc_example_data[16:16 + rlen], edata)

            encf.seek(128, io.SEEK_SET)
            self.assertEqual(128, encf.tell())
            edata = encf.read()
            self.assertEqual(enc_example_data[128:], edata)

        if sys.version_info >= (3, 11):
            # iterator bytes
            cipher.no_bytes = True
            eiter = cipher.encrypt(example_data)
            self.assertIsInstance(eiter, aes_ctr.IterableEncryptor)
            edata = b''
            for d in eiter:
                edata += d
            self.assertEqual(enc_example_data, edata)

            # iterator str
            cipher.no_str = True
            eiter = cipher.encrypt('1234567890abcdefghijklmnopqrstuvwxyz')
            self.assertIsInstance(eiter, aes_ctr.IterableEncryptor)
            edata = b''
            for d in eiter:
                edata += d

            cipher.no_str = False
            edata1 = cipher.encrypt('1234567890abcdefghijklmnopqrstuvwxyz')
            self.assertEqual(edata1, edata)
            self.assertEqual(len(edata1), len('1234567890abcdefghijklmnopqrstuvwxyz'))


        # file-like + offset
        edata = b''
        with open("./tests/data/example.jpg", 'rb') as f:
            # seek ahead offset
            cipher = aes_ctr._AesCtr(
                cipher_data=cipher_data,
                offset=128
            )
            f.seek(128, io.SEEK_SET)
            encf = cipher.encrypt(f)
            edata = encf.read()
            self.assertEqual(enc_example_data[128:], edata)


    def test_encrypt_exception(self):
        cipher = rsa_cipher.MasterRsaCipher(None, None, rsa_private)
        encrypted_key = "nyXOp7delQ/MQLjKQMhHLaT0w7u2yQoDLkSnK8MFg/MwYdh4na4/LS8LLbLcM18m8I/ObWUHU775I50sJCpdv+f4e0jLeVRRiDFWe+uo7Puc9j4xHj8YB3QlcIOFQiTxHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg="
        encrypted_iv = "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwox4WhLGng5DK2vNXxULmulMUUpYkdc9umqmDilgSy5Z3Foafw+v4JJThfw68T/9G2gxZLrQTbAlvFPFfPM9Ehk6cY4+8WpY32uN8w5vrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw="
        key = cipher.decrypt(base64.b64decode(encrypted_key))
        iv = cipher.decrypt(base64.b64decode(encrypted_iv))
        cipher_data = CipherData(
            iv = iv,
            key=key,
            encrypted_iv=base64.b64decode(encrypted_iv),
            encrypted_key=base64.b64decode(encrypted_key),
            mat_desc='',
            wrap_algorithm='RSA/NONE/PKCS1Padding',
            cek_algorithm='AES/CTR/NoPadding'
        )

        # unsupport type
        cipher = aes_ctr._AesCtr(
            cipher_data=cipher_data,
            offset=0
        )
        try:
            cipher.encrypt(123)
            self.fail('should not here')
        except TypeError as err:
            self.assertIn("src is not str/bytes/file-like/Iterable type, got", str(err))


        # file-like
        edata = b''
        with open("./tests/data/example.jpg", 'rb') as f:
            encf = cipher.encrypt(f)
            self.assertIsInstance(encf, aes_ctr.FileLikeEncryptor)
            encf = cast(aes_ctr.FileLikeEncryptor, encf)
            self.assertEqual(0, len(edata))

            # offset not align to encrypt block
            encf.seek(17, io.SEEK_SET)
            try:
                edata = encf.read(8*1024)
                self.fail('should not here')
            except ValueError as err:
                self.assertIn("offset is not align to encrypt block", str(err))

            # offset not align to encrypt block
            encf.seek(32, io.SEEK_SET)
            try:
                edata = encf.read(1234)
                self.fail('should not here')
            except ValueError as err:
                self.assertIn("n is not align to encrypt block", str(err))

            # seek ahead offset
            cipher = aes_ctr._AesCtr(
                cipher_data=cipher_data,
                offset=128
            )
            f.seek(128, io.SEEK_SET)
            encf = cipher.encrypt(f)
            try:
                encf.seek(0, io.SEEK_SET)
                self.fail('should not here')
            except ValueError as err:
                self.assertIn(", can not creates cipher.", str(err))


    def test_decrypt(self):
        cipher = rsa_cipher.MasterRsaCipher(None, None, rsa_private)
        encrypted_key = "nyXOp7delQ/MQLjKQMhHLaT0w7u2yQoDLkSnK8MFg/MwYdh4na4/LS8LLbLcM18m8I/ObWUHU775I50sJCpdv+f4e0jLeVRRiDFWe+uo7Puc9j4xHj8YB3QlcIOFQiTxHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg="
        encrypted_iv = "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwox4WhLGng5DK2vNXxULmulMUUpYkdc9umqmDilgSy5Z3Foafw+v4JJThfw68T/9G2gxZLrQTbAlvFPFfPM9Ehk6cY4+8WpY32uN8w5vrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw="
        key = cipher.decrypt(base64.b64decode(encrypted_key))
        iv = cipher.decrypt(base64.b64decode(encrypted_iv))
        cipher_data = CipherData(
            iv = iv,
            key=key,
            encrypted_iv=base64.b64decode(encrypted_iv),
            encrypted_key=base64.b64decode(encrypted_key),
            mat_desc='',
            wrap_algorithm='RSA/NONE/PKCS1Padding',
            cek_algorithm='AES/CTR/NoPadding'
        )

        cipher = aes_ctr._AesCtr(
            cipher_data=cipher_data,
            offset=0
        )

        example_data = b''
        with open("./tests/data/example.jpg", 'rb') as f:
            example_data = f.read()
        self.assertTrue(len(example_data) > 0)

        enc_example_data = b''
        with open("./tests/data/enc-example.jpg", 'rb') as f:
            enc_example_data = f.read()

        # decrypt bytes
        data = cipher.decrypt(enc_example_data)
        self.assertIsInstance(data, bytes)
        self.assertEqual(example_data, data)

        # decrypt StreamBody
        dataf = cipher.decrypt(StubStreamBody(data=enc_example_data))
        self.assertIsInstance(dataf, aes_ctr.StreamBodyDecryptor)
        dataf = cast(aes_ctr.StreamBodyDecryptor, dataf)
        self.assertEqual(example_data, dataf.content)
        self.assertEqual(example_data, dataf.read())

        data = b''
        check_once = True
        for d in dataf.iter_bytes():
            if check_once:
                self.assertEqual(4*1024, len(d))
                check_once = False
            data += d
        self.assertEqual(example_data, dataf.read())

        data = b''
        check_once = True
        for d in dataf.iter_bytes(block_size=8*1024):
            if check_once:
                self.assertEqual(8*1024, len(d))
                check_once = False
            data += d
        self.assertEqual(example_data, dataf.read())

