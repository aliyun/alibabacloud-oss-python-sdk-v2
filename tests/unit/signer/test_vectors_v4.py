# pylint: skip-file
import unittest
import datetime
from urllib.parse import quote, urlsplit
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider
from alibabacloud_oss_v2.signer.vectors_v4 import VectorsSignerV4
from alibabacloud_oss_v2.types import HttpRequest, SigningContext


class TestVectorsSignerV4(unittest.TestCase):
    def test_auth_header_with_empty_token(self) -> None:
        provider = StaticCredentialsProvider(
            'ak', 'sk', security_token='')
        cred = provider.get_credentials()
        request = HttpRequest(
            'GET', 'http://example.com')

        signer = VectorsSignerV4('123')
        context = SigningContext(
            region='cn-hangzhou',
            bucket='bucket',
            request=request,
            credentials=cred,
            product='oss',
            signing_time=datetime.datetime.fromtimestamp(1702743657, tz=datetime.timezone.utc)
        )
        signer.sign(context)
        self.assertIsNone(context.request.headers.get('x-oss-security-token'))

    def test_auth_query_with_empty_token(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk", "")
        cred = provider.get_credentials()
        request = HttpRequest(
            "GET", "http://example.com")

        signer = VectorsSignerV4('123')
        context = SigningContext(
            region='cn-hangzhou',
            bucket='bucket',
            key='key',
            request=request,
            credentials=cred,
            product='oss',
            signing_time=datetime.datetime.fromtimestamp(1702743657, tz=datetime.timezone.utc),
        )
        context.expiration_time = datetime.datetime.fromtimestamp(1702744257, tz=datetime.timezone.utc)
        context.auth_method_query = True

        signer.sign(context)

        queries = _get_url_query(request.url)
        self.assertIsNone(queries.get('x-oss-security-token'))

    def test_build_bucket_arn(self) -> None:
        """
        Tests the URI construction logic within VectorsSignerV4 by directly calling
        _calc_canonical_request.
        Corresponds to TestSignerVectorV4BuildBucketArn in Go.
        """
        account_id = "123"
        signer = VectorsSignerV4(account_id)

        base_sign_ctx = SigningContext(
            request=HttpRequest("GET", "http://example.com"),
        )

        def mock_common_additional_headers(*args, **kwargs):
            return set()

        signer._common_additional_headers = mock_common_additional_headers  # type: ignore

        # Test 1: Only region
        sign_ctx = SigningContext()
        sign_ctx.__dict__.update(base_sign_ctx.__dict__)
        sign_ctx.region = 'cn-hangzhou'
        canonical_request_output = signer._calc_canonical_request(sign_ctx, set())
        expected_uri_1 = f'/acs:ossvector:cn-hangzhou::/'
        lines = canonical_request_output.split('\n')
        self.assertEqual(lines[1], quote(expected_uri_1), "URI mismatch for region-only case")

        # Test 2: Region and bucket
        sign_ctx = SigningContext(region='cn-hangzhou', bucket='bucket')
        sign_ctx.__dict__.update(base_sign_ctx.__dict__)
        sign_ctx.region = 'cn-hangzhou'
        sign_ctx.bucket = 'bucket'
        canonical_request_output = signer._calc_canonical_request(sign_ctx, set())
        expected_uri_2 = f'/acs:ossvector:cn-hangzhou:{account_id}:bucket/'
        lines = canonical_request_output.split('\n')
        self.assertEqual(lines[1], quote(expected_uri_2), "URI mismatch for region-bucket case")

        # Test 3: Region, bucket, and simple key
        sign_ctx = SigningContext(region='cn-hangzhou', bucket='bucket', key='key')
        sign_ctx.__dict__.update(base_sign_ctx.__dict__)
        sign_ctx.region = 'cn-hangzhou'
        sign_ctx.bucket = 'bucket'
        sign_ctx.key = 'key'
        canonical_request_output = signer._calc_canonical_request(sign_ctx, set())
        expected_uri_3 = f'/acs:ossvector:cn-hangzhou:{account_id}:bucket/key'
        lines = canonical_request_output.split('\n')
        self.assertEqual(lines[1], quote(expected_uri_3), "URI mismatch for region-bucket-key case")

        # Test 4: Region, bucket, and complex key that needs escaping
        complex_key = "key-1/key-2"
        escaped_key = quote(complex_key, safe='')
        sign_ctx = SigningContext(region='cn-hangzhou', bucket='bucket', key=complex_key)
        sign_ctx.__dict__.update(base_sign_ctx.__dict__)
        sign_ctx.region = 'cn-hangzhou'
        sign_ctx.bucket = 'bucket'
        sign_ctx.key = escaped_key
        canonical_request_output = signer._calc_canonical_request(sign_ctx, set())
        expected_uri_4 = f'/acs:ossvector:cn-hangzhou:{account_id}:bucket/{escaped_key}'
        lines = canonical_request_output.split('\n')
        self.assertEqual(lines[1], quote(expected_uri_4), "URI mismatch for region-bucket-complex-key case")


def _get_url_query(url: str):
    encoded_pairs = {}
    parts = urlsplit(url)
    if parts.query:
        for pair in parts.query.split('&'):
            key, _, value = pair.partition('=')
            encoded_pairs[key] = value
    return encoded_pairs
