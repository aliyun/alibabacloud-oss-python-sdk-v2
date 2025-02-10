# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import object_basic as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestCleanRestoredObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CleanRestoredObjectRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.key)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CleanRestoredObjectRequest(
            bucket='bucketexampletest',
            key='multipart.data',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('multipart.data', request.key)

    def test_serialize_request(self):
        request = model.CleanRestoredObjectRequest(
            bucket='bucketexampletest',
            key='test.jpg',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CleanRestoredObject',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CleanRestoredObject', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.CleanRestoredObjectResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.CleanRestoredObjectResult()
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

