# pylint: skip-file
from typing import List
import unittest
from alibabacloud_oss_v2.retry import retryer_impl, error_retryable
from alibabacloud_oss_v2.exceptions import ServiceError
from alibabacloud_oss_v2.defaults import DEFAULT_BASE_DELAY_S, DEFAULT_MAX_ATTEMPTS, DEFAULT_MAX_BACKOFF_S

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


class NopRetryable(error_retryable.ErrorRetryable):
    def is_error_retryable(self, error: Exception) -> bool:
        return False


class TestRetryerImpl(unittest.TestCase):

    def test_nop_retryer(self):
        r = retryer_impl.NopRetryer()
        self.assertEqual(1, r.max_attempts())
        self.assertFalse(r.is_error_retryable(Exception()))

    def test_standard_retryer_deafult(self):
        r = retryer_impl.StandardRetryer()
        self.assertIsNotNone(r)
        self.assertEqual(DEFAULT_MAX_ATTEMPTS, r.max_attempts())

        self.assertFalse(r.is_error_retryable(None))
        self.assertFalse(r.is_error_retryable(Exception()))
        self.assertFalse(r.is_error_retryable(gen_status_code_error(403)))
        self.assertFalse(r.is_error_retryable(gen_status_code_error(405)))
        self.assertTrue(r.is_error_retryable(gen_status_code_error(401)))
        self.assertFalse(r.is_error_retryable(gen_service_code_error('123')))
        self.assertTrue(r.is_error_retryable(
            gen_service_code_error("RequestTimeTooSkewed")))
        self.assertTrue(r.is_error_retryable(
            gen_service_code_error("BadRequest")))

        error = gen_status_code_error(501)
        self.assertTrue(r.is_error_retryable(error))
        for i in range(64 * 2):
            delay = r.retry_delay(i, error)
            self.assertGreater(delay, 0.0)
            self.assertLess(delay, DEFAULT_MAX_BACKOFF_S + 1)

    def test_standard_retryer(self):
        max_backoff = 30.5
        r = retryer_impl.StandardRetryer(
            max_attempts=4,
            max_backoff=max_backoff,
            base_delay=1.0,
            error_retryables=[NopRetryable()]
        )
        self.assertIsNotNone(r)
        self.assertEqual(4, r.max_attempts())

        self.assertFalse(r.is_error_retryable(None))
        self.assertFalse(r.is_error_retryable(Exception()))
        self.assertFalse(r.is_error_retryable(gen_status_code_error(403)))
        self.assertFalse(r.is_error_retryable(gen_status_code_error(405)))
        self.assertFalse(r.is_error_retryable(gen_status_code_error(401)))
        self.assertFalse(r.is_error_retryable(gen_service_code_error('123')))
        self.assertFalse(r.is_error_retryable(
            gen_service_code_error("RequestTimeTooSkewed")))
        self.assertFalse(r.is_error_retryable(
            gen_service_code_error("BadRequest")))

        error = gen_status_code_error(501)
        self.assertFalse(r.is_error_retryable(error))
        values:List[float] = []
        for i in range(64 * 2):
            delay = r.retry_delay(i, error)
            self.assertGreater(delay, 0.0)
            self.assertLess(delay, max_backoff + 1)
            if delay > DEFAULT_MAX_BACKOFF_S:
                values.append(delay)

        self.assertGreater(len(values), 0)

