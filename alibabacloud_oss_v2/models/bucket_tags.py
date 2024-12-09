import datetime
from typing import Optional, List, Any, Union
from .. import serde


class Tag(serde.Model):
    """
    The container used to store the tag that you want to configure.
    """

    _attribute_map = { 
        'key': {'tag': 'xml', 'rename': 'Key', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Tag'
    }

    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        key (str, optional): The key of a tag. *   A tag key can be up to 64 bytes in length.*   A tag key cannot start with `http://`, `https://`, or `Aliyun`.*   A tag key must be UTF-8 encoded.*   A tag key cannot be left empty.
        value (str, optional): The value of the tag that you want to add or modify. *   A tag value can be up to 128 bytes in length.*   A tag value must be UTF-8 encoded.*   The tag value can be left empty.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value

class TagSet(serde.Model):
    """
    The container for tags.
    """

    _attribute_map = {
        'tags': {'tag': 'xml', 'rename': 'Tag', 'type': '[Tag]'},
    }

    _xml_map = {
        'name': 'TagSet'
    }

    _dependency_map = {
        'Tag': {'new': lambda: Tag()},
    }

    def __init__(
        self,
        tags: Optional[List[Tag]] = None,
        **kwargs: Any
    ) -> None:
        """
        tags (List[Tag], optional): The tags.
        """
        super().__init__(**kwargs)
        self.tags = tags


class Tagging(serde.Model):
    """
    The container that stores the returned tags of the bucket. If no tags are configured for the bucket, an XML message body is returned in which the Tagging element is empty.
    """

    _attribute_map = { 
        'tag_set': {'tag': 'xml', 'rename': 'TagSet', 'type': 'TagSet'},
    }

    _xml_map = {
        'name': 'Tagging'
    }

    _dependency_map = { 
        'TagSet': {'new': lambda: TagSet()},
    }

    def __init__(
        self,
        tag_set: Optional[TagSet] = None,
        **kwargs: Any
    ) -> None:
        """
        tag_set (TagSet, optional): The container that stores the returned tags of the bucket.
        """
        super().__init__(**kwargs)
        self.tag_set = tag_set


class PutBucketTagsRequest(serde.RequestModel):
    """
    The request for the PutBucketTags operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'tagging': {'tag': 'input', 'position': 'body', 'rename': 'Tagging', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        tagging: Optional[Tagging] = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        tagging (Tagging, optional): The request body schema.
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
        **kwargs: Any
    ) -> None:
        """
        tagging (Tagging, optional): The container that stores the returned tags of the bucket. If no tags are configured for the bucket, an XML message body is returned in which the Tagging element is empty.
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
        bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteBucketTagsResult(serde.ResultModel):
    """
    The request for the DeleteBucketTags operation.
    """
