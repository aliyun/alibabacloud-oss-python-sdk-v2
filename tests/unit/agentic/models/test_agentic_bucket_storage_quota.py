# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.agentic import models
from alibabacloud_oss_v2.models.bucket_storage_quota import QuotaConfiguration
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from ... import MockHttpResponse


def _output(body, status_code=200, status='OK'):
    return OperationOutput(
        status=status,
        status_code=status_code,
        headers=CaseInsensitiveDict({'x-oss-request-id': 'req-1'}),
        http_response=MockHttpResponse(status_code=status_code, headers={}, body=body),
    )


class TestPutAgenticBucketStorageQuota(unittest.TestCase):
    def test_constructor_request(self):
        request = models.PutAgenticBucketStorageQuotaRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.quota_configuration)
        self.assertIsInstance(request, serde.RequestModel)

        request = models.PutAgenticBucketStorageQuotaRequest(
            bucket='my-agentic',
            quota_configuration=QuotaConfiguration(
                storage_quota=10737418240,
                mode='Strict',
            ),
        )
        self.assertEqual('my-agentic', request.bucket)
        self.assertEqual(10737418240, request.quota_configuration.storage_quota)
        self.assertEqual('Strict', request.quota_configuration.mode)

    def test_serialize_request(self):
        request = models.PutAgenticBucketStorageQuotaRequest(
            bucket='my-agentic',
            quota_configuration=QuotaConfiguration(
                storage_quota=10737418240,
                mode='Strict',
            ),
        )
        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAgenticBucketStorageQuota',
            method='PUT',
            parameters={'agenticBucket': '', 'quota': ''},
            bucket=request.bucket,
        ))
        self.assertEqual('PutAgenticBucketStorageQuota', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('my-agentic', op_input.bucket)
        self.assertEqual('', op_input.parameters.get('agenticBucket'))
        self.assertEqual('', op_input.parameters.get('quota'))

        # Build the expected canonical XML bytes by round-tripping the expected xml.
        expected_xml = (
            '<QuotaConfiguration>'
            '  <StorageQuota>10737418240</StorageQuota>'
            '  <Mode>Strict</Mode>'
            '</QuotaConfiguration>'
        )
        expected_body = QuotaConfiguration()
        serde.deserialize_xml(expected_xml.encode('utf-8'), expected_body, expect_tag='QuotaConfiguration')
        expected_xml_bytes = serde.serialize_xml(expected_body, root='QuotaConfiguration')

        body = request.quota_configuration
        _xml_map = getattr(body, '_xml_map', {})
        xml_bytes = serde.serialize_xml(body, root=_xml_map.get('name', None))
        self.assertEqual(xml_bytes, expected_xml_bytes)
        self.assertEqual(expected_xml_bytes, op_input.body)

    def test_constructor_result(self):
        result = models.PutAgenticBucketStorageQuotaResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        result = serde.deserialize_output(
            models.PutAgenticBucketStorageQuotaResult(), _output(None),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-1', result.request_id)


class TestGetAgenticBucketStorageQuota(unittest.TestCase):
    def test_constructor_request(self):
        request = models.GetAgenticBucketStorageQuotaRequest()
        self.assertIsNone(request.bucket)
        self.assertIsInstance(request, serde.RequestModel)

        request = models.GetAgenticBucketStorageQuotaRequest(bucket='my-agentic')
        self.assertEqual('my-agentic', request.bucket)

    def test_serialize_request(self):
        request = models.GetAgenticBucketStorageQuotaRequest(bucket='my-agentic')
        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetAgenticBucketStorageQuota',
            method='GET',
            parameters={'agenticBucket': '', 'quota': ''},
            bucket=request.bucket,
        ))
        self.assertEqual('GetAgenticBucketStorageQuota', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('my-agentic', op_input.bucket)

    def test_constructor_result(self):
        result = models.GetAgenticBucketStorageQuotaResult()
        self.assertIsNone(result.quota_configuration)
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        # The Agent Bucket level query does NOT return CurrentUsage.
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<QuotaConfiguration>'
            b'<Mode>Strict</Mode>'
            b'<StorageQuota>104857600</StorageQuota>'
            b'</QuotaConfiguration>'
        )
        result = serde.deserialize_output(
            models.GetAgenticBucketStorageQuotaResult(), _output(xml),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.quota_configuration)
        self.assertEqual('Strict', result.quota_configuration.mode)
        self.assertEqual(104857600, result.quota_configuration.storage_quota)
        self.assertIsNone(result.quota_configuration.current_usage)


class TestDeleteAgenticBucketStorageQuota(unittest.TestCase):
    def test_constructor_request(self):
        request = models.DeleteAgenticBucketStorageQuotaRequest()
        self.assertIsNone(request.bucket)
        self.assertIsInstance(request, serde.RequestModel)

        request = models.DeleteAgenticBucketStorageQuotaRequest(bucket='my-agentic')
        self.assertEqual('my-agentic', request.bucket)

    def test_serialize_request(self):
        request = models.DeleteAgenticBucketStorageQuotaRequest(bucket='my-agentic')
        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteAgenticBucketStorageQuota',
            method='DELETE',
            parameters={'agenticBucket': '', 'quota': ''},
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteAgenticBucketStorageQuota', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('my-agentic', op_input.bucket)

    def test_constructor_result(self):
        result = models.DeleteAgenticBucketStorageQuotaResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        result = serde.deserialize_output(
            models.DeleteAgenticBucketStorageQuotaResult(),
            _output(None, status_code=204, status='No Content'),
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual(204, result.status_code)
        self.assertEqual('req-1', result.request_id)


if __name__ == '__main__':
    unittest.main()
