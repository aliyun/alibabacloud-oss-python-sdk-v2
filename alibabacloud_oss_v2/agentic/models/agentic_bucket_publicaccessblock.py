# pylint: disable=line-too-long
from typing import Optional, Any
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models.bucket_public_access_block import PublicAccessBlockConfiguration


class PutAgenticBucketPublicAccessBlockRequest(serde.RequestModel):
    """The request for the PutAgenticBucketPublicAccessBlock operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'public_access_block_configuration': {'tag': 'input', 'position': 'body', 'rename': 'PublicAccessBlockConfiguration', 'type': 'xml'},
    }

    def __init__(self, bucket: str = None, public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket
        self.public_access_block_configuration = public_access_block_configuration


class PutAgenticBucketPublicAccessBlockResult(serde.ResultModel):
    """The result for the PutAgenticBucketPublicAccessBlock operation."""


class GetAgenticBucketPublicAccessBlockRequest(serde.RequestModel):
    """The request for the GetAgenticBucketPublicAccessBlock operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class GetAgenticBucketPublicAccessBlockResult(serde.ResultModel):
    """The result for the GetAgenticBucketPublicAccessBlock operation."""

    _attribute_map = {
        'public_access_block_configuration': {'tag': 'output', 'position': 'body', 'rename': 'PublicAccessBlockConfiguration', 'type': 'PublicAccessBlockConfiguration,xml'},
    }
    _dependency_map = {
        'PublicAccessBlockConfiguration': {'new': lambda: PublicAccessBlockConfiguration()},
    }

    def __init__(self, public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.public_access_block_configuration = public_access_block_configuration


class DeleteAgenticBucketPublicAccessBlockRequest(serde.RequestModel):
    """The request for the DeleteAgenticBucketPublicAccessBlock operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteAgenticBucketPublicAccessBlockResult(serde.ResultModel):
    """The result for the DeleteAgenticBucketPublicAccessBlock operation."""
