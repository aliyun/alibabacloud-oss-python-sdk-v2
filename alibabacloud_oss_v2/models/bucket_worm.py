import datetime
from typing import Optional, List, Any, Union
from enum import Enum
from .. import serde


class BucketWormStateType(str, Enum):
    """
    The status of the retention policy
    """

    IN_PROGRESS = 'InProgress'
    LOCKED = 'Locked'


class InitiateWormConfiguration(serde.Model):
    """
    The container that stores the root node.
    """

    _attribute_map = { 
        'retention_period_in_days': {'tag': 'xml', 'rename': 'RetentionPeriodInDays', 'type': 'int'},
    }

    _xml_map = {
        'name': 'InitiateWormConfiguration'
    }

    def __init__(
        self,
        retention_period_in_days: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            retention_period_in_days (int, optional): The number of days for which objects can be retained.
        """
        super().__init__(**kwargs)
        self.retention_period_in_days = retention_period_in_days


class ExtendWormConfiguration(serde.Model):
    """
    The container that stores the root node.
    """

    _attribute_map = { 
        'retention_period_in_days': {'tag': 'xml', 'rename': 'RetentionPeriodInDays', 'type': 'int'},
    }

    _xml_map = {
        'name': 'ExtendWormConfiguration'
    }

    def __init__(
        self,
        retention_period_in_days: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            retention_period_in_days (int, optional): The number of days for which objects can be retained.
        """
        super().__init__(**kwargs)
        self.retention_period_in_days = retention_period_in_days


class WormConfiguration(serde.Model):
    """
    The container that stores the information about retention policies of the bucket.
    """

    _attribute_map = { 
        'worm_id': {'tag': 'xml', 'rename': 'WormId', 'type': 'str'},
        'state': {'tag': 'xml', 'rename': 'State', 'type': 'str'},
        'retention_period_in_days': {'tag': 'xml', 'rename': 'RetentionPeriodInDays', 'type': 'int'},
        'creation_date': {'tag': 'xml', 'rename': 'CreationDate', 'type': 'str'},
        'expiration_date': {'tag': 'xml', 'rename': 'ExpirationDate', 'type': 'str'},
    }

    _xml_map = {
        'name': 'WormConfiguration'
    }

    def __init__(
        self,
        worm_id: Optional[str] = None,
        state: Optional[Union[str, BucketWormStateType]] = None,
        retention_period_in_days: Optional[int] = None,
        creation_date: Optional[str] = None,
        expiration_date: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            worm_id (str, optional): The ID of the retention policy.Note If the specified retention policy ID that is used to query the retention policy configurations of the bucket does not exist, OSS returns the 404 error code.
            state (str | BucketWormStateType, optional): The status of the retention policy. Valid values:- InProgress: indicates that the retention policy is in the InProgress state. By default, a retention policy is in the InProgress state after it is created. The policy remains in this state for 24 hours.- Locked: indicates that the retention policy is in the Locked state.
            retention_period_in_days (int, optional): The number of days for which objects can be retained.
            creation_date (str, optional): The time at which the retention policy was created.
            expiration_date (str, optional): The time at which the retention policy will be expired.
        """
        super().__init__(**kwargs)
        self.worm_id = worm_id
        self.state = state
        self.retention_period_in_days = retention_period_in_days
        self.creation_date = creation_date
        self.expiration_date = expiration_date


class InitiateBucketWormRequest(serde.RequestModel):
    """
    The request for the InitiateBucketWorm operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'initiate_worm_configuration': {'tag': 'input', 'position': 'body', 'rename': 'InitiateWormConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        initiate_worm_configuration: Optional[InitiateWormConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            initiate_worm_configuration (InitiateWormConfiguration, optional): The container of the request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.initiate_worm_configuration = initiate_worm_configuration


class InitiateBucketWormResult(serde.ResultModel):
    """
    The request for the InitiateBucketWorm operation.
    """

    _attribute_map = { 
        'worm_id': {'tag': 'output', 'position': 'header', 'rename': 'x-oss-worm-id', 'type': 'str'},
    }

    def __init__(
        self,
        worm_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            worm_id (str, optional): <no value>
        """
        super().__init__(**kwargs)
        self.worm_id = worm_id

class AbortBucketWormRequest(serde.RequestModel):
    """
    The request for the AbortBucketWorm operation.
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


class AbortBucketWormResult(serde.ResultModel):
    """
    The request for the AbortBucketWorm operation.
    """

class CompleteBucketWormRequest(serde.RequestModel):
    """
    The request for the CompleteBucketWorm operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'worm_id': {'tag': 'input', 'position': 'query', 'rename': 'wormId', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        worm_id: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            worm_id (str, required): The ID of the retention policy.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.worm_id = worm_id


class CompleteBucketWormResult(serde.ResultModel):
    """
    The request for the CompleteBucketWorm operation.
    """

class ExtendBucketWormRequest(serde.RequestModel):
    """
    The request for the ExtendBucketWorm operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'worm_id': {'tag': 'input', 'position': 'query', 'rename': 'wormId', 'type': 'str', 'required': True},
        'extend_worm_configuration': {'tag': 'input', 'position': 'body', 'rename': 'ExtendWormConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        worm_id: str = None,
        extend_worm_configuration: Optional[ExtendWormConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            worm_id (str, required): The ID of the retention policy.  If the ID of the retention policy that specifies the number of days for which objects can be retained does not exist, the HTTP status code 404 is returned.
            extend_worm_configuration (ExtendWormConfiguration, optional): The container of the request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.worm_id = worm_id
        self.extend_worm_configuration = extend_worm_configuration


class ExtendBucketWormResult(serde.ResultModel):
    """
    The request for the ExtendBucketWorm operation.
    """

class GetBucketWormRequest(serde.RequestModel):
    """
    The request for the GetBucketWorm operation.
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


class GetBucketWormResult(serde.ResultModel):
    """
    The request for the GetBucketWorm operation.
    """

    _attribute_map = { 
        'worm_configuration': {'tag': 'output', 'position': 'body', 'rename': 'WormConfiguration', 'type': 'WormConfiguration,xml'},
    }

    _dependency_map = { 
        'WormConfiguration': {'new': lambda: WormConfiguration()},
    }

    def __init__(
        self,
        worm_configuration: Optional[WormConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            worm_configuration (WormConfiguration, optional): The container that stores the information about retention policies of the bucket.
        """
        super().__init__(**kwargs)
        self.worm_configuration = worm_configuration
