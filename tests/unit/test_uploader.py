# pylint: skip-file
"""Unit tests for alibabacloud_oss_v2.uploader.
"""
import io
import os
import shutil
import tempfile
import unittest

from alibabacloud_oss_v2 import models, defaults
from alibabacloud_oss_v2.uploader import Uploader, UploadAPIClient, UploadError, _UploaderDelegate


def _make_result(cls, **kwargs):
    obj = cls(**kwargs)
    obj.status = 'OK'
    obj.status_code = 200
    obj.request_id = 'mock-request-id'
    obj.headers = {}
    return obj


class _MockUploadClient(UploadAPIClient):
    """Configurable mock client used to drive Uploader through resumable paths."""

    def __init__(self,
                 list_parts_pages=None,
                 fail_after_n_parts=None,
                 part_size=None):
        self.list_parts_pages = list_parts_pages if list_parts_pages is not None else [[]]
        self.fail_after_n_parts = fail_after_n_parts
        self.part_size = part_size

        self.initiate_calls = 0
        self.list_parts_calls = 0
        self.upload_part_calls = 0
        self.complete_calls = 0
        self.abort_calls = 0
        self.put_calls = 0

        # Track abort request details for verification
        self.last_abort_request = None

        self._next_upload_id = 1

    def put_object(self, request, **kwargs):
        self.put_calls += 1
        return _make_result(models.PutObjectResult, etag='"put-etag"')

    def head_object(self, request, **kwargs):
        raise NotImplementedError

    def initiate_multipart_upload(self, request, **kwargs):
        self.initiate_calls += 1
        upload_id = f'mock-upload-id-{self._next_upload_id:04d}'
        self._next_upload_id += 1
        return _make_result(
            models.InitiateMultipartUploadResult,
            bucket=request.bucket,
            key=request.key,
            upload_id=upload_id,
        )

    def upload_part(self, request, **kwargs):
        self.upload_part_calls += 1
        if (self.fail_after_n_parts is not None
                and self.upload_part_calls > self.fail_after_n_parts):
            raise RuntimeError('mock network timeout')
        return _make_result(
            models.UploadPartResult,
            etag=f'"etag-part-{request.part_number}"',
        )

    def complete_multipart_upload(self, request, **kwargs):
        self.complete_calls += 1
        return _make_result(
            models.CompleteMultipartUploadResult,
            etag='"final-etag"',
        )

    def abort_multipart_upload(self, request, **kwargs):
        self.abort_calls += 1
        self.last_abort_request = request
        return _make_result(models.AbortMultipartUploadResult)

    def list_parts(self, request, **kwargs):
        self.list_parts_calls += 1
        idx = self.list_parts_calls - 1
        if idx >= len(self.list_parts_pages):
            parts = []
            is_truncated = False
        else:
            parts = list(self.list_parts_pages[idx])
            is_truncated = idx + 1 < len(self.list_parts_pages)
        return _make_result(
            models.ListPartsResult,
            bucket=request.bucket,
            key=request.key,
            upload_id=request.upload_id,
            part_number_marker=0,
            next_part_number_marker=parts[-1].part_number if parts else 0,
            max_parts=1000,
            is_truncated=is_truncated,
            parts=parts,
        )


