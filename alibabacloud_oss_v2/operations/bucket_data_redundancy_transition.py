# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def create_bucket_data_redundancy_transition(client: _SyncClientImpl, request: models.CreateBucketDataRedundancyTransitionRequest, **kwargs) -> models.CreateBucketDataRedundancyTransitionResult:
    """
    create_bucket_data_redundancy_transition synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (CreateBucketDataRedundancyTransitionRequest): The request for the CreateBucketDataRedundancyTransition operation.

    Returns:
        CreateBucketDataRedundancyTransitionResult: The result for the CreateBucketDataRedundancyTransition operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateBucketDataRedundancyTransition',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'redundancyTransition': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['redundancyTransition', 'x-oss-target-redundancy-type']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CreateBucketDataRedundancyTransitionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_data_redundancy_transition(client: _SyncClientImpl, request: models.GetBucketDataRedundancyTransitionRequest, **kwargs) -> models.GetBucketDataRedundancyTransitionResult:
    """
    get_bucket_data_redundancy_transition synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketDataRedundancyTransitionRequest): The request for the GetBucketDataRedundancyTransition operation.

    Returns:
        GetBucketDataRedundancyTransitionResult: The result for the GetBucketDataRedundancyTransition operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketDataRedundancyTransition',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'redundancyTransition': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['redundancyTransition', 'x-oss-redundancy-transition-taskid']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketDataRedundancyTransitionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def list_bucket_data_redundancy_transition(client: _SyncClientImpl, request: models.ListBucketDataRedundancyTransitionRequest, **kwargs) -> models.ListBucketDataRedundancyTransitionResult:
    """
    list_bucket_data_redundancy_transition synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListBucketDataRedundancyTransitionRequest): The request for the ListBucketDataRedundancyTransition operation.

    Returns:
        ListBucketDataRedundancyTransitionResult: The result for the ListBucketDataRedundancyTransition operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListBucketDataRedundancyTransition',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'redundancyTransition': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['redundancyTransition']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListBucketDataRedundancyTransitionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def list_user_data_redundancy_transition(client: _SyncClientImpl, request: models.ListUserDataRedundancyTransitionRequest, **kwargs) -> models.ListUserDataRedundancyTransitionResult:
    """
    list_user_data_redundancy_transition synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListUserDataRedundancyTransitionRequest): The request for the ListUserDataRedundancyTransition operation.

    Returns:
        ListUserDataRedundancyTransitionResult: The result for the ListUserDataRedundancyTransition operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListUserDataRedundancyTransition',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'redundancyTransition': '',
            },
            op_metadata={'sub-resource': ['redundancyTransition']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListUserDataRedundancyTransitionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_data_redundancy_transition(client: _SyncClientImpl, request: models.DeleteBucketDataRedundancyTransitionRequest, **kwargs) -> models.DeleteBucketDataRedundancyTransitionResult:
    """
    delete_bucket_data_redundancy_transition synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketDataRedundancyTransitionRequest): The request for the DeleteBucketDataRedundancyTransition operation.

    Returns:
        DeleteBucketDataRedundancyTransitionResult: The result for the DeleteBucketDataRedundancyTransition operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketDataRedundancyTransition',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'redundancyTransition': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['redundancyTransition', 'x-oss-redundancy-transition-taskid']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketDataRedundancyTransitionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
