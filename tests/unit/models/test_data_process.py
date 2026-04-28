# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import data_process as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestDoMetaQueryAction(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DoMetaQueryActionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.action)
        self.assertIsNone(request.body)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DoMetaQueryActionRequest(
            bucket='bucketexampletest',
            action='createDataset',
            body=b'<MetaQuery></MetaQuery>',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('createDataset', request.action)
        self.assertEqual(b'<MetaQuery></MetaQuery>', request.body)

    def test_serialize_request(self):
        request = model.DoMetaQueryActionRequest(
            bucket='bucketexampletest',
            action='createDataset',
            body=b'<MetaQuery></MetaQuery>',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DoMetaQueryAction',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('DoMetaQueryAction', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual(b'<MetaQuery></MetaQuery>', op_input.body)

    def test_constructor_result(self):
        result = model.DoMetaQueryActionResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DoMetaQueryActionResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
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


class TestDoDataPipelineAction(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DoDataPipelineActionRequest(
        )
        self.assertIsNone(request.action)
        self.assertIsNone(request.body)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DoDataPipelineActionRequest(
            action='putDataPipelineConfiguration',
            body=b'<DataPipeline></DataPipeline>',
        )
        self.assertEqual('putDataPipelineConfiguration', request.action)
        self.assertEqual(b'<DataPipeline></DataPipeline>', request.body)

    def test_serialize_request(self):
        request = model.DoDataPipelineActionRequest(
            action='putDataPipelineConfiguration',
            body=b'<DataPipeline></DataPipeline>',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DoDataPipelineAction',
            method='POST',
        ))
        self.assertEqual('DoDataPipelineAction', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual(b'<DataPipeline></DataPipeline>', op_input.body)

    def test_constructor_result(self):
        result = model.DoDataPipelineActionResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DoDataPipelineActionResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
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
