# -*- coding: utf-8 -*-
"""Table Bucket operations for tables."""
from urllib.parse import urlencode, quote
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models
from ._serde import serialize_input_tables_json_model
from ._serde import deserialize_output_tables_json_model

def create_table_bucket(client: _SyncClientImpl, request: models.CreateTableBucketRequest, **kwargs) -> models.CreateTableBucketResult:
    """
    Creates a table bucket.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (CreateTableBucketRequest): The request for the CreateTableBucket operation.

    Returns:
        CreateTableBucketResult: The result for the CreateTableBucket operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='CreateTableBucket',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )
    op_input.key = 'buckets'

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.CreateTableBucketResult(),
        op_output=op_output,
    )


def delete_table_bucket(client: _SyncClientImpl, request: models.DeleteTableBucketRequest, **kwargs) -> models.DeleteTableBucketResult:
    """
    Deletes a table bucket.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (DeleteTableBucketRequest): The request for the DeleteTableBucket operation.

    Returns:
        DeleteTableBucketResult: The result for the DeleteTableBucket operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='DeleteTableBucket',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            op_metadata={
                'is_bucket_arn': True,
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )
    op_input.bucket = request.table_bucket_arn
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.DeleteTableBucketResult(),
        op_output=op_output,
    )


def get_table_bucket(client: _SyncClientImpl, request: models.GetTableBucketRequest, **kwargs) -> models.GetTableBucketResult:
    """
    Gets the information of a table bucket.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (GetTableBucketRequest): The request for the GetTableBucket operation.

    Returns:
        GetTableBucketResult: The result for the GetTableBucket operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTableBucket',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            op_metadata={
                'is_bucket_arn': True,
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )
    op_input.bucket = request.table_bucket_arn
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTableBucketResult(),
        op_output=op_output,
    )


def list_table_buckets(client: _SyncClientImpl, request: models.ListTableBucketsRequest, **kwargs) -> models.ListTableBucketsResult:
    """
    Lists table buckets.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (ListTableBucketsRequest): The request for the ListTableBuckets operation.

    Returns:
        ListTableBucketsResult: The result for the ListTableBuckets operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='ListTableBuckets',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )
    op_input.key = 'buckets'

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.ListTableBucketsResult(),
        op_output=op_output,
    )
