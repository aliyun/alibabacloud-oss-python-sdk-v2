import datetime
from dataclasses import dataclass
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


class GetPublicAccessBlockRequest(serde.RequestModel):
    """
    The request for the GetPublicAccessBlock operation.
    """

    _attribute_map = { 
    }

    def __init__(
        self,
        **kwargs: Any
    ) -> None:
        """
        """
        super().__init__(**kwargs)


class GetPublicAccessBlockResult(serde.ResultModel):
    """
    The request for the GetPublicAccessBlock operation.
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

@dataclass
class PutPublicAccessBlockRequest(serde.RequestModel):
    """
    The request for the PutPublicAccessBlock operation.
    """

    _attribute_map = { 
        'public_access_block_configuration': {'tag': 'input', 'position': 'body', 'rename': 'PublicAccessBlockConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            public_access_block_configuration (PublicAccessBlockConfiguration, optional): Request body.
        """
        super().__init__(**kwargs)
        self.public_access_block_configuration = public_access_block_configuration


class PutPublicAccessBlockResult(serde.ResultModel):
    """
    The request for the PutPublicAccessBlock operation.
    """

class DeletePublicAccessBlockRequest(serde.RequestModel):
    """
    The request for the DeletePublicAccessBlock operation.
    """

    _attribute_map = { 
    }

    def __init__(
        self,
        **kwargs: Any
    ) -> None:
        """
        """
        super().__init__(**kwargs)


class DeletePublicAccessBlockResult(serde.ResultModel):
    """
    The request for the DeletePublicAccessBlock operation.
    """
