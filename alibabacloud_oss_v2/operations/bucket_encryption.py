# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_encryption(client: _SyncClientImpl, request: models.PutBucketEncryptionRequest, **kwargs) -> models.PutBucketEncryptionResult:
    """
    put_bucket_encryption synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketEncryptionRequest): The request for the PutBucketEncryption operation.

    Returns:
        PutBucketEncryptionResult: The result for the PutBucketEncryption operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketEncryption',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'encryption': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['encryption']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketEncryptionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_encryption(client: _SyncClientImpl, request: models.GetBucketEncryptionRequest, **kwargs) -> models.GetBucketEncryptionResult:
    """
    get_bucket_encryption synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketEncryptionRequest): The request for the GetBucketEncryption operation.

    Returns:
        GetBucketEncryptionResult: The result for the GetBucketEncryption operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketEncryption',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'encryption': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['encryption']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketEncryptionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_encryption(client: _SyncClientImpl, request: models.DeleteBucketEncryptionRequest, **kwargs) -> models.DeleteBucketEncryptionResult:
    """
    delete_bucket_encryption synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketEncryptionRequest): The request for the DeleteBucketEncryption operation.

    Returns:
        DeleteBucketEncryptionResult: The result for the DeleteBucketEncryption operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketEncryption',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'encryption': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['encryption']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketEncryptionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
