# pylint: skip-file
"""Integration tests for paginator and convenience methods."""
import tempfile
import os
import alibabacloud_oss_v2 as oss
from . import (
    TestIntegration,
    random_str,
    REGION,
    ENDPOINT,
    OBJECTNAME_PREFIX)


class TestPaginator(TestIntegration):
    """Integration tests for paginator functionality."""

    def test_list_objects_v2_paginator(self):
        """Test list_objects_v2 paginator with real data."""
        prefix = OBJECTNAME_PREFIX + 'paginator-v2-' + random_str(8) + '/'
        for i in range(5):
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=f'{prefix}obj-{i}',
                body=f'data-{i}'))
            self.assertEqual(200, result.status_code)

        paginator = self.client.list_objects_v2_paginator()
        all_keys = []
        for page in paginator.iter_page(oss.ListObjectsV2Request(
            bucket=self.bucket_name,
            prefix=prefix,
            max_keys=2)):
            self.assertIsNotNone(page)
            if page.contents:
                for obj in page.contents:
                    all_keys.append(obj.key)

        self.assertEqual(5, len(all_keys))

    def test_list_objects_v2_paginator_with_limit(self):
        """Test list_objects_v2 paginator with limit kwarg."""
        prefix = OBJECTNAME_PREFIX + 'paginator-v2-limit-' + random_str(8) + '/'
        for i in range(5):
            self.client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=f'{prefix}obj-{i}',
                body=f'data-{i}'))

        paginator = self.client.list_objects_v2_paginator(limit=2)
        page_count = 0
        all_keys = []
        for page in paginator.iter_page(oss.ListObjectsV2Request(
            bucket=self.bucket_name,
            prefix=prefix)):
            page_count += 1
            if page.contents:
                for obj in page.contents:
                    all_keys.append(obj.key)

        self.assertEqual(5, len(all_keys))
        self.assertGreaterEqual(page_count, 3)

    def test_list_objects_paginator(self):
        """Test list_objects paginator with real data."""
        prefix = OBJECTNAME_PREFIX + 'paginator-v1-' + random_str(8) + '/'
        for i in range(5):
            self.client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=f'{prefix}obj-{i}',
                body=f'data-{i}'))

        paginator = self.client.list_objects_paginator()
        all_keys = []
        for page in paginator.iter_page(oss.ListObjectsRequest(
            bucket=self.bucket_name,
            prefix=prefix,
            max_keys=2)):
            self.assertIsNotNone(page)
            if page.contents:
                for obj in page.contents:
                    all_keys.append(obj.key)

        self.assertEqual(5, len(all_keys))

    def test_list_object_versions_paginator(self):
        """Test list_object_versions paginator."""
        self.client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=self.bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))

        prefix = OBJECTNAME_PREFIX + 'paginator-ver-' + random_str(8) + '/'
        key = f'{prefix}obj-versioned'
        for i in range(3):
            self.client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=f'data-{i}'))

        paginator = self.client.list_object_versions_paginator()
        total_versions = 0
        for page in paginator.iter_page(oss.ListObjectVersionsRequest(
            bucket=self.bucket_name,
            prefix=prefix)):
            self.assertIsNotNone(page)
            if page.version:
                total_versions += len(page.version)

        self.assertEqual(3, total_versions)

        # Cleanup: delete all versions
        paginator2 = self.client.list_object_versions_paginator()
        delete_objects = []
        for page in paginator2.iter_page(oss.ListObjectVersionsRequest(
            bucket=self.bucket_name,
            prefix=prefix)):
            if page.version:
                for v in page.version:
                    delete_objects.append(oss.DeleteObject(key=v.key, version_id=v.version_id))
            if page.delete_marker:
                for d in page.delete_marker:
                    delete_objects.append(oss.DeleteObject(key=d.key, version_id=d.version_id))
        if delete_objects:
            self.client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
                bucket=self.bucket_name,
                objects=delete_objects))

    def test_list_buckets_paginator(self):
        """Test list_buckets paginator."""
        paginator = self.client.list_buckets_paginator()
        bucket_names = []
        for page in paginator.iter_page(oss.ListBucketsRequest(
            prefix=self.bucket_name)):
            self.assertIsNotNone(page)
            if page.buckets:
                for b in page.buckets:
                    bucket_names.append(b.name)

        self.assertIn(self.bucket_name, bucket_names)

    def test_list_multipart_uploads_paginator(self):
        """Test list_multipart_uploads paginator."""
        prefix = OBJECTNAME_PREFIX + 'paginator-mpu-' + random_str(8) + '/'
        upload_ids = []
        for i in range(3):
            result = self.client.initiate_multipart_upload(
                oss.InitiateMultipartUploadRequest(
                    bucket=self.bucket_name,
                    key=f'{prefix}obj-{i}')
            )
            upload_ids.append(result.upload_id)

        paginator = self.client.list_multipart_uploads_paginator()
        found_uploads = []
        for page in paginator.iter_page(oss.ListMultipartUploadsRequest(
            bucket=self.bucket_name,
            prefix=prefix)):
            self.assertIsNotNone(page)
            if page.uploads:
                for u in page.uploads:
                    found_uploads.append(u.upload_id)

        for uid in upload_ids:
            self.assertIn(uid, found_uploads)

        # Cleanup
        for i, uid in enumerate(upload_ids):
            self.client.abort_multipart_upload(
                oss.AbortMultipartUploadRequest(
                    bucket=self.bucket_name,
                    key=f'{prefix}obj-{i}',
                    upload_id=uid)
            )

    def test_list_parts_paginator(self):
        """Test list_parts paginator."""
        key = OBJECTNAME_PREFIX + 'paginator-parts-' + random_str(16)
        result = self.client.initiate_multipart_upload(
            oss.InitiateMultipartUploadRequest(
                bucket=self.bucket_name,
                key=key)
        )
        upload_id = result.upload_id

        for i in range(1, 4):
            data = random_str(100 * 1024)
            self.client.upload_part(oss.UploadPartRequest(
                bucket=self.bucket_name,
                key=key,
                part_number=i,
                upload_id=upload_id,
                body=data))

        paginator = self.client.list_parts_paginator()
        total_parts = 0
        for page in paginator.iter_page(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=upload_id,
            max_parts=2)):
            self.assertIsNotNone(page)
            if page.parts:
                total_parts += len(page.parts)

        self.assertEqual(3, total_parts)

        # Cleanup
        self.client.abort_multipart_upload(
            oss.AbortMultipartUploadRequest(
                bucket=self.bucket_name,
                key=key,
                upload_id=upload_id)
        )


