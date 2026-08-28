"""utils for stream wrapper"""
import os
from typing import Optional, IO, List, AsyncIterable, Any, AsyncIterator, Awaitable, Callable
from .. import utils
from ..types import AsyncStreamBody, AsyncHttpResponse
from ..exceptions import ResponseNotReadError, StreamConsumedError, StreamClosedError
from ..filelike import _check_object_same

# pylint: disable=no-member
# pylint: disable=protected-access
def is_seekable_io(fileobj):
    """is seekable io
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


class TeeAsyncIterator:
    """A AsyncIterator that writes to w what it reads from source
    """

    def __aiter__(self):
        return self.aiter_bytes()

    async def __anext__(self):
        d = await self.anext()
        if self._writers is not None:
            for w in self._writers:
                w.write(d)
        return d

    def seekable(self):
        """Is there a file pointer offset
        """
        return self._seekable

    def reset(self) -> None:
        """Resets the buffer to the marked position.
        """
        if self._writers is not None:
            for w in self._writers:
                if hasattr(w, 'reset'):
                    w.reset()

    @staticmethod
    def from_source(source: Any, writers: List[Any], **kwargs: Any) -> "TeeAsyncIterator":
        """Converts source to TeeAsyncIterator

        Args:
            source (Any): what it reads from
            writers (List[Any]): what it writes to

        Raises:
            TypeError: If the type of source is is not supported, raises error.

        Returns:
            TeeAsyncIterator: A AsyncIterator that writes to w what it reads from source
        """

        block_size = kwargs.get("block_size", 64 * 1024)

        if isinstance(source, str):
            return _TeeAsyncIteratorStr(source, writers, block_size)

        if isinstance(source, bytes):
            return _TeeAsyncIteratorBytes(source, writers, block_size)

        # file-like object
        if hasattr(source, 'seek') and hasattr(source, 'read'):
            data_len = utils.guess_content_length(source)
            if data_len is not None:
                return _TeeAsyncIteratorIOLen(source, data_len, writers, block_size)
            return _TeeAsyncIteratorIO(source, writers, block_size)

        if isinstance(source, AsyncIterable):
            return _TeeAsyncIteratorIter(source, writers)

        raise TypeError(
            f'Invalid type for body. Expected str, bytes, file-like object, got {type(source)}')


class _TeeAsyncIteratorStr(TeeAsyncIterator):
    """Iterator str information
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

    def aiter_bytes(self):
        """iter bytes
        """
        self._content = self._data.encode()
        self._total = len(self._content)
        self._offset = 0
        return self

    async def anext(self):
        """Next data
        """
        if self._offset >= self._total:
            raise StopAsyncIteration

        remains = self._total - self._offset
        remains = min(self._block_size, remains)

        ret = self._content[self._offset: self._offset + remains]
        self._offset += remains

        return ret


class _TeeAsyncIteratorBytes(TeeAsyncIterator):
    """Iterator bytes information
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

    def aiter_bytes(self):
        """iter bytes
        """
        self._content = self._data
        self._total = len(self._content)
        self._offset = 0
        return self

    async def anext(self):
        """Next data
        """
        if self._offset >= self._total:
            raise StopAsyncIteration

        remains = self._total - self._offset
        remains = min(self._block_size, remains)

        ret = self._content[self._offset: self._offset + remains]
        self._offset += remains

        return ret

class _TeeAsyncIteratorIOLen(TeeAsyncIterator):
    """Iterator io len information
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
        self._check_type_done = False
        self._do_cast = False

    def __len__(self):
        return self._total

    def aiter_bytes(self):
        """iter bytes
        """
        if self._seekable:
            self._data.seek(self._start_offset, os.SEEK_SET)

        return self

    async def anext(self):
        """Next data
        """
        d = self._data.read(self._block_size)

        if d:
            if not self._check_type_done:
                self._check_type_done = True
                if isinstance(d, str):
                    self._do_cast = True

            if self._do_cast:
                return d.encode()
            else:
                return d

        raise StopAsyncIteration

