# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_referer(client: _SyncClientImpl, request: models.PutBucketRefererRequest, **kwargs) -> models.PutBucketRefererResult:
    """
    put_bucket_referer synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketRefererRequest): The request for the PutBucketReferer operation.

    Returns:
        PutBucketRefererResult: The result for the PutBucketReferer operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketReferer',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'referer': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['referer']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketRefererResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_referer(client: _SyncClientImpl, request: models.GetBucketRefererRequest, **kwargs) -> models.GetBucketRefererResult:
    """
    get_bucket_referer synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketRefererRequest): The request for the GetBucketReferer operation.

    Returns:
        GetBucketRefererResult: The result for the GetBucketReferer operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketReferer',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'referer': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['referer']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketRefererResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
