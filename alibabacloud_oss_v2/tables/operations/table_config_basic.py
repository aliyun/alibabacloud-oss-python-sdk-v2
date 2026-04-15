# -*- coding: utf-8 -*-
"""Table configuration operations for tables."""

from urllib.parse import quote
from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models
from ._serde import serialize_input_tables_json_model
from ._serde import deserialize_output_tables_json_model

def get_table_encryption(client: _SyncClientImpl, request: models.GetTableEncryptionRequest, **kwargs) -> models.GetTableEncryptionResult:
    """
    Gets the encryption configuration of a table.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTableEncryption',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/encryption"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTableEncryptionResult(),
        op_output=op_output,
    )


def get_table_maintenance_configuration(client: _SyncClientImpl, request: models.GetTableMaintenanceConfigurationRequest, **kwargs) -> models.GetTableMaintenanceConfigurationResult:
    """
    Gets the maintenance configuration of a table.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTableMaintenanceConfiguration',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/maintenance"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTableMaintenanceConfigurationResult(),
        op_output=op_output,
    )


def put_table_maintenance_configuration(client: _SyncClientImpl, request: models.PutTableMaintenanceConfigurationRequest, **kwargs) -> models.PutTableMaintenanceConfigurationResult:
    """
    Sets the maintenance configuration of a table.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='PutTableMaintenanceConfiguration',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/maintenance/{quote(request.type, safe='')}"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.PutTableMaintenanceConfigurationResult(),
        op_output=op_output,
    )


def get_table_maintenance_job_status(client: _SyncClientImpl, request: models.GetTableMaintenanceJobStatusRequest, **kwargs) -> models.GetTableMaintenanceJobStatusResult:
    """
    Gets the maintenance job status of a table.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTableMaintenanceJobStatus',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/maintenance-job-status"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTableMaintenanceJobStatusResult(),
        op_output=op_output,
    )


def get_table_metadata_location(client: _SyncClientImpl, request: models.GetTableMetadataLocationRequest, **kwargs) -> models.GetTableMetadataLocationResult:
    """
    Gets the metadata location of a table.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTableMetadataLocation',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/metadata-location"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTableMetadataLocationResult(),
        op_output=op_output,
    )


def update_table_metadata_location(client: _SyncClientImpl, request: models.UpdateTableMetadataLocationRequest, **kwargs) -> models.UpdateTableMetadataLocationResult:
    """
    Updates the metadata location of a table.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='UpdateTableMetadataLocation',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/metadata-location"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.UpdateTableMetadataLocationResult(),
        op_output=op_output,
    )


def delete_table_policy(client: _SyncClientImpl, request: models.DeleteTablePolicyRequest, **kwargs) -> models.DeleteTablePolicyResult:
    """
    Deletes the policy of a table.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='DeleteTablePolicy',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/policy"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.DeleteTablePolicyResult(),
        op_output=op_output,
    )


def get_table_policy(client: _SyncClientImpl, request: models.GetTablePolicyRequest, **kwargs) -> models.GetTablePolicyResult:
    """
    Gets the policy of a table.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='GetTablePolicy',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/policy"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.GetTablePolicyResult(),
        op_output=op_output,
    )


def put_table_policy(client: _SyncClientImpl, request: models.PutTablePolicyRequest, **kwargs) -> models.PutTablePolicyResult:
    """
    Sets the policy of a table.
    """
    op_input = serialize_input_tables_json_model(
        request=request,
        op_input=OperationInput(
            op_name='PutTablePolicy',
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
    op_input.key = f"tables/{quote(request.table_bucket_arn, safe='')}/{quote(request.namespace, safe='')}/{quote(request.name, safe='')}/policy"

    op_output = client.invoke_operation(op_input, **kwargs)

    return deserialize_output_tables_json_model(
        result=models.PutTablePolicyResult(),
        op_output=op_output,
    )
