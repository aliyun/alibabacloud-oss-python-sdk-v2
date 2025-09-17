# pylint: skip-file

from ast import literal_eval
import alibabacloud_oss_v2.vectors as oss_vectors
from tests.integration import TestIntegrationVectors, random_short_bucket_name


class TestVectorBasic(TestIntegrationVectors):
    """Integration tests for basic Vector operations."""

    def test_vector_basic(self):
        """Test put, get, list, delete and query vector operations."""
        # 1. Create bucket
        bucket_name = random_short_bucket_name()
        vector_key = "vector-key-1"

        result = self.vector_client.put_vector_bucket(oss_vectors.models.PutVectorBucketRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # 2. Create index (required for vector operations)
        index_name = 'testIndexForIntegrationVector'
        dimension = 3
        distance_metric = 'cosine'
        data_type = 'float32'
        metadata = {"nonFilterableMetadataKeys": ["key1", "key2"]}

        put_index_request = oss_vectors.models.PutVectorIndexRequest(
            bucket=bucket_name,
            data_type=data_type,
            dimension=dimension,
            distance_metric=distance_metric,
            index_name=index_name,
            metadata=metadata
        )

        put_result = self.vector_client.put_vector_index(put_index_request)
        self.assertEqual(200, put_result.status_code)
        self.assertEqual('OK', put_result.status)
        self.assertEqual(24, len(put_result.request_id))
        self.assertEqual(24, len(put_result.headers.get('x-oss-request-id')))

        # 3. Put vectors
        vectors_to_put = [
            {
                "data": {"float32": [0.1, 0.2, 0.3]},
                "key": vector_key,
                "metadata": {"key1": "value1", "key2": "value2"}
            }
        ]

        put_result = self.vector_client.put_vectors(oss_vectors.models.PutVectorsRequest(
            bucket=bucket_name,
            index_name=index_name,
            vectors=vectors_to_put
        ))
        self.assertEqual(200, put_result.status_code)
        self.assertEqual('OK', put_result.status)
        self.assertEqual(24, len(put_result.request_id))
        self.assertEqual(24, len(put_result.headers.get('x-oss-request-id')))

        # 4. Get vectors
        get_result = self.vector_client.get_vectors(oss_vectors.models.GetVectorsRequest(
            bucket=bucket_name,
            index_name=index_name,
            keys=[vector_key],
            return_data=True,
            return_metadata=True
        ))
        self.assertEqual(200, get_result.status_code)
        self.assertEqual('OK', get_result.status)
        self.assertEqual(24, len(get_result.request_id))
        self.assertEqual(24, len(get_result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(get_result.vectors)
        self.assertEqual(1, len(get_result.vectors))
        self.assertEqual(vector_key, get_result.vectors[0].get('key'))
        self.assertIsNotNone(get_result.vectors[0].get('data'))
        self.assertIsNotNone(get_result.vectors[0].get('metadata'))
        self.assertEqual(literal_eval('{"key1": "value1", "key2": "value2"}'), get_result.vectors[0].get('metadata'))

        # 5. List vectors
        list_result = self.vector_client.list_vectors(oss_vectors.models.ListVectorsRequest(
            bucket=bucket_name,
            index_name=index_name,
            max_results=100,
            return_data=True,
            return_metadata=True,
            segment_count=2,
            segment_index=1
        ))
        self.assertEqual(200, list_result.status_code)
        self.assertEqual('OK', list_result.status)
        self.assertEqual(24, len(list_result.request_id))
        self.assertEqual(24, len(list_result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(list_result.vectors)
        # Check that we have at least one vector in the list
        self.assertGreaterEqual(len(list_result.vectors), 0)
        self.assertEqual(vector_key, list_result.vectors[0].get('key'))
        self.assertIsNotNone(list_result.vectors[0].get('data'))
        self.assertIsNotNone(list_result.vectors[0].get('metadata'))
        self.assertEqual(literal_eval('{"key1": "value1", "key2": "value2"}'), list_result.vectors[0].get('metadata'))


        # 6. Query vectors
        query_filter = {
            "$and": [{
                "type": {
                    "$nin": ["comedy", "documentary"]
                }
            }]
        }
        query_vector = {"float32": [0.1, 0.2, 0.3]}
        query_result = self.vector_client.query_vectors(oss_vectors.models.QueryVectorsRequest(
            bucket=bucket_name,
            index_name=index_name,
            query_vector=query_vector,
            filter=query_filter,
            return_distance=True,
            return_metadata=True,
            top_k=10
        ))
        self.assertEqual(200, query_result.status_code)
        self.assertEqual('OK', query_result.status)
        self.assertEqual(24, len(query_result.request_id))
        self.assertEqual(24, len(query_result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(query_result)


        # 7. Delete vectors
        delete_result = self.vector_client.delete_vectors(oss_vectors.models.DeleteVectorsRequest(
            bucket=bucket_name,
            index_name=index_name,
            keys=[vector_key]
        ))
        self.assertEqual(204, delete_result.status_code)
        self.assertEqual(24, len(delete_result.request_id))
        self.assertEqual(24, len(delete_result.headers.get('x-oss-request-id')))

        # 8. Get index to verify it exists
        get_index_result = self.vector_client.get_vector_index(oss_vectors.models.GetVectorIndexRequest(
            bucket=bucket_name,
            index_name=index_name
        ))
        self.assertEqual(200, get_index_result.status_code)
        self.assertEqual('OK', get_index_result.status)
        self.assertEqual(24, len(get_index_result.request_id))
        self.assertEqual(24, len(get_index_result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(get_index_result.index)
        self.assertEqual(index_name, get_index_result.index.get('indexName'))

        # 9. List indexes
        list_index_result = self.vector_client.list_vector_indexes(oss_vectors.models.ListVectorIndexesRequest(
            bucket=bucket_name
        ))
        self.assertEqual(200, list_index_result.status_code)
        self.assertEqual('OK', list_index_result.status)
        self.assertEqual(24, len(list_index_result.request_id))
        self.assertEqual(24, len(list_index_result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(list_index_result.indexes)
        # Check that we have at least one index in the list
        self.assertEqual(len(list_index_result.indexes), 1)

        # Verify our index is in the list
        found_index = None
        for index in list_index_result.indexes:
            if index.get('indexName') == index_name:
                found_index = index
                break
        self.assertIsNotNone(found_index)
        self.assertEqual(index_name, found_index.get('indexName'))
        self.assertEqual(dimension, found_index.get('dimension'))

        # 10. Delete index (cleanup)
        delete_index_result = self.vector_client.delete_vector_index(oss_vectors.models.DeleteVectorIndexRequest(
            bucket=bucket_name,
            index_name=index_name
        ))
        self.assertEqual(204, delete_index_result.status_code)
        self.assertEqual(24, len(delete_index_result.request_id))
        self.assertEqual(24, len(delete_index_result.headers.get('x-oss-request-id')))

        # 11. Delete bucket (cleanup)
        result = self.vector_client.delete_vector_bucket(oss_vectors.models.DeleteVectorBucketRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
