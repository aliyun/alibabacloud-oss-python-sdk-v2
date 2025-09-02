"""AsyncHttpClient implement based on aiohttp
"""
from typing import cast, MutableMapping, Optional, Type, AsyncIterator, Any, Callable
from types import TracebackType
import collections.abc
import asyncio

try:
    import aiohttp
    import aiohttp.client_exceptions
except ImportError:
    raise ImportError("Please install aiohttp by `pip install aiohttp`")

from ...types import AsyncHttpClient, HttpRequest, AsyncHttpResponse
from ... import exceptions
from ... import defaults

class _ResponseStopIteration(Exception):
    pass

class _AioHttpStreamDownloadGenerator(collections.abc.AsyncIterator):
    """Streams the response body data.
    """

    def __init__(
        self,
        response: "_AioHttpResponseImpl",
        block_size: Optional[int] = None
    ) -> None:
        self.response = response
        self.block_size = block_size or response._block_size
        self.content_length = int(response.headers.get("Content-Length", 0))

    def __len__(self):
        return self.content_length

    async def __anext__(self):
        error: Optional[Exception] = None
        internal_response = self.response._internal_response  # pylint: disable=protected-access
        try:
            chunk = await internal_response.content.read(self.block_size)  # pylint: disable=protected-access
            if not chunk:
                raise _ResponseStopIteration()
            return chunk
        except _ResponseStopIteration:
            internal_response.close()
            raise StopAsyncIteration()  # pylint: disable=raise-missing-from
        except aiohttp.client_exceptions.ClientPayloadError as err:
            error = err
            internal_response.close()
        except aiohttp.client_exceptions.ClientResponseError as err:
            error = err
        except asyncio.TimeoutError as err:
            error = err
        except aiohttp.client_exceptions.ClientError as err:
            error = err
        except Exception as err: # pylint: disable=broad-exception-caught
            internal_response.close()

        if error is not None:
            raise error

class _AioHttpResponseImpl(AsyncHttpResponse):
    """
    Implementation class for AsyncHttpResponse from aiohttp's response
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._request = kwargs.pop("request")
        self._block_size = kwargs.pop("block_size", None) or 4096
        self._internal_response = cast(aiohttp.ClientResponse, kwargs.pop("internal_response"))
        self._is_closed = False
        self._is_stream_consumed = False
        self._content: Optional[bytes] = None
        self._stream_download_generator: Callable = _AioHttpStreamDownloadGenerator

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
        return self._internal_response.status

    @property
    def headers(self) -> MutableMapping[str, str]:
        return self._internal_response.headers

    @property
    def reason(self) -> str:
        return self._internal_response.reason

    @property
    def content(self) -> bytes:
        if self._content is None:
            raise exceptions.ResponseNotReadError()
        return self._content

    async def read(self) -> bytes:
        if not self._content:
            self._stream_download_check()
            self._content = await self._internal_response.read()
        await self._set_read_checks()
        return self._content

    async def close(self) -> None:
        if not self.is_closed:
            self._is_closed = True
            self._internal_response.close()
            await asyncio.sleep(0)

    async def iter_bytes(self, **kwargs: Any) -> AsyncIterator[bytes]:
        """Asynchronously iterates over the response's bytes.

        Args:
            block_size (int, optional): The number of bytes it should read into memory.

        Returns:
            AsyncIterator[bytes]: An async iterator of bytes from the response
        """
        block_size = kwargs.pop("block_size", self._block_size)

        if self._content is not None:
            for i in range(0, len(self.content), block_size):
                yield self.content[i : i + block_size]
        else:
            self._stream_download_check()
            async for part in self._stream_download_generator(response=self, block_size=block_size):
                yield part
            await self.close()


    async def __aenter__(self) -> "_AioHttpResponseImpl":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        await self.close()

    def _stream_download_check(self):
        if self._is_stream_consumed:
            raise exceptions.StreamConsumedError()
        if self.is_closed:
            raise exceptions.StreamClosedError()
        self._is_stream_consumed = True

    async def _set_read_checks(self):
        self._is_stream_consumed = True
        await self.close()

class AioHttpClient(AsyncHttpClient):
    """Implements a basic aiohttp HTTP sender.
    """

    def __init__(self, **kwargs) -> None:
        self.session_owner = False
        self.session = kwargs.get("session", None)
        # client's configuration
        self._connect_timeout = kwargs.get(
            "connect_timeout", defaults.DEFAULT_CONNECT_TIMEOUT)
        self._read_timeout = kwargs.get(
            "readwrite_timeout", defaults.DEFAULT_READWRITE_TIMEOUT)
        self._max_connections = kwargs.get(
            "max_connections", defaults.DEFAULT_MAX_CONNECTIONS)
        self._verify = True
        if kwargs.get("insecure_skip_verify") is True:
            self._verify = False
        self._allow_redirects = kwargs.get("enabled_redirect", False)
        self._proxies = kwargs.get("proxy_host", None)
        self._block_size = kwargs.get("block_size", defaults.DEFAULT_BLOCK_SIZE)

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        await self.close()

    async def open(self):
        if not self.session:
            clientsession_kwargs = {}
            self.session = aiohttp.ClientSession(**clientsession_kwargs)
            self.session_owner = True
        self.session = cast(aiohttp.ClientSession, self.session)
        await self.session.__aenter__()

    async def close(self):
        if self.session_owner and self.session:
            await self.session.close()
            self.session_owner = False
            self.session = None

    async def send(self, request: HttpRequest, **kwargs: Any) -> AsyncHttpResponse:
        await self.open()
        error: Optional[Exception] = None
        resp: _AioHttpResponseImpl = None

        try:
            # api's configuration
            connect_timeout = kwargs.pop("connect_timeout", self._connect_timeout)
            read_timeout = kwargs.pop("readwrite_timeout", self._read_timeout)
            stream = kwargs.pop("stream", False)
            socket_timeout = aiohttp.ClientTimeout(
                sock_connect=connect_timeout,
                sock_read=read_timeout
            )
            response = await self.session.request(  # type: ignore
                request.method,
                request.url,
                headers=request.headers,
                data=request.body,
                timeout=socket_timeout,
                allow_redirects=False,
                skip_auto_headers={"Content-Type", "Accept-Encoding"},
                proxy=self._proxies,
                **kwargs
            )

            resp = _AioHttpResponseImpl(
                request=request,
                internal_response=response,
                block_size=self._block_size
            )

            if not stream:
                await _handle_no_stream_response(resp)

        except aiohttp.client_exceptions.ClientResponseError as err:
            error = exceptions.ResponseError(error=err)
        except asyncio.TimeoutError as err:
            error = exceptions.ResponseError(error=err)
        except aiohttp.client_exceptions.ClientError as err:
            error = exceptions.RequestError(error=err)

        if error:
            raise error

        return resp

async def _handle_no_stream_response(response: "_AioHttpResponseImpl") -> None:
    """Handle reading and closing of non stream rest responses.
    For our new rest responses, we have to call .read() and .close() for our non-stream
    responses. This way, we load in the body for users to access.

    :param response: The response to read and close.
    :type response: ~azure.core.rest.AsyncHttpResponse
    """
    try:
        await response.read()
        await response.close()
    except Exception as exc:
        await response.close()
        raise exc
