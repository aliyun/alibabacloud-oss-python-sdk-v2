# pylint: disable=line-too-long
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models


def put_vector_bucket(client: _SyncClientImpl, request: models.PutVectorBucketRequest, **kwargs) -> models.PutVectorBucketResult:
    """
    put bucket synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutVectorBucketRequest): The request for the PutVectorBucket operation.

    Returns:
        PutVectorBucketResult: The result for the PutVectorBucket operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='PutVectorBucket',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutVectorBucketResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_discardbody
        ],
    )

def get_vector_bucket(client: _SyncClientImpl, request: models.GetVectorBucketRequest, **kwargs) -> models.GetVectorBucketResult:
    """
    GetBucketInfo Queries information about a bucket.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetVectorBucketRequest): The request for the GetVectorBucket operation.

    Returns:
        GetVectorBucketResult: The result for the GetVectorBucket operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='GetVectorBucket',
            method='GET',
            parameters={
                'bucketInfo': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetVectorBucketResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def delete_vector_bucket(client: _SyncClientImpl, request: models.DeleteVectorBucketRequest, **kwargs) -> models.DeleteVectorBucketResult:
    """
    delete bucket synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteVectorBucketRequest): The request for the DeleteVectorBucket operation.

    Returns:
        DeleteVectorBucketResult: The result for the DeleteVectorBucket operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='DeleteVectorBucket',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteVectorBucketResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_discardbody
        ],
    )


def list_vector_buckets(client: _SyncClientImpl, request: models.ListVectorBucketsRequest, **kwargs) -> models.ListVectorBucketsResult:
    """
    list buckets synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListVectorBucketsRequest): The request for the ListVectorBuckets operation.

    Returns:
        ListVectorBucketsResult: The result for the ListVectorBuckets operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='ListVectorBuckets',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/octet-stream',
            }),
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListVectorBucketsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody,
        ],
    )


