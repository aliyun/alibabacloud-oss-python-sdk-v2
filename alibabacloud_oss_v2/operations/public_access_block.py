# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def get_public_access_block(client: _SyncClientImpl, request: models.GetPublicAccessBlockRequest, **kwargs) -> models.GetPublicAccessBlockResult:
    """
    get_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetPublicAccessBlockRequest): The request for the GetPublicAccessBlock operation.

    Returns:
        GetPublicAccessBlockResult: The result for the GetPublicAccessBlock operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetPublicAccessBlock',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
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
            serde.deserialize_output_xmlbody
        ],
    )

def put_public_access_block(client: _SyncClientImpl, request: models.PutPublicAccessBlockRequest, **kwargs) -> models.PutPublicAccessBlockResult:
    """
    put_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutPublicAccessBlockRequest): The request for the PutPublicAccessBlock operation.

    Returns:
        PutPublicAccessBlockResult: The result for the PutPublicAccessBlock operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutPublicAccessBlock',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
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
            serde.deserialize_output_xmlbody
        ],
    )

def delete_public_access_block(client: _SyncClientImpl, request: models.DeletePublicAccessBlockRequest, **kwargs) -> models.DeletePublicAccessBlockResult:
    """
    delete_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeletePublicAccessBlockRequest): The request for the DeletePublicAccessBlock operation.

    Returns:
        DeletePublicAccessBlockResult: The result for the DeletePublicAccessBlock operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeletePublicAccessBlock',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
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
            serde.deserialize_output_xmlbody
        ],
    )
