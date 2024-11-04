# pylint: skip-file
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_access_monitor as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketAccessMonitor(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketAccessMonitorRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_monitor_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketAccessMonitorRequest(
            bucket='bucket_name',
            access_monitor_configuration=model.AccessMonitorConfiguration(
                status=model.AccessMonitorStatusType.DISABLED
            ),
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual(model.AccessMonitorStatusType.DISABLED, request.access_monitor_configuration.status)

        request = model.PutBucketAccessMonitorRequest(
            bucket='bucket_name',
            access_monitor_configuration=model.AccessMonitorConfiguration(
                status='Enabled'
            ),
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('Enabled', request.access_monitor_configuration.status)

    def test_serialize_request(self):
        request = model.PutBucketAccessMonitorRequest(
            bucket='bucket_name',
            access_monitor_configuration=model.AccessMonitorConfiguration(
                status=model.AccessMonitorStatusType.DISABLED
            ),
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual(model.AccessMonitorStatusType.DISABLED, request.access_monitor_configuration.status)

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketAccessMonitor',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketAccessMonitor', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketAccessMonitorResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketAccessMonitorResult()
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


class TestGetBucketAccessMonitor(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketAccessMonitorRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketAccessMonitorRequest(
            bucket='bucket_name',
        )
        self.assertEqual('bucket_name', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketAccessMonitorRequest(
            bucket='bucket_name',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketAccessMonitor',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketAccessMonitor', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketAccessMonitorResult()
        self.assertIsNone(result.access_monitor_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketAccessMonitorResult(
            access_monitor_configuration=model.AccessMonitorConfiguration(
                status=model.AccessMonitorStatusType.ENABLED
            ),
        )
        self.assertEqual(model.AccessMonitorStatusType.ENABLED, result.access_monitor_configuration.status)

        result = model.GetBucketAccessMonitorResult(
            access_monitor_configuration=model.AccessMonitorConfiguration(
                status='Disabled'
            ),
        )
        self.assertEqual('Disabled', result.access_monitor_configuration.status)

    def test_deserialize_result(self):
        xml_data = r'''
        <AccessMonitorConfiguration>
        </AccessMonitorConfiguration>'''

        result = model.GetBucketAccessMonitorResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <AccessMonitorConfiguration>
          <Status>Enabled</Status>
        </AccessMonitorConfiguration>
        '''

        result = model.GetBucketAccessMonitorResult()
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
        self.assertEqual('Enabled', result.access_monitor_configuration.status)

