# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_overwrite_config(client: _SyncClientImpl, request: models.PutBucketOverwriteConfigRequest, **kwargs) -> models.PutBucketOverwriteConfigResult:
    """
    put_bucket_overwrite_config synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketOverwriteConfigRequest): The request for the PutBucketOverwriteConfig operation.

    Returns:
        PutBucketOverwriteConfigResult: The result for the PutBucketOverwriteConfig operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketOverwriteConfig',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'overwriteConfig': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['overwriteConfig']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketOverwriteConfigResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_overwrite_config(client: _SyncClientImpl, request: models.GetBucketOverwriteConfigRequest, **kwargs) -> models.GetBucketOverwriteConfigResult:
    """
    get_bucket_overwrite_config synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketOverwriteConfigRequest): The request for the GetBucketOverwriteConfig operation.

    Returns:
        GetBucketOverwriteConfigResult: The result for the GetBucketOverwriteConfig operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketOverwriteConfig',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'overwriteConfig': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['overwriteConfig']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketOverwriteConfigResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_overwrite_config(client: _SyncClientImpl, request: models.DeleteBucketOverwriteConfigRequest, **kwargs) -> models.DeleteBucketOverwriteConfigResult:
    """
    delete_bucket_overwrite_config synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketOverwriteConfigRequest): The request for the DeleteBucketOverwriteConfig operation.

    Returns:
        DeleteBucketOverwriteConfigResult: The result for the DeleteBucketOverwriteConfig operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketOverwriteConfig',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'overwriteConfig': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['overwriteConfig']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketOverwriteConfigResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
