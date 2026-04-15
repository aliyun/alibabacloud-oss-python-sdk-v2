# -*- coding: utf-8 -*-
"""Unit tests for tables table_basic models."""

import unittest
from alibabacloud_oss_v2.tables.models.table_basic import (
    CreateTableRequest,
    CreateTableResult,
    DeleteTableRequest,
    DeleteTableResult,
    GetTableRequest,
    GetTableResult,
    ListTablesRequest,
    ListTablesResult,
    RenameTableRequest,
    RenameTableResult,
)
from alibabacloud_oss_v2.tables.models.common import (
    SchemaField,
    IcebergPartitionField,
    IcebergPartitionSpec,
    IcebergSchema,
    IcebergMetadata,
    TableMetadata,
    EncryptionConfiguration,
)


class TestCreateTableRequest(unittest.TestCase):
    """Test cases for CreateTableRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = CreateTableRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.name)
        self.assertIsNone(request.format)
        self.assertIsNone(request.metadata)
        self.assertIsNone(request.encryption_configuration)

    def test_init_with_basic_fields(self):
        """Test initialization with basic fields."""
        request = CreateTableRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="test_namespace",
            name="test_table",
            format="iceberg"
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.name, "test_table")
        self.assertEqual(request.format, "iceberg")

    def test_init_with_encryption_configuration(self):
        """Test initialization with encryption configuration."""
        encryption_config = EncryptionConfiguration(sse_algorithm="AES256")
        request = CreateTableRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="test_namespace",
            name="test_table",
            format="iceberg",
            encryption_configuration=encryption_config
        )
        self.assertIsNotNone(request.encryption_configuration)
        self.assertEqual(request.encryption_configuration.sse_algorithm, "AES256")

    def test_init_with_full_metadata(self):
        """Test initialization with full metadata."""
        schema = IcebergSchema(fields=[
            SchemaField(name="id", type="long", required=True),
            SchemaField(name="name", type="string", required=False),
            SchemaField(name="ts", type="timestamptz", required=False),
        ])

        partition_field = IcebergPartitionField(
            source_id=2,
            field_id=1001,
            name="region",
            transform="identity"
        )
        partition_spec = IcebergPartitionSpec(spec_id=0, fields=[partition_field])

        iceberg_metadata = IcebergMetadata(
            schema=schema,
            partition_spec=partition_spec,
            properties={"owner": "table-owner", "environment": "production"}
        )

        metadata = TableMetadata(iceberg=iceberg_metadata)

        request = CreateTableRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="test_namespace",
            name="test_table",
            format="iceberg",
            metadata=metadata
        )

        self.assertIsNotNone(request.metadata)
        self.assertIsNotNone(request.metadata.iceberg)
        self.assertIsNotNone(request.metadata.iceberg.schema)
        self.assertEqual(len(request.metadata.iceberg.schema.fields), 3)
        self.assertIsNotNone(request.metadata.iceberg.partition_spec)

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", CreateTableRequest._attribute_map)
        self.assertIn("namespace", CreateTableRequest._attribute_map)
        self.assertIn("name", CreateTableRequest._attribute_map)
        self.assertIn("format", CreateTableRequest._attribute_map)
        self.assertIn("metadata", CreateTableRequest._attribute_map)
        self.assertEqual(CreateTableRequest._attribute_map["table_bucket_arn"]["rename"], "x-oss-table-bucket-arn")
        self.assertEqual(CreateTableRequest._attribute_map["namespace"]["position"], "query")


class TestCreateTableResult(unittest.TestCase):
    """Test cases for CreateTableResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = CreateTableResult()
        self.assertIsNone(result.table_arn)
        self.assertIsNone(result.version_token)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        result = CreateTableResult(
            table_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id",
            version_token="aaabbb"
        )
        self.assertEqual(result.table_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id")
        self.assertEqual(result.version_token, "aaabbb")


class TestGetTableResult(unittest.TestCase):
    """Test cases for GetTableResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTableResult()
        self.assertIsNone(result.namespace)
        self.assertIsNone(result.name)
        self.assertIsNone(result.type)
        self.assertIsNone(result.table_arn)
        self.assertIsNone(result.created_at)
        self.assertIsNone(result.modified_at)
        self.assertIsNone(result.namespace_id)
        self.assertIsNone(result.format)
        self.assertIsNone(result.metadata)
        self.assertIsNone(result.encryption_configuration)
        self.assertIsNone(result.version_token)
        self.assertIsNone(result.metadata_location)
        self.assertIsNone(result.warehouse_location)
        self.assertIsNone(result.created_by)
        self.assertIsNone(result.modified_by)
        self.assertIsNone(result.owner_account_id)
        self.assertIsNone(result.table_bucket_id)

    def test_init_with_basic_fields(self):
        """Test initialization with basic fields."""
        result = GetTableResult(
            namespace=["my_namespace"],
            name="my_table",
            type="customer",
            table_arn="acs:osstable:cn-hangzhou:1234567890:bucket/my-table-bucket/table/table_id",
            namespace_id="ns-xxxxxxxx",
            version_token="aaabbb",
            metadata_location="oss://data-bucket/metadata/00000-xxx.metadata.json",
            warehouse_location="oss://data-bucket/warehouse/",
            format="iceberg",
            table_bucket_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            created_by="1234567890",
            modified_by="1234567890",
            owner_account_id="1234567890"
        )
        self.assertEqual(result.namespace, ["my_namespace"])
        self.assertEqual(result.name, "my_table")
        self.assertEqual(result.type, "customer")
        self.assertEqual(result.table_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/my-table-bucket/table/table_id")
        self.assertEqual(result.namespace_id, "ns-xxxxxxxx")
        self.assertEqual(result.version_token, "aaabbb")
        self.assertEqual(result.metadata_location, "oss://data-bucket/metadata/00000-xxx.metadata.json")
        self.assertEqual(result.warehouse_location, "oss://data-bucket/warehouse/")
        self.assertEqual(result.format, "iceberg")
        self.assertEqual(result.table_bucket_id, "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.assertEqual(result.created_by, "1234567890")
        self.assertEqual(result.modified_by, "1234567890")
        self.assertEqual(result.owner_account_id, "1234567890")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("name", GetTableResult._attribute_map)
        self.assertIn("type", GetTableResult._attribute_map)
        self.assertIn("table_arn", GetTableResult._attribute_map)
        self.assertIn("namespace", GetTableResult._attribute_map)
        self.assertIn("namespace_id", GetTableResult._attribute_map)
        self.assertIn("version_token", GetTableResult._attribute_map)
        self.assertEqual(GetTableResult._attribute_map["name"]["rename"], "name")
        self.assertEqual(GetTableResult._attribute_map["table_arn"]["rename"], "tableArn")


class TestDeleteTableRequest(unittest.TestCase):
    """Test cases for DeleteTableRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = DeleteTableRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.name)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = DeleteTableRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="test_namespace",
            name="test_table"
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.name, "test_table")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", DeleteTableRequest._attribute_map)
        self.assertIn("namespace", DeleteTableRequest._attribute_map)
        self.assertIn("name", DeleteTableRequest._attribute_map)
        self.assertEqual(DeleteTableRequest._attribute_map["namespace"]["position"], "path")
        self.assertEqual(DeleteTableRequest._attribute_map["name"]["position"], "path")


