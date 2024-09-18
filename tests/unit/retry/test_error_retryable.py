# pylint: skip-file

import unittest
from alibabacloud_oss_v2.retry import error_retryable
from alibabacloud_oss_v2.exceptions import ServiceError, RequestError, ResponseError

attempted_celling = 64


def gen_status_code_error(status_code: int):
    return ServiceError(
        status_code=status_code,
        code='',
        request_id='',
        message='',
        ec='',
        timestamp='',
        request_target=''
    )


def gen_service_code_error(code: str):
    return ServiceError(
        status_code=0,
        code=code,
        request_id='',
        message='',
        ec='',
        timestamp='',
        request_target=''
    )


class TestErrorRetryable(unittest.TestCase):

    def test_http_status_code_retryable(self):
        r = error_retryable.HTTPStatusCodeRetryable()
        self.assertFalse(r.is_error_retryable(Exception()))
        self.assertFalse(r.is_error_retryable(None))
        self.assertFalse(r.is_error_retryable(gen_status_code_error(403)))
        self.assertFalse(r.is_error_retryable(gen_status_code_error(405)))
        self.assertTrue(r.is_error_retryable(gen_status_code_error(401)))
        self.assertTrue(r.is_error_retryable(gen_status_code_error(408)))
        self.assertTrue(r.is_error_retryable(gen_status_code_error(429)))
        self.assertTrue(r.is_error_retryable(gen_status_code_error(500)))
        self.assertTrue(r.is_error_retryable(gen_status_code_error(501)))
        self.assertTrue(r.is_error_retryable(gen_status_code_error(599)))

    def test_service_error_code_retryable(self):
        r = error_retryable.ServiceErrorCodeRetryable()
        self.assertFalse(r.is_error_retryable(Exception()))
        self.assertFalse(r.is_error_retryable(None))
        self.assertFalse(r.is_error_retryable(gen_service_code_error('123')))
        self.assertTrue(r.is_error_retryable(
            gen_service_code_error("RequestTimeTooSkewed")))
        self.assertTrue(r.is_error_retryable(
            gen_service_code_error("BadRequest")))

    def test_client_error_retryable(self):
        r = error_retryable.ClientErrorRetryable()
        self.assertFalse(r.is_error_retryable(Exception()))
        self.assertFalse(r.is_error_retryable(None))

        self.assertTrue(r.is_error_retryable(RequestError(error=Exception())))
        self.assertTrue(r.is_error_retryable(ResponseError(error=Exception())))
