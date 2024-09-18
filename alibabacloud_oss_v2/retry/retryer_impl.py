"""Modules for retryer """
from typing import Optional, List
from ..types import Retryer
from .. import defaults
from . import error_retryable
from . import backoff

_default_error_retryables = [
    error_retryable.HTTPStatusCodeRetryable(),
    error_retryable.ServiceErrorCodeRetryable(),
    error_retryable.ClientErrorRetryable()
]


class NopRetryer(Retryer):
    """nop retryer"""

    def is_error_retryable(self, error: Exception) -> bool:
        return False

    def max_attempts(self) -> int:
        return 1

    def retry_delay(self, attempt: int, error: Exception) -> float:
        raise NotImplementedError()


class StandardRetryer(Retryer):
    """standard retryer"""

    def __init__(
        self,
        max_attempts: Optional[int] = None,
        max_backoff: Optional[float] = None,
        base_delay: Optional[float] = None,
        error_retryables: Optional[List[error_retryable.ErrorRetryable]] = None,
        backoff_delayer: Optional[backoff.BackoffDelayer] = None,
    ) -> None:
        """
        Args:
            max_attempts (int, optional): max retry attempt
            max_backoff (float, optional): the max duration in second.
            base_delay (float, optional): the base delay duration in second.
            error_retryables ([ErrorRetryable], optional): error retryables list.
            backoff_delayer ([BackoffDelayer], optional): backoff delayer.
        """
        super().__init__()
        self._max_attempts = max_attempts or defaults.DEFAULT_MAX_ATTEMPTS
        self._max_backoff = max_backoff or defaults.DEFAULT_MAX_BACKOFF_S
        self._base_delay = base_delay or defaults.DEFAULT_BASE_DELAY_S
        self._error_retryables = error_retryables or _default_error_retryables
        if backoff_delayer is None:
            backoff_delayer = backoff.FullJitterBackoff(
                self._base_delay, self._max_backoff)
        self._backoff_delayer = backoff_delayer

    def is_error_retryable(self, error: Exception) -> bool:
        for r in self._error_retryables:
            if r.is_error_retryable(error):
                return True
        return False

    def max_attempts(self) -> int:
        return self._max_attempts

    def retry_delay(self, attempt: int, error: Exception) -> float:
        return self._backoff_delayer.backoff_delay(attempt, error)
