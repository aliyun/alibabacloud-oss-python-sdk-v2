# pylint: skip-file
import unittest
import datetime
from urllib.parse import urlsplit
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider
from alibabacloud_oss_v2.signer.tables_v4 import TablesSignerV4
from alibabacloud_oss_v2.types import HttpRequest, SigningContext


class TestTablesSignerV4(unittest.TestCase):
    def test_auth_header_with_empty_token(self) -> None:
        provider = StaticCredentialsProvider(
            'ak', 'sk', security_token='')
        cred = provider.get_credentials()
        request = HttpRequest(
            'PUT', 'http://bucket.oss-cn-hangzhou.aliyuncs.com')
        request.headers.update(
            {
                'x-oss-head1': 'value',
                'content-type': 'text/plain',
                'x-oss-content-sha256': 'UNSIGNED-PAYLOAD',
            }
        )

        context = SigningContext(
            bucket='bucket',
            key='key',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702784856),
        )

        signer = TablesSignerV4()
        signer.sign(context)
        self.assertIsNone(context.request.headers.get('x-oss-security-token'))

    def test_auth_query_with_empty_token(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk", "")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://bucket.oss-cn-hangzhou.aliyuncs.com")
        request.headers.update(
            {
                'x-oss-head1': 'value',
                'content-type': 'application/octet-stream',
            }
        )

        context = SigningContext(
            bucket='bucket',
            key='key',
            request=request,
            credentials=cred,
            product='oss',
            region='cn-hangzhou',
            signing_time=datetime.datetime.fromtimestamp(1702785388),
        )
        context.expiration_time = datetime.datetime.fromtimestamp(1702785987)
        context.auth_method_query = True

        signer = TablesSignerV4()
        signer.sign(context)

        queries = _get_url_query(request.url)
        self.assertIsNone(queries.get('x-oss-security-token'))


def _get_url_query(url: str):
    encoded_pairs = {}
    parts = urlsplit(url)
    if parts.query:
        for pair in parts.query.split('&'):
            key, _, value = pair.partition('=')
            encoded_pairs[key] = value
    return encoded_pairs
