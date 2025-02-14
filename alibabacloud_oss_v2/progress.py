"""Progress for upload, download and copy"""
from typing import Optional


class Progress:
    """Progress
    """

    def __init__(
        self,
        progress_fn,
        total: Optional[int],
    ) -> None:
        self._progress_fn = progress_fn
        self._total = total or -1
        self._written = 0
        self._lwritten = 0

    def reset(self):
        """reset
        """
        self._lwritten = self._written
        self._written = 0

    def write(self, s: bytes):
        """write
        """
        n = _len(s)
        self._written = self._written + n

        if self._progress_fn is None or self._written < self._lwritten:
            return

        self._progress_fn(n, self._written, self._total)


def _len(s):
    if isinstance(s, int):
        return 1
    return len(s)
