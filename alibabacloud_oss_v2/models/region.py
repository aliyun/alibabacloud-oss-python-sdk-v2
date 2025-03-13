"""Models for region operation APIs"""
# pylint: disable=too-few-public-methods, too-many-instance-attributes, unnecessary-lambda
# pylint: disable=super-init-not-called, too-many-lines, line-too-long, too-many-arguments
# pylint: disable=too-many-locals
from typing import Optional, Any, List
from .. import serde

class DescribeRegionsRequest(serde.RequestModel):
    """The request for the DescribeRegions operation."""

    _attribute_map = {
        "regions": {"tag": "input", "position": "query", "rename": "regions"},
    }

    def __init__(
        self,
        regions: Optional[str] = '',
        **kwargs: Any
    ) -> None:
        """
        Args:
            regions (str, optional): Regional information
        """
        super().__init__(**kwargs)
        self.regions = regions

class RegionInfo(serde.Model):
    """Regional information."""

    _attribute_map = {
        "region": {"tag": "xml", "rename": "Region"},
        "internet_endpoint": {"tag": "xml", "rename": "InternetEndpoint"},
        "internal_endpoint": {"tag": "xml", "rename": "InternalEndpoint"},
        "accelerate_endpoint": {"tag": "xml", "rename": "AccelerateEndpoint"},
    }

    _xml_map = {
        "name": "RegionInfo"
    }

    def __init__(
        self,
        region: Optional[str] = None,
        internet_endpoint: Optional[str] = None,
        internal_endpoint: Optional[str] = None,
        accelerate_endpoint: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            region (str, optional): OSS dedicated region ID.
            internet_endpoint (str, optional): External endpoint.
            internal_endpoint (str, optional): Internal network endpoint.
            accelerate_endpoint (str, optional): Transfer acceleration endpoint.
        """
        super().__init__(**kwargs)
        self.region = region
        self.internet_endpoint = internet_endpoint
        self.internal_endpoint = internal_endpoint
        self.accelerate_endpoint = accelerate_endpoint

class DescribeRegionsResult(serde.ResultModel):
    """The result for the DescribeRegions operation."""

    _attribute_map = {
        "region_info": {"tag": "xml", "rename": "RegionInfo", "type": "[RegionInfo]"},
    }

    _dependency_map = {
        "RegionInfo": {"new": lambda: RegionInfo()},
    }

    _xml_map = {
        "name": "RegionInfoList"
    }

    def __init__(
        self,
        region_info: Optional[List[RegionInfo]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            region_info (RegionInfo, optional): The result for the DescribeRegions operation.
        """
        super().__init__(**kwargs)
        self.region_info = region_info
