# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_style(client: _SyncClientImpl, request: models.PutStyleRequest, **kwargs) -> models.PutStyleResult:
    """
    put_style synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutStyleRequest): The request for the PutStyle operation.

    Returns:
        PutStyleResult: The result for the PutStyle operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutStyle',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'style': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['style', 'styleName']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutStyleResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def list_style(client: _SyncClientImpl, request: models.ListStyleRequest, **kwargs) -> models.ListStyleResult:
    """
    list_style synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListStyleRequest): The request for the ListStyle operation.

    Returns:
        ListStyleResult: The result for the ListStyle operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListStyle',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'style': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['style']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListStyleResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_style(client: _SyncClientImpl, request: models.GetStyleRequest, **kwargs) -> models.GetStyleResult:
    """
    get_style synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetStyleRequest): The request for the GetStyle operation.

    Returns:
        GetStyleResult: The result for the GetStyle operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetStyle',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'style': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['style', 'styleName']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetStyleResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_style(client: _SyncClientImpl, request: models.DeleteStyleRequest, **kwargs) -> models.DeleteStyleResult:
    """
    delete_style synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteStyleRequest): The request for the DeleteStyle operation.

    Returns:
        DeleteStyleResult: The result for the DeleteStyle operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteStyle',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'style': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['style', 'styleName']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteStyleResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
