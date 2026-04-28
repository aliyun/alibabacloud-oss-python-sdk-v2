# pylint: disable=line-too-long

from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from ... import models
from .._aioclient import _AsyncClientImpl


async def do_meta_query_action(client: _AsyncClientImpl, request: models.DoMetaQueryActionRequest, **kwargs) -> models.DoMetaQueryActionResult:
    """
    do_meta_query_action asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (DoMetaQueryActionRequest): The request for the DoMetaQueryAction operation.

    Returns:
        DoMetaQueryActionResult: The result for the DoMetaQueryAction operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DoMetaQueryAction',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'MetaQuery': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['MetaQuery']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DoMetaQueryActionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


async def do_data_pipeline_action(client: _AsyncClientImpl, request: models.DoDataPipelineActionRequest, **kwargs) -> models.DoDataPipelineActionResult:
    """
    do_data_pipeline_action asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (DoDataPipelineActionRequest): The request for the DoDataPipelineAction operation.

    Returns:
        DoDataPipelineActionResult: The result for the DoDataPipelineAction operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DoDataPipelineAction',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'dataPipeline': '',
            },
            op_metadata={'sub-resource': ['dataPipeline']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DoDataPipelineActionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
