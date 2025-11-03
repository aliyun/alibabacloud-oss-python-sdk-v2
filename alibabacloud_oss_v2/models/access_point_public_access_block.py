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


class PutAccessPointPublicAccessBlockRequest(serde.RequestModel):
    """
    The request for the PutAccessPointPublicAccessBlock operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_name': {'tag': 'input', 'position': 'query', 'rename': 'x-oss-access-point-name', 'type': 'str', 'required': True},
        'public_access_block_configuration': {'tag': 'input', 'position': 'body', 'rename': 'PublicAccessBlockConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_name: str = None,
        public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            access_point_name (str, required): The name of the access point.
            public_access_block_configuration (PublicAccessBlockConfiguration, optional): The request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_name = access_point_name
        self.public_access_block_configuration = public_access_block_configuration


class PutAccessPointPublicAccessBlockResult(serde.ResultModel):
    """
    The request for the PutAccessPointPublicAccessBlock operation.
    """


class GetAccessPointPublicAccessBlockRequest(serde.RequestModel):
    """
    The request for the GetAccessPointPublicAccessBlock operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_name': {'tag': 'input', 'position': 'query', 'rename': 'x-oss-access-point-name', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            access_point_name (str, optional): The name of the access point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_name = access_point_name


class GetAccessPointPublicAccessBlockResult(serde.ResultModel):
    """
    The request for the GetAccessPointPublicAccessBlock operation.
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


class DeleteAccessPointPublicAccessBlockRequest(serde.RequestModel):
    """
    The request for the DeleteAccessPointPublicAccessBlock operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_name': {'tag': 'input', 'position': 'query', 'rename': 'x-oss-access-point-name', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            access_point_name (str, optional): The name of the access point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_name = access_point_name


class DeleteAccessPointPublicAccessBlockResult(serde.ResultModel):
    """
    The request for the DeleteAccessPointPublicAccessBlock operation.
    """
