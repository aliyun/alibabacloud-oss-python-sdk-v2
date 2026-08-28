# pylint: skip-file
import unittest
from alibabacloud_oss_v2.aio.aio_utils import AsyncStreamBodyReader, AsyncResumableStreamBodyReader
from alibabacloud_oss_v2.exceptions import ResponseNotReadError, StreamConsumedError, StreamClosedError
from alibabacloud_oss_v2.types import AsyncStreamBody
from .. import MockAsyncHttpResponse


class TestAsyncStreamBodyReader(unittest.IsolatedAsyncioTestCase):
    async def test_async_context_manager(self):
        response = MockAsyncHttpResponse(
            status_code=200,
            body=b'hello world',
        )
        async with AsyncStreamBodyReader(response) as reader:
            self.assertFalse(reader.is_closed)
            self.assertEqual(b'hello world', await reader.read())

        self.assertTrue(reader.is_closed)
        self.assertTrue(response.is_closed)

    async def test_read(self):
        reader = AsyncStreamBodyReader(MockAsyncHttpResponse(
            status_code=200,
            body=b'hello world',
        ))

        try:
            _ = reader.content
            self.fail('should not here')
        except ResponseNotReadError:
            pass

        self.assertEqual(b'hello world', await reader.read())
        self.assertTrue(reader.is_stream_consumed)
        self.assertEqual(b'hello world', reader.content)

        await reader.close()
        self.assertTrue(reader.is_closed)


class ChunkedBody(AsyncStreamBody):
    """Yields data in fixed-size blocks, optionally raising after N blocks."""

    def __init__(self, data: bytes, block_size: int = 4, fail_after: int = None) -> None:
        self._data = data
        self._block_size = block_size
        self._fail_after = fail_after
        self._closed = False

    async def __aenter__(self) -> "ChunkedBody":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    @property
    def is_closed(self) -> bool:
        return self._closed

    @property
    def is_stream_consumed(self) -> bool:
        return False

    @property
    def content(self) -> bytes:
        raise ResponseNotReadError()

    async def read(self) -> bytes:
        return self._data

    async def close(self) -> None:
        self._closed = True

    async def iter_bytes(self, **kwargs):
        return self._iter_bytes()

    async def _iter_bytes(self):
        sent = 0
        for i in range(0, len(self._data), self._block_size):
            if self._fail_after is not None and sent == self._fail_after:
                raise OSError('connection reset by peer')
            yield self._data[i: i + self._block_size]
            sent += 1


class FakeResult:
    def __init__(self, body, content_length=None, content_range=None, etag=None, last_modified=None) -> None:
        self.body = body
        self.content_length = content_length
        self.etag = etag
        self.last_modified = last_modified
        self.headers = {}
        if content_range is not None:
            self.headers['Content-Range'] = content_range


DATA = b'0123456789abcdef'
ETAG = '"D41D8CD98F00B204E9800998ECF8****"'
MODTIME = 'Fri, 13 Nov 2023 14:47:53 GMT'


