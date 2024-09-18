"""APIs for presign operation."""
# pylint: disable=line-too-long
import datetime
from typing import Union, Optional, MutableMapping
from .types import OperationInput, OperationOutput, HttpClient, HttpRequest, HttpResponse
from . import serde
from . import models
from . import exceptions
from ._client import _SyncClientImpl
from .signer import SignerV4


PresignRequest = Union[
    models.GetObjectRequest,
    models.PutObjectRequest,
    models.HeadObjectRequest,
    models.InitiateMultipartUploadRequest,
    models.UploadPartRequest,
    models.CompleteMultipartUploadRequest,
    models.AbortMultipartUploadRequest
]


class PresignResult:
    """The result for the presign operation."""

    def __init__(
        self,
        method: Optional[str] = None,
        url: Optional[str] = None,
        expiration: Optional[datetime.datetime] = None,
        signed_headers: Optional[MutableMapping] = None,
    ) -> None:
        """
        Args:
            method (str, optional): The HTTP method, which corresponds to the operation.
                For example, the HTTP method of the GetObject operation is GET.
            url (str, optional): The pre-signed URL.
            expiration (datetime.datetime, optional): The time when the pre-signed URL expires.
            signed_headers (MutableMapping, optional): The request headers specified in the request.
                For example, if Content-Type is specified for PutObject, Content-Type is returned.
        """
        self.method = method
        self.url = url
        self.expiration = expiration
        self.signed_headers = signed_headers


class _nopResponse(HttpResponse):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._request = kwargs.pop("request")

    @property
    def request(self) -> HttpRequest:
        return self._request

    @property
    def is_closed(self) -> bool:
        return True

    @property
    def is_stream_consumed(self) -> bool:
        return True

    @property
    def status_code(self) -> int:
        return 200

    @property
    def headers(self):
        return {}

    @property
    def reason(self) -> str:
        return "OK"

    @property
    def content(self) -> bytes:
        return b''

    def __repr__(self) -> str:
        return '_nopResponse'

    def __enter__(self) -> "_nopResponse":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        pass

    def read(self) -> bytes:
        return b''

    def iter_bytes(self, **kwargs):
        """iter bytes"""
        return iter([])


class _nopHttpClient(HttpClient):
    def send(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return _nopResponse(request=request)

    def open(self) -> None:
        pass

    def close(self) -> None:
        pass


_presign_kwargs = {
    'http_client': _nopHttpClient(),
    'auth_method': 'query'
}


def presign_inner(client: _SyncClientImpl, request: PresignRequest, **kwargs) -> PresignResult:
    """
    presign synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PresignRequest): The request for the Presign operation.
        expires (datetime.timedelta, optional): The expiration duration for the generated presign url.
        expiration (datetime.datetime, optional): The expiration time for the generated presign url.

    Returns:
        PresignResult: The result for the Presign operation.
    """

    op_input = _serialize_input(request)

    # expiration
    expires = kwargs.pop("expires", None)
    expiration = kwargs.pop("expiration", None)
    if expiration is not None:
        op_input.op_metadata['expiration_time'] = expiration
    elif expires is not None:
        now = datetime.datetime.now(datetime.timezone.utc)
        op_input.op_metadata['expiration_time'] = now + expires

    op_output = client.invoke_operation(op_input, **_presign_kwargs)

    return _deserialize_output(client, op_output)


def _serialize_input(request: PresignRequest) -> OperationInput:
    op_input = OperationInput(op_name="", method="")
    if isinstance(request, models.GetObjectRequest):
        op_input.op_name = "GetObject"
        op_input.method = "GET"
        op_input.bucket = request.bucket
        op_input.key = request.key

    elif isinstance(request, models.PutObjectRequest):
        op_input.op_name = "PutObject"
        op_input.method = "PUT"
        op_input.bucket = request.bucket
        op_input.key = request.key

    elif isinstance(request, models.HeadObjectRequest):
        op_input.op_name = "HeadObject"
        op_input.method = "HEAD"
        op_input.bucket = request.bucket
        op_input.key = request.key

    elif isinstance(request, models.InitiateMultipartUploadRequest):
        op_input.op_name = "InitiateMultipartUpload"
        op_input.method = "POST"
        op_input.bucket = request.bucket
        op_input.key = request.key
        op_input.parameters = {"uploads": ""}

    elif isinstance(request, models.UploadPartRequest):
        op_input.op_name = "UploadPart"
        op_input.method = "PUT"
        op_input.bucket = request.bucket
        op_input.key = request.key

    elif isinstance(request, models.CompleteMultipartUploadRequest):
        op_input.op_name = "CompleteMultipartUpload"
        op_input.method = "POST"
        op_input.bucket = request.bucket
        op_input.key = request.key

    elif isinstance(request, models.AbortMultipartUploadRequest):
        op_input.op_name = "AbortMultipartUpload"
        op_input.method = "DELETE"
        op_input.bucket = request.bucket
        op_input.key = request.key

    else:
        raise exceptions.ParamInvalidError(field='request')

    return serde.serialize_input(request, op_input)


def _deserialize_output(client: _SyncClientImpl, op_output: OperationOutput) -> PresignResult:
    result = PresignResult()
    result.method = op_output.http_response.request.method
    result.url = op_output.http_response.request.url
    result.expiration = op_output.op_metadata.get('expiration_time', None)
    result.signed_headers = {}

    _options = getattr(client, '_options', None)
    if _options:
        s = getattr(_options, 'signer', None)
        if s:
            for k, v in op_output.http_response.request.headers.items():
                if s.is_signed_header(k):
                    result.signed_headers[k] = v

        if result.expiration is not None and isinstance(s, SignerV4):
            now = datetime.datetime.now(datetime.timezone.utc)
            if (result.expiration - now) > datetime.timedelta(days=7):
                raise exceptions.PresignExpirationError()

    return result
