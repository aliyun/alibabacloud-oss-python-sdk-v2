# pylint: disable=line-too-long
from ... import exceptions
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models
from ._serde import serialize_input_vector_json_model
from ._serde import deserialize_output_vector_json_model


def _validate_query_vectors_fusion_request(request: models.QueryVectorsFusionRequest) -> None:
    """Check the parts of a fusion query that cannot drift with the service.

    knn is the one clause whose shape is fixed by the wire format itself: it
    is either a single object or an array of objects. Python carries those two
    as dict and list and json.dumps encodes them correctly, which is why no
    restricted interface is needed here. Anything else, a string or a number
    for instance, can never become a valid knn clause, so it is rejected
    before the request is signed instead of after a round trip.

    The required bucket, index name and schema are not checked here, the
    serializer already raises ParamRequiredError for them.

    Deliberately not validated: the documented mutual exclusion between
    retriever and the other top level fields, and every numeric bound such as
    topK, numCandidates, limit or windowSize. That part of the protocol is not
    final yet, and hard coding it here would make the SDK disagree with the
    service as soon as either side moves. The service remains the authority on
    those rules.
    """

    knn = request.knn
    if knn is None:
        return

    if isinstance(knn, dict):
        return

    invalid_type = type(knn).__name__
    if isinstance(knn, list):
        for item in knn:
            if not isinstance(item, dict):
                invalid_type = type(item).__name__
                break
        else:
            return

    raise exceptions.ParamInvalidError(
        field='knn, expected a dict or a list of dict, got %s' % invalid_type)


def query_vectors_fusion(client: _SyncClientImpl, request: models.QueryVectorsFusionRequest, **kwargs) -> models.QueryVectorsFusionResult:
    """
    query_vectors_fusion synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (QueryVectorsFusionRequest): The request for the QueryVectorsFusion operation.

    Returns:
        QueryVectorsFusionResult: The result for the QueryVectorsFusion operation.
    """

    _validate_query_vectors_fusion_request(request)

    op_input = serialize_input_vector_json_model(
        request=request,
        op_input=OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'queryVectorsFusion': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.QueryVectorsFusionResult(),
        op_output=op_output,
        custom_deserializer=[
            deserialize_output_vector_json_model
        ],
    )
