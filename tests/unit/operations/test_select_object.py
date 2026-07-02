# pylint: skip-file
from typing import cast
from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.models import select_object as model
from alibabacloud_oss_v2.operations.select_object import select_object, create_select_object_meta
from . import TestOperations
from .. import MockHttpResponse

class TestSelectObject(TestOperations):

    def test_select_object_not_requried_args(self):
        try:
            request = model.SelectObjectRequest(
                #bucket='bucket',
                #key='key',
                #process='csv/select'
            )
            result = select_object(self.client, request)
            self.fail('should not here')
        except exceptions.ParamRequiredError as ope:
            """"""

        try:
            request = model.SelectObjectRequest(
                bucket='bucket',
                #key='key',
                #process='csv/select'
            )
            result = select_object(self.client, request)
            self.fail('should not here')
        except exceptions.ParamRequiredError as ope:
            """"""

        try:
            request = model.SelectObjectRequest(
                bucket='bucket',
                key='key',
                #process='csv/select'
            )
            result = select_object(self.client, request)
            self.fail('should not here')
        except exceptions.ParamRequiredError as ope:
            """"""

        try:
            request = model.SelectObjectRequest(
                bucket='bucket',
                key='key',
                process='csv/select'
            )
            result = select_object(self.client, request)
            self.fail('should not here')
        except exceptions.ParamRequiredError as ope:
            """"""

        request = model.SelectObjectRequest(
            bucket='bucket',
            key='key',
            process='csv/select',
            select_request=model.SelectRequest(),
        )
        result = select_object(self.client, request)


    def test_test_select_object_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.SelectObjectRequest(
            bucket='bucket',
            key='key',
            process='csv/select',
            select_request=model.SelectRequest(),
        )

        try:
            result = select_object(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/key?x-oss-process=csv%2Fselect', self.request_dump.url)
        self.assertEqual('POST', self.request_dump.method)

    def test_create_select_object_meta_not_requried_args(self):
        try:
            request = model.CreateSelectObjectMetaRequest(
                #bucket='bucket',
                #key='key',
                #process='csv/meta'
            )
            result = create_select_object_meta(self.client, request)
            self.fail('should not here')
        except exceptions.ParamRequiredError as ope:
            """"""

        try:
            request = model.CreateSelectObjectMetaRequest(
                bucket='bucket',
                #key='key',
                #process='csv/meta'
            )
            result = create_select_object_meta(self.client, request)
            self.fail('should not here')
        except exceptions.ParamRequiredError as ope:
            """"""

        try:
            request = model.CreateSelectObjectMetaRequest(
                bucket='bucket',
                key='key',
                #process='csv/meta'
            )
            result = create_select_object_meta(self.client, request)
            self.fail('should not here')
        except exceptions.ParamRequiredError as ope:
            """"""

        try:
            request = model.CreateSelectObjectMetaRequest(
                bucket='bucket',
                key='key',
                process='csv/meta'
            )
            result = create_select_object_meta(self.client, request)
            self.fail('should not here')
        except exceptions.ParamRequiredError as ope:
            """"""

        request = model.CreateSelectObjectMetaRequest(
            bucket='bucket',
            key='key',
            process='csv/meta',
            select_meta_request = model.CreateSelectObjectMetaRequest(),
        )
        result = create_select_object_meta(self.client, request)


    def test_select_object_response_with_error(self):
        def response_invalid() -> MockHttpResponse:
            data = b'\0x01\0x80\0x00\0x06\0x00\0x00\0x00\0x25,0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0xc5\0x00\0x00\0x00\0x00,0x00\0x00\0x00\0xc5\0x00\0x00\0x00\0xc8\0x00\0x00\0x00\0x01\0x00\0x00\0x00\0x00,0x00\0x00\0x00\0x05\0x00\0x00\0x00\0x04\0x2e\0x78\0x95\0x1f\0x00'
            return MockHttpResponse(
                status_code=206,
                reason='OK',
                headers={
                    'Server': 'AliyunOSS',
                    'Date': 'Tue, 23 Jul 2024 13:01:06 GMT',
                    'Content-Type': 'application/xml',
                    'x-oss-ec': '0002-00000902',
                    'x-oss-request-id': 'id-1234',
                    'x-oss-select-output-raw': 'false',
                },
                body=data
            )

        self.set_responseFunc(response_invalid)

        try:
            request = model.SelectObjectRequest(
                bucket='bucket',
                key='key',
                process='csv/meta',
                select_request = model.SelectRequest(),
            )
            result = select_object(self.client, request)
            self.assertEqual(206, result.status_code)
            result.body.read()
            self.fail('should not here')
        except Exception as e:
            self.assertTrue(str(e).__contains__("Unexpected frame type"))


    # Real framed response bytes captured from the server for a csv/select
    # request with enable_payload_crc=True. Layout: two DATA frames + END frame.
    # Each DATA frame ends with a 4-byte crc32 checksum over its payload.
    _SELECT_CRC_FRAMES = bytes.fromhex(
        '018000010000008500000000000000000000007d4c6f7261204672616e6369732c5363686f6f6c2c537461706c657320496e632c32370a456c65616e6f72204c6974746c652c5363686f6f6c2c22436f6e65637469762c20496e63222c34330a526f736965204875676865732c5363686f6f6c2c5765737465726e20476173205265736f757263657320496e632c34340a5b34e125018000010000002d0000000000000000000000a24c617772656e636520526f73732c5363686f6f6c2c4d65744c69666520496e632e2c32340a0573d26101800005000000140000000000000000000000a200000000000000a2000000c8e3c5c650'
    )
    _SELECT_CRC_EXPECTED = (
        b'Lora Francis,School,Staples Inc,27\n'
        b'Eleanor Little,School,"Conectiv, Inc",43\n'
        b'Rosie Hughes,School,Western Gas Resources Inc,44\n'
        b'Lawrence Ross,School,MetLife Inc.,24\n'
    )
    # Offset of the first DATA frame's crc32 checksum (12-byte header + 133-byte payload).
    _SELECT_CRC_CHECKSUM_OFFSET = 145

    def _select_crc_response(self, body: bytes):
        def response() -> MockHttpResponse:
            return MockHttpResponse(
                status_code=206,
                reason='Partial Content',
                headers={
                    'Server': 'AliyunOSS',
                    'Content-Type': 'application/octet-stream',
                    'x-oss-request-id': 'id-1234',
                    'x-oss-select-output-raw': 'false',
                },
                body=body,
            )
        return response

    def _select_crc_request(self, enable_payload_crc):
        return model.SelectObjectRequest(
            bucket='bucket',
            key='key',
            process='csv/select',
            select_request=model.SelectRequest(
                output_serialization=model.OutputSerialization(
                    enable_payload_crc=enable_payload_crc,
                ),
            ),
        )

    def test_select_object_crc_check_pass(self):
        self.set_responseFunc(self._select_crc_response(self._SELECT_CRC_FRAMES))
        result = select_object(self.client, self._select_crc_request(True))
        self.assertEqual(206, result.status_code)
        self.assertEqual('false', result.headers.get('x-oss-select-output-raw'))
        self.assertEqual(self._SELECT_CRC_EXPECTED, result.body.content)

    def test_select_object_crc_check_mismatch(self):
        corrupt = bytearray(self._SELECT_CRC_FRAMES)
        corrupt[self._SELECT_CRC_CHECKSUM_OFFSET] ^= 0xFF
        self.set_responseFunc(self._select_crc_response(bytes(corrupt)))
        try:
            select_object(self.client, self._select_crc_request(True)).body.content
            self.fail('should not here')
        except Exception as e:
            self.assertTrue(str(e).__contains__('Incorrect checksum'))

    def test_select_object_crc_check_disabled(self):
        corrupt = bytearray(self._SELECT_CRC_FRAMES)
        corrupt[self._SELECT_CRC_CHECKSUM_OFFSET] ^= 0xFF
        self.set_responseFunc(self._select_crc_response(bytes(corrupt)))
        result = select_object(self.client, self._select_crc_request(False))
        self.assertEqual(self._SELECT_CRC_EXPECTED, result.body.content)

    def test_create_select_object_meta_response_with_error(self):
        def response_invalid() -> MockHttpResponse:
            data = b'\0x01\0x80\0x00\0x06\0x00\0x00\0x00\0x25,0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0xc5\0x00\0x00\0x00\0x00,0x00\0x00\0x00\0xc5\0x00\0x00\0x00\0xc8\0x00\0x00\0x00\0x01\0x00\0x00\0x00\0x00,0x00\0x00\0x00\0x05\0x00\0x00\0x00\0x04\0x2e\0x78\0x95\0x1f\0x00'
            return MockHttpResponse(
                status_code=200,
                reason='OK',
                headers={
                    'Server': 'AliyunOSS',
                    'Date': 'Tue, 23 Jul 2024 13:01:06 GMT',
                    'Content-Type': 'application/xml',
                    'x-oss-ec': '0002-00000902',
                    'x-oss-request-id': 'id-1234',
                },
                body=data
            )

        self.set_responseFunc(response_invalid)

        try:
            request = model.CreateSelectObjectMetaRequest(
                bucket='bucket',
                key='key',
                process='csv/meta',
                select_meta_request = model.CreateSelectObjectMetaRequest(),
            )
            result = create_select_object_meta(self.client, request)
            self.fail('should not here')
        except exceptions.DeserializationError as e:
            self.assertTrue(str(e).__contains__("parse CreateSelectObjectMetaResult fail"))
            