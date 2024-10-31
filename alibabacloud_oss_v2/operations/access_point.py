# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl

def create_access_point(client: _SyncClientImpl, request: models.CreateAccessPointRequest, **kwargs) -> models.CreateAccessPointResult:
    """
    create_access_point synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (CreateAccessPointRequest): The request for the CreateAccessPoint operation.

    Returns:
        CreateAccessPointResult: The result for the CreateAccessPoint operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateAccessPoint',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'accessPoint': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPoint']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CreateAccessPointResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def get_access_point(client: _SyncClientImpl, request: models.GetAccessPointRequest, **kwargs) -> models.GetAccessPointResult:
    """
    get_access_point synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetAccessPointRequest): The request for the GetAccessPoint operation.

    Returns:
        GetAccessPointResult: The result for the GetAccessPoint operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAccessPoint',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPoint': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPoint']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetAccessPointResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def list_access_points(client: _SyncClientImpl, request: models.ListAccessPointsRequest, **kwargs) -> models.ListAccessPointsResult:
    """
    list_access_points synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListAccessPointsRequest): The request for the ListAccessPoints operation.

    Returns:
        ListAccessPointsResult: The result for the ListAccessPoints operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListAccessPoints',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'accessPoint': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPoint']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListAccessPointsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_access_point(client: _SyncClientImpl, request: models.DeleteAccessPointRequest, **kwargs) -> models.DeleteAccessPointResult:
    """
    delete_access_point synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteAccessPointRequest): The request for the DeleteAccessPoint operation.

    Returns:
        DeleteAccessPointResult: The result for the DeleteAccessPoint operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteAccessPoint',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'accessPoint': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPoint']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteAccessPointResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def put_access_point_policy(client: _SyncClientImpl, request: models.PutAccessPointPolicyRequest, **kwargs) -> models.PutAccessPointPolicyResult:
    """
    put_access_point_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutAccessPointPolicyRequest): The request for the PutAccessPointPolicy operation.

    Returns:
        PutAccessPointPolicyResult: The result for the PutAccessPointPolicy operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutAccessPointPolicy',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'accessPointPolicy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointPolicy']},
        ),
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutAccessPointPolicyResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_access_point_policy(client: _SyncClientImpl, request: models.GetAccessPointPolicyRequest, **kwargs) -> models.GetAccessPointPolicyResult:
    """
    get_access_point_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetAccessPointPolicyRequest): The request for the GetAccessPointPolicy operation.

    Returns:
        GetAccessPointPolicyResult: The result for the GetAccessPointPolicy operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAccessPointPolicy',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointPolicy': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointPolicy']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetAccessPointPolicyResult(
            body=op_output.http_response.content.decode()
        ),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_access_point_policy(client: _SyncClientImpl, request: models.DeleteAccessPointPolicyRequest, **kwargs) -> models.DeleteAccessPointPolicyResult:
    """
    delete_access_point_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteAccessPointPolicyRequest): The request for the DeleteAccessPointPolicy operation.

    Returns:
        DeleteAccessPointPolicyResult: The result for the DeleteAccessPointPolicy operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteAccessPointPolicy',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessPointPolicy': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['accessPointPolicy']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteAccessPointPolicyResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
