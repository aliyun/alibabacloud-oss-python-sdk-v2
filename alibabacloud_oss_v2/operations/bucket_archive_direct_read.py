# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def get_bucket_archive_direct_read(client: _SyncClientImpl, request: models.GetBucketArchiveDirectReadRequest, **kwargs) -> models.GetBucketArchiveDirectReadResult:
    """
    get_bucket_archive_direct_read synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketArchiveDirectReadRequest): The request for the GetBucketArchiveDirectRead operation.

    Returns:
        GetBucketArchiveDirectReadResult: The result for the GetBucketArchiveDirectRead operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketArchiveDirectRead',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'bucketArchiveDirectRead': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['bucketArchiveDirectRead']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketArchiveDirectReadResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_bucket_archive_direct_read(client: _SyncClientImpl, request: models.PutBucketArchiveDirectReadRequest, **kwargs) -> models.PutBucketArchiveDirectReadResult:
    """
    put_bucket_archive_direct_read synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketArchiveDirectReadRequest): The request for the PutBucketArchiveDirectRead operation.

    Returns:
        PutBucketArchiveDirectReadResult: The result for the PutBucketArchiveDirectRead operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketArchiveDirectRead',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'bucketArchiveDirectRead': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['bucketArchiveDirectRead']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketArchiveDirectReadResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
