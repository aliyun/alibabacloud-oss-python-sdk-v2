# -*- coding: utf-8 -*-
"""Table Bucket configuration operations for tables."""

from urllib.parse import quote
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models
from ._serde import serialize_input_tables_json_model
from ._serde import deserialize_output_tables_json_model

def delete_table_bucket_encryption(client: _SyncClientImpl, request: models.DeleteTableBucketEncryptionRequest, **kwargs) -> models.DeleteTableBucketEncryptionResult:
    """
    Deletes the encryption configuration of a table bucket.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='DeleteTableBucketEncryption',
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
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}/encryption"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.DeleteTableBucketEncryptionResult(),
        op_output=op_output,
    )


def get_table_bucket_encryption(client: _SyncClientImpl, request: models.GetTableBucketEncryptionRequest, **kwargs) -> models.GetTableBucketEncryptionResult:
    """
    Gets the encryption configuration of a table bucket.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTableBucketEncryption',
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
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}/encryption"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTableBucketEncryptionResult(),
        op_output=op_output,
    )


def put_table_bucket_encryption(client: _SyncClientImpl, request: models.PutTableBucketEncryptionRequest, **kwargs) -> models.PutTableBucketEncryptionResult:
    """
    Sets the encryption configuration of a table bucket.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='PutTableBucketEncryption',
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
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}/encryption"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.PutTableBucketEncryptionResult(),
        op_output=op_output,
    )


def get_table_bucket_maintenance_configuration(client: _SyncClientImpl, request: models.GetTableBucketMaintenanceConfigurationRequest, **kwargs) -> models.GetTableBucketMaintenanceConfigurationResult:
    """
    Gets the maintenance configuration of a table bucket.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTableBucketMaintenanceConfiguration',
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
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}/maintenance"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTableBucketMaintenanceConfigurationResult(),
        op_output=op_output,
    )


def put_table_bucket_maintenance_configuration(client: _SyncClientImpl, request: models.PutTableBucketMaintenanceConfigurationRequest, **kwargs) -> models.PutTableBucketMaintenanceConfigurationResult:
    """
    Sets the maintenance configuration of a table bucket.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='PutTableBucketMaintenanceConfiguration',
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
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}/maintenance/{quote(request.type, safe='')}"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.PutTableBucketMaintenanceConfigurationResult(),
        op_output=op_output,
    )


def delete_table_bucket_policy(client: _SyncClientImpl, request: models.DeleteTableBucketPolicyRequest, **kwargs) -> models.DeleteTableBucketPolicyResult:
    """
    Deletes the policy of a table bucket.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='DeleteTableBucketPolicy',
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
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}/policy"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.DeleteTableBucketPolicyResult(),
        op_output=op_output,
    )


def get_table_bucket_policy(client: _SyncClientImpl, request: models.GetTableBucketPolicyRequest, **kwargs) -> models.GetTableBucketPolicyResult:
    """
    Gets the policy of a table bucket.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTableBucketPolicy',
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
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}/policy"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTableBucketPolicyResult(),
        op_output=op_output,
    )


def put_table_bucket_policy(client: _SyncClientImpl, request: models.PutTableBucketPolicyRequest, **kwargs) -> models.PutTableBucketPolicyResult:
    """
    Sets the policy of a table bucket.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='PutTableBucketPolicy',
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
    op_input.key = f"buckets/{quote(request.table_bucket_arn, safe='')}/policy"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.PutTableBucketPolicyResult(),
        op_output=op_output,
    )
