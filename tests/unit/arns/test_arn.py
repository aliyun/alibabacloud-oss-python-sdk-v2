# pylint: skip-file

import unittest
from alibabacloud_oss_v2.arns import Arn, ArnResource


class TestArnResource(unittest.TestCase):

    def test_from_string_simple(self):
        resource = ArnResource.from_string('bucket/my-bucket')
        self.assertEqual('bucket', resource.resource_type)
        self.assertEqual('my-bucket', resource.resource)
        self.assertIsNone(resource.qualifier)

    def test_from_string_with_qualifier(self):
        resource = ArnResource.from_string('bucket/my-bucket/index/my-index')
        self.assertEqual('bucket', resource.resource_type)
        self.assertEqual('my-bucket', resource.resource)
        self.assertEqual('index/my-index', resource.qualifier)

    def test_from_string_no_type(self):
        resource = ArnResource.from_string('my-resource')
        self.assertIsNone(resource.resource_type)
        self.assertEqual('my-resource', resource.resource)
        self.assertIsNone(resource.qualifier)

    def test_from_string_empty(self):
        resource = ArnResource.from_string('')
        self.assertIsNone(resource.resource_type)
        self.assertEqual('', resource.resource)
        self.assertIsNone(resource.qualifier)

    def test_from_string_with_slash_suffix(self):
        resource = ArnResource.from_string('bucket/my-bucket/')
        self.assertEqual('bucket', resource.resource_type)
        self.assertEqual('my-bucket', resource.resource)
        self.assertEqual('', resource.qualifier)

    def test_from_string_multiple_colons(self):
        # ':' is not a splitter after the first one, only '/' works as splitter for qualifier
        resource = ArnResource.from_string('table:namespace:table1')
        self.assertEqual('table', resource.resource_type)
        self.assertEqual('namespace', resource.resource)
        self.assertEqual('table1', resource.qualifier)


class TestArn(unittest.TestCase):

    def test_from_string_valid(self):
        arn_str = 'acs:oss:cn-hangzhou:123456789:bucket/my-bucket'
        arn = Arn.from_string(arn_str)
        self.assertEqual('oss', arn.service)
        self.assertEqual('cn-hangzhou', arn.region)
        self.assertEqual('123456789', arn.account_id)
        self.assertEqual('bucket/my-bucket', arn.resource)

    def test_from_string_with_empty_region(self):
        arn_str = 'acs:oss::123456789:bucket/my-bucket'
        arn = Arn.from_string(arn_str)
        self.assertEqual('oss', arn.service)
        self.assertIsNone(arn.region)
        self.assertEqual('123456789', arn.account_id)
        self.assertEqual('bucket/my-bucket', arn.resource)

    def test_from_string_with_empty_account(self):
        arn_str = 'acs:oss:cn-hangzhou::bucket/my-bucket'
        arn = Arn.from_string(arn_str)
        self.assertEqual('oss', arn.service)
        self.assertEqual('cn-hangzhou', arn.region)
        self.assertIsNone(arn.account_id)
        self.assertEqual('bucket/my-bucket', arn.resource)

    def test_from_string_tables_arn(self):
        arn_str = 'acs:osstables:cn-hangzhou:123456789:bucket/my-bucket/'
        arn = Arn.from_string(arn_str)
        self.assertEqual('osstables', arn.service)
        self.assertEqual('cn-hangzhou', arn.region)
        self.assertEqual('123456789', arn.account_id)
        self.assertEqual('bucket/my-bucket/', arn.resource)
        self.assertEqual('bucket', arn.arn_resource.resource_type)
        self.assertEqual('my-bucket', arn.arn_resource.resource)

    def test_from_string_vectors_arn(self):
        arn_str = 'acs:ossvector:cn-hangzhou:123456:bucket/my-bucket/index/my-index'
        arn = Arn.from_string(arn_str)
        self.assertEqual('ossvector', arn.service)
        self.assertEqual('cn-hangzhou', arn.region)
        self.assertEqual('123456', arn.account_id)
        self.assertEqual('bucket/my-bucket/index/my-index', arn.resource)
        self.assertEqual('bucket', arn.arn_resource.resource_type)
        self.assertEqual('my-bucket', arn.arn_resource.resource)
        self.assertEqual('index/my-index', arn.arn_resource.qualifier)

    def test_from_string_invalid_not_acs_prefix(self):
        arn_str = 'aws:oss:cn-hangzhou:123456:bucket/test'
        with self.assertRaises(ValueError):
            Arn.from_string(arn_str)

    def test_from_string_invalid_no_service(self):
        arn_str = 'acs::cn-hangzhou:123456:bucket/test'
        with self.assertRaises(ValueError):
            Arn.from_string(arn_str)

    def test_from_string_invalid_no_region_colon(self):
        arn_str = 'acs:oss:123456:bucket/test'
        with self.assertRaises(ValueError):
            Arn.from_string(arn_str)

    def test_from_string_invalid_no_account_colon(self):
        arn_str = 'acs:oss:cn-hangzhou:bucket/test'
        with self.assertRaises(ValueError):
            Arn.from_string(arn_str)

    def test_from_string_invalid_no_resource(self):
        arn_str = 'acs:oss:cn-hangzhou:123456:'
        with self.assertRaises(ValueError):
            Arn.from_string(arn_str)

    def test_from_string_invalid_none(self):
        with self.assertRaises(ValueError):
            Arn.from_string(None)

    def test_try_from_string_valid(self):
        arn_str = 'acs:oss:cn-hangzhou:123456:bucket/test'
        arn = Arn.try_from_string(arn_str)
        self.assertIsNotNone(arn)
        self.assertEqual('oss', arn.service)
        self.assertEqual('cn-hangzhou', arn.region)
        self.assertEqual('123456', arn.account_id)
        self.assertEqual('bucket/test', arn.resource)

    def test_try_from_string_invalid(self):
        arn_str = 'invalid-arn'
        arn = Arn.try_from_string(arn_str)
        self.assertIsNone(arn)

    def test_try_from_string_none(self):
        arn = Arn.try_from_string(None)
        self.assertIsNone(arn)

    def test_resource_as_string(self):
        arn_str = 'acs:oss:cn-hangzhou:123456:bucket/test'
        arn = Arn.from_string(arn_str)
        self.assertEqual('bucket/test', arn.resource_as_string())


    def test_arn_resource_table_arn(self):
        arn_str = 'acs:oss:cn-hangzhou:123456:bucket/test'
        arn = Arn.from_string(arn_str)
        self.assertIsInstance(arn.arn_resource, ArnResource)
        self.assertEqual('bucket', arn.arn_resource.resource_type)
        self.assertEqual('test', arn.arn_resource.resource)

    def test_arn_resource_table_arn(self):
        arn_str = 'acs:osstables:cn-beijing:123456:bucket/test-bucket-9326/table/ad3fca49-9de8-4e5f-8d7c-e15c2588c2ad'
        arn = Arn.from_string(arn_str)
        self.assertIsInstance(arn.arn_resource, ArnResource)
        self.assertEqual('bucket', arn.arn_resource.resource_type)
        self.assertEqual('test-bucket-9326', arn.arn_resource.resource)
        self.assertEqual('table/ad3fca49-9de8-4e5f-8d7c-e15c2588c2ad', arn.arn_resource.qualifier)
