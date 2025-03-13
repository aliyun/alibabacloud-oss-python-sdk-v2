import datetime
from typing import Optional, List, Any, Union
from .. import serde


class TLS(serde.Model):
    """
    The container that stores TLS version configurations.
    """

    _attribute_map = { 
        'enable': {'tag': 'xml', 'rename': 'Enable', 'type': 'bool'},
        'tls_versions': {'tag': 'xml', 'rename': 'TLSVersion', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'TLS'
    }

    def __init__(
        self,
        enable: Optional[bool] = None,
        tls_versions: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            enable (bool, optional): Specifies whether to enable TLS version management for the bucket.Valid values:*true     *false
            tls_versions (List[str], optional): The TLS versions.
        """
        super().__init__(**kwargs)
        self.enable = enable
        self.tls_versions = tls_versions


class HttpsConfiguration(serde.Model):
    """
    The container that stores Transport Layer Security (TLS) version configurations.
    """

    _attribute_map = { 
        'tls': {'tag': 'xml', 'rename': 'TLS', 'type': 'TLS'},
    }

    _xml_map = {
        'name': 'HttpsConfiguration'
    }

    _dependency_map = { 
        'TLS': {'new': lambda: TLS()},
    }

    def __init__(
        self,
        tls: Optional[TLS] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            tls (TLS, optional): The container that stores TLS version configurations.
        """
        super().__init__(**kwargs)
        self.tls = tls




class GetBucketHttpsConfigRequest(serde.RequestModel):
    """
    The request for the GetBucketHttpsConfig operation.
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


class GetBucketHttpsConfigResult(serde.ResultModel):
    """
    The request for the GetBucketHttpsConfig operation.
    """

    _attribute_map = { 
        'https_configuration': {'tag': 'output', 'position': 'body', 'rename': 'HttpsConfiguration', 'type': 'HttpsConfiguration,xml'},
    }

    _dependency_map = { 
        'HttpsConfiguration': {'new': lambda: HttpsConfiguration()},
    }

    def __init__(
        self,
        https_configuration: Optional[HttpsConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            https_configuration (HttpsConfiguration, optional): The container that stores HTTPS configurations.
        """
        super().__init__(**kwargs)
        self.https_configuration = https_configuration

class PutBucketHttpsConfigRequest(serde.RequestModel):
    """
    The request for the PutBucketHttpsConfig operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'https_configuration': {'tag': 'input', 'position': 'body', 'rename': 'HttpsConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        https_configuration: Optional[HttpsConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): This name of the bucket.
            https_configuration (HttpsConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.https_configuration = https_configuration


class PutBucketHttpsConfigResult(serde.ResultModel):
    """
    The request for the PutBucketHttpsConfig operation.
    """
