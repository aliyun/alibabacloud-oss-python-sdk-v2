# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_cname(client: _SyncClientImpl, request: models.PutCnameRequest, **kwargs) -> models.PutCnameResult:
    """
    put_cname synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutCnameRequest): The request for the PutCname operation.

    Returns:
        PutCnameResult: The result for the PutCname operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutCname',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'cname': '', 
                'comp': 'add', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['cname', 'comp']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutCnameResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def list_cname(client: _SyncClientImpl, request: models.ListCnameRequest, **kwargs) -> models.ListCnameResult:
    """
    list_cname synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListCnameRequest): The request for the ListCname operation.

    Returns:
        ListCnameResult: The result for the ListCname operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListCname',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'cname': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['cname']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListCnameResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_cname(client: _SyncClientImpl, request: models.DeleteCnameRequest, **kwargs) -> models.DeleteCnameResult:
    """
    delete_cname synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteCnameRequest): The request for the DeleteCname operation.

    Returns:
        DeleteCnameResult: The result for the DeleteCname operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteCname',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'cname': '', 
                'comp': 'delete', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['cname', 'comp']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteCnameResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_cname_token(client: _SyncClientImpl, request: models.GetCnameTokenRequest, **kwargs) -> models.GetCnameTokenResult:
    """
    get_cname_token synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetCnameTokenRequest): The request for the GetCnameToken operation.

    Returns:
        GetCnameTokenResult: The result for the GetCnameToken operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetCnameToken',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'comp': 'token', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['comp', 'cname']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetCnameTokenResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def create_cname_token(client: _SyncClientImpl, request: models.CreateCnameTokenRequest, **kwargs) -> models.CreateCnameTokenResult:
    """
    create_cname_token synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (CreateCnameTokenRequest): The request for the CreateCnameToken operation.

    Returns:
        CreateCnameTokenResult: The result for the CreateCnameToken operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateCnameToken',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'cname': '', 
                'comp': 'token', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['cname', 'comp']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CreateCnameTokenResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
