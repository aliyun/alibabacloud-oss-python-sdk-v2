# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.vectors.operations import _serde
from alibabacloud_oss_v2.vectors.models import index_basic as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from ... import MockHttpResponse


class TestPutVectorIndex(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutVectorIndexRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.data_type)
        self.assertIsNone(request.dimension)
        self.assertIsNone(request.distance_metric)
        self.assertIsNone(request.index_name)
        self.assertIsNone(request.metadata)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        metadata = {"nonFilterableMetadataKeys": ["key1", "key2"]}
        request = model.PutVectorIndexRequest(
            bucket='test-bucket',
            data_type='vector',
            dimension=128,
            distance_metric='EUCLIDEAN',
            index_name='test-index',
            metadata=metadata
        )
        json_str = '{"dataType": "vector", "dimension": 128, "distanceMetric": "EUCLIDEAN", "indexName": "test-index", "metadata": {"nonFilterableMetadataKeys": ["key1", "key2"]}}'

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='PutVectorIndex',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'PutVectorIndex')
        self.assertEqual(op_input.method, 'POST')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(request.data_type, 'vector')
        self.assertEqual(request.dimension, 128)
        self.assertEqual(request.distance_metric, 'EUCLIDEAN')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(request.metadata, metadata)
        self.assertIsInstance(request, serde.RequestModel)
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        result = model.PutVectorIndexResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = None
        result = model.PutVectorIndexResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
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
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))



