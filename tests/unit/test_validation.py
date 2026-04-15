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

    def test_assert_validate_arn_bucket_valid(self):
        """Test valid bucket ARN formats."""
        # Standard bucket ARN
        validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/my-bucket")
        validation.assert_validate_arn_bucket("acs:oss:cn-beijing:123456789012:bucket/test-bucket")
        validation.assert_validate_arn_bucket("acs:oss:cn-shanghai:987654321098:bucket/bucket123")
        validation.assert_validate_arn_bucket("acs:oss:us-west-1:123456789012:bucket/my-bucket")
        validation.assert_validate_arn_bucket("acs:oss:ap-southeast-1:123456789012:bucket/my-bucket")
        # Minimal valid bucket name (3 characters)
        validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/abc")
        # Maximal valid bucket name (63 characters)
        validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/" + "a" * 63)

    def test_assert_validate_arn_bucket_invalid_format(self):
        """Test invalid ARN formats."""
        # Doesn't start with 'acs:'
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("arn:oss:cn-hangzhou:123456789012:bucket/my-bucket")
        self.assertIn("Malformed ARN - doesn't start with 'acs:'", str(context.exception))

        # No service specified
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs::cn-hangzhou:123456789012:bucket/my-bucket")
        self.assertIn("service cannot be empty", str(context.exception))

        # No resource specified
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:")
        self.assertIn("Malformed ARN - no resource specified", str(context.exception))

        # None input
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket(None)
        self.assertIn("ARN parsing failed", str(context.exception))

        # Empty string input
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("")
        self.assertIn("Malformed ARN", str(context.exception))

    def test_assert_validate_arn_bucket_invalid_resource(self):
        """Test invalid bucket resource formats."""
        # Resource doesn't start with 'bucket/'
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:object/my-object")
        self.assertIn("Malformed ARN - doesn't contain bucket resource", str(context.exception))

        # Resource is 'bucket' but missing '/' separator
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucketmy-bucket")
        self.assertIn("Malformed ARN - doesn't contain bucket resource", str(context.exception))

    def test_assert_validate_arn_bucket_invalid_bucket_name(self):
        """Test invalid bucket names in ARN."""
        # Bucket name starts with hyphen
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/-invalid")
        self.assertIn("bucket resource is invalid", str(context.exception))

        # Bucket name ends with hyphen
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/invalid-")
        self.assertIn("bucket resource is invalid", str(context.exception))

        # Bucket name too short (less than 3 characters)
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/ab")
        self.assertIn("bucket resource is invalid", str(context.exception))

        # Bucket name too long (more than 63 characters)
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/" + "a" * 64)
        self.assertIn("bucket resource is invalid", str(context.exception))

        # Bucket name contains uppercase letters
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/My-Bucket")
        self.assertIn("bucket resource is invalid", str(context.exception))

        # Bucket name contains underscore
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/my_bucket")
        self.assertIn("bucket resource is invalid", str(context.exception))

        # Bucket name contains special characters (dot)
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/my.bucket")
        self.assertIn("bucket resource is invalid", str(context.exception))

        # Bucket name is empty
        with self.assertRaises(ValueError) as context:
            validation.assert_validate_arn_bucket("acs:oss:cn-hangzhou:123456789012:bucket/")
        self.assertIn("bucket resource is invalid", str(context.exception))
