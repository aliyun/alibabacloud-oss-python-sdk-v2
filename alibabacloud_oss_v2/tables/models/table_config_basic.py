# -*- coding: utf-8 -*-
"""Table configuration models for tables operations."""

import datetime
from typing import Optional, List, Any, Dict
from ... import serde
from .common import TableMetadata, EncryptionConfiguration


class GetTableEncryptionRequest(serde.RequestModel):
    """The request for the GetTableEncryption operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table name.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name


class GetTableEncryptionResult(serde.ResultModel):
    """The result for the GetTableEncryption operation."""

    _attribute_map = {
        "encryption_configuration": {"tag": "output", "position": "body", "rename": "encryptionConfiguration", "type": "EncryptionConfiguration"},
    }

    _dependency_map = {
        "EncryptionConfiguration": {"new": lambda: EncryptionConfiguration()},
    }

    def __init__(
        self,
        encryption_configuration: Optional[EncryptionConfiguration] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.encryption_configuration = encryption_configuration


class GetTableMaintenanceConfigurationRequest(serde.RequestModel):
    """The request for the GetTableMaintenanceConfiguration operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table name.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name


class GetTableMaintenanceConfigurationResult(serde.ResultModel):
    """The result for the GetTableMaintenanceConfiguration operation."""

    _attribute_map = {
        "table_arn": {"tag": "output", "position": "body", "rename": "tableARN"},
        "configuration": {"tag": "output", "position": "body", "rename": "configuration"},
    }

    def __init__(
        self,
        table_arn: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_arn (str, optional): The ARN of the table.
            configuration (Dict[str, Any], optional): The maintenance configuration map.
        """
        super().__init__(**kwargs)
        self.table_arn = table_arn
        self.configuration = configuration


class PutTableMaintenanceConfigurationRequest(serde.RequestModel):
    """The request for the PutTableMaintenanceConfiguration operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
        "type": {"tag": "input", "position": "path", "rename": "type", "required": True},
        "value": {"tag": "input", "position": "body", "rename": "value"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        type: str = None,
        value: Optional[Dict] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table name.
            type (str, required): The maintenance type, e.g., icebergUnreferencedFileRemoval.
            value (Dict, optional): The maintenance configuration value.
                Example: {
                    'status': 'enabled',
                    'settings': {
                        'icebergUnreferencedFileRemoval': {
                            'unreferencedDays': 7,
                            'nonCurrentDays': 30
                        }
                    }
                }
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name
        self.type = type
        self.value = value


class PutTableMaintenanceConfigurationResult(serde.ResultModel):
    """The result for the PutTableMaintenanceConfiguration operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GetTableMaintenanceJobStatusRequest(serde.RequestModel):
    """The request for the GetTableMaintenanceJobStatus operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "table_arn": {"tag": "input", "position": "header", "rename": "x-oss-table-arn", "required": False},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        table_arn: str = None,
        namespace: str = None,
        name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            table_arn (str, optional): The ARN of the table (required for admin users).
            namespace (str, required): The namespace.
            name (str, required): The table name.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.table_arn = table_arn
        self.namespace = namespace
        self.name = name


class GetTableMaintenanceJobStatusResult(serde.ResultModel):
    """The result for the GetTableMaintenanceJobStatus operation."""

    _attribute_map = {
        "table_arn": {"tag": "output", "position": "body", "rename": "tableARN"},
        "status": {"tag": "output", "position": "body", "rename": "status", "type": "dict"},
    }

    def __init__(
        self,
        table_arn: Optional[str] = None,
        status: Optional[Dict] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_arn (str, optional): The ARN of the table.
            status (Dict, optional): The job status map.
        """
        super().__init__(**kwargs)
        self.table_arn = table_arn
        self.status = status


class GetTableMetadataLocationRequest(serde.RequestModel):
    """The request for the GetTableMetadataLocation operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table name.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name


class GetTableMetadataLocationResult(serde.ResultModel):
    """The result for the GetTableMetadataLocation operation."""

    _attribute_map = {
        "version_token": {"tag": "output", "position": "body", "rename": "versionToken"},
        "metadata_location": {"tag": "output", "position": "body", "rename": "metadataLocation"},
        "warehouse_location": {"tag": "output", "position": "body", "rename": "warehouseLocation"},
    }

    def __init__(
        self,
        version_token: Optional[str] = None,
        metadata_location: Optional[str] = None,
        warehouse_location: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.version_token = version_token
        self.metadata_location = metadata_location
        self.warehouse_location = warehouse_location


class UpdateTableMetadataLocationRequest(serde.RequestModel):
    """The request for the UpdateTableMetadataLocation operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
        "version_token": {"tag": "input", "position": "body", "rename": "versionToken"},
        "metadata_location": {"tag": "input", "position": "body", "rename": "metadataLocation"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        version_token: Optional[str] = None,
        metadata_location: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table name.
            version_token (str, optional): The version token.
            metadata_location (str, optional): The metadata location.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name
        self.version_token = version_token
        self.metadata_location = metadata_location


class UpdateTableMetadataLocationResult(serde.ResultModel):
    """The result for the UpdateTableMetadataLocation operation."""

    _attribute_map = {
        "name": {"tag": "output", "position": "body", "rename": "name"},
        "version_token": {"tag": "output", "position": "body", "rename": "versionToken"},
        "metadata_location": {"tag": "output", "position": "body", "rename": "metadataLocation"},
        "namespace": {"tag": "output", "position": "body", "rename": "namespace", "type": "[str]"},
        "table_arn": {"tag": "output", "position": "body", "rename": "tableARN"},
    }

    def __init__(
        self,
        name: Optional[str] = None,
        version_token: Optional[str] = None,
        metadata_location: Optional[str] = None,
        namespace: Optional[List[str]] = None,
        table_arn: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.version_token = version_token
        self.metadata_location = metadata_location
        self.namespace = namespace
        self.table_arn = table_arn


class DeleteTablePolicyRequest(serde.RequestModel):
    """The request for the DeleteTablePolicy operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table name.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name


class DeleteTablePolicyResult(serde.ResultModel):
    """The result for the DeleteTablePolicy operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GetTablePolicyRequest(serde.RequestModel):
    """The request for the GetTablePolicy operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table name.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name


class GetTablePolicyResult(serde.ResultModel):
    """The result for the GetTablePolicy operation."""

    _attribute_map = {
        "resource_policy": {"tag": "output", "position": "body", "rename": "resourcePolicy"},
    }

    def __init__(
        self,
        resource_policy: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.resource_policy = resource_policy


class PutTablePolicyRequest(serde.RequestModel):
    """The request for the PutTablePolicy operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
        "name": {"tag": "input", "position": "path", "rename": "name", "required": True},
        "resource_policy": {"tag": "input", "position": "body", "rename": "resourcePolicy"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        name: str = None,
        resource_policy: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace.
            name (str, required): The table name.
            resource_policy (str, optional): The resource policy document.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace
        self.name = name
        self.resource_policy = resource_policy


class PutTablePolicyResult(serde.ResultModel):
    """The result for the PutTablePolicy operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
