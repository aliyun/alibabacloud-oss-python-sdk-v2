# pylint: skip-file
"""Unit tests for alibabacloud_oss_v2.downloader."""
import io
import os
import tempfile
import unittest

from alibabacloud_oss_v2 import models, defaults
from alibabacloud_oss_v2.downloader import Downloader, DownloadAPIClient, DownloadError


def _make_result(cls, **kwargs):
    obj = cls(**kwargs)
    obj.status = 'OK'
    obj.status_code = 200
    obj.request_id = 'mock-request-id'
    obj.headers = kwargs.get('headers', {})
    return obj


class _MockStreamBody:
    """Simulates a response body with iter_bytes()."""

    def __init__(self, data, fail_after=None):
        self._data = data
        self._fail_after = fail_after
        self._pos = 0
        self.is_closed = False
        self.content_length = len(data)

    def iter_bytes(self, **kwargs):
        block_size = kwargs.get('block_size', 8192)
        yielded = 0
        while self._pos < len(self._data):
            if self._fail_after is not None and yielded >= self._fail_after:
                raise IOError('mock stream error')
            end = min(self._pos + block_size, len(self._data))
            chunk = self._data[self._pos:end]
            self._pos = end
            yielded += len(chunk)
            yield chunk

    def close(self):
        self.is_closed = True


class _AlwaysFailStreamBody:
    """A stream body that always fails on iter_bytes."""

    def __init__(self, content_length):
        self.is_closed = False
        self.content_length = content_length

    def iter_bytes(self, **kwargs):
        raise IOError('persistent stream failure')

    def close(self):
        self.is_closed = True


class _MockDownloadClient(DownloadAPIClient):
    """Mock client for testing Downloader."""

    def __init__(self, data, fail_stream_after=None, always_fail_stream=False):
        self._data = data
        self._fail_stream_after = fail_stream_after
        self._always_fail_stream = always_fail_stream
        self.head_calls = 0
        self.get_calls = 0

    def head_object(self, request, **kwargs):
        self.head_calls += 1
        return _make_result(
            models.HeadObjectResult,
            content_length=len(self._data),
            headers={'Content-Length': str(len(self._data))},
        )

    def get_object(self, request, **kwargs):
        self.get_calls += 1

        # Parse range header
        start = 0
        end = len(self._data) - 1
        if request.range_header:
            # format: bytes=start-end
            range_str = request.range_header.replace('bytes=', '')
            parts = range_str.split('-')
            start = int(parts[0])
            if parts[1]:
                end = int(parts[1])

        chunk = self._data[start:end + 1]

        if self._always_fail_stream:
            body = _AlwaysFailStreamBody(len(chunk))
        else:
            body = _MockStreamBody(chunk, fail_after=self._fail_stream_after)

        result = _make_result(
            models.GetObjectResult,
            content_length=len(chunk),
            headers={
                'Content-Length': str(len(chunk)),
                'Content-Range': f'bytes {start}-{end}/{len(self._data)}'
            },
        )
        result.body = body
        return result


class TestDownloaderBasicFlow(unittest.TestCase):
    """Tests basic download paths."""

    def test_single_part_download(self):
        """File smaller than part_size downloads in one GET."""
        data = b'\xab' * 1024  # 1 KB
        client = _MockDownloadClient(data)
        downloader = Downloader(client, part_size=6 * 1024 * 1024, parallel_num=1)

        buf = io.BytesIO()
        request = models.GetObjectRequest(bucket='test-bucket', key='test-key')
        result = downloader.download_to(request, buf)

        self.assertEqual(len(data), result.written)
        self.assertEqual(data, buf.getvalue())
        self.assertEqual(1, client.head_calls)

    def test_multi_part_download(self):
        """File larger than part_size downloads in multiple GETs."""
        part_size = 1024
        data = b'\xcd' * (part_size * 3 + 500)
        client = _MockDownloadClient(data)
        downloader = Downloader(client, part_size=part_size, parallel_num=1)

        buf = io.BytesIO()
        request = models.GetObjectRequest(bucket='test-bucket', key='test-key')
        result = downloader.download_to(request, buf)

        self.assertEqual(len(data), result.written)
        self.assertEqual(data, buf.getvalue())
        # 1 head + multiple gets (4 parts: 3 full + 1 tail)
        self.assertEqual(4, client.get_calls)

    def test_download_to_file(self):
        """download_file writes data to a local file."""
        data = b'\xef' * 2048
        client = _MockDownloadClient(data)
        downloader = Downloader(client, part_size=6 * 1024 * 1024, parallel_num=1)

        filepath = os.path.join(tempfile.gettempdir(), 'test_dl.bin')
        request = models.GetObjectRequest(bucket='test-bucket', key='test-key')
        try:
            result = downloader.download_file(request, filepath)
            self.assertEqual(len(data), result.written)
            with open(filepath, 'rb') as f:
                self.assertEqual(data, f.read())
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)


class TestDownloaderNoProgressRetry(unittest.TestCase):
    """Tests that persistent stream failures don't loop forever (Bug 5 fix)."""

    def test_always_failing_stream_raises_after_max_retries(self):
        """When iter_bytes always raises, download fails after 3 retries."""
        data = b'\x00' * 2048
        client = _MockDownloadClient(data, always_fail_stream=True)
        downloader = Downloader(client, part_size=6 * 1024 * 1024, parallel_num=1)

        buf = io.BytesIO()
        request = models.GetObjectRequest(bucket='test-bucket', key='test-key')

        with self.assertRaises(DownloadError) as ctx:
            downloader.download_to(request, buf)

        # Should have retried 3 times (get_object succeeds, iter_bytes fails)
        self.assertEqual(3, client.get_calls)

    def test_progress_fn_called(self):
        """progress_fn receives correct increments."""
        data = b'\xab' * 1024
        client = _MockDownloadClient(data)
        downloader = Downloader(client, part_size=6 * 1024 * 1024, parallel_num=1)

        progress_data = []

        def _progress(increment, written, total):
            progress_data.append((increment, written, total))

        buf = io.BytesIO()
        request = models.GetObjectRequest(bucket='test-bucket', key='test-key', progress_fn=_progress)
        result = downloader.download_to(request, buf)

        self.assertEqual(len(data), result.written)
        self.assertGreater(len(progress_data), 0)
        # Last entry should have written == total
        self.assertEqual(progress_data[-1][1], len(data))