class TestUploaderResumeRecovery(unittest.TestCase):
    """Regression tests for resumable-upload recovery paths."""

    PART_SIZE = 100 * 1024  # 100 KiB

    def setUp(self):
        self.workdir = tempfile.mkdtemp(prefix='oss-uploader-test-')
        self.cp_dir = os.path.join(self.workdir, 'cp')
        os.makedirs(self.cp_dir, exist_ok=True)
        # NOTE: UploadCheckpoint takes ``os.path.dirname(basedir)`` as the actual
        # checkpoint directory, so we must pass a path *inside* cp_dir (a
        # placeholder name) to make the .ucp file land in cp_dir.
        self._cp_arg = os.path.join(self.cp_dir, '_placeholder')

        # 3 full parts + 1 tail part
        self.total_size = self.PART_SIZE * 3 + 1234
        self.filepath = os.path.join(self.workdir, 'data.bin')
        with open(self.filepath, 'wb') as f:
            f.write(b'\xab' * self.total_size)

        self.request = models.PutObjectRequest(bucket='mock-bucket', key='mock-key')

    def tearDown(self):
        shutil.rmtree(self.workdir, ignore_errors=True)

    def _new_uploader(self, client):
        return Uploader(
            client,
            part_size=self.PART_SIZE,
            parallel_num=1,
            enable_checkpoint=True,
            checkpoint_dir=self._cp_arg,
        )

    def _phase_one_write_checkpoint(self):
        """Run a failing upload to populate the checkpoint with a stale upload_id."""
        client = _MockUploadClient(fail_after_n_parts=2, part_size=self.PART_SIZE)
        uploader = self._new_uploader(client)
        with self.assertRaises(UploadError):
            uploader.upload_file(self.request, self.filepath)
        # checkpoint must have been written
        ucp_files = [n for n in os.listdir(self.cp_dir) if n.endswith('.ucp')]
        self.assertTrue(ucp_files,
                        'checkpoint file should be written after phase-1 failure')
        return client

    def test_resume_when_list_parts_returns_empty(self):
        """ListParts returns no parts -> uploader must fall back to a fresh upload."""
        self._phase_one_write_checkpoint()

        # Phase 2: server has GC'd the upload, list_parts returns empty.
        client2 = _MockUploadClient(list_parts_pages=[[]], part_size=self.PART_SIZE)
        uploader2 = self._new_uploader(client2)

        # Should NOT raise TypeError; it should re-initiate a multipart upload.
        result = uploader2.upload_file(self.request, self.filepath)

        self.assertIsNotNone(result)
        self.assertEqual('"final-etag"', result.etag)
        self.assertEqual(1, client2.initiate_calls,
                         'a brand new multipart upload should have been initiated')
        self.assertEqual(1, client2.complete_calls)
        # 3 full parts + 1 tail part = 4 upload_part calls
        self.assertEqual(4, client2.upload_part_calls)

    def test_resume_when_list_parts_first_part_invalid_size(self):
        """If existing parts fail size validation, uploader must re-initiate."""
        self._phase_one_write_checkpoint()

        bad_part = models.Part(
            part_number=1,
            etag='"stale"',
            size=self.PART_SIZE // 2,  # wrong size -> generator returns immediately
        )
        client2 = _MockUploadClient(
            list_parts_pages=[[bad_part]],
            part_size=self.PART_SIZE,
        )
        uploader2 = self._new_uploader(client2)

        result = uploader2.upload_file(self.request, self.filepath)

        self.assertIsNotNone(result)
        self.assertEqual('"final-etag"', result.etag)
        self.assertEqual(1, client2.initiate_calls)
        self.assertEqual(4, client2.upload_part_calls)

    def test_resume_with_valid_parts_continues_from_offset(self):
        """When ListParts returns valid sequential parts, uploader should reuse them."""
        self._phase_one_write_checkpoint()

        valid_parts = [
            models.Part(part_number=1, etag='"p1"', size=self.PART_SIZE,
                        hash_crc64=None),
            models.Part(part_number=2, etag='"p2"', size=self.PART_SIZE,
                        hash_crc64=None),
        ]
        client2 = _MockUploadClient(
            list_parts_pages=[valid_parts],
            part_size=self.PART_SIZE,
        )
        uploader2 = self._new_uploader(client2)

        result = uploader2.upload_file(self.request, self.filepath)

        self.assertIsNotNone(result)
        self.assertEqual('"final-etag"', result.etag)
        # checkpoint upload_id is reused -> no new initiate
        self.assertEqual(0, client2.initiate_calls)
        # only the remaining 2 parts (#3 + tail) should be uploaded
        self.assertEqual(2, client2.upload_part_calls)
        self.assertEqual(1, client2.complete_calls)


class TestUploaderPartSizeAutoAdjust(unittest.TestCase):
    """Tests that part_size auto-adjusts for large files (Bug 1 fix)."""

    def test_apply_source_adjusts_part_size_for_large_file(self):
        """When total_size / part_size >= MAX_UPLOAD_PARTS, part_size increases."""
        part_size = 100
        # file size that exceeds MAX_UPLOAD_PARTS * part_size
        total_size = defaults.MAX_UPLOAD_PARTS * part_size + 1

        client = _MockUploadClient()
        uploader = Uploader(client, part_size=part_size, parallel_num=1)
        request = models.PutObjectRequest(bucket='test-bucket', key='test-key')
        delegate = uploader._delegate(request)

        reader = io.BytesIO(b'\x00' * total_size)
        delegate.apply_source(reader)

        # part_size must have increased so that total_size / new_part_size < MAX_UPLOAD_PARTS
        self.assertGreater(delegate._options.part_size, part_size)
        self.assertLess(total_size / delegate._options.part_size, defaults.MAX_UPLOAD_PARTS)

    def test_apply_source_no_adjust_for_small_file(self):
        """Small files don't need part_size adjustment."""
        part_size = 100 * 1024
        total_size = 50 * 1024  # less than one part

        client = _MockUploadClient()
        uploader = Uploader(client, part_size=part_size, parallel_num=1)
        request = models.PutObjectRequest(bucket='test-bucket', key='test-key')
        delegate = uploader._delegate(request)

        reader = io.BytesIO(b'\x00' * total_size)
        delegate.apply_source(reader)

        self.assertEqual(delegate._options.part_size, part_size)


