# pylint: skip-file
import datetime
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.vector_models import vector_bucket_basic as vector_models
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestPutVectorBucket(unittest.TestCase):
    def test_constructor_request(self):
        request = vector_models.PutVectorBucketRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.create_bucket_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = vector_models.PutVectorBucketRequest(
            bucket='bucketexampletest',
            create_bucket_configuration=vector_models.CreateBucketConfiguration(
                storage_class='Standard',
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('Standard', request.create_bucket_configuration.storage_class)

    def test_serialize_request(self):
        request = vector_models.PutVectorBucketRequest(
            bucket='bucketexampletest',
            create_bucket_configuration=vector_models.CreateBucketConfiguration(
                storage_class='Standard',
            ),
        )

        op_input = serde.serialize_input_json(request, OperationInput(
            op_name='PutVectorBucket',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutVectorBucket', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = vector_models.PutVectorBucketResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = None
        result = vector_models.PutVectorBucketResult()
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


class TestGetVectorBucket(unittest.TestCase):
    def test_constructor_request(self):
        request = vector_models.GetVectorBucketRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = vector_models.GetVectorBucketRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = vector_models.GetVectorBucketRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetVectorBucket',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetVectorBucket', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = vector_models.GetVectorBucketResult()
        self.assertIsNone(result.bucket_info)
        self.assertIsInstance(result, serde.Model)

        result = vector_models.GetVectorBucketResult(
            bucket_info=vector_models.BucketInfo(
                name='test-bucket',
                location='oss-cn-hangzhou',
                creation_date='2023-01-01T00:00:00.000Z',
            ),
        )
        self.assertEqual('test-bucket', result.bucket_info.name)
        self.assertEqual('oss-cn-hangzhou', result.bucket_info.location)
        self.assertEqual('2023-01-01T00:00:00.000Z', result.bucket_info.creation_date)

    def test_deserialize_result(self):
        json_data = r'''
        {
          "BucketInfo": {
                "CreationDate": "2013-07-31T10:56:21.000Z",
                "ExtranetEndpoint": "oss-cn-hangzhou.aliyuncs.com",
                "IntranetEndpoint": "oss-cn-hangzhou-internal.aliyuncs.com",
                "Location": "oss-cn-hangzhou",
                "Name": "oss-example",
                "ResourceGroupId": "rg-aek27t"
          }
        }'''

        result = vector_models.GetVectorBucketResult()
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
        self.assertEqual('oss-example', result.bucket_info.name)
        self.assertEqual('oss-cn-hangzhou', result.bucket_info.location)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.bucket_info.creation_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))


class TestDeleteVectorBucket(unittest.TestCase):
    def test_constructor_request(self):
        request = vector_models.DeleteVectorBucketRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = vector_models.DeleteVectorBucketRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = vector_models.DeleteVectorBucketRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteVectorBucket',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteVectorBucket', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = vector_models.DeleteVectorBucketResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = None
        result = vector_models.DeleteVectorBucketResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=204,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                }),
                http_response=MockHttpResponse(
                    status_code=204,
                    reason='No Content',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=json_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(204, result.status_code)
        self.assertEqual('123', result.request_id)


class TestListVectorBuckets(unittest.TestCase):
    def test_constructor_request(self):
        request = vector_models.ListVectorBucketsRequest(
        )
        self.assertIsNone(request.prefix)
        self.assertIsNone(request.marker)
        self.assertIsNone(request.max_keys)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = vector_models.ListVectorBucketsRequest(
            prefix='test',
            marker='marker1',
            max_keys=100,
        )
        self.assertEqual('test', request.prefix)
        self.assertEqual('marker1', request.marker)
        self.assertEqual(100, request.max_keys)

    def test_serialize_request(self):
        request = vector_models.ListVectorBucketsRequest(
            prefix='test',
            marker='marker1',
            max_keys=100,
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListVectorBuckets',
            method='GET',
        ))
        self.assertEqual('ListVectorBuckets', op_input.op_name)
        self.assertEqual('GET', op_input.method)

    def test_constructor_result(self):
        result = vector_models.ListVectorBucketsResult()
        self.assertIsNone(result.buckets)
        self.assertIsNone(result.prefix)
        self.assertIsNone(result.marker)
        self.assertIsNone(result.max_keys)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.next_marker)
        self.assertIsInstance(result, serde.Model)

        result = vector_models.ListVectorBucketsResult(
            prefix='test',
            marker='marker1',
            max_keys=100,
            is_truncated=False,
            next_marker='',
            buckets=[vector_models.BucketProperties(
                name='bucket1',
                location='oss-cn-hangzhou',
                creation_date=datetime.datetime.fromtimestamp(1702733657),
            )],
        )
        self.assertEqual('test', result.prefix)
        self.assertEqual('marker1', result.marker)
        self.assertEqual(100, result.max_keys)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual('bucket1', result.buckets[0].name)

    def test_deserialize_result(self):
        json_data = r'''
        {
            "ListAllMyBucketsResult": {
                "Prefix": "test",
                "Marker": "marker1",
                "MaxKeys": 100,
                "IsTruncated": false,
                "NextMarker": "",
                "Buckets": [
                    {
                      "CreationDate": "2014-02-07T18:12:43.000Z",
                      "ExtranetEndpoint": "oss-cn-shanghai.oss-vectors.aliyuncs.com",
                      "IntranetEndpoint": "oss-cn-shanghai-internal.oss-vectors.aliyuncs.com",
                      "Location": "oss-cn-shanghai",
                      "Name": "test-bucket-3",
                      "Region": "cn-shanghai",
                      "ResourceGroupId": "rg-default-id"
                    },
                    {
                      "CreationDate": "2014-02-05T11:21:04.000Z",
                      "ExtranetEndpoint": "oss-cn-hangzhou.oss-vectors.aliyuncs.com",
                      "IntranetEndpoint": "oss-cn-hangzhou-internal.oss-vectors.aliyuncs.com",
                      "Location": "oss-cn-hangzhou",
                      "Name": "test-bucket-4",
                      "Region": "cn-hangzhou",
                      "ResourceGroupId": "rg-default-id"
                    }
                ]
              }
        }
        '''

        result = vector_models.ListVectorBucketsResult()
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
        self.assertEqual('test', result.prefix)
        self.assertEqual('marker1', result.marker)
        self.assertEqual(100, result.max_keys)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual('', result.next_marker)
        self.assertEqual(2, len(result.buckets))
        self.assertEqual('test-bucket-3', result.buckets[0].name)
        self.assertEqual('oss-cn-shanghai', result.buckets[0].location)
        self.assertEqual('2014-02-07T18:12:43.000Z', result.buckets[0].creation_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('test-bucket-4', result.buckets[1].name)
        self.assertEqual('oss-cn-hangzhou', result.buckets[1].location)
        self.assertEqual('2014-02-05T11:21:04.000Z', result.buckets[1].creation_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
