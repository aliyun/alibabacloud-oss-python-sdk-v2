"""HttpClient implement based on requests
"""
from typing import Optional, MutableMapping, Iterator, cast
from urllib3.util.retry import Retry
from urllib3.exceptions import NewConnectionError, ConnectTimeoutError
import requests
import requests.adapters

from ..types import HttpRequest, HttpResponse, HttpClient
from .. import exceptions
from .. import defaults


class _RequestsHttpResponseImpl(HttpResponse):
    """Implementation class for HttpRespone from requests's response
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._request = kwargs.pop("request")
        self._block_size = kwargs.pop("block_size")
        self._internal_response = cast(requests.Response, kwargs.pop("internal_response"))
        self._is_closed = False
        self._is_stream_consumed = False
        self._content = None

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
        return self._internal_response.status_code

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

    def __repr__(self) -> str:
        content_type = self.headers.get("Content-Type", "")
        return f"<HttpResponse: {self.status_code} {self.reason}, Content-Type: {content_type}>"

    def __enter__(self) -> "_RequestsHttpResponseImpl":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        if not self.is_closed:
            self._is_closed = True
            self._internal_response.close()

    def read(self) -> bytes:
        if self._content is None:
            self._content = self._internal_response.content
        self._set_read_checks()
        return self._content

    def iter_bytes(self, **kwargs) -> Iterator[bytes]:
        """Iterates over the response's bytes.

        Args:
            block_size (int, optional): The number of bytes it should read into memory.

        Returns:
            Iterator[bytes]: An iterator of bytes from the response
        """
        block_size = kwargs.pop("block_size", self._block_size)

        return self._internal_response.iter_content(block_size)

    def _set_read_checks(self):
        self._is_stream_consumed = True
        self.close()

def convert_proxy_host(proxy_host):
    if proxy_host is None:
        return None

    if isinstance(proxy_host, str):
        return {"http://": proxy_host, "https://": proxy_host}

    if isinstance(proxy_host, dict):
        return proxy_host

    raise exceptions.RequestError(error="proxy_host must be str or dict")


class RequestsHttpClient(HttpClient):
    """Implements a basic requests HTTP sender.

    In this implementation:
    - You provide the configured session if you want to, or a basic session is created.
    - All kwargs received by "do" are sent to session.request directly
    """

    _protocols = ["http://", "https://"]

    def __init__(self, **kwargs) -> None:
        """
        Args:
            session (requests.Session, optional): Request session to use
                instead of the default one.
            adapters (requests.adapters, optional): Request adapters to use
                instead of the default one.
        """

        self.session_owner = False
        self.session = kwargs.get("session", None)
        self.adapter = kwargs.get("adapter", None)

        # client's configuration
        self._connect_timeout = kwargs.get("connect_timeout", defaults.DEFAULT_CONNECT_TIMEOUT)
        self._read_timeout = kwargs.get("readwrite_timeout", defaults.DEFAULT_READWRITE_TIMEOUT)
        self._max_connections = kwargs.get("max_connections", defaults.DEFAULT_MAX_CONNECTIONS)
        self._verify = True
        if kwargs.get("insecure_skip_verify") is True:
            self._verify = False
        self._allow_redirects = kwargs.get("enabled_redirect", False)
        self._proxies = convert_proxy_host(kwargs.get("proxy_host", None))
        self._block_size = kwargs.get("block_size", defaults.DEFAULT_BLOCK_SIZE)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def _init_session(self, session: requests.Session) -> None:
        """Init session level configuration of requests.
        This is initialization I want to do once only on a session.
        """
        if self.adapter is None:
            disable_retries = Retry(total=False, redirect=False, raise_on_status=False)
            self.adapter = requests.adapters.HTTPAdapter(max_retries=disable_retries,
                                                         pool_maxsize=self._max_connections,
                                                         pool_connections=self._max_connections)

        self.adapter = cast(requests.adapters.HTTPAdapter, self.adapter)
        for p in self._protocols:
            session.mount(p, self.adapter)

    def open(self):
        if not self.session:
            self.session = requests.Session()
            self.session_owner = True
            self._init_session(self.session)
        self.session = cast(requests.Session, self.session)

    def close(self):
        if self.session_owner and self.session is not None:
            self.session.close()
            self.session_owner = False
            self.session = None

    def send(self, request: HttpRequest, **kwargs) -> HttpResponse:
        self.open()
        error: Optional[Exception] = None
        resp: _RequestsHttpResponseImpl = None

        try:
            # api's configuration
            connect_timeout = kwargs.pop("connect_timeout", self._connect_timeout)
            read_timeout = kwargs.pop("readwrite_timeout", self._read_timeout)
            stream = kwargs.pop("stream", False)

            # tell requests not to add 'Accept-Encoding: gzip, deflate' by default
            if 'accept-encoding' not in request.headers:
                request.headers.update({'Accept-Encoding': None})

            response = self.session.request(
                request.method,
                request.url,
                headers=request.headers,
                data=request.body,
                verify=self._verify,
                timeout=(connect_timeout, read_timeout),
                allow_redirects=self._allow_redirects,
                proxies=self._proxies,
                stream=stream,
                **kwargs
            )

            resp = _RequestsHttpResponseImpl(
                request=request,
                internal_response=response,
                block_size=self._block_size
            )

            if not stream:
                _ = resp.read()
                resp.close()

        except (NewConnectionError, ConnectTimeoutError) as err:
            error = exceptions.RequestError(error=err)
        except requests.exceptions.ConnectionError as err:
            error = exceptions.RequestError(error=err)
        except requests.exceptions.ReadTimeout as err:
            error = exceptions.ResponseError(error=err)
        except requests.RequestException as err:
            error = exceptions.RequestError(error=err)

        if error:
            raise error

        return resp

