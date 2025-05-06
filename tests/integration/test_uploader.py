# pylint: skip-file

import tempfile
import alibabacloud_oss_v2 as oss
from typing import Dict, Any
from . import TestIntegration, random_bucket_name, random_str, OBJECTNAME_PREFIX


class TestUploader(TestIntegration):
    def test_uploader_with_sequential(self):
        length = 100 * 1024 + 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        key_2 = OBJECTNAME_PREFIX + random_str(16)

        uploader = self.client.uploader()

        # case 1: usually uploader
        with tempfile.TemporaryFile() as fp:
            fp.write(data.encode())
            fp.seek(0)

            result = uploader.upload_from(oss.PutObjectRequest(
                    bucket=self.bucket_name,
                    key=key,
                ),
                reader=fp,
                part_size=100*1024,
            )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        head_result = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        etag = head_result.etag
        self.assertEqual(200, head_result.status_code)
        self.assertEqual("Multipart", head_result.object_type)
        self.assertIsNone(head_result.content_md5)

        # case 2: sequential uploader
        kwargs: Dict[str, Any] = {}
        kwargs['parameters'] = {'sequential': ''}

        with tempfile.TemporaryFile() as fp:
            fp.write(data.encode())
            fp.seek(0)

            result = uploader.upload_from(oss.PutObjectRequest(
                    bucket=self.bucket_name,
                    key=key_2,
                    **kwargs,
                ),
                reader=fp,
                part_size=100*1024,
            )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        head_result = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key_2,
        ))
        self.assertEqual(200, head_result.status_code)
        self.assertEqual("Multipart", head_result.object_type)
        self.assertEqual(etag, head_result.etag)
        self.assertIsNotNone(head_result.content_md5)
