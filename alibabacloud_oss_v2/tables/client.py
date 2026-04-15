# -*- coding: utf-8 -*-
"""Client used to interact with **Alibaba Cloud OSS Tables**."""
import copy
from .._client import _SyncClientImpl, AddressStyle
from ..config import Config
from ..types import OperationInput, OperationOutput
from ..signer.tables_v4 import TablesSignerV4
from .. import utils
from .. import validation

from . import models
from . import operations
from . import endpoints
from .paginator import (
    ListNamespacesPaginator,
    ListTableBucketsPaginator,
    ListTablesPaginator
)


class Client:
    """Tables Client
    """

    def __init__(self, config: Config, **kwargs) -> None:
        """Initialize Tables Client

        Args:
            config (Config): _description_
        """

        _config = copy.copy(config)
        self._resolve_tables_endpoint(_config)
        self._build_tables_user_agent(_config)
        self._client = _SyncClientImpl(_config, **kwargs)
        self._client._options.signer = TablesSignerV4()

        self._client._options.endpoint_provider = endpoints.TablesEndpointProvider(
            endpoint=self._client._options.endpoint,
            address_style=self._client._options.address_style
        )
        self._client._options.product = 'osstables'

    def __repr__(self) -> str:
        return "<OssTablesClient>"

    def _resolve_tables_endpoint(self, config: Config) -> None:
        """tables endpoint"""
        if config.endpoint is not None:
            return

        if not validation.is_valid_region(config.region):
            return

        if bool(config.use_internal_endpoint):
            etype = "internal"
        else:
            etype = "default"

        config.endpoint = endpoints.from_region(config.region, etype)


    def _build_tables_user_agent(self, config: Config) -> str:
        if config.user_agent:
            return f'{utils.get_tables_user_agent()}/{config.user_agent}'

        return utils.get_tables_user_agent()

    def invoke_operation(self, op_input: OperationInput, **kwargs
                         ) -> OperationOutput:
        """invoke operation

        Args:
            op_input (OperationInput): _description_

        Returns:
            OperationOutput: _description_
        """
        return self._client.invoke_operation(op_input, **kwargs)

    # namespace
    def create_namespace(self, request: models.CreateNamespaceRequest, **kwargs
                   ) -> models.CreateNamespaceResult:
        """
        Creates a namespace.

        Args:
            request (CreateNamespaceRequest): Request parameters for CreateNamespace operation.

        Returns:
            CreateNamespaceResult: Response result for CreateNamespace operation.
        """

        return operations.create_namespace(self._client, request, **kwargs)

    def delete_namespace(self, request: models.DeleteNamespaceRequest, **kwargs
                        ) -> models.DeleteNamespaceResult:
        """
        Deletes a namespace.

        Args:
            request (DeleteNamespaceRequest): Request parameters for DeleteNamespace operation.

        Returns:
            DeleteNamespaceResult: Response result for DeleteNamespace operation.
        """

        return operations.delete_namespace(self._client, request, **kwargs)

    def get_namespace(self, request: models.GetNamespaceRequest, **kwargs
                        ) -> models.GetNamespaceResult:
        """
        Gets the information of a namespace.

        Args:
            request (GetNamespaceRequest): Request parameters for GetNamespace operation.

        Returns:
            GetNamespaceResult: Response result for GetNamespace operation.
        """

        return operations.get_namespace(self._client, request, **kwargs)

    def list_namespaces(self, request: models.ListNamespacesRequest, **kwargs
                     ) -> models.ListNamespacesResult:
        """
        Lists namespaces.

        Args:
            request (ListNamespacesRequest): Request parameters for ListNamespaces operation.

        Returns:
            ListNamespacesResult: Response result for ListNamespaces operation.
        """

        return operations.list_namespaces(self._client, request, **kwargs)

    # table bucket
    def create_table_bucket(self, request: models.CreateTableBucketRequest, **kwargs
                   ) -> models.CreateTableBucketResult:
        """
        Creates a table bucket.

        Args:
            request (CreateTableBucketRequest): Request parameters for CreateTableBucket operation.

        Returns:
            CreateTableBucketResult: Response result for CreateTableBucket operation.
        """

        return operations.create_table_bucket(self._client, request, **kwargs)

    def delete_table_bucket(self, request: models.DeleteTableBucketRequest, **kwargs
                      ) -> models.DeleteTableBucketResult:
        """
        Deletes a table bucket.

        Args:
            request (DeleteTableBucketRequest): Request parameters for DeleteTableBucket operation.

        Returns:
            DeleteTableBucketResult: Response result for DeleteTableBucket operation.
        """

        return operations.delete_table_bucket(self._client, request, **kwargs)

    def get_table_bucket(self, request: models.GetTableBucketRequest, **kwargs
                        ) -> models.GetTableBucketResult:
        """
        Gets the information of a table bucket.

        Args:
            request (GetTableBucketRequest): Request parameters for GetTableBucket operation.

        Returns:
            GetTableBucketResult: Response result for GetTableBucket operation.
        """

        return operations.get_table_bucket(self._client, request, **kwargs)

    def list_table_buckets(self, request: models.ListTableBucketsRequest, **kwargs
                     ) -> models.ListTableBucketsResult:
        """
        Lists table buckets.

        Args:
            request (ListTableBucketsRequest): Request parameters for ListTableBuckets operation.

        Returns:
            ListTableBucketsResult: Response result for ListTableBuckets operation.
        """

        return operations.list_table_buckets(self._client, request, **kwargs)

    # table
    def create_table(self, request: models.CreateTableRequest, **kwargs) -> models.CreateTableResult:
        """
        Creates a table.

        Args:
            request (CreateTableRequest): The request for the CreateTable operation.

        Returns:
            CreateTableResult: The result for the CreateTable operation.
        """
        return operations.create_table(self._client, request, **kwargs)

    def delete_table(self, request: models.DeleteTableRequest, **kwargs) -> models.DeleteTableResult:
        """
        Deletes a table.

        Args:
            request (DeleteTableRequest): The request for the DeleteTable operation.

        Returns:
            DeleteTableResult: The result for the DeleteTable operation.
        """
        return operations.delete_table(self._client, request, **kwargs)

    def get_table(self, request: models.GetTableRequest, **kwargs) -> models.GetTableResult:
        """
        Gets the information of a table.

        Args:
            request (GetTableRequest): The request for the GetTable operation.

        Returns:
            GetTableResult: The result for the GetTable operation.
        """
        return operations.get_table(self._client, request, **kwargs)

    def list_tables(self, request: models.ListTablesRequest, **kwargs) -> models.ListTablesResult:
        """
        Lists tables.

        Args:
            request (ListTablesRequest): The request for the ListTables operation.

        Returns:
            ListTablesResult: The result for the ListTables operation.
        """
        return operations.list_tables(self._client, request, **kwargs)

    def rename_table(self, request: models.RenameTableRequest, **kwargs) -> models.RenameTableResult:
        """
        Renames a table.

        Args:
            request (RenameTableRequest): The request for the RenameTable operation.

        Returns:
            RenameTableResult: The result for the RenameTable operation.
        """
        return operations.rename_table(self._client, request, **kwargs)

    # paginator
    def list_namespaces_paginator(self, **kwargs) -> ListNamespacesPaginator:
        """Creates a paginator for ListNamespaces

        Returns:
            ListNamespacesPaginator: a paginator for ListNamespaces
        """
        return ListNamespacesPaginator(self, **kwargs)

    def list_table_buckets_paginator(self, **kwargs) -> ListTableBucketsPaginator:
        """Creates a paginator for ListTableBuckets

        Returns:
            ListTableBucketsPaginator: a paginator for ListTableBuckets
        """
        return ListTableBucketsPaginator(self, **kwargs)

    def list_tables_paginator(self, **kwargs) -> ListTablesPaginator:
        """Creates a paginator for ListTables

        Returns:
            ListTablesPaginator: a paginator for ListTables
        """
        return ListTablesPaginator(self, **kwargs)

    # table bucket config api
    def delete_table_bucket_encryption(self, request: models.DeleteTableBucketEncryptionRequest, **kwargs
                      ) -> models.DeleteTableBucketEncryptionResult:
        """
        Deletes the encryption configuration of a table bucket.

        Args:
            request (DeleteTableBucketEncryptionRequest): Request parameters for DeleteTableBucketEncryption operation.

        Returns:
            DeleteTableBucketEncryptionResult: Response result for DeleteTableBucketEncryption operation.
        """

        return operations.delete_table_bucket_encryption(self._client, request, **kwargs)

    def get_table_bucket_encryption(self, request: models.GetTableBucketEncryptionRequest, **kwargs
                        ) -> models.GetTableBucketEncryptionResult:
        """
        Gets the encryption configuration of a table bucket.

        Args:
            request (GetTableBucketEncryptionRequest): Request parameters for GetTableBucketEncryption operation.

        Returns:
            GetTableBucketEncryptionResult: Response result for GetTableBucketEncryption operation.
        """

        return operations.get_table_bucket_encryption(self._client, request, **kwargs)

    def put_table_bucket_encryption(self, request: models.PutTableBucketEncryptionRequest, **kwargs
                      ) -> models.PutTableBucketEncryptionResult:
        """
        Sets the encryption configuration of a table bucket.

        Args:
            request (PutTableBucketEncryptionRequest): Request parameters for PutTableBucketEncryption operation.

        Returns:
            PutTableBucketEncryptionResult: Response result for PutTableBucketEncryption operation.
        """

        return operations.put_table_bucket_encryption(self._client, request, **kwargs)

    def get_table_bucket_maintenance_configuration(self, request: models.GetTableBucketMaintenanceConfigurationRequest, **kwargs
                      ) -> models.GetTableBucketMaintenanceConfigurationResult:
        """
        Gets the maintenance configuration of a table bucket.

        Args:
            request (GetTableBucketMaintenanceConfigurationRequest): Request parameters for GetTableBucketMaintenanceConfiguration operation.

        Returns:
            GetTableBucketMaintenanceConfigurationResult: Response result for GetTableBucketMaintenanceConfiguration operation.
        """

        return operations.get_table_bucket_maintenance_configuration(self._client, request, **kwargs)

    def put_table_bucket_maintenance_configuration(self, request: models.PutTableBucketMaintenanceConfigurationRequest, **kwargs
                      ) -> models.PutTableBucketMaintenanceConfigurationResult:
        """
        Sets the maintenance configuration of a table bucket.

        Args:
            request (PutTableBucketMaintenanceConfigurationRequest): Request parameters for PutTableBucketMaintenanceConfiguration operation.

        Returns:
            PutTableBucketMaintenanceConfigurationResult: Response result for PutTableBucketMaintenanceConfiguration operation.
        """

        return operations.put_table_bucket_maintenance_configuration(self._client, request, **kwargs)

    def delete_table_bucket_policy(self, request: models.DeleteTableBucketPolicyRequest, **kwargs
                      ) -> models.DeleteTableBucketPolicyResult:
        """
        Deletes the policy of a table bucket.

        Args:
            request (DeleteTableBucketPolicyRequest): Request parameters for DeleteTableBucketPolicy operation.

        Returns:
            DeleteTableBucketPolicyResult: Response result for DeleteTableBucketPolicy operation.
        """

        return operations.delete_table_bucket_policy(self._client, request, **kwargs)

    def get_table_bucket_policy(self, request: models.GetTableBucketPolicyRequest, **kwargs
                        ) -> models.GetTableBucketPolicyResult:
        """
        Gets the policy of a table bucket.

        Args:
            request (GetTableBucketPolicyRequest): Request parameters for GetTableBucketPolicy operation.

        Returns:
            GetTableBucketPolicyResult: Response result for GetTableBucketPolicy operation.
        """

        return operations.get_table_bucket_policy(self._client, request, **kwargs)

    def put_table_bucket_policy(self, request: models.PutTableBucketPolicyRequest, **kwargs
                      ) -> models.PutTableBucketPolicyResult:
        """
        Sets the policy of a table bucket.

        Args:
            request (PutTableBucketPolicyRequest): Request parameters for PutTableBucketPolicy operation.

        Returns:
            PutTableBucketPolicyResult: Response result for PutTableBucketPolicy operation.
        """

        return operations.put_table_bucket_policy(self._client, request, **kwargs)

    # table config api
    def get_table_encryption(self, request: models.GetTableEncryptionRequest, **kwargs
                   ) -> models.GetTableEncryptionResult:
        """
        Gets the encryption configuration of a table.

        Args:
            request (GetTableEncryptionRequest): Request parameters for GetTableEncryption operation.

        Returns:
            GetTableEncryptionResult: Response result for GetTableEncryption operation.
        """

        return operations.get_table_encryption(self._client, request, **kwargs)

    def get_table_maintenance_configuration(self, request: models.GetTableMaintenanceConfigurationRequest, **kwargs
                   ) -> models.GetTableMaintenanceConfigurationResult:
        """
        Gets the maintenance configuration of a table.

        Args:
            request (GetTableMaintenanceConfigurationRequest): Request parameters for GetTableMaintenanceConfiguration operation.

        Returns:
            GetTableMaintenanceConfigurationResult: Response result for GetTableMaintenanceConfiguration operation.
        """

        return operations.get_table_maintenance_configuration(self._client, request, **kwargs)

    def put_table_maintenance_configuration(self, request: models.PutTableMaintenanceConfigurationRequest, **kwargs
                   ) -> models.PutTableMaintenanceConfigurationResult:
        """
        Sets the maintenance configuration of a table.

        Args:
            request (PutTableMaintenanceConfigurationRequest): Request parameters for PutTableMaintenanceConfiguration operation.

        Returns:
            PutTableMaintenanceConfigurationResult: Response result for PutTableMaintenanceConfiguration operation.
        """

        return operations.put_table_maintenance_configuration(self._client, request, **kwargs)

    def get_table_maintenance_job_status(self, request: models.GetTableMaintenanceJobStatusRequest, **kwargs
                   ) -> models.GetTableMaintenanceJobStatusResult:
        """
        Gets the maintenance job status of a table.

        Args:
            request (GetTableMaintenanceJobStatusRequest): Request parameters for GetTableMaintenanceJobStatus operation.

        Returns:
            GetTableMaintenanceJobStatusResult: Response result for GetTableMaintenanceJobStatus operation.
        """

        return operations.get_table_maintenance_job_status(self._client, request, **kwargs)

    def get_table_metadata_location(self, request: models.GetTableMetadataLocationRequest, **kwargs
                   ) -> models.GetTableMetadataLocationResult:
        """
        Gets the metadata location of a table.

        Args:
            request (GetTableMetadataLocationRequest): Request parameters for GetTableMetadataLocation operation.

        Returns:
            GetTableMetadataLocationResult: Response result for GetTableMetadataLocation operation.
        """

        return operations.get_table_metadata_location(self._client, request, **kwargs)

    def update_table_metadata_location(self, request: models.UpdateTableMetadataLocationRequest, **kwargs
                   ) -> models.UpdateTableMetadataLocationResult:
        """
        Updates the metadata location of a table.

        Args:
            request (UpdateTableMetadataLocationRequest): Request parameters for UpdateTableMetadataLocation operation.

        Returns:
            UpdateTableMetadataLocationResult: Response result for UpdateTableMetadataLocation operation.
        """

        return operations.update_table_metadata_location(self._client, request, **kwargs)

    def delete_table_policy(self, request: models.DeleteTablePolicyRequest, **kwargs
                   ) -> models.DeleteTablePolicyResult:
        """
        Deletes the policy of a table.

        Args:
            request (DeleteTablePolicyRequest): Request parameters for DeleteTablePolicy operation.

        Returns:
            DeleteTablePolicyResult: Response result for DeleteTablePolicy operation.
        """

        return operations.delete_table_policy(self._client, request, **kwargs)

    def get_table_policy(self, request: models.GetTablePolicyRequest, **kwargs
                   ) -> models.GetTablePolicyResult:
        """
        Gets the policy of a table.

        Args:
            request (GetTablePolicyRequest): Request parameters for GetTablePolicy operation.

        Returns:
            GetTablePolicyResult: Response result for GetTablePolicy operation.
        """

        return operations.get_table_policy(self._client, request, **kwargs)

    def put_table_policy(self, request: models.PutTablePolicyRequest, **kwargs
                   ) -> models.PutTablePolicyResult:
        """
        Sets the policy of a table.

        Args:
            request (PutTablePolicyRequest): Request parameters for PutTablePolicy operation.

        Returns:
            PutTablePolicyResult: Response result for PutTablePolicy operation.
        """

        return operations.put_table_policy(self._client, request, **kwargs)