class _TeeAsyncIteratorIO(TeeAsyncIterator):
    """Iterator io information
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
        self._check_type_done = False
        self._do_cast = False

        if self._total is not None:
            setattr(self, '__len__', lambda x: x._total)

    def aiter_bytes(self):
        """iter bytes
        """
        if self._seekable:
            self._data.seek(self._start_offset, os.SEEK_SET)

        return self

    async def anext(self):
        """Next data
        """
        d = self._data.read(self._block_size)

        if d:
            if not self._check_type_done:
                self._check_type_done = True
                if isinstance(d, str):
                    self._do_cast = True

            if self._do_cast:
                return d.encode()
            else:
                return d

        raise StopAsyncIteration

class _TeeAsyncIteratorIter(TeeAsyncIterator):
    """Iterator iter information
    """

    def __init__(
        self,
        data: AsyncIterable[bytes],
        writers: List[Any],
    ) -> None:
        self._data = data
        self._writers = writers
        self._iter = None
        self._seekable = not isinstance(self._data, AsyncIterator)
        self._check_type_done = False
        self._cast_func = None

    def aiter_bytes(self):
        """iter bytes
        """
        if isinstance(self._data, AsyncIterator):
            self._iter = self._data
        else:
            self._iter = iter(self._data)
        return self

    async def anext(self):
        """Next data
        """
        return self._to_bytes(await self._iter.__anext__())

    def _to_bytes(self, d) -> bytes:
        if  d is None:
            return d
        if not self._check_type_done:
            self._check_type_done = True
            if isinstance(d, str):
                self._cast_func = lambda x: x.encode()

        if self._cast_func:
            return self._cast_func(d)

        return d

class AsyncStreamBodyReader(AsyncStreamBody):
    """
    A StreamBodyReader that convert AsyncHttpResponse type to AsyncStreamBody type.
    """
    def __init__(
        self,
        response: AsyncHttpResponse,
    ) -> None:
        self._response = response

    async def __aenter__(self) -> "AsyncStreamBodyReader":
        await self._response.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._response.__aexit__(*args)

    @property
    def is_closed(self) -> bool:
        return self._response.is_closed

    @property
    def is_stream_consumed(self) -> bool:
        return self._response.is_stream_consumed

    @property
    def content(self) -> bytes:
        if not self._response.is_stream_consumed:
            raise ResponseNotReadError()
        return self._response.content

    async def read(self) -> bytes:
        return await self._response.read()

    async def close(self) -> None:
        await self._response.close()

    async def iter_bytes(self, **kwargs: Any) -> AsyncIterator[bytes]:
        return self._response.iter_bytes(**kwargs)


class AsyncResumableStreamBodyReader(AsyncStreamBody):
    """
    A AsyncStreamBody that streams the object's data and transparently resumes
    from the last consumed offset with a ranged GET when the connection breaks.
    """

    def __init__(
        self,
        result: Any,
        resume_fn: Callable[[int, Optional[int]], Awaitable[Any]],
    ) -> None:
        self._resume_fn = resume_fn
        self._body: Optional[AsyncStreamBody] = result.body
        self._iter: Optional[AsyncIterator[bytes]] = None
        self._iter_kwargs: dict = {}
        self._src_etag = result.etag
        self._src_modtime = result.last_modified
        self._start = 0
        self._end = None
        if (crange := (result.headers or {}).get('Content-Range', None)):
            self._start, self._end, _ = utils.parse_content_range(crange)
        self._expected = result.content_length
        self._consumed = 0
        self._content: Optional[bytes] = None
        self._closed = False
        self._stream_consumed = False

    async def __aenter__(self) -> "AsyncResumableStreamBodyReader":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    @property
    def is_closed(self) -> bool:
        return self._closed

    @property
    def is_stream_consumed(self) -> bool:
        return self._stream_consumed

    @property
    def content(self) -> bytes:
        if self._content is None:
            raise ResponseNotReadError()
        return self._content

    async def read(self) -> bytes:
        if self._content is None:
            chunks = []
            async for chunk in await self.iter_bytes():
                chunks.append(chunk)
            self._content = b''.join(chunks)
        return self._content

    async def close(self) -> None:
        self._closed = True
        await self._drop_stream()

    async def iter_bytes(self, **kwargs: Any) -> AsyncIterator[bytes]:
        if self._stream_consumed:
            raise StreamConsumedError()
        if self._closed:
            raise StreamClosedError()
        self._iter_kwargs = kwargs
        return self._iter_bytes()

    async def _iter_bytes(self) -> AsyncIterator[bytes]:
        while True:
            if self._iter is None:
                # not guarded: a permanent failure must propagate instead of looping forever
                await self._open_stream()

            try:
                chunk = await self._iter.__anext__()
            except StopAsyncIteration:
                if self._expected is not None and self._consumed < self._expected:
                    await self._drop_stream()
                    continue
                self._stream_consumed = True
                return
            except Exception:  # pylint: disable=broad-except
                await self._drop_stream()
                continue

            self._consumed += len(chunk)
            yield chunk

    async def _open_stream(self) -> None:
        if self._body is None:
            offset = self._start + self._consumed
            result = await self._resume_fn(offset, self._end)
            if (err := _check_object_same(self._src_modtime, self._src_etag, offset, result)):
                await result.body.close()
                raise err
            self._body = result.body

        self._iter = await self._body.iter_bytes(**self._iter_kwargs)

    async def _drop_stream(self) -> None:
        if self._body is not None:
            await self._body.close()
        self._body = None
        self._iter = None
