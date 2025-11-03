import datetime
from typing import Optional, List, Any, Union
from .. import serde


class PublicAccessBlockConfiguration(serde.Model):
    """
    The container in which the Block Public Access configurations are stored.
    """

    _attribute_map = { 
        'block_public_access': {'tag': 'xml', 'rename': 'BlockPublicAccess', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'PublicAccessBlockConfiguration'
    }

    def __init__(
        self,
        block_public_access: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            block_public_access (bool, optional): Specifies whether to enable Block Public Access.true: enables Block Public Access.false (default): disables Block Public Access.
        """
        super().__init__(**kwargs)
        self.block_public_access = block_public_access




class GetBucketPublicAccessBlockRequest(serde.RequestModel):
    """
    The request for the GetBucketPublicAccessBlock operation.
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
            bucket (str, required):
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetBucketPublicAccessBlockResult(serde.ResultModel):
    """
    The request for the GetBucketPublicAccessBlock operation.
    """

    _attribute_map = { 
        'public_access_block_configuration': {'tag': 'output', 'position': 'body', 'rename': 'PublicAccessBlockConfiguration', 'type': 'PublicAccessBlockConfiguration,xml'},
    }

    _dependency_map = { 
        'PublicAccessBlockConfiguration': {'new': lambda: PublicAccessBlockConfiguration()},
    }

    def __init__(
        self,
        public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            public_access_block_configuration (PublicAccessBlockConfiguration, optional): The container in which the Block Public Access configurations are stored.
        """
        super().__init__(**kwargs)
        self.public_access_block_configuration = public_access_block_configuration

class PutBucketPublicAccessBlockRequest(serde.RequestModel):
    """
    The request for the PutBucketPublicAccessBlock operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'public_access_block_configuration': {'tag': 'input', 'position': 'body', 'rename': 'PublicAccessBlockConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            public_access_block_configuration (PublicAccessBlockConfiguration, optional): Request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.public_access_block_configuration = public_access_block_configuration


class PutBucketPublicAccessBlockResult(serde.ResultModel):
    """
    The request for the PutBucketPublicAccessBlock operation.
    """

class DeleteBucketPublicAccessBlockRequest(serde.RequestModel):
    """
    The request for the DeleteBucketPublicAccessBlock operation.
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


class DeleteBucketPublicAccessBlockResult(serde.ResultModel):
    """
    The request for the DeleteBucketPublicAccessBlock operation.
    """
