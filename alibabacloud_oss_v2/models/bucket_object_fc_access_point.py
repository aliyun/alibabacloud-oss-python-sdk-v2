import datetime
from typing import Optional, List, Any, Union
from .. import serde


class FunctionCompute(serde.Model):
    """
    The container that stores the information about Function Compute.
    """

    _attribute_map = { 
        'function_assume_role_arn': {'tag': 'xml', 'rename': 'FunctionAssumeRoleArn', 'type': 'str'},
        'function_arn': {'tag': 'xml', 'rename': 'FunctionArn', 'type': 'str'},
    }

    _xml_map = {
        'name': 'FunctionCompute'
    }

    def __init__(
        self,
        function_assume_role_arn: Optional[str] = None,
        function_arn: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        function_assume_role_arn (str, optional): The Alibaba Cloud Resource Name (ARN) of the role that Function Compute uses to access your resources in other cloud services. The default role is AliyunFCDefaultRole.
        function_arn (str, optional): The ARN of the function.
        """
        super().__init__(**kwargs)
        self.function_assume_role_arn = function_assume_role_arn
        self.function_arn = function_arn


class CustomForwardHeaders(serde.Model):
    """

    """

    _attribute_map = {
        'custom_forward_headers': {'tag': 'xml', 'rename': 'CustomForwardHeader', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'CustomForwardHeaders'
    }

    def __init__(
        self,
        custom_forward_headers: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        custom_forward_headers (List[str], optional):
        """
        super().__init__(**kwargs)
        self.custom_forward_headers = custom_forward_headers


class AccessPointForObjectProcess(serde.Model):
    """
    The container that stores information about a single Object FC Access Point.
    """

    _attribute_map = { 
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'allow_anonymous_access_for_object_process': {'tag': 'xml', 'rename': 'AllowAnonymousAccessForObjectProcess', 'type': 'str'},
        'access_point_name_for_object_process': {'tag': 'xml', 'rename': 'AccessPointNameForObjectProcess', 'type': 'str'},
        'access_point_for_object_process_alias': {'tag': 'xml', 'rename': 'AccessPointForObjectProcessAlias', 'type': 'str'},
        'access_point_name': {'tag': 'xml', 'rename': 'AccessPointName', 'type': 'str'},
    }

    _xml_map = {
        'name': 'AccessPointForObjectProcess'
    }


    def __init__(
        self,
        status: Optional[str] = None,
        allow_anonymous_access_for_object_process: Optional[str] = None,
        access_point_name_for_object_process: Optional[str] = None,
        access_point_for_object_process_alias: Optional[str] = None,
        access_point_name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        status (str, optional): The status of the Object FC Access Point. Valid values:enable: The Object FC Access Point is created.disable: The Object FC Access Point is disabled.creating: The Object FC Access Point is being created.deleting: The Object FC Access Point is deleted.
        allow_anonymous_access_for_object_process (str, optional): Whether allow anonymous user access this FC Access Point.
        access_point_name_for_object_process (str, optional): The name of the Object FC Access Point.
        access_point_for_object_process_alias (str, optional): The alias of the Object FC Access Point.
        access_point_name (str, optional): The name of the access point.
        """
        super().__init__(**kwargs)
        self.status = status
        self.allow_anonymous_access_for_object_process = allow_anonymous_access_for_object_process
        self.access_point_name_for_object_process = access_point_name_for_object_process
        self.access_point_for_object_process_alias = access_point_for_object_process_alias
        self.access_point_name = access_point_name


class AllowedFeatures(serde.Model):
    """
    The container that stores allowed features.
    """

    _attribute_map = {
        'allowed_features': {'tag': 'xml', 'rename': 'AllowedFeature', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'AllowedFeatures'
    }

    def __init__(
        self,
        allowed_features: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        allowed_features (List[str], optional): Specifies that Function Compute supports Range GetObject requests.
        """
        super().__init__(**kwargs)
        self.allowed_features = allowed_features


class AccessPointActions(serde.Model):
    """
    The container that stores the operations.
    """

    _attribute_map = {
        'actions': {'tag': 'xml', 'rename': 'Action', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'Actions'
    }

    def __init__(
        self,
        actions: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        actions (List[str], optional): The supported OSS API operations. Only the GetObject operation is supported.
        """
        super().__init__(**kwargs)
        self.actions = actions


class AccessPointEndpoints(serde.Model):
    """
    The container that stores the endpoints of the Object FC Access Point.
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
        public_endpoint (str, optional): The public endpoint of the Object FC Access Point.
        internal_endpoint (str, optional): The internal endpoint of the Object FC Access Point.
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
        block_public_access (bool, optional): Specifies whether to enable Block Public Access.true: enables Block Public Access.false (default): disables Block Public Access.
        """
        super().__init__(**kwargs)
        self.block_public_access = block_public_access


class AdditionalFeatures(serde.Model):
    """

    """

    _attribute_map = {
        'custom_forward_headers': {'tag': 'xml', 'rename': 'CustomForwardHeaders', 'type': 'CustomForwardHeaders'},
    }

    _xml_map = {
        'name': 'AdditionalFeatures'
    }

    _dependency_map = {
        'CustomForwardHeaders': {'new': lambda: CustomForwardHeaders()},
    }

    def __init__(
            self,
            custom_forward_headers: Optional[CustomForwardHeaders] = None,
            **kwargs: Any
    ) -> None:
        """
        custom_forward_headers (CustomForwardHeaders, optional):
        """
        super().__init__(**kwargs)
        self.custom_forward_headers = custom_forward_headers


class ContentTransformation(serde.Model):
    """
    The container that stores the content of the transformation configurations.
    """

    _attribute_map = { 
        'function_compute': {'tag': 'xml', 'rename': 'FunctionCompute', 'type': 'FunctionCompute'},
        'additional_features': {'tag': 'xml', 'rename': 'AdditionalFeatures', 'type': 'AdditionalFeatures'},
    }

    _xml_map = {
        'name': 'ContentTransformation'
    }

    _dependency_map = { 
        'FunctionCompute': {'new': lambda: FunctionCompute()},
        'AdditionalFeatures': {'new': lambda: AdditionalFeatures()},
    }

    def __init__(
        self,
        function_compute: Optional[FunctionCompute] = None,
        additional_features: Optional[AdditionalFeatures] = None,
        **kwargs: Any
    ) -> None:
        """
        function_compute (FunctionCompute, optional): The container that stores the information about Function Compute.
        additional_features (AdditionalFeatures, optional): 
        """
        super().__init__(**kwargs)
        self.function_compute = function_compute
        self.additional_features = additional_features


class TransformationConfiguration(serde.Model):
    """
    The container that stores the transformation configurations.
    """

    _attribute_map = {
        'actions': {'tag': 'xml', 'rename': 'Actions', 'type': 'Actions'},
        'content_transformation': {'tag': 'xml', 'rename': 'ContentTransformation', 'type': 'ContentTransformation'},
    }

    _xml_map = {
        'name': 'TransformationConfiguration'
    }

    _dependency_map = {
        'Actions': {'new': lambda: AccessPointActions()},
        'ContentTransformation': {'new': lambda: ContentTransformation()},
    }

    def __init__(
        self,
        actions: Optional[AccessPointActions] = None,
        content_transformation: Optional[ContentTransformation] = None,
        **kwargs: Any
    ) -> None:
        """
        actions (Actions, optional): The container that stores the operations.
        content_transformation (ContentTransformation, optional): The container that stores the content of the transformation configurations.
        """
        super().__init__(**kwargs)
        self.actions = actions
        self.content_transformation = content_transformation


class TransformationConfigurations(serde.Model):
    """
    The container that stores the transformation configurations.
    """

    _attribute_map = {
        'transformation_configurations': {'tag': 'xml', 'rename': 'TransformationConfiguration', 'type': '[TransformationConfiguration]'},
    }

    _xml_map = {
        'name': 'TransformationConfigurations'
    }

    _dependency_map = {
        'TransformationConfiguration': {'new': lambda: TransformationConfiguration()},
    }

    def __init__(
        self,
        transformation_configurations: Optional[List[TransformationConfiguration]] = None,
        **kwargs: Any
    ) -> None:
        """
        transformation_configurations (List[TransformationConfiguration], optional): The container that stores the transformation configurations.
        """
        super().__init__(**kwargs)
        self.transformation_configurations = transformation_configurations


class AccessPointsForObjectProcess(serde.Model):
    """
    The container that stores information about all Object FC Access Points.
    """

    _attribute_map = { 
        'access_point_for_object_processs': {'tag': 'xml', 'rename': 'AccessPointForObjectProcess', 'type': '[AccessPointForObjectProcess]'},
    }

    _xml_map = {
        'name': 'AccessPointsForObjectProcess'
    }

    _dependency_map = {
        'AccessPointForObjectProcess': {'new': lambda: AccessPointForObjectProcess()},
    }

    def __init__(
        self,
        access_point_for_object_processs: Optional[List[AccessPointForObjectProcess]] = None,
        **kwargs: Any
    ) -> None:
        """
        access_point_for_object_processs (List[AccessPointForObjectProcess], optional): The container that stores information about a single Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.access_point_for_object_processs = access_point_for_object_processs


class ObjectProcessConfiguration(serde.Model):
    """
    The container that stores the processing information about the Object FC Access Point.
    """

    _attribute_map = { 
        'allowed_features': {'tag': 'xml', 'rename': 'AllowedFeatures', 'type': 'AllowedFeatures'},
        'transformation_configurations': {'tag': 'xml', 'rename': 'TransformationConfigurations', 'type': 'TransformationConfigurations'},
    }

    _xml_map = {
        'name': 'ObjectProcessConfiguration'
    }

    _dependency_map = {
        'AllowedFeatures': {'new': lambda: AllowedFeatures()},
        'TransformationConfigurations': {'new': lambda: TransformationConfigurations()},
    }

    def __init__(
        self,
        allowed_features: Optional[AllowedFeatures] = None,
        transformation_configurations: Optional[TransformationConfigurations] = None,
        **kwargs: Any
    ) -> None:
        """
        allowed_features (AllowedFeatures, optional): The container that stores allowed features.
        transformation_configurations (TransformationConfigurations, optional): The container that stores the transformation configurations.
        """
        super().__init__(**kwargs)
        self.allowed_features = allowed_features
        self.transformation_configurations = transformation_configurations


class PutAccessPointConfigForObjectProcessConfiguration(serde.Model):
    """
    The container that stores the processing information about the Object Access Point Config.
    """

    _attribute_map = {
        'allow_anonymous_access_for_object_process': {'tag': 'xml', 'rename': 'AllowAnonymousAccessForObjectProcess', 'type': 'str'},
        'public_access_block_configuration': {'tag': 'xml', 'rename': 'PublicAccessBlockConfiguration', 'type': 'PublicAccessBlockConfiguration'},
        'object_process_configuration': {'tag': 'xml', 'rename': 'ObjectProcessConfiguration', 'type': 'ObjectProcessConfiguration'},
    }

    _xml_map = {
        'name': 'PutAccessPointConfigForObjectProcessConfiguration'
    }

    _dependency_map = {
        'PublicAccessBlockConfiguration': {'new': lambda: PublicAccessBlockConfiguration()},
        'ObjectProcessConfiguration': {'new': lambda: ObjectProcessConfiguration()},
    }

    def __init__(
        self,
        allow_anonymous_access_for_object_process: Optional[str] = None,
        public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None,
        object_process_configuration: Optional[ObjectProcessConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        allow_anonymous_access_for_object_process (str, optional): Whether allow anonymous user to access this FC Access Point.
        public_access_block_configuration (PublicAccessBlockConfiguration, optional): The container in which the Block Public Access configurations are stored.
        object_process_configuration (ObjectProcessConfiguration, optional): The container that stores the processing information about the Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.allow_anonymous_access_for_object_process = allow_anonymous_access_for_object_process
        self.public_access_block_configuration = public_access_block_configuration
        self.object_process_configuration = object_process_configuration


class CreateAccessPointForObjectProcessConfiguration(serde.Model):
    """
    The container that stores the processing information about the Object Access Point Config.
    """

    _attribute_map = {
        'allow_anonymous_access_for_object_process': {'tag': 'xml', 'rename': 'AllowAnonymousAccessForObjectProcess', 'type': 'str'},
        'access_point_name': {'tag': 'xml', 'rename': 'AccessPointName', 'type': 'str'},
        'object_process_configuration': {'tag': 'xml', 'rename': 'ObjectProcessConfiguration', 'type': 'ObjectProcessConfiguration'},
    }

    _xml_map = {
        'name': 'CreateAccessPointForObjectProcessConfiguration'
    }

    _dependency_map = {
        'ObjectProcessConfiguration': {'new': lambda: ObjectProcessConfiguration()},
    }

    def __init__(
        self,
        allow_anonymous_access_for_object_process: Optional[str] = None,
        access_point_name: Optional[str] = None,
        object_process_configuration: Optional[ObjectProcessConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        allow_anonymous_access_for_object_process (str, optional): Whether allow anonymous user to access this FC Access Point.
        access_point_name (str, optional): The name of the access point.
        object_process_configuration (ObjectProcessConfiguration, optional): The container that stores the processing information about the Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.allow_anonymous_access_for_object_process = allow_anonymous_access_for_object_process
        self.access_point_name = access_point_name
        self.object_process_configuration = object_process_configuration





class CreateAccessPointForObjectProcessRequest(serde.RequestModel):
    """
    The request for the CreateAccessPointForObjectProcess operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_for_object_process_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-for-object-process-name', 'type': 'str', 'required': True},
        'create_access_point_for_object_process_configuration': {'tag': 'input', 'position': 'body', 'rename': 'CreateAccessPointForObjectProcessConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_for_object_process_name: str = None,
        create_access_point_for_object_process_configuration: Optional[CreateAccessPointForObjectProcessConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        access_point_for_object_process_name (str, required): The name of the Object FC Access Point.
        create_access_point_for_object_process_configuration (CreateAccessPointForObjectProcessConfiguration, optional): The request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_for_object_process_name = access_point_for_object_process_name
        self.create_access_point_for_object_process_configuration = create_access_point_for_object_process_configuration


class CreateAccessPointForObjectProcessResult(serde.ResultModel):
    """
    The request for the CreateAccessPointForObjectProcess operation.
    """

    _attribute_map = { 
        'access_point_for_object_process_alias': {'tag': 'xml', 'rename': 'AccessPointForObjectProcessAlias', 'type': 'str,xml'},
        'access_point_for_object_process_arn': {'tag': 'xml', 'rename': 'AccessPointForObjectProcessArn', 'type': 'str,xml'},
    }

    def __init__(
        self,
        access_point_for_object_process_alias: Optional[str] = None,
        access_point_for_object_process_arn: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        access_point_for_object_process_alias (str, optional): The alias of the Object FC Access Point.
        access_point_for_object_process_arn (str, optional): The ARN of the Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.access_point_for_object_process_alias = access_point_for_object_process_alias
        self.access_point_for_object_process_arn = access_point_for_object_process_arn

class GetAccessPointForObjectProcessRequest(serde.RequestModel):
    """
    The request for the GetAccessPointForObjectProcess operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_for_object_process_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-for-object-process-name', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_for_object_process_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        access_point_for_object_process_name (str, required): The name of the Object FC Access Point. The name of an Object FC Access Point must meet the following requirements:The name cannot exceed 63 characters in length.The name can contain only lowercase letters, digits, and hyphens (-) and cannot start or end with a hyphen (-).The name must be unique in the current region.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_for_object_process_name = access_point_for_object_process_name


class GetAccessPointForObjectProcessResult(serde.ResultModel):
    """
    The request for the GetAccessPointForObjectProcess operation.
    """

    _attribute_map = { 
        'access_point_name_for_object_process': {'tag': 'xml', 'rename': 'AccessPointNameForObjectProcess', 'type': 'str,xml'},
        'access_point_for_object_process_alias': {'tag': 'xml', 'rename': 'AccessPointForObjectProcessAlias', 'type': 'str,xml'},
        'account_id': {'tag': 'xml', 'rename': 'AccountId', 'type': 'str,xml'},
        'access_point_for_object_process_arn': {'tag': 'xml', 'rename': 'AccessPointForObjectProcessArn', 'type': 'str,xml'},
        'fc_status': {'tag': 'xml', 'rename': 'Status', 'type': 'str,xml'},
        'access_point_name': {'tag': 'xml', 'rename': 'AccessPointName', 'type': 'str,xml'},
        'creation_date': {'tag': 'xml', 'rename': 'CreationDate', 'type': 'str,xml'},
        'endpoints': {'tag': 'xml', 'rename': 'Endpoints', 'type': 'Endpoints,xml'},
        'allow_anonymous_access_for_object_process': {'tag': 'xml', 'rename': 'AllowAnonymousAccessForObjectProcess', 'type': 'str,xml'},
        'public_access_block_configuration': {'tag': 'xml', 'rename': 'PublicAccessBlockConfiguration', 'type': 'PublicAccessBlockConfiguration,xml'},
    }

    _dependency_map = { 
        'Endpoints': {'new': lambda: AccessPointEndpoints()},
        'PublicAccessBlockConfiguration': {'new': lambda: PublicAccessBlockConfiguration()},
    }

    def __init__(
        self,
        access_point_name_for_object_process: Optional[str] = None,
        access_point_for_object_process_alias: Optional[str] = None,
        account_id: Optional[str] = None,
        access_point_for_object_process_arn: Optional[str] = None,
        fc_status: Optional[str] = None,
        access_point_name: Optional[str] = None,
        creation_date: Optional[str] = None,
        endpoints: Optional[AccessPointEndpoints] = None,
        allow_anonymous_access_for_object_process: Optional[str] = None,
        public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        access_point_name_for_object_process (str, optional): The name of the Object FC Access Point.
        access_point_for_object_process_alias (str, optional): The alias of the Object FC Access Point.
        account_id (str, optional): The public endpoint of the Object FC Access Point.
        access_point_for_object_process_arn (str, optional): The ARN of the Object FC Access Point.
        fc_status (str, optional): The status of the Object FC Access Point. Valid values:enable: The Object FC Access Point is created.disable: The Object FC Access Point is disabled.creating: The Object FC Access Point is being created.deleting: The Object FC Access Point is deleted.
        access_point_name (str, optional): The name of the access point.
        creation_date (str, optional): The time when the Object FC Access Point was created. The value is a timestamp.
        endpoints (Endpoints, optional): <no value>
        allow_anonymous_access_for_object_process (str, optional): Whether allow anonymous users to access this FC Access Point.
        public_access_block_configuration (PublicAccessBlockConfiguration, optional): The public endpoint of the Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.access_point_name_for_object_process = access_point_name_for_object_process
        self.access_point_for_object_process_alias = access_point_for_object_process_alias
        self.account_id = account_id
        self.access_point_for_object_process_arn = access_point_for_object_process_arn
        self.fc_status = fc_status
        self.access_point_name = access_point_name
        self.creation_date = creation_date
        self.endpoints = endpoints
        self.allow_anonymous_access_for_object_process = allow_anonymous_access_for_object_process
        self.public_access_block_configuration = public_access_block_configuration

class ListAccessPointsForObjectProcessRequest(serde.RequestModel):
    """
    The request for the ListAccessPointsForObjectProcess operation.
    """

    _attribute_map = { 
        'max_keys': {'tag': 'input', 'position': 'query', 'rename': 'max-keys', 'type': 'int'},
        'continuation_token': {'tag': 'input', 'position': 'query', 'rename': 'continuation-token', 'type': 'str'},
    }

    def __init__(
        self,
        max_keys: Optional[int] = None,
        continuation_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        max_keys (int, optional): The maximum number of Object FC Access Points to return.Valid values: 1 to 1000 If the list cannot be complete at a time due to the configurations of the max-keys element, the NextContinuationToken element is included in the response as the token for the next list.
        continuation_token (str, optional): The token from which the list operation must start. You can obtain this token from the NextContinuationToken element in the returned result.
        """
        super().__init__(**kwargs)
        self.max_keys = max_keys
        self.continuation_token = continuation_token


class ListAccessPointsForObjectProcessResult(serde.ResultModel):
    """
    The request for the ListAccessPointsForObjectProcess operation.
    """

    _attribute_map = { 
        'is_truncated': {'tag': 'xml', 'rename': 'IsTruncated', 'type': 'bool,xml'},
        'next_continuation_token': {'tag': 'xml', 'rename': 'NextContinuationToken', 'type': 'str,xml'},
        'account_id': {'tag': 'xml', 'rename': 'AccountId', 'type': 'str,xml'},
        'access_points_for_object_process': {'tag': 'xml', 'rename': 'AccessPointsForObjectProcess', 'type': 'AccessPointsForObjectProcess,xml'},
    }

    _dependency_map = {
        'AccessPointsForObjectProcess': {'new': lambda: AccessPointsForObjectProcess()},
    }

    def __init__(
        self,
        is_truncated: Optional[bool] = None,
        next_continuation_token: Optional[str] = None,
        account_id: Optional[str] = None,
        access_points_for_object_process: Optional[AccessPointsForObjectProcess] = None,
        **kwargs: Any
    ) -> None:
        """
        is_truncated (bool, optional): Indicates whether the returned results are truncated. Valid values:true: indicates that not all results are returned for the request.false: indicates that all results are returned for the request.
        next_continuation_token (str, optional): Indicates that this ListAccessPointsForObjectProcess request contains subsequent results. You need to set the NextContinuationToken element to continuation-token for subsequent results.
        account_id (str, optional): The UID of the Alibaba Cloud account to which the Object FC Access Points belong.
        access_points_for_object_process (AccessPointsForObjectProcess, optional): <no value>
        """
        super().__init__(**kwargs)
        self.is_truncated = is_truncated
        self.next_continuation_token = next_continuation_token
        self.account_id = account_id
        self.access_points_for_object_process = access_points_for_object_process

class DeleteAccessPointForObjectProcessRequest(serde.RequestModel):
    """
    The request for the DeleteAccessPointForObjectProcess operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_for_object_process_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-for-object-process-name', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_for_object_process_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        access_point_for_object_process_name (str, required): The name of the Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_for_object_process_name = access_point_for_object_process_name


class DeleteAccessPointForObjectProcessResult(serde.ResultModel):
    """
    The request for the DeleteAccessPointForObjectProcess operation.
    """

class GetAccessPointConfigForObjectProcessRequest(serde.RequestModel):
    """
    The request for the GetAccessPointConfigForObjectProcess operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_for_object_process_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-for-object-process-name', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_for_object_process_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        access_point_for_object_process_name (str, required): The name of the Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_for_object_process_name = access_point_for_object_process_name


class GetAccessPointConfigForObjectProcessResult(serde.ResultModel):
    """
    The request for the GetAccessPointConfigForObjectProcess operation.
    """

    _attribute_map = { 
        'public_access_block_configuration': {'tag': 'xml', 'rename': 'PublicAccessBlockConfiguration', 'type': 'PublicAccessBlockConfiguration,xml'},
        'object_process_configuration': {'tag': 'xml', 'rename': 'ObjectProcessConfiguration', 'type': 'ObjectProcessConfiguration,xml'},
        'allow_anonymous_access_for_object_process': {'tag': 'xml', 'rename': 'AllowAnonymousAccessForObjectProcess', 'type': 'str,xml'},
    }

    _dependency_map = { 
        'PublicAccessBlockConfiguration': {'new': lambda: PublicAccessBlockConfiguration()},
        'ObjectProcessConfiguration': {'new': lambda: ObjectProcessConfiguration()},
    }

    def __init__(
        self,
        public_access_block_configuration: Optional[PublicAccessBlockConfiguration] = None,
        object_process_configuration: Optional[ObjectProcessConfiguration] = None,
        allow_anonymous_access_for_object_process: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        public_access_block_configuration (PublicAccessBlockConfiguration, optional): The container in which the Block Public Access configurations are stored.
        object_process_configuration (ObjectProcessConfiguration, optional): The container that stores the processing information about the Object FC Access Point.
        allow_anonymous_access_for_object_process (str, optional): Whether allow anonymous user to access this FC Access Points.
        """
        super().__init__(**kwargs)
        self.public_access_block_configuration = public_access_block_configuration
        self.object_process_configuration = object_process_configuration
        self.allow_anonymous_access_for_object_process = allow_anonymous_access_for_object_process

class PutAccessPointConfigForObjectProcessRequest(serde.RequestModel):
    """
    The request for the PutAccessPointConfigForObjectProcess operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_for_object_process_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-for-object-process-name', 'type': 'str', 'required': True},
        'put_access_point_config_for_object_process_configuration': {'tag': 'input', 'position': 'body', 'rename': 'PutAccessPointConfigForObjectProcessConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_for_object_process_name: str = None,
        put_access_point_config_for_object_process_configuration: Optional[PutAccessPointConfigForObjectProcessConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        access_point_for_object_process_name (str, required): The name of the Object FC Access Point. The name of an Object FC Access Point must meet the following requirements:The name cannot exceed 63 characters in length.The name can contain only lowercase letters, digits, and hyphens (-) and cannot start or end with a hyphen (-).The name must be unique in the current region.
        put_access_point_config_for_object_process_configuration (PutAccessPointConfigForObjectProcessConfiguration, optional): The request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_for_object_process_name = access_point_for_object_process_name
        self.put_access_point_config_for_object_process_configuration = put_access_point_config_for_object_process_configuration


class PutAccessPointConfigForObjectProcessResult(serde.ResultModel):
    """
    The request for the PutAccessPointConfigForObjectProcess operation.
    """

class PutAccessPointPolicyForObjectProcessRequest(serde.RequestModel):
    """
    The request for the PutAccessPointPolicyForObjectProcess operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_for_object_process_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-for-object-process-name', 'type': 'str', 'required': True},
        'body': {'tag': 'input', 'position': 'body', 'rename': 'nop', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_for_object_process_name: str = None,
        body: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        access_point_for_object_process_name (str, required): The name of the Object FC Access Point.
        body (io.Reader, optional): The json format permission policies for an Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_for_object_process_name = access_point_for_object_process_name
        self.body = body


class PutAccessPointPolicyForObjectProcessResult(serde.ResultModel):
    """
    The request for the PutAccessPointPolicyForObjectProcess operation.
    """

class GetAccessPointPolicyForObjectProcessRequest(serde.RequestModel):
    """
    The request for the GetAccessPointPolicyForObjectProcess operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_for_object_process_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-for-object-process-name', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_for_object_process_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        access_point_for_object_process_name (str, required): The name of the Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_for_object_process_name = access_point_for_object_process_name


class GetAccessPointPolicyForObjectProcessResult(serde.ResultModel):
    """
    The request for the GetAccessPointPolicyForObjectProcess operation.
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
        body (io.ReadCloser, optional): <no value>
        """
        super().__init__(**kwargs)
        self.body = body

class DeleteAccessPointPolicyForObjectProcessRequest(serde.RequestModel):
    """
    The request for the DeleteAccessPointPolicyForObjectProcess operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'access_point_for_object_process_name': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-access-point-for-object-process-name', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        access_point_for_object_process_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        access_point_for_object_process_name (str, required): The name of the Object FC Access Point.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.access_point_for_object_process_name = access_point_for_object_process_name


class DeleteAccessPointPolicyForObjectProcessResult(serde.ResultModel):
    """
    The request for the DeleteAccessPointPolicyForObjectProcess operation.
    """


class WriteGetObjectResponseRequest(serde.RequestModel):
    """
    The request for the WriteGetObjectResponse operation.
    """

    _attribute_map = {
        'request_route': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-request-route', 'type': 'str', 'required': True},
        'request_token': {'tag': 'input', 'position': 'header', 'rename': '-oss-request-token', 'type': 'str', 'required': True},
        'fwd_status': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-status', 'type': 'str', 'required': True},
        'fwd_header_accept_ranges': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-Accept-Ranges', 'type': 'str'},
        'fwd_header_cache_control': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-Cache-Control', 'type': 'str'},
        'fwd_header_content_disposition': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-Content-Disposition', 'type': 'str'},
        'fwd_header_content_encoding': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-Content-Encoding', 'type': 'str'},
        'fwd_header_content_language': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-Content-Language', 'type': 'str'},
        'fwd_header_content_range': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-Content-Range', 'type': 'str'},
        'fwd_header_content_type': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-Content-Type', 'type': 'str'},
        'fwd_header_etag': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-ETag', 'type': 'str'},
        'fwd_header_expires': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-Expires', 'type': 'str'},
        'fwd_header_last_modified': {'tag': 'input', 'position': 'header', 'rename': 'x-oss-fwd-header-Last-Modified', 'type': 'str'},
        'body': {'tag': 'input', 'position': 'header', 'rename': 'body', 'type': 'nop'},
    }

    def __init__(
        self,
        request_route: str = None,
        request_token: str = None,
        fwd_status: str = None,
        fwd_header_accept_ranges: str = None,
        fwd_header_cache_control: str = None,
        fwd_header_content_disposition: str = None,
        fwd_header_content_encoding: str = None,
        fwd_header_content_language: str = None,
        fwd_header_content_range: str = None,
        fwd_header_content_type: str = None,
        fwd_header_etag: str = None,
        fwd_header_expires: str = None,
        fwd_header_last_modified: str = None,
        body: str = None,
        **kwargs: Any
    ) -> None:
        """
        request_route (str, required): The router forwarding address obtained from the event parameter of Function Compute.
        request_token (str, required): The unique forwarding token obtained from the event parameter of Function Compute.
        fwd_status (str, required): The HTTP status code returned by the backend server.
        fwd_header_accept_ranges (str, optional): The HTTP response header returned by the backend server. It is used to specify the scope of the resources that you want to query.
        fwd_header_cache_control (str, optional): The HTTP response header returned by the backend server. It is used to specify the resource cache method that the client uses. Valid values: no-cache, no-store, public, private, max-age
        fwd_header_content_disposition (str, optional): The HTTP response header returned by the backend server. It is used to specify the name of the object to download and whether and how the object is downloaded. Valid values:
                Content-Disposition:inline: The object is previewed.
                Content-Disposition:attachment: The object is downloaded to the specified path in the browser with the original object name.
                Content-Disposition:attachment; filename="yourFileName": The object is downloaded to the specified path in the browser with a custom name. yourFileName specifies the custom name of the downloaded object, such as example.jpg.
        fwd_header_content_encoding (str, optional): The HTTP response header returned by the backend server. It is used to specify the compression and encoding method of the downloaded object. Valid values:
                identity (default): OSS does not compress or encode the object.
                gzip: OSS uses the LZ77 compression algorithm created by Lempel and Ziv in 1977 and 32-bit cyclic redundancy check (CRC) to encode the object.
                compress: OSS uses the Lempel–Ziv–Welch (LZW) compression algorithm to encode the object.
                deflate: OSS uses the zlib library and the deflate algorithm to encode the object.
                br: OSS uses the Brotli algorithm to encode the object.
        fwd_header_content_language (str, optional): The HTTP response header returned by the backend server. It is used to specify the language of the downloaded object.
        fwd_header_content_range (str, optional): The HTTP response header returned by the backend server. It is used to specify the range of the object that you want to query.
                For example, if the Content-Range header is set to bytes 0-9/67589, the size of the entire object is 67589 and the content of the first 10 bytes (0 to 9) is returned.
        fwd_header_content_type (str, optional): The HTTP response header returned by the backend server. It is used to specify the type of the received or sent data.
        fwd_header_etag (str, optional): he HTTP response header returned by the backend server. It uniquely identifies the object.
        fwd_header_expires (str, optional): The HTTP response header returned by the backend server. It specifies the absolute expiration time of the cache.
        fwd_header_last_modified (str, optional): The HTTP response header returned by the backend server. It specifies the time when the requested resource was last modified.
        body (str, optional): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.request_route = request_route
        self.request_token = request_token
        self.fwd_status = fwd_status
        self.fwd_header_accept_ranges = fwd_header_accept_ranges
        self.fwd_header_cache_control = fwd_header_cache_control
        self.fwd_header_content_disposition = fwd_header_content_disposition
        self.fwd_header_content_encoding = fwd_header_content_encoding
        self.fwd_header_content_language = fwd_header_content_language
        self.fwd_header_content_range = fwd_header_content_range
        self.fwd_header_content_type = fwd_header_content_type
        self.fwd_header_etag = fwd_header_etag
        self.fwd_header_expires = fwd_header_expires
        self.fwd_header_last_modified = fwd_header_last_modified
        self.body = body


class WriteGetObjectResponseResult(serde.ResultModel):
    """
    The request for the WriteGetObjectResponse operation.
    """
