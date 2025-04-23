from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl

def list_cloud_boxes(client: _SyncClientImpl, request: models.ListCloudBoxesRequest, **kwargs) -> models.ListCloudBoxesResult:
    """
    ListCloudBoxes Lists cloud box buckets that belong to the current account.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListCloudBoxesRequest): The request for the ListCloudBoxes operation.

    Returns:
        ListCloudBoxesResult: The result for the ListCloudBoxes operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListCloudBoxes',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'cloudboxes': '',
            },
            op_metadata={'sub-resource': ['cloudboxes']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListCloudBoxesResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

