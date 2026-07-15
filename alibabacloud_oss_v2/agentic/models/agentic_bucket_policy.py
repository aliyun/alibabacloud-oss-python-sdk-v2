# pylint: disable=line-too-long
from typing import Optional, Any
from alibabacloud_oss_v2 import serde, BodyType


class PutAgenticBucketPolicyRequest(serde.RequestModel):
    """The request for the PutAgenticBucketPolicy operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'body': {'tag': 'input', 'position': 'body', 'rename': 'nop', 'required': True},
    }

    def __init__(self, bucket: str = None, body: Optional[BodyType] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket
        self.body = body


class PutAgenticBucketPolicyResult(serde.ResultModel):
    """The result for the PutAgenticBucketPolicy operation."""


class GetAgenticBucketPolicyRequest(serde.RequestModel):
    """The request for the GetAgenticBucketPolicy operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class GetAgenticBucketPolicyResult(serde.ResultModel):
    """The result for the GetAgenticBucketPolicy operation."""

    _attribute_map = {
        'body': {'tag': 'output', 'position': 'body', 'type': 'str'},
    }

    def __init__(self, body: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.body = body


class DeleteAgenticBucketPolicyRequest(serde.RequestModel):
    """The request for the DeleteAgenticBucketPolicy operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteAgenticBucketPolicyResult(serde.ResultModel):
    """The result for the DeleteAgenticBucketPolicy operation."""
