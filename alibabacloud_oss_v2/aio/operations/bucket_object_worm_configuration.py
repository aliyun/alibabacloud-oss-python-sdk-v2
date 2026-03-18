"""APIs for object worm configuration operation."""
# pylint: disable=line-too-long

from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from ... import models
from .._aioclient import _AsyncClientImpl


async def put_bucket_object_worm_configuration(client: _AsyncClientImpl, request: models.PutBucketObjectWormConfigurationRequest, **kwargs) -> models.PutBucketObjectWormConfigurationResult:
    """
    put_bucket_object_worm_configuration asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (PutBucketObjectWormConfigurationRequest): The request for the PutBucketObjectWormConfiguration operation.

    Returns:
        PutBucketObjectWormConfigurationResult: The result for the PutBucketObjectWormConfiguration operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketObjectWormConfiguration',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'objectWorm': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['objectWorm']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketObjectWormConfigurationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


async def get_bucket_object_worm_configuration(client: _AsyncClientImpl, request: models.GetBucketObjectWormConfigurationRequest, **kwargs) -> models.GetBucketObjectWormConfigurationResult:
    """
    get_bucket_object_worm_configuration asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (GetBucketObjectWormConfigurationRequest): The request for the GetBucketObjectWormConfiguration operation.

    Returns:
        GetBucketObjectWormConfigurationResult: The result for the GetBucketObjectWormConfiguration operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketObjectWormConfiguration',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'objectWorm': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['objectWorm']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketObjectWormConfigurationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
