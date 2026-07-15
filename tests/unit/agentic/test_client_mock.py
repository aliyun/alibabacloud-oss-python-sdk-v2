# pylint: skip-file
import unittest
from typing import Any
from urllib.parse import urlparse, parse_qs
from alibabacloud_oss_v2 import config, credentials
from alibabacloud_oss_v2.agentic import AgenticBucketClient, BucketSpaceClient
from alibabacloud_oss_v2.agentic import models
from alibabacloud_oss_v2.types import HttpRequest, HttpResponse, HttpClient
from .. import MockHttpResponse


class RecordingHttpClient(HttpClient):
    def __init__(self, response):
        self.last_request: HttpRequest = None
        self._response = response

    def send(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        self.last_request = request
        self._response._request = request
        return self._response

    def open(self) -> None:
        return

    def close(self) -> None:
        return


def _client(http_client, account_id="1234567890123456", region="cn-hangzhou"):
    cfg = config.load_default()
    cfg.region = region
    cfg.account_id = account_id
    cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
    cfg.http_client = http_client
    return AgenticBucketClient(cfg)


class TestAgenticClientMockURL(unittest.TestCase):
    def _ok_response(self, body=None):
        return MockHttpResponse(status_code=200, reason='OK', headers={'x-oss-request-id': 'r1'}, body=body)

    def test_create_agentic_bucket_url(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http)
        client.create_agentic_bucket(models.CreateAgenticBucketRequest(bucket='my-agentic'))
        req = http.last_request
        u = urlparse(req.url)
        self.assertEqual('PUT', req.method)
        self.assertEqual('my-agentic-1234567890123456-cn-hangzhou-ab-apsr.oss-cn-hangzhou.aliyuncs.com', u.netloc)
        self.assertIn('agenticBucket', parse_qs(u.query, keep_blank_values=True))

    def test_get_agentic_bucket_url(self):
        http = RecordingHttpClient(self._ok_response(
            b'<AgenticBucketInfo><Name>my-agentic-1234567890123456-cn-hangzhou-ab-apsr</Name></AgenticBucketInfo>'))
        client = _client(http)
        result = client.get_agentic_bucket(models.GetAgenticBucketRequest(bucket='my-agentic'))
        u = urlparse(http.last_request.url)
        self.assertEqual('GET', http.last_request.method)
        self.assertEqual('my-agentic-1234567890123456-cn-hangzhou-ab-apsr.oss-cn-hangzhou.aliyuncs.com', u.netloc)
        self.assertEqual('my-agentic-1234567890123456-cn-hangzhou-ab-apsr', result.agentic_bucket_info.name)

    def test_list_agentic_buckets_region_host(self):
        http = RecordingHttpClient(self._ok_response(
            b'<ListAgenticBucketsResult><IsTruncated>false</IsTruncated></ListAgenticBucketsResult>'))
        client = _client(http)
        client.list_agentic_buckets(models.ListAgenticBucketsRequest(max_keys=10))
        u = urlparse(http.last_request.url)
        # No bucket -> region-level host
        self.assertEqual('oss-cn-hangzhou.aliyuncs.com', u.netloc)
        q = parse_qs(u.query, keep_blank_values=True)
        self.assertIn('agenticBucket', q)
        self.assertEqual(['10'], q['max-keys'])

    def test_status_url_has_status_param(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http)
        client.put_agentic_bucket_status(models.PutAgenticBucketStatusRequest(
            bucket='my-agentic', agentic_bucket_status=models.AgenticBucketStatus(status='Disabled')))
        u = urlparse(http.last_request.url)
        q = parse_qs(u.query, keep_blank_values=True)
        self.assertIn('agenticBucket', q)
        self.assertIn('status', q)

    def test_list_bucket_spaces_url(self):
        http = RecordingHttpClient(self._ok_response(
            b'<ListBucketSpacesResult><IsTruncated>false</IsTruncated></ListBucketSpacesResult>'))
        client = _client(http)
        client.list_bucket_spaces(models.ListBucketSpacesRequest(bucket='my-agentic', prefix='foo'))
        u = urlparse(http.last_request.url)
        self.assertEqual('my-agentic-1234567890123456-cn-hangzhou-ab-apsr.oss-cn-hangzhou.aliyuncs.com', u.netloc)
        q = parse_qs(u.query, keep_blank_values=True)
        self.assertIn('agenticBucket', q)
        self.assertIn('bucketSpace', q)
        self.assertEqual(['foo'], q['prefix'])

    def test_encryption_url(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http)
        from alibabacloud_oss_v2.models.bucket_encryption import (
            ServerSideEncryptionRule, ApplyServerSideEncryptionByDefault)
        client.put_agentic_bucket_encryption(models.PutAgenticBucketEncryptionRequest(
            bucket='my-agentic',
            server_side_encryption_rule=ServerSideEncryptionRule(
                apply_server_side_encryption_by_default=ApplyServerSideEncryptionByDefault(sse_algorithm='AES256'))))
        u = urlparse(http.last_request.url)
        q = parse_qs(u.query, keep_blank_values=True)
        self.assertIn('agenticBucket', q)
        self.assertIn('encryption', q)

    def test_policy_url_and_content_md5(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http)
        client.put_agentic_bucket_policy(models.PutAgenticBucketPolicyRequest(
            bucket='my-agentic', body=b'{"Version":"1","Statement":[]}'))
        req = http.last_request
        u = urlparse(req.url)
        q = parse_qs(u.query, keep_blank_values=True)
        self.assertIn('agenticBucket', q)
        self.assertIn('policy', q)
        self.assertEqual('application/json', req.headers.get('Content-Type'))
        self.assertIsNotNone(req.headers.get('Content-MD5'))

    def test_delete_agentic_bucket_url(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http)
        client.delete_agentic_bucket(models.DeleteAgenticBucketRequest(bucket='my-agentic'))
        req = http.last_request
        u = urlparse(req.url)
        self.assertEqual('DELETE', req.method)
        self.assertEqual('my-agentic-1234567890123456-cn-hangzhou-ab-apsr.oss-cn-hangzhou.aliyuncs.com', u.netloc)
        self.assertIn('agenticBucket', parse_qs(u.query, keep_blank_values=True))

    def test_delete_encryption_url(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http)
        client.delete_agentic_bucket_encryption(
            models.DeleteAgenticBucketEncryptionRequest(bucket='my-agentic'))
        req = http.last_request
        q = parse_qs(urlparse(req.url).query, keep_blank_values=True)
        self.assertEqual('DELETE', req.method)
        self.assertIn('agenticBucket', q)
        self.assertIn('encryption', q)

    def test_delete_policy_url(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http)
        client.delete_agentic_bucket_policy(
            models.DeleteAgenticBucketPolicyRequest(bucket='my-agentic'))
        req = http.last_request
        q = parse_qs(urlparse(req.url).query, keep_blank_values=True)
        self.assertEqual('DELETE', req.method)
        self.assertIn('agenticBucket', q)
        self.assertIn('policy', q)

    def test_delete_public_access_block_url(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http)
        client.delete_agentic_bucket_public_access_block(
            models.DeleteAgenticBucketPublicAccessBlockRequest(bucket='my-agentic'))
        req = http.last_request
        q = parse_qs(urlparse(req.url).query, keep_blank_values=True)
        self.assertEqual('DELETE', req.method)
        self.assertIn('agenticBucket', q)
        self.assertIn('publicAccessBlock', q)

    def test_invalid_account_id_raises(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http, account_id='not-numeric')
        with self.assertRaises(Exception) as ctx:
            client.get_agentic_bucket(models.GetAgenticBucketRequest(bucket='my-agentic'))
        self.assertIn('invalid account id', str(ctx.exception))

    def test_non_ascii_digit_account_id_raises(self):
        # Unicode digits (e.g. Arabic-Indic) are rejected; only ASCII 0-9 allowed.
        http = RecordingHttpClient(self._ok_response())
        client = _client(http, account_id='١٢٣')
        with self.assertRaises(Exception) as ctx:
            client.get_agentic_bucket(models.GetAgenticBucketRequest(bucket='my-agentic'))
        self.assertIn('invalid account id', str(ctx.exception))

    def test_user_agent_marker_then_custom(self):
        http = RecordingHttpClient(self._ok_response())
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.account_id = '1234567890123456'
        cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
        cfg.http_client = http
        cfg.user_agent = 'mytool/1.0'
        client = AgenticBucketClient(cfg)
        ua = client._client._inner.user_agent
        # marker sits right after the base SDK UA, caller-provided UA comes last
        self.assertIn('/agentic-client/mytool/1.0', ua)
        self.assertTrue(ua.startswith('alibabacloud-python-sdk-v2/'))

    def test_user_agent_marker_without_custom(self):
        http = RecordingHttpClient(self._ok_response())
        client = _client(http)
        self.assertTrue(client._client._inner.user_agent.endswith('/agentic-client'))


class TestBucketSpaceClientMockURL(unittest.TestCase):
    def _ok_response(self, body=None):
        return MockHttpResponse(status_code=200, reason='OK', headers={'x-oss-request-id': 'r1'}, body=body)

    def _client(self, http_client, account_id="1234567890123456", region="cn-hangzhou"):
        cfg = config.load_default()
        cfg.region = region
        cfg.account_id = account_id
        cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
        cfg.http_client = http_client
        return BucketSpaceClient.create(cfg)

    def test_bucket_space_client_resolves_prefix(self):
        from alibabacloud_oss_v2 import models as oss_models
        http = RecordingHttpClient(self._ok_response())
        client = self._client(http)
        client.put_bucket(oss_models.PutBucketRequest(bucket='my-agent'))
        u = urlparse(http.last_request.url)
        self.assertEqual('my-agent-1234567890123456-cn-hangzhou-bs-apsr.oss-cn-hangzhou.aliyuncs.com', u.netloc)

    def test_invalid_account_id_raises(self):
        from alibabacloud_oss_v2 import models as oss_models
        http = RecordingHttpClient(self._ok_response())
        client = self._client(http, account_id='not-numeric')
        with self.assertRaises(Exception) as ctx:
            client.put_bucket(oss_models.PutBucketRequest(bucket='my-agent'))
        self.assertIn('invalid account id', str(ctx.exception))

    def test_non_ascii_digit_account_id_raises(self):
        # Unicode digits (e.g. Arabic-Indic) are rejected; only ASCII 0-9 allowed.
        from alibabacloud_oss_v2 import models as oss_models
        http = RecordingHttpClient(self._ok_response())
        client = self._client(http, account_id='١٢٣')
        with self.assertRaises(Exception) as ctx:
            client.put_bucket(oss_models.PutBucketRequest(bucket='my-agent'))
        self.assertIn('invalid account id', str(ctx.exception))

    def test_user_agent_marker_then_custom(self):
        http = RecordingHttpClient(self._ok_response())
        cfg = config.load_default()
        cfg.region = 'cn-hangzhou'
        cfg.account_id = '1234567890123456'
        cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
        cfg.http_client = http
        cfg.user_agent = 'mytool/1.0'
        client = BucketSpaceClient.create(cfg)
        ua = client._client._inner.user_agent
        self.assertIn('/bucketspace-client/mytool/1.0', ua)
        self.assertTrue(ua.startswith('alibabacloud-python-sdk-v2/'))


if __name__ == '__main__':
    unittest.main()
