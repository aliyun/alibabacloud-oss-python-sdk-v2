# pylint: skip-file
"""Unit tests for alibabacloud_oss_v2.copier."""
import unittest

from alibabacloud_oss_v2 import models, defaults
from alibabacloud_oss_v2.copier import Copier, CopyAPIClient, CopyError


def _make_result(cls, **kwargs):
    obj = cls(**kwargs)
    obj.status = 'OK'
    obj.status_code = 200
    obj.request_id = 'mock-request-id'
    obj.headers = kwargs.get('headers', {})
    return obj


class _MockCopyClient(CopyAPIClient):
    """Mock client for testing Copier."""

    def __init__(self, source_size=1024, fail_copy_part_after=None,
                 server_side_encryption=None, tagging_count=0):
        self._source_size = source_size
        self._fail_copy_part_after = fail_copy_part_after
        self._server_side_encryption = server_side_encryption
        self._tagging_count = tagging_count

        self.head_calls = 0
        self.copy_calls = 0
        self.initiate_calls = 0
        self.upload_part_copy_calls = 0
        self.complete_calls = 0
        self.abort_calls = 0
        self.get_tagging_calls = 0

        self.last_abort_request = None

    def copy_object(self, request, **kwargs):
        self.copy_calls += 1
        return _make_result(
            models.CopyObjectResult,
            etag='"copy-etag"',
            hash_crc64='12345',
            headers={'x-oss-hash-crc64ecma': '12345'},
        )

    def head_object(self, request, **kwargs):
        self.head_calls += 1
        result = _make_result(
            models.HeadObjectResult,
            content_length=self._source_size,
            hash_crc64='12345',
            headers={'Content-Length': str(self._source_size)},
        )
        result.server_side_encryption = self._server_side_encryption
        result.tagging_count = self._tagging_count
        return result

    def initiate_multipart_upload(self, request, **kwargs):
        self.initiate_calls += 1
        return _make_result(
            models.InitiateMultipartUploadResult,
            bucket=request.bucket,
            key=request.key,
            upload_id='mock-copy-upload-id',
        )

    def upload_part_copy(self, request, **kwargs):
        self.upload_part_copy_calls += 1
        if (self._fail_copy_part_after is not None
                and self.upload_part_copy_calls > self._fail_copy_part_after):
            raise RuntimeError('mock copy part failure')
        return _make_result(
            models.UploadPartCopyResult,
            etag=f'"copy-part-{request.part_number}"',
        )

    def complete_multipart_upload(self, request, **kwargs):
        self.complete_calls += 1
        return _make_result(
            models.CompleteMultipartUploadResult,
            etag='"final-copy-etag"',
            hash_crc64='12345',
            headers={'x-oss-hash-crc64ecma': '12345'},
        )

    def abort_multipart_upload(self, request, **kwargs):
        self.abort_calls += 1
        self.last_abort_request = request
        return _make_result(models.AbortMultipartUploadResult)

    def list_parts(self, request, **kwargs):
        return _make_result(
            models.ListPartsResult,
            bucket=request.bucket,
            key=request.key,
            upload_id=request.upload_id,
            part_number_marker=0,
            next_part_number_marker=0,
            max_parts=1000,
            is_truncated=False,
            parts=[],
        )

    def get_object_tagging(self, request, **kwargs):
        self.get_tagging_calls += 1
        return _make_result(
            models.GetObjectTaggingResult,
            tag_set=models.TagSet(tags=[
                models.Tag(key='env', value='test'),
            ]),
        )


class TestCopierSingleCopy(unittest.TestCase):
    """Tests single (non-multipart) copy path."""

    def test_small_object_uses_copy_object(self):
        """Object below threshold uses copy_object directly."""
        source_size = 1024
        client = _MockCopyClient(source_size=source_size)
        copier = Copier(
            client,
            part_size=64 * 1024 * 1024,
            parallel_num=1,
            multipart_copy_threshold=200 * 1024 * 1024,
            disable_shallow_copy=True,
        )

        request = models.CopyObjectRequest(
            bucket='dst-bucket',
            key='dst-key',
            source_key='src-key',
        )
        result = copier.copy(request)

        self.assertEqual('"copy-etag"', result.etag)
        self.assertEqual(1, client.copy_calls)
        self.assertEqual(0, client.initiate_calls)
        self.assertEqual(1, client.head_calls)


