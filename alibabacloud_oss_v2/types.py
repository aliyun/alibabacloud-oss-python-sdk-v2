"""Type Information
"""
import abc
import datetime
from typing import (
    Optional,
    Any,
    Iterable,
    Iterator,
    Union,
    IO,
    MutableMapping,
    Mapping,
    Set,
    Dict,
    AsyncIterator,
    AsyncContextManager,
)
from requests.structures import CaseInsensitiveDict

BodyType = Union[str, bytes, Iterable[bytes], IO[str], IO[bytes]]


class Credentials:
    """
    Holds the credentials needed to authenticate requests.

    :type access_key_id: str
    :param access_key_id: The access key id of the credentials.

    :type access_key_secret: str
    :param access_key_secret: The access key secret of the credentials.

    :type security_token: str
    :param security_token: The security token of the credentials.    

    :type expiration: datetime.datetime
    :param expiration: The token's expiration time in utc.    

    """

    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        security_token: Optional[str] = None,
        expiration: Optional[datetime.datetime] = None,
    ) -> None:
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.security_token = security_token
        self.expiration = expiration

    def has_keys(self) -> bool:
        """Check whether the credentials keys are set.

        :rtype: bool
        :return: True if the credentials keys are set.
        """
        if self.access_key_id is None or len(self.access_key_id) == 0:
            return False

        if self.access_key_secret is None or len(self.access_key_secret) == 0:
            return False

        return True

    def is_expired(self) -> bool:
        """Check whether the credentials have expired.

        :rtype: bool
        :return: True if the credentials have expired.
        """

        if self.expiration is None:
            return False
        now = datetime.datetime.now(datetime.timezone.utc)
        return self.expiration < now


class CredentialsProvider(abc.ABC):
    """Abstract base class for CredentialsProvider."""

    @abc.abstractmethod
    def get_credentials(self) -> Credentials:
        """Retrieve the credentials.

        :rtype: Credentials
        :return: a Credentials instance if it successfully retrieved the value.
        """


class Retryer(abc.ABC):
    """Abstract base class for Retryer."""

    @abc.abstractmethod
    def is_error_retryable(self, error: Exception) -> bool:
        """Check whether the error is retryable.

        :type error: Exception
        :param error: the error meets

        :rtype: bool
        :return: True if the error is retryable.
        """

    @abc.abstractmethod
    def max_attempts(self) -> int:
        """Retrieve max attempts.

        :rtype: int
        :return: max attempts.
        """

    @abc.abstractmethod
    def retry_delay(self, attempt: int, error: Exception) -> float:
        """Returns the delay that should be used before retrying the attempt.

        :type attempt: int
        :param attempt: current retry attempt

        :type error: Exception
        :param error: the error meets

        :rtype: float
        :return: delay duration in second.
        """

class HttpRequest:
    """A HttpRequest represents an HTTP request received by a server or to be sent by a client.

    It should be passed to your client's `send` method.

    :type method: str
    :param method: HTTP method (GET, HEAD, etc.)

    :type url: str
    :param url: The url for your request

    :type headers: mapping
    :param headers:  HTTP headers you want in your request. Your input should
        be a mapping of header name to header value.

    :type params: mapping
    :param params: Query parameters to be mapped into your URL. Your input
        should be a mapping of query name to query value(s).

    :type body: str or bytes or iterable[bytes] or IO[str] or IO[bytes]
    :param body: The request's body.

    """

    def __init__(
        self,
        method: str,
        url: str,
        headers: Optional[MutableMapping[str, str]] = None,
        body: Optional[BodyType] = None,
        #**kwargs: Any
    ):
        self.method = method
        self.url = url

        # params
        # params: Optional[Mapping[str, str]] = None,
        # self.params = params

        # body
        self.body = body

        # header
        default_headers: MutableMapping[str, str] = {}
        self.headers = CaseInsensitiveDict(default_headers)
        self.headers.update(headers or {})

    def __repr__(self) -> str:
        return f"<HttpRequest [{self.method}], url: '{self.url}'>"


