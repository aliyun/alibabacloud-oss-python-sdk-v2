# pylint: disable=line-too-long
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models
from ._serde import serialize_input_vector_json_model
from ._serde import deserialize_output_vector_json_model

def put_vector_index(client: _SyncClientImpl, request: models.PutVectorIndexRequest, **kwargs) -> models.PutVectorIndexResult:
    """
    put_vector_index synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutVectorIndexRequest): The request for the PutVectorIndex operation.

    Returns:
        PutVectorIndexResult: The result for the PutVectorIndex operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='PutVectorIndex',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'putVectorIndex': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutVectorIndexResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )


def get_vector_index(client: _SyncClientImpl, request: models.GetVectorIndexRequest, **kwargs) -> models.GetVectorIndexResult:
    """
    get_vector_index synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetVectorIndexRequest): The request for the GetVectorIndex operation.

    Returns:
        GetVectorIndexResult: The result for the GetVectorIndex operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetVectorIndex',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'getVectorIndex': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetVectorIndexResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )


def list_vector_indexes(client: _SyncClientImpl, request: models.ListVectorIndexesRequest, **kwargs) -> models.ListVectorIndexesResult:
    """
    list_vector_index synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListVectorIndexesRequest): The request for the ListVectorIndexes operation.

    Returns:
        ListVectorIndexesResult: The result for the ListVectorIndexes operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='ListVectorIndexes',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'listVectorIndexes': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListVectorIndexesResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )


def delete_vector_index(client: _SyncClientImpl, request: models.DeleteVectorIndexRequest, **kwargs) -> models.DeleteVectorIndexResult:
    """
    delete_vector_index synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteVectorIndexRequest): The request for the DeleteVectorIndex operation.

    Returns:
        DeleteVectorIndexResult: The result for the DeleteVectorIndex operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='DeleteVectorIndex',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'deleteVectorIndex': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteVectorIndexResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )
