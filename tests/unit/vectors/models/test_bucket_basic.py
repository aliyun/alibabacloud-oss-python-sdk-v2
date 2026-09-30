# pylint: skip-file
import datetime
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.vectors.models import bucket_basic as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from ... import MockHttpResponse


class TestPutVectorBucket(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutVectorBucketRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutVectorBucketRequest(
            bucket='examplebucket',
        )
        self.assertEqual('examplebucket', request.bucket)

    def test_serialize_request(self):
        request = model.PutVectorBucketRequest(
            bucket='examplebucket',
        )

        op_input = serde.serialize_input_json(request, OperationInput(
            op_name='PutVectorBucket',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutVectorBucket', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('examplebucket', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutVectorBucketResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = None
        result = model.PutVectorBucketResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                    'Location': '/examplebucket',
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
        self.assertEqual('/examplebucket', result.headers.get('Location'))


class TestGetVectorBucket(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetVectorBucketRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetVectorBucketRequest(
            bucket='examplebucket',
        )
        self.assertEqual('examplebucket', request.bucket)

    def test_serialize_request(self):
        request = model.GetVectorBucketRequest(
            bucket='examplebucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetVectorBucket',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetVectorBucket', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('examplebucket', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetVectorBucketResult()
        self.assertIsNone(result.bucket_info)
        self.assertIsInstance(result, serde.Model)

        result = model.GetVectorBucketResult(
            bucket_info=model.BucketInfo(
                name='acs:ossvector:cn-shanghai:103735**********:examplebucket',
                location='oss-cn-hangzhou',
                creation_date='2013-07-31T10:56:21.000Z',
                extranet_endpoint='cn-hangzhou.oss-vectors.aliyuncs.com',
                intranet_endpoint='cn-hangzhou-internal.oss-vectors.aliyuncs.com',
                region='cn-hangzhou',
                resource_group_id='rg-aek27t',
            ),
        )
        self.assertEqual('acs:ossvector:cn-shanghai:103735**********:examplebucket', result.bucket_info.name)
        self.assertEqual('oss-cn-hangzhou', result.bucket_info.location)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.bucket_info.creation_date)
        self.assertEqual('cn-hangzhou.oss-vectors.aliyuncs.com', result.bucket_info.extranet_endpoint)
        self.assertEqual('cn-hangzhou-internal.oss-vectors.aliyuncs.com', result.bucket_info.intranet_endpoint)
        self.assertEqual('cn-hangzhou', result.bucket_info.region)
        self.assertEqual('rg-aek27t', result.bucket_info.resource_group_id)

    def test_deserialize_result(self):
        json_data = r'''
        {
          "BucketInfo": {
                "CreationDate": "2013-07-31T10:56:21.000Z",
                "ExtranetEndpoint": "cn-hangzhou.oss-vectors.aliyuncs.com",
                "IntranetEndpoint": "cn-hangzhou-internal.oss-vectors.aliyuncs.com",
                "Location": "oss-cn-hangzhou",
                "Name": "acs:ossvector:cn-shanghai:103735**********:examplebucket",
                "Region": "cn-hangzhou",
                "ResourceGroupId": "rg-aek27t"
          }
        }'''

        result = model.GetVectorBucketResult()
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
        self.assertEqual('acs:ossvector:cn-shanghai:103735**********:examplebucket', result.bucket_info.name)
        self.assertEqual('oss-cn-hangzhou', result.bucket_info.location)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.bucket_info.creation_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('cn-hangzhou.oss-vectors.aliyuncs.com', result.bucket_info.extranet_endpoint)
        self.assertEqual('cn-hangzhou-internal.oss-vectors.aliyuncs.com', result.bucket_info.intranet_endpoint)
        self.assertEqual('cn-hangzhou', result.bucket_info.region)
        self.assertEqual('rg-aek27t', result.bucket_info.resource_group_id)


class TestDeleteVectorBucket(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteVectorBucketRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteVectorBucketRequest(
            bucket='examplebucket',
        )
        self.assertEqual('examplebucket', request.bucket)

    def test_serialize_request(self):
        request = model.DeleteVectorBucketRequest(
            bucket='examplebucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteVectorBucket',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteVectorBucket', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('examplebucket', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteVectorBucketResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = None
        result = model.DeleteVectorBucketResult()
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
        request = model.ListVectorBucketsRequest(
        )
        self.assertIsNone(request.prefix)
        self.assertIsNone(request.marker)
        self.assertIsNone(request.max_keys)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListVectorBucketsRequest(
            prefix='my',
            marker='mybucket',
            max_keys=10,
        )
        self.assertEqual('my', request.prefix)
        self.assertEqual('mybucket', request.marker)
        self.assertEqual(10, request.max_keys)

    def test_serialize_request(self):
        request = model.ListVectorBucketsRequest(
            prefix='my',
            marker='mybucket',
            max_keys=10,
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListVectorBuckets',
            method='GET',
        ))
        self.assertEqual('ListVectorBuckets', op_input.op_name)
        self.assertEqual('GET', op_input.method)

    def test_constructor_result(self):
        result = model.ListVectorBucketsResult()
        self.assertIsNone(result.buckets)
        self.assertIsNone(result.prefix)
        self.assertIsNone(result.marker)
        self.assertIsNone(result.max_keys)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.next_marker)
        self.assertIsInstance(result, serde.Model)

        result = model.ListVectorBucketsResult(
            prefix='my',
            marker='mybucket',
            max_keys=10,
            is_truncated=True,
            next_marker='mybucket10',
            buckets=[model.BucketProperties(
                name='acs:ossvector:cn-shanghai:103735**********:test-bucket-3',
                location='oss-cn-shanghai',
                creation_date=datetime.datetime.fromtimestamp(1702733657),
                region='cn-shanghai',
                resource_group_id='rg-default-id',
            )],
        )
        self.assertEqual('my', result.prefix)
        self.assertEqual('mybucket', result.marker)
        self.assertEqual(10, result.max_keys)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('mybucket10', result.next_marker)
        self.assertEqual('acs:ossvector:cn-shanghai:103735**********:test-bucket-3', result.buckets[0].name)
        self.assertEqual('rg-default-id', result.buckets[0].resource_group_id)

    def test_deserialize_result(self):
        json_data = r'''
        {
            "ListAllMyBucketsResult": {
                "Prefix": "my",
                "Marker": "mybucket",
                "MaxKeys": 10,
                "IsTruncated": true,
                "NextMarker": "mybucket10",
                "Buckets": [
                    {
                      "CreationDate": "2014-02-07T18:12:43.000Z",
                      "ExtranetEndpoint": "cn-shanghai.oss-vectors.aliyuncs.com",
                      "IntranetEndpoint": "cn-shanghai-internal.oss-vectors.aliyuncs.com",
                      "Location": "oss-cn-shanghai",
                      "Name": "acs:ossvector:cn-shanghai:103735**********:test-bucket-3",
                      "Region": "cn-shanghai",
                      "ResourceGroupId": "rg-default-id"
                    },
                    {
                      "CreationDate": "2014-02-05T11:21:04.000Z",
                      "ExtranetEndpoint": "cn-shanghai.oss-vectors.aliyuncs.com",
                      "IntranetEndpoint": "cn-shanghai-internal.oss-vectors.aliyuncs.com",
                      "Location": "oss-cn-hangzhou",
                      "Name": "acs:ossvector:cn-shanghai:103735**********:test-bucket-4",
                      "Region": "cn-hangzhou",
                      "ResourceGroupId": "rg-default-id"
                    }
                ]
              }
        }
        '''

        result = model.ListVectorBucketsResult()
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
        self.assertEqual('my', result.prefix)
        self.assertEqual('mybucket', result.marker)
        self.assertEqual(10, result.max_keys)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('mybucket10', result.next_marker)
        self.assertEqual(2, len(result.buckets))
        self.assertEqual('acs:ossvector:cn-shanghai:103735**********:test-bucket-3', result.buckets[0].name)
        self.assertEqual('oss-cn-shanghai', result.buckets[0].location)
        self.assertEqual('2014-02-07T18:12:43.000Z', result.buckets[0].creation_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('cn-shanghai.oss-vectors.aliyuncs.com', result.buckets[0].extranet_endpoint)
        self.assertEqual('cn-shanghai-internal.oss-vectors.aliyuncs.com', result.buckets[0].intranet_endpoint)
        self.assertEqual('cn-shanghai', result.buckets[0].region)
        self.assertEqual('rg-default-id', result.buckets[0].resource_group_id)
        self.assertEqual('acs:ossvector:cn-shanghai:103735**********:test-bucket-4', result.buckets[1].name)
        self.assertEqual('oss-cn-hangzhou', result.buckets[1].location)
        self.assertEqual('2014-02-05T11:21:04.000Z', result.buckets[1].creation_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('cn-shanghai.oss-vectors.aliyuncs.com', result.buckets[1].extranet_endpoint)
        self.assertEqual('cn-shanghai-internal.oss-vectors.aliyuncs.com', result.buckets[1].intranet_endpoint)
        self.assertEqual('cn-hangzhou', result.buckets[1].region)
        self.assertEqual('rg-default-id', result.buckets[1].resource_group_id)
