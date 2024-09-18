# pylint: skip-file
import unittest
import datetime
from urllib.parse import urlencode, quote, urlsplit
from alibabacloud_oss_v2.signer import SignerV1
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider
from alibabacloud_oss_v2.types import HttpRequest, SigningContext

class TestSignerV1(unittest.TestCase):

    def test_auth_header_1(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://examplebucket.oss-cn-hangzhou.aliyuncs.com")
        request.headers.update(
            {
                'Content-MD5': 'eB5eJF1ptWaXm4bijSPyxw==',
                'Content-Type': 'text/html',
                'x-oss-meta-author': 'alice',
                'x-oss-meta-magic': 'abracadabra',
                'x-oss-date': 'Wed, 28 Dec 2022 10:27:41 GMT',
            }
        )

        context = SigningContext(
            bucket='examplebucket',
            key='nelson',
            request=request,
            credentials=cred,
            signing_time=datetime.datetime.fromtimestamp(1702743657),
        )

        signer = SignerV1()
        signer.sign(context)
        self.assertEqual("PUT\neB5eJF1ptWaXm4bijSPyxw==\ntext/html\nWed, 28 Dec 2022 10:27:41 GMT\nx-oss-date:Wed, 28 Dec 2022 10:27:41 GMT\nx-oss-meta-author:alice\nx-oss-meta-magic:abracadabra\n/examplebucket/nelson", context.string_to_sign)
        self.assertEqual("OSS ak:kSHKmLxlyEAKtZPkJhG9bZb5k7M=", context.request.headers.get('Authorization'))

    def test_auth_header_2(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://examplebucket.oss-cn-hangzhou.aliyuncs.com/?acl")
        request.headers.update(
            {
                'Content-MD5': 'eB5eJF1ptWaXm4bijSPyxw==',
                'Content-Type': 'text/html',
                'x-oss-meta-author': 'alice',
                'x-oss-meta-magic': 'abracadabra',
                'x-oss-date': 'Wed, 28 Dec 2022 10:27:41 GMT',
            }
        )

        context = SigningContext(
            bucket='examplebucket',
            key='nelson',
            request=request,
            credentials=cred,
            signing_time=datetime.datetime.fromtimestamp(1702743657),
        )

        signer = SignerV1()
        signer.sign(context)
        self.assertEqual("PUT\neB5eJF1ptWaXm4bijSPyxw==\ntext/html\nWed, 28 Dec 2022 10:27:41 GMT\nx-oss-date:Wed, 28 Dec 2022 10:27:41 GMT\nx-oss-meta-author:alice\nx-oss-meta-magic:abracadabra\n/examplebucket/nelson?acl", context.string_to_sign)
        self.assertEqual("OSS ak:/afkugFbmWDQ967j1vr6zygBLQk=", context.request.headers.get('Authorization'))


    def test_auth_header_3(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "GET", "http://examplebucket.oss-cn-hangzhou.aliyuncs.com/?resourceGroup&non-resousce=null")
        request.headers.update(
            {
                'x-oss-date': 'Wed, 28 Dec 2022 10:27:41 GMT',
            }
        )

        context = SigningContext(
            bucket='examplebucket',
            request=request,
            credentials=cred,
            signing_time=datetime.datetime.fromtimestamp(1702743657),
        )

        signer = SignerV1()
        signer.sign(context)
        self.assertEqual("GET\n\n\nWed, 28 Dec 2022 10:27:41 GMT\nx-oss-date:Wed, 28 Dec 2022 10:27:41 GMT\n/examplebucket/?resourceGroup", context.string_to_sign)
        self.assertEqual("OSS ak:vkQmfuUDyi1uDi3bKt67oemssIs=", context.request.headers.get('Authorization'))

    def test_auth_header_4(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "GET", "http://examplebucket.oss-cn-hangzhou.aliyuncs.com/?resourceGroup&acl")
        request.headers.update(
            {
                'x-oss-date': 'Wed, 28 Dec 2022 10:27:41 GMT',
            }
        )

        context = SigningContext(
            bucket='examplebucket',
            request=request,
            credentials=cred,
            signing_time=datetime.datetime.fromtimestamp(1702743657),
        )

        signer = SignerV1()
        signer.__init_subclass__()
        signer.sign(context)
        self.assertEqual("GET\n\n\nWed, 28 Dec 2022 10:27:41 GMT\nx-oss-date:Wed, 28 Dec 2022 10:27:41 GMT\n/examplebucket/?acl&resourceGroup", context.string_to_sign)
        self.assertEqual("OSS ak:x3E5TgOvl/i7PN618s5mEvpJDYk=", context.request.headers.get('Authorization'))


    def test_auth_query(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "GET", "http://bucket.oss-cn-hangzhou.aliyuncs.com/key?versionId=versionId")
        request.headers.update()

        context = SigningContext(
            bucket='bucket',
            key='key',
            request=request,
            credentials=cred,
        )
        context.expiration_time = datetime.datetime.fromtimestamp(1699807420)
        context.auth_method_query = True

        signer = SignerV1()

        signer.sign(context)

        queries = _get_url_query(request.url)

        #print(datetime.datetime.fromtimestamp(1699807420))

        self.assertEqual('versionId', queries.get('versionId'))
        self.assertIsNotNone(queries.get('Expires'))
        self.assertEqual('ak', queries.get('OSSAccessKeyId'))
        self.assertEqual('dcLTea%2BYh9ApirQ8o8dOPqtvJXQ%3D', queries.get('Signature'))

    def test_auth_query_with_token(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk", "token")
        cred = provider.get_credentials()
        request = HttpRequest(
            "GET", "http://bucket.oss-cn-hangzhou.aliyuncs.com/key+123?versionId=versionId")

        context = SigningContext(
            bucket='bucket',
            key='key+123',
            request=request,
            credentials=cred,
        )
        context.expiration_time = datetime.datetime.fromtimestamp(1699808204)
        context.auth_method_query = True


        signer = SignerV1()

        signer.sign(context)

        queries = _get_url_query(request.url)

        self.assertIsNotNone(queries.get('Expires'))
        self.assertEqual('ak', queries.get('OSSAccessKeyId'))
        self.assertEqual('token', queries.get('security-token'))
        self.assertEqual('jzKYRrM5y6Br0dRFPaTGOsbrDhY%3D', queries.get('Signature'))

    def test_auth_query_param_with_token(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk", "token")
        cred = provider.get_credentials()
        request = HttpRequest(
            "GET", "http://bucket.oss-cn-hangzhou.aliyuncs.com/key?versionId=versionId")
        request.headers.update(
            {
                'x-oss-head1': 'value',
                'abc': 'value',
                'ZAbc': 'value',
                'XYZ': 'value',
                'content-type': 'application/octet-stream',
            }
        )

        context = SigningContext(
            bucket='bucket',
            key='key',
            request=request,
            credentials=cred,
        )
        context.expiration_time = datetime.datetime.fromtimestamp(1699808204)
        context.auth_method_query = True

        parameters = {
            'param1': 'value1',
            '+param1': 'value3',
            '|param1': 'value4',
            '+param2': '',
            '|param2': '',
            'param2': '',
            'response-content-disposition': 'attachment; filename=example.txt'
        }
        query = urlencode(parameters, quote_via=quote)

        request.url = request.url + "?" + query

        signer = SignerV1()

        signer.sign(context)

        queries = _get_url_query(request.url)

        self.assertIsNotNone(queries.get('Expires'))
        self.assertEqual('ak', queries.get('OSSAccessKeyId'))
        self.assertEqual('attachment%3B%20filename%3Dexample.txt', queries.get('response-content-disposition'))
        self.assertEqual('token', queries.get('security-token'))
        self.assertEqual('3GJoEOv5LX2ASp0HJk%2FhAk%2BqLJc%3D', queries.get('Signature'))


def _get_url_query(url: str):
    encoded_pairs = {}
    parts = urlsplit(url)
    if parts.query:
        for pair in parts.query.split('&'):
            key, _, value = pair.partition('=')
            encoded_pairs[key] = value
    return encoded_pairs
