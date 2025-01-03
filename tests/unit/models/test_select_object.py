# pylint: skip-file
import base64
import unittest
import xml.etree.ElementTree as ET
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import select_object as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from .. import MockHttpResponse


class TestSelectObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.SelectObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsNotNone(request.key)
        self.assertIsNone(request.select_request)
        self.assertIsNone(request.request_payer)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.SelectObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            select_request=model.SelectRequest(
                expression=base64.b64encode('select * from ossobject as s where cast(s.age as int) > 40'.encode()).decode(),
                input_serialization=model.InputSerialization(
                    compression_type='GZIP',
                    json_input=model.JSONInput(
                        type='DOCUMENT|LINES',
                        range='line-range=start-end|split-range=start-end',
                        parse_json_number_as_string=True,
                    ),
                    csv_input=model.CSVInput(
                        file_header_info='DOCUMENT|LINES',
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character='\"',
                        comment_character='#',
                        range='line-range=start-end',
                        allow_quoted_record_delimiter=True,
                    ),
                ),
                output_serialization=model.OutputSerialization(
                    csv_output=model.CSVOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character=base64.b64encode('\"'.encode()).decode(),
                    ),
                    json_output=model.JSONOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                    ),
                    output_raw_data=False,
                    keep_all_columns=True,
                    enable_payload_crc=True,
                    output_header=False,
                ),
                options=model.SelectOptions(
                    skip_partial_data_record=True,
                    max_skipped_records_allowed=111,
                ),
            ),
            request_payer='requester',
        )

        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual(base64.b64encode('select * from ossobject as s where cast(s.age as int) > 40'.encode()).decode(), request.select_request.expression)
        self.assertEqual('GZIP', request.select_request.input_serialization.compression_type)
        self.assertEqual('DOCUMENT|LINES', request.select_request.input_serialization.json_input.type)
        self.assertEqual('line-range=start-end|split-range=start-end', request.select_request.input_serialization.json_input.range)
        self.assertEqual(True, request.select_request.input_serialization.json_input.parse_json_number_as_string)
        self.assertEqual('DOCUMENT|LINES', request.select_request.input_serialization.csv_input.file_header_info)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.input_serialization.csv_input.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.select_request.input_serialization.csv_input.field_delimiter)
        self.assertEqual('\"', request.select_request.input_serialization.csv_input.quote_character)
        self.assertEqual('#', request.select_request.input_serialization.csv_input.comment_character)
        self.assertEqual('line-range=start-end', request.select_request.input_serialization.csv_input.range)
        self.assertEqual(True, request.select_request.input_serialization.csv_input.allow_quoted_record_delimiter)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.output_serialization.csv_output.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.select_request.output_serialization.csv_output.field_delimiter)
        self.assertEqual(base64.b64encode('\"'.encode()).decode(), request.select_request.output_serialization.csv_output.quote_character)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.output_serialization.json_output.record_delimiter)
        self.assertEqual(False, request.select_request.output_serialization.output_raw_data)
        self.assertEqual(True, request.select_request.output_serialization.keep_all_columns)
        self.assertEqual(True, request.select_request.output_serialization.enable_payload_crc)
        self.assertEqual(False, request.select_request.output_serialization.output_header)
        self.assertEqual(True, request.select_request.options.skip_partial_data_record)
        self.assertEqual(111, request.select_request.options.max_skipped_records_allowed)
        self.assertEqual('requester', request.request_payer)


        request = model.SelectObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('bucket_name', request.bucket)
        self.assertTrue(hasattr(request, 'key'))
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertFalse(hasattr(request, 'invalid_field'))

        request = model.SelectObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.SelectObjectRequest(
            bucket='bucket_name',
            key='example-object-2.jpg',
            select_request=model.SelectRequest(
                expression=base64.b64encode('select * from ossobject as s where cast(s.age as int) > 40'.encode()).decode(),
                input_serialization=model.InputSerialization(
                    compression_type='GZIP',
                    json_input=model.JSONInput(
                        type='DOCUMENT|LINES',
                        range='line-range=start-end|split-range=start-end',
                        parse_json_number_as_string=True,
                    ),
                    csv_input=model.CSVInput(
                        file_header_info='DOCUMENT|LINES',
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character='\"',
                        comment_character='#',
                        range='line-range=start-end',
                        allow_quoted_record_delimiter=True,
                    ),
                ),
                output_serialization=model.OutputSerialization(
                    csv_output=model.CSVOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character=base64.b64encode('\"'.encode()).decode(),
                    ),
                    json_output=model.JSONOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                    ),
                    output_raw_data=False,
                    keep_all_columns=True,
                    enable_payload_crc=True,
                    output_header=False,
                ),
                options=model.SelectOptions(
                    skip_partial_data_record=True,
                    max_skipped_records_allowed=111,
                ),
            ),
            request_payer='requester',
        )

        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual(base64.b64encode('select * from ossobject as s where cast(s.age as int) > 40'.encode()).decode(), request.select_request.expression)
        self.assertEqual('GZIP', request.select_request.input_serialization.compression_type)
        self.assertEqual('DOCUMENT|LINES', request.select_request.input_serialization.json_input.type)
        self.assertEqual('line-range=start-end|split-range=start-end', request.select_request.input_serialization.json_input.range)
        self.assertEqual(True, request.select_request.input_serialization.json_input.parse_json_number_as_string)
        self.assertEqual('DOCUMENT|LINES', request.select_request.input_serialization.csv_input.file_header_info)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.input_serialization.csv_input.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.select_request.input_serialization.csv_input.field_delimiter)
        self.assertEqual('\"', request.select_request.input_serialization.csv_input.quote_character)
        self.assertEqual('#', request.select_request.input_serialization.csv_input.comment_character)
        self.assertEqual('line-range=start-end', request.select_request.input_serialization.csv_input.range)
        self.assertEqual(True, request.select_request.input_serialization.csv_input.allow_quoted_record_delimiter)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.output_serialization.csv_output.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.select_request.output_serialization.csv_output.field_delimiter)
        self.assertEqual(base64.b64encode('\"'.encode()).decode(), request.select_request.output_serialization.csv_output.quote_character)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.output_serialization.json_output.record_delimiter)
        self.assertEqual(False, request.select_request.output_serialization.output_raw_data)
        self.assertEqual(True, request.select_request.output_serialization.keep_all_columns)
        self.assertEqual(True, request.select_request.output_serialization.enable_payload_crc)
        self.assertEqual(False, request.select_request.output_serialization.output_header)
        self.assertEqual(True, request.select_request.options.skip_partial_data_record)
        self.assertEqual(111, request.select_request.options.max_skipped_records_allowed)
        self.assertEqual('requester', request.request_payer)

        op_input = serde.serialize_input(request, OperationInput(
            op_name='SelectObject',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('SelectObject', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('requester', op_input.headers.get('x-oss-request-payer'))

        root = ET.fromstring(op_input.body)
        self.assertEqual('SelectRequest', root.tag)
        self.assertEqual(base64.b64encode('select * from ossobject as s where cast(s.age as int) > 40'.encode()).decode(), root.findtext('Expression'))


    def test_constructor_result(self):
        result = model.SelectObjectResult()
        self.assertIsNone(result.body)
        self.assertIsInstance(result, serde.Model)

        result = model.SelectObjectResult(
            invalid_field='invalid_field',
        )
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = None
        result = model.SelectObjectResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                    'x-oss-select-output-raw': 'false',
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
        self.assertEqual('false', result.headers.get('x-oss-select-output-raw'))



class TestCreateSelectObjectMeta(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CreateSelectObjectMetaRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.key)
        self.assertIsNone(request.csv_meta_request)
        self.assertIsNone(request.json_meta_request)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CreateSelectObjectMetaRequest(
            bucket='bucketexampletest',
            key='test_key',
            csv_meta_request=model.CsvMetaRequest(
                input_serialization=model.InputSerialization(
                    compression_type='GZIP',
                    json_input=model.JSONInput(
                        type='DOCUMENT|LINES',
                        range='line-range=start-end|split-range=start-end',
                        parse_json_number_as_string=True,
                    ),
                    csv_input=model.CSVInput(
                        file_header_info='DOCUMENT|LINES',
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character='"',
                        comment_character='#',
                        range='line-range=start-end',
                        allow_quoted_record_delimiter=True,
                    ),
                ),
                overwrite_if_exists=False,
            ),
            json_meta_request=model.JsonMetaRequest(
                input_serialization=model.InputSerialization(
                    compression_type='None',
                    json_input=model.JSONInput(
                        type='LINES',
                        range='split-range=10-20',
                        parse_json_number_as_string=False,
                    ),
                    csv_input=model.CSVInput(
                        file_header_info='DOCUMENT',
                        record_delimiter=base64.b64encode('\n\r'.encode()).decode(),
                        field_delimiter=base64.b64encode(',.'.encode()).decode(),
                        quote_character='\\',
                        comment_character='//',
                        range='split-range=20-660',
                        allow_quoted_record_delimiter=False,
                    ),
                ),
                overwrite_if_exists=True,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_key', request.key)
        self.assertEqual('GZIP', request.csv_meta_request.input_serialization.compression_type)
        self.assertEqual('DOCUMENT|LINES', request.csv_meta_request.input_serialization.json_input.type)
        self.assertEqual('line-range=start-end|split-range=start-end', request.csv_meta_request.input_serialization.json_input.range)
        self.assertEqual(True, request.csv_meta_request.input_serialization.json_input.parse_json_number_as_string)
        self.assertEqual('DOCUMENT|LINES', request.csv_meta_request.input_serialization.csv_input.file_header_info)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.csv_meta_request.input_serialization.csv_input.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.csv_meta_request.input_serialization.csv_input.field_delimiter)
        self.assertEqual('"', request.csv_meta_request.input_serialization.csv_input.quote_character)
        self.assertEqual('#', request.csv_meta_request.input_serialization.csv_input.comment_character)
        self.assertEqual('line-range=start-end', request.csv_meta_request.input_serialization.csv_input.range)
        self.assertEqual(True, request.csv_meta_request.input_serialization.csv_input.allow_quoted_record_delimiter)
        self.assertEqual(False, request.csv_meta_request.overwrite_if_exists)
        self.assertEqual('None', request.json_meta_request.input_serialization.compression_type)
        self.assertEqual('LINES', request.json_meta_request.input_serialization.json_input.type)
        self.assertEqual('split-range=10-20', request.json_meta_request.input_serialization.json_input.range)
        self.assertEqual(False, request.json_meta_request.input_serialization.json_input.parse_json_number_as_string)
        self.assertEqual('DOCUMENT', request.json_meta_request.input_serialization.csv_input.file_header_info)
        self.assertEqual(base64.b64encode('\n\r'.encode()).decode(), request.json_meta_request.input_serialization.csv_input.record_delimiter)
        self.assertEqual(base64.b64encode(',.'.encode()).decode(), request.json_meta_request.input_serialization.csv_input.field_delimiter)
        self.assertEqual('\\', request.json_meta_request.input_serialization.csv_input.quote_character)
        self.assertEqual('//', request.json_meta_request.input_serialization.csv_input.comment_character)
        self.assertEqual('split-range=20-660', request.json_meta_request.input_serialization.csv_input.range)
        self.assertEqual(False, request.json_meta_request.input_serialization.csv_input.allow_quoted_record_delimiter)
        self.assertEqual(True, request.json_meta_request.overwrite_if_exists)

    def test_serialize_request(self):
        request = model.CreateSelectObjectMetaRequest(
            bucket='bucketexampletest',
            key='test_key',
            csv_meta_request=model.CsvMetaRequest(
                input_serialization=model.InputSerialization(
                    compression_type='GZIP',
                    json_input=model.JSONInput(
                        type='DOCUMENT|LINES',
                        range='line-range=start-end|split-range=start-end',
                        parse_json_number_as_string=True,
                    ),
                    csv_input=model.CSVInput(
                        file_header_info='DOCUMENT|LINES',
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character='\"',
                        comment_character='#',
                        range='line-range=start-end',
                        allow_quoted_record_delimiter=True,
                    ),
                ),
                overwrite_if_exists=False,
            )
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CreateSelectObjectMeta',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CreateSelectObjectMeta', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.CreateSelectObjectMetaResult()
        self.assertIsNone(result.body)
        self.assertIsInstance(result, serde.Model)

        result = model.CreateSelectObjectMetaResult(
            body=model.SelectResult(
                resp=MockHttpResponse(),
                progress_callback='progress_callback',
                content_length=11,
                crc_enabled=False,
            ),
        )
        self.assertEqual('progress_callback', result.body.select_resp.callback)
        self.assertEqual(11, result.body.select_resp.content_length)
        self.assertEqual(False, result.body.select_resp.enable_crc)

    def test_deserialize_result(self):
        xml_data = None
        result = model.CreateSelectObjectMetaResult()
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

