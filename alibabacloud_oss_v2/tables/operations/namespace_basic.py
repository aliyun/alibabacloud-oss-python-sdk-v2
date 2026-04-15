# -*- coding: utf-8 -*-
"""Namespace operations for tables."""
from urllib.parse import quote
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models
from ._serde import serialize_input_tables_json_model
from ._serde import deserialize_output_tables_json_model

def create_namespace(client: _SyncClientImpl, request: models.CreateNamespaceRequest, **kwargs) -> models.CreateNamespaceResult:
    """
    Creates a namespace.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (CreateNamespaceRequest): The request for the CreateNamespace operation.

    Returns:
        CreateNamespaceResult: The result for the CreateNamespace operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='CreateNamespace',
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
    op_input.key = f"namespaces/{quote(request.table_bucket_arn, safe='')}"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.CreateNamespaceResult(),
        op_output=op_output,
    )


def delete_namespace(client: _SyncClientImpl, request: models.DeleteNamespaceRequest, **kwargs) -> models.DeleteNamespaceResult:
    """
    Deletes a namespace.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (DeleteNamespaceRequest): The request for the DeleteNamespace operation.

    Returns:
        DeleteNamespaceResult: The result for the DeleteNamespace operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='DeleteNamespace',
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
    op_input.key = f"namespaces/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.DeleteNamespaceResult(),
        op_output=op_output,
    )


def get_namespace(client: _SyncClientImpl, request: models.GetNamespaceRequest, **kwargs) -> models.GetNamespaceResult:
    """
    Gets the information of a namespace.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (GetNamespaceRequest): The request for the GetNamespace operation.

    Returns:
        GetNamespaceResult: The result for the GetNamespace operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetNamespace',
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
    op_input.key = f"namespaces/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetNamespaceResult(),
        op_output=op_output,
    )


def list_namespaces(client: _SyncClientImpl, request: models.ListNamespacesRequest, **kwargs) -> models.ListNamespacesResult:
    """
    Lists namespaces.

    Args:
        client (_SyncClientImpl): A client that sends the request.
        request (ListNamespacesRequest): The request for the ListNamespaces operation.

    Returns:
        ListNamespacesResult: The result for the ListNamespaces operation.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='ListNamespaces',
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
    op_input.key = f"namespaces/{quote(request.table_bucket_arn, safe='')}"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.ListNamespacesResult(),
        op_output=op_output,
    )
