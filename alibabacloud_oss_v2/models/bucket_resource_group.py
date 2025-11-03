import datetime
from typing import Optional, List, Any, Union
from .. import serde


class BucketResourceGroupConfiguration(serde.Model):
    """
    The configurations of the resource group to which the bucket belongs.
    """

    _attribute_map = { 
        'resource_group_id': {'tag': 'xml', 'rename': 'ResourceGroupId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'BucketResourceGroupConfiguration'
    }

    def __init__(
        self,
        resource_group_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            resource_group_id (str, optional): The ID of the resource group to which the bucket belongs.
        """
        super().__init__(**kwargs)
        self.resource_group_id = resource_group_id




class GetBucketResourceGroupRequest(serde.RequestModel):
    """
    The request for the GetBucketResourceGroup operation.
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
            bucket (str, required): The name of the bucket that you want to query.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetBucketResourceGroupResult(serde.ResultModel):
    """
    The request for the GetBucketResourceGroup operation.
    """

    _attribute_map = { 
        'bucket_resource_group_configuration': {'tag': 'output', 'position': 'body', 'rename': 'BucketResourceGroupConfiguration', 'type': 'BucketResourceGroupConfiguration,xml'},
    }

    _dependency_map = { 
        'BucketResourceGroupConfiguration': {'new': lambda: BucketResourceGroupConfiguration()},
    }

    def __init__(
        self,
        bucket_resource_group_configuration: Optional[BucketResourceGroupConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket_resource_group_configuration (BucketResourceGroupConfiguration, optional): The container that stores the ID of the resource group.
        """
        super().__init__(**kwargs)
        self.bucket_resource_group_configuration = bucket_resource_group_configuration

class PutBucketResourceGroupRequest(serde.RequestModel):
    """
    The request for the PutBucketResourceGroup operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'bucket_resource_group_configuration': {'tag': 'input', 'position': 'body', 'rename': 'BucketResourceGroupConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        bucket_resource_group_configuration: Optional[BucketResourceGroupConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The bucket for which you want to modify the ID of the resource group.
            bucket_resource_group_configuration (BucketResourceGroupConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.bucket_resource_group_configuration = bucket_resource_group_configuration


class PutBucketResourceGroupResult(serde.ResultModel):
    """
    The request for the PutBucketResourceGroup operation.
    """
