# pylint: disable=line-too-long
from alibabacloud_oss_v2._client import _SyncClientImpl
from alibabacloud_oss_v2.types import OperationInput, CaseInsensitiveDict
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import serde_utils
from alibabacloud_oss_v2 import vector_models


def put_vectors(client: _SyncClientImpl, request: vector_models.PutVectorsRequest, **kwargs) -> vector_models.PutVectorsResult:
    """
    put_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutVectorsRequest): The request for the PutVectors operation.

    Returns:
        PutVectorsResult: The result for the PutVectors operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='PutVectors',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'PutVectors': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['PutVectors']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=vector_models.PutVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def get_vectors(client: _SyncClientImpl, request: vector_models.GetVectorsRequest, **kwargs) -> vector_models.GetVectorsResult:
    """
    get_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetVectorsRequest): The request for the GetVectors operation.

    Returns:
        GetVectorsResult: The result for the GetVectors operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='GetVectors',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'GetVectors': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['GetVectors']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=vector_models.GetVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def list_vectors(client: _SyncClientImpl, request: vector_models.ListVectorsRequest, **kwargs) -> vector_models.ListVectorsResult:
    """
    list_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListVectorsRequest): The request for the ListVectors operation.

    Returns:
        ListVectorsResult: The result for the ListVectors operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='ListVectors',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'ListVectors': '',
                'maxResults': request.max_results,
                'nextToken': request.next_token,
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['ListVectors']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=vector_models.ListVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def delete_vectors(client: _SyncClientImpl, request: vector_models.DeleteVectorsRequest, **kwargs) -> vector_models.DeleteVectorsResult:
    """
    delete_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteVectorsRequest): The request for the DeleteVectors operation.

    Returns:
        DeleteVectorsResult: The result for the DeleteVectors operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='DeleteVectors',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'DeleteVectors': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['DeleteVectors']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=vector_models.DeleteVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def query_vectors(client: _SyncClientImpl, request: vector_models.QueryVectorsRequest, **kwargs) -> vector_models.QueryVectorsResult:
    """
    query_vectors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (QueryVectorsRequest): The request for the QueryVectors operation.

    Returns:
        QueryVectorsResult: The result for the QueryVectors operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='QueryVectors',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'QueryVectors': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['QueryVectors']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=vector_models.QueryVectorsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )
