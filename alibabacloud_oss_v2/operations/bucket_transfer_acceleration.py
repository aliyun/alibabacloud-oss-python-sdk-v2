# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_transfer_acceleration(client: _SyncClientImpl, request: models.PutBucketTransferAccelerationRequest, **kwargs) -> models.PutBucketTransferAccelerationResult:
    """
    put_bucket_transfer_acceleration synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketTransferAccelerationRequest): The request for the PutBucketTransferAcceleration operation.

    Returns:
        PutBucketTransferAccelerationResult: The result for the PutBucketTransferAcceleration operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketTransferAcceleration',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'transferAcceleration': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['transferAcceleration']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketTransferAccelerationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_transfer_acceleration(client: _SyncClientImpl, request: models.GetBucketTransferAccelerationRequest, **kwargs) -> models.GetBucketTransferAccelerationResult:
    """
    get_bucket_transfer_acceleration synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketTransferAccelerationRequest): The request for the GetBucketTransferAcceleration operation.

    Returns:
        GetBucketTransferAccelerationResult: The result for the GetBucketTransferAcceleration operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketTransferAcceleration',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'transferAcceleration': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['transferAcceleration']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketTransferAccelerationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
