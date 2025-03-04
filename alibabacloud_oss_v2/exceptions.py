"""exception information
"""


def _exception_from_packed_args(exception_cls, args=None, kwargs=None):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    return exception_cls(*args, **kwargs)


class BaseError(Exception):
    """
    The base exception class for oss sdk exceptions.

    :ivar msg: The descriptive message associated with the error.
    """

    fmt = 'An unspecified error occurred'

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs

    def __reduce__(self):
        return _exception_from_packed_args, (self.__class__, None, self.kwargs)


class CredentialsBaseError(BaseError):
    """
    The base exception class for oss sdk exceptions.
    """


class CredentialsEmptyError(CredentialsBaseError):
    """
    The access key or access key secret associated with a credentials is not exist.
    """

    fmt = 'Credentials is null or empty'


class CredentialsFetchError(CredentialsBaseError):
    """
    Fetch Credentials error.
    """
    fmt = 'Fetch Credentials raised an exception: {error}'


class StreamConsumedError(BaseError):
    """
    Stream Consumed Error.
    """
    fmt = 'You have likely already consumed this stream, so it can not be accessed anymore.'


class StreamClosedError(BaseError):
    """
    Stream Closed Error.
    """
    fmt = 'The content for response can no longer be read or streamed.'


class ResponseNotReadError(BaseError):
    """
    Response Not ReadError.
    """
    fmt = 'You have not read in the bytes for the response. Call .read() on the response first.'


class RequestError(BaseError):
    """An error occurred while attempt to make a request to the service.
    No request was sent.
    """
    fmt = 'request error: {error}.'

    def __init__(self, **kwargs):
        BaseError.__init__(self, **kwargs)
        self._error = kwargs.get("error", None)

    def unwrap(self) -> Exception:
        """returns the detail error"""
        return self._error


class ResponseError(BaseError):
    """The request was sent, but the client failed to understand the response.
    The connection may have timed out. These errors can be retried for idempotent or safe operations
    """
    fmt = 'response error: {error}.'

    def __init__(self, **kwargs):
        BaseError.__init__(self, **kwargs)
        self._error = kwargs.get("error", None)

    def unwrap(self) -> Exception:
        """returns the detail error"""
        return self._error

class ServiceError(BaseError):
    """
    The exception class for error from oss service.
    """
    fmt = 'Error returned by Service.\n\
        Http Status Code: {status_code}.\n\
        Error Code: {code}.\n\
        Request Id: {request_id}.\n\
        Message: {message}.\n\
        EC: {ec}.\n\
        Timestamp: {timestamp}.\n\
        Request Endpoint: {request_target}.'

    def __init__(self, **kwargs):
        BaseError.__init__(self, **kwargs)
        self.status_code = kwargs.get("status_code", 0)
        self.code = kwargs.get("code", None)
        self.message = kwargs.get("message", None)
        self.request_id = kwargs.get("request_id", None)
        self.ec = kwargs.get("ec", None)
        self.timestamp = kwargs.get("timestamp", None)
        self.request_target = kwargs.get("request_target", None)
        self.snapshot = kwargs.get("snapshot", None)
        self.headers = kwargs.get("headers", None)
        self.error_fileds = kwargs.get("error_fileds", None)


class ParamInvalidError(BaseError):
    """
    Param Invalid Error.
    """
    fmt = 'invalid field, {field}.'


class ParamNullError(BaseError):
    """
    Param Null Error.
    """
    fmt = 'null field, {field}.'


class ParamNullOrEmptyError(BaseError):
    """
    Param Null or Empty Error.
    """
    fmt = 'null or empty field, {field}.'


class ParamRequiredError(BaseError):
    """
    Param Required Error.
    """
    fmt = 'missing required field, {field}.'


class OperationError(BaseError):
    """
    Operation Error.
    """
    fmt = 'operation error {name}: {error}.'

    def __init__(self, **kwargs):
        BaseError.__init__(self, **kwargs)
        self._error = kwargs.get("error", None)

    def unwrap(self) -> Exception:
        """returns the detail error"""
        return self._error


class MD5UnavailableError(BaseError):
    """
    MD5 Unavailable Error.
    """
    fmt = "This system does not support MD5 generation."


class SerializationError(BaseError):
    """Raised if an error is encountered during serialization."""
    fmt = 'Serialization raised an exception: {error}'


class DeserializationError(BaseError):
    """Raised if an error is encountered during deserialization."""
    fmt = 'Deserialization raised an exception: {error}'


class BucketNameInvalidError(BaseError):
    """
    Param Invalid Error.
    """
    fmt = 'Bucket name is invalid, got {name}.'


class ObjectNameInvalidError(BaseError):
    """
    Param Invalid Error.
    """
    fmt = 'Object name is invalid.'


class InconsistentError(BaseError):
    """
    crc check Error.
    """
    fmt = 'crc is inconsistent, client {client_crc}, server {server_crc}'

class PresignExpirationError(BaseError):
    """
    Presign Expiration Error.
    """
    fmt = 'expires should be not greater than 604800(seven days)'

class FileNotExist(BaseError):
    """
    File not exists.
    """
    fmt = 'File not exists, {filepath}'

class FileNotReadable(BaseError):
    """
    File is not readable.
    """
    fmt = 'File is not readable, {filepath}'