class TestCopierMultipartCopy(unittest.TestCase):
    """Tests multipart copy path."""

    def test_large_object_uses_multipart_copy(self):
        """Object above threshold uses multipart copy."""
        part_size = 1024
        threshold = 2048
        source_size = 3000  # above threshold, needs 3 parts
        client = _MockCopyClient(source_size=source_size)
        copier = Copier(
            client,
            part_size=part_size,
            parallel_num=1,
            multipart_copy_threshold=threshold,
            disable_shallow_copy=True,
        )

        request = models.CopyObjectRequest(
            bucket='dst-bucket',
            key='dst-key',
            source_key='src-key',
        )
        result = copier.copy(request)

        self.assertEqual('"final-copy-etag"', result.etag)
        self.assertEqual(1, client.initiate_calls)
        self.assertEqual(3, client.upload_part_copy_calls)
        self.assertEqual(1, client.complete_calls)
        self.assertEqual(0, client.copy_calls)

    def test_multipart_copy_aborts_on_failure(self):
        """When copy part fails, abort is called with correct request."""
        part_size = 1024
        threshold = 2048
        source_size = 5000
        client = _MockCopyClient(source_size=source_size, fail_copy_part_after=2)
        copier = Copier(
            client,
            part_size=part_size,
            parallel_num=1,
            multipart_copy_threshold=threshold,
            leave_parts_on_error=False,
            disable_shallow_copy=True,
        )

        request = models.CopyObjectRequest(
            bucket='dst-bucket',
            key='dst-key',
            source_key='src-key',
        )

        with self.assertRaises(CopyError):
            copier.copy(request)

        self.assertEqual(1, client.abort_calls)
        self.assertIsNotNone(client.last_abort_request)
        self.assertEqual('dst-bucket', client.last_abort_request.bucket)
        self.assertEqual('dst-key', client.last_abort_request.key)
        self.assertEqual('mock-copy-upload-id', client.last_abort_request.upload_id)

    def test_multipart_copy_with_tags(self):
        """When source has tags, copier fetches and applies them."""
        part_size = 1024
        threshold = 2048
        source_size = 3000
        client = _MockCopyClient(source_size=source_size, tagging_count=1)
        copier = Copier(
            client,
            part_size=part_size,
            parallel_num=1,
            multipart_copy_threshold=threshold,
            disable_shallow_copy=True,
        )

        request = models.CopyObjectRequest(
            bucket='dst-bucket',
            key='dst-key',
            source_key='src-key',
        )
        result = copier.copy(request)

        self.assertEqual('"final-copy-etag"', result.etag)
        self.assertEqual(1, client.get_tagging_calls)


class TestCopierProgressCallback(unittest.TestCase):
    """Tests progress callback for copier."""

    def test_progress_fn_called_for_single_copy(self):
        """progress_fn is called for single-copy path."""
        source_size = 1024
        client = _MockCopyClient(source_size=source_size)
        copier = Copier(
            client,
            part_size=64 * 1024 * 1024,
            parallel_num=1,
            multipart_copy_threshold=200 * 1024 * 1024,
            disable_shallow_copy=True,
        )

        progress_data = []

        def _progress(increment, transferred, total):
            progress_data.append((increment, transferred, total))

        request = models.CopyObjectRequest(
            bucket='dst-bucket',
            key='dst-key',
            source_key='src-key',
            progress_fn=_progress,
        )
        result = copier.copy(request)

        self.assertEqual('"copy-etag"', result.etag)
        self.assertEqual(1, len(progress_data))
        self.assertEqual(source_size, progress_data[0][0])
