# pylint: disable=line-too-long
from typing import Optional, Any
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models.bucket_encryption import ServerSideEncryptionRule


class PutAgenticBucketEncryptionRequest(serde.RequestModel):
    """The request for the PutAgenticBucketEncryption operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'server_side_encryption_rule': {'tag': 'input', 'position': 'body', 'rename': 'ServerSideEncryptionRule', 'type': 'xml'},
    }

    def __init__(self, bucket: str = None, server_side_encryption_rule: Optional[ServerSideEncryptionRule] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket
        self.server_side_encryption_rule = server_side_encryption_rule


class PutAgenticBucketEncryptionResult(serde.ResultModel):
    """The result for the PutAgenticBucketEncryption operation."""


class GetAgenticBucketEncryptionRequest(serde.RequestModel):
    """The request for the GetAgenticBucketEncryption operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class GetAgenticBucketEncryptionResult(serde.ResultModel):
    """The result for the GetAgenticBucketEncryption operation."""

    _attribute_map = {
        'server_side_encryption_rule': {'tag': 'output', 'position': 'body', 'rename': 'ServerSideEncryptionRule', 'type': 'ServerSideEncryptionRule,xml'},
    }
    _dependency_map = {
        'ServerSideEncryptionRule': {'new': lambda: ServerSideEncryptionRule()},
    }

    def __init__(self, server_side_encryption_rule: Optional[ServerSideEncryptionRule] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.server_side_encryption_rule = server_side_encryption_rule


class DeleteAgenticBucketEncryptionRequest(serde.RequestModel):
    """The request for the DeleteAgenticBucketEncryption operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteAgenticBucketEncryptionResult(serde.ResultModel):
    """The result for the DeleteAgenticBucketEncryption operation."""
