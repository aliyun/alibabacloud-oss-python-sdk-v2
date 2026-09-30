import datetime
from typing import Optional, List, Any, Union
from .. import serde


class QuotaConfiguration(serde.Model):
    """
    The container that stores the bucket storage quota configuration.
    """

    _attribute_map = {
        'storage_quota': {'tag': 'xml', 'rename': 'StorageQuota', 'type': 'int'},
        'mode': {'tag': 'xml', 'rename': 'Mode', 'type': 'str'},
        'current_usage': {'tag': 'xml', 'rename': 'CurrentUsage', 'type': 'int'},
    }

    _xml_map = {
        'name': 'QuotaConfiguration'
    }

    def __init__(
        self,
        storage_quota: Optional[int] = None,
        mode: Optional[str] = None,
        current_usage: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            storage_quota (int, optional): The storage capacity limit, in bytes. It must be a positive integer.
            mode (str, optional): The quota mode. Valid values: Strict and Warning. It is case-sensitive.
            current_usage (int, optional): The last measured used capacity of the bucket space, in bytes. It is only returned by the query operation.
        """
        super().__init__(**kwargs)
        self.storage_quota = storage_quota
        self.mode = mode
        self.current_usage = current_usage


class PutBucketStorageQuotaRequest(serde.RequestModel):
    """
    The request for the PutBucketStorageQuota operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'quota_configuration': {'tag': 'input', 'position': 'body', 'rename': 'QuotaConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        quota_configuration: Optional[QuotaConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            quota_configuration (QuotaConfiguration, optional): The container that stores the storage quota configuration.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.quota_configuration = quota_configuration


class PutBucketStorageQuotaResult(serde.ResultModel):
    """
    The result for the PutBucketStorageQuota operation.
    """


class GetBucketStorageQuotaRequest(serde.RequestModel):
    """
    The request for the GetBucketStorageQuota operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetBucketStorageQuotaResult(serde.ResultModel):
    """
    The result for the GetBucketStorageQuota operation.
    """

    _attribute_map = {
        'quota_configuration': {'tag': 'output', 'position': 'body', 'rename': 'QuotaConfiguration', 'type': 'QuotaConfiguration,xml'},
    }

    _dependency_map = {
        'QuotaConfiguration': {'new': lambda: QuotaConfiguration()},
    }

    def __init__(
        self,
        quota_configuration: Optional[QuotaConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            quota_configuration (QuotaConfiguration, optional): The container that stores the storage quota configuration.
        """
        super().__init__(**kwargs)
        self.quota_configuration = quota_configuration


class DeleteBucketStorageQuotaRequest(serde.RequestModel):
    """
    The request for the DeleteBucketStorageQuota operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteBucketStorageQuotaResult(serde.ResultModel):
    """
    The result for the DeleteBucketStorageQuota operation.
    """
