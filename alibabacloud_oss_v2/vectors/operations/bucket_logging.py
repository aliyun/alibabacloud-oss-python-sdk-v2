# pylint: disable=line-too-long
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models


def put_bucket_logging(client: _SyncClientImpl, request: models.PutBucketLoggingRequest, **kwargs) -> models.PutBucketLoggingResult:
    """
    put_bucket_logging synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketLoggingRequest): The request for the PutBucketLogging operation.

    Returns:
        PutBucketLoggingResult: The result for the PutBucketLogging operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketLogging',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'logging': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['logging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketLoggingResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def get_bucket_logging(client: _SyncClientImpl, request: models.GetBucketLoggingRequest, **kwargs) -> models.GetBucketLoggingResult:
    """
    get_bucket_logging synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketLoggingRequest): The request for the GetBucketLogging operation.

    Returns:
        GetBucketLoggingResult: The result for the GetBucketLogging operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketLogging',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'logging': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['logging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketLoggingResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def delete_bucket_logging(client: _SyncClientImpl, request: models.DeleteBucketLoggingRequest, **kwargs) -> models.DeleteBucketLoggingResult:
    """
    delete_bucket_logging synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketLoggingRequest): The request for the DeleteBucketLogging operation.

    Returns:
        DeleteBucketLoggingResult: The result for the DeleteBucketLogging operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketLogging',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'logging': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['logging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketLoggingResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )
