"""utils for stream wrapper"""
import os
import sys
import errno
import threading
from typing import Optional, IO, List, Iterable, Any, AnyStr, Iterator
from . import utils
from .types import StreamBody, HttpResponse

# pylint: disable=no-member
# pylint: disable=protected-access


class TeeIterator:
    """A Iterator that writes to w what it reads from source
    """

    def __iter__(self):
        return self.iter_bytes()

    def __next__(self):
        d = self.next()
        if self._writers is not None:
            for w in self._writers:
                w.write(d)
        return d

    def seekable(self):
        """_summary_
        """
        return self._seekable

    def reset(self) -> None:
        """_summary_
        """
        if self._writers is not None:
            for w in self._writers:
                if hasattr(self._writers, 'reset'):
                    w.reset()

    @staticmethod
    def from_source(source: Any, writers: List[Any], **kwargs: Any) -> "TeeIterator":
        """Converts source to TeeIterator

        Args:
            source (Any): what it reads from
            writers (List[Any]): what it writes to

        Raises:
            TypeError: If the type of source is is not supported, raises error.

        Returns:
            TeeIterator: A Iterator that writes to w what it reads from source
        """

        block_size = kwargs.get("block_size", 32 * 1024)

        if isinstance(source, str):
            return _TeeIteratorStr(source, writers, block_size)

        if isinstance(source, bytes):
            return _TeeIteratorBytes(source, writers, block_size)

        # file-like object
        if hasattr(source, 'seek') and hasattr(source, 'read'):
            data_len = utils.guess_content_length(source)
            if data_len is not None:
                return _TeeIteratorIOLen(source, data_len, writers, block_size)
            return _TeeIteratorIO(source, writers, block_size)

        if isinstance(source, Iterable):
            return _TeeIteratorIter(source, writers)

        raise TypeError(
            f'Invalid type for body. Expected str, bytes, file-like object, got {type(source)}')


class _TeeIteratorStr(TeeIterator):
    """_summary_
    """

    def __init__(
        self,
        data: str,
        writers: List[Any],
        block_size: Optional[int] = None
    ) -> None:
        self._data = data
        self._writers = writers
        self._block_size = block_size
        self._offset = 0
        self._total = 0
        self._seekable = True
        self._content = None

    def __len__(self):
        return len(self._data)

    def iter_bytes(self):
        """_summary_
        """
        self._content = self._data.encode()
        self._total = len(self._content)
        self._offset = 0
        return self

    def next(self):
        """_summary_
        """
        if self._offset >= self._total:
            raise StopIteration

        remains = self._total - self._offset
        remains = min(self._block_size, remains)

        ret = self._content[self._offset: self._offset + remains]
        self._offset += remains

        return ret


class _TeeIteratorBytes(TeeIterator):
    """_summary_
    """

    def __init__(
        self,
        data: bytes,
        writers: List[Any],
        block_size: Optional[int] = None
    ) -> None:
        self._data = data
        self._writers = writers
        self._block_size = block_size
        self._offset = 0
        self._total = 0
        self._seekable = True
        self._content = None

    def __len__(self):
        return len(self._data)

    def iter_bytes(self):
        """_summary_
        """
        self._content = self._data
        self._total = len(self._content)
        self._offset = 0
        return self

    def next(self):
        """_summary_
        """
        if self._offset >= self._total:
            raise StopIteration

        remains = self._total - self._offset
        remains = min(self._block_size, remains)

        ret = self._content[self._offset: self._offset + remains]
        self._offset += remains

        return ret

class _TeeIteratorIOLen(TeeIterator):
    """_summary_
    """

    def __init__(
        self,
        data: IO,
        total: int,
        writers: List[Any],
        block_size: Optional[int] = None
    ) -> None:
        self._data = data
        self._total = total
        self._writers = writers
        self._block_size = block_size
        seekable = is_seekable_io(data)
        self._start_offset = 0 if not seekable else data.seek(0, os.SEEK_CUR)
        self._seekable = seekable

    def __len__(self):
        return self._total

    def iter_bytes(self):
        """_summary_
        """
        if self._seekable:
            self._data.seek(self._start_offset, os.SEEK_SET)

        return self

    def next(self):
        """_summary_
        """
        d = self._data.read(self._block_size)

        if d:
            return d

        raise StopIteration

