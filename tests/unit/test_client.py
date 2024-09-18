# pylint: skip-file
import tempfile
import unittest
from alibabacloud_oss_v2 import models, config, client, credentials, exceptions
from alibabacloud_oss_v2.types import HttpRequest, HttpResponse, HttpClient
from . import MockHttpResponse, MockHttpClient


def _mock_client(request_fn, response_fn, **kwargs):
    cfg = config.load_default()
    cfg.region = 'cn-hangzhou'
    cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
    cfg.http_client = MockHttpClient(
        request_fn=request_fn,
        response_fn=response_fn,
        kwargs=kwargs
    )
    return client.Client(cfg)

def _get_tempfile() -> str:
    filename = ''
    with tempfile.TemporaryFile('w+b', delete=False) as f:
        filename = f.name
    return filename


progress_save_n = 0
def _progress_fn(n, _written, total):
    global progress_save_n
    progress_save_n += n

class TestClientBase(unittest.TestCase):
    def setUp(self):
        self.set_requestFunc(None)
        self.set_responseFunc(None)

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls.request_dump: HttpRequest = None
        cls.client = _mock_client(cls.requestFunc, cls.responseFunc)
        cls.invoke_request = None
        cls.invoke_response = None

    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def requestFunc(cls, request: HttpRequest):
        cls.request_dump = request
        if cls.invoke_request is not None:
            cls.invoke_request(request)

    @classmethod
    def responseFunc(cls) -> MockHttpResponse:
        if cls.invoke_response is not None:
            return cls.invoke_response()

        return MockHttpResponse(
            status_code=200,
            reason='OK',
            headers={'x-oss-request-id': 'id-1234'},
            body=''
        )

    @classmethod
    def set_requestFunc(cls, fn):
        cls.invoke_request = fn

    @classmethod
    def set_responseFunc(cls, fn):
        cls.invoke_response = fn

    @classmethod
    def response_403_InvalidAccessKeyId(cls) -> MockHttpResponse:
        err_xml = r'''<?xml version="1.0" encoding="UTF-8"?>
            <Error>
                <Code>InvalidAccessKeyId</Code>
                <Message>The OSS Access Key Id you provided does not exist in our records.</Message>
                <RequestId>id-1234</RequestId>
                <HostId>oss-cn-hangzhou.aliyuncs.com</HostId>
                <OSSAccessKeyId>ak</OSSAccessKeyId>
                <EC>0002-00000902</EC>
                <RecommendDoc>https://api.aliyun.com/troubleshoot?q=0002-00000902</RecommendDoc>
            </Error>
        '''
        return MockHttpResponse(
            status_code=403,
            reason='Forbidden',
            headers={
                'Server': 'AliyunOSS',
                'Date': 'Tue, 23 Jul 2024 13:01:06 GMT',
                'Content-Type': 'application/xml',
                'x-oss-ec': '0002-00000902',
                'x-oss-request-id': 'id-1234',
            },
            body=err_xml.encode()
        )

class TestClientExtension(TestClientBase):
    def test_get_object_to_file(self):
        def response_200() -> MockHttpResponse:
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={
                    'Server': 'AliyunOSS',
                    'Date': 'Tue, 03 Sep 2024 06:33:10 GMT',
                    'Content-Length': '11',
                    'Content-MD5': 'XrY7u+Ae7tCTyyK7j1rNww==',
                    'x-oss-request-id': 'id-1234',
                    'x-oss-hash-crc64ecma': '5981764153023615706',
                },
                body=b'hello world'
            )

        self.set_responseFunc(response_200)
        request = models.GetObjectRequest(
            bucket='bucket',
            key='123%456+789#0',
        )
        filepath = _get_tempfile()
        result = self.client.get_object_to_file(request, filepath)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/123%25456%2B789%230', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)
        self.assertEqual('5981764153023615706', result.hash_crc64)

        data = b''
        with open(filepath, 'rb') as f:
            data = f.read()

        self.assertEqual(b'hello world', data)

        #progress
        global progress_save_n
        progress_save_n = 0
        request = models.GetObjectRequest(
            bucket='bucket',
            key='123%456+789#0',
            progress_fn=_progress_fn,
        )
        filepath = _get_tempfile()
        result = self.client.get_object_to_file(request, filepath)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/123%25456%2B789%230', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)
        self.assertEqual('5981764153023615706', result.hash_crc64)
        self.assertEqual(11, progress_save_n)

    def test_get_object_to_file_crc_fail(self):
        def response_200() -> MockHttpResponse:
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={
                    'Server': 'AliyunOSS',
                    'Date': 'Tue, 03 Sep 2024 06:33:10 GMT',
                    'Content-Length': '11',
                    'Content-MD5': 'XrY7u+Ae7tCTyyK7j1rNww==',
                    'x-oss-request-id': 'id-1234',
                    'x-oss-hash-crc64ecma': '5981764153023615707',
                },
                body=b'hello world'
            )

        self.set_responseFunc(response_200)
        request = models.GetObjectRequest(
            bucket='bucket',
            key='123%456+789#0',
        )
        filepath = _get_tempfile()
        try:
            self.client.get_object_to_file(request, filepath)
            self.fail('should not here')
        except exceptions.InconsistentError as err:
            self.assertIn('crc is inconsistent, client 5981764153023615706, server 5981764153023615707', str(err))