class _HttpResponseBase(abc.ABC):
    """Base abstract base class for HttpResponses"""

    @property
    @abc.abstractmethod
    def request(self) -> HttpRequest:
        """The request that resulted in this response.

        :rtype: HttpRequest
        :return: The request that resulted in this response.
        """

    @property
    @abc.abstractmethod
    def status_code(self) -> int:
        """The status code of this response.

        :rtype: int
        :return: The status code of this response.
        """

    @property
    @abc.abstractmethod
    def headers(self) -> MutableMapping[str, str]:
        """The response headers. Must be case-insensitive.

        :rtype: MutableMapping[str, str]
        :return: The response headers. Must be case-insensitive.
        """

    @property
    @abc.abstractmethod
    def reason(self) -> str:
        """Textual reason of responded HTTP Status, e.g. "Not Found" or "OK".

        :rtype: str
        :return: Textual reason of responded HTTP Status
        """

    @property
    @abc.abstractmethod
    def is_closed(self) -> bool:
        """Whether the network connection has been closed yet.

        :rtype: bool
        :return: Whether the network connection has been closed yet.
        """
    @property
    @abc.abstractmethod
    def is_stream_consumed(self) -> bool:
        """Whether the stream has been consumed.

        :rtype: bool
        :return: Whether the stream has been consumed.
        """

    @property
    @abc.abstractmethod
    def content(self) -> bytes:
        """Content of the response, in bytes.

        :rtype: bytes
        :return: The response's content in bytes.
        """

class HttpResponse(_HttpResponseBase):
    """Abstract base class for a HttpResponse, the response from an HTTP request."""

    @abc.abstractmethod
    def __enter__(self) -> "HttpResponse": ...

    @abc.abstractmethod
    def __exit__(self, *args: Any) -> None: ...

    @abc.abstractmethod
    def read(self) -> bytes:
        """Read the response's bytes.

        :return: The read in bytes
        :rtype: bytes
        """

    @abc.abstractmethod
    def close(self) -> None:
        """close the response"""

    @abc.abstractmethod
    def iter_bytes(self, **kwargs: Any) -> Iterator[bytes]:
        """Iterates over the response's bytes. Will decompress in the process.

        :return: An iterator of bytes from the response
        :rtype: Iterator[str]
        """

    def __repr__(self) -> str:
        return f'<HttpResponse: {self.status_code} {self.reason}>'

