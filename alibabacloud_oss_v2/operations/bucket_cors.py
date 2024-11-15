# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_cors(client: _SyncClientImpl, request: models.PutBucketCorsRequest, **kwargs) -> models.PutBucketCorsResult:
    """
    put_bucket_cors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketCorsRequest): The request for the PutBucketCors operation.

    Returns:
        PutBucketCorsResult: The result for the PutBucketCors operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketCors',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'cors': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['cors']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketCorsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_cors(client: _SyncClientImpl, request: models.GetBucketCorsRequest, **kwargs) -> models.GetBucketCorsResult:
    """
    get_bucket_cors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketCorsRequest): The request for the GetBucketCors operation.

    Returns:
        GetBucketCorsResult: The result for the GetBucketCors operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketCors',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'cors': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['cors']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketCorsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_cors(client: _SyncClientImpl, request: models.DeleteBucketCorsRequest, **kwargs) -> models.DeleteBucketCorsResult:
    """
    delete_bucket_cors synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketCorsRequest): The request for the DeleteBucketCors operation.

    Returns:
        DeleteBucketCorsResult: The result for the DeleteBucketCors operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketCors',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'cors': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['cors']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketCorsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def option_object(client: _SyncClientImpl, request: models.OptionObjectRequest, **kwargs) -> models.OptionObjectResult:
    """
    option_object synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (OptionObjectRequest): The request for the OptionObject operation.

    Returns:
        OptionObjectResult: The result for the OptionObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='OptionObject',
            method='OPTIONS',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            bucket=request.bucket,
            key=request.key,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.OptionObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde.deserialize_output_headers
        ],
    )
