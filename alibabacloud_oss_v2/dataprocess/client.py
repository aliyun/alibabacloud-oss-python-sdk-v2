# -*- coding: utf-8 -*-
"""Client used to interact with **Alibaba Cloud OSS DataProcess**."""
import copy
from .._client import _SyncClientImpl
from ..config import Config
from ..types import OperationInput, OperationOutput
from .. import utils

from . import models
from . import operations


class Client:
    """DataProcess Client
    """

    def __init__(self, config: Config, **kwargs) -> None:
        """Initialize DataProcess Client

        Args:
            config (Config): The configuration for the client.
        """
        _config = copy.copy(config)
        self._build_dataprocess_user_agent(_config)
        self._client = _SyncClientImpl(_config, **kwargs)

    def __repr__(self) -> str:
        return "<OssDataProcessClient>"

    def _build_dataprocess_user_agent(self, config: Config) -> str:
        base_agent = f'{utils.get_default_user_agent()};dataprocess-client'
        if config.user_agent:
            return f'{base_agent}/{config.user_agent}'
        return base_agent

    def invoke_operation(self, op_input: OperationInput, **kwargs) -> OperationOutput:
        """invoke operation

        Args:
            op_input (OperationInput): The input for the operation.

        Returns:
            OperationOutput: The output for the operation.
        """
        return self._client.invoke_operation(op_input, **kwargs)

    # ==================== Dataset ====================

    def create_dataset(self, request: models.CreateDatasetRequest, **kwargs) -> models.CreateDatasetResult:
        """Creates a dataset.

        Args:
            request (CreateDatasetRequest): The request for the CreateDataset operation.

        Returns:
            CreateDatasetResult: The result for the CreateDataset operation.
        """
        return operations.create_dataset(self._client, request, **kwargs)

    def get_dataset(self, request: models.GetDatasetRequest, **kwargs) -> models.GetDatasetResult:
        """Gets a dataset.

        Args:
            request (GetDatasetRequest): The request for the GetDataset operation.

        Returns:
            GetDatasetResult: The result for the GetDataset operation.
        """
        return operations.get_dataset(self._client, request, **kwargs)

    def update_dataset(self, request: models.UpdateDatasetRequest, **kwargs) -> models.UpdateDatasetResult:
        """Updates a dataset.

        Args:
            request (UpdateDatasetRequest): The request for the UpdateDataset operation.

        Returns:
            UpdateDatasetResult: The result for the UpdateDataset operation.
        """
        return operations.update_dataset(self._client, request, **kwargs)

    def delete_dataset(self, request: models.DeleteDatasetRequest, **kwargs) -> models.DeleteDatasetResult:
        """Deletes a dataset.

        Args:
            request (DeleteDatasetRequest): The request for the DeleteDataset operation.

        Returns:
            DeleteDatasetResult: The result for the DeleteDataset operation.
        """
        return operations.delete_dataset(self._client, request, **kwargs)

    def list_datasets(self, request: models.ListDatasetsRequest, **kwargs) -> models.ListDatasetsResult:
        """Lists datasets.

        Args:
            request (ListDatasetsRequest): The request for the ListDatasets operation.

        Returns:
            ListDatasetsResult: The result for the ListDatasets operation.
        """
        return operations.list_datasets(self._client, request, **kwargs)

    def delete_file_meta(self, request: models.DeleteFileMetaRequest, **kwargs) -> models.DeleteFileMetaResult:
        """Deletes file metadata.

        Args:
            request (DeleteFileMetaRequest): The request for the DeleteFileMeta operation.

        Returns:
            DeleteFileMetaResult: The result for the DeleteFileMeta operation.
        """
        return operations.delete_file_meta(self._client, request, **kwargs)

    # ==================== Query ====================

    def simple_query(self, request: models.SimpleQueryRequest, **kwargs) -> models.SimpleQueryResult:
        """Performs a simple query.

        Args:
            request (SimpleQueryRequest): The request for the SimpleQuery operation.

        Returns:
            SimpleQueryResult: The result for the SimpleQuery operation.
        """
        return operations.simple_query(self._client, request, **kwargs)

    def semantic_query(self, request: models.SemanticQueryRequest, **kwargs) -> models.SemanticQueryResult:
        """Performs a semantic query.

        Args:
            request (SemanticQueryRequest): The request for the SemanticQuery operation.

        Returns:
            SemanticQueryResult: The result for the SemanticQuery operation.
        """
        return operations.semantic_query(self._client, request, **kwargs)

    # ==================== MetaQuery ====================

    def open_meta_query(self, request: models.OpenMetaQueryRequest, **kwargs) -> models.OpenMetaQueryResult:
        """Opens meta query for a bucket.

        Args:
            request (OpenMetaQueryRequest): The request for the OpenMetaQuery operation.

        Returns:
            OpenMetaQueryResult: The result for the OpenMetaQuery operation.
        """
        return operations.open_meta_query(self._client, request, **kwargs)

    def get_meta_query_status(self, request: models.GetMetaQueryStatusRequest, **kwargs) -> models.GetMetaQueryStatusResult:
        """Gets the meta query status.

        Args:
            request (GetMetaQueryStatusRequest): The request for the GetMetaQueryStatus operation.

        Returns:
            GetMetaQueryStatusResult: The result for the GetMetaQueryStatus operation.
        """
        return operations.get_meta_query_status(self._client, request, **kwargs)

    def close_meta_query(self, request: models.CloseMetaQueryRequest, **kwargs) -> models.CloseMetaQueryResult:
        """Closes meta query for a bucket.

        Args:
            request (CloseMetaQueryRequest): The request for the CloseMetaQuery operation.

        Returns:
            CloseMetaQueryResult: The result for the CloseMetaQuery operation.
        """
        return operations.close_meta_query(self._client, request, **kwargs)

    def do_meta_query(self, request: models.DoMetaQueryRequest, **kwargs) -> models.DoMetaQueryResult:
        """Performs a meta query.

        Args:
            request (DoMetaQueryRequest): The request for the DoMetaQuery operation.

        Returns:
            DoMetaQueryResult: The result for the DoMetaQuery operation.
        """
        return operations.do_meta_query(self._client, request, **kwargs)

    # ==================== SmartCluster ====================

    def create_smart_cluster(self, request: models.CreateSmartClusterRequest, **kwargs) -> models.CreateSmartClusterResult:
        """Creates a smart cluster.

        Args:
            request (CreateSmartClusterRequest): The request for the CreateSmartCluster operation.

        Returns:
            CreateSmartClusterResult: The result for the CreateSmartCluster operation.
        """
        return operations.create_smart_cluster(self._client, request, **kwargs)

    def get_smart_cluster(self, request: models.GetSmartClusterRequest, **kwargs) -> models.GetSmartClusterResult:
        """Gets a smart cluster.

        Args:
            request (GetSmartClusterRequest): The request for the GetSmartCluster operation.

        Returns:
            GetSmartClusterResult: The result for the GetSmartCluster operation.
        """
        return operations.get_smart_cluster(self._client, request, **kwargs)

    def update_smart_cluster(self, request: models.UpdateSmartClusterRequest, **kwargs) -> models.UpdateSmartClusterResult:
        """Updates a smart cluster.

        Args:
            request (UpdateSmartClusterRequest): The request for the UpdateSmartCluster operation.

        Returns:
            UpdateSmartClusterResult: The result for the UpdateSmartCluster operation.
        """
        return operations.update_smart_cluster(self._client, request, **kwargs)

    def delete_smart_cluster(self, request: models.DeleteSmartClusterRequest, **kwargs) -> models.DeleteSmartClusterResult:
        """Deletes a smart cluster.

        Args:
            request (DeleteSmartClusterRequest): The request for the DeleteSmartCluster operation.

        Returns:
            DeleteSmartClusterResult: The result for the DeleteSmartCluster operation.
        """
        return operations.delete_smart_cluster(self._client, request, **kwargs)

    def list_smart_clusters(self, request: models.ListSmartClustersRequest, **kwargs) -> models.ListSmartClustersResult:
        """Lists smart clusters.

        Args:
            request (ListSmartClustersRequest): The request for the ListSmartClusters operation.

        Returns:
            ListSmartClustersResult: The result for the ListSmartClusters operation.
        """
        return operations.list_smart_clusters(self._client, request, **kwargs)

    # ==================== DataPipeline ====================

    def put_data_pipeline_configuration(self, request: models.PutDataPipelineConfigurationRequest, **kwargs) -> models.PutDataPipelineConfigurationResult:
        """Creates or updates a data pipeline configuration.

        Args:
            request (PutDataPipelineConfigurationRequest): The request for the PutDataPipelineConfiguration operation.

        Returns:
            PutDataPipelineConfigurationResult: The result for the PutDataPipelineConfiguration operation.
        """
        return operations.put_data_pipeline_configuration(self._client, request, **kwargs)

    def get_data_pipeline_configuration(self, request: models.GetDataPipelineConfigurationRequest, **kwargs) -> models.GetDataPipelineConfigurationResult:
        """Gets a data pipeline configuration.

        Args:
            request (GetDataPipelineConfigurationRequest): The request for the GetDataPipelineConfiguration operation.

        Returns:
            GetDataPipelineConfigurationResult: The result for the GetDataPipelineConfiguration operation.
        """
        return operations.get_data_pipeline_configuration(self._client, request, **kwargs)

    def delete_data_pipeline_configuration(self, request: models.DeleteDataPipelineConfigurationRequest, **kwargs) -> models.DeleteDataPipelineConfigurationResult:
        """Deletes a data pipeline configuration.

        Args:
            request (DeleteDataPipelineConfigurationRequest): The request for the DeleteDataPipelineConfiguration operation.

        Returns:
            DeleteDataPipelineConfigurationResult: The result for the DeleteDataPipelineConfiguration operation.
        """
        return operations.delete_data_pipeline_configuration(self._client, request, **kwargs)

    def list_data_pipeline_configurations(self, request: models.ListDataPipelineConfigurationsRequest, **kwargs) -> models.ListDataPipelineConfigurationsResult:
        """Lists data pipeline configurations.

        Args:
            request (ListDataPipelineConfigurationsRequest): The request for the ListDataPipelineConfigurations operation.

        Returns:
            ListDataPipelineConfigurationsResult: The result for the ListDataPipelineConfigurations operation.
        """
        return operations.list_data_pipeline_configurations(self._client, request, **kwargs)

    def pause_data_pipeline(self, request: models.PauseDataPipelineRequest, **kwargs) -> models.PauseDataPipelineResult:
        """Pauses a data pipeline.

        Args:
            request (PauseDataPipelineRequest): The request for the PauseDataPipeline operation.

        Returns:
            PauseDataPipelineResult: The result for the PauseDataPipeline operation.
        """
        return operations.pause_data_pipeline(self._client, request, **kwargs)

    def restart_data_pipeline(self, request: models.RestartDataPipelineRequest, **kwargs) -> models.RestartDataPipelineResult:
        """Restarts a data pipeline.

        Args:
            request (RestartDataPipelineRequest): The request for the RestartDataPipeline operation.

        Returns:
            RestartDataPipelineResult: The result for the RestartDataPipeline operation.
        """
        return operations.restart_data_pipeline(self._client, request, **kwargs)
