import datetime
from typing import Optional, List, Any, Union
from .. import serde


class ArchiveDirectReadConfiguration(serde.Model):
    """
    The container that stores the configurations for real-time access of Archive objects.
    """

    _attribute_map = { 
        'enabled': {'tag': 'xml', 'rename': 'Enabled', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'ArchiveDirectReadConfiguration'
    }

    def __init__(
        self,
        enabled: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            enabled (bool, optional): Specifies whether to enable real-time access of Archive objects for a bucket. Valid values:- true- false
        """
        super().__init__(**kwargs)
        self.enabled = enabled


class PutBucketArchiveDirectReadRequest(serde.RequestModel):
    """
    The request for the PutBucketArchiveDirectRead operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'archive_direct_read_configuration': {'tag': 'input', 'position': 'body', 'rename': 'ArchiveDirectReadConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        archive_direct_read_configuration: Optional[ArchiveDirectReadConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            archive_direct_read_configuration (ArchiveDirectReadConfiguration, optional): The request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.archive_direct_read_configuration = archive_direct_read_configuration


class PutBucketArchiveDirectReadResult(serde.ResultModel):
    """
    The request for the PutBucketArchiveDirectRead operation.
    """


class GetBucketArchiveDirectReadRequest(serde.RequestModel):
    """
    The request for the GetBucketArchiveDirectRead operation.
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


class GetBucketArchiveDirectReadResult(serde.ResultModel):
    """
    The request for the GetBucketArchiveDirectRead operation.
    """

    _attribute_map = { 
        'archive_direct_read_configuration': {'tag': 'output', 'position': 'body', 'rename': 'ArchiveDirectReadConfiguration', 'type': 'ArchiveDirectReadConfiguration,xml'},
    }

    _dependency_map = { 
        'ArchiveDirectReadConfiguration': {'new': lambda: ArchiveDirectReadConfiguration()},
    }

    def __init__(
        self,
        archive_direct_read_configuration: Optional[ArchiveDirectReadConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            archive_direct_read_configuration (ArchiveDirectReadConfiguration, optional): The container that stores the configurations for real-time access of Archive objects.
        """
        super().__init__(**kwargs)
        self.archive_direct_read_configuration = archive_direct_read_configuration

