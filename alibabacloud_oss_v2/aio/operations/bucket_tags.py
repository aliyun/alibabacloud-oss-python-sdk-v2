# pylint: disable=line-too-long

from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from ... import models
from .._aioclient import _AsyncClientImpl


async def put_bucket_tags(client: _AsyncClientImpl, request: models.PutBucketTagsRequest, **kwargs) -> models.PutBucketTagsResult:
    """
    put_bucket_tags synchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (PutBucketTagsRequest): The request for the PutBucketTags operation.

    Returns:
        PutBucketTagsResult: The result for the PutBucketTags operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketTags',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'tagging': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['tagging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketTagsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

async def get_bucket_tags(client: _AsyncClientImpl, request: models.GetBucketTagsRequest, **kwargs) -> models.GetBucketTagsResult:
    """
    get_bucket_tags synchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (GetBucketTagsRequest): The request for the GetBucketTags operation.

    Returns:
        GetBucketTagsResult: The result for the GetBucketTags operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketTags',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'tagging': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['tagging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketTagsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

async def delete_bucket_tags(client: _AsyncClientImpl, request: models.DeleteBucketTagsRequest, **kwargs) -> models.DeleteBucketTagsResult:
    """
    delete_bucket_tags synchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (DeleteBucketTagsRequest): The request for the DeleteBucketTags operation.

    Returns:
        DeleteBucketTagsResult: The result for the DeleteBucketTags operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketTags',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'tagging': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['tagging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketTagsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
