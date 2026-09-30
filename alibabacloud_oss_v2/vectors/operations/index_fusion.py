# pylint: disable=line-too-long
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models
from ._serde import serialize_input_vector_json_model
from ._serde import deserialize_output_vector_json_model

def put_vector_index_fusion(client: _SyncClientImpl, request: models.PutVectorIndexFusionRequest, **kwargs) -> models.PutVectorIndexFusionResult:
    """
    put_vector_index_fusion synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutVectorIndexFusionRequest): The request for the PutVectorIndexFusion operation.

    Returns:
        PutVectorIndexFusionResult: The result for the PutVectorIndexFusion operation.
    """

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='PutVectorIndexFusion',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'putVectorIndexFusion': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutVectorIndexFusionResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )
