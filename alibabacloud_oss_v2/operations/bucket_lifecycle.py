# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_lifecycle(client: _SyncClientImpl, request: models.PutBucketLifecycleRequest, **kwargs) -> models.PutBucketLifecycleResult:
    """
    put_bucket_lifecycle synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketLifecycleRequest): The request for the PutBucketLifecycle operation.

    Returns:
        PutBucketLifecycleResult: The result for the PutBucketLifecycle operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketLifecycle',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'lifecycle': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['lifecycle']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketLifecycleResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_lifecycle(client: _SyncClientImpl, request: models.GetBucketLifecycleRequest, **kwargs) -> models.GetBucketLifecycleResult:
    """
    get_bucket_lifecycle synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketLifecycleRequest): The request for the GetBucketLifecycle operation.

    Returns:
        GetBucketLifecycleResult: The result for the GetBucketLifecycle operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketLifecycle',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'lifecycle': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['lifecycle']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketLifecycleResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_lifecycle(client: _SyncClientImpl, request: models.DeleteBucketLifecycleRequest, **kwargs) -> models.DeleteBucketLifecycleResult:
    """
    delete_bucket_lifecycle synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketLifecycleRequest): The request for the DeleteBucketLifecycle operation.

    Returns:
        DeleteBucketLifecycleResult: The result for the DeleteBucketLifecycle operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketLifecycle',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'lifecycle': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['lifecycle']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketLifecycleResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