class _TeeIteratorIO(TeeIterator):
    """_summary_
    """

    def __init__(
        self,
        data: IO,
        writers: List[Any],
        block_size: Optional[int] = None
    ) -> None:
        self._data = data
        self._writers = writers
        self._block_size = block_size

        seekable = is_seekable_io(data)
        self._start_offset = 0 if not seekable else data.seek(0, os.SEEK_CUR)
        self._total = utils.guess_content_length(data)
        self._seekable = seekable

        if self._total is not None:
            setattr(self, '__len__', lambda x: x._total)

    def iter_bytes(self):
        """_summary_
        """
        if self._seekable:
            self._data.seek(self._start_offset, os.SEEK_SET)

        return self

    def next(self):
        """_summary_
        """
        d = self._data.read(self._block_size)

        if d:
            return d

        raise StopIteration


class _TeeIteratorIter(TeeIterator):
    """_summary_
    """

    def __init__(
        self,
        data: Iterable[bytes],
        writers: List[Any],
    ) -> None:
        self._data = data
        self._writers = writers
        self._seekable = True
        self._iter = None

    def iter_bytes(self):
        """_summary_
        """
        self._iter = iter(self._data)
        return self

    def next(self):
        """_summary_
        """
        return next(self._iter)


def is_seekable_io(fileobj):
    """_summary_
    """
    if hasattr(fileobj, 'seekable'):
        return fileobj.seekable()

    if hasattr(fileobj, 'seek') and hasattr(fileobj, 'tell'):
        try:
            fileobj.seek(0, os.SEEK_CUR)
            return True
        except OSError:
            return False

    return False


