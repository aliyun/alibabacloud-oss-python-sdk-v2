# -*- coding: utf-8 -*-
"""Dataset and Query operations for dataprocess."""

from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models


def create_dataset(client: _SyncClientImpl, request: models.CreateDatasetRequest, **kwargs) -> models.CreateDatasetResult:
    """Creates a dataset."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateDataset',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'createDataset',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CreateDatasetResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def get_dataset(client: _SyncClientImpl, request: models.GetDatasetRequest, **kwargs) -> models.GetDatasetResult:
    """Gets a dataset."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetDataset',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'getDataset',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetDatasetResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def update_dataset(client: _SyncClientImpl, request: models.UpdateDatasetRequest, **kwargs) -> models.UpdateDatasetResult:
    """Updates a dataset."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='UpdateDataset',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'updateDataset',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.UpdateDatasetResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def delete_dataset(client: _SyncClientImpl, request: models.DeleteDatasetRequest, **kwargs) -> models.DeleteDatasetResult:
    """Deletes a dataset."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteDataset',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'deleteDataset',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteDatasetResult(),
        op_output=op_output,
    )


def list_datasets(client: _SyncClientImpl, request: models.ListDatasetsRequest, **kwargs) -> models.ListDatasetsResult:
    """Lists datasets."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListDatasets',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'listDatasets',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListDatasetsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def simple_query(client: _SyncClientImpl, request: models.SimpleQueryRequest, **kwargs) -> models.SimpleQueryResult:
    """Performs a simple query."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='SimpleQuery',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'simpleQuery',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.SimpleQueryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def semantic_query(client: _SyncClientImpl, request: models.SemanticQueryRequest, **kwargs) -> models.SemanticQueryResult:
    """Performs a semantic query."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='SemanticQuery',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'semanticQuery',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.SemanticQueryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def delete_file_meta(client: _SyncClientImpl, request: models.DeleteFileMetaRequest, **kwargs) -> models.DeleteFileMetaResult:
    """Deletes file metadata."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteFileMeta',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'deleteFileMeta',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteFileMetaResult(),
        op_output=op_output,
    )
