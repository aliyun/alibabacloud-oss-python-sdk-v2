# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_request_payment(client: _SyncClientImpl, request: models.PutBucketRequestPaymentRequest, **kwargs) -> models.PutBucketRequestPaymentResult:
    """
    put_bucket_request_payment synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketRequestPaymentRequest): The request for the PutBucketRequestPayment operation.

    Returns:
        PutBucketRequestPaymentResult: The result for the PutBucketRequestPayment operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketRequestPayment',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'requestPayment': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['requestPayment']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketRequestPaymentResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_request_payment(client: _SyncClientImpl, request: models.GetBucketRequestPaymentRequest, **kwargs) -> models.GetBucketRequestPaymentResult:
    """
    get_bucket_request_payment synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketRequestPaymentRequest): The request for the GetBucketRequestPayment operation.

    Returns:
        GetBucketRequestPaymentResult: The result for the GetBucketRequestPayment operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketRequestPayment',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'requestPayment': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['requestPayment']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketRequestPaymentResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
