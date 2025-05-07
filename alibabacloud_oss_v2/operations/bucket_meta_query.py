# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def get_meta_query_status(client: _SyncClientImpl, request: models.GetMetaQueryStatusRequest, **kwargs) -> models.GetMetaQueryStatusResult:
    """
    get_meta_query_status synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetMetaQueryStatusRequest): The request for the GetMetaQueryStatus operation.

    Returns:
        GetMetaQueryStatusResult: The result for the GetMetaQueryStatus operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetMetaQueryStatus',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'metaQuery': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetMetaQueryStatusResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def close_meta_query(client: _SyncClientImpl, request: models.CloseMetaQueryRequest, **kwargs) -> models.CloseMetaQueryResult:
    """
    close_meta_query synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (CloseMetaQueryRequest): The request for the CloseMetaQuery operation.

    Returns:
        CloseMetaQueryResult: The result for the CloseMetaQuery operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CloseMetaQuery',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'comp': 'delete', 
                'metaQuery': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'comp']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CloseMetaQueryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def do_meta_query(client: _SyncClientImpl, request: models.DoMetaQueryRequest, **kwargs) -> models.DoMetaQueryResult:
    """
    do_meta_query synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DoMetaQueryRequest): The request for the DoMetaQuery operation.

    Returns:
        DoMetaQueryResult: The result for the DoMetaQuery operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DoMetaQuery',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'comp': 'query', 
                'metaQuery': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'comp']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DoMetaQueryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def open_meta_query(client: _SyncClientImpl, request: models.OpenMetaQueryRequest, **kwargs) -> models.OpenMetaQueryResult:
    """
    open_meta_query synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (OpenMetaQueryRequest): The request for the OpenMetaQuery operation.

    Returns:
        OpenMetaQueryResult: The result for the OpenMetaQuery operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='OpenMetaQuery',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'comp': 'add', 
                'metaQuery': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'comp']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.OpenMetaQueryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
