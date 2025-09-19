# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.vectors.models import bucket_logging as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from ... import MockHttpResponse


class TestPutBucketLogging(unittest.TestCase):
    def test_constructor_request(self):
        """
        Test PutBucketLoggingRequest constructor
        """
        request = model.PutBucketLoggingRequest()
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.bucket_logging_status)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketLoggingRequest(
            bucket='examplebucket',
            bucket_logging_status=model.BucketLoggingStatus(
                logging_enabled=model.LoggingEnabled(
                    target_bucket='examplebucket',
                    target_prefix='MyLog-',
                    logging_role='AliyunOSSLoggingDefaultRole'
                )
            )
        )
        self.assertEqual('examplebucket', request.bucket)
        self.assertIsNotNone(request.bucket_logging_status)
        self.assertIsNotNone(request.bucket_logging_status.logging_enabled)
        self.assertEqual('examplebucket', request.bucket_logging_status.logging_enabled.target_bucket)
        self.assertEqual('MyLog-', request.bucket_logging_status.logging_enabled.target_prefix)
        self.assertEqual('AliyunOSSLoggingDefaultRole', request.bucket_logging_status.logging_enabled.logging_role)

    def test_serialize_request(self):
        """
        Test PutBucketLoggingRequest serialization
        """
        request = model.PutBucketLoggingRequest(
            bucket='examplebucket',
            bucket_logging_status=model.BucketLoggingStatus(
                logging_enabled=model.LoggingEnabled(
                    target_bucket='examplebucket',
                    target_prefix='MyLog-',
                    logging_role='AliyunOSSLoggingDefaultRole'
                )
            )
        )

        json_str = '{"BucketLoggingStatus": {"LoggingEnabled": {"TargetBucket": "examplebucket", "TargetPrefix": "MyLog-", "LoggingRole": "AliyunOSSLoggingDefaultRole"}}}'

        op_input = serde.serialize_input_json(request, OperationInput(
            op_name='PutBucketLogging',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketLogging', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('examplebucket', op_input.bucket)
        self.assertEqual(json_str, op_input.body.decode())

    def test_constructor_result(self):
        """
        Test PutBucketLoggingResult constructor
        """
        result = model.PutBucketLoggingResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        """
        Test PutBucketLoggingResult deserialization
        """
        json_data = None
        result = model.PutBucketLoggingResult()
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
                    body=json_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))


class TestGetBucketLogging(unittest.TestCase):
    def test_constructor_request(self):
        """
        Test GetBucketLoggingRequest constructor
        """
        request = model.GetBucketLoggingRequest()
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketLoggingRequest(
            bucket='examplebucket',
        )
        self.assertEqual('examplebucket', request.bucket)

    def test_serialize_request(self):
        """
        Test GetBucketLoggingRequest serialization
        """
        request = model.GetBucketLoggingRequest(
            bucket='examplebucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketLogging',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketLogging', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('examplebucket', op_input.bucket)

    def test_constructor_result(self):
        """
        Test GetBucketLoggingResult constructor
        """
        result = model.GetBucketLoggingResult()
        self.assertIsNone(result.bucket_logging_status)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketLoggingResult(
            bucket_logging_status=model.BucketLoggingStatus(
                logging_enabled=model.LoggingEnabled(
                    target_bucket='mybucketlogs',
                    target_prefix='mybucket-access_log/',
                    logging_role='AliyunOSSLoggingDefaultRole'
                )
            )
        )
        self.assertIsNotNone(result.bucket_logging_status)
        self.assertIsNotNone(result.bucket_logging_status.logging_enabled)
        self.assertEqual('mybucketlogs', result.bucket_logging_status.logging_enabled.target_bucket)
        self.assertEqual('mybucket-access_log/', result.bucket_logging_status.logging_enabled.target_prefix)
        self.assertEqual('AliyunOSSLoggingDefaultRole', result.bucket_logging_status.logging_enabled.logging_role)

    def test_deserialize_result_with_logging_enabled(self):
        """
        Test GetBucketLoggingResult deserialization with logging enabled
        """
        json_data = r'''
        {
          "BucketLoggingStatus": {
            "LoggingEnabled": {
              "TargetBucket": "mybucketlogs",
              "TargetPrefix": "mybucket-access_log/",
              "LoggingRole": "AliyunOSSLoggingDefaultRole"
            }
          }
        }'''

        result = model.GetBucketLoggingResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        deserializer = [serde.deserialize_output_jsonbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertIsNotNone(result.bucket_logging_status)
        self.assertIsNotNone(result.bucket_logging_status.logging_enabled)
        self.assertEqual('mybucketlogs', result.bucket_logging_status.logging_enabled.target_bucket)
        self.assertEqual('mybucket-access_log/', result.bucket_logging_status.logging_enabled.target_prefix)
        self.assertEqual('AliyunOSSLoggingDefaultRole', result.bucket_logging_status.logging_enabled.logging_role)

    def test_deserialize_result_without_logging_enabled(self):
        """
        Test GetBucketLoggingResult deserialization without logging enabled
        """
        json_data = r'''
        {
            "BucketLoggingStatus": {
            }
        }'''

        result = model.GetBucketLoggingResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        deserializer = [serde.deserialize_output_jsonbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertIsNotNone(result.bucket_logging_status)
        self.assertIsNone(result.bucket_logging_status.logging_enabled)


class TestDeleteBucketLogging(unittest.TestCase):
    def test_constructor_request(self):
        """
        Test DeleteBucketLoggingRequest constructor
        """
        request = model.DeleteBucketLoggingRequest()
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketLoggingRequest(
            bucket='examplebucket',
        )
        self.assertEqual('examplebucket', request.bucket)

    def test_serialize_request(self):
        """
        Test DeleteBucketLoggingRequest serialization
        """
        request = model.DeleteBucketLoggingRequest(
            bucket='examplebucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketLogging',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketLogging', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('examplebucket', op_input.bucket)

    def test_constructor_result(self):
        """
        Test DeleteBucketLoggingResult constructor
        """
        result = model.DeleteBucketLoggingResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        """
        Test DeleteBucketLoggingResult deserialization
        """
        json_data = None
        result = model.DeleteBucketLoggingResult()
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
                    body=json_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
