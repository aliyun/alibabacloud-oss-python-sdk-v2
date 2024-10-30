# pylint: skip-file
import base64
from typing import cast
from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.models import select_object_basic as model
from alibabacloud_oss_v2.operations import select_object_basic as operations
from . import TestOperations

class TestSelectObject(TestOperations):
    def test_select_object(self):
        request = model.SelectObjectRequest(
            bucket='bucket',
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
                ),
                output_serialization=model.OutputSerialization(
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

        result = operations.select_object(self.client, request)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?x-oss-process=json%2Fselect', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)
        self.assertEqual('requester', self.request_dump.headers.get('x-oss-request-payer'))


    def test_select_object_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.SelectObjectRequest(
            bucket='bucket',
            key='example-object-2.jpg',
            select_request=model.SelectRequest(
                expression=base64.b64encode(
                    'select * from ossobject as s where cast(s.age as int) > 40'.encode()).decode(),
                input_serialization=model.InputSerialization(
                    compression_type='GZIP',
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
            ),
        )

        try:
            result = operations.select_object(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/example-object-2.jpg?x-oss-process=csv%2Fselect', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)