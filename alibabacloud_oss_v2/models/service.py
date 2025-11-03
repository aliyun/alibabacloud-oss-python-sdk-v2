"""Models for service operation APIs"""
# pylint: disable=too-few-public-methods, too-many-instance-attributes, unnecessary-lambda
# pylint: disable=super-init-not-called, too-many-lines, line-too-long, too-many-arguments
# pylint: disable=too-many-locals
import datetime
from typing import Optional, Any, List
from .. import serde
from .bucket_basic import Owner


class ListBucketsRequest(serde.RequestModel):
    """The request for the ListBuckets operation."""

    _attribute_map = {
        "marker": {"tag": "input", "position": "query", "rename": "marker"},
        "max_keys": {"tag": "input", "position": "query", "rename": "max-keys", "type": "int"},
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
        "resource_group_id": {"tag": "input", "position": "header", "rename": "x-oss-resource-group-id"},
        "tag_key": {"tag": "input", "position": "query", "rename": "tag-key"},
        "tag_value": {"tag": "input", "position": "query", "rename": "tag-value"},
        "tagging": {"tag": "input", "position": "query", "rename": "tagging"},
    }

    def __init__(
        self,
        marker: Optional[str] = None,
        max_keys: Optional[int] = None,
        prefix: Optional[str] = None,
        resource_group_id: Optional[str] = None,
        tag_key: Optional[str] = None,
        tag_value: Optional[str] = None,
        tagging: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            marker (str, optional): The name of the bucket from which the list operation begins.
            max_keys (int, optional): The maximum number of buckets that can be returned in the single query.
                Valid values: 1 to 1000.
            prefix (str, optional): The prefix that the names of returned buckets must contain.
                Limits the response to keys that begin with the specified prefix
            resource_group_id (str, optional): The ID of the resource group.
            tag_key (str, optional): A tag key of target buckets. The listing results will only include Buckets that have been tagged with this key.
            tag_value (str, optional): A tag value for the target buckets. If this parameter is specified in the request, the tag-key must also be specified. 
                The listing results will only include Buckets that have been tagged with this key-value pair.
            tagging (str, optional): Tag list of target buckets. Only Buckets that match all the key-value pairs in the list will added into the listing results. 
                The tagging parameter cannot be used with the tag-key and tag-value parameters in a request.
        """
        super().__init__(**kwargs)
        self.marker = marker
        self.max_keys = max_keys
        self.prefix = prefix
        self.resource_group_id = resource_group_id
        self.tag_key = tag_key
        self.tag_value = tag_value
        self.tagging = tagging


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

class ListBucketsResult(serde.ResultModel):
    """The result for the ListBuckets operation."""

    _attribute_map = {
        "prefix": {"tag": "xml", "rename": "Prefix"},
        "marker": {"tag": "xml", "rename": "Marker"},
        "max_keys": {"tag": "xml", "rename": "MaxKeys", "type": "int"},
        "is_truncated": {"tag": "xml", "rename": "IsTruncated", "type": "bool"},
        "next_marker": {"tag": "xml", "rename": "NextMarker"},
        "owner": {"tag": "xml", "rename": "Owner", "type": "Owner"},
        "buckets": {"tag": "xml", "rename": "Buckets/Bucket", "type": "[BucketProperties]"},
    }

    _dependency_map = {
        "ObjectProperties": {"new": lambda: BucketProperties()},
        "Owner": {"new": lambda: Owner()},
    }

    _xml_map = {"name":"ListAllMyBucketsResult"}

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

