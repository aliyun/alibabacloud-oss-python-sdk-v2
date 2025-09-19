# pylint: disable=line-too-long
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models

def put_bucket_policy(client: _SyncClientImpl, request: models.PutBucketPolicyRequest, **kwargs) -> models.PutBucketPolicyResult:
    """
    put_bucket_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketPolicyRequest): The request for the PutBucketPolicy operation.

    Returns:
        PutBucketPolicyResult: The result for the PutBucketPolicy operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketPolicy',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'policy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['policy']},
        )
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketPolicyResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )

def get_bucket_policy(client: _SyncClientImpl, request: models.GetBucketPolicyRequest, **kwargs) -> models.GetBucketPolicyResult:
    """
    get_bucket_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketPolicyRequest): The request for the GetBucketPolicy operation.

    Returns:
        GetBucketPolicyResult: The result for the GetBucketPolicy operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketPolicy',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'policy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['policy']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketPolicyResult(
            body=op_output.http_response.content.decode()
        ),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )

def delete_bucket_policy(client: _SyncClientImpl, request: models.DeleteBucketPolicyRequest, **kwargs) -> models.DeleteBucketPolicyResult:
    """
    delete_bucket_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketPolicyRequest): The request for the DeleteBucketPolicy operation.

    Returns:
        DeleteBucketPolicyResult: The result for the DeleteBucketPolicy operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketPolicy',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'policy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['policy']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketPolicyResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )

