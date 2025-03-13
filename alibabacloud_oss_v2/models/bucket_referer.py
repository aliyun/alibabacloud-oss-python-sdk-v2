import datetime
from typing import Optional, List, Any, Union
from .. import serde


class RefererList(serde.Model):
    """
    The container that stores the Referer whitelist.  ****The PutBucketReferer operation overwrites the existing Referer whitelist with the Referer whitelist specified in RefererList. If RefererList is not specified in the request, which specifies that no Referer elements are included, the operation clears the existing Referer whitelist.
    """

    _attribute_map = { 
        'referers': {'tag': 'xml', 'rename': 'Referer', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'RefererList'
    }

    def __init__(
        self,
        referers: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            referers (List[str], optional): The addresses in the Referer whitelist.
        """
        super().__init__(**kwargs)
        self.referers = referers


class RefererBlacklist(serde.Model):
    """
    The container that stores the Referer blacklist.
    """

    _attribute_map = { 
        'referers': {'tag': 'xml', 'rename': 'Referer', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'RefererBlacklist'
    }

    def __init__(
        self,
        referers: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            referers (List[str], optional): The addresses in the Referer blacklist.
        """
        super().__init__(**kwargs)
        self.referers = referers


class RefererConfiguration(serde.Model):
    """
    The container that stores the hotlink protection configurations.
    """

    _attribute_map = { 
        'allow_empty_referer': {'tag': 'xml', 'rename': 'AllowEmptyReferer', 'type': 'bool'},
        'allow_truncate_query_string': {'tag': 'xml', 'rename': 'AllowTruncateQueryString', 'type': 'bool'},
        'truncate_path': {'tag': 'xml', 'rename': 'TruncatePath', 'type': 'bool'},
        'referer_list': {'tag': 'xml', 'rename': 'RefererList', 'type': 'RefererList'},
        'referer_blacklist': {'tag': 'xml', 'rename': 'RefererBlacklist', 'type': 'RefererBlacklist'},
    }

    _xml_map = {
        'name': 'RefererConfiguration'
    }

    _dependency_map = { 
        'RefererList': {'new': lambda: RefererList()},
        'RefererBlacklist': {'new': lambda: RefererBlacklist()},
    }

    def __init__(
        self,
        allow_empty_referer: Optional[bool] = None,
        allow_truncate_query_string: Optional[bool] = None,
        truncate_path: Optional[bool] = None,
        referer_list: Optional[RefererList] = None,
        referer_blacklist: Optional[RefererBlacklist] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            allow_empty_referer (bool, optional): Specifies whether to allow a request whose Referer field is empty. Valid values:*   true (default)*   false
            allow_truncate_query_string (bool, optional): Specifies whether to truncate the query string in the URL when the Referer is matched. Valid values:*   true (default)*   false
            truncate_path (bool, optional): Specifies whether to truncate the path and parts that follow the path in the URL when the Referer is matched. Valid values:*   true*   false
            referer_list (RefererList, optional): The container that stores the Referer whitelist.  ****The PutBucketReferer operation overwrites the existing Referer whitelist with the Referer whitelist specified in RefererList. If RefererList is not specified in the request, which specifies that no Referer elements are included, the operation clears the existing Referer whitelist.
            referer_blacklist (RefererBlacklist, optional): The container that stores the Referer blacklist.
        """
        super().__init__(**kwargs)
        self.allow_empty_referer = allow_empty_referer
        self.allow_truncate_query_string = allow_truncate_query_string
        self.truncate_path = truncate_path
        self.referer_list = referer_list
        self.referer_blacklist = referer_blacklist




class PutBucketRefererRequest(serde.RequestModel):
    """
    The request for the PutBucketReferer operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'referer_configuration': {'tag': 'input', 'position': 'body', 'rename': 'RefererConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        referer_configuration: Optional[RefererConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            referer_configuration (RefererConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.referer_configuration = referer_configuration


class PutBucketRefererResult(serde.ResultModel):
    """
    The request for the PutBucketReferer operation.
    """

class GetBucketRefererRequest(serde.RequestModel):
    """
    The request for the GetBucketReferer operation.
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


class GetBucketRefererResult(serde.ResultModel):
    """
    The request for the GetBucketReferer operation.
    """

    _attribute_map = { 
        'referer_configuration': {'tag': 'output', 'position': 'body', 'rename': 'RefererConfiguration', 'type': 'RefererConfiguration,xml'},
    }

    _dependency_map = { 
        'RefererConfiguration': {'new': lambda: RefererConfiguration()},
    }

    def __init__(
        self,
        referer_configuration: Optional[RefererConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            referer_configuration (RefererConfiguration, optional): The container that stores the hotlink protection configurations.
        """
        super().__init__(**kwargs)
        self.referer_configuration = referer_configuration
