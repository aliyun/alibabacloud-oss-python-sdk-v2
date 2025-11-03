import datetime
from typing import Optional, List, Any, Union
from .. import serde


class StyleInfo(serde.Model):
    """
    The container that stores style infomration.
    """

    _attribute_map = { 
        'name': {'tag': 'xml', 'rename': 'Name', 'type': 'str'},
        'content': {'tag': 'xml', 'rename': 'Content', 'type': 'str'},
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'last_modify_time': {'tag': 'xml', 'rename': 'LastModifyTime', 'type': 'str'},
        'category': {'tag': 'xml', 'rename': 'Category', 'type': 'str'},
    }

    _xml_map = {
        'name': 'StyleInfo'
    }

    def __init__(
        self,
        name: Optional[str] = None,
        content: Optional[str] = None,
        create_time: Optional[str] = None,
        last_modify_time: Optional[str] = None,
        category: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The style name.
            content (str, optional): The content of the style.
            create_time (str, optional): The time when the style was created.
            last_modify_time (str, optional): The time when the style was last modified.
            category (str, optional): The category of this style。  Invalid value：image、document、video。
        """
        super().__init__(**kwargs)
        self.name = name
        self.content = content
        self.create_time = create_time
        self.last_modify_time = last_modify_time
        self.category = category


class StyleList(serde.Model):
    """
    The container that was used to query the information about image styles.
    """

    _attribute_map = { 
        'styles': {'tag': 'xml', 'rename': 'Style', 'type': '[StyleInfo]'},
    }

    _xml_map = {
        'name': 'StyleList'
    }

    _dependency_map = { 
        'StyleInfo': {'new': lambda: StyleInfo()},
    }

    def __init__(
        self,
        styles: Optional[List[StyleInfo]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            styles (List[StyleInfo], optional): The list of styles.
        """
        super().__init__(**kwargs)
        self.styles = styles

class StyleContent(serde.Model):
    """
    The container that stores the content information about the image style.
    """

    _attribute_map = {
        'content': {'tag': 'xml', 'rename': 'Content', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Style'
    }

    def __init__(
        self,
        content: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            content (str, optional): The content of the style.
        """
        super().__init__(**kwargs)
        self.content = content

class PutStyleRequest(serde.RequestModel):
    """
    The request for the PutStyle operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'style_name': {'tag': 'input', 'position': 'query', 'rename': 'styleName', 'type': 'str', 'required': True},
        'category': {'tag': 'input', 'position': 'query', 'rename': 'category', 'type': 'str'},
        'style': {'tag': 'input', 'position': 'body', 'rename': 'Style', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        style_name: str = None,
        category: Optional[str] = None,
        style: Optional[StyleContent] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            style_name (str, required): The name of the image style.
            category (str, optional): The category of the style.
            style (Style, optional): The container that stores the content information about the image style.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.style_name = style_name
        self.category = category
        self.style = style


class PutStyleResult(serde.ResultModel):
    """
    The request for the PutStyle operation.
    """

class ListStyleRequest(serde.RequestModel):
    """
    The request for the ListStyle operation.
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


class ListStyleResult(serde.ResultModel):
    """
    The request for the ListStyle operation.
    """

    _attribute_map = { 
        'style_list': {'tag': 'output', 'position': 'body', 'rename': 'StyleList', 'type': 'StyleList,xml'},
    }

    _dependency_map = { 
        'StyleList': {'new': lambda: StyleList()},
    }

    def __init__(
        self,
        style_list: Optional[StyleList] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            style_list (StyleList, optional): The container that was used to query the information about image styles.
        """
        super().__init__(**kwargs)
        self.style_list = style_list

class GetStyleRequest(serde.RequestModel):
    """
    The request for the GetStyle operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'style_name': {'tag': 'input', 'position': 'query', 'rename': 'styleName', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        style_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            style_name (str, required): The name of the image style.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.style_name = style_name


class GetStyleResult(serde.ResultModel):
    """
    The request for the GetStyle operation.
    """

    _attribute_map = { 
        'style': {'tag': 'output', 'position': 'body', 'rename': 'Style', 'type': 'StyleInfo,xml'},
    }

    _dependency_map = { 
        'StyleInfo': {'new': lambda: StyleInfo()},
    }

    def __init__(
        self,
        style: Optional[StyleInfo] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            style (StyleInfo, optional): The container that stores the information about the image style.
        """
        super().__init__(**kwargs)
        self.style = style

class DeleteStyleRequest(serde.RequestModel):
    """
    The request for the DeleteStyle operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'style_name': {'tag': 'input', 'position': 'query', 'rename': 'styleName', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        style_name: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            style_name (str, required): The name of the image style.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.style_name = style_name


class DeleteStyleResult(serde.ResultModel):
    """
    The request for the DeleteStyle operation.
    """
