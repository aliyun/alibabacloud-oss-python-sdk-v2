# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def get_bucket_resource_group(client: _SyncClientImpl, request: models.GetBucketResourceGroupRequest, **kwargs) -> models.GetBucketResourceGroupResult:
    """
    get_bucket_resource_group synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketResourceGroupRequest): The request for the GetBucketResourceGroup operation.

    Returns:
        GetBucketResourceGroupResult: The result for the GetBucketResourceGroup operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketResourceGroup',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'resourceGroup': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['resourceGroup']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketResourceGroupResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_bucket_resource_group(client: _SyncClientImpl, request: models.PutBucketResourceGroupRequest, **kwargs) -> models.PutBucketResourceGroupResult:
    """
    put_bucket_resource_group synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketResourceGroupRequest): The request for the PutBucketResourceGroup operation.

    Returns:
        PutBucketResourceGroupResult: The result for the PutBucketResourceGroup operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketResourceGroup',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'resourceGroup': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['resourceGroup']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketResourceGroupResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
