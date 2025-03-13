
from typing import Optional, Any
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
        Args:
            key (str, optional): The key of a tag. *   A tag key can be up to 64 bytes in length.*   A tag key cannot start with `http://`, `https://`, or `Aliyun`.*   A tag key must be UTF-8 encoded.*   A tag key cannot be left empty.
            value (str, optional): The value of the tag that you want to add or modify. *   A tag value can be up to 128 bytes in length.*   A tag value must be UTF-8 encoded.*   The tag value can be left empty.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value

