# pylint: disable=line-too-long
from typing import Optional, Any
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models.bucket_basic import VersioningConfiguration


class PutAgenticBucketVersioningRequest(serde.RequestModel):
    """The request for the PutAgenticBucketVersioning operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'versioning_configuration': {'tag': 'input', 'position': 'body', 'rename': 'VersioningConfiguration', 'type': 'xml'},
    }

    def __init__(self, bucket: str = None, versioning_configuration: Optional[VersioningConfiguration] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket
        self.versioning_configuration = versioning_configuration


class PutAgenticBucketVersioningResult(serde.ResultModel):
    """The result for the PutAgenticBucketVersioning operation."""


class GetAgenticBucketVersioningRequest(serde.RequestModel):
    """The request for the GetAgenticBucketVersioning operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class GetAgenticBucketVersioningResult(serde.ResultModel):
    """The result for the GetAgenticBucketVersioning operation."""

    _attribute_map = {
        'version_status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
    }
    _xml_map = {'name': 'VersioningConfiguration'}

    def __init__(self, version_status: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.version_status = version_status
