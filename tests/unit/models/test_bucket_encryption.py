# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_encryption as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketEncryption(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketEncryptionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.server_side_encryption_rule)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketEncryptionRequest(
            bucket='bucketexampletest',
            server_side_encryption_rule=model.ServerSideEncryptionRule(
                apply_server_side_encryption_by_default=model.ApplyServerSideEncryptionByDefault(
                    kms_master_key_id='0022012****',
                    kms_data_encryption='SM4',
                    sse_algorithm='KMS',
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('0022012****', request.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_master_key_id)
        self.assertEqual('SM4', request.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_data_encryption)
        self.assertEqual('KMS', request.server_side_encryption_rule.apply_server_side_encryption_by_default.sse_algorithm)


    def test_serialize_request(self):
        request = model.PutBucketEncryptionRequest(
            bucket='bucketexampletest',
            server_side_encryption_rule=model.ServerSideEncryptionRule(
                apply_server_side_encryption_by_default=model.ApplyServerSideEncryptionByDefault(
                    kms_master_key_id='0022012****',
                    kms_data_encryption='user_example',
                    sse_algorithm='SM4',
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketEncryption',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketEncryption', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketEncryptionResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketEncryptionResult()
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


class TestGetBucketEncryption(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketEncryptionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketEncryptionRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketEncryptionRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketEncryption',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketEncryption', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketEncryptionResult()
        self.assertIsNone(result.server_side_encryption_rule)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketEncryptionResult(
            server_side_encryption_rule=model.ServerSideEncryptionRule(
                apply_server_side_encryption_by_default=model.ApplyServerSideEncryptionByDefault(
                    kms_master_key_id='0022012****',
                    kms_data_encryption='SM4',
                    sse_algorithm='KMS',
                ),
            ),
        )
        self.assertEqual('0022012****', result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_master_key_id)
        self.assertEqual('SM4', result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_data_encryption)
        self.assertEqual('KMS', result.server_side_encryption_rule.apply_server_side_encryption_by_default.sse_algorithm)

    def test_deserialize_result(self):
        xml_data = r'''
        <ServerSideEncryptionRule>
        </ServerSideEncryptionRule>'''

        result = model.GetBucketEncryptionResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ServerSideEncryptionRule>
          <ApplyServerSideEncryptionByDefault>
            <SSEAlgorithm>KMS</SSEAlgorithm>
            <KMSDataEncryption>SM4</KMSDataEncryption>
            <KMSMasterKeyID>9468da86-3509-4f8d-a61e-6eab1eac****</KMSMasterKeyID>
          </ApplyServerSideEncryptionByDefault>
        </ServerSideEncryptionRule>
        '''

        result = model.GetBucketEncryptionResult()
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
        self.assertEqual('KMS', result.server_side_encryption_rule.apply_server_side_encryption_by_default.sse_algorithm)
        self.assertEqual('SM4', result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_master_key_id)


class TestDeleteBucketEncryption(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketEncryptionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketEncryptionRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)


    def test_serialize_request(self):
        request = model.DeleteBucketEncryptionRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketEncryption',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketEncryption', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketEncryptionResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketEncryptionResult()
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
