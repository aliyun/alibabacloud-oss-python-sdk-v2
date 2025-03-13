import datetime
from typing import Optional, List, Any, Union
from .. import serde


class TransferAccelerationConfiguration(serde.Model):
    """
    The container that stores the transfer acceleration configurations.
    """

    _attribute_map = { 
        'enabled': {'tag': 'xml', 'rename': 'Enabled', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'TransferAccelerationConfiguration'
    }

    def __init__(
        self,
        enabled: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            enabled (bool, optional): Whether the transfer acceleration is enabled for this bucket.
        """
        super().__init__(**kwargs)
        self.enabled = enabled




class PutBucketTransferAccelerationRequest(serde.RequestModel):
    """
    The request for the PutBucketTransferAcceleration operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'transfer_acceleration_configuration': {'tag': 'input', 'position': 'body', 'rename': 'TransferAccelerationConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        transfer_acceleration_configuration: Optional[TransferAccelerationConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            transfer_acceleration_configuration (TransferAccelerationConfiguration, optional): The container of the request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.transfer_acceleration_configuration = transfer_acceleration_configuration


class PutBucketTransferAccelerationResult(serde.ResultModel):
    """
    The request for the PutBucketTransferAcceleration operation.
    """

class GetBucketTransferAccelerationRequest(serde.RequestModel):
    """
    The request for the GetBucketTransferAcceleration operation.
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


class GetBucketTransferAccelerationResult(serde.ResultModel):
    """
    The request for the GetBucketTransferAcceleration operation.
    """

    _attribute_map = { 
        'transfer_acceleration_configuration': {'tag': 'output', 'position': 'body', 'rename': 'TransferAccelerationConfiguration', 'type': 'TransferAccelerationConfiguration,xml'},
    }

    _dependency_map = { 
        'TransferAccelerationConfiguration': {'new': lambda: TransferAccelerationConfiguration()},
    }

    def __init__(
        self,
        transfer_acceleration_configuration: Optional[TransferAccelerationConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            transfer_acceleration_configuration (TransferAccelerationConfiguration, optional): The container that stores the transfer acceleration configurations.
        """
        super().__init__(**kwargs)
        self.transfer_acceleration_configuration = transfer_acceleration_configuration
