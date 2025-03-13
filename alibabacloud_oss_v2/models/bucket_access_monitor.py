import datetime
from typing import Optional, List, Any, Union
from enum import Enum
from .. import serde


class AccessMonitorStatusType(str, Enum):
    """
    A short description of struct
    """

    ENABLED = 'Enabled'
    DISABLED = 'Disabled'


class AccessMonitorConfiguration(serde.Model):
    """
    The container that stores access monitor configuration.
    """

    _attribute_map = { 
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
    }

    _xml_map = {
        'name': 'AccessMonitorConfiguration'
    }

    def __init__(
        self,
        status: Optional[Union[str, AccessMonitorStatusType]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            status (str | AccessMonitorStatusType, optional): The access tracking status of the bucket. Valid values:- Enabled: Access tracking is enabled.- Disabled: Access tracking is disabled.
        """
        super().__init__(**kwargs)
        self.status = status


class PutBucketAccessMonitorRequest(serde.RequestModel):
    """
    The request for the PutBucketAccessMonitor operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_monitor_configuration': {'tag': 'input', 'position': 'body', 'rename': 'AccessMonitorConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        access_monitor_configuration: Optional[AccessMonitorConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            access_monitor_configuration (AccessMonitorConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_monitor_configuration = access_monitor_configuration


class PutBucketAccessMonitorResult(serde.ResultModel):
    """
    The request for the PutBucketAccessMonitor operation.
    """

class GetBucketAccessMonitorRequest(serde.RequestModel):
    """
    The request for the GetBucketAccessMonitor operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
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


class GetBucketAccessMonitorResult(serde.ResultModel):
    """
    The request for the GetBucketAccessMonitor operation.
    """

    _attribute_map = { 
        'access_monitor_configuration': {'tag': 'output', 'position': 'body', 'rename': 'AccessMonitorConfiguration', 'type': 'AccessMonitorConfiguration,xml'},
    }

    _dependency_map = { 
        'AccessMonitorConfiguration': {'new': lambda: AccessMonitorConfiguration()},
    }

    _xml_map = {
        'name': 'AccessMonitorConfiguration'
    }

    def __init__(
        self,
        access_monitor_configuration: Optional[AccessMonitorConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            access_monitor_configuration (AccessMonitorConfiguration, optional): The container that stores access monitor configuration.
        """
        super().__init__(**kwargs)
        self.access_monitor_configuration = access_monitor_configuration