class TestUploaderAbortRequest(unittest.TestCase):
    """Tests that abort_multipart_upload receives correct bucket/key (Bug 2 fix)."""

    PART_SIZE = 100 * 1024

    def test_abort_request_has_bucket_and_key(self):
        """When upload fails and leave_parts_on_error=False, abort request has bucket/key."""
        client = _MockUploadClient(fail_after_n_parts=1)
        uploader = Uploader(
            client,
            part_size=self.PART_SIZE,
            parallel_num=1,
            leave_parts_on_error=False,
        )

        total_size = self.PART_SIZE * 3
        filepath = os.path.join(tempfile.gettempdir(), 'test_abort_req.bin')
        with open(filepath, 'wb') as f:
            f.write(b'\x00' * total_size)

        request = models.PutObjectRequest(bucket='my-bucket', key='my-key')
        try:
            with self.assertRaises(UploadError):
                uploader.upload_file(request, filepath)

            # abort must have been called
            self.assertEqual(1, client.abort_calls)
            # abort request must carry correct bucket and key
            self.assertEqual('my-bucket', client.last_abort_request.bucket)
            self.assertEqual('my-key', client.last_abort_request.key)
            self.assertIsNotNone(client.last_abort_request.upload_id)
        finally:
            os.remove(filepath)


class TestUploaderSmallFileAndStream(unittest.TestCase):
    """Tests single-part upload and upload_from stream path."""

    def test_small_file_uses_put_object(self):
        """File smaller than part_size goes through put_object."""
        client = _MockUploadClient()
        part_size = 100 * 1024
        uploader = Uploader(client, part_size=part_size, parallel_num=1)

        filepath = os.path.join(tempfile.gettempdir(), 'test_small.bin')
        with open(filepath, 'wb') as f:
            f.write(b'\xab' * 1024)  # 1KB << part_size

        request = models.PutObjectRequest(bucket='test-bucket', key='test-key')
        try:
            result = uploader.upload_file(request, filepath)
            self.assertEqual('"put-etag"', result.etag)
            self.assertEqual(1, client.put_calls)
            self.assertEqual(0, client.initiate_calls)
        finally:
            os.remove(filepath)

    def test_upload_from_stream(self):
        """upload_from with a stream triggers multipart when size unknown."""
        client = _MockUploadClient()
        part_size = 1024
        uploader = Uploader(client, part_size=part_size, parallel_num=1)

        # Use a non-seekable stream wrapper
        data = b'\xcd' * (part_size * 2 + 100)

        class NonSeekableStream:
            def __init__(self, data):
                self._buf = io.BytesIO(data)
            def read(self, n=-1):
                return self._buf.read(n)
            def readable(self):
                return True

        stream = NonSeekableStream(data)
        request = models.PutObjectRequest(bucket='test-bucket', key='test-key')
        result = uploader.upload_from(request, stream)

        self.assertEqual('"final-etag"', result.etag)
        self.assertEqual(1, client.initiate_calls)
        self.assertEqual(3, client.upload_part_calls)  # 2 full + 1 tail
        self.assertEqual(1, client.complete_calls)


class TestUploaderIterUploadedPartError(unittest.TestCase):
    """Tests that mid-iteration error discards partial parts (Bug 4 fix)."""

    PART_SIZE = 100 * 1024

    def test_iter_error_midway_discards_stale_parts(self):
        """If _iter_uploaded_part raises midway, stale parts are discarded."""
        client = _MockUploadClient()
        uploader = Uploader(client, part_size=self.PART_SIZE, parallel_num=1)
        request = models.PutObjectRequest(bucket='test-bucket', key='test-key')
        delegate = uploader._delegate(request)

        # Simulate checkpoint loaded an upload_id
        delegate._upload_id = 'stale-upload-id'
        delegate._reader_seekable = True
        delegate._total_size = self.PART_SIZE * 5

        # Monkey-patch _iter_uploaded_part to yield one part then raise
        call_count = [0]
        def _bad_iter():
            call_count[0] += 1
            yield models.Part(part_number=1, etag='"p1"', size=self.PART_SIZE, hash_crc64=None)
            # Simulate mid-iteration error: set upload_id = None (as the real code does)
            delegate._upload_id = None

        delegate._iter_uploaded_part = _bad_iter

        # After adjust_source, stale parts should be discarded
        delegate.adjust_source()

        # upload_id was cleared, so no stale state
        self.assertIsNone(delegate._upload_id)
        self.assertEqual([], delegate._uploaded_parts)
        self.assertIsNone(delegate._part_number)
