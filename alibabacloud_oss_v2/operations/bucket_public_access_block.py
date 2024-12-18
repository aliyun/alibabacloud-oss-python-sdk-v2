# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def get_bucket_public_access_block(client: _SyncClientImpl, request: models.GetBucketPublicAccessBlockRequest, **kwargs) -> models.GetBucketPublicAccessBlockResult:
    """
    get_bucket_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketPublicAccessBlockRequest): The request for the GetBucketPublicAccessBlock operation.

    Returns:
        GetBucketPublicAccessBlockResult: The result for the GetBucketPublicAccessBlock operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketPublicAccessBlock',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'publicAccessBlock': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['publicAccessBlock']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_bucket_public_access_block(client: _SyncClientImpl, request: models.PutBucketPublicAccessBlockRequest, **kwargs) -> models.PutBucketPublicAccessBlockResult:
    """
    put_bucket_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketPublicAccessBlockRequest): The request for the PutBucketPublicAccessBlock operation.

    Returns:
        PutBucketPublicAccessBlockResult: The result for the PutBucketPublicAccessBlock operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketPublicAccessBlock',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'publicAccessBlock': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['publicAccessBlock']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_public_access_block(client: _SyncClientImpl, request: models.DeleteBucketPublicAccessBlockRequest, **kwargs) -> models.DeleteBucketPublicAccessBlockResult:
    """
    delete_bucket_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketPublicAccessBlockRequest): The request for the DeleteBucketPublicAccessBlock operation.

    Returns:
        DeleteBucketPublicAccessBlockResult: The result for the DeleteBucketPublicAccessBlock operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketPublicAccessBlock',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'publicAccessBlock': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['publicAccessBlock']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
