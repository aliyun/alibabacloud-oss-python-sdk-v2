# -*- coding: utf-8 -*-
"""Unit tests for tables table_basic models."""

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.tables.operations import _serde
from alibabacloud_oss_v2.types import OperationInput, CaseInsensitiveDict
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
    IcebergSortField,
    IcebergSortOrder,
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
        self.assertIsNone(request.metadata.iceberg.schema_v2)

        json_str = (
            '{"name": "test_table", "format": "iceberg", "metadata": {"iceberg": {'
            '"schema": {"fields": [{"name": "id", "type": "long", "required": true}, '
            '{"name": "name", "type": "string", "required": false}, '
            '{"name": "ts", "type": "timestamptz", "required": false}]}, '
            '"partitionSpec": {"specId": 0, "fields": [{"sourceId": 2, "fieldId": 1001, '
            '"name": "region", "transform": "identity"}]}, '
            '"properties": {"owner": "table-owner", "environment": "production"}}}}'
        )
        op_input = _serde.serialize_input_tables_json_model(request, OperationInput(
            op_name='CreateTable', method='PUT', bucket=request.table_bucket_arn,
        ))
        self.assertEqual(op_input.op_name, 'CreateTable')
        self.assertEqual(op_input.method, 'PUT')
        self.assertEqual(op_input.bucket, 'acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket')
        self.assertEqual(op_input.parameters, {'namespace': 'test_namespace'})
        self.assertEqual(request.name, 'test_table')
        self.assertEqual(request.format, 'iceberg')
        self.assertEqual(request.metadata.iceberg.schema.fields[0].name, 'id')
        self.assertEqual(request.metadata.iceberg.schema.fields[0].type, 'long')
        self.assertIs(request.metadata.iceberg.schema.fields[0].required, True)
        self.assertIs(request.metadata.iceberg.schema.fields[1].required, False)
        self.assertEqual(request.metadata.iceberg.partition_spec.spec_id, 0)
        self.assertEqual(request.metadata.iceberg.partition_spec.fields[0].source_id, 2)
        self.assertEqual(request.metadata.iceberg.properties,
                         {'owner': 'table-owner', 'environment': 'production'})
        self.assertEqual(json_str, op_input.body.decode('utf-8'))

    def test_serialize_request_with_schema_v2(self):
        """Compare all model parameters and the JSON request body containing structs, lists, and maps."""
        schema_v2 = {
            "type": "struct", "schema-id": 0, "identifier-field-ids": [10],
            "fields": [
                {"id": 10, "name": "order_id", "type": "long", "required": True, "doc": "Order ID"},
                {
                    "id": 20, "name": "customer", "required": False,
                    "type": {"type": "struct", "fields": [
                        {"id": 21, "name": "name", "type": "string", "required": False},
                        {"id": 22, "name": "level", "type": "int", "required": False},
                    ]},
                },
                {
                    "id": 30, "name": "tags", "required": False,
                    "type": {"type": "list", "element-id": 31,
                             "element": "string", "element-required": False},
                },
                {
                    "id": 40, "name": "attributes", "required": False,
                    "type": {"type": "map", "key-id": 41, "key": "string",
                             "value-id": 42, "value": "string", "value-required": False},
                },
            ],
        }
        metadata = TableMetadata(iceberg=IcebergMetadata(
            partition_spec=IcebergPartitionSpec(spec_id=0, fields=[
                IcebergPartitionField(source_id=10, field_id=1001, name="order_id", transform="identity"),
            ]),
            sort_order=IcebergSortOrder(fields=[
                IcebergSortField(source_id=10, direction="asc", null_order="nulls-first", transform="identity"),
            ]),
            properties={"format-version": "2"},
            schema_v2=schema_v2,
        ))
        request = CreateTableRequest(
            table_bucket_arn='acs:osstables:cn-hangzhou:123456789012:bucket/test-table-bucket',
            namespace='test_namespace', name='orders_nested', format='ICEBERG',
            metadata=metadata,
            encryption_configuration=EncryptionConfiguration(sse_algorithm='AES256'),
        )
        json_str = (
            '{"name": "orders_nested", "format": "ICEBERG", "metadata": {"iceberg": {'
            '"partitionSpec": {"specId": 0, "fields": [{"sourceId": 10, "fieldId": 1001, '
            '"name": "order_id", "transform": "identity"}]}, '
            '"sortOrder": {"fields": [{"sourceId": 10, "direction": "asc", '
            '"nullOrder": "nulls-first", "transform": "identity"}]}, '
            '"properties": {"format-version": "2"}, '
            '"schemaV2": {"type": "struct", "schema-id": 0, "identifier-field-ids": [10], "fields": ['
            '{"id": 10, "name": "order_id", "type": "long", "required": true, "doc": "Order ID"}, '
            '{"id": 20, "name": "customer", "required": false, "type": {"type": "struct", "fields": ['
            '{"id": 21, "name": "name", "type": "string", "required": false}, '
            '{"id": 22, "name": "level", "type": "int", "required": false}]}}, '
            '{"id": 30, "name": "tags", "required": false, "type": {"type": "list", '
            '"element-id": 31, "element": "string", "element-required": false}}, '
            '{"id": 40, "name": "attributes", "required": false, "type": {"type": "map", '
            '"key-id": 41, "key": "string", "value-id": 42, "value": "string", "value-required": false}}'
            ']}}}, "encryptionConfiguration": {"sseAlgorithm": "AES256"}}'
        )
        op_input = _serde.serialize_input_tables_json_model(request, OperationInput(
            op_name='CreateTable', method='PUT', bucket=request.table_bucket_arn,
            headers=CaseInsensitiveDict({'Content-Type': 'application/json'}),
        ))
        self.assertIsInstance(request, serde.RequestModel)
        self.assertEqual(op_input.op_name, 'CreateTable')
        self.assertEqual(op_input.method, 'PUT')
        self.assertEqual(op_input.bucket, 'acs:osstables:cn-hangzhou:123456789012:bucket/test-table-bucket')
        self.assertEqual(op_input.parameters, {'namespace': 'test_namespace'})
        self.assertEqual(op_input.headers['Content-Type'], 'application/json')
        self.assertEqual(request.table_bucket_arn, op_input.bucket)
        self.assertEqual(request.namespace, 'test_namespace')
        self.assertEqual(request.name, 'orders_nested')
        self.assertEqual(request.format, 'ICEBERG')
        self.assertIsNone(request.metadata.iceberg.schema)
        self.assertEqual(request.metadata.iceberg.schema_v2, schema_v2)
        self.assertEqual(request.metadata.iceberg.properties, {'format-version': '2'})
        partition = request.metadata.iceberg.partition_spec
        self.assertEqual(partition.spec_id, 0)
        self.assertEqual(partition.fields[0].source_id, 10)
        self.assertEqual(partition.fields[0].field_id, 1001)
        self.assertEqual(partition.fields[0].name, 'order_id')
        self.assertEqual(partition.fields[0].transform, 'identity')
        sort_field = request.metadata.iceberg.sort_order.fields[0]
        self.assertEqual(sort_field.source_id, 10)
        self.assertEqual(sort_field.direction, 'asc')
        self.assertEqual(sort_field.null_order, 'nulls-first')
        self.assertEqual(sort_field.transform, 'identity')
        self.assertEqual(request.encryption_configuration.sse_algorithm, 'AES256')
        self.assertIsNone(request.encryption_configuration.kms_key_arn)
        fields = request.metadata.iceberg.schema_v2['fields']
        self.assertEqual(request.metadata.iceberg.schema_v2['type'], 'struct')
        self.assertEqual(request.metadata.iceberg.schema_v2['schema-id'], 0)
        self.assertEqual(request.metadata.iceberg.schema_v2['identifier-field-ids'], [10])
        self.assertEqual(fields[0], {'id': 10, 'name': 'order_id', 'type': 'long',
                                     'required': True, 'doc': 'Order ID'})
        self.assertIs(fields[1]['required'], False)
        self.assertEqual(fields[1]['type']['fields'][1]['type'], 'int')
        self.assertEqual(fields[2]['type']['element-id'], 31)
        self.assertEqual(fields[2]['type']['element'], 'string')
        self.assertIs(fields[2]['type']['element-required'], False)
        self.assertEqual(fields[3]['type']['key-id'], 41)
        self.assertEqual(fields[3]['type']['key'], 'string')
        self.assertEqual(fields[3]['type']['value-id'], 42)
        self.assertEqual(fields[3]['type']['value'], 'string')
        self.assertIs(fields[3]['type']['value-required'], False)
        self.assertEqual(json_str, op_input.body.decode('utf-8'))

    def test_serialize_request_with_schema_v2_dict_metadata(self):
        """Verify dictionary metadata and parameter forwarding for lists of structs containing maps."""
        schema_v2 = {
            'type': 'struct',
            'fields': [{
                'id': 10, 'name': 'items', 'required': False,
                'type': {
                    'type': 'list', 'element-id': 11, 'element-required': True,
                    'element': {'type': 'struct', 'fields': [{
                        'id': 12, 'name': 'attributes',
                        'type': {'type': 'map', 'key-id': 13, 'key': 'string',
                                 'value-id': 14, 'value': 'long', 'value-required': False},
                    }]},
                },
            }],
        }
        metadata = {'iceberg': {'schemaV2': schema_v2, 'properties': {'format-version': '2'}}}
        request = CreateTableRequest(
            table_bucket_arn='acs:osstables:cn-hangzhou:123456789012:bucket/test-table-bucket',
            namespace='test_namespace', name='nested_items', format='ICEBERG', metadata=metadata,
        )
        json_str = (
            '{"name": "nested_items", "format": "ICEBERG", "metadata": {"iceberg": {'
            '"schemaV2": {"type": "struct", "fields": [{"id": 10, "name": "items", "required": false, '
            '"type": {"type": "list", "element-id": 11, "element-required": true, '
            '"element": {"type": "struct", "fields": [{"id": 12, "name": "attributes", '
            '"type": {"type": "map", "key-id": 13, "key": "string", "value-id": 14, '
            '"value": "long", "value-required": false}}]}}}]}, "properties": {"format-version": "2"}}}}'
        )
        op_input = _serde.serialize_input_tables_json_model(request, OperationInput(
            op_name='CreateTable', method='PUT', bucket=request.table_bucket_arn,
        ))
        self.assertIsInstance(request, serde.RequestModel)
        self.assertEqual(op_input.op_name, 'CreateTable')
        self.assertEqual(op_input.method, 'PUT')
        self.assertEqual(op_input.bucket, 'acs:osstables:cn-hangzhou:123456789012:bucket/test-table-bucket')
        self.assertEqual(op_input.parameters, {'namespace': 'test_namespace'})
        self.assertEqual(request.table_bucket_arn, op_input.bucket)
        self.assertEqual(request.namespace, 'test_namespace')
        self.assertEqual(request.name, 'nested_items')
        self.assertEqual(request.format, 'ICEBERG')
        self.assertEqual(request.metadata, metadata)
        self.assertEqual(request.metadata['iceberg']['schemaV2'], schema_v2)
        self.assertEqual(request.metadata['iceberg']['properties'], {'format-version': '2'})
        self.assertIsNone(request.encryption_configuration)
        list_type = request.metadata['iceberg']['schemaV2']['fields'][0]['type']
        self.assertEqual(list_type['type'], 'list')
        self.assertEqual(list_type['element-id'], 11)
        self.assertIs(list_type['element-required'], True)
        self.assertEqual(list_type['element']['type'], 'struct')
        map_type = list_type['element']['fields'][0]['type']
        self.assertEqual(map_type, {'type': 'map', 'key-id': 13, 'key': 'string',
                                    'value-id': 14, 'value': 'long', 'value-required': False})
        self.assertEqual(json_str, op_input.body.decode('utf-8'))

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", CreateTableRequest._attribute_map)
        self.assertIn("namespace", CreateTableRequest._attribute_map)
        self.assertIn("name", CreateTableRequest._attribute_map)
        self.assertIn("format", CreateTableRequest._attribute_map)
        self.assertIn("metadata", CreateTableRequest._attribute_map)
        self.assertEqual(CreateTableRequest._attribute_map["table_bucket_arn"]["position"], "host")
        self.assertTrue(CreateTableRequest._attribute_map["table_bucket_arn"]["required"])
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
        self.assertEqual(GetTableResult._attribute_map["table_arn"]["rename"], "tableARN")


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
        self.assertIsNone(request.name)
        self.assertIsNone(request.new_namespace_name)
        self.assertIsNone(request.new_name)
        self.assertIsNone(request.version_token)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = RenameTableRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="test_namespace",
            name="old_table",
            new_namespace_name="new_namespace",
            new_name="new_table",
            version_token="aaabbb"
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.name, "old_table")
        self.assertEqual(request.new_namespace_name, "new_namespace")
        self.assertEqual(request.new_name, "new_table")
        self.assertEqual(request.version_token, "aaabbb")


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
