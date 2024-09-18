"""Modules for backoff """

import abc
import sys
import random
from math import log2

class BackoffDelayer(abc.ABC):
    """Abstract base class for backoff delayer."""

    @abc.abstractmethod
    def backoff_delay(self, attempt: int, error: Exception) -> float:
        """Returns the delay that should be used before retrying the attempt.

        Args:
            attempt (int): current retry attempt
            error (Exception): the error meets

        Returns:
            float: delay duration in second.
        """

class FixedDelayBackoff(BackoffDelayer):
    """FixedDelayBackoff implements fixed backoff."""

    def __init__(self, backoff:float) -> None:
        """
        Args:
            backoff (float): the delay duration in second
        """
        self._backoff = backoff

    def backoff_delay(self, attempt: int, error: Exception) -> float:
        """Returns the delay that should be used before retrying the attempt.

        Args:
            attempt (int): current retry attempt
            error (Exception): the error meets

        Returns:
            float: delay duration in second.
        """
        return self._backoff

    def __repr__(self) -> str:
        return f"<FixedDelayBackoff, backoff: '{self._backoff}'>"


class FullJitterBackoff(BackoffDelayer):
    """FullJitterBackoff implements capped exponential backoff with jitter.
       [0.0, 1.0) * min(2 ^ attempts * baseDealy, maxBackoff)
    """

    def __init__(self, base_delay:float, max_backoff:float) -> None:
        """
        Args:
            base_delay (float): the base delay duration in second
            max_backoff (float): the max duration in second
        """
        self._base_delay = base_delay
        self._max_backoff = max_backoff
        self._attempt_celling = int(log2(float(sys.maxsize) / base_delay))

    def backoff_delay(self, attempt: int, error: Exception) -> float:
        """Returns the delay that should be used before retrying the attempt.

        Args:
            attempt (int): current retry attempt
            error (Exception): the error meets

        Returns:
            float: delay duration in second.
        """
        attempt = min(attempt, self._attempt_celling)
        delay = min((self._base_delay * (1 << attempt)), self._max_backoff)
        rand = random.uniform(0, 1)
        return rand * delay

    def __repr__(self) -> str:
        return f"<FullJitterBackoff, base delay: '{self._base_delay}', max backoff: '{self._max_backoff}'>"


class EqualJitterBackoff(BackoffDelayer):
    """EqualJJitterBackoff implements equal jitter backoff.
       ceil = min(2 ^ attempts * baseDealy, maxBackoff)
       ceil/2 + [0.0, 1.0) *(ceil/2 + 1)
    """

    def __init__(self, base_delay:float, max_backoff:float) -> None:
        """
        Args:
            base_delay (float): the base delay duration in second
            max_backoff (float): the max duration in second
        """
        self._base_delay = base_delay
        self._max_backoff = max_backoff
        self._attempt_celling = int(log2(float(sys.maxsize) / base_delay))

    def backoff_delay(self, attempt: int, error: Exception) -> float:
        """Returns the delay that should be used before retrying the attempt.

        Args:
            attempt (int): current retry attempt
            error (Exception): the error meets

        Returns:
            float: delay duration in second.
        """
        attempt = min(attempt, self._attempt_celling)
        delay = min((self._base_delay * (1 << attempt)), self._max_backoff)
        half = delay/2
        rand = random.uniform(0, 1)
        return half + rand * (half + 1)

    def __repr__(self) -> str:
        return f"<EqualJitterBackoff, base delay: '{self._base_delay}', max backoff: '{self._max_backoff}'>"
