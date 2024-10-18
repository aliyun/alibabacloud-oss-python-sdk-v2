"""_summary_
"""
import abc
import datetime
import struct
import sys
import crcmod
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


class Signer(abc.ABC):
    """Abstract base class for Signer."""

    @abc.abstractmethod
    def sign(self, signing_ctx: SigningContext) -> None:
        """sign HTTP requests.

        :type signing_ctx: SigningContext
        :param signing_ctx: the signing context

        """


class OperationInput:
    """_summary_
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
    """_summary_
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


class SelectResult(object):
    def __init__(self, resp, progress_callback=None, content_length=None, crc_enabled=False):
        self.select_resp = SelectResponseAdapter(resp, progress_callback, content_length, enable_crc=crc_enabled)

    def read(self):
        return self.select_resp.response.read()

    def close(self):
        self.select_resp.response.close()

    def __iter__(self):
        return iter(self.select_resp)

    def __next__(self):
        return self.select_resp.next()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SelectResponseAdapter(object):
    _CHUNK_SIZE = 8 * 1024
    _CONTINIOUS_FRAME_TYPE = 8388612
    _DATA_FRAME_TYPE = 8388609
    _END_FRAME_TYPE = 8388613
    _META_END_FRAME_TYPE = 8388614
    _JSON_META_END_FRAME_TYPE = 8388615
    _FRAMES_FOR_PROGRESS_UPDATE = 10

    def __init__(self, response, progress_callback=None, content_length=None, enable_crc=False):
        self.response = response
        self.frame_off_set = 0
        self.frame_length = 0
        self.frame_data = b''
        self.check_sum_flag = 0
        self.file_offset = 0
        self.finished = 0
        self.raw_buffer = b''
        self.raw_buffer_offset = 0
        self.callback = progress_callback
        self.frames_since_last_progress_report = 0
        self.content_length = content_length
        self.resp_content_iter = response.iter_bytes()
        self.enable_crc = enable_crc
        self.payload = b''
        self.output_raw_data = response.headers.get("x-oss-select-output-raw", '') == "true"
        self.request_id = response.headers.get("x-oss-request-id", '')
        self.splits = 0
        self.rows = 0
        self.columns = 0

    def read(self):
        if self.finished:
            return b''

        content = b''
        for data in self:
            content += data

        return content

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.output_raw_data == True:
            data = next(self.resp_content_iter)
            if len(data) != 0:
                return data
            else:
                raise StopIteration

        while self.finished == 0:
            if self.frame_off_set < self.frame_length:
                data = self.frame_data[self.frame_off_set: self.frame_length]
                self.frame_length = self.frame_off_set = 0
                return data
            else:
                self.read_next_frame()
                self.frames_since_last_progress_report += 1
                if (self.frames_since_last_progress_report >= SelectResponseAdapter._FRAMES_FOR_PROGRESS_UPDATE and self.callback is not None):
                    self.callback(self.file_offset, self.content_length)
                    self.frames_since_last_progress_report = 0

        raise StopIteration

    def read_raw(self, amt):
        ret = b''
        read_count = 0
        while amt > 0 and self.finished == 0:
            size = len(self.raw_buffer)
            if size == 0:
                self.raw_buffer = next(self.resp_content_iter)
                self.raw_buffer_offset = 0
                size = len(self.raw_buffer)
                if size == 0:
                    break

            if size - self.raw_buffer_offset >= amt:
                data = self.raw_buffer[self.raw_buffer_offset:self.raw_buffer_offset + amt]
                data_size = len(data)
                self.raw_buffer_offset += data_size
                ret += data
                read_count += data_size
                amt -= data_size
            else:
                data = self.raw_buffer[self.raw_buffer_offset:]
                data_len = len(data)
                ret += data
                read_count += data_len
                amt -= data_len
                self.raw_buffer = b''

        return ret

    def change_endianness_if_needed(self, bytes_array):
        if sys.byteorder == 'little':
            bytes_array.reverse()

    def read_next_frame(self):
        frame_type = bytearray(self.read_raw(4))
        payload_length = bytearray(self.read_raw(4))
        self.change_endianness_if_needed(payload_length)  # convert to little endian
        payload_length_val = struct.unpack("I", bytes(payload_length))[0]
        header_checksum = bytearray(self.read_raw(4))

        frame_type[0] = 0  # mask the version bit
        self.change_endianness_if_needed(frame_type)  # convert to little endian
        frame_type_val = struct.unpack("I", bytes(frame_type))[0]
        if (frame_type_val != SelectResponseAdapter._DATA_FRAME_TYPE and
                frame_type_val != SelectResponseAdapter._CONTINIOUS_FRAME_TYPE and
                frame_type_val != SelectResponseAdapter._END_FRAME_TYPE and
                frame_type_val != SelectResponseAdapter._META_END_FRAME_TYPE and
                frame_type_val != SelectResponseAdapter._JSON_META_END_FRAME_TYPE):

            raise Exception(self.request_id, "Unexpected frame type:" + str(frame_type_val))

        self.payload = self.read_raw(payload_length_val)
        file_offset_bytes = bytearray(self.payload[0:8])
        self.change_endianness_if_needed(file_offset_bytes)
        self.file_offset = struct.unpack("Q", bytes(file_offset_bytes))[0]
        if frame_type_val == SelectResponseAdapter._DATA_FRAME_TYPE:
            self.frame_length = payload_length_val - 8
            self.frame_off_set = 0
            self.check_sum_flag = 1
            self.frame_data = self.payload[8:]
            checksum = bytearray(self.read_raw(4))  # read checksum crc32
            self.change_endianness_if_needed(checksum)
            checksum_val = struct.unpack("I", bytes(checksum))[0]
            if self.enable_crc:
                crc32 = Crc32()
                crc32.update(self.payload)
                checksum_calc = crc32.crc
                if checksum_val != checksum_calc:
                    raise Exception(
                        "Incorrect checksum: Actual" + str(checksum_val) + ". Calculated:" + str(checksum_calc),
                        self.request_id)

        elif frame_type_val == SelectResponseAdapter._CONTINIOUS_FRAME_TYPE:
            self.frame_length = self.frame_off_set = 0
            self.check_sum_flag = 1
            self.read_raw(4)
        elif frame_type_val == SelectResponseAdapter._END_FRAME_TYPE:
            self.frame_off_set = 0
            scanned_size_bytes = bytearray(self.payload[8:16])
            status_bytes = bytearray(self.payload[16:20])
            self.change_endianness_if_needed(status_bytes)
            status = struct.unpack("I", bytes(status_bytes))[0]
            error_msg_size = payload_length_val - 20
            error_msg = b''
            error_code = b''
            if error_msg_size > 0:
                error_msg = self.payload[20:error_msg_size + 20]
                error_code_index = error_msg.find(b'.')
                if error_code_index >= 0 and error_code_index < error_msg_size - 1:
                    error_code = error_msg[0:error_code_index]
                    error_msg = error_msg[error_code_index + 1:]

            if status // 100 != 2:
                raise Exception(status, error_code, error_msg)
            self.frame_length = 0
            if self.callback is not None:
                self.callback(self.file_offset, self.content_length)
            self.read_raw(4)  # read the payload checksum
            self.frame_length = 0
            self.finished = 1
        elif frame_type_val == SelectResponseAdapter._META_END_FRAME_TYPE or frame_type_val == SelectResponseAdapter._JSON_META_END_FRAME_TYPE:
            self.frame_off_set = 0
            scanned_size_bytes = bytearray(self.payload[8:16])
            status_bytes = bytearray(self.payload[16:20])
            self.change_endianness_if_needed(status_bytes)
            status = struct.unpack("I", bytes(status_bytes))[0]
            splits_bytes = bytearray(self.payload[20:24])
            self.change_endianness_if_needed(splits_bytes)
            self.splits = struct.unpack("I", bytes(splits_bytes))[0]
            lines_bytes = bytearray(self.payload[24:32])
            self.change_endianness_if_needed(lines_bytes)
            self.rows = struct.unpack("Q", bytes(lines_bytes))[0]

            error_index = 36
            if frame_type_val == SelectResponseAdapter._META_END_FRAME_TYPE:
                column_bytes = bytearray(self.payload[32:36])
                self.change_endianness_if_needed(column_bytes)
                self.columns = struct.unpack("I", bytes(column_bytes))[0]
            else:
                error_index = 32

            error_size = payload_length_val - error_index
            error_msg = b''
            error_code = b''
            if (error_size > 0):
                error_msg = self.payload[error_index:error_index + error_size]
                error_code_index = error_msg.find(b'.')
                if error_code_index >= 0 and error_code_index < error_size - 1:
                    error_code = error_msg[0:error_code_index]
                    error_msg = error_msg[error_code_index + 1:]

            self.read_raw(4)  # read the payload checksum
            self.final_status = status
            self.frame_length = 0
            self.finished = 1
            if (status / 100 != 2):
                raise Exception(status, error_code, error_msg)


class Crc32(object):
    _POLY = 0x104C11DB7
    _XOROUT = 0xFFFFFFFF

    def __init__(self, init_crc=0):
        self.crc32 = crcmod.Crc(self._POLY, initCrc=init_crc, rev=True, xorOut=self._XOROUT)

    def __call__(self, data):
        self.update(data)

    def update(self, data):
        self.crc32.update(data)

    @property
    def crc(self):
        return self.crc32.crcValue