class TestAsyncResumableStreamBodyReader(unittest.IsolatedAsyncioTestCase):
    def _reader(self, first_body, resumes):
        """Builds a reader whose n-th resume serves resumes[n]."""
        self.resume_calls = []
        first = FakeResult(first_body, content_length=len(DATA), etag=ETAG, last_modified=MODTIME)

        async def resume_fn(offset, end):
            self.resume_calls.append((offset, end))
            body, etag = resumes.pop(0)
            return FakeResult(
                body,
                content_length=len(DATA) - offset,
                content_range=f'bytes {offset}-{len(DATA) - 1}/{len(DATA)}',
                etag=etag,
                last_modified=MODTIME,
            )

        return AsyncResumableStreamBodyReader(first, resume_fn)

    async def test_iter_bytes_no_resume(self):
        reader = self._reader(ChunkedBody(DATA), [])

        got = b''
        async for chunk in await reader.iter_bytes():
            got += chunk

        self.assertEqual(DATA, got)
        self.assertEqual([], self.resume_calls)
        self.assertTrue(reader.is_stream_consumed)

    async def test_iter_bytes_resumes_on_error(self):
        reader = self._reader(
            ChunkedBody(DATA, fail_after=1),
            [(ChunkedBody(DATA[4:]), ETAG)],
        )

        got = b''
        async for chunk in await reader.iter_bytes():
            got += chunk

        self.assertEqual(DATA, got)
        self.assertEqual([(4, None)], self.resume_calls)

    async def test_iter_bytes_resumes_repeatedly(self):
        reader = self._reader(
            ChunkedBody(DATA, fail_after=1),
            [
                (ChunkedBody(DATA[4:], fail_after=1), ETAG),
                (ChunkedBody(DATA[8:]), ETAG),
            ],
        )

        got = b''
        async for chunk in await reader.iter_bytes():
            got += chunk

        self.assertEqual(DATA, got)
        self.assertEqual([(4, None), (8, None)], self.resume_calls)

    async def test_iter_bytes_resumes_on_truncated_stream(self):
        # clean EOF at 8 bytes while Content-Length promised 16
        reader = self._reader(
            ChunkedBody(DATA[:8]),
            [(ChunkedBody(DATA[8:]), ETAG)],
        )

        got = b''
        async for chunk in await reader.iter_bytes():
            got += chunk

        self.assertEqual(DATA, got)
        self.assertEqual([(8, None)], self.resume_calls)

    async def test_iter_bytes_resume_within_range(self):
        first = FakeResult(
            ChunkedBody(DATA[4:12], fail_after=1),
            content_length=8,
            content_range=f'bytes 4-11/{len(DATA)}',
            etag=ETAG,
            last_modified=MODTIME,
        )
        calls = []

        async def resume_fn(offset, end):
            calls.append((offset, end))
            return FakeResult(
                ChunkedBody(DATA[8:12]),
                content_length=4,
                content_range=f'bytes {offset}-11/{len(DATA)}',
                etag=ETAG,
                last_modified=MODTIME,
            )

        reader = AsyncResumableStreamBodyReader(first, resume_fn)

        got = b''
        async for chunk in await reader.iter_bytes():
            got += chunk

        self.assertEqual(DATA[4:12], got)
        self.assertEqual([(8, 11)], calls)

    async def test_iter_bytes_object_changed(self):
        reader = self._reader(
            ChunkedBody(DATA, fail_after=1),
            [(ChunkedBody(DATA[4:]), '"CHANGED98F00B204E9800998ECF8****"')],
        )

        try:
            async for _ in await reader.iter_bytes():
                pass
            self.fail('should not here')
        except ValueError as err:
            self.assertIn('Source file is changed', str(err))

    async def test_read_then_content(self):
        reader = self._reader(
            ChunkedBody(DATA, fail_after=2),
            [(ChunkedBody(DATA[8:]), ETAG)],
        )

        try:
            _ = reader.content
            self.fail('should not here')
        except ResponseNotReadError:
            pass

        self.assertEqual(DATA, await reader.read())
        self.assertEqual(DATA, reader.content)
        self.assertEqual(DATA, await reader.read())

    async def test_iter_bytes_twice(self):
        reader = self._reader(ChunkedBody(DATA), [])

        async for _ in await reader.iter_bytes():
            pass

        try:
            await reader.iter_bytes()
            self.fail('should not here')
        except StreamConsumedError:
            pass

    async def test_close(self):
        body = ChunkedBody(DATA)
        reader = self._reader(body, [])

        async with reader:
            pass

        self.assertTrue(reader.is_closed)
        self.assertTrue(body.is_closed)

        try:
            await reader.iter_bytes()
            self.fail('should not here')
        except StreamClosedError:
            pass


if __name__ == '__main__':
    unittest.main()
