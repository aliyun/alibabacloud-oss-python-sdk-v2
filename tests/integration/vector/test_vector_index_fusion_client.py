# pylint: skip-file
import alibabacloud_oss_v2.vectors as oss_vectors
from .. import TestIntegrationVectors, random_vector_bucket_name


class TestVectorIndexFusion(TestIntegrationVectors):
    """Integration tests for fusion vector index operations."""

    def test_put_vector_index_fusion_lifecycle(self):
        bucket_name = random_vector_bucket_name()
        index_name = 'testFusionIndexForIntegration'
        schema_configuration = {
            'fields': [
                {
                    'name': 'text_vector',
                    'type': 'vector',
                    'dataType': 'float32',
                    'dimension': 4,
                    'distanceMetric': 'cosine'
                },
                {
                    'name': 'image_vector',
                    'type': 'vector',
                    'dataType': 'float32',
                    'dimension': 4,
                    'distanceMetric': 'cosine'
                }
            ]
        }

        result = self.vector_client.put_vector_bucket(
            oss_vectors.models.PutVectorBucketRequest(bucket=bucket_name)
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual(24, len(result.request_id))

        result = self.vector_client.put_vector_index_fusion(
            oss_vectors.models.PutVectorIndexFusionRequest(
                bucket=bucket_name,
                index_name=index_name,
                schema_configuration=schema_configuration
            )
        )
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        result = self.vector_client.get_vector_index(
            oss_vectors.models.GetVectorIndexRequest(
                bucket=bucket_name,
                index_name=index_name
            )
        )
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.index)
        self.assertEqual(index_name, result.index.get('indexName'))

        result = self.vector_client.list_vector_indexes(
            oss_vectors.models.ListVectorIndexesRequest(bucket=bucket_name)
        )
        self.assertEqual(200, result.status_code)
        self.assertTrue(any(index.get('indexName') == index_name for index in result.indexes))

        result = self.vector_client.delete_vector_index(
            oss_vectors.models.DeleteVectorIndexRequest(
                bucket=bucket_name,
                index_name=index_name
            )
        )
        self.assertEqual(204, result.status_code)

        result = self.vector_client.delete_vector_bucket(
            oss_vectors.models.DeleteVectorBucketRequest(bucket=bucket_name)
        )
        self.assertEqual(204, result.status_code)
