# -*- coding: utf-8 -*-
"""Table operations for tables."""
from urllib.parse import quote
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models
from ._serde import serialize_input_tables_json_model
from ._serde import deserialize_output_tables_json_model
from ...arns import Arn
from ... import exceptions

def create_table(client: _SyncClientImpl, request: models.CreateTableRequest, **kwargs) -> models.CreateTableResult:
    """
    Creates a table.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (CreateTableRequest): The request for the CreateTable operation.

    Returns:
        CreateTableResult: The result for the CreateTable operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='CreateTable',
            method='PUT',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.CreateTableResult(),
        op_output=op_output,
    )


def delete_table(client: _SyncClientImpl, request: models.DeleteTableRequest, **kwargs) -> models.DeleteTableResult:
    """
    Deletes a table.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (DeleteTableRequest): The request for the DeleteTable operation.

    Returns:
        DeleteTableResult: The result for the DeleteTable operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='DeleteTable',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}"
    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.DeleteTableResult(),
        op_output=op_output,
    )


def get_table(client: _SyncClientImpl, request: models.GetTableRequest, **kwargs) -> models.GetTableResult:
    """
    Gets the information of a table.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (GetTableRequest): The request for the GetTable operation.

    Returns:
        GetTableResult: The result for the GetTable operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTable',
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

    table_bucket_arn = ''
    if request.table_bucket_arn is not None:
        table_bucket_arn = request.table_bucket_arn
    elif request.table_arn is not None:
        arn = Arn.from_string(request.table_arn)
        arn_resource = arn.arn_resource
        if not ('bucket' == arn_resource.resource_type and 
            arn_resource.qualifier is not None and
            arn_resource.qualifier.startswith("table/")):
            raise exceptions.ParamInvalidError(field='request.table_arn')
        idx = request.table_arn.index('/table/')
        table_bucket_arn = request.table_arn[0:idx]
    else:
        raise exceptions.ParamRequiredError(field='request.table_bucket_arn')

    op_input.bucket = table_bucket_arn
    op_input.key = 'get-table'
    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTableResult(),
        op_output=op_output,
    )


def list_tables(client: _SyncClientImpl, request: models.ListTablesRequest, **kwargs) -> models.ListTablesResult:
    """
    Lists tables.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (ListTablesRequest): The request for the ListTables operation.

    Returns:
        ListTablesResult: The result for the ListTables operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='ListTables',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'namespace': request.namespace,
            },            
            op_metadata={
                'is_bucket_arn': True,
            },            
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_input.bucket = request.table_bucket_arn
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}"
    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.ListTablesResult(),
        op_output=op_output,
    )


def rename_table(client: _SyncClientImpl, request: models.RenameTableRequest, **kwargs) -> models.RenameTableResult:
    """
    Renames a table.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (RenameTableRequest): The request for the RenameTable operation.

    Returns:
        RenameTableResult: The result for the RenameTable operation.
    """
    from urllib.parse import quote

    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='RenameTable',
            method='PUT',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/rename"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.RenameTableResult(),
        op_output=op_output,
    )
