# pylint: skip-file
import unittest
import datetime
from urllib.parse import urlencode, quote, urlsplit
from alibabacloud_oss_v2.signer import SignerV4
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider
from alibabacloud_oss_v2.signer.vectors_v4 import VectorsSignerV4
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

    def test_auth_query_long_expiration(self) -> None:
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
        context.expiration_time = datetime.datetime.fromtimestamp(1702781677 + 5*24*60*60)
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
        self.assertEqual('432000', queries.get('x-oss-expires'))
        self.assertEqual(
            'ak%2F20231217%2Fcn-hangzhou%2Foss%2Faliyun_v4_request',
            queries.get('x-oss-credential'))
        self.assertEqual(
            '31029123dc7732d2d2cfd4006ea4fdb6cf86da6478f813e2bf8f87877c7b9fec',
            queries.get('x-oss-signature'))
        self.assertEqual('', queries.get('x-oss-additional-headers', ''))
    def test_auth_header_cloud_box(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://bucket.cb-123.cn-hangzhou.oss-cloudbox.aliyuncs.com/1234+-/123/1.txt")
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
            product='oss-cloudbox',
            region='cb-123',
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

        auth_pat = 'OSS4-HMAC-SHA256 Credential=ak/20231216/cb-123/oss-cloudbox/aliyun_v4_request,Signature=94ce1f12c17d148ea681030275a94449d3357f5b5b21133996eec80af3e08a43'
        self.assertEqual(auth_pat, context.request.headers.get('Authorization'))

    def test_auth_query_with_cloud_box(self) -> None:
        provider = StaticCredentialsProvider("ak", "sk")
        cred = provider.get_credentials()
        request = HttpRequest(
            "PUT", "http://bucket.cb-123.cn-hangzhou.oss-cloudbox.aliyuncs.com/1234+-/123/1.txt")
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
            product='oss-cloudbox',
            region='cb-123',
            signing_time=datetime.datetime.fromtimestamp(1702781677),
            additional_headers={'ZAbc', 'abc'}
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

        self.assertEqual('OSS4-HMAC-SHA256', queries.get('x-oss-signature-version'))
        self.assertEqual('20231217T025437Z', queries.get('x-oss-date'))
        self.assertEqual('599', queries.get('x-oss-expires'))
        self.assertEqual('ak%2F20231217%2Fcb-123%2Foss-cloudbox%2Faliyun_v4_request', queries.get('x-oss-credential'))
        self.assertEqual('07284191b9b4978ac3520cd39ee2dea2747eda454089359371ff463a6c7ba20f', queries.get('x-oss-signature'))
        self.assertEqual('abc%3Bzabc', queries.get('x-oss-additional-headers', ''))

        # with default signed header
        request = HttpRequest(
            "PUT", "http://bucket.cb-123.cn-hangzhou.oss-cloudbox.aliyuncs.com/1234+-/123/1.txt")
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
            product='oss-cloudbox',
            region='cb-123',
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

        self.assertEqual('OSS4-HMAC-SHA256', queries.get('x-oss-signature-version'))
        self.assertEqual('20231217T033009Z', queries.get('x-oss-date'))
        self.assertEqual('599', queries.get('x-oss-expires'))
        self.assertEqual('ak%2F20231217%2Fcb-123%2Foss-cloudbox%2Faliyun_v4_request', queries.get('x-oss-credential'))
        self.assertEqual('16782cc8a7a554523db055eb804b508522e7e370073108ad88ee2f47496701dd', queries.get('x-oss-signature'))
        self.assertEqual('abc%3Bzabc', queries.get('x-oss-additional-headers', ''))


    def test_signer_vector_v4_build_bucket_arn(self) -> None:
        """
        Tests the URI construction logic within VectorsSignerV4.
        Corresponds to TestSignerVectorV4BuildBucketArn in Go.
        Since the URI construction is internal, we test it by examining the string_to_sign
        which contains the canonical request.
        """
        account_id = "123"
        signer = VectorsSignerV4(account_id)

        # Test 1: Only region
        sign_ctx = SigningContext(
            region='cn-hangzhou',
            credentials=StaticCredentialsProvider("ak", "sk").get_credentials(),
            request=HttpRequest("GET", "http://example.com"),
            signing_time=datetime.datetime.fromtimestamp(1702743657, tz=datetime.timezone.utc)
        )
        signer.sign(sign_ctx)
        expected_uri_1 = f'/acs:ossvector:cn-hangzhou:{account_id}:'

        self.assertIn(expected_uri_1, sign_ctx.string_to_sign)

        # Test 2: Region and bucket
        sign_ctx = SigningContext(
            region='cn-hangzhou',
            bucket='bucket',
            credentials=StaticCredentialsProvider("ak", "sk").get_credentials(),
            request=HttpRequest("GET", "http://example.com"),
            signing_time=datetime.datetime.fromtimestamp(1702743657, tz=datetime.timezone.utc)
        )
        signer.sign(sign_ctx)
        expected_uri_2 = f'/acs:ossvector:cn-hangzhou:{account_id}:bucket/'
        self.assertIn(expected_uri_2, sign_ctx.string_to_sign)

        # Test 3: Region, bucket, and simple key
        sign_ctx = SigningContext(
            region='cn-hangzhou',
            bucket='bucket',
            key='key',
            credentials=StaticCredentialsProvider("ak", "sk").get_credentials(),
            request=HttpRequest("GET", "http://example.com"),
            signing_time=datetime.datetime.fromtimestamp(1702743657, tz=datetime.timezone.utc)
        )
        signer.sign(sign_ctx)
        expected_uri_3 = f'/acs:ossvector:cn-hangzhou:{account_id}:bucket/key'
        self.assertIn(expected_uri_3, sign_ctx.string_to_sign)

        # Test 4: Region, bucket, and complex key that needs escaping
        complex_key = "key-1/key-2"
        escaped_key = quote(complex_key, safe='')
        sign_ctx = SigningContext(
            region='cn-hangzhou',
            bucket='bucket',
            key=complex_key,
            credentials=StaticCredentialsProvider("ak", "sk").get_credentials(),
            request=HttpRequest("GET", "http://example.com"),
            signing_time=datetime.datetime.fromtimestamp(1702743657, tz=datetime.timezone.utc)
        )
        signer.sign(sign_ctx)
        # The key should be URL-encoded in the final URI
        expected_uri_4 = f'/acs:ossvector:cn-hangzhou:{account_id}:bucket/{escaped_key}'
        self.assertIn(expected_uri_4, sign_ctx.string_to_sign)

    def test_signer_vector_v4_build_bucket_arn(self) -> None:
        """
        Tests the URI construction logic within VectorsSignerV4 by directly calling
        _calc_canonical_request.
        Corresponds to TestSignerVectorV4BuildBucketArn in Go.
        """
        account_id = "123"
        signer = VectorsSignerV4(account_id)

        # Create a minimal, valid SigningContext for _calc_canonical_request
        # It doesn't need credentials or a full request for this specific test
        base_sign_ctx = SigningContext(
            request=HttpRequest("GET", "http://example.com"),
            # Credentials and other fields are not strictly needed for URI calculation in this test
        )

        # Mock the necessary methods/attributes that _calc_canonical_request uses
        # We only care about the URI part, so we can provide dummy values for headers etc.
        def mock_common_additional_headers(*args, **kwargs):
            return set()

        signer._common_additional_headers = mock_common_additional_headers  # type: ignore

        # Test 1: Only region
        sign_ctx = SigningContext()
        sign_ctx.__dict__.update(base_sign_ctx.__dict__)  # Merge base context
        sign_ctx.region = 'cn-hangzhou'
        canonical_request_output = signer._calc_canonical_request(sign_ctx, set())
        expected_uri_1 = f'/acs:ossvector:cn-hangzhou:{account_id}:'
        # The canonical request format is METHOD\nURI\nQUERY\nHEADERS\nADDITIONAL_HEADERS\nPAYLOAD
        # So the URI should be the second line.
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
        escaped_key = quote(complex_key, safe='')  # This is how it's escaped in _calc_canonical_request
        sign_ctx = SigningContext(region='cn-hangzhou', bucket='bucket', key=complex_key)
        sign_ctx.__dict__.update(base_sign_ctx.__dict__)
        sign_ctx.region = 'cn-hangzhou'
        sign_ctx.bucket = 'bucket'
        sign_ctx.key = escaped_key
        canonical_request_output = signer._calc_canonical_request(sign_ctx, set())
        # The key should be URL-encoded in the final URI by the quote() function inside _calc_canonical_request
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
