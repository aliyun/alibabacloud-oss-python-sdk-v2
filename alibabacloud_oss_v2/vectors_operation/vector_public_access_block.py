# pylint: disable=line-too-long
from alibabacloud_oss_v2._client import _SyncClientImpl
from alibabacloud_oss_v2.types import OperationInput, CaseInsensitiveDict
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import serde_utils
from alibabacloud_oss_v2 import models


def put_public_access_block_vector(client: _SyncClientImpl, request: models.PutPublicAccessBlockRequest, **kwargs) -> models.PutPublicAccessBlockResult:
    """
    put_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutPublicAccessBlockRequest): The request for the PutPublicAccessBlock operation.

    Returns:
        PutPublicAccessBlockResult: The result for the PutPublicAccessBlock operation.
    """

    op_input = serde.serialize_inputs_jsons_json(
        request=request,
        op_input=OperationInput(
            op_name='PutPublicAccessBlock',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={ 
                'publicAccessBlock': '', 
            },
            op_metadata={'sub-resource': ['publicAccessBlock']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )

def get_public_access_block_vector(client: _SyncClientImpl, request: models.GetPublicAccessBlockRequest, **kwargs) -> models.GetPublicAccessBlockResult:
    """
    get_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetPublicAccessBlockRequest): The request for the GetPublicAccessBlock operation.

    Returns:
        GetPublicAccessBlockResult: The result for the GetPublicAccessBlock operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='GetPublicAccessBlock',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'publicAccessBlock': '',
            },
            op_metadata={'sub-resource': ['publicAccessBlock']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def delete_public_access_block_vector(client: _SyncClientImpl, request: models.DeletePublicAccessBlockRequest, **kwargs) -> models.DeletePublicAccessBlockResult:
    """
    delete_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeletePublicAccessBlockRequest): The request for the DeletePublicAccessBlock operation.

    Returns:
        DeletePublicAccessBlockResult: The result for the DeletePublicAccessBlock operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='DeletePublicAccessBlock',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={ 
                'publicAccessBlock': '', 
            },
            op_metadata={'sub-resource': ['publicAccessBlock']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeletePublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )

