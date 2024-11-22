# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_policy as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketPolicy(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketPolicyRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.body)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketPolicyRequest(
            bucket='bucketexampletest',
            body='xml_data',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('xml_data', request.body)

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


class TestGetBucketPolicy(unittest.TestCase):
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

        result = model.GetBucketPolicyResult(
            body='xml_data',
        )
        self.assertEqual('xml_data', result.body)

    def test_deserialize_result(self):

        xml_data = r'''
        {
          "Version":"1",
          "Statement":[
            {
              "Action":[
                "oss:PutObject",
                "oss:GetObject"
              ],
              "Effect":"Deny",
              "Principal":["1234567890"],
              "Resource":["acs:oss:*:1234567890:*/*"]
            }
          ]
        }
        '''

        result = model.GetBucketPolicyResult(
            body=xml_data,
        )
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse()
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(xml_data, result.body)


class TestGetBucketPolicyStatus(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketPolicyStatusRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketPolicyStatusRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketPolicyStatusRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketPolicyStatus',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketPolicyStatus', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketPolicyStatusResult()
        self.assertIsNone(result.policy_status)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketPolicyStatusResult(
            policy_status=model.PolicyStatus(
                is_public=True,
            ),
        )
        self.assertEqual(True, result.policy_status.is_public)

    def test_deserialize_result(self):
        xml_data = r'''
        <PolicyStatus>
        </PolicyStatus>'''

        result = model.GetBucketPolicyStatusResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <PolicyStatus>
           <IsPublic>true</IsPublic>
        </PolicyStatus>
        '''

        result = model.GetBucketPolicyStatusResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(True, result.policy_status.is_public)


class TestDeleteBucketPolicy(unittest.TestCase):
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


