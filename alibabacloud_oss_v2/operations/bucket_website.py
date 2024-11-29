# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def get_bucket_website(client: _SyncClientImpl, request: models.GetBucketWebsiteRequest, **kwargs) -> models.GetBucketWebsiteResult:
    """
    get_bucket_website synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketWebsiteRequest): The request for the GetBucketWebsite operation.

    Returns:
        GetBucketWebsiteResult: The result for the GetBucketWebsite operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketWebsite',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'website': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['website']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketWebsiteResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_bucket_website(client: _SyncClientImpl, request: models.PutBucketWebsiteRequest, **kwargs) -> models.PutBucketWebsiteResult:
    """
    put_bucket_website synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketWebsiteRequest): The request for the PutBucketWebsite operation.

    Returns:
        PutBucketWebsiteResult: The result for the PutBucketWebsite operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketWebsite',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'website': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['website']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketWebsiteResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_website(client: _SyncClientImpl, request: models.DeleteBucketWebsiteRequest, **kwargs) -> models.DeleteBucketWebsiteResult:
    """
    delete_bucket_website synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketWebsiteRequest): The request for the DeleteBucketWebsite operation.

    Returns:
        DeleteBucketWebsiteResult: The result for the DeleteBucketWebsite operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketWebsite',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'website': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['website']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketWebsiteResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
