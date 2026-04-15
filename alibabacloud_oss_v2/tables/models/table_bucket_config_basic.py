# -*- coding: utf-8 -*-
"""Table Bucket configuration models for tables operations."""

from typing import Optional, Dict, Any
from ... import serde
from .common import EncryptionConfiguration


class DeleteTableBucketEncryptionRequest(serde.RequestModel):
    """The request for the DeleteTableBucketEncryption operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn


class DeleteTableBucketEncryptionResult(serde.ResultModel):
    """The result for the DeleteTableBucketEncryption operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GetTableBucketEncryptionRequest(serde.RequestModel):
    """The request for the GetTableBucketEncryption operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn


class GetTableBucketEncryptionResult(serde.ResultModel):
    """The result for the GetTableBucketEncryption operation."""

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
        """
        Args:
            encryption_configuration (EncryptionConfiguration, optional): The encryption configuration.
        """
        super().__init__(**kwargs)
        self.encryption_configuration = encryption_configuration


class PutTableBucketEncryptionRequest(serde.RequestModel):
    """The request for the PutTableBucketEncryption operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "encryption_configuration": {"tag": "input", "position": "body", "rename": "encryptionConfiguration", "type": "EncryptionConfiguration"},
    }

    _dependency_map = {
        "EncryptionConfiguration": {"new": lambda: EncryptionConfiguration()},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        encryption_configuration: Optional[EncryptionConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            encryption_configuration (EncryptionConfiguration, optional): The encryption configuration.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.encryption_configuration = encryption_configuration


class PutTableBucketEncryptionResult(serde.ResultModel):
    """The result for the PutTableBucketEncryption operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GetTableBucketMaintenanceConfigurationRequest(serde.RequestModel):
    """The request for the GetTableBucketMaintenanceConfiguration operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn


class GetTableBucketMaintenanceConfigurationResult(serde.ResultModel):
    """The result for the GetTableBucketMaintenanceConfiguration operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "output", "position": "body", "rename": "tableBucketARN"},
        "configuration": {"tag": "output", "position": "body", "rename": "configuration"},
    }

    def __init__(
        self,
        table_bucket_arn: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, optional): The ARN of the table bucket.
            configuration (Dict[str, Any], optional): The maintenance configuration map.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.configuration = configuration


class PutTableBucketMaintenanceConfigurationRequest(serde.RequestModel):
    """The request for the PutTableBucketMaintenanceConfiguration operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "type": {"tag": "input", "position": "path", "rename": "type", "required": True},
        "value": {"tag": "input", "position": "body", "rename": "value"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        type: str = None,
        value: Optional[Dict] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            type (str, required): The maintenance type, e.g., icebergUnreferencedFileRemoval.
            value (Dict, optional): The maintenance configuration value containing status and settings.
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
        self.type = type
        self.value = value


class PutTableBucketMaintenanceConfigurationResult(serde.ResultModel):
    """The result for the PutTableBucketMaintenanceConfiguration operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class DeleteTableBucketPolicyRequest(serde.RequestModel):
    """The request for the DeleteTableBucketPolicy operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn


class DeleteTableBucketPolicyResult(serde.ResultModel):
    """The result for the DeleteTableBucketPolicy operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GetTableBucketPolicyRequest(serde.RequestModel):
    """The request for the GetTableBucketPolicy operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn


class GetTableBucketPolicyResult(serde.ResultModel):
    """The result for the GetTableBucketPolicy operation."""

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


class PutTableBucketPolicyRequest(serde.RequestModel):
    """The request for the PutTableBucketPolicy operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "resource_policy": {"tag": "input", "position": "body", "rename": "resourcePolicy"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        resource_policy: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.resource_policy = resource_policy


class PutTableBucketPolicyResult(serde.ResultModel):
    """The result for the PutTableBucketPolicy operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
