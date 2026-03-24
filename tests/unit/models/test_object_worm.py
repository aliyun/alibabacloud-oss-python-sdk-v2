# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import object_worm as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestPutObjectRetention(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutObjectRetentionRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.bypass_governance_retention)
        self.assertIsNone(request.retention)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutObjectRetentionRequest(
            bucket='test-bucket',
            key='test-object',
            version_id='version123',
            bypass_governance_retention=True,
            retention=model.Retention(
                mode=model.ObjectRetentionModeType.COMPLIANCE,
                retain_until_date='2025-01-01T00:00:00.000Z',
            ),
        )
        self.assertEqual('test-bucket', request.bucket)
        self.assertEqual('test-object', request.key)
        self.assertEqual('version123', request.version_id)
        self.assertTrue(request.bypass_governance_retention)
        self.assertEqual('COMPLIANCE', request.retention.mode)
        self.assertEqual('2025-01-01T00:00:00.000Z', request.retention.retain_until_date)

    def test_serialize_request(self):
        request = model.PutObjectRetentionRequest(
            bucket='test-bucket',
            key='test-object',
            version_id='version123',
            bypass_governance_retention=True,
            retention=model.Retention(
                mode=model.ObjectRetentionModeType.GOVERNANCE,
                retain_until_date='2025-01-01T00:00:00.000Z',
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutObjectRetention',
            method='PUT',
            bucket=request.bucket,
            key=request.key,
        ))
        self.assertEqual('PutObjectRetention', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('test-bucket', op_input.bucket)
        self.assertEqual('test-object', op_input.key)
        self.assertEqual('version123', op_input.parameters.get('versionId'))
        self.assertEqual(True, bool(op_input.headers.get('x-oss-bypass-governance-retention')))

    def test_constructor_result(self):
        result = model.PutObjectRetentionResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutObjectRetentionResult()
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


class TestGetObjectRetention(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetObjectRetentionRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetObjectRetentionRequest(
            bucket='test-bucket',
            key='test-object',
            version_id='version123',
        )
        self.assertEqual('test-bucket', request.bucket)
        self.assertEqual('test-object', request.key)
        self.assertEqual('version123', request.version_id)

    def test_serialize_request(self):
        request = model.GetObjectRetentionRequest(
            bucket='test-bucket',
            key='test-object',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetObjectRetention',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        ))
        self.assertEqual('GetObjectRetention', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('test-bucket', op_input.bucket)
        self.assertEqual('test-object', op_input.key)

    def test_constructor_result(self):
        result = model.GetObjectRetentionResult()
        self.assertIsNone(result.retention)
        self.assertIsInstance(result, serde.Model)

        result = model.GetObjectRetentionResult(
            retention=model.Retention(
                mode=model.ObjectRetentionModeType.GOVERNANCE,
                retain_until_date='2025-01-01T00:00:00.000Z',
            ),
        )
        self.assertEqual('GOVERNANCE', result.retention.mode)
        self.assertEqual('2025-01-01T00:00:00.000Z', result.retention.retain_until_date)

    def test_deserialize_result(self):
        xml_data = r'''
        <Retention>
        </Retention>'''

        result = model.GetObjectRetentionResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <Retention>
          <Mode>GOVERNANCE</Mode>
          <RetainUntilDate>2025-01-01T00:00:00.000Z</RetainUntilDate>
        </Retention>
        '''

        result = model.GetObjectRetentionResult()
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
        self.assertEqual('GOVERNANCE', result.retention.mode)
        self.assertEqual('2025-01-01T00:00:00.000Z', result.retention.retain_until_date)


class TestPutObjectLegalHold(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutObjectLegalHoldRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertIsNone(request.legal_hold)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutObjectLegalHoldRequest(
            bucket='test-bucket',
            key='test-object',
            version_id='version123',
            legal_hold=model.LegalHold(
                status=model.ObjectLegalHoldStatusType.ON,
            ),
        )
        self.assertEqual('test-bucket', request.bucket)
        self.assertEqual('test-object', request.key)
        self.assertEqual('version123', request.version_id)
        self.assertEqual('ON', request.legal_hold.status)

    def test_serialize_request(self):
        request = model.PutObjectLegalHoldRequest(
            bucket='test-bucket',
            key='test-object',
            legal_hold=model.LegalHold(
                status=model.ObjectLegalHoldStatusType.OFF,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutObjectLegalHold',
            method='PUT',
            bucket=request.bucket,
            key=request.key,
        ))
        self.assertEqual('PutObjectLegalHold', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('test-bucket', op_input.bucket)
        self.assertEqual('test-object', op_input.key)

    def test_constructor_result(self):
        result = model.PutObjectLegalHoldResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutObjectLegalHoldResult()
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


class TestGetObjectLegalHold(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetObjectLegalHoldRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.key)
        self.assertIsNone(request.version_id)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetObjectLegalHoldRequest(
            bucket='test-bucket',
            key='test-object',
            version_id='version123',
        )
        self.assertEqual('test-bucket', request.bucket)
        self.assertEqual('test-object', request.key)
        self.assertEqual('version123', request.version_id)

    def test_serialize_request(self):
        request = model.GetObjectLegalHoldRequest(
            bucket='test-bucket',
            key='test-object',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetObjectLegalHold',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        ))
        self.assertEqual('GetObjectLegalHold', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('test-bucket', op_input.bucket)
        self.assertEqual('test-object', op_input.key)

    def test_constructor_result(self):
        result = model.GetObjectLegalHoldResult()
        self.assertIsNone(result.legal_hold)
        self.assertIsInstance(result, serde.Model)

        result = model.GetObjectLegalHoldResult(
            legal_hold=model.LegalHold(
                status=model.ObjectLegalHoldStatusType.ON,
            ),
        )
        self.assertEqual('ON', result.legal_hold.status)

    def test_deserialize_result(self):
        xml_data = r'''
        <LegalHold>
        </LegalHold>'''

        result = model.GetObjectLegalHoldResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <LegalHold>
          <Status>ON</Status>
        </LegalHold>
        '''

        result = model.GetObjectLegalHoldResult()
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
        self.assertEqual('ON', result.legal_hold.status)
