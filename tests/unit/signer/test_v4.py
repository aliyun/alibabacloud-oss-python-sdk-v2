# pylint: skip-file
import unittest
import datetime
from urllib.parse import urlencode, quote, urlsplit
from alibabacloud_oss_v2.signer import SignerV4
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider
from alibabacloud_oss_v2.types import HttpRequest, SigningContext

class TestSignerV4(unittest.TestCase):
    def test_auth_header(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://bucket.oss-cn-hangzhou.aliyuncs.com")
        request.headers.update(
            {
                'x-oss-head1': 'value',
                'abc': 'value',
                'ZAbc': 'value',
                'XYZ': 'value',
                'content-type': 'text/plain',
                'x-oss-content-sha256': 'UNSIGNED-PAYLOAD',
            }
        )

        context = SigningContext(
            bucket='bucket',
            key='1234+-/123/1.txt',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702743657),
        )

        parameters = {
            'param1': 'value1',
            '+param1': 'value3',
            '|param1': 'value4',
            '+param2': '',
            '|param2': '',
            'param2': '',
        }
        query = urlencode(parameters, quote_via=quote)

        request.url = request.url + "?" + query

        signer = SignerV4()

        signer.sign(context)

        auth_pat = 'OSS4-HMAC-SHA256 Credential=ak/20231216/cn-hangzhou/oss/aliyun_v4_request,Signature=e21d18daa82167720f9b1047ae7e7f1ce7cb77a31e8203a7d5f4624fa0284afe'
        self.assertEqual(auth_pat, context.request.headers.get('Authorization'))


    def test_auth_header_with_token(self) -> None:
        provider = StaticCredentialsProvider(
            'ak', 'sk', security_token='token')
        cred = provider.get_credentials()
        request = HttpRequest(
            'PUT', 'http://bucket.oss-cn-hangzhou.aliyuncs.com')
        request.headers.update(
            {
                'x-oss-head1': 'value',
                'abc': 'value',
                'ZAbc': 'value',
                'XYZ': 'value',
                'content-type': 'text/plain',
                'x-oss-content-sha256': 'UNSIGNED-PAYLOAD',
            }
        )

        context = SigningContext(
            bucket='bucket',
            key='1234+-/123/1.txt',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702784856),
        )

        parameters = {
            'param1': 'value1',
            '+param1': 'value3',
            '|param1': 'value4',
            '+param2': '',
            '|param2': '',
            'param2': '',
        }
        query = urlencode(parameters, quote_via=quote)

        request.url = request.url + "?" + query

        signer = SignerV4()

        signer.sign(context)

        auth_pat = 'OSS4-HMAC-SHA256 Credential=ak/20231217/cn-hangzhou/oss/aliyun_v4_request,Signature=b94a3f999cf85bcdc00d332fbd3734ba03e48382c36fa4d5af5df817395bd9ea'
        self.assertEqual(
            auth_pat, context.request.headers.get('Authorization'))

    def test_auth_header_with_additional_headers(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://bucket.oss-cn-hangzhou.aliyuncs.com")
        request.headers.update(
            {
                'x-oss-head1': 'value',
                'abc': 'value',
                'ZAbc': 'value',
                'XYZ': 'value',
                'content-type': 'text/plain',
                'x-oss-content-sha256': 'UNSIGNED-PAYLOAD',
            }
        )

        context = SigningContext(
            bucket='bucket',
            key='1234+-/123/1.txt',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702747512),
            additional_headers={'ZAbc', 'abc'}
        )

        parameters = {
            'param1': 'value1',
            '+param1': 'value3',
            '|param1': 'value4',
            '+param2': '',
            '|param2': '',
            'param2': '',
        }
        query = urlencode(parameters, quote_via=quote)

        request.url = request.url + "?" + query

        signer = SignerV4()

        signer.sign(context)

        auth_pat = 'OSS4-HMAC-SHA256 Credential=ak/20231216/cn-hangzhou/oss/aliyun_v4_request,AdditionalHeaders=abc;zabc,Signature=4a4183c187c07c8947db7620deb0a6b38d9fbdd34187b6dbaccb316fa251212f'
        self.assertEqual(
            auth_pat, context.request.headers.get('Authorization'))

        # with default signed header
        request = HttpRequest(
            "PUT", "http://bucket.oss-cn-hangzhou.aliyuncs.com")
        request.headers.update(
            {
                'x-oss-head1': 'value',
                'abc': 'value',
                'ZAbc': 'value',
                'XYZ': 'value',
                'content-type': 'text/plain',
                'x-oss-content-sha256': 'UNSIGNED-PAYLOAD',
            }
        )

        context = SigningContext(
            bucket='bucket',
            key='1234+-/123/1.txt',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702747512),
            additional_headers={'x-oss-no-exist', 'ZAbc', 'x-oss-head1', 'abc'}
        )

        parameters = {
            'param1': 'value1',
            '+param1': 'value3',
            '|param1': 'value4',
            '+param2': '',
            '|param2': '',
            'param2': '',
        }
        query = urlencode(parameters, quote_via=quote)

        request.url = request.url + "?" + query

        signer = SignerV4()

        signer.sign(context)

        auth_pat = 'OSS4-HMAC-SHA256 Credential=ak/20231216/cn-hangzhou/oss/aliyun_v4_request,AdditionalHeaders=abc;zabc,Signature=4a4183c187c07c8947db7620deb0a6b38d9fbdd34187b6dbaccb316fa251212f'
        self.assertEqual(
            auth_pat, context.request.headers.get('Authorization'))

    def test_auth_query(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://bucket.oss-cn-hangzhou.aliyuncs.com")
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
            key='1234+-/123/1.txt',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702781677),
        )
        context.expiration_time = datetime.datetime.fromtimestamp(1702782276)
        context.auth_method_query = True

        parameters = {
            'param1': 'value1',
            '+param1': 'value3',
            '|param1': 'value4',
            '+param2': '',
            '|param2': '',
            'param2': '',
        }
        query = urlencode(parameters, quote_via=quote)

        request.url = request.url + "?" + query

        signer = SignerV4()

        signer.sign(context)

        queries = _get_url_query(request.url)

        self.assertEqual('OSS4-HMAC-SHA256',
                         queries.get('x-oss-signature-version'))
        self.assertEqual('599', queries.get('x-oss-expires'))
        self.assertEqual(
            'ak%2F20231217%2Fcn-hangzhou%2Foss%2Faliyun_v4_request', 
            queries.get('x-oss-credential'))
        self.assertEqual(
            'a39966c61718be0d5b14e668088b3fa07601033f6518ac7b523100014269c0fe', 
            queries.get('x-oss-signature'))
        self.assertEqual('', queries.get('x-oss-additional-headers', ''))

    def test_auth_query_with_token(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk", "token")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://bucket.oss-cn-hangzhou.aliyuncs.com")
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
            key='1234+-/123/1.txt',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702785388),
        )
        context.expiration_time = datetime.datetime.fromtimestamp(1702785987)
        context.auth_method_query = True

        parameters = {
            'param1': 'value1',
            '+param1': 'value3',
            '|param1': 'value4',
            '+param2': '',
            '|param2': '',
            'param2': '',
        }
        query = urlencode(parameters, quote_via=quote)

        request.url = request.url + "?" + query

        signer = SignerV4()

        signer.sign(context)

        queries = _get_url_query(request.url)

        self.assertEqual('OSS4-HMAC-SHA256',
                         queries.get('x-oss-signature-version'))
        self.assertEqual('20231217T035628Z', queries.get('x-oss-date'))
        self.assertEqual('599', queries.get('x-oss-expires'))
        self.assertEqual(
            'ak%2F20231217%2Fcn-hangzhou%2Foss%2Faliyun_v4_request', 
            queries.get('x-oss-credential'))
        self.assertEqual(
            '3817ac9d206cd6dfc90f1c09c00be45005602e55898f26f5ddb06d7892e1f8b5', 
            queries.get('x-oss-signature'))
        self.assertEqual('', queries.get('x-oss-additional-headers', ''))

    def test_auth_query_with_additional_headers(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://bucket.oss-cn-hangzhou.aliyuncs.com")
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
            key='1234+-/123/1.txt',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702783809),
            additional_headers={'ZAbc', 'abc'}
        )
        context.expiration_time = datetime.datetime.fromtimestamp(1702784408)
        context.auth_method_query = True

        parameters = {
            'param1': 'value1',
            '+param1': 'value3',
            '|param1': 'value4',
            '+param2': '',
            '|param2': '',
            'param2': '',
        }
        query = urlencode(parameters, quote_via=quote)

        request.url = request.url + "?" + query

        signer = SignerV4()

        signer.sign(context)

        queries = _get_url_query(request.url)

        self.assertEqual('OSS4-HMAC-SHA256',
                         queries.get('x-oss-signature-version'))
        self.assertEqual('20231217T033009Z', queries.get('x-oss-date'))
        self.assertEqual('599', queries.get('x-oss-expires'))
        self.assertEqual(
            'ak%2F20231217%2Fcn-hangzhou%2Foss%2Faliyun_v4_request',
            queries.get('x-oss-credential'))
        self.assertEqual(
            '6bd984bfe531afb6db1f7550983a741b103a8c58e5e14f83ea474c2322dfa2b7',
             queries.get('x-oss-signature'))
        self.assertEqual('abc%3Bzabc', queries.get(
            'x-oss-additional-headers', ''))

        # with default signed header
        request = HttpRequest(
            "PUT", "http://bucket.oss-cn-hangzhou.aliyuncs.com")
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
            key='1234+-/123/1.txt',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702783809),
            additional_headers={'x-oss-no-exist', 'ZAbc', 'x-oss-head1', 'abc'}
        )
        context.expiration_time = datetime.datetime.fromtimestamp(1702784408)
        context.auth_method_query = True

        parameters = {
            'param1': 'value1',
            '+param1': 'value3',
            '|param1': 'value4',
            '+param2': '',
            '|param2': '',
            'param2': '',
        }
        query = urlencode(parameters, quote_via=quote)

        request.url = request.url + "?" + query

        signer = SignerV4()

        signer.sign(context)

        queries = _get_url_query(request.url)

        self.assertEqual('OSS4-HMAC-SHA256',
                         queries.get('x-oss-signature-version'))
        self.assertEqual('20231217T033009Z', queries.get('x-oss-date'))
        self.assertEqual('599', queries.get('x-oss-expires'))
        self.assertEqual(
            'ak%2F20231217%2Fcn-hangzhou%2Foss%2Faliyun_v4_request',
            queries.get('x-oss-credential'))
        self.assertEqual(
            '6bd984bfe531afb6db1f7550983a741b103a8c58e5e14f83ea474c2322dfa2b7',
            queries.get('x-oss-signature'))
        self.assertEqual('abc%3Bzabc', queries.get(
            'x-oss-additional-headers', ''))


def _get_url_query(url: str):
    encoded_pairs = {}
    parts = urlsplit(url)
    if parts.query:
        for pair in parts.query.split('&'):
            key, _, value = pair.partition('=')
            encoded_pairs[key] = value
    return encoded_pairs
