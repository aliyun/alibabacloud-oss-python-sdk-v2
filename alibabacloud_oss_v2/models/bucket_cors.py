import datetime
from typing import Optional, List, Any, Union
from .. import serde


class CORSRule(serde.Model):
    """
    The container that stores the CORS rules.Up to 10 CORS rules can be configured for a bucket. The XML message body in a request can be up to 16 KB in size.
    """

    _attribute_map = { 
        'allowed_origins': {'tag': 'xml', 'rename': 'AllowedOrigin', 'type': '[str]'},
        'allowed_methods': {'tag': 'xml', 'rename': 'AllowedMethod', 'type': '[str]'},
        'allowed_headers': {'tag': 'xml', 'rename': 'AllowedHeader', 'type': '[str]'},
        'expose_headers': {'tag': 'xml', 'rename': 'ExposeHeader', 'type': '[str]'},
        'max_age_seconds': {'tag': 'xml', 'rename': 'MaxAgeSeconds', 'type': 'int'},
    }

    _xml_map = {
        'name': 'CORSRule'
    }

    def __init__(
        self,
        allowed_origins: Optional[List[str]] = None,
        allowed_methods: Optional[List[str]] = None,
        allowed_headers: Optional[List[str]] = None,
        expose_headers: Optional[List[str]] = None,
        max_age_seconds: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            allowed_origins (List[str], optional): The origins from which cross-origin requests are allowed.
            allowed_methods (List[str], optional): The methods that you can use in cross-origin requests.
            allowed_headers (List[str], optional): Specifies whether the headers specified by Access-Control-Request-Headers in the OPTIONS preflight request are allowed. Each header specified by Access-Control-Request-Headers must match the value of an AllowedHeader element.  You can use only one asterisk (*) as the wildcard character.
            expose_headers (List[str], optional): The response headers for allowed access requests from applications, such as an XMLHttpRequest object in JavaScript.  The asterisk (*) wildcard character is not supported.
            max_age_seconds (int, optional): The period of time within which the browser can cache the response to an OPTIONS preflight request for the specified resource. Unit: seconds.You can specify only one MaxAgeSeconds element in a CORS rule.
        """
        super().__init__(**kwargs)
        self.allowed_origins = allowed_origins
        self.allowed_methods = allowed_methods
        self.allowed_headers = allowed_headers
        self.expose_headers = expose_headers
        self.max_age_seconds = max_age_seconds


class CORSConfiguration(serde.Model):
    """
    The container that stores CORS configuration.
    """

    _attribute_map = { 
        'cors_rules': {'tag': 'xml', 'rename': 'CORSRule', 'type': '[CORSRule]'},
        'response_vary': {'tag': 'xml', 'rename': 'ResponseVary', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'CORSConfiguration'
    }

    _dependency_map = { 
        'CORSRule': {'new': lambda: CORSRule()},
    }

    def __init__(
        self,
        cors_rules: Optional[List[CORSRule]] = None,
        response_vary: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            cors_rules (List[CORSRule], optional): The container that stores CORS rules. Up to 10 rules can be configured for a bucket.
            response_vary (bool, optional): Indicates whether the Vary: Origin header was returned. Default value: false.- true: The Vary: Origin header is returned regardless whether the request is a cross-origin request or whether the cross-origin request succeeds.- false: The Vary: Origin header is not returned.
        """
        super().__init__(**kwargs)
        self.cors_rules = cors_rules
        self.response_vary = response_vary




class PutBucketCorsRequest(serde.RequestModel):
    """
    The request for the PutBucketCors operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'cors_configuration': {'tag': 'input', 'position': 'body', 'rename': 'CORSConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        cors_configuration: Optional[CORSConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            cors_configuration (CORSConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.cors_configuration = cors_configuration


class PutBucketCorsResult(serde.ResultModel):
    """
    The request for the PutBucketCors operation.
    """

class GetBucketCorsRequest(serde.RequestModel):
    """
    The request for the GetBucketCors operation.
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


class GetBucketCorsResult(serde.ResultModel):
    """
    The request for the GetBucketCors operation.
    """

    _attribute_map = { 
        'cors_configuration': {'tag': 'output', 'position': 'body', 'rename': 'CORSConfiguration', 'type': 'CORSConfiguration,xml'},
    }

    _dependency_map = { 
        'CORSConfiguration': {'new': lambda: CORSConfiguration()},
    }

    def __init__(
        self,
        cors_configuration: Optional[CORSConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            cors_configuration (CORSConfiguration, optional): The container that stores CORS configuration.
        """
        super().__init__(**kwargs)
        self.cors_configuration = cors_configuration

class DeleteBucketCorsRequest(serde.RequestModel):
    """
    The request for the DeleteBucketCors operation.
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


class DeleteBucketCorsResult(serde.ResultModel):
    """
    The request for the DeleteBucketCors operation.
    """

class OptionObjectRequest(serde.RequestModel):
    """
    The request for the OptionObject operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'key': {'tag': 'input', 'position': 'path', 'rename': 'key', 'type': 'str', 'required': True},
        'origin': {'tag': 'input', 'position': 'header', 'rename': 'Origin', 'type': 'str'},
        'access_control_request_method': {'tag': 'input', 'position': 'header', 'rename': 'Access-Control-Request-Method', 'type': 'str'},
        'access_control_request_headers': {'tag': 'input', 'position': 'header', 'rename': 'Access-Control-Request-Headers', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        origin: Optional[str] = None,
        access_control_request_method: Optional[str] = None,
        access_control_request_headers: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The full path of the object.
            origin (str, optional): The origin of the request. It is used to identify a cross-origin request. You can specify only one Origin header in a cross-origin request. By default, this header is left empty.
            access_control_request_method (str, optional): The method to be used in the actual cross-origin request. You can specify only one Access-Control-Request-Method header in a cross-origin request. By default, this header is left empty.
            access_control_request_headers (str, optional): The custom headers to be sent in the actual cross-origin request. You can configure multiple custom headers in a cross-origin request. Custom headers are separated by commas (,). By default, this header is left empty.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.origin = origin
        self.access_control_request_method = access_control_request_method
        self.access_control_request_headers = access_control_request_headers


class OptionObjectResult(serde.ResultModel):
    """
    The request for the OptionObject operation.
    """

    _attribute_map = { 
        'access_control_allow_origin': {'tag': 'output', 'position': 'header', 'rename': 'Access-Control-Allow-Origin', 'type': 'str'},
        'access_control_allow_methods': {'tag': 'output', 'position': 'header', 'rename': 'Access-Control-Allow-Methods', 'type': 'str'},
        'access_control_allow_headers': {'tag': 'output', 'position': 'header', 'rename': 'Access-Control-Allow-Headers', 'type': 'str'},
        'access_control_expose_headers': {'tag': 'output', 'position': 'header', 'rename': 'Access-Control-Expose-Headers', 'type': 'str'},
        'access_control_max_age': {'tag': 'output', 'position': 'header', 'rename': 'Access-Control-Max-Age', 'type': 'int'},
    }

    def __init__(
        self,
        access_control_allow_origin: Optional[str] = None,
        access_control_allow_methods: Optional[str] = None,
        access_control_allow_headers: Optional[str] = None,
        access_control_expose_headers: Optional[str] = None,
        access_control_max_age: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            access_control_allow_origin (str, optional): <no value>
            access_control_allow_methods (str, optional): <no value>
            access_control_allow_headers (str, optional): <no value>
            access_control_expose_headers (str, optional): <no value>
            access_control_max_age (int, optional): <no value>
        """
        super().__init__(**kwargs)
        self.access_control_allow_origin = access_control_allow_origin
        self.access_control_allow_methods = access_control_allow_methods
        self.access_control_allow_headers = access_control_allow_headers
        self.access_control_expose_headers = access_control_expose_headers
        self.access_control_max_age = access_control_max_age
