# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import access_point_public_access_block as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutAccessPointPublicAccessBlock(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutAccessPointPublicAccessBlockRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_name)
        self.assertIsNone(request.public_access_block_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutAccessPointPublicAccessBlockRequest(
            bucket='bucketexampletest',
            access_point_name='test_access_point_name',
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_name', request.access_point_name)
        self.assertEqual(True, request.public_access_block_configuration.block_public_access)

    def test_serialize_request(self):
        request = model.PutAccessPointPublicAccessBlockRequest(
            bucket='bucketexampletest',
            access_point_name='test_access_point_name',
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAccessPointPublicAccessBlock',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutAccessPointPublicAccessBlock', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('test_access_point_name', op_input.parameters.get('x-oss-access-point-name'))

    def test_constructor_result(self):
        result = model.PutAccessPointPublicAccessBlockResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutAccessPointPublicAccessBlockResult()
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


class TestGetAccessPointPublicAccessBlock(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetAccessPointPublicAccessBlockRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetAccessPointPublicAccessBlockRequest(
            bucket='bucketexampletest',
            access_point_name='test_access_point_name',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_name', request.access_point_name)

    def test_serialize_request(self):
        request = model.GetAccessPointPublicAccessBlockRequest(
            bucket='bucketexampletest',
            access_point_name='test_access_point_name',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetAccessPointPublicAccessBlock',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetAccessPointPublicAccessBlock', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('test_access_point_name', op_input.parameters.get('x-oss-access-point-name'))

    def test_constructor_result(self):
        result = model.GetAccessPointPublicAccessBlockResult()
        self.assertIsNone(result.public_access_block_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetAccessPointPublicAccessBlockResult(
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )
        self.assertEqual(True, result.public_access_block_configuration.block_public_access)

    def test_deserialize_result(self):
        xml_data = r'''
        <PublicAccessBlockConfiguration>
        </PublicAccessBlockConfiguration>'''

        result = model.GetAccessPointPublicAccessBlockResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <PublicAccessBlockConfiguration>
          <BlockPublicAccess>true</BlockPublicAccess>
        </PublicAccessBlockConfiguration>
        '''

        result = model.GetAccessPointPublicAccessBlockResult()
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


class TestDeleteAccessPointPublicAccessBlock(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteAccessPointPublicAccessBlockRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteAccessPointPublicAccessBlockRequest(
            bucket='bucketexampletest',
            access_point_name='test_access_point_name',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_name', request.access_point_name)

    def test_serialize_request(self):
        request = model.DeleteAccessPointPublicAccessBlockRequest(
            bucket='bucketexampletest',
            access_point_name='test_access_point_name',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteAccessPointPublicAccessBlock',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteAccessPointPublicAccessBlock', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('test_access_point_name', op_input.parameters.get('x-oss-access-point-name'))

    def test_constructor_result(self):
        result = model.DeleteAccessPointPublicAccessBlockResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteAccessPointPublicAccessBlockResult()
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

