# pylint: disable=line-too-long
from typing import Optional, List, Any
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models.bucket_encryption import ServerSideEncryptionRule
from alibabacloud_oss_v2.models.bucket_basic import Owner


class CreateAgenticBucketConfiguration(serde.Model):
    """The configuration for the CreateAgenticBucket operation."""

    _attribute_map = {
        'storage_class': {'tag': 'xml', 'rename': 'StorageClass', 'type': 'str'},
        'data_redundancy_type': {'tag': 'xml', 'rename': 'DataRedundancyType', 'type': 'str'},
    }
    _xml_map = {
        'name': 'CreateAgenticBucketConfiguration'
    }

    def __init__(
        self,
        storage_class: Optional[str] = None,
        data_redundancy_type: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.storage_class = storage_class
        self.data_redundancy_type = data_redundancy_type


class CreateAgenticBucketRequest(serde.RequestModel):
    """The request for the CreateAgenticBucket operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'create_agentic_bucket_configuration': {'tag': 'input', 'position': 'body', 'rename': 'CreateAgenticBucketConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        create_agentic_bucket_configuration: Optional[CreateAgenticBucketConfiguration] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket
        self.create_agentic_bucket_configuration = create_agentic_bucket_configuration


class CreateAgenticBucketResult(serde.ResultModel):
    """The result for the CreateAgenticBucket operation."""


class DeleteAgenticBucketRequest(serde.RequestModel):
    """The request for the DeleteAgenticBucket operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteAgenticBucketResult(serde.ResultModel):
    """The result for the DeleteAgenticBucket operation."""


class GetAgenticBucketRequest(serde.RequestModel):
    """The request for the GetAgenticBucket operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(self, bucket: str = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bucket = bucket


class AgenticBucketInfo(serde.Model):
    """The information about an AgenticBucket."""

    _attribute_map = {
        'name': {'tag': 'xml', 'rename': 'Name', 'type': 'str'},
        'owner': {'tag': 'xml', 'rename': 'Owner', 'type': 'str'},
        'region': {'tag': 'xml', 'rename': 'Region', 'type': 'str'},
        'storage_class': {'tag': 'xml', 'rename': 'StorageClass', 'type': 'str'},
        'data_redundancy_type': {'tag': 'xml', 'rename': 'DataRedundancyType', 'type': 'str'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'bucket_resource_type': {'tag': 'xml', 'rename': 'BucketResourceType', 'type': 'str'},
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'acl': {'tag': 'xml', 'rename': 'ACL', 'type': 'str'},
        'public_access_block': {'tag': 'xml', 'rename': 'PublicAccessBlock', 'type': 'str'},
        'server_side_encryption_rule': {'tag': 'xml', 'rename': 'ServerSideEncryptionRule', 'type': 'ServerSideEncryptionRule'},
        'versioning': {'tag': 'xml', 'rename': 'Versioning', 'type': 'str'},
        'bucket_policy': {'tag': 'xml', 'rename': 'BucketPolicy', 'type': 'str'},
    }
    _xml_map = {'name': 'AgenticBucketInfo'}
    _dependency_map = {
        'ServerSideEncryptionRule': {'new': lambda: ServerSideEncryptionRule()},
    }

    def __init__(
        self,
        name: Optional[str] = None,
        owner: Optional[str] = None,
        region: Optional[str] = None,
        storage_class: Optional[str] = None,
        data_redundancy_type: Optional[str] = None,
        status: Optional[str] = None,
        bucket_resource_type: Optional[str] = None,
        create_time: Optional[str] = None,
        acl: Optional[str] = None,
        public_access_block: Optional[str] = None,
        server_side_encryption_rule: Optional[ServerSideEncryptionRule] = None,
        versioning: Optional[str] = None,
        bucket_policy: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.owner = owner
        self.region = region
        self.storage_class = storage_class
        self.data_redundancy_type = data_redundancy_type
        self.status = status
        self.bucket_resource_type = bucket_resource_type
        self.create_time = create_time
        self.acl = acl
        self.public_access_block = public_access_block
        self.server_side_encryption_rule = server_side_encryption_rule
        self.versioning = versioning
        self.bucket_policy = bucket_policy


class GetAgenticBucketResult(serde.ResultModel):
    """The result for the GetAgenticBucket operation."""

    _attribute_map = {
        'agentic_bucket_info': {'tag': 'output', 'position': 'body', 'rename': 'AgenticBucketInfo', 'type': 'AgenticBucketInfo,xml'},
    }
    _dependency_map = {
        'AgenticBucketInfo': {'new': lambda: AgenticBucketInfo()},
    }

    def __init__(self, agentic_bucket_info: Optional[AgenticBucketInfo] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.agentic_bucket_info = agentic_bucket_info


class ListAgenticBucketsRequest(serde.RequestModel):
    """The request for the ListAgenticBuckets operation (region-level host, no bucket)."""

    _attribute_map = {
        'continuation_token': {'tag': 'input', 'position': 'query', 'rename': 'continuation-token', 'type': 'str'},
        'max_keys': {'tag': 'input', 'position': 'query', 'rename': 'max-keys', 'type': 'int'},
    }

    def __init__(
        self,
        continuation_token: Optional[str] = None,
        max_keys: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.continuation_token = continuation_token
        self.max_keys = max_keys


class AgenticBucketSummary(serde.Model):
    """The summary of an AgenticBucket in ListAgenticBuckets."""

    _attribute_map = {
        'name': {'tag': 'xml', 'rename': 'Name', 'type': 'str'},
        'storage_class': {'tag': 'xml', 'rename': 'StorageClass', 'type': 'str'},
        'data_redundancy_type': {'tag': 'xml', 'rename': 'DataRedundancyType', 'type': 'str'},
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
    }
    _xml_map = {'name': 'AgenticBucket'}

    def __init__(self, name=None, storage_class=None, data_redundancy_type=None, create_time=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.storage_class = storage_class
        self.data_redundancy_type = data_redundancy_type
        self.create_time = create_time


class ListAgenticBucketsResult(serde.ResultModel):
    """The result for the ListAgenticBuckets operation."""

    _attribute_map = {
        'region': {'tag': 'xml', 'rename': 'Region', 'type': 'str'},
        'owner': {'tag': 'xml', 'rename': 'Owner', 'type': 'str'},
        'continuation_token': {'tag': 'xml', 'rename': 'ContinuationToken', 'type': 'str'},
        'next_continuation_token': {'tag': 'xml', 'rename': 'NextContinuationToken', 'type': 'str'},
        'is_truncated': {'tag': 'xml', 'rename': 'IsTruncated', 'type': 'bool'},
        'agentic_buckets': {'tag': 'xml', 'rename': 'AgenticBuckets/AgenticBucket', 'type': '[AgenticBucketSummary]'},
    }
    _dependency_map = {
        'AgenticBucketSummary': {'new': lambda: AgenticBucketSummary()},
    }
    _xml_map = {'name': 'ListAgenticBucketsResult'}

    def __init__(self, region=None, owner=None, continuation_token=None,
                 next_continuation_token=None, is_truncated=None, agentic_buckets=None, **kwargs):
        super().__init__(**kwargs)
        self.region = region
        self.owner = owner
        self.continuation_token = continuation_token
        self.next_continuation_token = next_continuation_token
        self.is_truncated = is_truncated
        self.agentic_buckets = agentic_buckets


class AgenticBucketStatus(serde.Model):
    """The status configuration of an AgenticBucket."""

    _attribute_map = {
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
    }
    _xml_map = {'name': 'AgenticBucketStatus'}

    def __init__(self, status: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.status = status


class PutAgenticBucketStatusRequest(serde.RequestModel):
    """The request for the PutAgenticBucketStatus operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'agentic_bucket_status': {'tag': 'input', 'position': 'body', 'rename': 'AgenticBucketStatus', 'type': 'xml'},
    }

    def __init__(self, bucket=None, agentic_bucket_status=None, **kwargs):
        super().__init__(**kwargs)
        self.bucket = bucket
        self.agentic_bucket_status = agentic_bucket_status


class PutAgenticBucketStatusResult(serde.ResultModel):
    """The result for the PutAgenticBucketStatus operation."""


class ListBucketSpacesRequest(serde.RequestModel):
    """The request for the ListBucketSpaces operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'prefix': {'tag': 'input', 'position': 'query', 'rename': 'prefix', 'type': 'str'},
        'continuation_token': {'tag': 'input', 'position': 'query', 'rename': 'continuation-token', 'type': 'str'},
        'max_keys': {'tag': 'input', 'position': 'query', 'rename': 'max-keys', 'type': 'int'},
    }

    def __init__(self, bucket=None, prefix=None, continuation_token=None, max_keys=None, **kwargs):
        super().__init__(**kwargs)
        self.bucket = bucket
        self.prefix = prefix
        self.continuation_token = continuation_token
        self.max_keys = max_keys


class BucketSpaceSummary(serde.Model):
    """The summary of a BucketSpace in ListBucketSpaces."""

    _attribute_map = {
        'name': {'tag': 'xml', 'rename': 'Name', 'type': 'str'},
        'location': {'tag': 'xml', 'rename': 'Location', 'type': 'str'},
        'creation_date': {'tag': 'xml', 'rename': 'CreationDate', 'type': 'str'},
        'storage_class': {'tag': 'xml', 'rename': 'StorageClass', 'type': 'str'},
    }
    _xml_map = {'name': 'BucketSpace'}

    def __init__(self, name=None, location=None, creation_date=None, storage_class=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.location = location
        self.creation_date = creation_date
        self.storage_class = storage_class


class ListBucketSpacesResult(serde.ResultModel):
    """The result for the ListBucketSpaces operation."""

    _attribute_map = {
        'owner': {'tag': 'xml', 'rename': 'Owner', 'type': 'Owner'},
        'bucket_spaces': {'tag': 'xml', 'rename': 'BucketSpaces/BucketSpace', 'type': '[BucketSpaceSummary]'},
        'prefix': {'tag': 'xml', 'rename': 'Prefix', 'type': 'str'},
        'max_keys': {'tag': 'xml', 'rename': 'MaxKeys', 'type': 'int'},
        'continuation_token': {'tag': 'xml', 'rename': 'ContinuationToken', 'type': 'str'},
        'next_continuation_token': {'tag': 'xml', 'rename': 'NextContinuationToken', 'type': 'str'},
        'is_truncated': {'tag': 'xml', 'rename': 'IsTruncated', 'type': 'bool'},
    }
    _dependency_map = {
        'Owner': {'new': lambda: Owner()},
        'BucketSpaceSummary': {'new': lambda: BucketSpaceSummary()},
    }
    _xml_map = {'name': 'ListBucketSpacesResult'}

    def __init__(self, owner=None, bucket_spaces=None, prefix=None, max_keys=None,
                 continuation_token=None, next_continuation_token=None, is_truncated=None, **kwargs):
        super().__init__(**kwargs)
        self.owner = owner
        self.bucket_spaces = bucket_spaces
        self.prefix = prefix
        self.max_keys = max_keys
        self.continuation_token = continuation_token
        self.next_continuation_token = next_continuation_token
        self.is_truncated = is_truncated
