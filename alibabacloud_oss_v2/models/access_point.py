import io
from typing import Optional, List, Any
from .. import serde, BodyType


class AccessPointVpcConfiguration(serde.Model):
    """
    The container that stores the information about the VPC.
    """

    _attribute_map = {
        'vpc_id': {'tag': 'xml', 'rename': 'VpcId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'VpcConfiguration'
    }

    def __init__(
        self,
        vpc_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            vpc_id (str, optional): The ID of the VPC that is required only when the NetworkOrigin parameter is set to vpc.
        """
        super().__init__(**kwargs)
        self.vpc_id = vpc_id

class CreateAccessPointConfiguration(serde.Model):
    """
    The container that stores the information about an access point.
    """

    _attribute_map = {
        'access_point_name': {'tag': 'xml', 'rename': 'AccessPointName', 'type': 'str'},
        'network_origin': {'tag': 'xml', 'rename': 'NetworkOrigin', 'type': 'str'},
        'vpc_configuration': {'tag': 'xml', 'rename': 'VpcConfiguration', 'type': 'AccessPointVpcConfiguration'},
    }

    _xml_map = {
        'name': 'CreateAccessPointConfiguration'
    }

    _dependency_map = {
        'AccessPointVpcConfiguration': {'new': lambda: AccessPointVpcConfiguration()},
    }

    def __init__(
        self,
        access_point_name: Optional[str] = None,
        network_origin: Optional[str] = None,
        vpc_configuration: Optional[AccessPointVpcConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            access_point_name (str, optional): The name of the access point. The name of the access point must meet the following naming rules:*   The name must be unique in a region of your Alibaba Cloud account.*   The name cannot end with -ossalias.*   The name can contain only lowercase letters, digits, and hyphens (-). It cannot start or end with a hyphen (-).*   The name must be 3 to 19 characters in length.
            network_origin (str, optional): The network origin of the access point.
            vpc_configuration (AccessPointVpcConfiguration, optional): The container that stores the information about the VPC.
        """
        super().__init__(**kwargs)
        self.access_point_name = access_point_name
        self.network_origin = network_origin
        self.vpc_configuration = vpc_configuration



class CreateAccessPointRequest(serde.RequestModel):
    """
    The request for the CreateAccessPoint operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'create_access_point_configuration': {'tag': 'input', 'position': 'body', 'rename': 'CreateAccessPointConfiguration', 'type': 'xml'},
    }

    def __init__(
            self,
            bucket: str = None,
            create_access_point_configuration: Optional[CreateAccessPointConfiguration] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            create_access_point_configuration (CreateAccessPointConfiguration, optional): The container of the request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.create_access_point_configuration = create_access_point_configuration


class CreateAccessPointResult(serde.ResultModel):
    """
    The request for the CreateAccessPoint operation.
    """

    _attribute_map = {
        'access_point_arn': {'tag': 'xml', 'rename': 'AccessPointArn', 'type': 'str'},
        'alias': {'tag': 'xml', 'rename': 'Alias', 'type': 'str'},
    }

    _xml_map = {
        'name': 'CreateAccessPointResult'
    }

    def __init__(
            self,
            access_point_arn: Optional[str] = None,
            alias: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            access_point_arn (str, optional): The Alibaba Cloud Resource Name (ARN) of the access point.
            alias (str, optional): The alias of the access point.
        """
        super().__init__(**kwargs)
        self.access_point_arn = access_point_arn
        self.alias = alias

class Endpoints(serde.Model):
    """
    The container that stores the network origin information about the access point.
    """

    _attribute_map = {
        'public_endpoint': {'tag': 'xml', 'rename': 'PublicEndpoint', 'type': 'str'},
        'internal_endpoint': {'tag': 'xml', 'rename': 'InternalEndpoint', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Endpoints'
    }

    def __init__(
        self,
        public_endpoint: Optional[str] = None,
        internal_endpoint: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            public_endpoint (str, optional): The public endpoint of the access point.
            internal_endpoint (str, optional): 接入点的内网Endpoint。
        """
        super().__init__(**kwargs)
        self.public_endpoint = public_endpoint
        self.internal_endpoint = internal_endpoint


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


class GetAccessPointRequest(serde.RequestModel):
    """
    The request for the GetAccessPoint operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-name', 'type': 'str', 'required': True},
    }

    def __init__(
            self,
            bucket: str = None,
            access_point_name: str = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            access_point_name (str, required): The name of the access point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_name = access_point_name


class GetAccessPointResult(serde.ResultModel):
    """
    The request for the GetAccessPoint operation.
    """

    _attribute_map = {
        'account_id': {'tag': 'xml', 'rename': 'AccountId', 'type': 'str'},
        'network_origin': {'tag': 'xml', 'rename': 'NetworkOrigin', 'type': 'str'},
        'access_point_arn': {'tag': 'xml', 'rename': 'AccessPointArn', 'type': 'str'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'creation_date': {'tag': 'xml', 'rename': 'CreationDate', 'type': 'str'},
        'access_point_name': {'tag': 'xml', 'rename': 'AccessPointName', 'type': 'str'},
        'bucket': {'tag': 'xml', 'rename': 'Bucket', 'type': 'str'},
        'endpoints': {'tag': 'xml', 'rename': 'Endpoints', 'type': 'Endpoints'},
        'public_access_block_configuration': {'tag': 'xml', 'rename': 'PublicAccessBlockConfiguration', 'type': 'PublicAccessBlockConfiguration'},
        'vpc_configuration': {'tag': 'xml', 'rename': 'VpcConfiguration', 'type': 'AccessPointVpcConfiguration'},
        'alias': {'tag': 'xml', 'rename': 'Alias', 'type': 'str'},
    }

    _xml_map = {
        'name': 'GetAccessPointResult'
    }

    _dependency_map = {
        'Endpoints': {'new': lambda: Endpoints()},
        'PublicAccessBlockConfiguration': {'new': lambda: PublicAccessBlockConfiguration()},
        'AccessPointVpcConfiguration': {'new': lambda: AccessPointVpcConfiguration()},
    }

    def __init__(
            self,
            account_id: Optional[str] = None,
            network_origin: Optional[str] = None,
            access_point_arn: Optional[str] = None,
            status: Optional[str] = None,
            creation_date: Optional[str] = None,
            access_point_name: Optional[str] = None,
            bucket: Optional[str] = None,
            endpoints: Optional[Endpoints] = None,
            public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None,
            vpc_configuration: Optional[AccessPointVpcConfiguration] = None,
            alias: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            account_id (str, optional): The ID of the Alibaba Cloud account for which the access point is configured.
            network_origin (str, optional): The network origin of the access point. Valid values: vpc and internet. vpc: You can only use the specified VPC ID to access the access point. internet: You can use public endpoints and internal endpoints to access the access point.
            access_point_arn (str, optional): The ARN of the access point.
            status (str, optional): The status of the access point.
            creation_date (str, optional): 接入点创建时间。
            access_point_name (str, optional): The name of the access point.
            bucket (str, optional): The name of the bucket for which the access point is configured.
            endpoints (Endpoints, optional): The container that stores the network origin information about the access point.
            public_access_block_configuration (PublicAccessBlockConfiguration, optional): 保存接入点阻止公共访问的配置
            vpc_configuration (AccessPointVpcConfiguration, optional): The container that stores the information about the VPC.
            alias (str, optional): The alias of the access point.
        """
        super().__init__(**kwargs)
        self.account_id = account_id
        self.network_origin = network_origin
        self.access_point_arn = access_point_arn
        self.status = status
        self.creation_date = creation_date
        self.access_point_name = access_point_name
        self.bucket = bucket
        self.endpoints = endpoints
        self.public_access_block_configuration = public_access_block_configuration
        self.vpc_configuration = vpc_configuration
        self.alias = alias


class AccessPoint(serde.Model):
    """
    The container that stores the information about an access point.
    """

    _attribute_map = {
        'network_origin': {'tag': 'xml', 'rename': 'NetworkOrigin', 'type': 'str'},
        'vpc_configuration': {'tag': 'xml', 'rename': 'VpcConfiguration', 'type': 'AccessPointVpcConfiguration'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'bucket': {'tag': 'xml', 'rename': 'Bucket', 'type': 'str'},
        'access_point_name': {'tag': 'xml', 'rename': 'AccessPointName', 'type': 'str'},
        'alias': {'tag': 'xml', 'rename': 'Alias', 'type': 'str'},
    }

    _xml_map = {
        'name': 'AccessPoint'
    }

    _dependency_map = {
        'AccessPointVpcConfiguration': {'new': lambda: AccessPointVpcConfiguration()},
    }

    def __init__(
        self,
        network_origin: Optional[str] = None,
        vpc_configuration: Optional[AccessPointVpcConfiguration] = None,
        status: Optional[str] = None,
        bucket: Optional[str] = None,
        access_point_name: Optional[str] = None,
        alias: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            network_origin (str, optional): The network origin of the access point.
            vpc_configuration (AccessPointVpcConfiguration, optional): The container that stores the information about the VPC.
            status (str, optional): The status of the access point.
            bucket (str, optional): The name of the bucket for which the access point is configured.
            access_point_name (str, optional): The name of the access point.
            alias (str, optional): The alias of the access point.
        """
        super().__init__(**kwargs)
        self.network_origin = network_origin
        self.vpc_configuration = vpc_configuration
        self.status = status
        self.bucket = bucket
        self.access_point_name = access_point_name
        self.alias = alias



class ListAccessPointsRequest(serde.RequestModel):
    """
    The request for the ListAccessPoints operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str'},
        'max_keys': {'tag': 'input', 'position': 'query', 'rename': 'max-keys', 'type': 'int'},
        'continuation_token': {'tag': 'input', 'position': 'query', 'rename': 'continuation-token', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        max_keys: Optional[int] = None,
        continuation_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            max_keys (int, optional): The maximum number of access points that can be returned. Valid values:*   For user-level access points: (0,1000].*   For bucket-level access points: (0,100].
            continuation_token (str, optional): The token from which the listing operation starts. You must specify the value of NextContinuationToken that is obtained from the previous query as the value of continuation-token.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.max_keys = max_keys
        self.continuation_token = continuation_token


class ListAccessPointsResult(serde.ResultModel):
    """
    The request for the ListAccessPoints operation.
    """

    _attribute_map = {
        'access_points': {'tag': 'xml', 'rename': 'AccessPoints/AccessPoint', 'type': '[AccessPoint]'},
        'max_keys': {'tag': 'xml', 'rename': 'MaxKeys', 'type': 'int'},
        'is_truncated': {'tag': 'xml', 'rename': 'IsTruncated', 'type': 'bool'},
        'next_continuation_token': {'tag': 'xml', 'rename': 'NextContinuationToken', 'type': 'str'},
        'account_id': {'tag': 'xml', 'rename': 'AccountId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ListAccessPointsResult'
    }

    _dependency_map = {
        'AccessPoint': {'new': lambda: AccessPoint()},
    }


    def __init__(
        self,
        access_points: Optional[List[AccessPoint]] = None,
        max_keys: Optional[int] = None,
        is_truncated: Optional[bool] = None,
        next_continuation_token: Optional[str] = None,
        account_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            access_points (List[AccessPoint], optional): The container that stores the information about all access point.
            max_keys (int, optional): The maximum number of results set for this enumeration operation.
            is_truncated (str, bool): Indicates whether the returned list is truncated. Valid values: * true: indicates that not all results are returned. * false: indicates that all results are returned.
            next_continuation_token (str, optional): Indicates that this ListAccessPoints request does not return all results that can be listed. You can use NextContinuationToken to continue obtaining list results.
            account_id (str, optional): The ID of the Alibaba Cloud account to which the access point belongs.
        """
        super().__init__(**kwargs)
        self.access_points = access_points
        self.max_keys = max_keys
        self.is_truncated = is_truncated
        self.next_continuation_token = next_continuation_token
        self.account_id = account_id


class DeleteAccessPointRequest(serde.RequestModel):
    """
    The request for the DeleteAccessPoint operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-name', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            access_point_name (str, required): The name of the access point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_name = access_point_name


class DeleteAccessPointResult(serde.ResultModel):
    """
    The request for the DeleteAccessPoint operation.
    """


class PutAccessPointPolicyRequest(serde.RequestModel):
    """
    The request for the PutAccessPointPolicy operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-name', 'type': 'str'},
        'body': {'tag': 'input', 'position': 'body', 'rename': 'nop'},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_name: Optional[str] = None,
        body: Optional[BodyType] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            access_point_name (str, optional): The name of the access point.
            body (BodyType, optional): The configurations of the access point policy.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_name = access_point_name
        self.body = body


class PutAccessPointPolicyResult(serde.ResultModel):
    """
    The request for the PutAccessPointPolicy operation.
    """

class GetAccessPointPolicyRequest(serde.RequestModel):
    """
    The request for the GetAccessPointPolicy operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-name', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            access_point_name (str, required): The name of the access point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_name = access_point_name


class GetAccessPointPolicyResult(serde.ResultModel):
    """
    The request for the GetAccessPointPolicy operation.
    """

    _attribute_map = { 
        'body': {'tag': 'output', 'position': 'body', 'type': 'str'},
    }

    def __init__(
        self,
        body: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            body (io.ReadCloser, optional): <no value>
        """
        super().__init__(**kwargs)
        self.body = body

class DeleteAccessPointPolicyRequest(serde.RequestModel):
    """
    The request for the DeleteAccessPointPolicy operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-name', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            access_point_name (str, required): The name of the access point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_name = access_point_name


class DeleteAccessPointPolicyResult(serde.ResultModel):
    """
    The request for the DeleteAccessPointPolicy operation.
    """