class TestGetVectorIndex(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetVectorIndexRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.index_name)
        self.assertIsInstance(request, serde.RequestModel)

    def test_constructor_request_with_parameters(self):
        request = model.GetVectorIndexRequest(
            bucket='test-bucket',
            index_name='test-index'
        )
        self.assertEqual(request.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        request = model.GetVectorIndexRequest(
            bucket='test-bucket',
            index_name='test-index'
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='GetVectorIndex',
            method='GET',
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'GetVectorIndex')
        self.assertEqual(op_input.method, 'GET')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')

    def test_constructor_result(self):
        result = model.GetVectorIndexResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = '''
        {
           "index": { 
              "createTime": "2023-12-17T00:20:57.000Z",
              "dataType": "vector",
              "dimension": 128,
              "distanceMetric": "EUCLIDEAN",
              "indexName": "test-index",
              "metadata": { 
                 "nonFilterableMetadataKeys": ["key1", "key2"]
              },
              "status": "Active",
              "vectorBucketName": "test-bucket"
           }
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.GetVectorIndexResult()

        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.index.get('createTime'), '2023-12-17T00:20:57.000Z')
        self.assertEqual(result.index.get('dataType'), 'vector')
        self.assertEqual(result.index.get('dimension'), 128)
        self.assertEqual(result.index.get('distanceMetric'), 'EUCLIDEAN')
        self.assertEqual(result.index.get('indexName'), 'test-index')
        self.assertEqual(result.index.get('status'), 'Active')
        self.assertEqual(result.index.get('vectorBucketName'), 'test-bucket')
        self.assertEqual(result.index.get('metadata').get('nonFilterableMetadataKeys'), ['key1', 'key2'])


class TestDeleteVectorIndex(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteVectorIndexRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.index_name)
        self.assertIsInstance(request, serde.RequestModel)

    def test_constructor_request_with_parameters(self):
        request = model.DeleteVectorIndexRequest(
            bucket='test-bucket',
            index_name='test-index'
        )
        self.assertEqual(request.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        request = model.DeleteVectorIndexRequest(
            bucket='test-bucket',
            index_name='test-index'
        )

        json_str = '{"indexName": "test-index"}'

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='DeleteVectorIndex',
            method='DELETE',
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'DeleteVectorIndex')
        self.assertEqual(op_input.method, 'DELETE')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-index')
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        result = model.DeleteVectorIndexResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = None
        result = model.DeleteVectorIndexResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
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
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))



class TestListVectorsIndex(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListVectorIndexesRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.max_results)
        self.assertIsNone(request.next_token)
        self.assertIsNone(request.prefix)
        self.assertIsInstance(request, serde.RequestModel)

    def test_constructor_request_with_parameters(self):
        request = model.ListVectorIndexesRequest(
            bucket='test-bucket',
            max_results=100,
            next_token='test-token',
            prefix='test-'
        )
        self.assertEqual(request.bucket, 'test-bucket')
        self.assertEqual(request.max_results, 100)
        self.assertEqual(request.next_token, 'test-token')
        self.assertEqual(request.prefix, 'test-')
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        request = model.ListVectorIndexesRequest(
            bucket='test-bucket',
            max_results=100,
            next_token='test-token',
            prefix='test-'
        )

        json_str = '{"maxResults": 100, "nextToken": "test-token", "prefix": "test-"}'


        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='ListVectorsIndex',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'ListVectorsIndex')
        self.assertEqual(op_input.method, 'POST')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(request.max_results, 100)
        self.assertEqual(request.next_token, 'test-token')
        self.assertEqual(request.prefix, 'test-')
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        result = model.ListVectorIndexesResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = '''
        {
            "indexes": [
                {
                    "createTime": "2023-12-17T00:20:57.000Z",
                    "indexName": "test-index1",
                    "dataType": "vector",
                    "dimension": 128,
                    "distanceMetric": "EUCLIDEAN",
                    "metadata": {
                        "nonFilterableMetadataKeys": ["key1", "key2"]
                    },
                    "vectorBucketName": "test-bucket",
                    "status": "Active"
                }
            ],
            "nextToken": "next-token"
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.ListVectorIndexesResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.next_token, 'next-token')
        self.assertIsNotNone(result.indexes)
        self.assertEqual(len(result.indexes), 1)
        self.assertEqual(result.indexes[0].get('createTime'), '2023-12-17T00:20:57.000Z')
        self.assertEqual(result.indexes[0].get('indexName'), 'test-index1')
        self.assertEqual(result.indexes[0].get('dataType'), 'vector')
        self.assertEqual(result.indexes[0].get('dimension'), 128)
        self.assertEqual(result.indexes[0].get('distanceMetric'), 'EUCLIDEAN')
        self.assertEqual(result.indexes[0].get('vectorBucketName'), 'test-bucket')
        self.assertEqual(result.indexes[0].get('status'), 'Active')
        self.assertIsNotNone(result.indexes[0].get('metadata'))
        self.assertIn('nonFilterableMetadataKeys', result.indexes[0].get('metadata'))
        self.assertEqual(result.indexes[0].get('metadata').get('nonFilterableMetadataKeys'), ['key1', 'key2'])


class TestGetVectorIndexFusion(unittest.TestCase):
    """GetVectorIndex reads a fusion index through the very same result model.

    index is a dict, so mode and schemaConfiguration arrive without any change
    to GetVectorIndexResult. That is the compatibility extension of section
    2.3, and on the Python side it needs no new field at all.
    """

    def test_deserialize_fusion_result(self):
        json_data = '''
        {
           "index": {
              "createTime": "2023-12-17T00:20:57.000Z",
              "indexName": "test-fusion-index",
              "mode": "fusion",
              "schemaConfiguration": {
                 "fields": [
                    {
                       "name": "text_vector",
                       "type": "vector",
                       "dataType": "float32",
                       "dimension": 4,
                       "distanceMetric": "cosine"
                    },
                    {
                       "name": "image_vector",
                       "type": "vector",
                       "dataType": "float32",
                       "dimension": 2,
                       "distanceMetric": "cosine"
                    },
                    {
                       "name": "title",
                       "type": "text",
                       "exactMatch": false,
                       "text": {
                          "enabled": true,
                          "analyzer": "single_word",
                          "analyzerParameters": {"caseSensitive": false}
                       }
                    }
                 ]
              },
              "status": "Active",
              "vectorBucketName": "test-bucket"
           }
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.GetVectorIndexResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.index.get('createTime'), '2023-12-17T00:20:57.000Z')
        self.assertEqual(result.index.get('indexName'), 'test-fusion-index')
        self.assertEqual(result.index.get('mode'), 'fusion')
        self.assertEqual(result.index.get('status'), 'Active')
        self.assertEqual(result.index.get('vectorBucketName'), 'test-bucket')

        fields = result.index.get('schemaConfiguration').get('fields')
        self.assertEqual(len(fields), 3)
        self.assertEqual(fields[0].get('name'), 'text_vector')
        self.assertEqual(fields[0].get('type'), 'vector')
        self.assertEqual(fields[0].get('dataType'), 'float32')
        self.assertEqual(fields[0].get('dimension'), 4)
        self.assertEqual(fields[0].get('distanceMetric'), 'cosine')
        self.assertEqual(fields[1].get('name'), 'image_vector')
        self.assertEqual(fields[1].get('dimension'), 2)
        self.assertEqual(fields[2].get('name'), 'title')
        self.assertEqual(fields[2].get('type'), 'text')
        # an explicit false read back from the wire stays False, not None
        self.assertIs(fields[2].get('exactMatch'), False)
        self.assertIs(fields[2].get('text').get('enabled'), True)
        self.assertEqual(fields[2].get('text').get('analyzer'), 'single_word')
        self.assertIs(fields[2].get('text').get('analyzerParameters').get('caseSensitive'), False)

        # a fusion index describes its vectors inside the schema, so the top
        # level dataType, dimension and distanceMetric stay empty
        self.assertIsNone(result.index.get('dataType'))
        self.assertIsNone(result.index.get('dimension'))
        self.assertIsNone(result.index.get('distanceMetric'))

    def test_deserialize_standard_result_has_no_mode(self):
        # An older service does not return mode, and a standard index keeps
        # filling the top level dataType, dimension and distanceMetric.
        json_data = '''
        {
           "index": {
              "createTime": "2023-12-17T00:20:57.000Z",
              "dataType": "vector",
              "dimension": 128,
              "distanceMetric": "EUCLIDEAN",
              "indexName": "test-index",
              "metadata": {
                 "nonFilterableMetadataKeys": ["key1", "key2"]
              },
              "status": "Active",
              "vectorBucketName": "test-bucket"
           }
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.GetVectorIndexResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertIsNone(result.index.get('mode'))
        self.assertIsNone(result.index.get('schemaConfiguration'))
        self.assertEqual(result.index.get('dataType'), 'vector')
        self.assertEqual(result.index.get('dimension'), 128)
        self.assertEqual(result.index.get('distanceMetric'), 'EUCLIDEAN')
        self.assertEqual(result.index.get('metadata').get('nonFilterableMetadataKeys'), ['key1', 'key2'])

    def test_deserialize_result_with_unknown_property(self):
        # A property the service adds later is still readable, because index is
        # a dict and nothing filters the keys.
        json_data = '''
        {
           "index": {
              "indexName": "test-fusion-index",
              "mode": "fusion",
              "someFutureProperty": {"nested": [1, 2]}
           }
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.GetVectorIndexResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.index.get('mode'), 'fusion')
        self.assertEqual(result.index.get('someFutureProperty'), {'nested': [1, 2]})


class TestListVectorIndexesMixed(unittest.TestCase):
    """ListVectorIndexes returns standard and fusion items in one page."""

    def test_deserialize_mixed_result(self):
        json_data = '''
        {
            "indexes": [
                {
                    "createTime": "2023-12-17T00:20:57.000Z",
                    "indexName": "standard-index",
                    "dataType": "vector",
                    "dimension": 128,
                    "distanceMetric": "EUCLIDEAN",
                    "vectorBucketName": "test-bucket",
                    "status": "Active"
                },
                {
                    "createTime": "2023-12-18T00:20:57.000Z",
                    "indexName": "fusion-summary-index",
                    "mode": "fusion",
                    "vectorBucketName": "test-bucket",
                    "status": "Active"
                },
                {
                    "createTime": "2023-12-19T00:20:57.000Z",
                    "indexName": "fusion-full-index",
                    "mode": "fusion",
                    "schemaConfiguration": {
                        "fields": [
                            {
                                "name": "text_vector",
                                "type": "vector",
                                "dataType": "float32",
                                "dimension": 4
                            }
                        ]
                    },
                    "vectorBucketName": "test-bucket",
                    "status": "Active"
                }
            ],
            "nextToken": "next-token"
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.ListVectorIndexesResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.next_token, 'next-token')
        self.assertIsNotNone(result.indexes)
        self.assertEqual(len(result.indexes), 3)

        # standard item, no mode at all
        self.assertEqual(result.indexes[0].get('indexName'), 'standard-index')
        self.assertIsNone(result.indexes[0].get('mode'))
        self.assertIsNone(result.indexes[0].get('schemaConfiguration'))
        self.assertEqual(result.indexes[0].get('dataType'), 'vector')
        self.assertEqual(result.indexes[0].get('dimension'), 128)

        # fusion item that only carries the summary, the schema is absent
        self.assertEqual(result.indexes[1].get('indexName'), 'fusion-summary-index')
        self.assertEqual(result.indexes[1].get('mode'), 'fusion')
        self.assertIsNone(result.indexes[1].get('schemaConfiguration'))
        self.assertIsNone(result.indexes[1].get('dataType'))

        # fusion item that does carry the schema
        self.assertEqual(result.indexes[2].get('indexName'), 'fusion-full-index')
        self.assertEqual(result.indexes[2].get('mode'), 'fusion')
        fields = result.indexes[2].get('schemaConfiguration').get('fields')
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].get('name'), 'text_vector')
        self.assertEqual(fields[0].get('dataType'), 'float32')
        self.assertEqual(fields[0].get('dimension'), 4)

        # every item still reports the common properties
        for index in result.indexes:
            self.assertEqual(index.get('vectorBucketName'), 'test-bucket')
            self.assertEqual(index.get('status'), 'Active')
            self.assertIsNotNone(index.get('createTime'))
