# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.vectors.operations import _serde
from alibabacloud_oss_v2.vectors.models import vector_basic as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from tests.unit import MockHttpResponse


class TestPutVectors(unittest.TestCase):
    def test_constructor_request(self):
        """
        Test PutVectorsRequest constructor
        """
        request = model.PutVectorsRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.index_name)
        self.assertIsNone(request.vectors)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        """
        Test PutVectorsRequest serialization
        """
        vectors = [
            {
                "data": {"float32": [0.1, 0.2, 0.3]},
                "key": "vector-key-1",
                "metadata": {"key1": "value1", "key2": "value2"}
            }
        ]

        request = model.PutVectorsRequest(
            bucket='test-bucket',
            index_name='test-index',
            vectors=vectors
        )

        json_str = '{"indexName": "test-index", "vectors": [{"data": {"float32": [0.1, 0.2, 0.3]}, "key": "vector-key-1", "metadata": {"key1": "value1", "key2": "value2"}}]}'

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='PutVectors',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'PutVectors')
        self.assertEqual(op_input.method, 'POST')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.vectors, vectors)
        self.assertIsInstance(request, serde.RequestModel)
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        """
        Test PutVectorsResult constructor
        """
        result = model.PutVectorsResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        """
        Test PutVectorsResult deserialization
        """
        json_data = None
        result = model.PutVectorsResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=json_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))


