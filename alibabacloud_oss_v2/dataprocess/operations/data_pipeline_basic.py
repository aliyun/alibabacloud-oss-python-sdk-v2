# -*- coding: utf-8 -*-
"""DataPipeline operations for dataprocess."""

from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models


def put_data_pipeline_configuration(client: _SyncClientImpl, request: models.PutDataPipelineConfigurationRequest, **kwargs) -> models.PutDataPipelineConfigurationResult:
    """Creates or updates a data pipeline configuration."""

    op_input = OperationInput(
        op_name='PutDataPipelineConfiguration',
        method='POST',
        headers=CaseInsensitiveDict({
            'Content-Type': 'application/xml',
        }),
        parameters={
            'dataPipeline': '',
            'action': 'putDataPipelineConfiguration',
        },
        op_metadata={'sub-resource': ['dataPipeline', 'action']},
    )

    # Serialize XML body if present
    if request.configuration is not None:
        _xml_map = getattr(request.configuration, '_xml_map', {})
        op_input.body = serde.serialize_xml(request.configuration, root=_xml_map.get('name', None))

    op_input = serde.serialize_input(
        request=request,
        op_input=op_input,
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutDataPipelineConfigurationResult(),
        op_output=op_output,
    )


def get_data_pipeline_configuration(client: _SyncClientImpl, request: models.GetDataPipelineConfigurationRequest, **kwargs) -> models.GetDataPipelineConfigurationResult:
    """Gets a data pipeline configuration."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetDataPipelineConfiguration',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'dataPipeline': '',
                'action': 'getDataPipelineConfiguration',
            },
            op_metadata={'sub-resource': ['dataPipeline', 'action']},
        ),
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetDataPipelineConfigurationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def delete_data_pipeline_configuration(client: _SyncClientImpl, request: models.DeleteDataPipelineConfigurationRequest, **kwargs) -> models.DeleteDataPipelineConfigurationResult:
    """Deletes a data pipeline configuration."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteDataPipelineConfiguration',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'dataPipeline': '',
                'action': 'deleteDataPipelineConfiguration',
            },
            op_metadata={'sub-resource': ['dataPipeline', 'action']},
        ),
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteDataPipelineConfigurationResult(),
        op_output=op_output,
    )


def list_data_pipeline_configurations(client: _SyncClientImpl, request: models.ListDataPipelineConfigurationsRequest, **kwargs) -> models.ListDataPipelineConfigurationsResult:
    """Lists data pipeline configurations."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListDataPipelineConfigurations',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'dataPipeline': '',
                'action': 'listDataPipelineConfigurations',
            },
            op_metadata={'sub-resource': ['dataPipeline', 'action']},
        ),
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListDataPipelineConfigurationsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def pause_data_pipeline(client: _SyncClientImpl, request: models.PauseDataPipelineRequest, **kwargs) -> models.PauseDataPipelineResult:
    """Pauses a data pipeline."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PauseDataPipeline',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'dataPipeline': '',
                'action': 'pauseDataPipeline',
            },
            op_metadata={'sub-resource': ['dataPipeline', 'action']},
        ),
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PauseDataPipelineResult(),
        op_output=op_output,
    )


def restart_data_pipeline(client: _SyncClientImpl, request: models.RestartDataPipelineRequest, **kwargs) -> models.RestartDataPipelineResult:
    """Restarts a data pipeline."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='RestartDataPipeline',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'dataPipeline': '',
                'action': 'restartDataPipeline',
            },
            op_metadata={'sub-resource': ['dataPipeline', 'action']},
        ),
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.RestartDataPipelineResult(),
        op_output=op_output,
    )
