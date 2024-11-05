# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_archive_direct_read as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketArchiveDirectRead(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketArchiveDirectReadRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.archive_direct_read_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketArchiveDirectReadRequest(
            bucket='bucket_name',
            archive_direct_read_configuration=model.ArchiveDirectReadConfiguration(
                enabled=False,
            ),
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual(False, request.archive_direct_read_configuration.enabled)

    def test_serialize_request(self):
        request = model.PutBucketArchiveDirectReadRequest(
            bucket='bucket_name',
            archive_direct_read_configuration=model.ArchiveDirectReadConfiguration(
                enabled=True,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketArchiveDirectRead',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketArchiveDirectRead', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketArchiveDirectReadResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketArchiveDirectReadResult()
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


class TestGetBucketArchiveDirectRead(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketArchiveDirectReadRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketArchiveDirectReadRequest(
            bucket='bucket_name',
        )
        self.assertEqual('bucket_name', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketArchiveDirectReadRequest(
            bucket='bucket_name',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketArchiveDirectRead',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketArchiveDirectRead', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketArchiveDirectReadResult()
        self.assertIsNone(result.archive_direct_read_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketArchiveDirectReadResult(
            archive_direct_read_configuration=model.ArchiveDirectReadConfiguration(
                enabled=True,
            ),
        )
        self.assertEqual(True, result.archive_direct_read_configuration.enabled)

    def test_deserialize_result(self):
        xml_data = r'''
        <ArchiveDirectReadConfiguration>
        </ArchiveDirectReadConfiguration>'''

        result = model.GetBucketArchiveDirectReadResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ArchiveDirectReadConfiguration>
            <Enabled>false</Enabled>
        </ArchiveDirectReadConfiguration>
        '''

        result = model.GetBucketArchiveDirectReadResult()
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
        self.assertEqual(False, result.archive_direct_read_configuration.enabled)
