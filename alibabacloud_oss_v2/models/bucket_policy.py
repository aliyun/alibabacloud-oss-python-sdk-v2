from typing import Optional, List, Any, Union
from .. import serde, BodyType


class PolicyStatus(serde.Model):
    """
    The container that stores public access information.
    """

    _attribute_map = { 
        'is_public': {'tag': 'xml', 'rename': 'IsPublic', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'PolicyStatus'
    }

    def __init__(
        self,
        is_public: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            is_public (bool, optional): Indicates whether the current bucket policy allows public access.truefalse
        """
        super().__init__(**kwargs)
        self.is_public = is_public




class PutBucketPolicyRequest(serde.RequestModel):
    """
    The request for the PutBucketPolicy operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'body': {'tag': 'input', 'position': 'body', 'rename': 'nop', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        body: Optional[BodyType] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            body (BodyType, required): The request parameters.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.body = body


class PutBucketPolicyResult(serde.ResultModel):
    """
    The request for the PutBucketPolicy operation.
    """

class GetBucketPolicyRequest(serde.RequestModel):
    """
    The request for the GetBucketPolicy operation.
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


class GetBucketPolicyResult(serde.ResultModel):
    """
    The request for the GetBucketPolicy operation.
    """

    _attribute_map = { 
        'body': {'tag': 'output', 'position': 'body', 'type': 'str'},
    }

    def __init__(
        self,
        body: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            body (str, optional): <no value>
        """
        super().__init__(**kwargs)
        self.body = body

class DeleteBucketPolicyRequest(serde.RequestModel):
    """
    The request for the DeleteBucketPolicy operation.
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


class DeleteBucketPolicyResult(serde.ResultModel):
    """
    The request for the DeleteBucketPolicy operation.
    """

class GetBucketPolicyStatusRequest(serde.RequestModel):
    """
    The request for the GetBucketPolicyStatus operation.
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


class GetBucketPolicyStatusResult(serde.ResultModel):
    """
    The request for the GetBucketPolicyStatus operation.
    """

    _attribute_map = { 
        'policy_status': {'tag': 'output', 'position': 'body', 'rename': 'PolicyStatus', 'type': 'PolicyStatus,xml'},
    }

    _dependency_map = { 
        'PolicyStatus': {'new': lambda: PolicyStatus()},
    }

    def __init__(
        self,
        policy_status: Optional[PolicyStatus] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            policy_status (PolicyStatus, optional): The container that stores public access information.
        """
        super().__init__(**kwargs)
        self.policy_status = policy_status
