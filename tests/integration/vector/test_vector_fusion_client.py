# pylint: skip-file
import time
import alibabacloud_oss_v2.vectors as oss_vectors
from .. import TestIntegrationVectors, random_vector_bucket_name


class TestVectorFusion(TestIntegrationVectors):
    """Integration tests for fusion vector query operations."""

    def test_query_vectors_fusion(self):
        bucket_name = random_vector_bucket_name()
        index_name = 'testFusionQueryForIntegration'
        vector_key = 'fusion-vector-key-1'
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

        result = self.vector_client.put_vector_index_fusion(
            oss_vectors.models.PutVectorIndexFusionRequest(
                bucket=bucket_name,
                index_name=index_name,
                schema_configuration=schema_configuration
            )
        )
        self.assertEqual(200, result.status_code)

        result = self.vector_client.put_vectors(
            oss_vectors.models.PutVectorsRequest(
                bucket=bucket_name,
                index_name=index_name,
                vectors=[{
                    'key': vector_key,
                    'data': {
                        'text_vector': [0.1, 0.2, 0.3, 0.4],
                        'image_vector': [0.4, 0.3, 0.2, 0.1]
                    },
                    'metadata': {'category': 'storage'}
                }]
            )
        )
        self.assertEqual(200, result.status_code)

        query_result = None
        for _ in range(12):
            query_result = self.vector_client.query_vectors_fusion(
                oss_vectors.models.QueryVectorsFusionRequest(
                    bucket=bucket_name,
                    index_name=index_name,
                    knn={
                        'field': 'text_vector',
                        'queryVector': [0.1, 0.2, 0.3, 0.4],
                        'topK': 10,
                        'numCandidates': 100
                    },
                    limit=10,
                    return_metadata=True
                )
            )
            if query_result.vectors and any(
                    vector.get('key') == vector_key for vector in query_result.vectors):
                break
            time.sleep(5)

        self.assertEqual(200, query_result.status_code)
        self.assertEqual('OK', query_result.status)
        self.assertEqual(24, len(query_result.request_id))
        self.assertEqual(24, len(query_result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(query_result.vectors)
        vector = next(
            (item for item in query_result.vectors if item.get('key') == vector_key),
            None
        )
        self.assertIsNotNone(vector)
        self.assertIsNotNone(vector.get('score'))
        self.assertEqual('storage', vector.get('metadata', {}).get('category'))

        result = self.vector_client.delete_vectors(
            oss_vectors.models.DeleteVectorsRequest(
                bucket=bucket_name,
                index_name=index_name,
                keys=[vector_key]
            )
        )
        self.assertEqual(204, result.status_code)

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