class TestConvenience(TestIntegration):
    """Integration tests for convenience methods."""

    def test_put_object_from_file(self):
        """Test put_object_from_file with a real file."""
        key = OBJECTNAME_PREFIX + 'from-file-' + random_str(16)
        data = random_str(1024)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(data)
            temp_path = f.name

        try:
            result = self.client.put_object_from_file(
                oss.PutObjectRequest(
                    bucket=self.bucket_name,
                    key=key),
                filepath=temp_path)
            self.assertEqual(200, result.status_code)
            self.assertIsNotNone(result.etag)
            self.assertIsNotNone(result.hash_crc64)

            gresult = self.client.get_object(oss.GetObjectRequest(
                bucket=self.bucket_name,
                key=key))
            self.assertEqual(200, gresult.status_code)
            self.assertEqual(data.encode(), gresult.body.content)
        finally:
            os.unlink(temp_path)

    def test_get_object_to_file(self):
        """Test get_object_to_file with a real file."""
        key = OBJECTNAME_PREFIX + 'to-file-' + random_str(16)
        data = random_str(2048)

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data))
        self.assertEqual(200, result.status_code)

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
            temp_path = f.name

        try:
            gresult = self.client.get_object_to_file(
                oss.GetObjectRequest(
                    bucket=self.bucket_name,
                    key=key),
                filepath=temp_path)
            self.assertEqual(200, gresult.status_code)

            with open(temp_path, 'rb') as f:
                file_content = f.read()

            self.assertEqual(data.encode(), file_content)
        finally:
            os.unlink(temp_path)

    def test_is_bucket_exist(self):
        """Test is_bucket_exist."""
        exist = self.client.is_bucket_exist(self.bucket_name)
        self.assertTrue(exist)

        exist = self.client.is_bucket_exist(self.bucket_name + '-no-exist')
        self.assertFalse(exist)

    def test_is_object_exist(self):
        """Test is_object_exist."""
        key = OBJECTNAME_PREFIX + 'exist-check-' + random_str(16)

        exist = self.client.is_object_exist(self.bucket_name, key)
        self.assertFalse(exist)

        self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=b'test'))

        exist = self.client.is_object_exist(self.bucket_name, key)
        self.assertTrue(exist)
