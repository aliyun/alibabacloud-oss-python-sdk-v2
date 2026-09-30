# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_storage_quota as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from .. import MockHttpResponse


class TestQuotaConfiguration(unittest.TestCase):
    def test_empty_constructor(self):
        cfg = model.QuotaConfiguration()
        self.assertIsNone(cfg.storage_quota)
        self.assertIsNone(cfg.mode)
        self.assertIsNone(cfg.current_usage)
        self.assertIsInstance(cfg, serde.Model)

    def test_full_constructor(self):
        cfg = model.QuotaConfiguration(
            storage_quota=10737418240,
            mode='Strict',
            current_usage=1049600,
        )
        self.assertEqual(10737418240, cfg.storage_quota)
        self.assertEqual('Strict', cfg.mode)
        self.assertEqual(1049600, cfg.current_usage)


class TestPutBucketStorageQuota(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketStorageQuotaRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.quota_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketStorageQuotaRequest(
            bucket='bucketexampletest',
            quota_configuration=model.QuotaConfiguration(
                storage_quota=10737418240,
                mode='Strict',
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(10737418240, request.quota_configuration.storage_quota)
        self.assertEqual('Strict', request.quota_configuration.mode)

    def test_serialize_request(self):
        request = model.PutBucketStorageQuotaRequest(
            bucket='bucketexampletest',
            quota_configuration=model.QuotaConfiguration(
                storage_quota=10737418240,
                mode='Strict',
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketStorageQuota',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketStorageQuota', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

        # Step 1: build the expected canonical XML bytes by round-tripping the expected xml.
        expected_xml = (
            '<QuotaConfiguration>'
            '  <StorageQuota>10737418240</StorageQuota>'
            '  <Mode>Strict</Mode>'
            '</QuotaConfiguration>'
        )
        expected_body = model.QuotaConfiguration()
        serde.deserialize_xml(expected_xml.encode('utf-8'), expected_body, expect_tag='QuotaConfiguration')
        expected_xml_bytes = serde.serialize_xml(expected_body, root='QuotaConfiguration')

        # Step 2: serialize the request body directly and compare exactly.
        body = request.quota_configuration
        _xml_map = getattr(body, '_xml_map', {})
        xml_bytes = serde.serialize_xml(body, root=_xml_map.get('name', None))
        self.assertEqual(xml_bytes, expected_xml_bytes)

        # Step 3: the serialized request body must match the canonical XML bytes.
        self.assertEqual(expected_xml_bytes, op_input.body)

    def test_constructor_result(self):
        result = model.PutBucketStorageQuotaResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        result = model.PutBucketStorageQuotaResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({'x-oss-request-id': '123'}),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': '123'},
                    body=None,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)


class TestGetBucketStorageQuota(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketStorageQuotaRequest()
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketStorageQuotaRequest(bucket='bucketexampletest')
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketStorageQuotaRequest(bucket='bucketexampletest')
        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketStorageQuota',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketStorageQuota', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketStorageQuotaResult()
        self.assertIsNone(result.quota_configuration)
        self.assertIsInstance(result, serde.ResultModel)

        result = model.GetBucketStorageQuotaResult(
            quota_configuration=model.QuotaConfiguration(
                storage_quota=10737418240,
                mode='Strict',
                current_usage=1049600,
            ),
        )
        self.assertEqual(10737418240, result.quota_configuration.storage_quota)
        self.assertEqual('Strict', result.quota_configuration.mode)
        self.assertEqual(1049600, result.quota_configuration.current_usage)

    def test_deserialize_result(self):
        xml_data = r'''<?xml version="1.0" encoding="UTF-8"?>
        <QuotaConfiguration>
          <Mode>Strict</Mode>
          <StorageQuota>10737418240</StorageQuota>
          <CurrentUsage>1049600</CurrentUsage>
        </QuotaConfiguration>'''

        result = model.GetBucketStorageQuotaResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            headers=CaseInsensitiveDict({'x-oss-request-id': 'req-get-quota'}),
            http_response=MockHttpResponse(
                status_code=200,
                headers={'x-oss-request-id': 'req-get-quota'},
                body=xml_data,
            )
        )
        serde.deserialize_output(
            result, op_output,
            custom_deserializer=[serde.deserialize_output_xmlbody])
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('req-get-quota', result.request_id)
        self.assertIsNotNone(result.quota_configuration)
        self.assertEqual('Strict', result.quota_configuration.mode)
        self.assertEqual(10737418240, result.quota_configuration.storage_quota)
        self.assertEqual(1049600, result.quota_configuration.current_usage)


class TestDeleteBucketStorageQuota(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketStorageQuotaRequest()
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketStorageQuotaRequest(bucket='bucketexampletest')
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.DeleteBucketStorageQuotaRequest(bucket='bucketexampletest')
        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketStorageQuota',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketStorageQuota', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketStorageQuotaResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        result = model.DeleteBucketStorageQuotaResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='No Content',
                status_code=204,
                headers=CaseInsensitiveDict({'x-oss-request-id': '123'}),
                http_response=MockHttpResponse(
                    status_code=204,
                    reason='No Content',
                    headers={'x-oss-request-id': '123'},
                    body=None,
                )
            )
        )
        self.assertEqual(204, result.status_code)
        self.assertEqual('123', result.request_id)


if __name__ == '__main__':
    unittest.main()
