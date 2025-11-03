import datetime
from typing import Optional, List, Any, Dict
from ... import serde

class BucketInfo(serde.Model):
    """BucketInfo defines Bucket information."""

    _attribute_map = {
        "name": {"tag": "xml", "rename": "Name"},
        "location": {"tag": "xml", "rename": "Location"},
        "creation_date": {"tag": "xml", "rename": "CreationDate", "type": "datetime"},
        "extranet_endpoint": {"tag": "xml", "rename": "ExtranetEndpoint"},
        "intranet_endpoint": {"tag": "xml", "rename": "IntranetEndpoint"},
        "resource_group_id": {"tag": "xml", "rename": "ResourceGroupId"},
    }

    _dependency_map = {

    }

    _xml_map = {
        "name": "BucketInfo"
    }

    def __init__(
        self,
        name: Optional[str] = None,
        location: Optional[str] = None,
        creation_date: Optional[datetime.datetime] = None,
        extranet_endpoint: Optional[str] = None,
        intranet_endpoint: Optional[str] = None,
        resource_group_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the bucket.
            location (str, optional): The region in which the bucket is located.
            creation_date (datetime, optional): The time when the bucket is created. The time is in UTC.
            extranet_endpoint (str, optional): The public endpoint that is used to access the bucket over the Internet.
            intranet_endpoint (str, optional): The internal endpoint that is used to access the bucket from Elastic
            resource_group_id (str, optional): The ID of the resource group to which the bucket belongs.
        """
        super().__init__(**kwargs)
        self.name = name
        self.location = location
        self.creation_date = creation_date
        self.extranet_endpoint = extranet_endpoint
        self.intranet_endpoint = intranet_endpoint
        self.resource_group_id = resource_group_id


class PutVectorBucketRequest(serde.RequestModel):
    """The request for the PutBucket operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "resource_group_id": {"tag": "input", "position": "header", "rename": "x-oss-resource-group-id"},
        "bucket_tagging": {"tag": "input", "position": "header", "rename": "x-oss-bucket-tagging"},
    }

    def __init__(
        self,
        bucket: str = None,
        resource_group_id: Optional[str] = None,
        bucket_tagging: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket to create.
            resource_group_id (str, optional): The ID of the resource group.
            bucket_tagging (str, optional): The tagging information for the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.resource_group_id = resource_group_id
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
        bucket: str = None,
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
        "buckets": {"tag": "xml", "rename": "Buckets", "type": "[BucketProperties]"},
    }

    _dependency_map = {
        "BucketProperties": {"new": lambda: BucketProperties()},
    }

    _xml_map = {"name": "ListAllMyBucketsResult"}

    def __init__(
        self,
        prefix: Optional[str] = None,
        marker: Optional[str] = None,
        max_keys: Optional[int] = None,
        is_truncated: Optional[bool] = None,
        next_marker: Optional[str] = None,
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
            buckets ([BucketProperties], optional): The container that stores information about buckets.
        """
        super().__init__(**kwargs)
        self.prefix = prefix
        self.marker = marker
        self.max_keys = max_keys
        self.is_truncated = is_truncated
        self.next_marker = next_marker
        self.buckets = buckets
