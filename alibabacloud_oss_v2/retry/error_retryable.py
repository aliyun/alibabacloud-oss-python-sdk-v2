"""Modules for error retryable """

import abc
from .. import exceptions


class ErrorRetryable(abc.ABC):
    """Abstract base class for backoff delayer."""

    @abc.abstractmethod
    def is_error_retryable(self, error: Exception) -> bool:
        """Check whether the error is retryable.

        Args:
            error (Exception): the error meets

        Returns:
            bool: True if the error is retryable.
        """


class HTTPStatusCodeRetryable(ErrorRetryable):
    """HTTPStatusCodeRetryable implements http status checker"""

    def __init__(self) -> None:
        # 401(Unauthorized) 408(Request Timeout) 429(Rate exceeded)
        self._status_code = set([401, 408, 429])

    def is_error_retryable(self, error: Exception) -> bool:
        """Check whether the error is retryable.

        Args:
            error (Exception): the error meets

        Returns:
            bool: True if the error is retryable.
        """
        if isinstance(error, exceptions.ServiceError):
            if error.status_code >= 500:
                return True
            if error.status_code in self._status_code:
                return True
        return False

    def __repr__(self) -> str:
        return "<HTTPStatusCodeRetryable>"


class ServiceErrorCodeRetryable(ErrorRetryable):
    """ServiceErrorCodeRetryable implements service's error code checker"""

    def __init__(self) -> None:
        self._error_codes = set(["RequestTimeTooSkewed", "BadRequest"])

    def is_error_retryable(self, error: Exception) -> bool:
        """Check whether the error is retryable.

        Args:
            error (Exception): the error meets

        Returns:
            bool: True if the error is retryable.
        """
        if isinstance(error, exceptions.ServiceError):
            if error.code in self._error_codes:
                return True
        return False

    def __repr__(self) -> str:
        return "<ServiceErrorCodeRetryable>"

class ClientErrorRetryable(ErrorRetryable):
    """ClientErrorRetryable implements client's error checker"""

    def __init__(self) -> None:
        self._exceptions = set([
            exceptions.RequestError,
            exceptions.ResponseError,
            exceptions.InconsistentError,
            exceptions.CredentialsFetchError
        ])


    def is_error_retryable(self, error: Exception) -> bool:
        """Check whether the error is retryable.

        Args:
            error (Exception): the error meets

        Returns:
            bool: True if the error is retryable.
        """
        for e in self._exceptions:
            if isinstance(error, e):
                return True
        return False

    def __repr__(self) -> str:
        return "<ClientErrorRetryable>"
