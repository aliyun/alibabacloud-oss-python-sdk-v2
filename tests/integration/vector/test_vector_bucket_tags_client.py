# pylint: skip-file

import alibabacloud_oss_v2.vectors as oss_vectors
from tests.integration import TestIntegrationVectors, random_bucket_name


class TestVectorBucketTags(TestIntegrationVectors):
    """Integration tests for Vector Bucket Tags operations."""

    def test_vector_bucket_tags(self):
        """Test put, get, and delete bucket tags operations."""
        # 1. Create bucket
        bucket_name = random_bucket_name()
        result = self.vector_client.put_vector_bucket(
            oss_vectors.models.PutVectorBucketRequest(
                bucket=bucket_name,
            )
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # 2. Put bucket tags
        tag1 = oss_vectors.models.Tag(
            key='key1',
            value='value1'
        )
        tag2 = oss_vectors.models.Tag(
            key='key2',
            value='value2'
        )
        tags = [tag1, tag2]

        put_result = self.vector_client.put_bucket_tags(
            oss_vectors.models.PutBucketTagsRequest(
                bucket=bucket_name,
                tagging=oss_vectors.models.Tagging(
                    tag_set=oss_vectors.models.TagSet(
                        tags=tags
                    )
                )
            )
        )
        self.assertEqual(200, put_result.status_code)
        self.assertEqual('OK', put_result.status)
        self.assertEqual(24, len(put_result.request_id))
        self.assertEqual(24, len(put_result.headers.get('x-oss-request-id')))

        # 3. Get bucket tags
        get_result = self.vector_client.get_bucket_tags(
            oss_vectors.models.GetBucketTagsRequest(
                bucket=bucket_name
            )
        )
        self.assertEqual(200, get_result.status_code)
        self.assertEqual('OK', get_result.status)
        self.assertEqual(24, len(get_result.request_id))
        self.assertEqual(24, len(get_result.headers.get('x-oss-request-id')))
        # Verify the tags retrieved match the ones set
        self.assertIsNotNone(get_result.tagging)
        self.assertIsNotNone(get_result.tagging.tag_set)
        self.assertEqual(2, len(get_result.tagging.tag_set.tags))
        # Check if tags are present (order might not be guaranteed)
        returned_tags = {(tag.key, tag.value) for tag in get_result.tagging.tag_set.tags}
        expected_tags = {('key1', 'value1'), ('key2', 'value2')}
        self.assertEqual(expected_tags, returned_tags)

        # 4. Delete bucket tags
        delete_result = self.vector_client.delete_bucket_tags(
            oss_vectors.models.DeleteBucketTagsRequest(
                bucket=bucket_name
            )
        )
        self.assertEqual(204, delete_result.status_code) # Delete typically returns 204 No Content
        self.assertEqual(24, len(delete_result.request_id))
        self.assertEqual(24, len(delete_result.headers.get('x-oss-request-id')))

        # 5. Verify tags are deleted by attempting to get them again
        get_result_after_delete = self.vector_client.get_bucket_tags(
            oss_vectors.models.GetBucketTagsRequest(
                bucket=bucket_name
            )
        )
        # According to OSS API, getting tags on a bucket with no tags might return 200 with empty TagSet
        # or potentially 404 depending on implementation details. Check for empty TagSet here.
        self.assertEqual(200, get_result_after_delete.status_code)
        self.assertEqual('OK', get_result_after_delete.status)
        self.assertEqual(24, len(get_result_after_delete.request_id))
        self.assertEqual(24, len(get_result_after_delete.headers.get('x-oss-request-id')))
        # Verify the tag set is now empty or None
        # The exact behavior depends on the service, but typically TagSet would be present but empty.
        self.assertIsNotNone(get_result_after_delete.tagging)
        self.assertIsNotNone(get_result_after_delete.tagging.tag_set)
        self.assertEqual(0, len(get_result_after_delete.tagging.tag_set.tags))


        # 6. Delete bucket (cleanup)
        delete_bucket_result = self.vector_client.delete_vector_bucket(
            oss_vectors.models.DeleteVectorBucketRequest(
                bucket=bucket_name,
            )
        )
        self.assertEqual(204, delete_bucket_result.status_code)
        self.assertEqual(24, len(delete_bucket_result.request_id))
        self.assertEqual(24, len(delete_bucket_result.headers.get('x-oss-request-id')))

