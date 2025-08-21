import datetime
from typing import Optional, List, Any, Dict
from alibabacloud_oss_v2 import serde


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
        "name": "BucketInfo"
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


class PutVectorBucketRequest(serde.RequestModel):
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




class PutVectorBucketResult(serde.ResultModel):
    """The result for the PutBucket operation."""



class GetVectorBucketRequest(serde.RequestModel):
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

class GetVectorBucketResult(serde.ResultModel):
    """The result for the GetBucketInfoResult operation."""

    _attribute_map = {
        "bucket_info": {"tag": "output", 'position': 'body', "rename": 'BucketInfo', "type": "BucketInfo,xml"},
    }

    _dependency_map = {
        "BucketInfo": {"new": lambda: BucketInfo()},
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




class DeleteVectorBucketRequest(serde.RequestModel):
    """The request for the DeleteBucket operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket to create.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteVectorBucketResult(serde.ResultModel):
    """The result for the DeleteBucket operation."""


class BucketProperties(serde.Model):
    """Stores the metadata of the bucket."""

    _attribute_map = {
        "name": {"tag": "xml", "rename": "Name"},
        "location": {"tag": "xml", "rename": "Location"},
        "creation_date": {"tag": "xml", "rename": "CreationDate", "type": "datetime"},
        "storage_class": {"tag": "xml", "rename": "StorageClass"},
        "extranet_endpoint": {"tag": "xml", "rename": "ExtranetEndpoint"},
        "intranet_endpoint": {"tag": "xml", "rename": "IntranetEndpoint"},
        "region": {"tag": "xml", "rename": "Region"},
        "resource_group_id": {"tag": "xml", "rename": "ResourceGroupId"},
    }

    def __init__(
        self,
        name: Optional[str] = None,
        location: Optional[str] = None,
        creation_date: Optional[datetime.datetime] = None,
        storage_class: Optional[str] = None,
        extranet_endpoint: Optional[str] = None,
        intranet_endpoint: Optional[str] = None,
        region: Optional[str] = None,
        resource_group_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the bucket.
            location (str, optional): The data center in which the bucket is located.
            creation_date (datetime, optional): The time when the bucket was created.
            storage_class (str, optional): The storage class of the bucket.
                Valid values: Standard, IA, Archive, ColdArchive and DeepColdArchive.
            extranet_endpoint (str, optional): The public endpoint used to access the bucket over the Internet.
            intranet_endpoint (str, optional): The internal endpoint that is used to access the bucket from ECS instances
                that reside in the same region as the bucket.
            region (str, optional): The region in which the bucket is located.
            resource_group_id (str, optional): The ID of the resource group to which the bucket belongs.
        """
        super().__init__(**kwargs)
        self.name = name
        self.location = location
        self.creation_date = creation_date
        self.storage_class = storage_class
        self.extranet_endpoint = extranet_endpoint
        self.intranet_endpoint = intranet_endpoint
        self.region = region
        self.resource_group_id = resource_group_id



class ListVectorBucketsRequest(serde.RequestModel):
    """The request for the ListBuckets operation."""

    _attribute_map = {
        "marker": {"tag": "input", "position": "query", "rename": "marker"},
        "max_keys": {"tag": "input", "position": "query", "rename": "max-keys", "type": "int"},
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
        "resource_group_id": {"tag": "input", "position": "header", "rename": "x-oss-resource-group-id"},
    }

    def __init__(
        self,
        marker: Optional[str] = None,
        max_keys: Optional[int] = None,
        prefix: Optional[str] = None,
        resource_group_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            marker (str, optional): The name of the bucket from which the list operation begins.
            max_keys (int, optional): The maximum number of buckets that can be returned in the single query.
                Valid values: 1 to 1000.
            prefix (str, optional): The prefix that the names of returned buckets must contain.
                Limits the response to keys that begin with the specified prefix
            request_payer (str, optional): The ID of the resource group.
        """
        super().__init__(**kwargs)
        self.marker = marker
        self.max_keys = max_keys
        self.prefix = prefix
        self.resource_group_id = resource_group_id



class ListVectorBucketsResult(serde.ResultModel):
    """The result for the ListBuckets operation."""

    _attribute_map = {
        "prefix": {"tag": "xml", "rename": "Prefix"},
        "marker": {"tag": "xml", "rename": "Marker"},
        "max_keys": {"tag": "xml", "rename": "MaxKeys", "type": "int"},
        "is_truncated": {"tag": "xml", "rename": "IsTruncated", "type": "bool"},
        "next_marker": {"tag": "xml", "rename": "NextMarker"},
        "owner": {"tag": "xml", "rename": "Owner", "type": "Owner"},
        "buckets": {"tag": "xml", "rename": "Buckets", "type": "[BucketProperties]"},
    }

    _dependency_map = {
        "BucketProperties": {"new": lambda: BucketProperties()},
        "Owner": {"new": lambda: Owner()},
    }

    _xml_map = {"name": "ListAllMyBucketsResult"}

    def __init__(
        self,
        prefix: Optional[str] = None,
        marker: Optional[str] = None,
        max_keys: Optional[int] = None,
        is_truncated: Optional[bool] = None,
        next_marker: Optional[str] = None,
        owner: Optional[Owner] = None,
        buckets: Optional[List[BucketProperties]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            prefix (str, optional): The prefix contained in the names of the returned bucket.
            marker (str, optional): The name of the bucket after which the ListBuckets operation starts
            max_keys (int, optional): The maximum number of buckets that can be returned for the request.
            is_truncated (bool, optional): Indicates whether the returned results are truncated.
                true indicates that not all results are returned this time.
                false indicates that all results are returned this time.
            next_marker (str, optional): The marker for the next ListBuckets request, which can be used
                to return the remaining results.
            owner (Owner, optional): The container that stores information about the bucket owner.
            buckets ([BucketProperties], optional): The container that stores information about buckets.
        """
        super().__init__(**kwargs)
        self.prefix = prefix
        self.marker = marker
        self.max_keys = max_keys
        self.is_truncated = is_truncated
        self.next_marker = next_marker
        self.owner = owner
        self.buckets = buckets
