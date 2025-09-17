# pylint: skip-file

import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors
from tests.integration import TestIntegrationVectors, random_short_bucket_name, random_bucket_name


class TestVectorBucketLogging(TestIntegrationVectors):
    """Integration tests for Vector Bucket Logging operations."""

    def test_vector_bucket_logging(self):
        """Test put, get, and delete bucket logging operations."""
        # 1. Create buckets: source bucket and target bucket
        source_bucket_name = random_short_bucket_name()
        target_bucket_name = random_bucket_name()

        print(source_bucket_name)
        print(target_bucket_name)

        # Create source bucket
        result = self.vector_client.put_vector_bucket(
            oss_vectors.models.PutVectorBucketRequest(
                bucket=source_bucket_name,
            )
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        # create target bucket
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=target_bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        # 2. Put bucket logging (enable logging)
        logging_prefix = 'log-prefix'
        logging_role = 'AliyunOSSLoggingDefaultRole'
        put_result = self.vector_client.put_bucket_logging(
            oss_vectors.models.PutBucketLoggingRequest(
                bucket=source_bucket_name,
                bucket_logging_status=oss_vectors.models.BucketLoggingStatus(
                    logging_enabled=oss_vectors.models.LoggingEnabled(
                        target_bucket=target_bucket_name,
                        target_prefix=logging_prefix,
                        logging_role=logging_role,
                    ),
                ),
            )
        )
        self.assertEqual(200, put_result.status_code)
        self.assertEqual('OK', put_result.status)
        self.assertEqual(24, len(put_result.request_id))
        self.assertEqual(24, len(put_result.headers.get('x-oss-request-id')))

        # 3. Get bucket logging (verify logging configuration)
        get_result = self.vector_client.get_bucket_logging(
            oss_vectors.models.GetBucketLoggingRequest(
                bucket=source_bucket_name
            )
        )
        self.assertEqual(200, get_result.status_code)
        self.assertEqual('OK', get_result.status)
        self.assertEqual(24, len(get_result.request_id))
        self.assertEqual(24, len(get_result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(get_result.bucket_logging_status)
        self.assertIsNotNone(get_result.bucket_logging_status.logging_enabled)
        self.assertEqual(target_bucket_name, get_result.bucket_logging_status.logging_enabled.target_bucket)
        self.assertEqual(logging_prefix, get_result.bucket_logging_status.logging_enabled.target_prefix)
        self.assertEqual(logging_role, get_result.bucket_logging_status.logging_enabled.logging_role)

        # 4. Delete bucket logging (disable logging)
        delete_result = self.vector_client.delete_bucket_logging(
            oss_vectors.models.DeleteBucketLoggingRequest(
                bucket=source_bucket_name
            )
        )
        self.assertEqual(204, delete_result.status_code)  # Delete typically returns 204 No Content
        self.assertEqual(24, len(delete_result.request_id))
        self.assertEqual(24, len(delete_result.headers.get('x-oss-request-id')))

        # 5. Verify logging is disabled by getting the configuration again
        get_result_after_delete = self.vector_client.get_bucket_logging(
            oss_vectors.models.GetBucketLoggingRequest(
                bucket=source_bucket_name
            )
        )
        self.assertEqual(200, get_result_after_delete.status_code)
        self.assertEqual('OK', get_result_after_delete.status)
        self.assertEqual(24, len(get_result_after_delete.request_id))
        self.assertEqual(24, len(get_result_after_delete.headers.get('x-oss-request-id')))
        self.assertIsNotNone(get_result_after_delete.bucket_logging_status)
        self.assertIsNone(get_result_after_delete.bucket_logging_status.logging_enabled.target_bucket)
        self.assertIsNone(get_result_after_delete.bucket_logging_status.logging_enabled.target_prefix)
        self.assertIsNone(get_result_after_delete.bucket_logging_status.logging_enabled.logging_role)

        # 6. Delete buckets (cleanup)
        # Delete source bucket
        delete_source_result = self.vector_client.delete_vector_bucket(
            oss_vectors.models.DeleteVectorBucketRequest(
                bucket=source_bucket_name,
            )
        )
        self.assertEqual(204, delete_source_result.status_code)
        self.assertEqual(24, len(delete_source_result.request_id))
        self.assertEqual(24, len(delete_source_result.headers.get('x-oss-request-id')))

        # Delete target bucket
        delete_target_result = self.client.delete_bucket(
            oss.models.DeleteBucketRequest(
                bucket=target_bucket_name,
            )
        )
        self.assertEqual(204, delete_target_result.status_code)
        self.assertEqual(24, len(delete_target_result.request_id))
        self.assertEqual(24, len(delete_target_result.headers.get('x-oss-request-id')))

