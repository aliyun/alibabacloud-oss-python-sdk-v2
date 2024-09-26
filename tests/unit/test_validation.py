# pylint: skip-file
import unittest
from alibabacloud_oss_v2 import validation

class TestValidation(unittest.TestCase):
    def test_is_valid_region(self):
        for region in ['cn-hangzhou', 'us-east-1']:
            self.assertTrue(validation.is_valid_region(region))

        for region in ['CN-hangzhou', '#ad,ad', '', None]:
            self.assertFalse(validation.is_valid_region(region))


    def test_is_valid_endpoint(self):
        for endpoint in [
                '192.168.1.1',
                '192.168.1.1:80',
                'www.test-inc.com',
                'http://www.test-inc.com',
                'WWW.test-inc_CN.com',
                'http://www.test-inc_test.com:80',
            ]:
            self.assertTrue(validation.is_valid_endpoint(endpoint))

        for endpoint in [
                'https://www.test-inc_test.com:80/test?123=x',
                'www.test-inc*test.com', 
                'www.test-inc.com\\oss-cn-hangzhou.aliyuncs.com',
                '',
                None
            ]:
            self.assertFalse(validation.is_valid_endpoint(endpoint))

    def test_is_valid_bucket_name(self):
        for bucket in [
                '123',
                'test',
                'test-123',
                '123-test',
                '123test',
            ]:
            self.assertTrue(validation.is_valid_bucket_name(bucket))

        for bucket in [
                '12',
                'abcdefghij-abcdefghij-abcdefghij-abcdefghij-abcdefghij-abcdefghij',
                '-test',
                'test-',
                'test_123',
                'TEst',
                '#?123',
                ''
            ]:
            self.assertFalse(validation.is_valid_bucket_name(bucket))


    def test_is_valid_object_name(self):
        for key in [
                '123',
                '#ADfa',
                '#ADfa?fasdk#ja',
            ]:
            self.assertTrue(validation.is_valid_object_name(key))

        for key in [
                '',
            ]:
            self.assertFalse(validation.is_valid_object_name(key))

    def test_is_valid_range(self):
        for value in [
                'bytes=123-abc',
                'bytes=123-',
                'bytes=-123',
            ]:
            self.assertTrue(validation.is_valid_range(value))

        for value in [
                '',
                'adfds',
            ]:
            self.assertFalse(validation.is_valid_range(value))

