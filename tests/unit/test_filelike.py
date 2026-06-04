# pylint: skip-file
"""Unit tests for alibabacloud_oss_v2.filelike (AppendOnlyFile, ReadOnlyFile)."""
import unittest

from alibabacloud_oss_v2 import models, exceptions
from alibabacloud_oss_v2.filelike import (
    AppendOnlyFile, AppendFileAPIClient,
    ReadOnlyFile, OpenFileAPIClient,
    PathError,
)


def _make_result(cls, **kwargs):
    obj = cls(**kwargs)
    obj.status = 'OK'
    obj.status_code = 200
    obj.request_id = 'mock-request-id'
    obj.headers = kwargs.get('headers', {})
    return obj


# ==============================================================================
# Mock clients for AppendOnlyFile
# ==============================================================================

class _MockAppendClient(AppendFileAPIClient):
    """Mock client for AppendOnlyFile tests."""

    def __init__(self, object_exists=False, object_size=0, object_type='Appendable'):
        self._object_exists = object_exists
        self._object_size = object_size
        self._object_type = object_type
        self._current_size = object_size

        self.head_calls = 0
        self.append_calls = 0

    def head_object(self, request, **kwargs):
        self.head_calls += 1
        if not self._object_exists:
            # Simulate 404
            serr = exceptions.ServiceError(
                status_code=404,
                code='NoSuchKey',
                message='not found',
                request_id='req-id',
                ec='',
                timestamp='',
                request_target='',
            )
            raise exceptions.OperationError(name='HeadObject', error=serr)
        return _make_result(
            models.HeadObjectResult,
            content_length=self._current_size,
            object_type=self._object_type,
            hash_crc64='111',
            headers={},
        )

    def append_object(self, request, **kwargs):
        self.append_calls += 1
        body = request.body
        size = len(body) if isinstance(body, bytes) else 0
        self._current_size += size
        return _make_result(
            models.AppendObjectResult,
            next_position=self._current_size,
            hash_crc64='222',
            headers={},
        )


# ==============================================================================
# Mock clients for ReadOnlyFile
# ==============================================================================

class _MockStreamBody:
    """Simulates a GetObject response body."""

    def __init__(self, data):
        self._data = data
        self._pos = 0
        self.is_closed = False

    def iter_bytes(self, **kwargs):
        block_size = kwargs.get('block_size', 8192)
        while self._pos < len(self._data):
            end = min(self._pos + block_size, len(self._data))
            chunk = self._data[self._pos:end]
            self._pos = end
            yield chunk

    def close(self):
        self.is_closed = True


class _MockOpenFileClient(OpenFileAPIClient):
    """Mock client for ReadOnlyFile tests."""

    def __init__(self, data):
        self._data = data
        self.head_calls = 0
        self.get_calls = 0

    def head_object(self, request, **kwargs):
        self.head_calls += 1
        return _make_result(
            models.HeadObjectResult,
            content_length=len(self._data),
            etag='"mock-etag"',
            headers={'Content-Length': str(len(self._data))},
        )

    def get_object(self, request, **kwargs):
        self.get_calls += 1
        start = 0
        end = len(self._data)
        if request.range_header:
            range_str = request.range_header.replace('bytes=', '')
            parts = range_str.split('-')
            start = int(parts[0])
            if parts[1]:
                end = int(parts[1]) + 1

        chunk = self._data[start:end]
        body = _MockStreamBody(chunk)
        result = _make_result(
            models.GetObjectResult,
            content_length=len(chunk),
            etag='"mock-etag"',
            headers={
                'Content-Length': str(len(chunk)),
                'Content-Range': f'bytes {start}-{end - 1}/{len(self._data)}'
            },
        )
        result.body = body
        return result


# ==============================================================================
# AppendOnlyFile tests
# ==============================================================================

class TestAppendOnlyFileNew(unittest.TestCase):
    """Tests AppendOnlyFile when the object does not exist."""

    def test_create_new_file_and_write(self):
        """Writing to a non-existent object creates it."""
        client = _MockAppendClient(object_exists=False)
        f = AppendOnlyFile(client, bucket='b', key='k')

        self.assertEqual(0, f.tell())
        self.assertFalse(f.closed)
        self.assertEqual('ab', f.mode)
        self.assertEqual('oss://b/k', f.name)

        n = f.write(b'hello')
        self.assertEqual(5, n)
        self.assertEqual(5, f.tell())
        self.assertEqual(1, client.append_calls)

    def test_write_multiple_times(self):
        """Multiple writes advance the offset."""
        client = _MockAppendClient(object_exists=False)
        f = AppendOnlyFile(client, bucket='b', key='k')

        f.write(b'aaa')
        f.write(b'bbbbb')

        self.assertEqual(8, f.tell())
        self.assertEqual(2, client.append_calls)

    def test_flush_creates_empty_object(self):
        """flush() on a new file calls append with empty bytes."""
        client = _MockAppendClient(object_exists=False)
        f = AppendOnlyFile(client, bucket='b', key='k')

        f.flush()
        self.assertEqual(1, client.append_calls)

    def test_close_prevents_further_writes(self):
        """After close(), write raises PathError."""
        client = _MockAppendClient(object_exists=False)
        f = AppendOnlyFile(client, bucket='b', key='k')
        f.close()

        self.assertTrue(f.closed)
        with self.assertRaises(PathError):
            f.write(b'data')

    def test_write_non_bytes_raises(self):
        """write() with non-bytes type raises PathError."""
        client = _MockAppendClient(object_exists=False)
        f = AppendOnlyFile(client, bucket='b', key='k')

        with self.assertRaises(PathError):
            f.write('string data')


