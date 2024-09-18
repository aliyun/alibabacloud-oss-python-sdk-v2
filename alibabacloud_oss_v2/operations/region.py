"""APIs for region operation."""
# pylint: disable=line-too-long

from ..types import OperationInput
from .. import serde
from .. import models
from .._client import _SyncClientImpl

def describe_regions(client: _SyncClientImpl, request: models.DescribeRegionsRequest, **kwargs) -> models.DescribeRegionsResult:
    """
    Queries the endpoints of all regions supported by Object Storage Service (OSS) or a specific region, including public endpoints, internal endpoints, and acceleration endpoints.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DescribeRegionsRequest): The request for the DescribeRegions operation.

    Returns:
        DescribeRegionsResult: The result for the DescribeRegions operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DescribeRegions',
            method='GET',
            parameters={
                'regions': '',
            },
        )
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DescribeRegionsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
