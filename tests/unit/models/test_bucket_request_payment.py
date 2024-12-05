# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_request_payment as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketRequestPayment(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketRequestPaymentRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.request_payment_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketRequestPaymentRequest(
            bucket='bucketexampletest',
            request_payment_configuration=model.RequestPaymentConfiguration(
                payer='Requester',
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('Requester', request.request_payment_configuration.payer)

    def test_serialize_request(self):
        request = model.PutBucketRequestPaymentRequest(
            bucket='bucketexampletest',
            request_payment_configuration=model.RequestPaymentConfiguration(
                payer='Requester',
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketRequestPayment',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketRequestPayment', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketRequestPaymentResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketRequestPaymentResult()
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


class TestGetBucketRequestPayment(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketRequestPaymentRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketRequestPaymentRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketRequestPaymentRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketRequestPayment',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketRequestPayment', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketRequestPaymentResult()
        self.assertIsNone(result.request_payment_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketRequestPaymentResult(
            request_payment_configuration=model.RequestPaymentConfiguration(
                payer='BucketOwner',
            ),
        )
        self.assertEqual('BucketOwner', result.request_payment_configuration.payer)

    def test_deserialize_result(self):
        xml_data = r'''
        <RequestPaymentConfiguration>
        </RequestPaymentConfiguration>'''

        result = model.GetBucketRequestPaymentResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <RequestPaymentConfiguration>
          <Payer>BucketOwner</Payer>
        </RequestPaymentConfiguration>
        '''

        result = model.GetBucketRequestPaymentResult()
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
        self.assertEqual('BucketOwner', result.request_payment_configuration.payer)


