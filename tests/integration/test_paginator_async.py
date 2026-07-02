# pylint: skip-file
"""Integration tests for paginator and presign methods (async)."""
import unittest
import alibabacloud_oss_v2 as oss
from . import (
    TestIntegration,
    random_str,
    REGION,
    ENDPOINT,
    OBJECTNAME_PREFIX,
    get_async_client,
)


class TestPaginatorAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):
    """Integration tests for async paginator functionality."""

    async def asyncSetUp(self):
        self.async_client = get_async_client(REGION, ENDPOINT)

    async def asyncTearDown(self):
        await self.async_client.close()

    async def test_list_objects_v2_paginator(self):
        """Test async list_objects_v2 paginator with real data."""
        prefix = OBJECTNAME_PREFIX + 'paginator-v2-' + random_str(8) + '/'
        for i in range(5):
            result = await self.async_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=f'{prefix}obj-{i}',
                body=f'data-{i}',
            ))
            self.assertEqual(200, result.status_code)

        paginator = self.async_client.list_objects_v2_paginator()
        all_keys = []
        async for page in paginator.iter_page(oss.ListObjectsV2Request(
            bucket=self.bucket_name,
            prefix=prefix,
            max_keys=2,
        )):
            self.assertIsNotNone(page)
            if page.contents:
                for obj in page.contents:
                    all_keys.append(obj.key)

        self.assertEqual(5, len(all_keys))

    async def test_list_objects_v2_paginator_with_limit(self):
        """Test async list_objects_v2 paginator with limit kwarg."""
        prefix = OBJECTNAME_PREFIX + 'paginator-v2-limit-' + random_str(8) + '/'
        for i in range(5):
            await self.async_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=f'{prefix}obj-{i}',
                body=f'data-{i}',
            ))

        paginator = self.async_client.list_objects_v2_paginator(limit=2)
        page_count = 0
        all_keys = []
        async for page in paginator.iter_page(oss.ListObjectsV2Request(
            bucket=self.bucket_name,
            prefix=prefix,
        )):
            page_count += 1
            if page.contents:
                for obj in page.contents:
                    all_keys.append(obj.key)

        self.assertEqual(5, len(all_keys))
        self.assertGreaterEqual(page_count, 3)

    async def test_list_objects_paginator(self):
        """Test async list_objects paginator with real data."""
        prefix = OBJECTNAME_PREFIX + 'paginator-v1-' + random_str(8) + '/'
        for i in range(5):
            await self.async_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=f'{prefix}obj-{i}',
                body=f'data-{i}',
            ))

        paginator = self.async_client.list_objects_paginator()
        all_keys = []
        async for page in paginator.iter_page(oss.ListObjectsRequest(
            bucket=self.bucket_name,
            prefix=prefix,
            max_keys=2,
        )):
            self.assertIsNotNone(page)
            if page.contents:
                for obj in page.contents:
                    all_keys.append(obj.key)

        self.assertEqual(5, len(all_keys))

    async def test_list_object_versions_paginator(self):
        """Test async list_object_versions paginator."""
        self.client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=self.bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))

        prefix = OBJECTNAME_PREFIX + 'paginator-ver-' + random_str(8) + '/'
        key = f'{prefix}obj-versioned'
        for i in range(3):
            await self.async_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=f'data-{i}',
            ))

        paginator = self.async_client.list_object_versions_paginator()
        total_versions = 0
        async for page in paginator.iter_page(oss.ListObjectVersionsRequest(
            bucket=self.bucket_name,
            prefix=prefix,
        )):
            self.assertIsNotNone(page)
            if page.version:
                total_versions += len(page.version)

        self.assertEqual(3, total_versions)

        # Cleanup: delete all versions
        paginator2 = self.async_client.list_object_versions_paginator()
        delete_objects = []
        async for page in paginator2.iter_page(oss.ListObjectVersionsRequest(
            bucket=self.bucket_name,
            prefix=prefix,
        )):
            if page.version:
                for v in page.version:
                    delete_objects.append(oss.DeleteObject(key=v.key, version_id=v.version_id))
            if page.delete_marker:
                for d in page.delete_marker:
                    delete_objects.append(oss.DeleteObject(key=d.key, version_id=d.version_id))
        if delete_objects:
            await self.async_client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
                bucket=self.bucket_name,
                objects=delete_objects,
            ))

    async def test_list_buckets_paginator(self):
        """Test async list_buckets paginator."""
        paginator = self.async_client.list_buckets_paginator()
        bucket_names = []
        async for page in paginator.iter_page(oss.ListBucketsRequest(
            prefix=self.bucket_name,
        )):
            self.assertIsNotNone(page)
            if page.buckets:
                for b in page.buckets:
                    bucket_names.append(b.name)

        self.assertIn(self.bucket_name, bucket_names)

    async def test_list_multipart_uploads_paginator(self):
        """Test async list_multipart_uploads paginator."""
        prefix = OBJECTNAME_PREFIX + 'paginator-mpu-' + random_str(8) + '/'
        upload_ids = []
        for i in range(3):
            result = await self.async_client.initiate_multipart_upload(
                oss.InitiateMultipartUploadRequest(
                    bucket=self.bucket_name,
                    key=f'{prefix}obj-{i}',
                )
            )
            upload_ids.append(result.upload_id)

        paginator = self.async_client.list_multipart_uploads_paginator()
        found_uploads = []
        async for page in paginator.iter_page(oss.ListMultipartUploadsRequest(
            bucket=self.bucket_name,
            prefix=prefix,
        )):
            self.assertIsNotNone(page)
            if page.uploads:
                for u in page.uploads:
                    found_uploads.append(u.upload_id)

        for uid in upload_ids:
            self.assertIn(uid, found_uploads)

        # Cleanup
        for i, uid in enumerate(upload_ids):
            await self.async_client.abort_multipart_upload(
                oss.AbortMultipartUploadRequest(
                    bucket=self.bucket_name,
                    key=f'{prefix}obj-{i}',
                    upload_id=uid,
                )
            )

    async def test_list_parts_paginator(self):
        """Test async list_parts paginator."""
        key = OBJECTNAME_PREFIX + 'paginator-parts-' + random_str(16)
        result = await self.async_client.initiate_multipart_upload(
            oss.InitiateMultipartUploadRequest(
                bucket=self.bucket_name,
                key=key,
            )
        )
        upload_id = result.upload_id

        for i in range(1, 4):
            data = random_str(100 * 1024)
            await self.async_client.upload_part(oss.UploadPartRequest(
                bucket=self.bucket_name,
                key=key,
                part_number=i,
                upload_id=upload_id,
                body=data,
            ))

        paginator = self.async_client.list_parts_paginator()
        total_parts = 0
        async for page in paginator.iter_page(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=upload_id,
            max_parts=2,
        )):
            self.assertIsNotNone(page)
            if page.parts:
                total_parts += len(page.parts)

        self.assertEqual(3, total_parts)

        # Cleanup
        await self.async_client.abort_multipart_upload(
            oss.AbortMultipartUploadRequest(
                bucket=self.bucket_name,
                key=key,
                upload_id=upload_id,
            )
        )

