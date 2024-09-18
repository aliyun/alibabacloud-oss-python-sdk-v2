# pylint: skip-file
import unittest
from alibabacloud_oss_v2.types import HttpRequest, HttpResponse, HttpClient
from .. import MockHttpResponse, mock_client

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.set_requestFunc(None)
        self.set_responseFunc(None)

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls.request_dump: HttpRequest = None
        cls.client = mock_client(cls.requestFunc, cls.responseFunc)
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