class HttpClient(abc.ABC):
    """Abstract base class for HTTP client."""

    @abc.abstractmethod
    def send(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        """Sends an HTTP request and returns an HTTP response.

        An error is returned if caused by client policy (such as CheckRedirect), 
        or failure to speak HTTP (such as a network connectivity problem). 
        A non-2xx status code doesn't cause an error.

        :type request: Any
        :param request: the http request sent to server.

        :rtype: httpResponse
        :return: The response object.
        """

    @abc.abstractmethod
    def open(self) -> None:
        """Assign new session if one does not already exist."""

    @abc.abstractmethod
    def close(self) -> None:
        """Close the session if it is not externally owned."""


class SigningContext(object):
    """SigningContext is the signing context."""

    def __init__(
        self,
        product: Optional[str] = None,
        region: Optional[str] = None,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        request: Optional[HttpRequest] = None,
        credentials: Optional[Credentials] = None,
        signing_time: Optional[datetime.datetime] = None,
        clock_offset: Optional[int] = 0,
        additional_headers: Optional[Set[str]] = None,
    ) -> None:
        self.product = product
        self.region = region
        self.bucket = bucket
        self.key = key
        self.request = request
        self.credentials = credentials
        self.auth_method_query = False
        self.signing_time = signing_time
        self.clock_offset = clock_offset
        self.signed_headers = {}
        self.string_to_sign = ''
        self.additional_headers = additional_headers
        self.expiration_time: Optional[datetime.datetime] = None
        self.sub_resource: Optional[str] = []


class Signer(abc.ABC):
    """Abstract base class for Signer."""

    @abc.abstractmethod
    def sign(self, signing_ctx: SigningContext) -> None:
        """sign HTTP requests.

        :type signing_ctx: SigningContext
        :param signing_ctx: the signing context

        """


class OperationInput:
    """Operation Input
    """

    def __init__(
        self,
        op_name: str,
        method: str,
        headers: Optional[MutableMapping[str, str]] = None,
        parameters: Optional[Mapping[str, str]] = None,
        body: Optional[BodyType] = None,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        op_metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.op_name = op_name
        self.method = method
        self.headers = headers
        self.parameters = parameters
        self.body = body
        self.bucket = bucket
        self.key = key
        self.op_metadata = op_metadata or {}

    def __str__(self) -> str:
        return str(self.__dict__)

class OperationOutput:
    """Operation Output
    """

    def __init__(
        self,
        status: str,
        status_code: int,
        headers: Optional[MutableMapping[str, str]] = None,
        body: Optional[BodyType] = None,
        op_metadata: Optional[Dict[str, Any]] = None,
        op_input: Optional[OperationInput] = None,
        http_response: Optional[HttpResponse] = None,
    ) -> None:
        self.status = status
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.op_input = op_input
        self.op_metadata = op_metadata or {}
        self.http_response = http_response

    def __str__(self) -> str:
        return str(self.__dict__)

class StreamBody(abc.ABC):
    """Abstract base class for a StreamBody."""

    @abc.abstractmethod
    def __enter__(self) -> "StreamBody": ...

    @abc.abstractmethod
    def __exit__(self, *args: Any) -> None: ...

    @property
    @abc.abstractmethod
    def is_closed(self) -> bool:
        """Whether the stream has been closed yet.

        :rtype: bool
        :return: Whether the stream has been closed yet.
        """

    @property
    @abc.abstractmethod
    def is_stream_consumed(self) -> bool:
        """Whether the stream has been consumed.

        :rtype: bool
        :return: Whether the stream has been consumed.
        """

    @property
    @abc.abstractmethod
    def content(self) -> bytes:
        """Content of the stream, in bytes.

        :rtype: bytes
        :return: The stream's content in bytes.
        """

    @abc.abstractmethod
    def read(self) -> bytes:
        """Read the stream's bytes.

        :return: The read in bytes
        :rtype: bytes
        """

    @abc.abstractmethod
    def close(self) -> None:
        """close the stream"""

    @abc.abstractmethod
    def iter_bytes(self, **kwargs: Any) -> Iterator[bytes]:
        """Iterates over the stream's bytes. Will decompress in the process.

        :return: An iterator of bytes from the stream
        :rtype: Iterator[str]
        """

class EndpointProvider(abc.ABC):
    """Abstract base class for a EndpointProvider."""

    @abc.abstractmethod
    def build_url(self, op_input: OperationInput) -> None:
        """build the request url"""

class AsyncStreamBody(abc.ABC):
    """Abstract base class for a AsyncStreamBody."""

    @abc.abstractmethod
    async def __aenter__(self):
        """Return `self` upon entering the runtime context."""

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        """Raise any exception triggered within the runtime context."""

    @property
    @abc.abstractmethod
    def is_closed(self) -> bool:
        """Whether the stream has been closed yet.

        :rtype: bool
        :return: Whether the stream has been closed yet.
        """

    @property
    @abc.abstractmethod
    def is_stream_consumed(self) -> bool:
        """Whether the stream has been consumed.

        :rtype: bool
        :return: Whether the stream has been consumed.
        """

    @property
    @abc.abstractmethod
    def content(self) -> bytes:
        """Content of the stream, in bytes.

        :rtype: bytes
        :return: The stream's content in bytes.
        """

    @abc.abstractmethod
    async def read(self) -> bytes:
        """Read the stream's bytes.

        :return: The read in bytes
        :rtype: bytes
        """

    @abc.abstractmethod
    async def close(self) -> None:
        """close the stream"""

    @abc.abstractmethod
    async def iter_bytes(self, **kwargs: Any) -> AsyncIterator[bytes]:
        """Iterates over the stream's bytes. Will decompress in the process.

        :return: An iterator of bytes from the stream
        :rtype: Iterator[str]
        """

class AsyncHttpResponse(_HttpResponseBase, AsyncContextManager["AsyncHttpResponse"]):
    """Abstract base class for a HttpResponse, the response from an HTTP request."""

    @abc.abstractmethod
    async def read(self) -> bytes:
        """Read the response's bytes.

        :return: The read in bytes
        :rtype: bytes
        """

    @abc.abstractmethod
    async def close(self) -> None:
        """close the response"""

    @abc.abstractmethod
    async def iter_bytes(self, **kwargs: Any) -> AsyncIterator[bytes]:
        """Asynchronously iterates over the response's bytes. Will decompress in the process.

        :return: An async iterator of bytes from the response
        :rtype: AsyncIterator[bytes]
        """
        raise NotImplementedError()
        yield  # pylint: disable=unreachable

    def __repr__(self) -> str:
        return f'<AsyncHttpResponse: {self.status_code} {self.reason}>'


class AsyncHttpClient(abc.ABC):
    """Abstract base class for Async HTTP client."""

    @abc.abstractmethod
    async def send(self, request: HttpRequest, **kwargs: Any) -> AsyncHttpResponse:
        """Sends an HTTP request and returns an HTTP response.

        An error is returned if caused by client policy (such as CheckRedirect), 
        or failure to speak HTTP (such as a network connectivity problem). 
        A non-2xx status code doesn't cause an error.

        :type request: Any
        :param request: the http request sent to server.

        :rtype: httpResponse
        :return: The response object.
        """

    @abc.abstractmethod
    async def open(self) -> None:
        """Assign new session if one does not already exist."""

    @abc.abstractmethod
    async def close(self) -> None:
        """Close the session if it is not externally owned."""
