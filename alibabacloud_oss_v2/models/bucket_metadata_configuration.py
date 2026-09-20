from enum import Enum
from typing import Any, Optional, Union

from .. import serde


class ConfigurationStateType(str, Enum):
    """The state of the inventory metadata table."""

    ENABLED = 'ENABLED'
    DISABLED = 'DISABLED'


class RecordExpirationType(str, Enum):
    """The expiration state of journal table records."""

    ENABLED = 'ENABLED'
    DISABLED = 'DISABLED'


class TableStatusType(str, Enum):
    """The creation state of a metadata table."""

    CREATING = 'CREATING'
    BACKFILLING = 'BACKFILLING'
    ACTIVE = 'ACTIVE'
    FAILED = 'FAILED'


class SseAlgorithmType(str, Enum):
    """The server-side encryption algorithm of a metadata table."""

    AES256 = 'AES256'
    OSS_KMS = 'oss:kms'


class RecordExpiration(serde.Model):
    """The container that stores the journal record expiration settings."""

    _attribute_map = {
        'expiration': {'tag': 'xml', 'rename': 'Expiration', 'type': 'str'},
        'days': {'tag': 'xml', 'rename': 'Days', 'type': 'int'},
    }

    _xml_map = {
        'name': 'RecordExpiration'
    }

    def __init__(
        self,
        expiration: Optional[Union[str, RecordExpirationType]] = None,
        days: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            expiration (str | RecordExpirationType, optional): Whether record expiration is enabled.
            days (int, optional): The number of days to retain records. The minimum value is 7.
        """
        super().__init__(**kwargs)
        self.expiration = expiration
        self.days = days


class MetadataTableEncryptionConfiguration(serde.Model):
    """The container that stores metadata table encryption settings."""

    _attribute_map = {
        'sse_algorithm': {'tag': 'xml', 'rename': 'SseAlgorithm', 'type': 'str'},
        'kms_key_arn': {'tag': 'xml', 'rename': 'KmsKeyArn', 'type': 'str'},
    }

    _xml_map = {
        'name': 'EncryptionConfiguration'
    }

    def __init__(
        self,
        sse_algorithm: Optional[Union[str, SseAlgorithmType]] = None,
        kms_key_arn: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            sse_algorithm (str | SseAlgorithmType, optional): The server-side encryption algorithm.
            kms_key_arn (str, optional): The ARN of the KMS key used for encryption.
        """
        super().__init__(**kwargs)
        self.sse_algorithm = sse_algorithm
        self.kms_key_arn = kms_key_arn


class JournalTableConfiguration(serde.Model):
    """The container that stores journal metadata table settings."""

    _attribute_map = {
        'record_expiration': {'tag': 'xml', 'rename': 'RecordExpiration', 'type': 'RecordExpiration,xml'},
        'encryption_configuration': {'tag': 'xml', 'rename': 'EncryptionConfiguration', 'type': 'MetadataTableEncryptionConfiguration,xml'},
    }

    _xml_map = {
        'name': 'JournalTableConfiguration'
    }

    _dependency_map = {
        'RecordExpiration': {'new': lambda: RecordExpiration()},
        'MetadataTableEncryptionConfiguration': {'new': lambda: MetadataTableEncryptionConfiguration()},
    }

    def __init__(
        self,
        record_expiration: Optional[RecordExpiration] = None,
        encryption_configuration: Optional[MetadataTableEncryptionConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            record_expiration (RecordExpiration, optional): The journal record expiration settings.
            encryption_configuration (MetadataTableEncryptionConfiguration, optional): The journal table encryption settings.
        """
        super().__init__(**kwargs)
        self.record_expiration = record_expiration
        self.encryption_configuration = encryption_configuration


class InventoryTableConfiguration(serde.Model):
    """The container that stores inventory metadata table settings."""

    _attribute_map = {
        'configuration_state': {'tag': 'xml', 'rename': 'ConfigurationState', 'type': 'str'},
        'encryption_configuration': {'tag': 'xml', 'rename': 'EncryptionConfiguration', 'type': 'MetadataTableEncryptionConfiguration,xml'},
    }

    _xml_map = {
        'name': 'InventoryTableConfiguration'
    }

    _dependency_map = {
        'MetadataTableEncryptionConfiguration': {'new': lambda: MetadataTableEncryptionConfiguration()},
    }

    def __init__(
        self,
        configuration_state: Optional[Union[str, ConfigurationStateType]] = None,
        encryption_configuration: Optional[MetadataTableEncryptionConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            configuration_state (str | ConfigurationStateType, optional): Whether the inventory table is enabled.
            encryption_configuration (MetadataTableEncryptionConfiguration, optional): The inventory table encryption settings.
        """
        super().__init__(**kwargs)
        self.configuration_state = configuration_state
        self.encryption_configuration = encryption_configuration


class MetadataConfiguration(serde.Model):
    """The container that stores bucket metadata table settings."""

    _attribute_map = {
        'journal_table_configuration': {'tag': 'xml', 'rename': 'JournalTableConfiguration', 'type': 'JournalTableConfiguration,xml'},
        'inventory_table_configuration': {'tag': 'xml', 'rename': 'InventoryTableConfiguration', 'type': 'InventoryTableConfiguration,xml'},
    }

    _xml_map = {
        'name': 'MetadataConfiguration'
    }

    _dependency_map = {
        'JournalTableConfiguration': {'new': lambda: JournalTableConfiguration()},
        'InventoryTableConfiguration': {'new': lambda: InventoryTableConfiguration()},
    }

    def __init__(
        self,
        journal_table_configuration: Optional[JournalTableConfiguration] = None,
        inventory_table_configuration: Optional[InventoryTableConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            journal_table_configuration (JournalTableConfiguration, optional): The journal metadata table settings.
            inventory_table_configuration (InventoryTableConfiguration, optional): The inventory metadata table settings.
        """
        super().__init__(**kwargs)
        self.journal_table_configuration = journal_table_configuration
        self.inventory_table_configuration = inventory_table_configuration


class MetadataTableError(serde.Model):
    """The container that stores a metadata table error."""

    _attribute_map = {
        'error_code': {'tag': 'xml', 'rename': 'ErrorCode', 'type': 'str'},
        'error_message': {'tag': 'xml', 'rename': 'ErrorMessage', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Error'
    }

    def __init__(
        self,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            error_code (str, optional): The metadata table error code.
            error_message (str, optional): The metadata table error message.
        """
        super().__init__(**kwargs)
        self.error_code = error_code
        self.error_message = error_message


class DestinationResult(serde.Model):
    """The container that stores the metadata table destination."""

    _attribute_map = {
        'table_bucket_type': {'tag': 'xml', 'rename': 'TableBucketType', 'type': 'str'},
        'table_bucket_arn': {'tag': 'xml', 'rename': 'TableBucketArn', 'type': 'str'},
        'table_namespace': {'tag': 'xml', 'rename': 'TableNamespace', 'type': 'str'},
    }

    _xml_map = {
        'name': 'DestinationResult'
    }

    def __init__(
        self,
        table_bucket_type: Optional[str] = None,
        table_bucket_arn: Optional[str] = None,
        table_namespace: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_type (str, optional): The destination bucket type. The value is oss.
            table_bucket_arn (str, optional): The ARN of the destination table bucket.
            table_namespace (str, optional): The namespace of the destination table bucket.
        """
        super().__init__(**kwargs)
        self.table_bucket_type = table_bucket_type
        self.table_bucket_arn = table_bucket_arn
        self.table_namespace = table_namespace


class JournalTableConfigurationResult(serde.Model):
    """The container that stores journal metadata table details."""

    _attribute_map = {
        'table_status': {'tag': 'xml', 'rename': 'TableStatus', 'type': 'str'},
        'table_name': {'tag': 'xml', 'rename': 'TableName', 'type': 'str'},
        'table_arn': {'tag': 'xml', 'rename': 'TableArn', 'type': 'str'},
        'record_expiration': {'tag': 'xml', 'rename': 'RecordExpiration', 'type': 'RecordExpiration,xml'},
        'encryption_configuration': {'tag': 'xml', 'rename': 'EncryptionConfiguration', 'type': 'MetadataTableEncryptionConfiguration,xml'},
        'error': {'tag': 'xml', 'rename': 'Error', 'type': 'MetadataTableError,xml'},
    }

    _xml_map = {
        'name': 'JournalTableConfigurationResult'
    }

    _dependency_map = {
        'RecordExpiration': {'new': lambda: RecordExpiration()},
        'MetadataTableEncryptionConfiguration': {'new': lambda: MetadataTableEncryptionConfiguration()},
        'MetadataTableError': {'new': lambda: MetadataTableError()},
    }

    def __init__(
        self,
        table_status: Optional[Union[str, TableStatusType]] = None,
        table_name: Optional[str] = None,
        table_arn: Optional[str] = None,
        record_expiration: Optional[RecordExpiration] = None,
        encryption_configuration: Optional[MetadataTableEncryptionConfiguration] = None,
        error: Optional[MetadataTableError] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_status (str | TableStatusType, optional): The creation state of the journal table.
            table_name (str, optional): The journal table name.
            table_arn (str, optional): The ARN of the journal table.
            record_expiration (RecordExpiration, optional): The journal record expiration settings.
            encryption_configuration (MetadataTableEncryptionConfiguration, optional): The journal table encryption settings.
            error (MetadataTableError, optional): The error returned when table creation fails.
        """
        super().__init__(**kwargs)
        self.table_status = table_status
        self.table_name = table_name
        self.table_arn = table_arn
        self.record_expiration = record_expiration
        self.encryption_configuration = encryption_configuration
        self.error = error


class InventoryTableConfigurationResult(serde.Model):
    """The container that stores inventory metadata table details."""

    _attribute_map = {
        'configuration_state': {'tag': 'xml', 'rename': 'ConfigurationState', 'type': 'str'},
        'table_status': {'tag': 'xml', 'rename': 'TableStatus', 'type': 'str'},
        'table_name': {'tag': 'xml', 'rename': 'TableName', 'type': 'str'},
        'table_arn': {'tag': 'xml', 'rename': 'TableArn', 'type': 'str'},
        'encryption_configuration': {'tag': 'xml', 'rename': 'EncryptionConfiguration', 'type': 'MetadataTableEncryptionConfiguration,xml'},
        'error': {'tag': 'xml', 'rename': 'Error', 'type': 'MetadataTableError,xml'},
    }

    _xml_map = {
        'name': 'InventoryTableConfigurationResult'
    }

    _dependency_map = {
        'MetadataTableEncryptionConfiguration': {'new': lambda: MetadataTableEncryptionConfiguration()},
        'MetadataTableError': {'new': lambda: MetadataTableError()},
    }

    def __init__(
        self,
        configuration_state: Optional[Union[str, ConfigurationStateType]] = None,
        table_status: Optional[Union[str, TableStatusType]] = None,
        table_name: Optional[str] = None,
        table_arn: Optional[str] = None,
        encryption_configuration: Optional[MetadataTableEncryptionConfiguration] = None,
        error: Optional[MetadataTableError] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            configuration_state (str | ConfigurationStateType, optional): Whether the inventory table is enabled.
            table_status (str | TableStatusType, optional): The creation state of the inventory table.
            table_name (str, optional): The inventory table name.
            table_arn (str, optional): The ARN of the inventory table.
            encryption_configuration (MetadataTableEncryptionConfiguration, optional): The inventory table encryption settings.
            error (MetadataTableError, optional): The error returned when table creation fails.
        """
        super().__init__(**kwargs)
        self.configuration_state = configuration_state
        self.table_status = table_status
        self.table_name = table_name
        self.table_arn = table_arn
        self.encryption_configuration = encryption_configuration
        self.error = error


class MetadataConfigurationResult(serde.Model):
    """The container that stores bucket metadata table configuration details."""

    _attribute_map = {
        'destination_result': {'tag': 'xml', 'rename': 'DestinationResult', 'type': 'DestinationResult,xml'},
        'journal_table_configuration_result': {'tag': 'xml', 'rename': 'JournalTableConfigurationResult', 'type': 'JournalTableConfigurationResult,xml'},
        'inventory_table_configuration_result': {'tag': 'xml', 'rename': 'InventoryTableConfigurationResult', 'type': 'InventoryTableConfigurationResult,xml'},
    }

    _xml_map = {
        'name': 'MetadataConfigurationResult'
    }

    _dependency_map = {
        'DestinationResult': {'new': lambda: DestinationResult()},
        'JournalTableConfigurationResult': {'new': lambda: JournalTableConfigurationResult()},
        'InventoryTableConfigurationResult': {'new': lambda: InventoryTableConfigurationResult()},
    }

    def __init__(
        self,
        destination_result: Optional[DestinationResult] = None,
        journal_table_configuration_result: Optional[JournalTableConfigurationResult] = None,
        inventory_table_configuration_result: Optional[InventoryTableConfigurationResult] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            destination_result (DestinationResult, optional): The metadata table destination.
            journal_table_configuration_result (JournalTableConfigurationResult, optional): The journal metadata table details.
            inventory_table_configuration_result (InventoryTableConfigurationResult, optional): The inventory metadata table details.
        """
        super().__init__(**kwargs)
        self.destination_result = destination_result
        self.journal_table_configuration_result = journal_table_configuration_result
        self.inventory_table_configuration_result = inventory_table_configuration_result


class CreateBucketMetadataConfigurationRequest(serde.RequestModel):
    """The request for the CreateBucketMetadataConfiguration operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'metadata_configuration': {'tag': 'input', 'position': 'body', 'rename': 'MetadataConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        metadata_configuration: Optional[MetadataConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            metadata_configuration (MetadataConfiguration, optional): The bucket metadata table configuration.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.metadata_configuration = metadata_configuration


class CreateBucketMetadataConfigurationResult(serde.ResultModel):
    """The result for the CreateBucketMetadataConfiguration operation."""


class GetBucketMetadataConfigurationRequest(serde.RequestModel):
    """The request for the GetBucketMetadataConfiguration operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetBucketMetadataConfigurationResult(serde.ResultModel):
    """The result for the GetBucketMetadataConfiguration operation."""

    _attribute_map = {
        'metadata_configuration_result': {'tag': 'xml', 'rename': 'MetadataConfigurationResult', 'type': 'MetadataConfigurationResult,xml'},
    }

    _xml_map = {
        'name': 'GetBucketMetadataConfigurationResult'
    }

    _dependency_map = {
        'MetadataConfigurationResult': {'new': lambda: MetadataConfigurationResult()},
    }

    def __init__(
        self,
        metadata_configuration_result: Optional[MetadataConfigurationResult] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            metadata_configuration_result (MetadataConfigurationResult, optional): The bucket metadata table configuration details.
        """
        super().__init__(**kwargs)
        self.metadata_configuration_result = metadata_configuration_result


class DeleteBucketMetadataConfigurationRequest(serde.RequestModel):
    """The request for the DeleteBucketMetadataConfiguration operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteBucketMetadataConfigurationResult(serde.ResultModel):
    """The result for the DeleteBucketMetadataConfiguration operation."""


class UpdateBucketMetadataInventoryTableConfigurationRequest(serde.RequestModel):
    """The request for the UpdateBucketMetadataInventoryTableConfiguration operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'inventory_table_configuration': {'tag': 'input', 'position': 'body', 'rename': 'InventoryTableConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        inventory_table_configuration: Optional[InventoryTableConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            inventory_table_configuration (InventoryTableConfiguration, optional): The inventory metadata table settings.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.inventory_table_configuration = inventory_table_configuration


class UpdateBucketMetadataInventoryTableConfigurationResult(serde.ResultModel):
    """The result for the UpdateBucketMetadataInventoryTableConfiguration operation."""


class UpdateBucketMetadataJournalTableConfigurationRequest(serde.RequestModel):
    """The request for the UpdateBucketMetadataJournalTableConfiguration operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'journal_table_configuration': {'tag': 'input', 'position': 'body', 'rename': 'JournalTableConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        journal_table_configuration: Optional[JournalTableConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            journal_table_configuration (JournalTableConfiguration, optional): The journal metadata table settings.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.journal_table_configuration = journal_table_configuration


class UpdateBucketMetadataJournalTableConfigurationResult(serde.ResultModel):
    """The result for the UpdateBucketMetadataJournalTableConfiguration operation."""
