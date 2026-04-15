# -*- coding: utf-8 -*-
"""Common models for tables operations."""

import datetime
from typing import Optional, List, Any, Dict
from ... import serde


class SchemaField(serde.Model):
    """SchemaField defines a field in the schema."""

    _attribute_map = {
        "name": {"tag": "json", "rename": "name"},
        "type": {"tag": "json", "rename": "type"},
        "required": {"tag": "json", "rename": "required", "type": "bool"},
    }

    def __init__(
        self,
        name: Optional[str] = None,
        type: Optional[str] = None,
        required: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the field.
            type (str, optional): The type of the field.
            required (bool, optional): Whether the field is required.
        """
        super().__init__(**kwargs)
        self.name = name
        self.type = type
        self.required = required


class IcebergPartitionField(serde.Model):
    """IcebergPartitionField defines a partition field."""

    _attribute_map = {
        "source_id": {"tag": "json", "rename": "sourceId", "type": "int"},
        "field_id": {"tag": "json", "rename": "fieldId", "type": "int"},
        "name": {"tag": "json", "rename": "name"},
        "transform": {"tag": "json", "rename": "transform"},
    }

    def __init__(
        self,
        source_id: Optional[int] = None,
        field_id: Optional[int] = None,
        name: Optional[str] = None,
        transform: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            source_id (int, optional): The source column id.
            field_id (int, optional): The partition field id.
            name (str, optional): The name of the partition field.
            transform (str, optional): The transform function.
        """
        super().__init__(**kwargs)
        self.source_id = source_id
        self.field_id = field_id
        self.name = name
        self.transform = transform


class IcebergSortField(serde.Model):
    """IcebergSortField defines a sort field."""

    _attribute_map = {
        "source_id": {"tag": "json", "rename": "sourceId", "type": "int"},
        "direction": {"tag": "json", "rename": "direction"},
        "null_order": {"tag": "json", "rename": "nullOrder"},
        "transform": {"tag": "json", "rename": "transform"},
    }

    def __init__(
        self,
        source_id: Optional[int] = None,
        direction: Optional[str] = None,
        null_order: Optional[str] = None,
        transform: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            source_id (int, optional): The source column id.
            direction (str, optional): The sort direction.
            null_order (str, optional): The null order.
            transform (str, optional): The transform function.
        """
        super().__init__(**kwargs)
        self.source_id = source_id
        self.direction = direction
        self.null_order = null_order
        self.transform = transform


class IcebergSchema(serde.Model):
    """IcebergSchema defines the schema of an Iceberg table."""

    _attribute_map = {
        "fields": {"tag": "json", "rename": "fields", "type": "[SchemaField]"},
    }

    _dependency_map = {
        "SchemaField": {"new": lambda: SchemaField()},
    }

    def __init__(
        self,
        fields: Optional[List[SchemaField]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            fields (List[SchemaField], optional): The list of schema fields.
        """
        super().__init__(**kwargs)
        self.fields = fields


class IcebergPartitionSpec(serde.Model):
    """IcebergPartitionSpec defines the partition specification."""

    _attribute_map = {
        "spec_id": {"tag": "json", "rename": "specId", "type": "int"},
        "fields": {"tag": "json", "rename": "fields", "type": "[IcebergPartitionField]"},
    }

    _dependency_map = {
        "IcebergPartitionField": {"new": lambda: IcebergPartitionField()},
    }

    def __init__(
        self,
        spec_id: Optional[int] = None,
        fields: Optional[List[IcebergPartitionField]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            spec_id (int, optional): The partition specification ID.
            fields (List[IcebergPartitionField], optional): The list of partition fields.
        """
        super().__init__(**kwargs)
        self.spec_id = spec_id
        self.fields = fields


class IcebergSortOrder(serde.Model):
    """IcebergSortOrder defines the sort order."""

    _attribute_map = {
        "fields": {"tag": "json", "rename": "fields", "type": "[IcebergSortField]"},
    }

    _dependency_map = {
        "IcebergSortField": {"new": lambda: IcebergSortField()},
    }

    def __init__(
        self,
        fields: Optional[List[IcebergSortField]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            fields (List[IcebergSortField], optional): The list of sort fields.
        """
        super().__init__(**kwargs)
        self.fields = fields


class IcebergMetadata(serde.Model):
    """IcebergMetadata defines the Iceberg metadata."""

    _attribute_map = {
        "schema": {"tag": "json", "rename": "schema", "type": "IcebergSchema"},
        "partition_spec": {"tag": "json", "rename": "partitionSpec", "type": "IcebergPartitionSpec"},
        "sort_order": {"tag": "json", "rename": "sortOrder", "type": "IcebergSortOrder"},
        "properties": {"tag": "json", "rename": "properties", "type": "dict"},
    }

    _dependency_map = {
        "IcebergSchema": {"new": lambda: IcebergSchema()},
        "IcebergPartitionSpec": {"new": lambda: IcebergPartitionSpec()},
        "IcebergSortOrder": {"new": lambda: IcebergSortOrder()},
    }

    def __init__(
        self,
        schema: Optional[IcebergSchema] = None,
        partition_spec: Optional[IcebergPartitionSpec] = None,
        sort_order: Optional[IcebergSortOrder] = None,
        properties: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            schema (IcebergSchema, optional): The schema of the Iceberg table.
            partition_spec (IcebergPartitionSpec, optional): The partition specification.
            sort_order (IcebergSortOrder, optional): The sort order.
            properties (Dict[str, str], optional): The properties map.
        """
        super().__init__(**kwargs)
        self.schema = schema
        self.partition_spec = partition_spec
        self.sort_order = sort_order
        self.properties = properties


class TableMetadata(serde.Model):
    """TableMetadata defines the metadata of a table."""

    _attribute_map = {
        "iceberg": {"tag": "json", "rename": "iceberg", "type": "IcebergMetadata"},
    }

    _dependency_map = {
        "IcebergMetadata": {"new": lambda: IcebergMetadata()},
    }

    def __init__(
        self,
        iceberg: Optional[IcebergMetadata] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            iceberg (IcebergMetadata, optional): The Iceberg metadata.
        """
        super().__init__(**kwargs)
        self.iceberg = iceberg


class EncryptionConfiguration(serde.Model):
    """EncryptionConfiguration defines the encryption configuration."""

    _attribute_map = {
        "sse_algorithm": {"tag": "json", "rename": "sseAlgorithm"},
        "kms_key_arn": {"tag": "json", "rename": "kmsKeyArn"},
    }

    def __init__(
        self,
        sse_algorithm: Optional[str] = None,
        kms_key_arn: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            sse_algorithm (str, optional): The server-side encryption algorithm.
            kms_key_arn (str, optional): The ARN of the KMS key.
        """
        super().__init__(**kwargs)
        self.sse_algorithm = sse_algorithm
        self.kms_key_arn = kms_key_arn


class NamespaceSummary(serde.Model):
    """NamespaceSummary defines the namespace summary information."""

    _attribute_map = {
        "namespace": {"tag": "json", "rename": "namespace", "type": "[str]"},
        "created_at": {"tag": "json", "rename": "createdAt"},
        "created_by": {"tag": "json", "rename": "createdBy"},
        "owner_account_id": {"tag": "json", "rename": "ownerAccountId"},
        "namespace_id": {"tag": "json", "rename": "namespaceId"},
    }

    def __init__(
        self,
        namespace: Optional[List[str]] = None,
        created_at: Optional[datetime.datetime] = None,
        created_by: Optional[str] = None,
        owner_account_id: Optional[str] = None,
        namespace_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            namespace (List[str], optional): The namespace path.
            created_at (datetime, optional): The creation time.
            created_by (str, optional): The creator.
            owner_account_id (str, optional): The owner account ID.
            namespace_id (str, optional): The namespace ID.
        """
        super().__init__(**kwargs)
        self.namespace = namespace
        self.created_at = created_at
        self.created_by = created_by
        self.owner_account_id = owner_account_id
        self.namespace_id = namespace_id


class TableBucketSummary(serde.Model):
    """TableBucketSummary defines the table bucket summary information."""

    _attribute_map = {
        "arn": {"tag": "json", "rename": "arn"},
        "name": {"tag": "json", "rename": "name"},
        "owner_account_id": {"tag": "json", "rename": "ownerAccountId"},
        "created_at": {"tag": "json", "rename": "createdAt", "type": "datetime"},
        "table_bucket_id": {"tag": "json", "rename": "tableBucketId"},
        "type": {"tag": "json", "rename": "type"},
    }

    def __init__(
        self,
        arn: Optional[str] = None,
        name: Optional[str] = None,
        owner_account_id: Optional[str] = None,
        created_at: Optional[datetime.datetime] = None,
        table_bucket_id: Optional[str] = None,
        type: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            arn (str, optional): The ARN of the table bucket.
            name (str, optional): The name of the table bucket.
            owner_account_id (str, optional): The owner account ID.
            created_at (datetime, optional): The creation time.
            table_bucket_id (str, optional): The table bucket ID.
            type (str, optional): The type of the table bucket.
        """
        super().__init__(**kwargs)
        self.arn = arn
        self.name = name
        self.owner_account_id = owner_account_id
        self.created_at = created_at
        self.table_bucket_id = table_bucket_id
        self.type = type


class TableSummary(serde.Model):
    """TableSummary defines the table summary information."""

    _attribute_map = {
        "namespace": {"tag": "json", "rename": "namespace", "type": "[str]"},
        "name": {"tag": "json", "rename": "name"},
        "type": {"tag": "json", "rename": "type"},
        "table_arn": {"tag": "json", "rename": "tableARN"},
        "created_at": {"tag": "json", "rename": "createdAt"},
        "modified_at": {"tag": "json", "rename": "modifiedAt"},
    }

    def __init__(
        self,
        namespace: Optional[List[str]] = None,
        name: Optional[str] = None,
        type: Optional[str] = None,
        table_arn: Optional[str] = None,
        created_at: Optional[str] = None,
        modified_at: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            namespace (List[str], optional): The namespace path.
            name (str, optional): The name of the table.
            type (str, optional): The type of the table.
            table_arn (str, optional): The ARN of the table.
            created_at (str, optional): The creation time.
            modified_at (str, optional): The modification time.
        """
        super().__init__(**kwargs)
        self.namespace = namespace
        self.name = name
        self.type = type
        self.table_arn = table_arn
        self.created_at = created_at
        self.modified_at = modified_at
