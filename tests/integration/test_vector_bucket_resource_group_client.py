# pylint: skip-file

import alibabacloud_oss_v2.models as oss
import alibabacloud_oss_v2.vectors as oss_vectors
from . import TestIntegrationVectors, random_bucket_name


class TestVectorBucketResourceGroup(TestIntegrationVectors):

    def test_vector_bucket_resource_group(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.vector_client.put_vector_bucket(oss_vectors.models.PutVectorBucketRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket resource group
        resource_group_id = 'rg-acfmy7mo47b3ad5****'
        result = self.vector_client.put_bucket_resource_group(oss_vectors.models.PutBucketResourceGroupRequest(
            bucket=bucket_name,
            bucket_resource_group_configuration=oss_vectors.models.BucketResourceGroupConfiguration(
                resource_group_id=resource_group_id,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket resource group
        result = self.vector_client.get_bucket_resource_group(oss_vectors.models.GetBucketResourceGroupRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(resource_group_id, result.bucket_resource_group_configuration.resource_group_id)

        # delete bucket (cleanup)
        result = self.vector_client.delete_vector_bucket(oss_vectors.models.DeleteVectorBucketRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
