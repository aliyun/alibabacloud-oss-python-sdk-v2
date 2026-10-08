"""APIs for bucket metadata table configuration operations."""
# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import models, serde, serde_utils
from .._client import _SyncClientImpl


def create_bucket_metadata_configuration(client: _SyncClientImpl, request: models.CreateBucketMetadataConfigurationRequest, **kwargs) -> models.CreateBucketMetadataConfigurationResult:
    """Creates the metadata table configuration of a bucket."""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateBucketMetadataConfiguration',
            method='POST',
            headers=CaseInsensitiveDict({'Content-Type': 'application/xml'}),
            parameters={'metadataConfiguration': ''},
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metadataConfiguration']},
        ),
        custom_serializer=[serde_utils.add_content_md5]
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.CreateBucketMetadataConfigurationResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def get_bucket_metadata_configuration(client: _SyncClientImpl, request: models.GetBucketMetadataConfigurationRequest, **kwargs) -> models.GetBucketMetadataConfigurationResult:
    """Gets the metadata table configuration of a bucket."""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketMetadataConfiguration',
            method='GET',
            headers=CaseInsensitiveDict({'Content-Type': 'application/xml'}),
            parameters={'metadataConfiguration': ''},
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metadataConfiguration']},
        ),
        custom_serializer=[serde_utils.add_content_md5]
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetBucketMetadataConfigurationResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def delete_bucket_metadata_configuration(client: _SyncClientImpl, request: models.DeleteBucketMetadataConfigurationRequest, **kwargs) -> models.DeleteBucketMetadataConfigurationResult:
    """Deletes the metadata table configuration of a bucket."""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketMetadataConfiguration',
            method='DELETE',
            headers=CaseInsensitiveDict({'Content-Type': 'application/xml'}),
            parameters={'metadataConfiguration': ''},
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metadataConfiguration']},
        ),
        custom_serializer=[serde_utils.add_content_md5]
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.DeleteBucketMetadataConfigurationResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def update_bucket_metadata_inventory_table_configuration(client: _SyncClientImpl, request: models.UpdateBucketMetadataInventoryTableConfigurationRequest, **kwargs) -> models.UpdateBucketMetadataInventoryTableConfigurationResult:
    """Updates the inventory metadata table configuration of a bucket."""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='UpdateBucketMetadataInventoryTableConfiguration',
            method='PUT',
            headers=CaseInsensitiveDict({'Content-Type': 'application/xml'}),
            parameters={'metadataInventoryTable': ''},
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metadataInventoryTable']},
        ),
        custom_serializer=[serde_utils.add_content_md5]
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.UpdateBucketMetadataInventoryTableConfigurationResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def update_bucket_metadata_journal_table_configuration(client: _SyncClientImpl, request: models.UpdateBucketMetadataJournalTableConfigurationRequest, **kwargs) -> models.UpdateBucketMetadataJournalTableConfigurationResult:
    """Updates the journal metadata table configuration of a bucket."""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='UpdateBucketMetadataJournalTableConfiguration',
            method='PUT',
            headers=CaseInsensitiveDict({'Content-Type': 'application/xml'}),
            parameters={'metadataJournalTable': ''},
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metadataJournalTable']},
        ),
        custom_serializer=[serde_utils.add_content_md5]
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.UpdateBucketMetadataJournalTableConfigurationResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )
