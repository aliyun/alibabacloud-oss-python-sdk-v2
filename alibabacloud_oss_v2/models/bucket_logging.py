from typing import Optional, List, Any, Union
from .. import serde


class LoggingHeaderSet(serde.Model):
    """
    The container that stores the configurations of custom request headers.
    """

    _attribute_map = { 
        'headers': {'tag': 'xml', 'rename': 'header', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'HeaderSet'
    }

    def __init__(
        self,
        headers: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            headers (List[str], optional): The list of the custom request headers.
        """
        super().__init__(**kwargs)
        self.headers = headers


class LoggingParamSet(serde.Model):
    """
    The container that stores the configurations of custom URL parameters.
    """

    _attribute_map = { 
        'parameters': {'tag': 'xml', 'rename': 'parameter', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'ParamSet'
    }

    def __init__(
        self,
        parameters: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            parameters (List[str], optional): The list of the custom URL parameters.
        """
        super().__init__(**kwargs)
        self.parameters = parameters


class LoggingEnabled(serde.Model):
    """
    The container that stores the information about access log collection.
    """

    _attribute_map = { 
        'target_bucket': {'tag': 'xml', 'rename': 'TargetBucket', 'type': 'str'},
        'target_prefix': {'tag': 'xml', 'rename': 'TargetPrefix', 'type': 'str'},
        'logging_role': {'tag': 'xml', 'rename': 'LoggingRole', 'type': 'str'},
    }

    _xml_map = {
        'name': 'LoggingEnabled'
    }

    def __init__(
        self,
        target_bucket: Optional[str] = None,
        target_prefix: Optional[str] = None,
        logging_role: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            target_bucket (str, optional): The bucket that stores access logs.
            target_prefix (str, optional): The prefix of the log objects. This parameter can be left empty.
            logging_role (str, optional): The role used for logging operations.
        """
        super().__init__(**kwargs)
        self.target_bucket = target_bucket
        self.target_prefix = target_prefix
        self.logging_role = logging_role


class UserDefinedLogFieldsConfiguration(serde.Model):
    """
    The specified field configurations of real-time logs in a bucket.
    """

    _attribute_map = { 
        'header_set': {'tag': 'xml', 'rename': 'HeaderSet', 'type': 'HeaderSet'},
        'param_set': {'tag': 'xml', 'rename': 'ParamSet', 'type': 'ParamSet'},
    }

    _xml_map = {
        'name': 'UserDefinedLogFieldsConfiguration'
    }

    _dependency_map = { 
        'HeaderSet': {'new': lambda: LoggingHeaderSet()},
        'ParamSet': {'new': lambda: LoggingParamSet()},
    }

    def __init__(
        self,
        header_set: Optional[LoggingHeaderSet] = None,
        param_set: Optional[LoggingParamSet] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            header_set (HeaderSet, optional): The container that stores the configurations of custom request headers.
            param_set (ParamSet, optional): The container that stores the configurations of custom URL parameters.
        """
        super().__init__(**kwargs)
        self.header_set = header_set
        self.param_set = param_set


class BucketLoggingStatus(serde.Model):
    """
    Indicates the container used to store access logging configuration of a bucket.
    """

    _attribute_map = { 
        'logging_enabled': {'tag': 'xml', 'rename': 'LoggingEnabled', 'type': 'LoggingEnabled'},
    }

    _xml_map = {
        'name': 'BucketLoggingStatus'
    }

    _dependency_map = { 
        'LoggingEnabled': {'new': lambda: LoggingEnabled()},
    }

    def __init__(
        self,
        logging_enabled: Optional[LoggingEnabled] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            logging_enabled (LoggingEnabled, optional): Indicates the container used to store access logging information. This element is returned if it is enabled and is not returned if it is disabled.
        """
        super().__init__(**kwargs)
        self.logging_enabled = logging_enabled




class PutBucketLoggingRequest(serde.RequestModel):
    """
    The request for the PutBucketLogging operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'bucket_logging_status': {'tag': 'input', 'position': 'body', 'rename': 'BucketLoggingStatus', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        bucket_logging_status: Optional[BucketLoggingStatus] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            bucket_logging_status (BucketLoggingStatus, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.bucket_logging_status = bucket_logging_status


class PutBucketLoggingResult(serde.ResultModel):
    """
    The request for the PutBucketLogging operation.
    """

class GetBucketLoggingRequest(serde.RequestModel):
    """
    The request for the GetBucketLogging operation.
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


class GetBucketLoggingResult(serde.ResultModel):
    """
    The request for the GetBucketLogging operation.
    """

    _attribute_map = { 
        'bucket_logging_status': {'tag': 'output', 'position': 'body', 'rename': 'BucketLoggingStatus', 'type': 'BucketLoggingStatus,xml'},
    }

    _dependency_map = { 
        'BucketLoggingStatus': {'new': lambda: BucketLoggingStatus()},
    }

    def __init__(
        self,
        bucket_logging_status: Optional[BucketLoggingStatus] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket_logging_status (BucketLoggingStatus, optional): Indicates the container used to store access logging configuration of a bucket.
        """
        super().__init__(**kwargs)
        self.bucket_logging_status = bucket_logging_status

class DeleteBucketLoggingRequest(serde.RequestModel):
    """
    The request for the DeleteBucketLogging operation.
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


class DeleteBucketLoggingResult(serde.ResultModel):
    """
    The request for the DeleteBucketLogging operation.
    """

class PutUserDefinedLogFieldsConfigRequest(serde.RequestModel):
    """
    The request for the PutUserDefinedLogFieldsConfig operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'user_defined_log_fields_configuration': {'tag': 'input', 'position': 'body', 'rename': 'UserDefinedLogFieldsConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        user_defined_log_fields_configuration: Optional[UserDefinedLogFieldsConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            user_defined_log_fields_configuration (UserDefinedLogFieldsConfiguration, optional): The container that stores the specified log configurations.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.user_defined_log_fields_configuration = user_defined_log_fields_configuration


class PutUserDefinedLogFieldsConfigResult(serde.ResultModel):
    """
    The request for the PutUserDefinedLogFieldsConfig operation.
    """

class GetUserDefinedLogFieldsConfigRequest(serde.RequestModel):
    """
    The request for the GetUserDefinedLogFieldsConfig operation.
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


class GetUserDefinedLogFieldsConfigResult(serde.ResultModel):
    """
    The request for the GetUserDefinedLogFieldsConfig operation.
    """

    _attribute_map = { 
        'user_defined_log_fields_configuration': {'tag': 'output', 'position': 'body', 'rename': 'UserDefinedLogFieldsConfiguration', 'type': 'UserDefinedLogFieldsConfiguration,xml'},
    }

    _dependency_map = { 
        'UserDefinedLogFieldsConfiguration': {'new': lambda: UserDefinedLogFieldsConfiguration()},
    }

    def __init__(
        self,
        user_defined_log_fields_configuration: Optional[UserDefinedLogFieldsConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            user_defined_log_fields_configuration (UserDefinedLogFieldsConfiguration, optional): The container for the user-defined logging configuration.
        """
        super().__init__(**kwargs)
        self.user_defined_log_fields_configuration = user_defined_log_fields_configuration

class DeleteUserDefinedLogFieldsConfigRequest(serde.RequestModel):
    """
    The request for the DeleteUserDefinedLogFieldsConfig operation.
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


class DeleteUserDefinedLogFieldsConfigResult(serde.ResultModel):
    """
    The request for the DeleteUserDefinedLogFieldsConfig operation.
    """
