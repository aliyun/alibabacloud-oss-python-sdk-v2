from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl
from .. import SelectResult

def select_object(client: _SyncClientImpl, request: models.SelectObjectRequest, **kwargs) -> models.SelectObjectResult:
    """
    SelectObject Executes SQL statements to perform operations on an object and obtains the execution results.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (SelectObjectRequest): The request for the SelectObject operation.

    Returns:
        SelectObjectResult: The result for the SelectObject operation.
    """

    if request.select_request and request.select_request.input_serialization.json_input is None:
        process = 'csv/select'
    else:
        process = 'json/select'

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='SelectObject',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            bucket=request.bucket,
            key=request.key,
            parameters={
                'x-oss-process': process,
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    enable_payload_crc = None
    if request.select_request.output_serialization is not None:
        enable_payload_crc = request.select_request.output_serialization.enable_payload_crc

    return serde.deserialize_output(
        result=models.SelectObjectResult(
            body=SelectResult(op_output.http_response, request.progress_callback, op_input.headers.get('content-length'), enable_payload_crc)
        ),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
        ],
    )


def create_select_object_meta(client: _SyncClientImpl, request: models.CreateSelectObjectMetaRequest, **kwargs) -> models.CreateSelectObjectMetaResult:
    """
    create_select_object_meta synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (CreateSelectObjectMetaRequest): The request for the CreateSelectObjectMeta operation.

    Returns:
        CreateSelectObjectMetaResult: The result for the CreateSelectObjectMeta operation.
    """

    if request.csv_meta_request and request.csv_meta_request.input_serialization.json_input is None:
        process = 'csv/meta'
    else:
        process = 'json/meta'

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateSelectObjectMeta',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            bucket=request.bucket,
            key=request.key,
            parameters={
                'x-oss-process': process,
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CreateSelectObjectMetaResult(
            body=SelectResult(op_output.http_response, None, op_input.headers.get('content-length'), None)
        ),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )