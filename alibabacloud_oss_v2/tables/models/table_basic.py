# -*- coding: utf-8 -*-
"""Table models for tables operations."""

import datetime
from typing import Optional, List, Any, Dict, Union
from ... import serde
from .common import TableSummary, TableMetadata, EncryptionConfiguration


class CreateTableRequest(serde.RequestModel):
    """The request for the CreateTable operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "query", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "body", "rename": "name"},
        "format": {"tag": "input", "position": "body", "rename": "format"},
        "metadata": {"tag": "input", "position": "body", "rename": "metadata", "type": "TableMetadata"},
        "encryption_configuration": {"tag": "input", "position": "body", "rename": "encryptionConfiguration", "type": "EncryptionConfiguration"},
    }

    _dependency_map = {
        "TableMetadata": {"new": lambda: TableMetadata()},
        "EncryptionConfiguration": {"new": lambda: EncryptionConfiguration()},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: Optional[str] = None,
        format: Optional[str] = None,
        metadata: Optional[Union[TableMetadata,Dict]] = None,
        encryption_configuration: Optional[EncryptionConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, optional): The name of the table.
            format (str, optional): The format of the table.
            metadata (TableMetadata, optional): The metadata of the table.
            encryption_configuration (EncryptionConfiguration, optional): The encryption configuration.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name
        self.format = format
        self.metadata = metadata
        self.encryption_configuration = encryption_configuration


class CreateTableResult(serde.ResultModel):
    """The result for the CreateTable operation."""

    _attribute_map = {
        "table_arn": {"tag": "output", "position": "body", "rename": "tableARN"},
        "version_token": {"tag": "output", "position": "body", "rename": "versionToken"},
    }

    def __init__(
        self,
        table_arn: Optional[str] = None,
        version_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_arn (str, optional): The ARN of the created table.
            version_token (str, optional): The version token of the created table.
        """
        super().__init__(**kwargs)
        self.table_arn = table_arn
        self.version_token = version_token


class DeleteTableRequest(serde.RequestModel):
    """The request for the DeleteTable operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
        "version_token": {"tag": "input", "position": "query", "rename": "versionToken"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        version_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table to delete.
            version_token (str, optional): The version token.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name
        self.version_token = version_token


class DeleteTableResult(serde.ResultModel):
    """The result for the DeleteTable operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GetTableRequest(serde.RequestModel):
    """The request for the GetTable operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "query", "rename": "tableBucketARN"},
        "namespace": {"tag": "input", "position": "query", "rename": "namespace"},
        "name": {"tag": "input", "position": "query", "rename": "name"},
        "table_arn": {"tag": "input", "position": "query", "rename": "tableArn"},
    }

    def __init__(
        self,
        table_bucket_arn: Optional[str] = None,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        table_arn: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, optional): The ARN of the table bucket.
            namespace (str, optional): The namespace.
            name (str, optional): The table to get.
            table_arn (str, optional): The ARN of the table bucket.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name
        self.table_arn = table_arn


class GetTableResult(serde.ResultModel):
    """The result for the GetTable operation."""

    _attribute_map = {
        "namespace": {"tag": "output", "position": "body", "rename": "namespace", "type": "[str]"},
        "name": {"tag": "output", "position": "body", "rename": "name"},
        "type": {"tag": "output", "position": "body", "rename": "type"},
        "table_arn": {"tag": "output", "position": "body", "rename": "tableARN"},
        "created_at": {"tag": "output", "position": "body", "rename": "createdAt"},
        "modified_at": {"tag": "output", "position": "body", "rename": "modifiedAt"},
        "namespace_id": {"tag": "output", "position": "body", "rename": "namespaceId"},
        "format": {"tag": "output", "position": "body", "rename": "format"},
        "version_token": {"tag": "output", "position": "body", "rename": "versionToken"},
        "metadata_location": {"tag": "output", "position": "body", "rename": "metadataLocation"},
        "warehouse_location": {"tag": "output", "position": "body", "rename": "warehouseLocation"},
        "created_by": {"tag": "output", "position": "body", "rename": "createdBy"},
        "modified_by": {"tag": "output", "position": "body", "rename": "modifiedBy"},
        "owner_account_id": {"tag": "output", "position": "body", "rename": "ownerAccountId"},
        "table_bucket_id": {"tag": "output", "position": "body", "rename": "tableBucketId"},
    }

    def __init__(
        self,
        namespace: Optional[List[str]] = None,
        name: Optional[str] = None,
        type: Optional[str] = None,
        table_arn: Optional[str] = None,
        created_at: Optional[str] = None,
        modified_at: Optional[str] = None,
        namespace_id: Optional[str] = None,
        format: Optional[str] = None,
        version_token: Optional[str] = None,
        metadata_location: Optional[str] = None,
        warehouse_location: Optional[str] = None,
        created_by: Optional[str] = None,
        modified_by: Optional[str] = None,
        owner_account_id: Optional[str] = None,
        table_bucket_id: Optional[str] = None,
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
            namespace_id (str, optional): The namespace ID.
            format (str, optional): The format of the table.
            version_token (str, optional): The version token of the table.
            metadata_location (str, optional): The metadata location of the table.
            warehouse_location (str, optional): The warehouse location of the table.
            created_by (str, optional): The creator of the table.
            modified_by (str, optional): The last modifier of the table.
            owner_account_id (str, optional): The owner account ID of the table.
            table_bucket_id (str, optional): The table bucket ID.
        """
        super().__init__(**kwargs)
        self.namespace = namespace
        self.name = name
        self.type = type
        self.table_arn = table_arn
        self.created_at = created_at
        self.modified_at = modified_at
        self.namespace_id = namespace_id
        self.format = format
        self.version_token = version_token
        self.metadata_location = metadata_location
        self.warehouse_location = warehouse_location
        self.created_by = created_by
        self.modified_by = modified_by
        self.owner_account_id = owner_account_id
        self.table_bucket_id = table_bucket_id


class ListTablesRequest(serde.RequestModel):
    """The request for the ListTables operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "query", "rename": "namespace", "required": True},
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
        "continuation_token": {"tag": "input", "position": "query", "rename": "continuationToken"},
        "max_tables": {"tag": "input", "position": "query", "rename": "maxTables"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        prefix: Optional[str] = None,
        continuation_token: Optional[str] = None,
        max_tables: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            prefix (str, optional): The prefix to filter tables.
            continuation_token (str, optional): The continuation token.
            max_tables (int, optional): The maximum number of tables.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.prefix = prefix
        self.continuation_token = continuation_token
        self.max_tables = max_tables


class ListTablesResult(serde.ResultModel):
    """The result for the ListTables operation."""

    _attribute_map = {
        "tables": {"tag": "output", "position": "body", "rename": "tables", "type": "[TableSummary]"},
        "continuation_token": {"tag": "output", "position": "body", "rename": "continuationToken"},
    }

    _dependency_map = {
        "TableSummary": {"new": lambda: TableSummary()},
    }

    def __init__(
        self,
        table_summaries: Optional[List[TableSummary]] = None,
        continuation_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_summaries (List[TableSummary], optional): The list of table summaries.
            continuation_token (str, optional): The continuation token.
        """
        super().__init__(**kwargs)
        self.table_summaries = table_summaries
        self.continuation_token = continuation_token


class RenameTableRequest(serde.RequestModel):
    """The request for the RenameTable operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
        "new_namespace_name": {"tag": "input", "position": "body", "rename": "newNamespaceName"},
        "new_name": {"tag": "input", "position": "body", "rename": "newName"},
        "version_token": {"tag": "input", "position": "body", "rename": "versionToken"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        new_namespace_name: Optional[str] = None,
        new_name: Optional[str] = None,
        version_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table to rename.
            new_namespace_name (str, optional): The new namespace name.
            new_name (str, optional): The new name of the table.
            version_token (str, optional): The version token.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name
        self.new_namespace_name = new_namespace_name
        self.new_name = new_name
        self.version_token = version_token


class RenameTableResult(serde.ResultModel):
    """The result for the RenameTable operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
