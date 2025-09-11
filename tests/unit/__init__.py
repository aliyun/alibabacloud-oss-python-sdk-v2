# pylint: skip-file
from typing import Any
from alibabacloud_oss_v2 import _client
from alibabacloud_oss_v2.aio._aioclient import _AsyncClientImpl
from alibabacloud_oss_v2 import config, credentials
from alibabacloud_oss_v2.types import HttpRequest, HttpResponse, HttpClient
from alibabacloud_oss_v2.types import HttpRequest, AsyncHttpResponse, AsyncHttpClient

class MockHttpResponse(HttpResponse):
    def __init__(self, **kwargs) -> None:
        super(MockHttpResponse, self).__init__()
        self._status_code = kwargs.pop("status_code", None)
        self._reason = kwargs.pop("reason", None)
        self._headers = kwargs.pop("headers", None)
        self._body = kwargs.pop("body", None)
        self._is_closed = False
        self._is_stream_consumed = False
        self._request: HttpRequest = None

    @property
    def request(self) -> HttpRequest:
        return self._request

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    @property
    def is_stream_consumed(self) -> bool:
        return self._is_stream_consumed

    @property
    def status_code(self) -> int:
        return self._status_code or 0

    @property
    def headers(self):
        return self._headers or {}

    @property
    def reason(self) -> str:
        return self._reason or ''

    @property
    def content(self) -> bytes:
        if self._body is not None:
            if not isinstance(self._body, (bytes, str)):
                raise TypeError(f"not support type {type(self._body)}")
            if isinstance(self._body, str):
                return self._body.encode()
        return self._body

    def __repr__(self) -> str:
        return 'MockHttpResponse'

    def __enter__(self) -> "MockHttpResponse":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        if not self.is_closed:
            self._is_closed = True

    def read(self) -> bytes:
        return self.content

    def iter_bytes(self, **kwargs):
        data = b''
        block_size = kwargs.get('block_size', 8*1024)
        if self._body is not None:
            data = self._body
            if not isinstance(self._body, (bytes, str)):
                raise TypeError(f"not support type {type(self._body)}")            
            if isinstance(self._body, str):
                data  = self._body.encode()

        for i in range(0, len(data), block_size):
            yield self.content[i : i + block_size]        
 
class MockHttpClient(HttpClient):

    def __init__(self, request_fn, response_fn, **kwargs) -> None:
        super(MockHttpClient, self).__init__()
        self._request_fn = request_fn
        self._response_fn = response_fn

    def send(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        if self._request_fn is not None:
            self._request_fn(request)

        if self._response_fn is not None:
            response = self._response_fn()
            response._request = request
            return response

        raise NotImplementedError()

    def open(self) -> None:
        return

    def close(self) -> None:
        return


def mock_client(request_fn, response_fn, **kwargs):
    cfg = config.load_default()
    cfg.region = 'cn-hangzhou'
    cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
    cfg.http_client = MockHttpClient(
        request_fn=request_fn,
        response_fn=response_fn,
        kwargs=kwargs
    )
    return _client._SyncClientImpl(cfg)



class MockAsyncHttpResponse(AsyncHttpResponse):
    def __init__(self, **kwargs) -> None:
        super(MockAsyncHttpResponse, self).__init__()
        self._status_code = kwargs.pop("status_code", None)
        self._reason = kwargs.pop("reason", None)
        self._headers = kwargs.pop("headers", None)
        self._body = kwargs.pop("body", None)
        self._is_closed = False
        self._is_stream_consumed = False
        self._request: HttpRequest = None

    @property
    def request(self) -> HttpRequest:
        return self._request

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    @property
    def is_stream_consumed(self) -> bool:
        return self._is_stream_consumed

    @property
    def status_code(self) -> int:
        return self._status_code or 0

    @property
    def headers(self):
        return self._headers or {}

    @property
    def reason(self) -> str:
        return self._reason or ''

    @property
    def content(self) -> bytes:
        if self._body is not None:
            if not isinstance(self._body, (bytes, str)):
                raise TypeError(f"not support type {type(self._body)}")
            if isinstance(self._body, str):
                return self._body.encode()
        return self._body

    def __repr__(self) -> str:
        return 'MockHttpResponse'

    async def __aenter__(self) -> "MockAsyncHttpResponse":
        return self

    async def __aexit__(
        self,
        exc_type  = None,
        exc_value = None,
        traceback = None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if not self.is_closed:
            self._is_closed = True

    async def read(self) -> bytes:
        return self.content

    async def iter_bytes(self, **kwargs):
        data = b''
        block_size = kwargs.get('block_size', 8*1024)
        if self._body is not None:
            data = self._body
            if not isinstance(self._body, (bytes, str)):
                raise TypeError(f"not support type {type(self._body)}")            
            if isinstance(self._body, str):
                data  = self._body.encode()

        for i in range(0, len(data), block_size):
            yield self.content[i : i + block_size]        
 
class MockAsyncHttpClient(AsyncHttpClient):

    def __init__(self, request_fn, response_fn, **kwargs) -> None:
        super(MockAsyncHttpClient, self).__init__()
        self._request_fn = request_fn
        self._response_fn = response_fn

    async def send(self, request: HttpRequest, **kwargs: Any) -> AsyncHttpResponse:
        if self._request_fn is not None:
            self._request_fn(request)

        if self._response_fn is not None:
            response = self._response_fn()
            response._request = request
            return response

        raise NotImplementedError()

    async def open(self) -> None:
        return

    async def close(self) -> None:
        return


def mock_client(request_fn, response_fn, **kwargs):
    cfg = config.load_default()
    cfg.region = 'cn-hangzhou'
    cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
    cfg.http_client = MockHttpClient(
        request_fn=request_fn,
        response_fn=response_fn,
        kwargs=kwargs
    )
    return _client._SyncClientImpl(cfg)

def mock_async_client(request_fn, response_fn, **kwargs):
    cfg = config.load_default()
    cfg.region = 'cn-hangzhou'
    cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
    cfg.http_client = MockAsyncHttpClient(
        request_fn=request_fn,
        response_fn=response_fn,
        kwargs=kwargs
    )
    return _AsyncClientImpl(cfg)