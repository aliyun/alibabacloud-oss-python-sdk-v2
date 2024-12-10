# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import public_access_block as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutPublicAccessBlock(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutPublicAccessBlockRequest(
        )
        self.assertIsNone(request.public_access_block_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutPublicAccessBlockRequest(
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )
        self.assertEqual(True, request.public_access_block_configuration.block_public_access)

    def test_serialize_request(self):
        request = model.PutPublicAccessBlockRequest(
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutPublicAccessBlock',
            method='PUT',
        ))
        self.assertEqual('PutPublicAccessBlock', op_input.op_name)
        self.assertEqual('PUT', op_input.method)

    def test_constructor_result(self):
        result = model.PutPublicAccessBlockResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutPublicAccessBlockResult()
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


class TestGetPublicAccessBlock(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetPublicAccessBlockRequest(
        )
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)


    def test_serialize_request(self):
        request = model.GetPublicAccessBlockRequest(
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetPublicAccessBlock',
            method='GET',
        ))
        self.assertEqual('GetPublicAccessBlock', op_input.op_name)
        self.assertEqual('GET', op_input.method)

    def test_constructor_result(self):
        result = model.GetPublicAccessBlockResult()
        self.assertIsNone(result.public_access_block_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetPublicAccessBlockResult(
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )
        self.assertEqual(True, result.public_access_block_configuration.block_public_access)

    def test_deserialize_result(self):
        xml_data = r'''
        <PublicAccessBlockConfiguration>
        </PublicAccessBlockConfiguration>'''

        result = model.GetPublicAccessBlockResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <PublicAccessBlockConfiguration>
          <BlockPublicAccess>true</BlockPublicAccess>
        </PublicAccessBlockConfiguration>
        '''

        result = model.GetPublicAccessBlockResult()
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


class TestDeletePublicAccessBlock(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeletePublicAccessBlockRequest(
        )
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)


    def test_serialize_request(self):
        request = model.DeletePublicAccessBlockRequest(
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeletePublicAccessBlock',
            method='DELETE',
        ))
        self.assertEqual('DeletePublicAccessBlock', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)

    def test_constructor_result(self):
        result = model.DeletePublicAccessBlockResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeletePublicAccessBlockResult()
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
