# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_access_point_public_access_block(client: _SyncClientImpl, request: models.PutAccessPointPublicAccessBlockRequest, **kwargs) -> models.PutAccessPointPublicAccessBlockResult:
    """
    put_access_point_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutAccessPointPublicAccessBlockRequest): The request for the PutAccessPointPublicAccessBlock operation.

    Returns:
        PutAccessPointPublicAccessBlockResult: The result for the PutAccessPointPublicAccessBlock operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutAccessPointPublicAccessBlock',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'publicAccessBlock': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['publicAccessBlock', 'x-oss-access-point-name']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutAccessPointPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_access_point_public_access_block(client: _SyncClientImpl, request: models.GetAccessPointPublicAccessBlockRequest, **kwargs) -> models.GetAccessPointPublicAccessBlockResult:
    """
    get_access_point_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetAccessPointPublicAccessBlockRequest): The request for the GetAccessPointPublicAccessBlock operation.

    Returns:
        GetAccessPointPublicAccessBlockResult: The result for the GetAccessPointPublicAccessBlock operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAccessPointPublicAccessBlock',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'publicAccessBlock': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['publicAccessBlock', 'x-oss-access-point-name']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetAccessPointPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def delete_access_point_public_access_block(client: _SyncClientImpl, request: models.DeleteAccessPointPublicAccessBlockRequest, **kwargs) -> models.DeleteAccessPointPublicAccessBlockResult:
    """
    delete_access_point_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteAccessPointPublicAccessBlockRequest): The request for the DeleteAccessPointPublicAccessBlock operation.

    Returns:
        DeleteAccessPointPublicAccessBlockResult: The result for the DeleteAccessPointPublicAccessBlock operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteAccessPointPublicAccessBlock',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'publicAccessBlock': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['publicAccessBlock', 'x-oss-access-point-name']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteAccessPointPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
