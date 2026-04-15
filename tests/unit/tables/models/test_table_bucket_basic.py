# -*- coding: utf-8 -*-
"""Unit tests for tables table_bucket_basic models."""

import unittest
from alibabacloud_oss_v2.tables.models.table_bucket_basic import (
    CreateTableBucketRequest,
    CreateTableBucketResult,
    DeleteTableBucketRequest,
    DeleteTableBucketResult,
    GetTableBucketRequest,
    GetTableBucketResult,
    ListTableBucketsRequest,
    ListTableBucketsResult,
)
from alibabacloud_oss_v2.tables.models.common import EncryptionConfiguration


class TestCreateTableBucketRequest(unittest.TestCase):
    """Test cases for CreateTableBucketRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = CreateTableBucketRequest()
        self.assertIsNone(request.name)
        self.assertIsNone(request.encryption_configuration)
        self.assertIsNone(request.tags)

    def test_init_with_name(self):
        """Test initialization with name."""
        request = CreateTableBucketRequest(name="test-bucket")
        self.assertEqual(request.name, "test-bucket")
        self.assertIsNone(request.encryption_configuration)
        self.assertIsNone(request.tags)

    def test_init_with_encryption_configuration(self):
        """Test initialization with encryption configuration."""
        encryption_config = EncryptionConfiguration(sse_algorithm="AES256")
        request = CreateTableBucketRequest(
            name="test-bucket",
            encryption_configuration=encryption_config
        )
        self.assertIsNotNone(request.encryption_configuration)
        self.assertEqual(request.encryption_configuration.sse_algorithm, "AES256")

    def test_init_with_tags(self):
        """Test initialization with tags."""
        tags = {"env": "production", "team": "data"}
        request = CreateTableBucketRequest(
            name="test-bucket",
            tags=tags
        )
        self.assertEqual(request.tags, tags)
        self.assertEqual(request.tags["env"], "production")
        self.assertEqual(request.tags["team"], "data")

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        encryption_config = EncryptionConfiguration(sse_algorithm="KMS")
        tags = {"env": "production"}
        request = CreateTableBucketRequest(
            name="test-bucket",
            encryption_configuration=encryption_config,
            tags=tags
        )
        self.assertEqual(request.name, "test-bucket")
        self.assertEqual(request.encryption_configuration.sse_algorithm, "KMS")
        self.assertEqual(request.tags["env"], "production")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("name", CreateTableBucketRequest._attribute_map)
        self.assertIn("encryption_configuration", CreateTableBucketRequest._attribute_map)
        self.assertIn("tags", CreateTableBucketRequest._attribute_map)
        self.assertEqual(CreateTableBucketRequest._attribute_map["name"]["position"], "body")


class TestCreateTableBucketResult(unittest.TestCase):
    """Test cases for CreateTableBucketResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = CreateTableBucketResult()
        self.assertIsNone(result.arn)

    def test_init_with_arn(self):
        """Test initialization with arn."""
        result = CreateTableBucketResult(
            arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(result.arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")


class TestDeleteTableBucketRequest(unittest.TestCase):
    """Test cases for DeleteTableBucketRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = DeleteTableBucketRequest()
        self.assertIsNone(request.table_bucket_arn)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = DeleteTableBucketRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", DeleteTableBucketRequest._attribute_map)
        self.assertEqual(DeleteTableBucketRequest._attribute_map["table_bucket_arn"]["position"], "host")
        self.assertTrue(DeleteTableBucketRequest._attribute_map["table_bucket_arn"]["required"])


class TestDeleteTableBucketResult(unittest.TestCase):
    """Test cases for DeleteTableBucketResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = DeleteTableBucketResult()


class TestGetTableBucketRequest(unittest.TestCase):
    """Test cases for GetTableBucketRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTableBucketRequest()
        self.assertIsNone(request.table_bucket_arn)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = GetTableBucketRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", GetTableBucketRequest._attribute_map)
        self.assertEqual(GetTableBucketRequest._attribute_map["table_bucket_arn"]["position"], "host")
        self.assertTrue(GetTableBucketRequest._attribute_map["table_bucket_arn"]["required"])


class TestGetTableBucketResult(unittest.TestCase):
    """Test cases for GetTableBucketResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTableBucketResult()
        self.assertIsNone(result.arn)
        self.assertIsNone(result.name)
        self.assertIsNone(result.owner_account_id)
        self.assertIsNone(result.created_at)
        self.assertIsNone(result.table_bucket_id)
        self.assertIsNone(result.type)

    def test_init_with_basic_fields(self):
        """Test initialization with basic fields."""
        result = GetTableBucketResult(
            arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            name="test-bucket",
            owner_account_id="123456789012",
            table_bucket_id="tb-1234567890abcdef",
            type="TABLE"
        )
        self.assertEqual(result.arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(result.name, "test-bucket")
        self.assertEqual(result.owner_account_id, "123456789012")
        self.assertEqual(result.table_bucket_id, "tb-1234567890abcdef")
        self.assertEqual(result.type, "TABLE")

    def test_init_with_created_at(self):
        """Test initialization with created_at."""
        from datetime import datetime
        created_at = datetime(2023, 12, 17, 0, 20, 57)
        result = GetTableBucketResult(
            arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            name="test-bucket",
            created_at=created_at
        )
        self.assertEqual(result.created_at, created_at)

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        from datetime import datetime
        created_at = datetime(2023, 12, 17, 0, 20, 57)
        result = GetTableBucketResult(
            arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            name="test-bucket",
            owner_account_id="123456789012",
            created_at=created_at,
            table_bucket_id="tb-1234567890abcdef",
            type="TABLE"
        )
        self.assertEqual(result.arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(result.name, "test-bucket")
        self.assertEqual(result.owner_account_id, "123456789012")
        self.assertEqual(result.created_at, created_at)
        self.assertEqual(result.table_bucket_id, "tb-1234567890abcdef")
        self.assertEqual(result.type, "TABLE")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("arn", GetTableBucketResult._attribute_map)
        self.assertIn("name", GetTableBucketResult._attribute_map)
        self.assertIn("owner_account_id", GetTableBucketResult._attribute_map)
        self.assertIn("created_at", GetTableBucketResult._attribute_map)
        self.assertIn("table_bucket_id", GetTableBucketResult._attribute_map)
        self.assertIn("type", GetTableBucketResult._attribute_map)
        self.assertEqual(GetTableBucketResult._attribute_map["arn"]["rename"], "arn")
        self.assertEqual(GetTableBucketResult._attribute_map["table_bucket_id"]["rename"], "tableBucketId")


class TestListTableBucketsRequest(unittest.TestCase):
    """Test cases for ListTableBucketsRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = ListTableBucketsRequest()
        self.assertIsNone(request.continuation_token)
        self.assertIsNone(request.max_table_buckets)

    def test_init_with_continuation_token(self):
        """Test initialization with continuation_token."""
        request = ListTableBucketsRequest(continuation_token="abc123")
        self.assertEqual(request.continuation_token, "abc123")
        self.assertIsNone(request.max_table_buckets)

    def test_init_with_max_table_buckets(self):
        """Test initialization with max_table_buckets."""
        request = ListTableBucketsRequest(max_table_buckets="100")
        self.assertIsNone(request.continuation_token)
        self.assertEqual(request.max_table_buckets, "100")

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        request = ListTableBucketsRequest(
            continuation_token="abc123",
            max_table_buckets="50"
        )
        self.assertEqual(request.continuation_token, "abc123")
        self.assertEqual(request.max_table_buckets, "50")


class TestListTableBucketsResult(unittest.TestCase):
    """Test cases for ListTableBucketsResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = ListTableBucketsResult()
        self.assertIsNone(result.table_buckets)
        self.assertIsNone(result.continuation_token)

    def test_init_with_continuation_token(self):
        """Test initialization with continuation_token."""
        result = ListTableBucketsResult(continuation_token="abc123")
        self.assertIsNone(result.table_buckets)
        self.assertEqual(result.continuation_token, "abc123")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_buckets", ListTableBucketsResult._attribute_map)
        self.assertIn("continuation_token", ListTableBucketsResult._attribute_map)
        self.assertEqual(ListTableBucketsResult._attribute_map["table_buckets"]["rename"], "tableBuckets")


if __name__ == '__main__':
    unittest.main()
