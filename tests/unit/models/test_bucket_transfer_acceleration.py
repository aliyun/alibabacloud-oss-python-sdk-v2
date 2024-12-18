# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_transfer_acceleration as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestPutBucketTransferAcceleration(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketTransferAccelerationRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.transfer_acceleration_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketTransferAccelerationRequest(
            bucket='bucketexampletest',
            transfer_acceleration_configuration=model.TransferAccelerationConfiguration(
                enabled=True,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(True, request.transfer_acceleration_configuration.enabled)

    def test_serialize_request(self):
        request = model.PutBucketTransferAccelerationRequest(
            bucket='bucketexampletest',
            transfer_acceleration_configuration=model.TransferAccelerationConfiguration(
                enabled=True,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketTransferAcceleration',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketTransferAcceleration', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketTransferAccelerationResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketTransferAccelerationResult()
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


class TestGetBucketTransferAcceleration(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketTransferAccelerationRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketTransferAccelerationRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketTransferAccelerationRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketTransferAcceleration',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketTransferAcceleration', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketTransferAccelerationResult()
        self.assertIsNone(result.transfer_acceleration_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketTransferAccelerationResult(
            transfer_acceleration_configuration=model.TransferAccelerationConfiguration(
                enabled=True,
            ),
        )
        self.assertEqual(True, result.transfer_acceleration_configuration.enabled)

    def test_deserialize_result(self):
        xml_data = r'''
        <TransferAccelerationConfiguration>
        </TransferAccelerationConfiguration>'''

        result = model.GetBucketTransferAccelerationResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <TransferAccelerationConfiguration>
         <Enabled>true</Enabled>
        </TransferAccelerationConfiguration>
        '''

        result = model.GetBucketTransferAccelerationResult()
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
        self.assertEqual(True, result.transfer_acceleration_configuration.enabled)

