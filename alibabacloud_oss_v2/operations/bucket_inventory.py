# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_inventory(client: _SyncClientImpl, request: models.PutBucketInventoryRequest, **kwargs) -> models.PutBucketInventoryResult:
    """
    put_bucket_inventory synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketInventoryRequest): The request for the PutBucketInventory operation.

    Returns:
        PutBucketInventoryResult: The result for the PutBucketInventory operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketInventory',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'inventory': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['inventory', 'inventoryId']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketInventoryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_inventory(client: _SyncClientImpl, request: models.GetBucketInventoryRequest, **kwargs) -> models.GetBucketInventoryResult:
    """
    get_bucket_inventory synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketInventoryRequest): The request for the GetBucketInventory operation.

    Returns:
        GetBucketInventoryResult: The result for the GetBucketInventory operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketInventory',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'inventory': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['inventory', 'inventoryId']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketInventoryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def list_bucket_inventory(client: _SyncClientImpl, request: models.ListBucketInventoryRequest, **kwargs) -> models.ListBucketInventoryResult:
    """
    list_bucket_inventory synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListBucketInventoryRequest): The request for the ListBucketInventory operation.

    Returns:
        ListBucketInventoryResult: The result for the ListBucketInventory operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListBucketInventory',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'inventory': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['inventory', 'inventoryId']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListBucketInventoryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_inventory(client: _SyncClientImpl, request: models.DeleteBucketInventoryRequest, **kwargs) -> models.DeleteBucketInventoryResult:
    """
    delete_bucket_inventory synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketInventoryRequest): The request for the DeleteBucketInventory operation.

    Returns:
        DeleteBucketInventoryResult: The result for the DeleteBucketInventory operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketInventory',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'inventory': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['inventory', 'inventoryId']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketInventoryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
