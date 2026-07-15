# pylint: disable=line-too-long
from typing import Optional, Any
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models.bucket_basic import Owner


class PutAgenticBucketAclRequest(serde.RequestModel):
    """The request for the PutAgenticBucketAcl operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'acl': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-acl', 'type': 'str'},
    }

    def __init__(self, bucket: str = None, acl: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket
        self.acl = acl


class PutAgenticBucketAclResult(serde.ResultModel):
    """The result for the PutAgenticBucketAcl operation."""


class GetAgenticBucketAclRequest(serde.RequestModel):
    """The request for the GetAgenticBucketAcl operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class GetAgenticBucketAclResult(serde.ResultModel):
    """The result for the GetAgenticBucketAcl operation."""

    _attribute_map = {
        'owner': {'tag': 'xml', 'rename': 'Owner', 'type': 'Owner'},
        'acl': {'tag': 'xml', 'rename': 'AccessControlList/Grant', 'type': 'str'},
    }
    _dependency_map = {
        'Owner': {'new': lambda: Owner()},
    }
    _xml_map = {'name': 'AccessControlPolicy'}

    def __init__(self, owner: Optional[Owner] = None, acl: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.owner = owner
        self.acl = acl
