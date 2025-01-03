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
            