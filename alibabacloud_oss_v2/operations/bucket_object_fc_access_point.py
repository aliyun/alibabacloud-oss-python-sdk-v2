# pylint: disable=line-too-long
from ..io_utils import StreamBodyReader
from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def create_access_point_for_object_process(client: _SyncClientImpl, request: models.CreateAccessPointForObjectProcessRequest, **kwargs) -> models.CreateAccessPointForObjectProcessResult:
    """
    create_access_point_for_object_process synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (CreateAccessPointForObjectProcessRequest): The request for the CreateAccessPointForObjectProcess operation.

    Returns:
        CreateAccessPointForObjectProcessResult: The result for the CreateAccessPointForObjectProcess operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateAccessPointForObjectProcess',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointForObjectProcess': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointForObjectProcess']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CreateAccessPointForObjectProcessResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_access_point_for_object_process(client: _SyncClientImpl, request: models.GetAccessPointForObjectProcessRequest, **kwargs) -> models.GetAccessPointForObjectProcessResult:
    """
    get_access_point_for_object_process synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetAccessPointForObjectProcessRequest): The request for the GetAccessPointForObjectProcess operation.

    Returns:
        GetAccessPointForObjectProcessResult: The result for the GetAccessPointForObjectProcess operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAccessPointForObjectProcess',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointForObjectProcess': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointForObjectProcess']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetAccessPointForObjectProcessResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def list_access_points_for_object_process(client: _SyncClientImpl, request: models.ListAccessPointsForObjectProcessRequest, **kwargs) -> models.ListAccessPointsForObjectProcessResult:
    """
    list_access_points_for_object_process synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListAccessPointsForObjectProcessRequest): The request for the ListAccessPointsForObjectProcess operation.

    Returns:
        ListAccessPointsForObjectProcessResult: The result for the ListAccessPointsForObjectProcess operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListAccessPointsForObjectProcess',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointForObjectProcess': '', 
            },
            op_metadata={'sub-resource': ['accessPointForObjectProcess']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListAccessPointsForObjectProcessResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_access_point_for_object_process(client: _SyncClientImpl, request: models.DeleteAccessPointForObjectProcessRequest, **kwargs) -> models.DeleteAccessPointForObjectProcessResult:
    """
    delete_access_point_for_object_process synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteAccessPointForObjectProcessRequest): The request for the DeleteAccessPointForObjectProcess operation.

    Returns:
        DeleteAccessPointForObjectProcessResult: The result for the DeleteAccessPointForObjectProcess operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteAccessPointForObjectProcess',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointForObjectProcess': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointForObjectProcess']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteAccessPointForObjectProcessResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_access_point_config_for_object_process(client: _SyncClientImpl, request: models.GetAccessPointConfigForObjectProcessRequest, **kwargs) -> models.GetAccessPointConfigForObjectProcessResult:
    """
    get_access_point_config_for_object_process synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetAccessPointConfigForObjectProcessRequest): The request for the GetAccessPointConfigForObjectProcess operation.

    Returns:
        GetAccessPointConfigForObjectProcessResult: The result for the GetAccessPointConfigForObjectProcess operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAccessPointConfigForObjectProcess',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointConfigForObjectProcess': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointConfigForObjectProcess']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetAccessPointConfigForObjectProcessResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_access_point_config_for_object_process(client: _SyncClientImpl, request: models.PutAccessPointConfigForObjectProcessRequest, **kwargs) -> models.PutAccessPointConfigForObjectProcessResult:
    """
    put_access_point_config_for_object_process synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutAccessPointConfigForObjectProcessRequest): The request for the PutAccessPointConfigForObjectProcess operation.

    Returns:
        PutAccessPointConfigForObjectProcessResult: The result for the PutAccessPointConfigForObjectProcess operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutAccessPointConfigForObjectProcess',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointConfigForObjectProcess': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointConfigForObjectProcess']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutAccessPointConfigForObjectProcessResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_access_point_policy_for_object_process(client: _SyncClientImpl, request: models.PutAccessPointPolicyForObjectProcessRequest, **kwargs) -> models.PutAccessPointPolicyForObjectProcessResult:
    """
    put_access_point_policy_for_object_process synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutAccessPointPolicyForObjectProcessRequest): The request for the PutAccessPointPolicyForObjectProcess operation.

    Returns:
        PutAccessPointPolicyForObjectProcessResult: The result for the PutAccessPointPolicyForObjectProcess operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutAccessPointPolicyForObjectProcess',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointPolicyForObjectProcess': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointPolicyForObjectProcess']},
        ),
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutAccessPointPolicyForObjectProcessResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_access_point_policy_for_object_process(client: _SyncClientImpl, request: models.GetAccessPointPolicyForObjectProcessRequest, **kwargs) -> models.GetAccessPointPolicyForObjectProcessResult:
    """
    get_access_point_policy_for_object_process synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetAccessPointPolicyForObjectProcessRequest): The request for the GetAccessPointPolicyForObjectProcess operation.

    Returns:
        GetAccessPointPolicyForObjectProcessResult: The result for the GetAccessPointPolicyForObjectProcess operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAccessPointPolicyForObjectProcess',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointPolicyForObjectProcess': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointPolicyForObjectProcess']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetAccessPointPolicyForObjectProcessResult(
            body=op_output.http_response.content.decode()
        ),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_access_point_policy_for_object_process(client: _SyncClientImpl, request: models.DeleteAccessPointPolicyForObjectProcessRequest, **kwargs) -> models.DeleteAccessPointPolicyForObjectProcessResult:
    """
    delete_access_point_policy_for_object_process synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteAccessPointPolicyForObjectProcessRequest): The request for the DeleteAccessPointPolicyForObjectProcess operation.

    Returns:
        DeleteAccessPointPolicyForObjectProcessResult: The result for the DeleteAccessPointPolicyForObjectProcess operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteAccessPointPolicyForObjectProcess',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointPolicyForObjectProcess': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointPolicyForObjectProcess']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteAccessPointPolicyForObjectProcessResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def write_get_object_response(client: _SyncClientImpl, request: models.WriteGetObjectResponseRequest, **kwargs) -> models.WriteGetObjectResponseResult:
    """
    Specifies the return data and response headers for a GetObject request.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (WriteGetObjectResponseRequest): The request for the WriteGetObjectResponse operation.

    Returns:
        WriteGetObjectResponseResult: The result for the WriteGetObjectResponse operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='WriteGetObjectResponse',
            method='POST',
            op_metadata={'response-stream':True}
        ),
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.WriteGetObjectResponseResult(
            body=StreamBodyReader(op_output.http_response)
        ),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )