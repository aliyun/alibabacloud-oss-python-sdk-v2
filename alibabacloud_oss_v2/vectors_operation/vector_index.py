# pylint: disable=line-too-long
from alibabacloud_oss_v2._client import _SyncClientImpl
from alibabacloud_oss_v2.types import OperationInput, CaseInsensitiveDict
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import serde_utils
from alibabacloud_oss_v2 import vector_models


def put_vector_index(client: _SyncClientImpl, request: vector_models.PutVectorIndexRequest, **kwargs) -> vector_models.PutVectorIndexResult:
    """
    put_vector_index synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutVectorIndexRequest): The request for the PutVectorIndex operation.

    Returns:
        PutVectorIndexResult: The result for the PutVectorIndex operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='PutVectorIndex',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'PutVectorIndex': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['PutVectorIndex']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=vector_models.PutVectorIndexResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def get_vector_index(client: _SyncClientImpl, request: vector_models.GetVectorIndexRequest, **kwargs) -> vector_models.GetVectorIndexResult:
    """
    get_vector_index synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetVectorIndexRequest): The request for the GetVectorIndex operation.

    Returns:
        GetVectorIndexResult: The result for the GetVectorIndex operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='GetVectorIndex',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'GetVectorIndex': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['GetVectorIndex']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=vector_models.GetVectorIndexResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def list_vector_index(client: _SyncClientImpl, request: vector_models.ListVectorsIndexRequest, **kwargs) -> vector_models.ListVectorsIndexResult:
    """
    list_vector_index synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListVectorsIndexRequest): The request for the ListVectorIndex operation.

    Returns:
        ListVectorsIndexResult: The result for the ListVectorIndex operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='ListVectorIndex',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'ListVectorIndexes': '',
                'maxResults': request.max_results,
                'nextToken': request.next_token,
                'prefix': request.prefix,
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['ListVectorIndexes']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=vector_models.ListVectorsIndexResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )


def delete_vector_index(client: _SyncClientImpl, request: vector_models.DeleteVectorIndexRequest, **kwargs) -> vector_models.DeleteVectorIndexResult:
    """
    delete_vector_index synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteVectorIndexRequest): The request for the DeleteVectorIndex operation.

    Returns:
        DeleteVectorIndexResult: The result for the DeleteVectorIndex operation.
    """

    op_input = serde.serialize_input_json(
        request=request,
        op_input=OperationInput(
            op_name='DeleteVectorIndex',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'DeleteVectorIndex': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['DeleteVectorIndex']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=vector_models.DeleteVectorIndexResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_jsonbody
        ],
    )
