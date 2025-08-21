# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_policy as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutVectorBucketPolicy(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketPolicyRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.body)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        json_data = r'''
        {
           "Version":"1",
           "Statement":[
               {
                 "Action":[
                   "ossvector:PutVectors",
                   "ossvector:GetVectors"
                ],
                "Effect":"Deny",
                "Principal":["1234567890"],
                "Resource":["acs:ossvector:cn-hangzhou:1234567890:*"]
               }
            ]
         }
        '''

        request = model.PutBucketPolicyRequest(
            bucket='bucketexampletest',
            body=json_data,
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(json_data, request.body)

    def test_serialize_request(self):
        request = model.PutBucketPolicyRequest(
            bucket='bucketexampletest',
            body='xml_data',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketPolicy',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketPolicy', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketPolicyResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketPolicyResult()
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
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestGetVectorBucketPolicy(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketPolicyRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketPolicyRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketPolicyRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketPolicy',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketPolicy', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketPolicyResult()
        self.assertIsNone(result.body)
        self.assertIsInstance(result, serde.Model)

        json_data = r'''
                {
                   "Version":"1",
                   "Statement":[
                       {
                         "Action":[
                           "ossvector:PutVectors",
                           "ossvector:GetVectors"
                        ],
                        "Effect":"Deny",
                        "Principal":["1234567890"],
                        "Resource":["acs:ossvector:cn-hangzhou:1234567890:*"]
                       }
                    ]
                 }
                '''

        result = model.GetBucketPolicyResult(
            body=json_data,
        )
        self.assertEqual(json_data, result.body)

    def test_deserialize_result(self):

        json_data = r'''
        {
           "Version":"1",
           "Statement":[
               {
                 "Action":[
                   "ossvector:PutVectors",
                   "ossvector:GetVectors"
                ],
                "Effect":"Deny",
                "Principal":["1234567890"],
                "Resource":["acs:ossvector:cn-hangzhou:1234567890:*"]
               }
            ]
         }
        '''

        result = model.GetBucketPolicyResult(
            body=json_data,
        )
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse()
        )
        deserializer = []
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(json_data, result.body)


class TestDeleteVectorBucketPolicy(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketPolicyRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketPolicyRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)


    def test_serialize_request(self):
        request = model.DeleteBucketPolicyRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketPolicy',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketPolicy', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketPolicyResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketPolicyResult()
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
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


