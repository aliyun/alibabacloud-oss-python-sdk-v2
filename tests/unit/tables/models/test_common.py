# -*- coding: utf-8 -*-
"""Unit tests for tables common models."""

import unittest
from alibabacloud_oss_v2.tables.models.common import (
    SchemaField,
    IcebergPartitionField,
    IcebergSortField,
    IcebergSchema,
    IcebergPartitionSpec,
    IcebergSortOrder,
    IcebergMetadata,
    TableMetadata,
    EncryptionConfiguration,
    NamespaceSummary,
    TableBucketSummary,
    TableSummary,
)


class TestIcebergPartitionSpec(unittest.TestCase):
    """Test cases for IcebergPartitionSpec model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        spec = IcebergPartitionSpec()
        self.assertIsNone(spec.spec_id)
        self.assertIsNone(spec.fields)

    def test_init_with_spec_id(self):
        """Test initialization with spec_id field."""
        spec = IcebergPartitionSpec(spec_id=1)
        self.assertEqual(spec.spec_id, 1)
        self.assertIsNone(spec.fields)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        field1 = IcebergPartitionField(source_id=1, field_id=100, name="date", transform="day")
        field2 = IcebergPartitionField(source_id=2, field_id=101, name="region", transform="bucket")
        spec = IcebergPartitionSpec(fields=[field1, field2])
        self.assertIsNone(spec.spec_id)
        self.assertEqual(len(spec.fields), 2)
        self.assertEqual(spec.fields[0].name, "date")
        self.assertEqual(spec.fields[1].name, "region")

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        field = IcebergPartitionField(source_id=1, field_id=100, name="date", transform="day")
        spec = IcebergPartitionSpec(spec_id=1, fields=[field])
        self.assertEqual(spec.spec_id, 1)
        self.assertEqual(len(spec.fields), 1)
        self.assertEqual(spec.fields[0].source_id, 1)
        self.assertEqual(spec.fields[0].field_id, 100)

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("spec_id", IcebergPartitionSpec._attribute_map)
        self.assertIn("fields", IcebergPartitionSpec._attribute_map)
        self.assertEqual(IcebergPartitionSpec._attribute_map["spec_id"]["rename"], "specId")
        self.assertEqual(IcebergPartitionSpec._attribute_map["spec_id"]["type"], "int")


class TestIcebergMetadata(unittest.TestCase):
    """Test cases for IcebergMetadata model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        metadata = IcebergMetadata()
        self.assertIsNone(metadata.schema)
        self.assertIsNone(metadata.partition_spec)
        self.assertIsNone(metadata.sort_order)
        self.assertIsNone(metadata.properties)

    def test_init_with_schema(self):
        """Test initialization with schema."""
        schema = IcebergSchema(fields=[SchemaField(name="id", type="int", required=True)])
        metadata = IcebergMetadata(schema=schema)
        self.assertIsNotNone(metadata.schema)
        self.assertEqual(len(metadata.schema.fields), 1)
        self.assertIsNone(metadata.partition_spec)
        self.assertIsNone(metadata.sort_order)
        self.assertIsNone(metadata.properties)

    def test_init_with_partition_spec(self):
        """Test initialization with partition_spec."""
        partition_spec = IcebergPartitionSpec(spec_id=1)
        metadata = IcebergMetadata(partition_spec=partition_spec)
        self.assertIsNone(metadata.schema)
        self.assertIsNotNone(metadata.partition_spec)
        self.assertEqual(metadata.partition_spec.spec_id, 1)
        self.assertIsNone(metadata.sort_order)
        self.assertIsNone(metadata.properties)

    def test_init_with_sort_order(self):
        """Test initialization with sort_order."""
        sort_field = IcebergSortField(source_id=1, direction="asc", null_order="first", transform="identity")
        sort_order = IcebergSortOrder(fields=[sort_field])
        metadata = IcebergMetadata(sort_order=sort_order)
        self.assertIsNone(metadata.schema)
        self.assertIsNone(metadata.partition_spec)
        self.assertIsNotNone(metadata.sort_order)
        self.assertEqual(len(metadata.sort_order.fields), 1)
        self.assertIsNone(metadata.properties)

    def test_init_with_properties(self):
        """Test initialization with properties dict."""
        properties = {
            "key1": "value1",
            "key2": "value2",
            "owner": "test-user"
        }
        metadata = IcebergMetadata(properties=properties)
        self.assertIsNone(metadata.schema)
        self.assertIsNone(metadata.partition_spec)
        self.assertIsNone(metadata.sort_order)
        self.assertEqual(metadata.properties, properties)
        self.assertEqual(metadata.properties["key1"], "value1")
        self.assertEqual(metadata.properties["key2"], "value2")

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        schema = IcebergSchema(fields=[SchemaField(name="id", type="int", required=True)])
        partition_spec = IcebergPartitionSpec(spec_id=1, fields=[
            IcebergPartitionField(source_id=1, field_id=100, name="date", transform="day")
        ])
        sort_field = IcebergSortField(source_id=1, direction="asc")
        sort_order = IcebergSortOrder(fields=[sort_field])
        properties = {"owner": "test-user", "env": "prod"}

        metadata = IcebergMetadata(
            schema=schema,
            partition_spec=partition_spec,
            sort_order=sort_order,
            properties=properties
        )

        self.assertIsNotNone(metadata.schema)
        self.assertEqual(len(metadata.schema.fields), 1)
        self.assertIsNotNone(metadata.partition_spec)
        self.assertEqual(metadata.partition_spec.spec_id, 1)
        self.assertIsNotNone(metadata.sort_order)
        self.assertEqual(len(metadata.sort_order.fields), 1)
        self.assertIsNotNone(metadata.properties)
        self.assertEqual(metadata.properties["owner"], "test-user")
        self.assertEqual(metadata.properties["env"], "prod")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("schema", IcebergMetadata._attribute_map)
        self.assertIn("partition_spec", IcebergMetadata._attribute_map)
        self.assertIn("sort_order", IcebergMetadata._attribute_map)
        self.assertIn("properties", IcebergMetadata._attribute_map)
        self.assertEqual(IcebergMetadata._attribute_map["properties"]["rename"], "properties")


