# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import vector_models as vector_models
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestPutVectorIndex(unittest.TestCase):
    def test_constructor_request(self):
        request = vector_models.PutVectorIndexRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.name)
        self.assertIsNone(request.dimension)
        self.assertIsNone(request.distance_metric)
        self.assertIsNone(request.index_type)
        self.assertIsNone(request.quantization_config)
        self.assertIsNone(request.description)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = vector_models.PutVectorIndexRequest(
            bucket='test-bucket',
            name='test-index',
            dimension=128,
            distance_metric='L2',
            index_type='FLAT',
            quantization_config=vector_models.QuantizationConfig(
                enable_quantization=False,
            ),
            description='test description',
        )
        self.assertEqual('test-bucket', request.bucket)
        self.assertEqual('test-index', request.name)
        self.assertEqual(128, request.dimension)
        self.assertEqual('L2', request.distance_metric)
        self.assertEqual('FLAT', request.index_type)
        self.assertEqual(False, request.quantization_config.enable_quantization)
        self.assertEqual('test description', request.description)

    def test_serialize_request(self):
        request = vector_models.PutVectorIndexRequest(
            bucket='test-bucket',
            name='test-index',
            dimension=128,
            distance_metric='L2',
            index_type='FLAT',
            quantization_config=vector_models.QuantizationConfig(
                enable_quantization=False,
            ),
            description='test description',
        )

        json_str = '{"Bucket": "test-bucket", "Name": "test-index", "Dimension": 128, "DistanceMetric": "L2", "IndexType": "FLAT", "QuantizationConfig": {"EnableQuantization": "false"}, "Description": "test description"}'

        op_input = serde.serialize_input_json(request, OperationInput(
            op_name='PutVectorIndex',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutVectorIndex', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('test-bucket', op_input.bucket)
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        result = vector_models.PutVectorIndexResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = None
        result = vector_models.PutVectorIndexResult()
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
        request = vector_models.GetVectorIndexRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = vector_models.GetVectorIndexRequest(
            bucket='test-bucket',
            name='test-index',
        )
        self.assertEqual('test-bucket', request.bucket)
        self.assertEqual('test-index', request.name)

    def test_serialize_request(self):
        request = vector_models.GetVectorIndexRequest(
            bucket='test-bucket',
            name='test-index',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetVectorIndex',
            method='GET',
            bucket=request.bucket,
            parameters={
                'name': request.name,
            }
        ))
        self.assertEqual('GetVectorIndex', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('test-bucket', op_input.bucket)
        self.assertEqual('test-index', op_input.parameters.get('name'))

    def test_constructor_result(self):
        result = vector_models.GetVectorIndexResult()
        self.assertIsNone(result.index)
        self.assertIsInstance(result, serde.Model)

        result = vector_models.GetVectorIndexResult(
            index=vector_models.Index(
                name='test-index',
                dimension=128,
                distance_metric='L2',
                index_type='FLAT',
                quantization_config=vector_models.QuantizationConfig(
                    enable_quantization=False,
                ),
                description='test description',
                create_time='2023-01-01T00:00:00.000Z',
                update_time='2023-01-01T00:00:00.000Z',
                pending_task_count=0,
                failed_task_count=0,
            ),
        )
        self.assertEqual('test-index', result.index.name)
        self.assertEqual(128, result.index.dimension)
        self.assertEqual('L2', result.index.distance_metric)
        self.assertEqual('FLAT', result.index.index_type)
        self.assertEqual(False, result.index.quantization_config.enable_quantization)
        self.assertEqual('test description', result.index.description)

    def test_deserialize_result(self):
        json_data = r'''
            {
              "Index": {
                "Name": "test-index",
                "Dimension": 128,
                "DistanceMetric": "L2",
                "IndexType": "FLAT",
                "QuantizationConfig": {
                  "EnableQuantization": "false"
                },
                "Description": "test description",
                "CreateTime": "2023-01-01T00:00:00.000Z",
                "UpdateTime": "2023-01-01T00:00:00.000Z",
                "PendingTaskCount": 0,
                "FailedTaskCount": 0
              }
            }
        '''

        result = vector_models.GetVectorIndexResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )
        deserializer = [serde.deserialize_output_jsonbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('test-index', result.index.name)
        self.assertEqual(128, result.index.dimension)
        self.assertEqual('L2', result.index.distance_metric)
        self.assertEqual('FLAT', result.index.index_type)
        self.assertEqual(False, result.index.quantization_config.enable_quantization)
        self.assertEqual('test description', result.index.description)
        self.assertEqual(0, result.index.pending_task_count)
        self.assertEqual(0, result.index.failed_task_count)


class TestListVectorIndex(unittest.TestCase):
    def test_constructor_request(self):
        request = vector_models.ListVectorsIndexRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.max_results)
        self.assertIsNone(request.next_token)
        self.assertIsNone(request.prefix)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = vector_models.ListVectorsIndexRequest(
            bucket='test-bucket',
            max_results=100,
            next_token='next-token',
            prefix='test',
        )
        self.assertEqual('test-bucket', request.bucket)
        self.assertEqual(100, request.max_results)
        self.assertEqual('next-token', request.next_token)
        self.assertEqual('test', request.prefix)

    def test_serialize_request(self):
        request = vector_models.ListVectorsIndexRequest(
            bucket='test-bucket',
            max_results=100,
            next_token='next-token',
            prefix='test',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListVectorIndex',
            method='GET',
            bucket=request.bucket,
            parameters={
                'maxResults': request.max_results,
                'nextToken': request.next_token,
                'prefix': request.prefix,
            }
        ))
        self.assertEqual('ListVectorIndex', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('test-bucket', op_input.bucket)
        self.assertEqual(100, op_input.parameters.get('maxResults'))
        self.assertEqual('next-token', op_input.parameters.get('nextToken'))
        self.assertEqual('test', op_input.parameters.get('prefix'))

    def test_constructor_result(self):
        result = vector_models.ListVectorsIndexResult()
        self.assertIsNone(result.indexes)
        self.assertIsNone(result.max_results)
        self.assertIsNone(result.next_token)
        self.assertIsInstance(result, serde.Model)

        result = vector_models.ListVectorsIndexResult(
            indexes=[
                vector_models.Index(
                    name='test-index-1',
                    dimension=128,
                    distance_metric='L2',
                    index_type='FLAT',
                ),
                vector_models.Index(
                    name='test-index-2',
                    dimension=256,
                    distance_metric='IP',
                    index_type='HNSW',
                )
            ],
            max_results=100,
            next_token='next-token',
        )
        self.assertEqual(2, len(result.indexes))
        self.assertEqual('test-index-1', result.indexes[0].name)
        self.assertEqual(128, result.indexes[0].dimension)
        self.assertEqual('test-index-2', result.indexes[1].name)
        self.assertEqual(256, result.indexes[1].dimension)
        self.assertEqual(100, result.max_results)
        self.assertEqual('next-token', result.next_token)

    def test_deserialize_result(self):
        json_data = r'''
            {
              "Indexes": [
                {
                  "Name": "test-index-1",
                  "Dimension": 128,
                  "DistanceMetric": "L2",
                  "IndexType": "FLAT",
                  "QuantizationConfig": {
                    "EnableQuantization": "false"
                  },
                  "Description": "test description 1",
                  "CreateTime": "2023-01-01T00:00:00.000Z",
                  "UpdateTime": "2023-01-01T00:00:00.000Z",
                  "PendingTaskCount": 0,
                  "FailedTaskCount": 0
                },
                {
                  "Name": "test-index-2",
                  "Dimension": 256,
                  "DistanceMetric": "IP",
                  "IndexType": "HNSW",
                  "QuantizationConfig": {
                    "EnableQuantization": "true"
                  },
                  "Description": "test description 2",
                  "CreateTime": "2023-01-02T00:00:00.000Z",
                  "UpdateTime": "2023-01-02T00:00:00.000Z",
                  "PendingTaskCount": 1,
                  "FailedTaskCount": 0
                }
              ],
              "MaxResults": 100,
              "NextToken": "next-token"
            }
        '''

        result = vector_models.ListVectorsIndexResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )
        deserializer = [serde.deserialize_output_jsonbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(2, len(result.indexes))
        self.assertEqual('test-index-1', result.indexes[0].name)
        self.assertEqual(128, result.indexes[0].dimension)
        self.assertEqual('L2', result.indexes[0].distance_metric)
        self.assertEqual('FLAT', result.indexes[0].index_type)
        self.assertEqual('test-index-2', result.indexes[1].name)
        self.assertEqual(256, result.indexes[1].dimension)
        self.assertEqual('IP', result.indexes[1].distance_metric)
        self.assertEqual('HNSW', result.indexes[1].index_type)
        self.assertEqual(100, result.max_results)
        self.assertEqual('next-token', result.next_token)


class TestDeleteVectorIndex(unittest.TestCase):
    def test_constructor_request(self):
        request = vector_models.DeleteVectorIndexRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = vector_models.DeleteVectorIndexRequest(
            bucket='test-bucket',
            name='test-index',
        )
        self.assertEqual('test-bucket', request.bucket)
        self.assertEqual('test-index', request.name)

    def test_serialize_request(self):
        request = vector_models.DeleteVectorIndexRequest(
            bucket='test-bucket',
            name='test-index',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteVectorIndex',
            method='DELETE',
            bucket=request.bucket,
            parameters={
                'name': request.name,
            }
        ))
        self.assertEqual('DeleteVectorIndex', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('test-bucket', op_input.bucket)
        self.assertEqual('test-index', op_input.parameters.get('name'))

    def test_constructor_result(self):
        result = vector_models.DeleteVectorIndexResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = None
        result = vector_models.DeleteVectorIndexResult()
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
