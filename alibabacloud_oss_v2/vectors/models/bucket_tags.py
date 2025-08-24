
from typing import Optional, List, Any, Union, Dict, MutableMapping
from ... import serde

class Tagging(serde.Model):
    """
    The container that stores the returned tags of the bucket. If no tags are configured for the bucket, an XML message body is returned in which the Tagging element is empty.
    """

    _attribute_map = {
        "tags": {"tag": "xml", "type": "dict,usermeta"},

    }

    _xml_map = {
        'name': 'Tagging'
    }

    def __init__(
        self,
        tags: Optional[MutableMapping] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The key of the tag.
            value (str, optional): The value of the tag.
        """
        super().__init__(**kwargs)
        self.tags = tags





class PutBucketTagsRequest(serde.RequestModel):
    """
    The request for the PutBucketTags operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'tagging': {'tag': 'input', 'position': 'body', 'rename': 'Tagging', 'type': 'Tagging,xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        tagging: Optional[Tagging] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            tagging (dict, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.tagging = tagging


class PutBucketTagsResult(serde.ResultModel):
    """
    The request for the PutBucketTags operation.
    """

class GetBucketTagsRequest(serde.RequestModel):
    """
    The request for the GetBucketTags operation.
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


class GetBucketTagsResult(serde.ResultModel):
    """
    The request for the GetBucketTags operation.
    """

    _attribute_map = {
        'tagging': {'tag': 'output', 'position': 'body', 'rename': 'Tagging', 'type': 'Tagging,xml'},
    }
    _dependency_map = {
        'Tagging': {'new': lambda: Tagging()},
    }


    def __init__(
        self,
        tagging: Optional[Tagging] = None,
        # tagging: Optional[MutableMapping] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            tagging (VectorTagging, optional): The container that stores the returned tags of the bucket. If no tags are configured for the bucket, an XML message body is returned in which the Tagging element is empty.
        """
        super().__init__(**kwargs)
        self.tagging = tagging

class DeleteBucketTagsRequest(serde.RequestModel):
    """
    The request for the DeleteBucketTags operation.
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


class DeleteBucketTagsResult(serde.ResultModel):
    """
    The request for the DeleteBucketTags operation.
    """
