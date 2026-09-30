# pylint: disable=line-too-long
from typing import Optional, Any
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models.bucket_storage_quota import QuotaConfiguration


class PutAgenticBucketStorageQuotaRequest(serde.RequestModel):
    """The request for the PutAgenticBucketStorageQuota operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'quota_configuration': {'tag': 'input', 'position': 'body', 'rename': 'QuotaConfiguration', 'type': 'xml'},
    }

    def __init__(self, bucket: str = None, quota_configuration: Optional[QuotaConfiguration] = None, **kwargs: Any) -> None:
        """
        Args:
            bucket (str, required): The prefix of the Agent Bucket name.
            quota_configuration (QuotaConfiguration, optional): The default storage quota configuration applied to newly created bucket spaces.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.quota_configuration = quota_configuration


class PutAgenticBucketStorageQuotaResult(serde.ResultModel):
    """The result for the PutAgenticBucketStorageQuota operation."""


class GetAgenticBucketStorageQuotaRequest(serde.RequestModel):
    """The request for the GetAgenticBucketStorageQuota operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        """
        Args:
            bucket (str, required): The prefix of the Agent Bucket name.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetAgenticBucketStorageQuotaResult(serde.ResultModel):
    """The result for the GetAgenticBucketStorageQuota operation.

    Note: unlike the bucket space level result, the Agent Bucket level query does not
    return CurrentUsage because an Agent Bucket itself stores no objects.
    """

    _attribute_map = {
        'quota_configuration': {'tag': 'output', 'position': 'body', 'rename': 'QuotaConfiguration', 'type': 'QuotaConfiguration,xml'},
    }
    _dependency_map = {
        'QuotaConfiguration': {'new': lambda: QuotaConfiguration()},
    }

    def __init__(self, quota_configuration: Optional[QuotaConfiguration] = None, **kwargs: Any) -> None:
        """
        Args:
            quota_configuration (QuotaConfiguration, optional): The default storage quota configuration of the Agent Bucket.
        """
        super().__init__(**kwargs)
        self.quota_configuration = quota_configuration


class DeleteAgenticBucketStorageQuotaRequest(serde.RequestModel):
    """The request for the DeleteAgenticBucketStorageQuota operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        """
        Args:
            bucket (str, required): The prefix of the Agent Bucket name.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteAgenticBucketStorageQuotaResult(serde.ResultModel):
    """The result for the DeleteAgenticBucketStorageQuota operation."""
