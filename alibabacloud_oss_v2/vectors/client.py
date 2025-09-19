# pylint: disable=line-too-long
"""Client used to interact with **Alibaba Cloud Object Storage Service (OSS)**."""
import copy
from .._client import _SyncClientImpl
from ..config import Config
from ..types import OperationInput, OperationOutput
from ..signer.vectors_v4 import VectorsSignerV4
from .. import utils
from .. import validation

from . import models
from . import operations
from . import endpoints
from .paginator import (
    ListVectorBucketsPaginator,
    ListVectorIndexesPaginator,
    ListVectorsPaginator
)


class Client:
    """Vectors Client
    """

    def __init__(self, config: Config, **kwargs) -> None:
        """Initialize Vectors Client

        Args:
            config (Config): _description_
        """

        _config = copy.copy(config)
        self._resolve_vectors_endpoint(_config)
        self._build_vectors_user_agent(_config)
        self._client = _SyncClientImpl(_config, **kwargs)
        self._client._options.signer = VectorsSignerV4(account_id=config.account_id)
        self._client._options.endpoint_provider = endpoints.VectorsEndpointProvider(
            account_id=config.account_id,
            endpoint=self._client._options.endpoint
        )

    def __repr__(self) -> str:
        return "<OssVectorsClient>"

    def _resolve_vectors_endpoint(self, config: Config) -> None:
        """vectors endpoint"""
        if config.endpoint is not None:
            return

        if not validation.is_valid_region(config.region):
            return

        if bool(config.use_internal_endpoint):
            etype = "internal"
        else:
            etype = "default"

        config.endpoint = endpoints.from_region(config.region, etype)


    def _build_vectors_user_agent(self, config: Config) -> str:
        if config.user_agent:
            return f'{utils.get_vector_user_agent()}/{config.user_agent}'

        return utils.get_vector_user_agent()

    def invoke_operation(self, op_input: OperationInput, **kwargs
                         ) -> OperationOutput:
        """invoke operation

        Args:
            op_input (OperationInput): _description_

        Returns:
            OperationOutput: _description_
        """
        return self._client.invoke_operation(op_input, **kwargs)

    # bucket
    def put_vector_bucket(self, request: models.PutVectorBucketRequest, **kwargs
                   ) -> models.PutVectorBucketResult:
        """
        Creates a bucket.

        Args:
            request (PutVectorBucketRequest): Request parameters for PutVectorBucket operation.

        Returns:
            PutVectorBucketResult: Response result for PutBucket operation.
        """

        return operations.put_vector_bucket(self._client, request, **kwargs)

    def get_vector_bucket(self, request: models.GetVectorBucketRequest, **kwargs
                        ) -> models.GetVectorBucketResult:
        """
        GetBucketInfo Queries information about a bucket.

        Args:
            request (GetVectorBucketRequest): Request parameters for GetVectorBucket operation.

        Returns:
            GetVectorBucketResult: Response result for GetVectorBucket operation.
        """

        return operations.get_vector_bucket(self._client, request, **kwargs)

    def delete_vector_bucket(self, request: models.DeleteVectorBucketRequest, **kwargs
                      ) -> models.DeleteVectorBucketResult:
        """
        Deletes a bucket.

        Args:
            request (DeleteVectorBucketRequest): Request parameters for DeleteVectorBucket operation.

        Returns:
            DeleteVectorBucketResult: Response result for DeleteVectorBucket operation.
        """

        return operations.delete_vector_bucket(self._client, request, **kwargs)

    def list_vector_buckets(self, request: models.ListVectorBucketsRequest, **kwargs
                     ) -> models.ListVectorBucketsResult:
        """
        Lists all buckets that belong to your Alibaba Cloud account.

        Args:
            request (ListVectorBucketsRequest): Request parameters for ListBuckets operation.

        Returns:
            ListVectorBucketsResult: Response result for ListVectorBuckets operation.
        """

        return operations.list_vector_buckets(self._client, request, **kwargs)

    # bucket policy
    def put_bucket_policy(self, request: models.PutBucketPolicyRequest, **kwargs
                          ) -> models.PutBucketPolicyResult:
        """
        Configures a policy for a bucket.

        Args:
            request (PutBucketPolicyRequest): Request parameters for PutBucketPolicy operation.

        Returns:
            PutBucketPolicyResult: Response result for PutBucketPolicy operation.
        """
        return operations.put_bucket_policy(self._client, request, **kwargs)

    def get_bucket_policy(self, request: models.GetBucketPolicyRequest, **kwargs
                          ) -> models.GetBucketPolicyResult:
        """
        Queries the policies configured for a bucket.

        Args:
            request (GetBucketPolicyRequest): Request parameters for GetBucketPolicy operation.

        Returns:
            GetBucketPolicyResult: Response result for GetBucketPolicy operation.
        """
        return operations.get_bucket_policy(self._client, request, **kwargs)

    def delete_bucket_policy(self, request: models.DeleteBucketPolicyRequest, **kwargs
                             ) -> models.DeleteBucketPolicyResult:
        """
        Deletes a policy for a bucket.

        Args:
            request (DeleteBucketPolicyRequest): Request parameters for DeleteBucketPolicy operation.

        Returns:
            DeleteBucketPolicyResult: Response result for DeleteBucketPolicy operation.
        """
        return operations.delete_bucket_policy(self._client, request, **kwargs)


    # index
    def put_vector_index(self, request: models.PutVectorIndexRequest, **kwargs) -> models.PutVectorIndexResult:
        """
        Create or update a vector index.

        Args:
            request (PutVectorIndexRequest): The request for the PutVectorIndex operation.

        Returns:
            PutVectorIndexResult: The result for the PutVectorIndex operation.
        """
        return operations.put_vector_index(self._client, request, **kwargs)

    def get_vector_index(self, request: models.GetVectorIndexRequest, **kwargs) -> models.GetVectorIndexResult:
        """
        Get information about a specific vector index.

        Args:
            request (GetVectorIndexRequest): The request for the GetVectorIndex operation.

        Returns:
            GetVectorIndexResult: The result for the GetVectorIndex operation.
        """
        return operations.get_vector_index(self._client, request, **kwargs)

    def list_vector_indexes(self, request: models.ListVectorIndexesRequest, **kwargs) -> models.ListVectorIndexesResult:
        """
        List vector indexes in a bucket.

        Args:
            request (ListVectorIndexesRequest): The request for the ListVectorIndexes operation.

        Returns:
            ListVectorIndexesResult: The result for the ListVectorIndexes operation.
        """
        return operations.list_vector_indexes(self._client, request, **kwargs)

    def delete_vector_index(self, request: models.DeleteVectorIndexRequest, **kwargs) -> models.DeleteVectorIndexResult:
        """
        Delete a vector index.

        Args:
            request (DeleteVectorIndexRequest): The request for the DeleteVectorIndex operation.

        Returns:
            DeleteVectorIndexResult: The result for the DeleteVectorIndex operation.
        """
        return operations.delete_vector_index(self._client, request, **kwargs)

    # vector
    def put_vectors(self, request: models.PutVectorsRequest, **kwargs) -> models.PutVectorsResult:
        """
        Put vectors into an index.

        Args:
            request (PutVectorsRequest): The request for the PutVectors operation.

        Returns:
            PutVectorsResult: The result for the PutVectors operation.
        """
        return operations.put_vectors(self._client, request, **kwargs)

    def get_vectors(self, request: models.GetVectorsRequest, **kwargs) -> models.GetVectorsResult:
        """
        Get vectors from an index.

        Args:
            request (GetVectorsRequest): The request for the GetVectors operation.

        Returns:
            GetVectorsResult: The result for the GetVectors operation.
        """
        return operations.get_vectors(self._client, request, **kwargs)

    def list_vectors(self, request: models.ListVectorsRequest, **kwargs) -> models.ListVectorsResult:
        """
        List vectors in an index.

        Args:
            request (ListVectorsRequest): The request for the ListVectors operation.

        Returns:
            ListVectorsResult: The result for the ListVectors operation.
        """
        return operations.list_vectors(self._client, request, **kwargs)

    def delete_vectors(self, request: models.DeleteVectorsRequest, **kwargs) -> models.DeleteVectorsResult:
        """
        Delete vectors from an index.

        Args:
            request (DeleteVectorsRequest): The request for the DeleteVectors operation.

        Returns:
            DeleteVectorsResult: The result for the DeleteVectors operation.
        """
        return operations.delete_vectors(self._client, request, **kwargs)

    def query_vectors(self, request: models.QueryVectorsRequest, **kwargs) -> models.QueryVectorsResult:
        """
        Query vectors in an index.

        Args:
            request (QueryVectorsRequest): The request for the QueryVectors operation.

        Returns:
            QueryVectorsResult: The result for the QueryVectors operation.
        """
        return operations.query_vectors(self._client, request, **kwargs)

    # bucket logging
    def put_bucket_logging(self, request: models.PutBucketLoggingRequest, **kwargs
                           ) -> models.PutBucketLoggingResult:
        """
        Enables logging for a bucket.

        Args:
            request (PutBucketLoggingRequest): Request parameters for PutBucketLogging operation.

        Returns:
            PutBucketLoggingResult: Response result for PutBucketLogging operation.
        """
        return operations.put_bucket_logging(self._client, request, **kwargs)

    def get_bucket_logging(self, request: models.GetBucketLoggingRequest, **kwargs
                           ) -> models.GetBucketLoggingResult:
        """
        Queries the logging configurations of a bucket.

        Args:
            request (GetBucketLoggingRequest): Request parameters for GetBucketLogging operation.

        Returns:
            GetBucketLoggingResult: Response result for GetBucketLogging operation.
        """
        return operations.get_bucket_logging(self._client, request, **kwargs)

    def delete_bucket_logging(self, request: models.DeleteBucketLoggingRequest, **kwargs
                              ) -> models.DeleteBucketLoggingResult:
        """
        Disables logging for a bucket.

        Args:
            request (DeleteBucketLoggingRequest): Request parameters for DeleteBucketLogging operation.

        Returns:
            DeleteBucketLoggingResult: Response result for DeleteBucketLogging operation.
        """
        return operations.delete_bucket_logging(self._client, request, **kwargs)

    # paginator
    def list_vector_buckets_paginator(self, **kwargs) -> ListVectorBucketsPaginator:
        """Creates a paginator for ListVectorBuckets

        Returns:
            ListVectorBucketsPaginator: a paginator for ListVectorBuckets
        """
        return ListVectorBucketsPaginator(self, **kwargs)

    def list_vector_indexes_paginator(self, **kwargs) -> ListVectorIndexesPaginator:
        """Creates a paginator for ListVectorIndex

        Returns:
            ListVectorIndexesPaginator: a paginator for ListVectorIndex
        """
        return ListVectorIndexesPaginator(self, **kwargs)

    def list_vectors_paginator(self, **kwargs) -> ListVectorsPaginator:
        """Creates a paginator for ListVectors

        Returns:
            ListVectorsPaginator: a paginator for ListVectors
        """
        return ListVectorsPaginator(self, **kwargs)