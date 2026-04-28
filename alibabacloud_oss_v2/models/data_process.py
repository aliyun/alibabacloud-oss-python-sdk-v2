from typing import Optional, Any
from .. import serde


class DoMetaQueryActionRequest(serde.RequestModel):
    """
    The request for the DoMetaQueryAction operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'action': {'tag': 'input', 'position': 'query', 'rename': 'action', 'type': 'str', 'required': True},
        'body': {'tag': 'input', 'position': 'body'},
    }

    def __init__(
        self,
        bucket: str = None,
        action: Optional[str] = None,
        body: Optional[Any] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            action (str, required): The name of the action.
            body (Any, optional): The request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.action = action
        self.body = body


class DoMetaQueryActionResult(serde.ResultModel):
    """
    The result for the DoMetaQueryAction operation.
    """


class DoDataPipelineActionRequest(serde.RequestModel):
    """
    The request for the DoDataPipelineAction operation.
    """

    _attribute_map = {
        'action': {'tag': 'input', 'position': 'query', 'rename': 'action', 'type': 'str', 'required': True},
        'body': {'tag': 'input', 'position': 'body'},
    }

    def __init__(
        self,
        action: Optional[str] = None,
        body: Optional[Any] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            action (str, required): The name of the action.
            body (Any, optional): The request body.
        """
        super().__init__(**kwargs)
        self.action = action
        self.body = body


class DoDataPipelineActionResult(serde.ResultModel):
    """
    The result for the DoDataPipelineAction operation.
    """

