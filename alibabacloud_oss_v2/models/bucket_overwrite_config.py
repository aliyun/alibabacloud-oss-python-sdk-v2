from typing import Optional, List, Any
from .. import serde


class OverwritePrincipals(serde.Model):
    """
    A collection of authorized entities. The usage is similar to the `Principal` element in a bucket policy. You can specify an Alibaba Cloud account, a RAM user, or a RAM role. If this element is empty or not configured, overwrites are prohibited for all objects that match the prefix and suffix conditions.
    """

    _attribute_map = { 
        'principals': {'tag': 'xml', 'rename': 'Principal', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'Principals'
    }

    def __init__(
        self,
        principals: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            principals (List[str], optional): A collection of authorized entities. The usage is similar to the `Principal` element in a bucket policy. You can specify an Alibaba Cloud account, a RAM user, or a RAM role. If this element is empty or not configured, overwrites are prohibited for all objects that match the prefix and suffix conditions.
        """
        super().__init__(**kwargs)
        self.principals = principals


class OverwriteRule(serde.Model):
    """
    List of overwrite protection rules. A bucket can have a maximum of 100 rules.
    """

    _attribute_map = { 
        'action': {'tag': 'xml', 'rename': 'Action', 'type': 'str'},
        'prefix': {'tag': 'xml', 'rename': 'Prefix', 'type': 'str'},
        'suffix': {'tag': 'xml', 'rename': 'Suffix', 'type': 'str'},
        'principals': {'tag': 'xml', 'rename': 'Principals', 'type': 'Principals'},
        'id': {'tag': 'xml', 'rename': 'ID', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Rule'
    }

    _dependency_map = { 
        'Principals': {'new': lambda: OverwritePrincipals()},
    }

    def __init__(
        self,
        action: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        principals: Optional[OverwritePrincipals] = None,
        id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            action (str, optional): The operation type. Currently, only `forbid` (prohibit overwrites) is supported.
            prefix (str, optional): The prefix of object names to filter the objects that you want to process. The maximum length is 1,023 characters. Each rule can have at most one prefix. Prefixes and suffixes do not support regular expressions.
            suffix (str, optional): The suffix of object names to filter the objects that you want to process. The maximum length is 1,023 characters. Each rule can have at most one suffix. Prefixes and suffixes do not support regular expressions.
            principals (OverwritePrincipals, optional): A collection of authorized entities. The usage is similar to the `Principal` element in a bucket policy. You can specify an Alibaba Cloud account, a RAM user, or a RAM role. If this element is empty or not configured, overwrites are prohibited for all objects that match the prefix and suffix conditions.
            id (str, optional): The unique identifier of the rule. If you do not specify this element, a UUID is randomly generated. If you specify this element, the value must be unique. Different rules cannot have the same ID.
        """
        super().__init__(**kwargs)
        self.action = action
        self.prefix = prefix
        self.suffix = suffix
        self.principals = principals
        self.id = id


class OverwriteConfiguration(serde.Model):
    """
    The structure for the overwrite protection configuration.
    """

    _attribute_map = { 
        'rules': {'tag': 'xml', 'rename': 'Rule', 'type': '[Rule]'},
    }

    _xml_map = {
        'name': 'OverwriteConfiguration'
    }

    _dependency_map = { 
        'Rule': {'new': lambda: OverwriteRule()},
    }

    def __init__(
        self,
        rules: Optional[List[OverwriteRule]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            rules (List[OverwriteRule], optional): List of overwrite protection rules. A bucket can have a maximum of 100 rules.
        """
        super().__init__(**kwargs)
        self.rules = rules

class PutBucketOverwriteConfigRequest(serde.RequestModel):
    """
    The request for the PutBucketOverwriteConfig operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'overwrite_configuration': {'tag': 'input', 'position': 'body', 'rename': 'OverwriteConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        overwrite_configuration: Optional[OverwriteConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): Bucket Name
            overwrite_configuration (OverwriteConfiguration, optional): Structure of the API Request Body
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.overwrite_configuration = overwrite_configuration


class PutBucketOverwriteConfigResult(serde.ResultModel):
    """
    The request for the PutBucketOverwriteConfig operation.
    """

class GetBucketOverwriteConfigRequest(serde.RequestModel):
    """
    The request for the GetBucketOverwriteConfig operation.
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
            bucket (str, required): Bucket Name
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetBucketOverwriteConfigResult(serde.ResultModel):
    """
    The request for the GetBucketOverwriteConfig operation.
    """

    _attribute_map = { 
        'overwrite_configuration': {'tag': 'output', 'position': 'body', 'rename': 'OverwriteConfiguration', 'type': 'OverwriteConfiguration,xml'},
    }

    _dependency_map = { 
        'OverwriteConfiguration': {'new': lambda: OverwriteConfiguration()},
    }

    def __init__(
        self,
        overwrite_configuration: Optional[OverwriteConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            overwrite_configuration (OverwriteConfiguration, optional): Container for Saving Bucket Overwrite Rules
        """
        super().__init__(**kwargs)
        self.overwrite_configuration = overwrite_configuration

class DeleteBucketOverwriteConfigRequest(serde.RequestModel):
    """
    The request for the DeleteBucketOverwriteConfig operation.
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
            bucket (str, required): Bucket name
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteBucketOverwriteConfigResult(serde.ResultModel):
    """
    The request for the DeleteBucketOverwriteConfig operation.
    """