class TestGetTableRequest(unittest.TestCase):
    """Test cases for GetTableRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTableRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.name)
        self.assertIsNone(request.table_arn)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = GetTableRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="test_namespace",
            name="test_table"
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.name, "test_table")

    def test_init_with_table_arn(self):
        """Test initialization with table_arn."""
        request = GetTableRequest(
            table_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id"
        )
        self.assertEqual(request.table_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id")


class TestListTablesRequest(unittest.TestCase):
    """Test cases for ListTablesRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = ListTablesRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.prefix)
        self.assertIsNone(request.continuation_token)
        self.assertIsNone(request.max_tables)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = ListTablesRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="test_namespace",
            prefix="test_",
            continuation_token="abc123",
            max_tables=100
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.prefix, "test_")
        self.assertEqual(request.continuation_token, "abc123")
        self.assertEqual(request.max_tables, 100)


class TestListTablesResult(unittest.TestCase):
    """Test cases for ListTablesResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = ListTablesResult()
        self.assertIsNone(result.table_summaries)
        self.assertIsNone(result.continuation_token)

    def test_init_with_continuation_token(self):
        """Test initialization with continuation_token."""
        result = ListTablesResult(continuation_token="abc123")
        self.assertIsNone(result.table_summaries)
        self.assertEqual(result.continuation_token, "abc123")


class TestRenameTableRequest(unittest.TestCase):
    """Test cases for RenameTableRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = RenameTableRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)
        self.assertIsNone(request.new_table_name)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = RenameTableRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="test_namespace",
            table="old_table",
            new_table_name="new_table"
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "old_table")
        self.assertEqual(request.new_table_name, "new_table")


class TestDeleteTableResult(unittest.TestCase):
    """Test cases for DeleteTableResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = DeleteTableResult()


class TestRenameTableResult(unittest.TestCase):
    """Test cases for RenameTableResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = RenameTableResult()


if __name__ == '__main__':
    unittest.main()
