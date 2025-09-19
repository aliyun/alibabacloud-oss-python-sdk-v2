# pylint: skip-file
import alibabacloud_oss_v2.vectors as oss_vectors
from tests.integration import TestIntegrationVectors, random_short_bucket_name


class TestVectorIndex(TestIntegrationVectors):
    """Integration tests for Vector Index operations (using Put/Get/List/DeleteVectorIndex operations)."""

    def test_vector_index_lifecycle(self):
        """Test the full lifecycle of a vector index: create (put), get, list, and delete."""
        # 1. Create bucket for testing
        bucket_name = random_short_bucket_name()
        create_bucket_result = self.vector_client.put_vector_bucket(
            oss_vectors.models.PutVectorBucketRequest(
                bucket=bucket_name,
            )
        )
        self.assertEqual(200, create_bucket_result.status_code)
        self.assertEqual('OK', create_bucket_result.status)
        self.assertEqual(24, len(create_bucket_result.request_id))
        self.assertEqual(24, len(create_bucket_result.headers.get('x-oss-request-id')))

        # 2. Put (Create) a vector index
        index_name = 'testIndexForIntegration'
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

        # Assert successful creation
        self.assertEqual(200, put_result.status_code)
        self.assertEqual('OK', put_result.status)
        self.assertEqual(24, len(put_result.request_id))
        self.assertEqual(24, len(put_result.headers.get('x-oss-request-id')))

        # 3. Get the created vector index
        get_index_request = oss_vectors.models.GetVectorIndexRequest(
            bucket=bucket_name,
            index_name=index_name
        )

        get_result = self.vector_client.get_vector_index(get_index_request)

        # Assert successful retrieval
        self.assertEqual(200, get_result.status_code)
        self.assertEqual('OK', get_result.status)
        self.assertEqual(24, len(get_result.request_id))
        self.assertEqual(24, len(get_result.headers.get('x-oss-request-id')))

        # Assert retrieved index details match the created ones
        self.assertIsNotNone(get_result.index)
        self.assertEqual(index_name, get_result.index.get('indexName'))
        self.assertEqual(dimension, get_result.index.get('dimension'))
        self.assertEqual(distance_metric, get_result.index.get('distanceMetric'))

        # 4. List vector indexes and verify our index is included
        list_indexes_request = oss_vectors.models.ListVectorIndexesRequest(
            bucket=bucket_name
        )

        list_result = self.vector_client.list_vector_indexes(list_indexes_request)

        # Assert successful listing
        self.assertEqual(200, list_result.status_code)
        self.assertEqual('OK', list_result.status)
        self.assertEqual(24, len(list_result.request_id))
        self.assertEqual(24, len(list_result.headers.get('x-oss-request-id')))
        self.assertIsNotNone(list_result.indexes)
        self.assertEqual(len(list_result.indexes), 1)

        # Find our specific index in the list
        found_index = None
        for index in list_result.indexes:
            if index.get('indexName') == index_name:
                found_index = index
                break

        self.assertIsNotNone(found_index, f"Index '{index_name}' not found in the list")
        self.assertEqual(dimension, found_index.get('dimension'))
        self.assertEqual(distance_metric, found_index.get('distanceMetric'))

        # 5. Delete the vector index
        delete_index_request = oss_vectors.models.DeleteVectorIndexRequest(
            bucket=bucket_name,
            index_name=index_name
        )

        delete_result = self.vector_client.delete_vector_index(delete_index_request)

        # Assert successful deletion (Delete operations often return 204 No Content)
        self.assertEqual(204, delete_result.status_code)
        self.assertEqual(24, len(delete_result.request_id))
        self.assertEqual(24, len(delete_result.headers.get('x-oss-request-id')))

        # 6. Cleanup: Delete the test bucket
        delete_bucket_result = self.vector_client.delete_vector_bucket(
            oss_vectors.models.DeleteVectorBucketRequest(
                bucket=bucket_name,
            )
        )
        self.assertEqual(204, delete_bucket_result.status_code)
        self.assertEqual(24, len(delete_bucket_result.request_id))
        self.assertEqual(24, len(delete_bucket_result.headers.get('x-oss-request-id')))
