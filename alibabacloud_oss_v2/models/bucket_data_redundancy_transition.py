import datetime
from typing import Optional, List, Any, Union
from .. import serde


class BucketDataRedundancyTransition(serde.Model):
    """
    The container in which the redundancy type conversion task is stored.
    """

    _attribute_map = { 
        'bucket': {'tag': 'xml', 'rename': 'Bucket', 'type': 'str'},
        'task_id': {'tag': 'xml', 'rename': 'TaskId', 'type': 'str'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'start_time': {'tag': 'xml', 'rename': 'StartTime', 'type': 'str'},
        'end_time': {'tag': 'xml', 'rename': 'EndTime', 'type': 'str'},
        'process_percentage': {'tag': 'xml', 'rename': 'ProcessPercentage', 'type': 'int'},
        'estimated_remaining_time': {'tag': 'xml', 'rename': 'EstimatedRemainingTime', 'type': 'int'},
    }

    _xml_map = {
        'name': 'BucketDataRedundancyTransition'
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        task_id: Optional[str] = None,
        status: Optional[str] = None,
        create_time: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        process_percentage: Optional[int] = None,
        estimated_remaining_time: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            task_id (str, optional): The ID of the redundancy type conversion task. The ID can be used to view and delete the redundancy type conversion task.
            status (str, optional): The state of the redundancy type change task. Valid values:QueueingProcessingFinished.
            create_time (str, optional): The time when the redundancy type change task was created.
            start_time (str, optional): The time when the redundancy type change task was performed. This element is available when the task is in the Processing or Finished state.
            end_time (str, optional): The time when the redundancy type change task was finished. This element is available when the task is in the Finished state.
            process_percentage (str, optional): The progress of the redundancy type change task in percentage. Valid values: 0 to 100. This element is available when the task is in the Processing or Finished state.
            estimated_remaining_time (str, optional): The estimated period of time that is required for the redundancy type change task. Unit: hours. This element is available when the task is in the Processing or Finished state.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.task_id = task_id
        self.status = status
        self.create_time = create_time
        self.start_time = start_time
        self.end_time = end_time
        self.process_percentage = process_percentage
        self.estimated_remaining_time = estimated_remaining_time


class ListBucketDataRedundancyTransition(serde.Model):
    """
    The container for listed redundancy type change tasks.
    """

    _attribute_map = { 
        'bucket_data_redundancy_transition': {'tag': 'xml', 'rename': 'BucketDataRedundancyTransition', 'type': '[BucketDataRedundancyTransition]'},
        'is_truncated': {'tag': 'xml', 'rename': 'IsTruncated', 'type': 'bool'},
        'next_continuation_token': {'tag': 'xml', 'rename': 'NextContinuationToken', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ListBucketDataRedundancyTransition'
    }

    _dependency_map = { 
        'BucketDataRedundancyTransition': {'new': lambda: BucketDataRedundancyTransition()},
    }

    def __init__(
        self,
        bucket_data_redundancy_transition: Optional[List[BucketDataRedundancyTransition]] = None,
        is_truncated: Optional[bool] = None,
        next_continuation_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket_data_redundancy_transition (List[BucketDataRedundancyTransition], optional): The container in which the redundancy type conversion task is stored.
            is_truncated (bool, optional): Specifies whether to list all inventory tasks configured for the bucket.Valid values: true and false- The value of false indicates that all inventory tasks configured for the bucket are listed.- The value of true indicates that not all inventory tasks configured for the bucket are listed. To list the next page of inventory configurations, set the continuation-token parameter in the next request to the value of the NextContinuationToken header in the response to the current request.
            next_continuation_token (str, optional): If the value of IsTruncated in the response is true and value of this header is not null, set the continuation-token parameter in the next request to the value of this header.
        """
        super().__init__(**kwargs)
        self.bucket_data_redundancy_transition = bucket_data_redundancy_transition
        self.is_truncated = is_truncated
        self.next_continuation_token = next_continuation_token


class CreateBucketDataRedundancyTransitionRequest(serde.RequestModel):
    """
    The request for the CreateBucketDataRedundancyTransition operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'target_redundancy_type': {'tag': 'input', 'position': 'query', 'rename': 'x-oss-target-redundancy-type', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        target_redundancy_type: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            target_redundancy_type (str, required): The redundancy type to which you want to convert the bucket. You can only convert the redundancy type of a bucket from LRS to ZRS.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.target_redundancy_type = target_redundancy_type


class CreateBucketDataRedundancyTransitionResult(serde.ResultModel):
    """
    The request for the CreateBucketDataRedundancyTransition operation.
    """

    _attribute_map = { 
        'bucket_data_redundancy_transition': {'tag': 'output', 'position': 'body', 'rename': 'BucketDataRedundancyTransition', 'type': 'BucketDataRedundancyTransition,xml'},
    }

    _dependency_map = { 
        'BucketDataRedundancyTransition': {'new': lambda: BucketDataRedundancyTransition()},
    }

    def __init__(
        self,
        bucket_data_redundancy_transition: Optional[BucketDataRedundancyTransition] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket_data_redundancy_transition (BucketDataRedundancyTransition, optional): The container in which the redundancy type conversion task is stored.
        """
        super().__init__(**kwargs)
        self.bucket_data_redundancy_transition = bucket_data_redundancy_transition

class GetBucketDataRedundancyTransitionRequest(serde.RequestModel):
    """
    The request for the GetBucketDataRedundancyTransition operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'redundancy_transition_taskid': {'tag': 'input', 'position': 'query', 'rename': 'x-oss-redundancy-transition-taskid', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        redundancy_transition_taskid: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            redundancy_transition_taskid (str, required): The ID of the redundancy change task.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.redundancy_transition_taskid = redundancy_transition_taskid


class GetBucketDataRedundancyTransitionResult(serde.ResultModel):
    """
    The request for the GetBucketDataRedundancyTransition operation.
    """

    _attribute_map = {
        'bucket_data_redundancy_transition': {'tag': 'output', 'position': 'body', 'rename': 'BucketDataRedundancyTransition', 'type': 'BucketDataRedundancyTransition,xml'},
    }

    _dependency_map = {
        'BucketDataRedundancyTransition': {'new': lambda: BucketDataRedundancyTransition()},
    }

    def __init__(
        self,
        bucket_data_redundancy_transition: Optional[BucketDataRedundancyTransition] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket_data_redundancy_transition (BucketDataRedundancyTransition, optional): The container for a specific redundancy type change task.
        """
        super().__init__(**kwargs)
        self.bucket_data_redundancy_transition = bucket_data_redundancy_transition


class ListBucketDataRedundancyTransitionRequest(serde.RequestModel):
    """
    The request for the ListBucketDataRedundancyTransition operation.
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
            bucket (str, required):
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class ListBucketDataRedundancyTransitionResult(serde.ResultModel):
    """
    The request for the ListBucketDataRedundancyTransition operation.
    """

    _attribute_map = {
        'list_bucket_data_redundancy_transition': {'tag': 'output', 'position': 'body', 'rename': 'ListBucketDataRedundancyTransition', 'type': 'ListBucketDataRedundancyTransition,xml'},

    }

    _dependency_map = {
        'ListBucketDataRedundancyTransition': {'new': lambda: ListBucketDataRedundancyTransition()},
    }

    def __init__(
        self,
        list_bucket_data_redundancy_transition: Optional[ListBucketDataRedundancyTransition] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            list_bucket_data_redundancy_transition (ListBucketDataRedundancyTransition, optional): The container for listed redundancy type change tasks.
        """
        super().__init__(**kwargs)
        self.list_bucket_data_redundancy_transition = list_bucket_data_redundancy_transition


class ListUserDataRedundancyTransitionRequest(serde.RequestModel):
    """
    The request for the ListUserDataRedundancyTransitionRequest operation.
    """

    _attribute_map = {
        'max_keys': {'tag': 'input', 'position': 'query', 'rename': 'max-keys', 'type': 'int'},
        'continuation_token': {'tag': 'input', 'position': 'query', 'rename': 'continuation-token', 'type': 'str'},
    }

    def __init__(
        self,
        max_keys: Optional[Union[str, int]] = None,
        continuation_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            max_keys (Union[str, int], optional): The maximum number of access points that can be returned. Valid values:*   For user-level access points: (0,1000].*   For bucket-level access points: (0,100].
            continuation_token (str, optional): The token from which the listing operation starts. You must specify the value of NextContinuationToken that is obtained from the previous query as the value of continuation-token.
        """
        super().__init__(**kwargs)
        self.max_keys = max_keys
        self.continuation_token = continuation_token


class ListUserDataRedundancyTransitionResult(serde.ResultModel):
    """
    The request for the ListUserDataRedundancyTransitionRequest operation.
    """

    _attribute_map = {
        'list_bucket_data_redundancy_transition': {'tag': 'output', 'position': 'body', 'rename': 'ListBucketDataRedundancyTransition', 'type': 'ListBucketDataRedundancyTransition,xml'},

    }

    _dependency_map = {
        'ListBucketDataRedundancyTransition': {'new': lambda: ListBucketDataRedundancyTransition()},
    }

    def __init__(
        self,
        list_bucket_data_redundancy_transition: Optional[ListBucketDataRedundancyTransition] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            list_bucket_data_redundancy_transition (ListBucketDataRedundancyTransition, optional): The container for listed redundancy type change tasks.
        """
        super().__init__(**kwargs)
        self.list_bucket_data_redundancy_transition = list_bucket_data_redundancy_transition


class DeleteBucketDataRedundancyTransitionRequest(serde.RequestModel):
    """
    The request for the DeleteBucketDataRedundancyTransition operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'redundancy_transition_taskid': {'tag': 'input', 'position': 'query', 'rename': 'x-oss-redundancy-transition-taskid', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        redundancy_transition_taskid: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            redundancy_transition_taskid (str, required): The ID of the redundancy type change task.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.redundancy_transition_taskid = redundancy_transition_taskid


class DeleteBucketDataRedundancyTransitionResult(serde.ResultModel):
    """
    The request for the DeleteBucketDataRedundancyTransition operation.
    """
