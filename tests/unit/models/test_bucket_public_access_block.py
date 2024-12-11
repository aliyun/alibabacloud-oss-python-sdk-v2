# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_public_access_block as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketPublicAccessBlock(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketPublicAccessBlockRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.public_access_block_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketPublicAccessBlockRequest(
            bucket='bucketexampletest',
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(True, request.public_access_block_configuration.block_public_access)

    def test_serialize_request(self):
        request = model.PutBucketPublicAccessBlockRequest(
            bucket='bucketexampletest',
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketPublicAccessBlock',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketPublicAccessBlock', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketPublicAccessBlockResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketPublicAccessBlockResult()
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


class TestGetBucketPublicAccessBlock(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketPublicAccessBlockRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketPublicAccessBlockRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketPublicAccessBlockRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketPublicAccessBlock',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketPublicAccessBlock', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketPublicAccessBlockResult()
        self.assertIsNone(result.public_access_block_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketPublicAccessBlockResult(
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )
        self.assertEqual(True, result.public_access_block_configuration.block_public_access)

    def test_deserialize_result(self):
        xml_data = r'''
        <PublicAccessBlockConfiguration>
        </PublicAccessBlockConfiguration>'''

        result = model.GetBucketPublicAccessBlockResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <PublicAccessBlockConfiguration>
          <BlockPublicAccess>true</BlockPublicAccess>
        </PublicAccessBlockConfiguration>
        '''

        result = model.GetBucketPublicAccessBlockResult()
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
        self.assertEqual(True, result.public_access_block_configuration.block_public_access)


class TestDeleteBucketPublicAccessBlock(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketPublicAccessBlockRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketPublicAccessBlockRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.DeleteBucketPublicAccessBlockRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketPublicAccessBlock',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketPublicAccessBlock', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketPublicAccessBlockResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketPublicAccessBlockResult()
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