class TestAppendOnlyFileExisting(unittest.TestCase):
    """Tests AppendOnlyFile when the object already exists."""

    def test_open_existing_appendable_file(self):
        """Opening an existing appendable file resumes from current offset."""
        client = _MockAppendClient(object_exists=True, object_size=100)
        f = AppendOnlyFile(client, bucket='b', key='k')

        self.assertEqual(100, f.tell())

    def test_open_non_appendable_raises(self):
        """Opening a non-appendable object raises PathError."""
        client = _MockAppendClient(object_exists=True, object_size=100,
                                   object_type='Normal')
        with self.assertRaises(PathError):
            AppendOnlyFile(client, bucket='b', key='k')

    def test_context_manager(self):
        """AppendOnlyFile works as a context manager."""
        client = _MockAppendClient(object_exists=False)
        with AppendOnlyFile(client, bucket='b', key='k') as f:
            f.write(b'ctx')
            self.assertFalse(f.closed)
        self.assertTrue(f.closed)


# ==============================================================================
# ReadOnlyFile tests
# ==============================================================================

class TestReadOnlyFileBasic(unittest.TestCase):
    """Tests basic ReadOnlyFile operations."""

    def test_read_all(self):
        """read() without arg returns all data."""
        data = b'hello world this is test data'
        client = _MockOpenFileClient(data)
        f = ReadOnlyFile(client, bucket='b', key='k')

        result = f.read()
        self.assertEqual(data, result)
        self.assertEqual(len(data), f.tell())

    def test_read_n_bytes(self):
        """read(n) returns at most n bytes."""
        data = b'abcdefghij'
        client = _MockOpenFileClient(data)
        f = ReadOnlyFile(client, bucket='b', key='k')

        chunk = f.read(5)
        self.assertEqual(b'abcde', chunk)
        self.assertEqual(5, f.tell())

        chunk2 = f.read(3)
        self.assertEqual(b'fgh', chunk2)
        self.assertEqual(8, f.tell())

    def test_read_at_eof(self):
        """read() at EOF returns empty bytes."""
        data = b'abc'
        client = _MockOpenFileClient(data)
        f = ReadOnlyFile(client, bucket='b', key='k')

        f.read()  # read all
        result = f.read()
        self.assertEqual(b'', result)

    def test_seek_and_tell(self):
        """seek() moves position, tell() reports it."""
        data = b'0123456789'
        client = _MockOpenFileClient(data)
        f = ReadOnlyFile(client, bucket='b', key='k')

        self.assertEqual(0, f.tell())

        f.seek(5)
        self.assertEqual(5, f.tell())

        # SEEK_CUR
        f.seek(2, 1)
        self.assertEqual(7, f.tell())

        # SEEK_END
        f.seek(-3, 2)
        self.assertEqual(7, f.tell())

    def test_seek_invalid_raises(self):
        """Negative seek position raises PathError."""
        data = b'abc'
        client = _MockOpenFileClient(data)
        f = ReadOnlyFile(client, bucket='b', key='k')

        with self.assertRaises(PathError):
            f.seek(-1)

    def test_close(self):
        """close() marks file as closed."""
        data = b'abc'
        client = _MockOpenFileClient(data)
        f = ReadOnlyFile(client, bucket='b', key='k')

        self.assertFalse(f.closed)
        f.close()
        self.assertTrue(f.closed)

        with self.assertRaises(PathError):
            f.read()

    def test_properties(self):
        """Mode, name, seekable, readable."""
        data = b'abc'
        client = _MockOpenFileClient(data)
        f = ReadOnlyFile(client, bucket='b', key='k')

        self.assertEqual('rb', f.mode)
        self.assertEqual('oss://b/k', f.name)
        self.assertTrue(f.seekable())
        self.assertTrue(f.readable())

    def test_name_with_version_id(self):
        """Name includes versionId when specified."""
        data = b'abc'
        client = _MockOpenFileClient(data)
        f = ReadOnlyFile(client, bucket='b', key='k', version_id='v1')

        self.assertEqual('oss://b/k?versionId=v1', f.name)

    def test_context_manager(self):
        """ReadOnlyFile works as a context manager."""
        data = b'test'
        client = _MockOpenFileClient(data)
        with ReadOnlyFile(client, bucket='b', key='k') as f:
            result = f.read()
            self.assertEqual(data, result)
        self.assertTrue(f.closed)

    def test_readinto(self):
        """readinto() fills a buffer."""
        data = b'abcdefghij'
        client = _MockOpenFileClient(data)
        f = ReadOnlyFile(client, bucket='b', key='k')

        buf = bytearray(5)
        n = f.readinto(buf)
        self.assertEqual(5, n)
        self.assertEqual(b'abcde', bytes(buf))
        self.assertEqual(5, f.tell())