if sys.platform.startswith('win'):
    def rename_file(current_filename, new_filename):
        try:
            os.remove(new_filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
        os.rename(current_filename, new_filename)
else:
    rename_file = os.rename


class ReadAtReader:
    """A IO that implements read_at
    """
    def __init__(
        self,
        reader: IO[bytes],
    ) -> None:
        self._reader = reader
        self._readat_lock = threading.Lock()

    @property
    def mode(self) -> str:
        """_summary_
        """
        return self._reader.mode

    @property
    def name(self) -> str:
        """_summary_
        """
        return f'{self._reader.name} with read_at'

    def close(self) -> None:
        """_summary_
        """
        self._reader.close()

    @property
    def closed(self) -> bool:
        """_summary_
        """
        return self._reader.closed

    def fileno(self) -> int:
        """_summary_
        """
        return self._reader.fileno()

    def flush(self) -> None:
        """_summary_
        """
        self._reader.flush()

    def isatty(self) -> bool:
        """_summary_
        """
        return self._reader.isatty()

    def read(self, n: int = -1) -> AnyStr:
        """_summary_
        """
        return self._reader.read(n)

    def read_at(self, off: int, n: int = -1) -> AnyStr:
        """_summary_
        """
        with self._readat_lock:
            self._reader.seek(off)
            return self._reader.read(n)

    def readable(self) -> bool:
        """_summary_
        """
        return self._reader.readable()

    def readline(self, limit: int = -1) -> AnyStr:
        """_summary_
        """
        return self._reader.readline(limit)

    def readlines(self, hint: int = -1) -> List[AnyStr]:
        """_summary_
        """
        return self._reader.readlines(hint)

    def seek(self, offset: int, whence: int = 0) -> int:
        """_summary_
        """
        return self._reader.seek(offset, whence)

    def seekable(self) -> bool:
        """_summary_
        """
        return self._reader.seekable()

    def tell(self) -> int:
        """_summary_
        """
        return self._reader.tell()

    def __enter__(self) -> 'IO[AnyStr]':
        self._reader.__enter__()
        return self

    def __exit__(self, type_, value, traceback) -> None:
        self._reader.__exit__(type_, value, traceback)

class SectionReader:
    """
    A SectionReader that reads from r starting at offset off and stops with EOF after n bytes
    """
    def __init__(
        self,
        reader: ReadAtReader,
        off: int,
        n: int,
    ) -> None:
        self._reader = reader
        if off <= sys.maxsize-n:
            remaining = n + off
        else:
            remaining = sys.maxsize
        self._base = off
        self._off = off
        self._limit = remaining

    def read(self, n: int = -1) -> AnyStr:
        """_summary_
        """
        if self._off >= self._limit:
            return b''

        max_size = self._limit - self._off
        if n < 0 or n > max_size:
            n = max_size

        d = self._reader.read_at(self._off, n)
        self._off += len(d)
        return d

    def read_at(self, off: int, n: int = -1) -> AnyStr:
        """_summary_
        """
        if off < 0 or off >= self._limit - self._base:
            return b''

        off += self._base
        max_size = self._limit - off
        if n < 0 or n > max_size:
            n = max_size

        return self._reader.read_at(self._off, n)

    def readable(self) -> bool:
        """_summary_
        """
        return self._reader.readable()

    def seek(self, offset: int, whence: int = 0) -> int:
        """_summary_
        """
        if whence == os.SEEK_SET:
            offset += self._base
        elif whence == os.SEEK_CUR:
            offset += self._off
        elif whence == os.SEEK_END:
            offset += self._limit
        else:
            raise ValueError(f'invalid whence {whence}')

        if offset < self._base:
            raise OSError("seek() returned an invalid position")

        self._off = offset

        return offset - self._base

    def seekable(self) -> bool:
        """_summary_
        """
        return self._reader.seekable()

    def tell(self) -> int:
        """_summary_
        """
        return self._off - self._base

    def __len__(self):
        return self._limit - self._base

class StreamBodyReader(StreamBody):
    """
    A StreamBodyReader that convert HttpResponse type to StreamBody type.
    """
    def __init__(
        self,
        response: HttpResponse,
    ) -> None:
        self._response = response

    def __enter__(self) -> "StreamBodyReader":
        self._response.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self._response.__exit__(*args)

    @property
    def is_closed(self) -> bool:
        return self._response.is_closed

    @property
    def is_stream_consumed(self) -> bool:
        return self._response.is_stream_consumed

    @property
    def content(self) -> bytes:
        if not self._response.is_stream_consumed:
            self._response.read()
        return self._response.content

    def read(self) -> bytes:
        return self._response.read()

    def close(self) -> None:
        self._response.close()

    def iter_bytes(self, **kwargs: Any) -> Iterator[bytes]:
        return self._response.iter_bytes(**kwargs)

class StreamBodyDiscarder(StreamBody):
    """_summary_
    """
    def __init__(
        self,
        stream: StreamBody,
        discard: int
    ) -> None:
        self._stream = stream
        self._discard = discard

    def __enter__(self) -> "StreamBodyDiscarder":
        self._stream.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self._stream.__exit__(*args)

    @property
    def is_closed(self) -> bool:
        return self._stream.is_closed

    @property
    def is_stream_consumed(self) -> bool:
        return self._stream.is_stream_consumed

    @property
    def content(self) -> bytes:
        if not self._stream.is_stream_consumed:
            self._stream.read()
        return self._stream.content[self._discard:]

    def read(self) -> bytes:
        data = self._stream.read()
        return data[self._discard:]

    def close(self) -> None:
        self._stream.close()

    def iter_bytes(self, **kwargs: Any) -> Iterator[bytes]:
        discard = self._discard
        for d in self._stream.iter_bytes(**kwargs):
            if discard > 0:
                if discard > len(d):
                    discard -= len(d)
                else:
                    yield d[discard:]
                    discard = 0
            else:
                yield d


class LimitReader:
    """_summary_
    """
    def __init__(
        self,
        reader: IO[bytes],
        n: int,
    ) -> None:
        self._reader = reader
        self._n = n

    def read(self, n: int = -1) -> AnyStr:
        """_summary_
        """
        if self._n <= 0:
            return b''

        if n < 0 or n > self._n:
            n = self._n

        d = self._reader.read(n)
        self._n -= len(d)
        return d
