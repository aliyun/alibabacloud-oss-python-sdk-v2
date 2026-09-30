# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_storage_quota(client: _SyncClientImpl, request: models.PutBucketStorageQuotaRequest, **kwargs) -> models.PutBucketStorageQuotaResult:
    """
    put_bucket_storage_quota synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketStorageQuotaRequest): The request for the PutBucketStorageQuota operation.

    Returns:
        PutBucketStorageQuotaResult: The result for the PutBucketStorageQuota operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketStorageQuota',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'quota': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['quota']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketStorageQuotaResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def get_bucket_storage_quota(client: _SyncClientImpl, request: models.GetBucketStorageQuotaRequest, **kwargs) -> models.GetBucketStorageQuotaResult:
    """
    get_bucket_storage_quota synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketStorageQuotaRequest): The request for the GetBucketStorageQuota operation.

    Returns:
        GetBucketStorageQuotaResult: The result for the GetBucketStorageQuota operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketStorageQuota',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'quota': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['quota']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketStorageQuotaResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def delete_bucket_storage_quota(client: _SyncClientImpl, request: models.DeleteBucketStorageQuotaRequest, **kwargs) -> models.DeleteBucketStorageQuotaResult:
    """
    delete_bucket_storage_quota synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketStorageQuotaRequest): The request for the DeleteBucketStorageQuota operation.

    Returns:
        DeleteBucketStorageQuotaResult: The result for the DeleteBucketStorageQuota operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketStorageQuota',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'quota': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['quota']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketStorageQuotaResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