class TestTableMetadata(unittest.TestCase):
    """Test cases for TableMetadata model."""

    def test_with_iceberg_metadata(self):
        """Test TableMetadata with IcebergMetadata."""
        properties = {"key": "value"}
        iceberg = IcebergMetadata(properties=properties)
        table_metadata = TableMetadata(iceberg=iceberg)

        self.assertIsNotNone(table_metadata.iceberg)
        self.assertEqual(table_metadata.iceberg.properties["key"], "value")


class TestTableBucketSummary(unittest.TestCase):
    """Test cases for TableBucketSummary model."""

    def test_with_type_field(self):
        """Test TableBucketSummary with type field."""
        summary = TableBucketSummary(
            arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            name="test-bucket",
            owner_account_id="123456789012",
            table_bucket_id="tb-1234567890abcdef",
            created_at=None,
            type="TABLE"
        )
        self.assertEqual(summary.type, "TABLE")

    def test_attribute_map_has_type(self):
        """Test _attribute_map contains type field."""
        self.assertIn("type", TableBucketSummary._attribute_map)
        self.assertEqual(TableBucketSummary._attribute_map["type"]["rename"], "type")


class TestIcebergPartitionField(unittest.TestCase):
    """Test cases for IcebergPartitionField model."""

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("source_id", IcebergPartitionField._attribute_map)
        self.assertIn("field_id", IcebergPartitionField._attribute_map)
        self.assertIn("name", IcebergPartitionField._attribute_map)
        self.assertIn("transform", IcebergPartitionField._attribute_map)
        self.assertEqual(IcebergPartitionField._attribute_map["source_id"]["rename"], "sourceId")
        self.assertEqual(IcebergPartitionField._attribute_map["field_id"]["rename"], "fieldId")


class TestIcebergSortField(unittest.TestCase):
    """Test cases for IcebergSortField model."""

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("source_id", IcebergSortField._attribute_map)
        self.assertIn("direction", IcebergSortField._attribute_map)
        self.assertIn("null_order", IcebergSortField._attribute_map)
        self.assertIn("transform", IcebergSortField._attribute_map)
        self.assertEqual(IcebergSortField._attribute_map["source_id"]["rename"], "sourceId")


class TestTableSummary(unittest.TestCase):
    """Test cases for TableSummary model."""

    def test_with_type_field(self):
        """Test TableSummary with type field."""
        summary = TableSummary(
            namespace=["my-namespace"],
            name="test-table",
            type="managed",
            table_arn="arn:acs:oss-tables:table-123",
        )
        self.assertEqual(summary.type, "managed")

    def test_attribute_map_has_type(self):
        """Test _attribute_map contains type field."""
        self.assertIn("type", TableSummary._attribute_map)
        self.assertEqual(TableSummary._attribute_map["type"]["rename"], "type")


if __name__ == '__main__':
    unittest.main()
