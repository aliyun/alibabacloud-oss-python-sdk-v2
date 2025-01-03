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
                    json=model.JSONInput(
                        type='DOCUMENT|LINES',
                        range='line-range=start-end|split-range=start-end',
                        parse_json_number_as_string=True,
                    ),
                    csv=model.CSVInput(
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
                    csv=model.CSVOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character=base64.b64encode('\"'.encode()).decode(),
                    ),
                    json=model.JSONOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                    ),
                    output_raw_data=False,
                    keep_all_columns=True,
                    enable_payload_crc=True,
                    output_header=False,
                ),
                options=model.SelectRequestOptions(
                    skip_partial_data_record=True,
                    max_skipped_records_allowed=111,
                ),
            ),
        )

        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual(base64.b64encode('select * from ossobject as s where cast(s.age as int) > 40'.encode()).decode(), request.select_request.expression)
        self.assertEqual('GZIP', request.select_request.input_serialization.compression_type)
        self.assertEqual('DOCUMENT|LINES', request.select_request.input_serialization.json.type)
        self.assertEqual('line-range=start-end|split-range=start-end', request.select_request.input_serialization.json.range)
        self.assertEqual(True, request.select_request.input_serialization.json.parse_json_number_as_string)
        self.assertEqual('DOCUMENT|LINES', request.select_request.input_serialization.csv.file_header_info)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.input_serialization.csv.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.select_request.input_serialization.csv.field_delimiter)
        self.assertEqual('\"', request.select_request.input_serialization.csv.quote_character)
        self.assertEqual('#', request.select_request.input_serialization.csv.comment_character)
        self.assertEqual('line-range=start-end', request.select_request.input_serialization.csv.range)
        self.assertEqual(True, request.select_request.input_serialization.csv.allow_quoted_record_delimiter)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.output_serialization.csv.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.select_request.output_serialization.csv.field_delimiter)
        self.assertEqual(base64.b64encode('\"'.encode()).decode(), request.select_request.output_serialization.csv.quote_character)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.output_serialization.json.record_delimiter)
        self.assertEqual(False, request.select_request.output_serialization.output_raw_data)
        self.assertEqual(True, request.select_request.output_serialization.keep_all_columns)
        self.assertEqual(True, request.select_request.output_serialization.enable_payload_crc)
        self.assertEqual(False, request.select_request.output_serialization.output_header)
        self.assertEqual(True, request.select_request.options.skip_partial_data_record)
        self.assertEqual(111, request.select_request.options.max_skipped_records_allowed)

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
            process="json/select",
            select_request=model.SelectRequest(
                expression=base64.b64encode('select * from ossobject as s where cast(s.age as int) > 40'.encode()).decode(),
                input_serialization=model.InputSerialization(
                    compression_type='GZIP',
                    json=model.JSONInput(
                        type='DOCUMENT|LINES',
                        range='line-range=start-end|split-range=start-end',
                        parse_json_number_as_string=True,
                    ),
                    csv=model.CSVInput(
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
                    csv=model.CSVOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character=base64.b64encode('\"'.encode()).decode(),
                    ),
                    json=model.JSONOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                    ),
                    output_raw_data=False,
                    keep_all_columns=True,
                    enable_payload_crc=True,
                    output_header=False,
                ),
                options=model.SelectRequestOptions(
                    skip_partial_data_record=True,
                    max_skipped_records_allowed=111,
                ),
            ),
        )

        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('json/select', request.process)
        self.assertEqual(base64.b64encode('select * from ossobject as s where cast(s.age as int) > 40'.encode()).decode(), request.select_request.expression)
        self.assertEqual('GZIP', request.select_request.input_serialization.compression_type)
        self.assertEqual('DOCUMENT|LINES', request.select_request.input_serialization.json.type)
        self.assertEqual('line-range=start-end|split-range=start-end', request.select_request.input_serialization.json.range)
        self.assertEqual(True, request.select_request.input_serialization.json.parse_json_number_as_string)
        self.assertEqual('DOCUMENT|LINES', request.select_request.input_serialization.csv.file_header_info)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.input_serialization.csv.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.select_request.input_serialization.csv.field_delimiter)
        self.assertEqual('\"', request.select_request.input_serialization.csv.quote_character)
        self.assertEqual('#', request.select_request.input_serialization.csv.comment_character)
        self.assertEqual('line-range=start-end', request.select_request.input_serialization.csv.range)
        self.assertEqual(True, request.select_request.input_serialization.csv.allow_quoted_record_delimiter)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.output_serialization.csv.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.select_request.output_serialization.csv.field_delimiter)
        self.assertEqual(base64.b64encode('\"'.encode()).decode(), request.select_request.output_serialization.csv.quote_character)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_request.output_serialization.csv.record_delimiter)
        self.assertEqual(False, request.select_request.output_serialization.output_raw_data)
        self.assertEqual(True, request.select_request.output_serialization.keep_all_columns)
        self.assertEqual(True, request.select_request.output_serialization.enable_payload_crc)
        self.assertEqual(False, request.select_request.output_serialization.output_header)
        self.assertEqual(True, request.select_request.options.skip_partial_data_record)
        self.assertEqual(111, request.select_request.options.max_skipped_records_allowed)

        op_input = serde.serialize_input(request, OperationInput(
            op_name='SelectObject',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('SelectObject', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)
        self.assertEqual('json/select', op_input.parameters.get('x-oss-process'))

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
    
    def test_constructor_request_csv(self):
        request = model.CreateSelectObjectMetaRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.key)
        self.assertIsNone(request.process)
        self.assertIsNone(request.select_meta_request)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CreateSelectObjectMetaRequest(
            bucket='bucketexampletest',
            key='test_key',
            process='csv/select',
            select_meta_request=model.CSVMetaRequest(
                input_serialization=model.InputSerialization(
                    compression_type='GZIP',
                    csv=model.CSVInput(
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
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_key', request.key)
        self.assertEqual('csv/select', request.process)
        self.assertEqual('GZIP', request.select_meta_request.input_serialization.compression_type)
        self.assertEqual('"', request.select_meta_request.input_serialization.csv.quote_character)
        self.assertEqual('#', request.select_meta_request.input_serialization.csv.comment_character)
        self.assertEqual('line-range=start-end', request.select_meta_request.input_serialization.csv.range)
        self.assertEqual(True, request.select_meta_request.input_serialization.csv.allow_quoted_record_delimiter)
        self.assertEqual(False, request.select_meta_request.overwrite_if_exists)
        self.assertEqual('DOCUMENT|LINES', request.select_meta_request.input_serialization.csv.file_header_info)
        self.assertEqual(base64.b64encode('\n'.encode()).decode(), request.select_meta_request.input_serialization.csv.record_delimiter)
        self.assertEqual(base64.b64encode(','.encode()).decode(), request.select_meta_request.input_serialization.csv.field_delimiter)

    def test_constructor_request_json(self):
        request = model.CreateSelectObjectMetaRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.key)
        self.assertIsNone(request.process)
        self.assertIsNone(request.select_meta_request)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CreateSelectObjectMetaRequest(
            bucket='bucketexampletest',
            key='test_key',
            process='json/select',
            select_meta_request=model.JSONMetaRequest(
                input_serialization=model.InputSerialization(
                    compression_type='None',
                    json=model.JSONInput(
                        type='LINES',
                        range='split-range=10-20',
                        parse_json_number_as_string=False,
                    ),
                ),
                overwrite_if_exists=True,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_key', request.key)
        self.assertEqual('json/select', request.process)
        self.assertEqual('None', request.select_meta_request.input_serialization.compression_type)
        self.assertEqual('LINES', request.select_meta_request.input_serialization.json.type)
        self.assertEqual('split-range=10-20', request.select_meta_request.input_serialization.json.range)
        self.assertEqual(False, request.select_meta_request.input_serialization.json.parse_json_number_as_string)
        self.assertEqual(True, request.select_meta_request.overwrite_if_exists)


    def test_serialize_request_csv(self):
        request = model.CreateSelectObjectMetaRequest(
            bucket='bucketexampletest',
            key='test_key',
            process='csv/select',
            select_meta_request=model.CSVMetaRequest(
                input_serialization=model.InputSerialization(
                    compression_type='GZIP',
                    csv=model.CSVInput(
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
        self.assertEqual('csv/select', op_input.parameters.get('x-oss-process'))
        
        root = ET.fromstring(op_input.body)
        self.assertEqual('CsvMetaRequest', root.tag)


    def test_serialize_request_json(self):
        request = model.CreateSelectObjectMetaRequest(
            bucket='bucketexampletest',
            key='test_key',
            process='json/select',
            select_meta_request=model.JSONMetaRequest(
                input_serialization=model.InputSerialization(
                    compression_type='GZIP',
                    json=model.JSONInput(
                        type='DOCUMENT|LINES',
                        range='line-range=start-end|split-range=start-end',
                        parse_json_number_as_string=True,
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
        self.assertEqual('json/select', op_input.parameters.get('x-oss-process'))
        
        root = ET.fromstring(op_input.body)
        self.assertEqual('JsonMetaRequest', root.tag)        

    def test_constructor_result(self):
        result = model.CreateSelectObjectMetaResult()
        self.assertIsNone(result.offset)
        self.assertIsNone(result.total_scanned_bytes)
        self.assertIsNone(result.splits_count)
        self.assertIsNone(result.rows_count)
        self.assertIsInstance(result, serde.Model)

        result = model.CreateSelectObjectMetaResult(
            offset = 1,
            total_scanned_bytes=2,
            splits_count=3,
            rows_count=4,
        )
        self.assertEqual(1, result.offset)
        self.assertEqual(2, result.total_scanned_bytes)
        self.assertEqual(3, result.splits_count)
        self.assertEqual(4, result.rows_count)

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

