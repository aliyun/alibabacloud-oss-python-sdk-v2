"""Operations for object retention and legal hold APIs"""

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl

def put_object_retention(client: _SyncClientImpl, request: models.PutObjectRetentionRequest, **kwargs) -> models.PutObjectRetentionResult:
    """
    Configures object retention (WORM protection) for an object.

    Args:
        client (_SyncClientImpl): The OSS client.
        request (PutObjectRetentionRequest): Request parameters.

    Returns:
        PutObjectRetentionResult: Response result.
    """
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutObjectRetention',
            method='PUT',
            parameters={'retention': ''},
            bucket=request.bucket,
            key=request.key,
            op_metadata={'sub-resource': ['retention']},
        ),
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.PutObjectRetentionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
        ],
    )


def get_object_retention(client: _SyncClientImpl, request: models.GetObjectRetentionRequest, **kwargs) -> models.GetObjectRetentionResult:
    """
    Queries object retention (WORM protection) configuration for an object.

    Args:
        client (_SyncClientImpl): The OSS client.
        request (GetObjectRetentionRequest): Request parameters.

    Returns:
        GetObjectRetentionResult: Response result.
    """
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetObjectRetention',
            method='GET',
            parameters={'retention': ''},
            bucket=request.bucket,
            key=request.key,
            op_metadata={'sub-resource': ['retention']},
        ),
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetObjectRetentionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
            serde.deserialize_output_xmlbody
        ],
    )


def put_object_legal_hold(client: _SyncClientImpl, request: models.PutObjectLegalHoldRequest, **kwargs) -> models.PutObjectLegalHoldResult:
    """
    Configures legal hold for an object.

    Args:
        client (_SyncClientImpl): The OSS client.
        request (PutObjectLegalHoldRequest): Request parameters.

    Returns:
        PutObjectLegalHoldResult: Response result.
    """
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutObjectLegalHold',
            method='PUT',
            parameters={'legalHold': ''},
            bucket=request.bucket,
            key=request.key,
            op_metadata={'sub-resource': ['legalHold']},
        ),
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.PutObjectLegalHoldResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
        ],
    )


def get_object_legal_hold(client: _SyncClientImpl, request: models.GetObjectLegalHoldRequest, **kwargs) -> models.GetObjectLegalHoldResult:
    """
    Queries legal hold configuration for an object.

    Args:
        client (_SyncClientImpl): The OSS client.
        request (GetObjectLegalHoldRequest): Request parameters.

    Returns:
        GetObjectLegalHoldResult: Response result.
    """
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetObjectLegalHold',
            method='GET',
            parameters={'legalHold': ''},
            bucket=request.bucket,
            key=request.key,
            op_metadata={'sub-resource': ['legalHold']},
        ),
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetObjectLegalHoldResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
            serde.deserialize_output_xmlbody
        ],
    )
