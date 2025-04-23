from typing import Optional, List, Any
from .. import serde
from .bucket_basic import Owner

class CloudBoxProperties(serde.Model):
    """
    Information about cloud box.
    """

    _attribute_map = {
        'id': {'tag': 'xml', 'rename': 'ID'},
        'name': {'tag': 'xml', 'rename': 'Name'},
        'region': {'tag': 'xml', 'rename': 'Region'},
        'control_endpoint': {'tag': 'xml', 'rename': 'ControlEndpoint'},
        'data_endpoint': {'tag': 'xml', 'rename': 'DataEndpoint'},
        'alias': {'tag': 'xml', 'rename': 'Alias'},
    }

    _xml_map = {
        "name": "CloudBox"
    }

    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        region: Optional[str] = None,
        control_endpoint: Optional[str] = None,
        data_endpoint: Optional[str] = None,
        alias: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            id (str, optional): Cloud Box ID.
            name (str, optional): Cloud Box Name.
            region (str, optional): Regions supported by Cloud Box.
            control_endpoint (str, optional): control endpoint.
            data_endpoint (str, optional): data endpoint.
            alias (str, optional): The alias of the access point.
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.region = region
        self.control_endpoint = control_endpoint
        self.data_endpoint = data_endpoint
        self.alias = alias



class ListCloudBoxesRequest(serde.RequestModel):
    """
    The request for the ListCloudBoxes operation.
    """

    _attribute_map = {
        "marker": {"tag": "input", "position": "query", "rename": "marker"},
        "max_keys": {"tag": "input", "position": "query", "rename": "max-keys", "type": "int"},
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
    }

    def __init__(
        self,
        marker: Optional[str] = None,
        max_keys: Optional[int] = None,
        prefix: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            marker (str, optional): The name of the bucket from which the list operation begins.
            max_keys (int, optional): The maximum number of buckets that can be returned in the single query. Valid values: 1 to 1000.
            prefix (str, optional): The prefix that the names of returned buckets must contain.
        """
        super().__init__(**kwargs)
        self.marker = marker
        self.max_keys = max_keys
        self.prefix = prefix


class ListCloudBoxesResult(serde.ResultModel):
    """
    The result for the ListCloudBoxes operation.
    """

    _attribute_map = {
        'prefix': {'tag': 'xml', 'rename': 'Prefix'},
        'marker': {'tag': 'xml', 'rename': 'Marker'},
        'max_keys': {'tag': 'xml', 'rename': 'MaxKeys'},
        'is_truncated': {'tag': 'xml', 'rename': 'IsTruncated', 'type': 'bool'},
        'next_marker': {'tag': 'xml', 'rename': 'NextMarker'},
        "owner": {"tag": "xml", "rename": "Owner", "type": "Owner"},
        "cloud_boxes": {"tag": "xml", "rename": "CloudBoxes/CloudBox", "type": "[CloudBoxProperties]"},
    }

    _xml_map = {
        'name': 'ListCloudBoxResult'
    }

    _dependency_map = {
        "Owner": {"new": lambda: Owner()},
        "CloudBoxProperties": {"new": lambda: CloudBoxProperties()},
    }

    def __init__(
        self,
        prefix: Optional[str] = None,
        marker: Optional[str] = None,
        max_keys: Optional[int] = None,
        is_truncated: Optional[bool] = None,
        next_marker: Optional[str] = None,
        owner: Optional[Owner] = None,
        cloud_boxes: Optional[List[CloudBoxProperties]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            prefix (str, optional): The prefix that the names of returned buckets must contain.
            marker (str, optional): The name of the bucket from which the list operation begins.
            max_keys (int, optional): The maximum number of buckets that can be returned in the single query. Valid values: 1 to 1000.
            is_truncated (str, bool): Indicates whether the returned list is truncated. Valid values: * true: indicates that not all results are returned. * false: indicates that all results are returned.
            next_marker (str, optional): The marker for the next ListBuckets request, which can be used to return the remaining results.
            owner (Owner, optional): The container that stores information about the object owner.
            cloud_boxes ([CloudBoxProperties], optional): The container that stores information about cloud box bucket.
        """
        super().__init__(**kwargs)
        self.prefix = prefix
        self.marker = marker
        self.max_keys = max_keys
        self.is_truncated = is_truncated
        self.next_marker = next_marker
        self.owner = owner
        self.cloud_boxes = cloud_boxes