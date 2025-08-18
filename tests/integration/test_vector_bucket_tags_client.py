# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketTags(TestIntegration):

    def test_bucket_tags(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.vector_client.put_vector_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket tags
        result = self.vector_client.put_bucket_tags(oss.PutBucketTagsRequest(
            bucket=bucket_name,
            tagging=oss.Tagging(
                tag_set=oss.TagSet(
                    tags=[oss.Tag(
                        key='test_key',
                        value='test_value',
                    ), oss.Tag(
                        key='test_key2',
                        value='test_value2',
                    )],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket tags
        result = self.vector_client.get_bucket_tags(oss.GetBucketTagsRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('test_key', result.tagging.tag_set.tags[0].key)
        self.assertEqual('test_value', result.tagging.tag_set.tags[0].value)
        self.assertEqual('test_key2', result.tagging.tag_set.tags[1].key)
        self.assertEqual('test_value2', result.tagging.tag_set.tags[1].value)

        # delete bucket tags
        result = self.vector_client.delete_bucket_tags(oss.DeleteBucketTagsRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

