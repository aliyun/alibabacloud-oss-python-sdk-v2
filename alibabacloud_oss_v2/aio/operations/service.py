"""APIs for service operation."""
# pylint: disable=line-too-long

from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from ... import models
from .._aioclient import _AsyncClientImpl

async def list_buckets(client: _AsyncClientImpl, request: models.ListBucketsRequest, **kwargs) -> models.ListBucketsResult:
    """
    list buckets asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (ListBucketsRequest): The request for the ListBuckets operation.

    Returns:
        ListBucketsResult: The result for the ListBuckets operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListBuckets',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/octet-stream',
            }),
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListBucketsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
        ],
    )
