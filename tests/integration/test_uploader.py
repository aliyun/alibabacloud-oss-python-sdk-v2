# pylint: skip-file

import alibabacloud_oss_v2 as oss
from typing import Dict, Any
from . import TestIntegration, random_bucket_name, random_str, OBJECTNAME_PREFIX


class TestUploader(TestIntegration):
    def test_uploader_with_sequential(self):
        length = 100 * 1024 + 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)

        uploader = self.client.uploader()

        # case 1: usually uploader
        result = uploader.upload_from(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ), reader=data)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertIsNone(result.upload_id)

        head_result = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        etag = head_result.etag
        self.assertEqual(200, result.status_code)

        # case 2: sequential uploader
        kwargs: Dict[str, Any] = {}
        kwargs['parameters'] = {'sequential': ''}

        result = uploader.upload_from(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            **kwargs,
        ), reader=data)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertIsNone(result.upload_id)

        head_result = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(etag, head_result.etag)
