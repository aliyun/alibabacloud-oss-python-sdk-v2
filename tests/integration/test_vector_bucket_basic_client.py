# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors
from . import TestIntegrationVectors, random_bucket_name


class TestVectorBucketBasic(TestIntegrationVectors):

    def test_vector_bucket_basic(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.vector_client.put_vector_bucket(oss_vectors.models.PutVectorBucketRequest(
            bucket=bucket_name,
            acl='private',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket info
        result = self.vector_client.get_vector_bucket(oss_vectors.models.GetVectorBucketRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.bucket_info.name)
        self.assertIsNotNone(result.bucket_info.location)
        self.assertIsNotNone(result.bucket_info.creation_date)

        # list buckets
        result = self.vector_client.list_vector_buckets(oss_vectors.models.ListVectorBucketsRequest(
            prefix=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(result.buckets)
        self.assertGreater(len(result.buckets), 0)
        found = False
        for bucket in result.buckets:
            if bucket.name == bucket_name:
                found = True
                break
        self.assertTrue(found)

        # delete bucket
        result = self.vector_client.delete_vector_bucket(oss_vectors.models.DeleteVectorBucketRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