class TestGetVectors(unittest.TestCase):
    def test_constructor_request(self):
        """
        Test GetVectorsRequest constructor
        """
        request = model.GetVectorsRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.index_name)
        self.assertIsNone(request.keys)
        self.assertIsNone(request.return_data)
        self.assertIsNone(request.return_metadata)
        self.assertIsInstance(request, serde.RequestModel)

    def test_constructor_request_with_parameters(self):
        """
        Test GetVectorsRequest constructor with parameters
        """
        request = model.GetVectorsRequest(
            bucket='test-bucket',
            index_name='test-index',
            keys=['key1', 'key2'],
            return_data=True,
            return_metadata=False
        )
        self.assertEqual(request.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.keys, ['key1', 'key2'])
        self.assertEqual(request.return_data, True)
        self.assertEqual(request.return_metadata, False)
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        """
        Test GetVectorsRequest serialization
        """
        request = model.GetVectorsRequest(
            bucket='test-bucket',
            index_name='test-index',
            keys=['key1', 'key2'],
            return_data=True,
            return_metadata=False
        )

        json_str = '{"indexName": "test-index", "keys": ["key1", "key2"], "returnData": true, "returnMetadata": false}'

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='GetVectors',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'GetVectors')
        self.assertEqual(op_input.method, 'POST')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.keys, ['key1', 'key2'])
        self.assertEqual(request.return_data, True)
        self.assertEqual(request.return_metadata, False)
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        """
        Test GetVectorsResult constructor
        """
        result = model.GetVectorsResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        """
        Test GetVectorsResult deserialization
        """
        json_data = '''
        {
           "vectors": [
              {
                 "data": {
                    "float32": [0.1, 0.2, 0.3]
                 },
                 "key": "vector-key-1",
                 "metadata": {
                    "key1": "value1",
                    "key2": "value2"
                 }
              }
           ]
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.GetVectorsResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.vectors)
        self.assertEqual(len(result.vectors), 1)
        self.assertEqual(result.vectors[0].get('key'), 'vector-key-1')
        self.assertEqual(result.vectors[0].get('data').get('float32'), [0.1, 0.2, 0.3])
        self.assertIsNotNone(result.vectors[0].get('metadata'))
        self.assertEqual(result.vectors[0].get('metadata').get('key1'), 'value1')
        self.assertEqual(result.vectors[0].get('metadata').get('key2'), 'value2')


class TestListVectors(unittest.TestCase):
    def test_constructor_request(self):
        """
        Test ListVectorsRequest constructor
        """
        request = model.ListVectorsRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.index_name)
        self.assertIsNone(request.max_results)
        self.assertIsNone(request.next_token)
        self.assertIsNone(request.return_data)
        self.assertIsNone(request.return_metadata)
        self.assertIsNone(request.segment_count)
        self.assertIsNone(request.segment_index)
        self.assertIsInstance(request, serde.RequestModel)

    def test_constructor_request_with_parameters(self):
        """
        Test ListVectorsRequest constructor with parameters
        """
        request = model.ListVectorsRequest(
            bucket='test-bucket',
            index_name='test-index',
            max_results=100,
            next_token='test-token',
            return_data=True,
            return_metadata=False,
            segment_count=5,
            segment_index=2
        )
        self.assertEqual(request.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.max_results, 100)
        self.assertEqual(request.next_token, 'test-token')
        self.assertEqual(request.return_data, True)
        self.assertEqual(request.return_metadata, False)
        self.assertEqual(request.segment_count, 5)
        self.assertEqual(request.segment_index, 2)
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        """
        Test ListVectorsRequest serialization
        """
        request = model.ListVectorsRequest(
            bucket='test-bucket',
            index_name='test-index',
            max_results=100,
            next_token='test-token',
            return_data=True,
            return_metadata=False,
            segment_count=5,
            segment_index=2
        )

        json_str = '{"indexName": "test-index", "maxResults": 100, "nextToken": "test-token", "returnData": true, "returnMetadata": false, "segmentCount": 5, "segmentIndex": 2}'

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='ListVectors',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'ListVectors')
        self.assertEqual(op_input.method, 'POST')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.max_results, 100)
        self.assertEqual(request.next_token, 'test-token')
        self.assertEqual(request.return_data, True)
        self.assertEqual(request.return_metadata, False)
        self.assertEqual(request.segment_count, 5)
        self.assertEqual(request.segment_index, 2)
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        """
        Test ListVectorsResult constructor
        """
        result = model.ListVectorsResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        """
        Test ListVectorsResult deserialization
        """
        json_data = '''
        {
            "nextToken": "next-token",
            "vectors": [
                {
                    "data": {
                        "float32": [0.1, 0.2, 0.3]
                    },
                    "key": "vector-key-1",
                    "metadata": {
                        "key1": "value1",
                        "key2": "value2"
                    }
                }
            ]
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.ListVectorsResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.next_token, 'next-token')
        self.assertIsNotNone(result.vectors)
        self.assertEqual(len(result.vectors), 1)
        self.assertEqual(result.vectors[0].get('key'), 'vector-key-1')
        self.assertEqual(result.vectors[0].get('data').get('float32'), [0.1, 0.2, 0.3])
        self.assertIsNotNone(result.vectors[0].get('metadata'))
        self.assertEqual(result.vectors[0].get('metadata').get('key1'), 'value1')
        self.assertEqual(result.vectors[0].get('metadata').get('key2'), 'value2')


class TestDeleteVectors(unittest.TestCase):
    def test_constructor_request(self):
        """
        Test DeleteVectorsRequest constructor
        """
        request = model.DeleteVectorsRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.index_name)
        self.assertIsNone(request.keys)
        self.assertIsInstance(request, serde.RequestModel)

    def test_constructor_request_with_parameters(self):
        """
        Test DeleteVectorsRequest constructor with parameters
        """
        request = model.DeleteVectorsRequest(
            bucket='test-bucket',
            index_name='test-index',
            keys=['key1', 'key2', 'key3']
        )
        self.assertEqual(request.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.keys, ['key1', 'key2', 'key3'])
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        """
        Test DeleteVectorsRequest serialization
        """
        request = model.DeleteVectorsRequest(
            bucket='test-bucket',
            index_name='test-index',
            keys=['key1', 'key2', 'key3']
        )

        json_str = '{"indexName": "test-index", "keys": ["key1", "key2", "key3"]}'

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='DeleteVectors',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'DeleteVectors')
        self.assertEqual(op_input.method, 'POST')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.keys, ['key1', 'key2', 'key3'])
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        """
        Test DeleteVectorsResult constructor
        """
        result = model.DeleteVectorsResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        """
        Test DeleteVectorsResult deserialization
        """
        json_data = None
        result = model.DeleteVectorsResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=json_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))


