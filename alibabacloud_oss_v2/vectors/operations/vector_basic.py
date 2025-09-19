# pylint: disable=line-too-long
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models
from ._serde import serialize_input_vector_json_model
from ._serde import deserialize_output_vector_json_model

def put_vectors(client: _SyncClientImpl, request: models.PutVectorsRequest, **kwargs) -> models.PutVectorsResult:
    """
    put_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutVectorsRequest): The request for the PutVectors operation.

    Returns:
        PutVectorsResult: The result for the PutVectors operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='PutVectors',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'putVectors': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )


def get_vectors(client: _SyncClientImpl, request: models.GetVectorsRequest, **kwargs) -> models.GetVectorsResult:
    """
    get_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetVectorsRequest): The request for the GetVectors operation.

    Returns:
        GetVectorsResult: The result for the GetVectors operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetVectors',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'getVectors': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )


def list_vectors(client: _SyncClientImpl, request: models.ListVectorsRequest, **kwargs) -> models.ListVectorsResult:
    """
    list_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListVectorsRequest): The request for the ListVectors operation.

    Returns:
        ListVectorsResult: The result for the ListVectors operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='ListVectors',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'listVectors': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )


def delete_vectors(client: _SyncClientImpl, request: models.DeleteVectorsRequest, **kwargs) -> models.DeleteVectorsResult:
    """
    delete_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteVectorsRequest): The request for the DeleteVectors operation.

    Returns:
        DeleteVectorsResult: The result for the DeleteVectors operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='DeleteVectors',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'deleteVectors': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )


def query_vectors(client: _SyncClientImpl, request: models.QueryVectorsRequest, **kwargs) -> models.QueryVectorsResult:
    """
    query_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (QueryVectorsRequest): The request for the QueryVectors operation.

    Returns:
        QueryVectorsResult: The result for the QueryVectors operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='QueryVectors',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'queryVectors': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.QueryVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )
