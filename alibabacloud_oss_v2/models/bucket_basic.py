"""Models for bucket basic operation APIs"""
# pylint: disable=too-few-public-methods, too-many-instance-attributes, unnecessary-lambda
# pylint: disable=super-init-not-called, too-many-lines, line-too-long, too-many-arguments

import datetime
from typing import Optional, List, Any
from .. import serde


class CreateBucketConfiguration(serde.Model):
    """The configuration information for the bucket."""

    def __init__(
        self,
        storage_class: Optional[str] = None,
        data_redundancy_type: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            storage_class (str, optional): The storage class of the bucket.
            data_redundancy_type (str, optional): The redundancy type of the bucket.
        """
        super().__init__(**kwargs)
        self.storage_class = storage_class
        self.data_redundancy_type = data_redundancy_type

    _attribute_map = {
        "storage_class": {"tag": "xml", "rename": "StorageClass"},
        "data_redundancy_type": {"tag": "xml", "rename": "DataRedundancyType"},
    }
    _xml_map = {
        "name": "CreateBucketConfiguration"
    }


class PutBucketRequest(serde.RequestModel):
    """The request for the PutBucket operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "acl": {"tag": "input", "position": "header", "rename": "x-oss-acl"},
        "resource_group_id": {"tag": "input", "position": "header", "rename": "x-oss-resource-group-id"},
        "create_bucket_configuration": {"tag": "input", "position": "body", "rename": "CreateBucketConfiguration", "type": "xml"},
        "bucket_tagging": {"tag": "input", "position": "header", "rename": "x-oss-bucket-tagging"},
    }

    def __init__(
        self,
        bucket: str = None,
        acl: Optional[str] = None,
        resource_group_id: Optional[str] = None,
        create_bucket_configuration: Optional["CreateBucketConfiguration"] = None,
        bucket_tagging: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket to create.
            acl (str, optional): The access control list (ACL) of the bucket.
            resource_group_id (str, optional): The ID of the resource group.
            create_bucket_configuration (CreateBucketConfiguration, optional): 
                The configuration information for the bucket.
            bucket_tagging (str, optional): The tagging information for the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.acl = acl
        self.resource_group_id = resource_group_id
        self.create_bucket_configuration = create_bucket_configuration
        self.bucket_tagging = bucket_tagging


class PutBucketResult(serde.ResultModel):
    """The result for the PutBucket operation."""


class DeleteBucketRequest(serde.RequestModel):
    """The request for the DeleteBucket operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
    }

    def __init__(
        self,
        bucket: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket to create.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteBucketResult(serde.ResultModel):
    """The result for the DeleteBucket operation."""


class Owner(serde.Model):
    """Stores information about the bucket owner."""

    _attribute_map = {
        "id": {"tag": "xml", "rename": "ID"},
        "display_name": {"tag": "xml", "rename": "DisplayName"},
    }

    _xml_map = {
        "name": "Owner"
    }

    def __init__(
        self,
        id: Optional[str] = None,  # pylint: disable=redefined-builtin
        display_name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            id (str, optional): The ID of the bucket owner.
            display_name (str, optional): The name of the object owner..
        """
        super().__init__(**kwargs)
        self.id = id
        self.display_name = display_name


class ObjectProperties(serde.Model):
    """Stores the metadata of the object."""

    _attribute_map = {
        "key": {"tag": "xml", "rename": "Key"},
        "object_type": {"tag": "xml", "rename": "Type"},
        "size": {"tag": "xml", "rename": "Size", "type": "int"},
        "etag": {"tag": "xml", "rename": "ETag"},
        "last_modified": {"tag": "xml", "rename": "LastModified", "type": "datetime"},
        "storage_class": {"tag": "xml", "rename": "StorageClass"},
        "owner": {"tag": "xml", "rename": "Owner", "type": "Owner"},
        "restore_info": {"tag": "xml", "rename": "RestoreInfo"},
        "transition_time": {"tag": "xml", "rename": "TransitionTime"},
    }

    _dependency_map = {
        "Owner": {"new": lambda: Owner()},
    }

    _xml_map = {
        "name": "ObjectProperties"
    }

    def __init__(
        self,
        key: Optional[str] = None,
        object_type: Optional[str] = None,
        size: Optional[int] = None,
        etag: Optional[str] = None,
        last_modified: Optional[datetime.datetime] = None,
        storage_class: Optional[str] = None,
        owner: Optional[Owner] = None,
        restore_info: Optional[str] = None,
        transition_time: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The name of the object.
            object_type (str, optional): The type of the object.
                Valid values: Normal, Multipart and Appendable
            size (int, optional): The size of the returned object. Unit: bytes.
            etag (str, optional): The entity tag (ETag). An ETag is created when an object is created to 
                identify the content of the object.
            last_modified (datetime, optional): The time when the returned objects were last modified.
            storage_class (str, optional): The storage class of the object.
            owner (str, optional): The container that stores information about the bucket owner.
            restore_info (Owner, optional): The restoration status of the object.
            transition_time (str): The time when the storage class of the object is converted to Cold Archive or Deep Cold Archive based on lifecycle rules.
        """
        super().__init__(**kwargs)
        self.key = key
        self.object_type = object_type
        self.size = size
        self.etag = etag
        self.last_modified = last_modified
        self.storage_class = storage_class
        self.owner = owner
        self.restore_info = restore_info
        self.transition_time = transition_time


class CommonPrefix(serde.Model):
    """
        If the Delimiter parameter is specified in the request, 
        the response contains the CommonPrefixes parameter. 
        The objects whose names contain the same string from the prefix 
        to the next occurrence of the delimiter are grouped as 
        a single result element in the CommonPrefixes parameter.
    """

    _attribute_map = {
        "prefix": {"tag": "xml", "rename": "Prefix"},
    }

    _xml_map = {
        "name": "CommonPrefix"
    }

    def __init__(
        self,
        prefix: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            prefix (str, optional): The prefix contained in the returned object names.
        """
        super().__init__(**kwargs)
        self.prefix = prefix


class ListObjectsRequest(serde.RequestModel):
    """The request for the ListObjects operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "delimiter": {"tag": "input", "position": "query", "rename": "delimiter"},
        "encoding_type": {"tag": "input", "position": "query", "rename": "encoding-type"},
        "marker": {"tag": "input", "position": "query", "rename": "marker"},
        "max_keys": {"tag": "input", "position": "query", "rename": "max-keys", "type": "int"},
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        delimiter: Optional[str] = None,
        encoding_type: Optional[str] = None,
        marker: Optional[str] = None,
        max_keys: Optional[int] = None,
        prefix: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket to create.
            delimiter (str, optional): The character that is used to group objects by name. 
                If you specify the delimiter parameter in the request, the response contains 
                the CommonPrefixes parameter. The objects whose names contain the same string
                from the prefix to the next occurrence of the delimiter are grouped 
                as a single result element in CommonPrefixes.
            encoding_type (str, optional): The encoding type of the content in the response. Valid value: url
            marker (str, optional): The name of the object after which the ListObjects (GetBucket) operation starts.
                If this parameter is specified, objects whose names are alphabetically 
                greater than the marker value are returned.
            max_keys (int, optional): The maximum number of objects that you want to return.
                If the list operation cannot be complete at a time, because the max-keys parameter is specified,
                the NextMarker element is included in the response as the marker for the next list operation.
            prefix (str, optional): The prefix that the names of the returned objects must contain.
            request_payer (str, optional): To indicate that the requester is aware that the request 
                and data download will incur costs
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.delimiter = delimiter
        self.encoding_type = encoding_type
        self.marker = marker
        self.max_keys = max_keys
        self.prefix = prefix
        self.request_payer = request_payer


class ListObjectsResult(serde.ResultModel):
    """The result for the ListObjects operation."""

    _attribute_map = {
        "name": {"tag": "xml", "rename": "Name"},
        "prefix": {"tag": "xml", "rename": "Prefix"},
        "marker": {"tag": "xml", "rename": "Marker"},
        "max_keys": {"tag": "xml", "rename": "MaxKeys", "type": "int"},
        "delimiter": {"tag": "xml", "rename": "Delimiter"},
        "is_truncated": {"tag": "xml", "rename": "IsTruncated", "type": "bool"},
        "next_marker": {"tag": "xml", "rename": "NextMarker"},
        "encoding_type": {"tag": "xml", "rename": "EncodingType"},
        "contents": {"tag": "xml", "rename": "Contents", "type": "[ObjectProperties]"},
        "common_prefixes": {"tag": "xml", "rename": "CommonPrefixes", "type": "[CommonPrefix]"},
    }

    _dependency_map = {
        "ObjectProperties": {"new": lambda: ObjectProperties()},
        "CommonPrefix": {"new": lambda: CommonPrefix()},
    }

    def __init__(
        self,
        name: Optional[str] = None,
        prefix: Optional[str] = None,
        marker: Optional[str] = None,
        max_keys: Optional[int] = None,
        delimiter: Optional[str] = None,
        is_truncated: Optional[bool] = None,
        next_marker: Optional[str] = None,
        encoding_type: Optional[str] = None,
        contents: Optional[List[ObjectProperties]] = None,
        common_prefixes: Optional[List[CommonPrefix]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the bucket.
            prefix (str, optional): The prefix contained in the returned object names.
            marker (str, optional): The name of the object after which the list operation begins.
            max_keys (int, optional): The maximum number of returned objects in the response.
            delimiter (str, optional): The character that is used to group objects by name.
            is_truncated (bool, optional): Indicates whether the returned results are truncated.
                true indicates that not all results are returned this time.
                false indicates that all results are returned this time.
            next_marker (str, optional): The position from which the next list operation starts.
            encoding_type (str, optional): The encoding type of the content in the response.
            contents ([ObjectProperties], optional): The container that stores the metadata of the returned objects.
            common_prefixes ([CommonPrefix], optional): If the Delimiter parameter is specified in the request, 
                the response contains the CommonPrefixes element.
        """
        super().__init__(**kwargs)
        self.name = name
        self.prefix = prefix
        self.marker = marker
        self.max_keys = max_keys
        self.delimiter = delimiter
        self.is_truncated = is_truncated
        self.next_marker = next_marker
        self.encoding_type = encoding_type
        self.contents = contents
        self.common_prefixes = common_prefixes


class PutBucketAclRequest(serde.RequestModel):
    """The request for the PutBucketAcl operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "acl": {"tag": "input", "position": "header", "rename": "x-oss-acl"},
    }

    def __init__(
        self,
        bucket: str = None,
        acl: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            acl (str, optional): The access control list (ACL) of the object.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.acl = acl


class PutBucketAclResult(serde.ResultModel):
    """The result for the PutBucketAcl operation."""


class GetBucketAclRequest(serde.RequestModel):
    """The request for the GetBucketAcl operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
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

class AccessControlList(serde.Model):
    """Store ACL information."""

    _attribute_map = {
        "acl": {"tag": "xml", "rename": "Grant"},
    }

    _xml_map = {
        "name": "AccessControlList"
    }

    def __init__(
        self,
        acl: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            acl (str, optional): The access control list (ACL) of the object.
        """
        super().__init__(**kwargs)
        self.acl = acl


class GetBucketAclResult(serde.ResultModel):
    """The result for the GetBucketAcl operation."""

    _attribute_map = {
        "owner": {"tag": "xml", "rename": "Owner", "type": "Owner"},
        "acl": {"tag": "xml", "rename": "AccessControlList/Grant"},
    }

    _dependency_map = {
        "Owner": {"new": lambda: Owner()},
    }

    _xml_map = {
        "name": "AccessControlPolicy"
    }

    def __init__(
        self,
        owner: Optional[Owner] = None,
        acl: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            owner (str, optional): The container that stores information about the bucket owner.
            acl (str, optional): The access control list (ACL) of the object.
        """
        super().__init__(**kwargs)
        self.owner = owner
        self.acl = acl


class ListObjectsV2Request(serde.RequestModel):
    """The request for the ListObjectsV2 operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "delimiter": {"tag": "input", "position": "query", "rename": "delimiter"},
        "start_after": {"tag": "input", "position": "query", "rename": "start-after"},
        "encoding_type": {"tag": "input", "position": "query", "rename": "encoding-type"},
        "continuation_token": {"tag": "input", "position": "query", "rename": "continuation-token"},
        "max_keys": {"tag": "input", "position": "query", "rename": "max-keys", "type": "int"},
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
        "fetch_owner": {"tag": "input", "position": "query", "rename": "fetch-owner", "type": "bool"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        delimiter: Optional[str] = None,
        start_after: Optional[str] = None,
        encoding_type: Optional[str] = None,
        continuation_token: Optional[str] = None,
        max_keys: Optional[int] = None,
        prefix: Optional[str] = None,
        fetch_owner: Optional[bool] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            delimiter (str, optional): The character that is used to group objects by name.
                If you specify the delimiter parameter in the request, the response contains
                the CommonPrefixes parameter. The objects whose names contain the same string
                from the prefix to the next occurrence of the delimiter are grouped
                as a single result element in CommonPrefixes.
            start_after (str, optional): Set to return objects in alphabetical order starting from start after.
            encoding_type (str, optional): The encoding type of the content in the response. Valid value: url
            continuation_token (str, optional): The specified List operation needs to start from this token.
                You can obtain this token from the NextContinuationToken in the ListObjectiesV2 (GetBucketV2) result.
            max_keys (int, optional): The maximum number of objects that you want to return.
                If the list operation cannot be complete at a time, because the max-keys parameter is specified,
                the NextMarker element is included in the response as the marker for the next list operation.
            prefix (str, optional): The prefix that the names of the returned objects must contain.
            fetch_owner (str, optional): Specify whether to include owner information in the return result.
                Legitimate values: true, false
            request_payer (str, optional): To indicate that the requester is aware that the request
                and data download will incur costs
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.delimiter = delimiter
        self.start_after = start_after
        self.encoding_type = encoding_type
        self.continuation_token = continuation_token
        self.max_keys = max_keys
        self.prefix = prefix
        self.fetch_owner = fetch_owner
        self.request_payer = request_payer


class ListObjectsV2Result(serde.ResultModel):
    """The result for the ListObjectsV2 operation."""

    _attribute_map = {
        "name": {"tag": "xml", "rename": "Name"},
        "prefix": {"tag": "xml", "rename": "Prefix"},
        "continuation_token": {"tag": "xml", "rename": "ContinuationToken"},
        "max_keys": {"tag": "xml", "rename": "MaxKeys", "type": "int"},
        "delimiter": {"tag": "xml", "rename": "Delimiter"},
        "is_truncated": {"tag": "xml", "rename": "IsTruncated", "type": "bool"},
        "next_continuation_token": {"tag": "xml", "rename": "NextContinuationToken"},
        "encoding_type": {"tag": "xml", "rename": "EncodingType"},
        "contents": {"tag": "xml", "rename": "Contents", "type": "[ObjectProperties]"},
        "common_prefixes": {"tag": "xml", "rename": "CommonPrefixes", "type": "[CommonPrefix]"},
        "start_after": {"tag": "xml", "rename": "StartAfter"},
        "key_count": {"tag": "xml", "rename": "KeyCount", "type": "int"},
    }

    _dependency_map = {
        "ObjectProperties": {"new": lambda: ObjectProperties()},
        "CommonPrefix": {"new": lambda: CommonPrefix()},
    }

    def __init__(
        self,
        name: Optional[str] = None,
        prefix: Optional[str] = None,
        continuation_token: Optional[str] = None,
        max_keys: Optional[int] = None,
        delimiter: Optional[str] = None,
        is_truncated: Optional[bool] = None,
        next_continuation_token: Optional[str] = None,
        encoding_type: Optional[str] = None,
        contents: Optional[List[ObjectProperties]] = None,
        common_prefixes: Optional[List[CommonPrefix]] = None,
        start_after: Optional[str] = None,
        key_count: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the bucket.
            prefix (str, optional): The prefix contained in the returned object names.
            continuation_token (str, optional): The name of the object after which the list operation begins.
            max_keys (int, optional): The maximum number of returned objects in the response.
            delimiter (str, optional): The character that is used to group objects by name.
            is_truncated (bool, optional): Indicates whether the returned results are truncated.
                true indicates that not all results are returned this time.
                false indicates that all results are returned this time.
            next_continuation_token (str, optional): The position from which the next list operation starts.
            encoding_type (str, optional): The encoding type of the content in the response.
            contents ([ObjectProperties], optional): The container that stores the metadata of the returned objects.
            common_prefixes ([CommonPrefix], optional): If the Delimiter parameter is specified in the request,
                the response contains the CommonPrefixes element.
            start_after (str, optional): If the StartAfter parameter is specified in the request,
                the StartAfter element will be included in the returned response.
            key_count (int, optional): The number of keys returned in this request. If a delimiter is specified,
                KeyCount is the sum of the elements of Key and Commonprefixes.
        """
        super().__init__(**kwargs)
        self.name = name
        self.prefix = prefix
        self.continuation_token = continuation_token
        self.max_keys = max_keys
        self.delimiter = delimiter
        self.is_truncated = is_truncated
        self.next_continuation_token = next_continuation_token
        self.encoding_type = encoding_type
        self.contents = contents
        self.common_prefixes = common_prefixes
        self.start_after = start_after
        self.key_count = key_count


class GetBucketStatRequest(serde.RequestModel):
    """The request for the GetBucketStat operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
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


class GetBucketStatResult(serde.ResultModel):
    """The result for the GetBucketStat operation."""

    _attribute_map = {
        "storage": {"tag": "xml", "rename": "Storage", "type": "int"},
        "object_count": {"tag": "xml", "rename": "ObjectCount", "type": "int"},
        "multi_part_upload_count": {"tag": "xml", "rename": "MultipartUploadCount", "type": "int"},
        "live_channel_count": {"tag": "xml", "rename": "LiveChannelCount", "type": "int"},
        "last_modified_time": {"tag": "xml", "rename": "LastModifiedTime", "type": "int"},
        "standard_storage": {"tag": "xml", "rename": "StandardStorage", "type": "int"},
        "standard_object_count": {"tag": "xml", "rename": "StandardObjectCount", "type": "int"},
        "infrequent_access_storage": {"tag": "xml", "rename": "InfrequentAccessStorage", "type": "int"},
        "infrequent_access_real_storage": {"tag": "xml", "rename": "InfrequentAccessRealStorage", "type": "int"},
        "infrequent_access_object_count": {"tag": "xml", "rename": "InfrequentAccessObjectCount", "type": "int"},
        "archive_storage": {"tag": "xml", "rename": "ArchiveStorage", "type": "int"},
        "archive_real_storage": {"tag": "xml", "rename": "ArchiveRealStorage", "type": "int"},
        "archive_object_count": {"tag": "xml", "rename": "ArchiveObjectCount", "type": "int"},
        "cold_archive_storage": {"tag": "xml", "rename": "ColdArchiveStorage", "type": "int"},
        "cold_archive_real_storage": {"tag": "xml", "rename": "ColdArchiveRealStorage", "type": "int"},
        "cold_archive_object_count": {"tag": "xml", "rename": "ColdArchiveObjectCount", "type": "int"},
        "deep_cold_archive_storage": {"tag": "xml", "rename": "DeepColdArchiveStorage", "type": "int"},
        "deep_cold_archive_real_storage": {"tag": "xml", "rename": "DeepColdArchiveRealStorage", "type": "int"},
        "deep_cold_archive_object_count": {"tag": "xml", "rename": "DeepColdArchiveObjectCount", "type": "int"},
        "delete_marker_count": {"tag": "xml", "rename": "DeleteMarkerCount", "type": "int"},
    }

    _xml_map = {
        "name": "BucketStat"
    }

    def __init__(
        self,
        storage: Optional[int] = None,
        object_count: Optional[int] = None,
        multi_part_upload_count: Optional[int] = None,
        live_channel_count: Optional[int] = None,
        last_modified_time: Optional[int] = None,
        standard_storage: Optional[int] = None,
        standard_object_count: Optional[int] = None,
        infrequent_access_storage: Optional[int] = None,
        infrequent_access_real_storage: Optional[int] = None,
        infrequent_access_object_count: Optional[int] = None,
        archive_storage: Optional[int] = None,
        archive_real_storage: Optional[int] = None,
        archive_object_count: Optional[int] = None,
        cold_archive_storage: Optional[int] = None,
        cold_archive_real_storage: Optional[int] = None,
        cold_archive_object_count: Optional[int] = None,
        deep_cold_archive_storage: Optional[int] = None,
        deep_cold_archive_real_storage: Optional[int] = None,
        deep_cold_archive_object_count: Optional[int] = None,
        delete_marker_count: Optional[int] = None,

        **kwargs: Any
    ) -> None:
        """
        Args:
            storage (int, optional): The total actual storage capacity of the bucket, measured in bytes.
            object_count (int, optional): The total number of objects in the bucket.
            multi_part_upload_count (int, optional): The number of Multipart Uploads in the Bucket that have been initialized but not yet completed (Complete) or aborted (Abort).
            live_channel_count (int, optional): The number of live channels in the bucket.
            last_modified_time (int, optional): The time point at which the stored information is obtained, in the format of a timestamp and in seconds.
            standard_storage (int, optional): The storage capacity of standard storage types, measured in bytes.
            standard_object_count (int, optional): The number of standard storage type objects.
            infrequent_access_storage (int, optional): The billing storage capacity of low-frequency storage type, in bytes.
            infrequent_access_real_storage (int, optional): The actual storage capacity of low-frequency storage types, in bytes.
            infrequent_access_object_count (int, optional): The number of low-frequency storage type objects.
            archive_storage (int, optional): The billing storage capacity of archive storage type, in bytes.
            archive_object_count (int, optional): The actual storage capacity of the archive storage type, in bytes.
            cold_archive_storage (int, optional): The number of objects of archive storage type.
            cold_archive_real_storage (int, optional): The billing storage capacity of cold archive storage type, in bytes.
            cold_archive_object_count (int, optional): The actual storage capacity of the cold archive storage type, in bytes.
            deep_cold_archive_storage (int, optional): The billing storage capacity of deep cold archive storage type, in bytes.
            deep_cold_archive_real_storage (int, optional): The actual storage capacity of the deep cold archive storage type, in bytes.
            deep_cold_archive_object_count (int, optional): The number of objects of the deep cold archive storage type.
            delete_marker_count (int, optional): Delete the count of marker
        """
        super().__init__(**kwargs)
        self.storage = storage
        self.object_count = object_count
        self.multi_part_upload_count = multi_part_upload_count
        self.live_channel_count = live_channel_count
        self.last_modified_time = last_modified_time
        self.standard_storage = standard_storage
        self.standard_object_count = standard_object_count
        self.infrequent_access_storage = infrequent_access_storage
        self.infrequent_access_real_storage = infrequent_access_real_storage
        self.infrequent_access_object_count = infrequent_access_object_count
        self.archive_storage = archive_storage
        self.archive_real_storage = archive_real_storage
        self.archive_object_count = archive_object_count
        self.cold_archive_storage = cold_archive_storage
        self.cold_archive_real_storage = cold_archive_real_storage
        self.cold_archive_object_count = cold_archive_object_count
        self.deep_cold_archive_storage = deep_cold_archive_storage
        self.deep_cold_archive_real_storage = deep_cold_archive_real_storage
        self.deep_cold_archive_object_count = deep_cold_archive_object_count
        self.delete_marker_count = delete_marker_count


class GetBucketLocationRequest(serde.RequestModel):
    """The request for the GetBucketLocation operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
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

class GetBucketLocationResult(serde.ResultModel):
    """The result for the GetBucketLocation operation."""

    _attribute_map = {
        "location": {"tag": "xml", "rename": '.'},
    }

    _xml_map = {
        "name": "LocationConstraint"
    }

    def __init__(
        self,
        location: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            location (str, optional): The region in which the bucket is located.
        """
        super().__init__(**kwargs)
        self.location = location


class SSERule(serde.Model):
    """Information on server-side encryption methods."""

    _attribute_map = {
        "kms_master_key_id": {"tag": "xml", "rename": "KMSMasterKeyID"},
        "sse_algorithm": {"tag": "xml", "rename": "SSEAlgorithm"},
        "kms_data_encryption": {"tag": "xml", "rename": "KMSDataEncryption"},
    }

    _xml_map = {
        "name": "ServerSideEncryptionRule"
    }

    def __init__(
        self,
        kms_master_key_id: Optional[str] = None,
        sse_algorithm: Optional[str] = None,
        kms_data_encryption: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            kms_master_key_id (str, optional): The customer master key (CMK) ID in use. A valid value is returned only if you set SSEAlgorithm to KMS
                 and specify the CMK ID. In other cases, an empty value is returned.
            sse_algorithm (str, optional): The server-side encryption method that is used by default.
            kms_data_encryption (str, optional): Object's encryption algorithm. If this element is not included in the response,
                it indicates that the object is using the AES256 encryption algorithm.
                This option is only valid if the SSEAlgorithm value is KMS.
        """
        super().__init__(**kwargs)
        self.kms_master_key_id = kms_master_key_id
        self.sse_algorithm = sse_algorithm
        self.kms_data_encryption = kms_data_encryption

class BucketPolicy(serde.Model):
    """The container that stores the logs."""

    _attribute_map = {
        "log_bucket": {"tag": "xml", "rename": "LogBucket"},
        "log_prefix": {"tag": "xml", "rename": "LogPrefix"},
    }

    _xml_map = {
        "name": "BucketPolicy"
    }

    def __init__(
        self,
        log_bucket: Optional[str] = None,
        log_prefix: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            log_bucket (str, optional): The name of the bucket that stores the logs.
                 and specify the CMK ID. In other cases, an empty value is returned.
            log_prefix (str, optional): The directory in which logs are stored.
        """
        super().__init__(**kwargs)
        self.log_bucket = log_bucket
        self.log_prefix = log_prefix



class BucketInfo(serde.Model):
    """BucketInfo defines Bucket information."""

    _attribute_map = {
        "name": {"tag": "xml", "rename": "Name"},
        "access_monitor": {"tag": "xml", "rename": "AccessMonitor"},
        "location": {"tag": "xml", "rename": "Location"},
        "creation_date": {"tag": "xml", "rename": "CreationDate", "type": "datetime"},
        "extranet_endpoint": {"tag": "xml", "rename": "ExtranetEndpoint"},
        "intranet_endpoint": {"tag": "xml", "rename": "IntranetEndpoint"},
        "acl": {"tag": "xml", "rename": "AccessControlList/Grant"},
        "data_redundancy_type": {"tag": "xml", "rename": "DataRedundancyType"},
        "owner": {"tag": "xml", "rename": "Owner", "type": "Owner"},
        "storage_class": {"tag": "xml", "rename": "StorageClass"},
        "resource_group_id": {"tag": "xml", "rename": "ResourceGroupId"},
        "sse_rule": {"tag": "xml", "rename": "ServerSideEncryptionRule", "type": "SSERule"},
        "versioning": {"tag": "xml", "rename": "Versioning"},
        "transfer_acceleration": {"tag": "xml", "rename": "TransferAcceleration"},
        "cross_region_replication": {"tag": "xml", "rename": "CrossRegionReplication"},
        "bucket_policy": {"tag": "xml", "rename": "BucketPolicy", "type": "BucketPolicy"},
        "comment": {"tag": "xml", "rename": "Comment"},
        "block_public_access": {"tag": "xml", "rename": "BlockPublicAccess", "type": "bool"},
    }

    _dependency_map = {
        "Owner": {"new": lambda: Owner()},
        "SSERule": {"new": lambda: SSERule()},
        "BucketPolicy": {"new": lambda: BucketPolicy()},
    }

    _xml_map = {
        "name": "Bucket"
    }

    def __init__(
        self,
        name: Optional[str] = None,
        access_monitor: Optional[str] = None,
        location: Optional[str] = None,
        creation_date: Optional[datetime.datetime] = None,
        extranet_endpoint: Optional[str] = None,
        intranet_endpoint: Optional[str] = None,
        acl: Optional[str] = None,
        data_redundancy_type: Optional[str] = None,
        owner: Optional[Owner] = None,
        storage_class: Optional[str] = None,
        resource_group_id: Optional[str] = None,
        sse_rule: Optional[SSERule] = None,
        versioning: Optional[str] = None,
        transfer_acceleration: Optional[str] = None,
        cross_region_replication: Optional[str] = None,
        bucket_policy: Optional[BucketPolicy] = None,
        comment: Optional[str] = None,
        block_public_access: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the bucket.
            access_monitor (str, optional): Indicates whether access tracking is enabled for the bucket.
            location (str, optional): The region in which the bucket is located.
            creation_date (datetime, optional): The time when the bucket is created. The time is in UTC.
            extranet_endpoint (str, optional): The public endpoint that is used to access the bucket over the Internet.
            intranet_endpoint (str, optional): The internal endpoint that is used to access the bucket from Elastic
            acl (str, optional): The container that stores the access control list (ACL) information about the bucket.
            data_redundancy_type (str, optional): The disaster recovery type of the bucket.
            owner (Owner, optional): The container that stores information about the bucket owner.
            storage_class (str, optional): The storage class of the bucket.
            resource_group_id (str, optional): The ID of the resource group to which the bucket belongs.
            sse_rule (SSERule, optional): The container that stores the server-side encryption method.
            versioning (str, optional): Indicates whether versioning is enabled for the bucket.
            transfer_acceleration (str, optional): Indicates whether transfer acceleration is enabled for the bucket.
            cross_region_replication (str, optional): Indicates whether cross-region replication (CRR) is enabled for the bucket.
            bucket_policy (BucketPolicy, optional): The container that stores the logs.
            comment (str, optional): Annotation information.
            block_public_access (bool, optional): Obtain configuration information for Bucket to block public access.

        """
        super().__init__(**kwargs)
        self.name = name
        self.access_monitor = access_monitor
        self.location = location
        self.creation_date = creation_date
        self.extranet_endpoint = extranet_endpoint
        self.intranet_endpoint = intranet_endpoint
        self.acl = acl
        self.data_redundancy_type = data_redundancy_type
        self.owner = owner
        self.storage_class = storage_class
        self.resource_group_id = resource_group_id
        self.sse_rule = sse_rule
        self.versioning = versioning
        self.transfer_acceleration = transfer_acceleration
        self.cross_region_replication = cross_region_replication
        self.bucket_policy = bucket_policy
        self.comment = comment
        self.block_public_access = block_public_access

class GetBucketInfoRequest(serde.RequestModel):
    """The request for the GetBucketInfoRequest operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
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

class GetBucketInfoResult(serde.ResultModel):
    """The result for the GetBucketInfoResult operation."""

    _attribute_map = {
        "bucket_info": {"tag": "xml", "rename": 'Bucket', "type": "BucketInfo"},
    }

    _dependency_map = {
        "BucketInfo": {"new": lambda: BucketInfo()},
    }

    _xml_map = {
        "name": "BucketInfo"
    }

    def __init__(
        self,
        bucket_info: Optional[BucketInfo] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket_info (BucketInfo, optional): BucketInfo defines Bucket information.
        """
        super().__init__(**kwargs)
        self.bucket_info = bucket_info


class VersioningConfiguration(serde.Model):
    """The versioning state of the bucket. Valid values: Enabled,Suspended."""

    _attribute_map = {
        "status": {"tag": "xml", "rename": "Status"},
    }

    _xml_map = {
        "name": "VersioningConfiguration"
    }

    def __init__(
        self,
        status: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            status (str, optional): The versioning state of the bucket. Valid values: Enabled,Suspended
        """
        super().__init__(**kwargs)
        self.status = status


class PutBucketVersioningRequest(serde.RequestModel):
    """The request for the PutBucketVersioning operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "versioning_configuration": {"tag": "input", "position": "body", "rename": "VersioningConfiguration", "type": "xml"},
    }

    _xml_map = {
        "name": "VersioningConfiguration"
    }

    def __init__(
        self,
        bucket: str = None,
        versioning_configuration: Optional["VersioningConfiguration"] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            versioning_configuration (VersioningConfiguration, optional): A container for storing version control status.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.versioning_configuration = versioning_configuration


class PutBucketVersioningResult(serde.ResultModel):
    """The result for the PutBucketVersioning operation."""

class GetBucketVersioningRequest(serde.RequestModel):
    """The request for the GetBucketVersioning operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
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

class GetBucketVersioningResult(serde.ResultModel):
    """The result for the GetBucketVersioning operation."""

    _attribute_map = {
        "version_status": {"tag": "xml", "rename": "Status"},
    }

    _xml_map = {
        "name": "VersioningConfiguration"
    }

    def __init__(
        self,
        version_status: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_status (str, optional): The versioning state of the bucket. Valid values: Enabled,Suspended
        """
        super().__init__(**kwargs)
        self.version_status = version_status


class ListObjectVersionsRequest(serde.RequestModel):
    """The request for the ListObjectVersions operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "delimiter": {"tag": "input", "position": "query", "rename": "delimiter"},
        "key_marker": {"tag": "input", "position": "query", "rename": "key-marker"},
        "version_id_marker": {"tag": "input", "position": "query", "rename": "version-id-marker"},
        "max_keys": {"tag": "input", "position": "query", "rename": "max-keys", "type": "int"},
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
        "encoding_type": {"tag": "input", "position": "query", "rename": "encoding-type"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        delimiter: Optional[str] = None,
        key_marker: Optional[str] = None,
        version_id_marker: Optional[str] = None,
        max_keys: Optional[int] = None,
        prefix: Optional[str] = None,
        encoding_type: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            delimiter (str, optional): The character that is used to group objects by name.
                If you specify the delimiter parameter in the request, the response contains
                the CommonPrefixes parameter. The objects whose names contain the same string
                from the prefix to the next occurrence of the delimiter are grouped
                as a single result element in CommonPrefixes.
            key_marker (str, optional): Specifies that objects whose names are alphabetically after the value of the key-marker parameter are returned.
                This parameter can be specified together with version-id-marker.
                By default, this parameter is left empty.
            version_id_marker (str, optional): Specifies that the versions created before the version specified by version-id-marker for the object
                whose name is specified by key-marker are returned by creation time in descending order.
                By default, if this parameter is not specified, the results are returned from the latest
                version of the object whose name is alphabetically after the value of key-marker.
            max_keys (int, optional): The maximum number of objects that you want to return.
                If the list operation cannot be complete at a time, because the max-keys parameter is specified,
                the NextMarker element is included in the response as the marker for the next list operation.
            prefix (str, optional): The prefix that the names of the returned objects must contain.
            encoding_type (str, optional): The encoding type of the content in the response. Valid value: url
            request_payer (str, optional): To indicate that the requester is aware that the request
                and data download will incur costs
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.delimiter = delimiter
        self.key_marker = key_marker
        self.version_id_marker = version_id_marker
        self.max_keys = max_keys
        self.prefix = prefix
        self.encoding_type = encoding_type
        self.request_payer = request_payer


class ObjectVersionProperties(serde.Model):
    """Stores the metadata of the object version."""

    _attribute_map = {
        "key": {"tag": "xml", "rename": "Key"},
        "version_id": {"tag": "xml", "rename": "VersionId"},
        "is_latest": {"tag": "xml", "rename": "IsLatest", "type": "bool"},
        "object_type": {"tag": "xml", "rename": "Type"},
        "size": {"tag": "xml", "rename": "Size", "type": "int"},
        "etag": {"tag": "xml", "rename": "ETag"},
        "last_modified": {"tag": "xml", "rename": "LastModified", "type": "datetime"},
        "storage_class": {"tag": "xml", "rename": "StorageClass"},
        "owner": {"tag": "xml", "rename": "Owner", "type": "Owner"},
        "restore_info": {"tag": "xml", "rename": "RestoreInfo"},
        "transition_time": {"tag": "xml", "rename": "TransitionTime"},
    }

    _dependency_map = {
        "Owner": {"new": lambda: Owner()},
    }

    _xml_map = {
        "name": "Version"
    }

    def __init__(
        self,
        key: Optional[str] = None,
        version_id: Optional[str] = None,
        is_latest: Optional[bool] = None,
        object_type: Optional[str] = None,
        size: Optional[int] = None,
        etag: Optional[str] = None,
        last_modified: Optional[datetime.datetime] = None,
        storage_class: Optional[str] = None,
        owner: Optional[Owner] = None,
        restore_info: Optional[str] = None,
        transition_time: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The name of the object.
            version_id (str, optional): The version ID of the object.
            is_latest (bool, optional): Indicates whether the version is the current version.
            object_type (str, optional): The type of the object.
                Valid values: Normal, Multipart and Appendable
            size (int, optional): The size of the returned object. Unit: bytes.
            etag (str, optional): The entity tag (ETag). An ETag is created when an object is created to
                identify the content of the object.
            last_modified (datetime, optional): The time when the returned objects were last modified.
            storage_class (str, optional): The storage class of the object.
            owner (str, optional): The container that stores information about the bucket owner.
            restore_info (Owner, optional): The restoration status of the object.
            transition_time (str): The time when the storage class of the object is converted to Cold Archive or Deep Cold Archive based on lifecycle rules.
        """
        super().__init__(**kwargs)
        self.key = key
        self.version_id = version_id
        self.is_latest = is_latest
        self.object_type = object_type
        self.size = size
        self.etag = etag
        self.last_modified = last_modified
        self.storage_class = storage_class
        self.owner = owner
        self.restore_info = restore_info
        self.transition_time = transition_time


class DeleteMarkerProperties(serde.Model):
    """The container that stores delete markers."""

    _attribute_map = {
        "key": {"tag": "xml", "rename": "Key"},
        "version_id": {"tag": "xml", "rename": "VersionId"},
        "is_latest": {"tag": "xml", "rename": "IsLatest", "type": "bool"},
        "last_modified": {"tag": "xml", "rename": "LastModified", "type": "datetime"},
        "owner": {"tag": "xml", "rename": "Owner", "type": "Owner"},
    }

    _dependency_map = {
        "Owner": {"new": lambda: Owner()},
    }

    _xml_map = {
        "name": "DeleteMarker"
    }

    def __init__(
        self,
        key: Optional[str] = None,
        version_id: Optional[str] = None,
        is_latest: Optional[bool] = None,
        last_modified: Optional[datetime.datetime] = None,
        owner: Optional[Owner] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The name of the object.
            version_id (str, optional): The version ID of the object.
            is_latest (bool, optional): Indicates whether the version is the current version.
            last_modified (datetime, optional): The time when the returned objects were last modified.
            owner (str, optional): The container that stores information about the bucket owner.
        """
        super().__init__(**kwargs)
        self.key = key
        self.version_id = version_id
        self.is_latest = is_latest
        self.last_modified = last_modified
        self.owner = owner


class ListObjectVersionsResult(serde.ResultModel):
    """The result for the ListObjectVersions operation."""

    _attribute_map = {
        "name": {"tag": "xml", "rename": "Name"},
        "key_marker": {"tag": "xml", "rename": "KeyMarker"},
        "next_key_marker": {"tag": "xml", "rename": "NextKeyMarker"},
        "version_id_marker": {"tag": "xml", "rename": "VersionIdMarker"},
        "next_version_id_marker": {"tag": "xml", "rename": "NextVersionIdMarker"},
        "prefix": {"tag": "xml", "rename": "Prefix"},
        "max_keys": {"tag": "xml", "rename": "MaxKeys", "type": "int"},
        "delimiter": {"tag": "xml", "rename": "Delimiter"},
        "is_truncated": {"tag": "xml", "rename": "IsTruncated", "type": "bool"},
        "encoding_type": {"tag": "xml", "rename": "EncodingType"},
        "version": {"tag": "xml", "rename": "Version", "type": "[ObjectVersionProperties]"},
        "delete_marker": {"tag": "xml", "rename": "DeleteMarker", "type": "[DeleteMarkerProperties]"},
        "common_prefixes": {"tag": "xml", "rename": "CommonPrefixes", "type": "[CommonPrefix]"},
    }

    _dependency_map = {
        "ObjectVersionProperties": {"new": lambda: ObjectVersionProperties()},
        "DeleteMarkerProperties": {"new": lambda: DeleteMarkerProperties()},
        "CommonPrefix": {"new": lambda: CommonPrefix()},
    }

    _xml_map = {
        "name": "ListVersionsResult"
    }

    def __init__(
        self,
        name: Optional[str] = None,
        key_marker: Optional[str] = None,
        next_key_marker: Optional[str] = None,
        version_id_marker: Optional[str] = None,
        next_version_id_marker: Optional[str] = None,
        prefix: Optional[str] = None,
        max_keys: Optional[int] = None,
        delimiter: Optional[str] = None,
        is_truncated: Optional[bool] = None,
        encoding_type: Optional[str] = None,
        version: Optional[List[ObjectVersionProperties]] = None,
        delete_marker: Optional[List[DeleteMarkerProperties]] = None,
        common_prefixes: Optional[List[CommonPrefix]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the bucket.
            key_marker (str, optional): Indicates the object from which the ListObjectVersions (GetBucketVersions) operation starts.
            next_key_marker (str, optional): If not all results are returned for the request, the NextKeyMarker parameter is included
                in the response to indicate the key-marker value of the next ListObjectVersions (GetBucketVersions) request.
            version_id_marker (str, optional): The version from which the ListObjectVersions (GetBucketVersions) operation starts.
            next_version_id_marker (str, optional): If not all results are returned for the request, the NextVersionIdMarker parameter is included in
                the response to indicate the version-id-marker value of the next ListObjectVersions (GetBucketVersions) request.
            prefix (str, optional): The prefix contained in the returned object names.
            max_keys (int, optional): The maximum number of returned objects in the response.
            delimiter (str, optional): The character that is used to group objects by name.
            is_truncated (bool, optional): Indicates whether the returned results are truncated.
                true indicates that not all results are returned this time.
                false indicates that all results are returned this time.
            encoding_type (str, optional): The encoding type of the content in the response.
            version ([ObjectVersionProperties], optional): The container that stores the versions of objects, excluding delete markers.
            delete_marker ([DeleteMarkerProperties], optional): The container that stores delete markers.
            common_prefixes ([CommonPrefix], optional): If the Delimiter parameter is specified in the request,
                the response contains the CommonPrefixes element.
        """
        super().__init__(**kwargs)
        self.name = name
        self.key_marker = key_marker
        self.next_key_marker = next_key_marker
        self.version_id_marker = version_id_marker
        self.next_version_id_marker = next_version_id_marker
        self.prefix = prefix
        self.max_keys = max_keys
        self.delimiter = delimiter
        self.is_truncated = is_truncated
        self.encoding_type = encoding_type
        self.version = version
        self.delete_marker = delete_marker
        self.common_prefixes = common_prefixes