class TestQueryVectors(unittest.TestCase):
    def test_constructor_request(self):
        """
        Test QueryVectorsRequest constructor
        """
        request = model.QueryVectorsRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.filter)
        self.assertIsNone(request.index_name)
        self.assertIsNone(request.query_vector)
        self.assertIsNone(request.return_distance)
        self.assertIsNone(request.return_metadata)
        self.assertIsNone(request.top_k)
        self.assertIsInstance(request, serde.RequestModel)

    def test_constructor_request_with_parameters(self):
        """
        Test QueryVectorsRequest constructor with parameters
        """
        query_filter = {
            "$and": [{
                "type": {
                    "$in": ["comedy", "documentary"]
                }
            }, {
                "year": {
                    "$gte": 2020
                }
            }]
        }

        query_vector = {"float32": [0.1, 0.2, 0.3]}

        request = model.QueryVectorsRequest(
            bucket='test-bucket',
            filter=query_filter,
            index_name='test-index',
            query_vector=query_vector,
            return_distance=True,
            return_metadata=False,
            top_k=10
        )
        self.assertEqual(request.bucket, 'test-bucket')
        self.assertEqual(request.filter, query_filter)
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.query_vector, query_vector)
        self.assertEqual(request.return_distance, True)
        self.assertEqual(request.return_metadata, False)
        self.assertEqual(request.top_k, 10)
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        """
        Test QueryVectorsRequest serialization
        """
        query_filter = {
            "$and": [{
                "type": {
                    "$in": ["comedy", "documentary"]
                }
            }, {
                "year": {
                    "$gte": 2020
                }
            }]
        }

        query_vector = {"float32": [0.1, 0.2, 0.3]}

        request = model.QueryVectorsRequest(
            bucket='test-bucket',
            filter=query_filter,
            index_name='test-index',
            query_vector=query_vector,
            return_distance=True,
            return_metadata=False,
            top_k=10
        )

        json_str = '{"filter": {"$and": [{"type": {"$in": ["comedy", "documentary"]}}, {"year": {"$gte": 2020}}]}, "indexName": "test-index", "queryVector": {"float32": [0.1, 0.2, 0.3]}, "returnDistance": true, "returnMetadata": false, "topK": 10}'

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectors',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'QueryVectors')
        self.assertEqual(op_input.method, 'POST')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.filter, query_filter)
        self.assertEqual(request.query_vector, query_vector)
        self.assertEqual(request.return_distance, True)
        self.assertEqual(request.return_metadata, False)
        self.assertEqual(request.top_k, 10)
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        """
        Test QueryVectorsResult constructor
        """
        result = model.QueryVectorsResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        """
        Test QueryVectorsResult deserialization
        """
        json_data = '''
        {
           "vectors": [
              {
                 "data": {
                    "float32": [0.1, 0.2, 0.3]
                 },
                 "distance": 0.5,
                 "key": "vector-key-1",
                 "metadata": {
                    "key1": "value1",
                    "key2": "value2"
                 }
              }
           ]
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.QueryVectorsResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.vectors)
        self.assertEqual(len(result.vectors), 1)
        self.assertEqual(result.vectors[0].get('key'), 'vector-key-1')
        self.assertEqual(result.vectors[0].get('distance'), 0.5)
        self.assertEqual(result.vectors[0].get('data').get('float32'), [0.1, 0.2, 0.3])
        self.assertIsNotNone(result.vectors[0].get('metadata'))
        self.assertEqual(result.vectors[0].get('metadata').get('key1'), 'value1')
        self.assertEqual(result.vectors[0].get('metadata').get('key2'), 'value2')
