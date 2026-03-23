"""Async operations for object retention and legal hold APIs"""

from typing import TYPE_CHECKING
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from ... import models
from .._aioclient import _AsyncClientImpl
if TYPE_CHECKING:
    from ..operations import OperationInput, OperationOutput


async def put_object_retention(client: _AsyncClientImpl, request: models.PutObjectRetentionRequest, **kwargs) -> models.PutObjectRetentionResult:
    """
    Configures object retention (WORM protection) for an object.

    Args:
        client (_AsyncClientImpl): The OSS async client.
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
    op_output = await client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.PutObjectRetentionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
        ],
    )


async def get_object_retention(client: _AsyncClientImpl, request: models.GetObjectRetentionRequest, **kwargs) -> models.GetObjectRetentionResult:
    """
    Queries object retention (WORM protection) configuration for an object.

    Args:
        client (_AsyncClientImpl): The OSS async client.
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
    op_output = await client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetObjectRetentionResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
            serde.deserialize_output_xmlbody
        ],
    )


async def put_object_legal_hold(client: _AsyncClientImpl, request: models.PutObjectLegalHoldRequest, **kwargs) -> models.PutObjectLegalHoldResult:
    """
    Configures legal hold for an object.

    Args:
        client (_AsyncClientImpl): The OSS async client.
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
    op_output = await client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.PutObjectLegalHoldResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
        ],
    )


async def get_object_legal_hold(client: _AsyncClientImpl, request: models.GetObjectLegalHoldRequest, **kwargs) -> models.GetObjectLegalHoldResult:
    """
    Queries legal hold configuration for an object.

    Args:
        client (_AsyncClientImpl): The OSS async client.
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
    op_output = await client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetObjectLegalHoldResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
            serde.deserialize_output_xmlbody
        ],
    )
