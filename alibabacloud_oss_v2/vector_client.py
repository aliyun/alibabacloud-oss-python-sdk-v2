# pylint: disable=line-too-long
"""Client used to interact with **Alibaba Cloud Object Storage Service (OSS)**."""
import copy
from ._client import _SyncClientImpl
from .config import Config
from .types import OperationInput, OperationOutput
from . import models, vector_models
from . import vectors_operation
from . import utils
from . import validation
from . import endpoints

class VectorClient:
    """Client
    """

    def __init__(self, config: Config, **kwargs) -> None:
        """Initialize Vector Client

        Args:
            config (Config): _description_
        """

        _config = copy.copy(config)
        self._resolve_vectors_endpoint(_config)
        self._build_vector_user_agent(_config)
        self._client = _SyncClientImpl(_config, **kwargs)
        # TODO
        # self._client._options.signer = SignerVectorsV4()


    def __repr__(self) -> str:
        return "<OssVectorClient>"

    def _resolve_vectors_endpoint(self, config: Config) -> None:
        """vectors endpoint"""
        disable_ssl = utils.safety_bool(config.disable_ssl)
        endpoint = utils.safety_str(config.endpoint)
        region = utils.safety_str(config.region)
        if len(endpoint) > 0:
            endpoint = endpoints.add_scheme(endpoint, disable_ssl)
        elif validation.is_valid_region(region):
            if bool(config.use_internal_endpoint):
                etype = "internal"
            else:
                etype = "default"

            endpoint = endpoints.from_region(region, disable_ssl, etype)

        if endpoint == "":
            return

        config.endpoint = endpoint

    def _build_vector_user_agent(self, config: Config) -> str:
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
    def put_vector_bucket(self, request: vector_models.PutVectorBucketRequest, **kwargs
                   ) -> vector_models.PutVectorBucketResult:
        """
        Creates a bucket.

        Args:
            request (PutVectorBucketRequest): Request parameters for PutVectorBucket operation.

        Returns:
            PutVectorBucketResult: Response result for PutBucket operation.
        """

        return vectors_operation.put_vector_bucket(self._client, request, **kwargs)

    def get_vector_bucket(self, request: vector_models.GetVectorBucketRequest, **kwargs
                        ) -> vector_models.GetVectorBucketResult:
        """
        GetBucketInfo Queries information about a bucket.

        Args:
            request (GetVectorBucketRequest): Request parameters for GetVectorBucket operation.

        Returns:
            GetVectorBucketResult: Response result for GetVectorBucket operation.
        """

        return vectors_operation.get_vector_bucket(self._client, request, **kwargs)

    def delete_vector_bucket(self, request: vector_models.DeleteVectorBucketRequest, **kwargs
                      ) -> vector_models.DeleteVectorBucketResult:
        """
        Deletes a bucket.

        Args:
            request (DeleteVectorBucketRequest): Request parameters for DeleteVectorBucket operation.

        Returns:
            DeleteVectorBucketResult: Response result for DeleteVectorBucket operation.
        """

        return vectors_operation.delete_vector_bucket(self._client, request, **kwargs)

    def list_vector_buckets(self, request: vector_models.ListVectorBucketsRequest, **kwargs
                     ) -> vector_models.ListVectorBucketsResult:
        """
        Lists all buckets that belong to your Alibaba Cloud account.

        Args:
            request (ListVectorBucketsRequest): Request parameters for ListBuckets operation.

        Returns:
            ListVectorBucketsResult: Response result for ListVectorBuckets operation.
        """

        return vectors_operation.list_vector_buckets(self._client, request, **kwargs)

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
        return vectors_operation.put_bucket_policy(self._client, request, **kwargs)

    def get_bucket_policy(self, request: models.GetBucketPolicyRequest, **kwargs
                          ) -> models.GetBucketPolicyResult:
        """
        Queries the policies configured for a bucket.

        Args:
            request (GetBucketPolicyRequest): Request parameters for GetBucketPolicy operation.

        Returns:
            GetBucketPolicyResult: Response result for GetBucketPolicy operation.
        """
        return vectors_operation.get_bucket_policy(self._client, request, **kwargs)

    def delete_bucket_policy(self, request: models.DeleteBucketPolicyRequest, **kwargs
                             ) -> models.DeleteBucketPolicyResult:
        """
        Deletes a policy for a bucket.

        Args:
            request (DeleteBucketPolicyRequest): Request parameters for DeleteBucketPolicy operation.

        Returns:
            DeleteBucketPolicyResult: Response result for DeleteBucketPolicy operation.
        """
        return vectors_operation.delete_bucket_policy(self._client, request, **kwargs)


    # public access block
    def put_public_access_block(self, request: models.PutPublicAccessBlockRequest, **kwargs
                                ) -> models.PutPublicAccessBlockResult:
        """
        Enables or disables Block Public Access for Object Storage Service (OSS) resources.

        Args:
            request (PutPublicAccessBlockRequest): Request parameters for PutPublicAccessBlock operation.

        Returns:
            PutPublicAccessBlockResult: Response result for PutPublicAccessBlock operation.
        """
        return vectors_operation.put_public_access_block(self._client, request, **kwargs)


    def get_public_access_block(self, request: models.GetPublicAccessBlockRequest, **kwargs
                                ) -> models.GetPublicAccessBlockResult:
        """
        Queries the Block Public Access configurations of OSS resources.

        Args:
            request (GetPublicAccessBlockRequest): Request parameters for GetPublicAccessBlock operation.

        Returns:
            GetPublicAccessBlockResult: Response result for GetPublicAccessBlock operation.
        """
        return vectors_operation.get_public_access_block(self._client, request, **kwargs)

    def delete_public_access_block(self, request: models.DeletePublicAccessBlockRequest, **kwargs
                                   ) -> models.DeletePublicAccessBlockResult:
        """
        Deletes the Block Public Access configurations of OSS resources.

        Args:
            request (DeletePublicAccessBlockRequest): Request parameters for DeletePublicAccessBlock operation.

        Returns:
            DeletePublicAccessBlockResult: Response result for DeletePublicAccessBlock operation.
        """
        return vectors_operation.delete_public_access_block(self._client, request, **kwargs)

    # bucket tags
    def put_bucket_tags(self, request: vector_models.PutBucketTagsRequest, **kwargs
                        ) -> vector_models.PutBucketTagsResult:
        """
        Adds tags to or modifies the existing tags of a bucket.

        Args:
            request (PutBucketTagsRequest): Request parameters for PutBucketTags operation.

        Returns:
            PutBucketTagsResult: Response result for PutBucketTags operation.
        """
        return vectors_operation.put_bucket_tags(self._client, request, **kwargs)


    def get_bucket_tags(self, request: vector_models.GetBucketTagsRequest, **kwargs
                        ) -> vector_models.GetBucketTagsResult:
        """
        Queries the tags of a bucket.

        Args:
            request (GetBucketTagsRequest): Request parameters for GetBucketTags operation.

        Returns:
            GetBucketTagsResult: Response result for GetBucketTags operation.
        """
        return vectors_operation.get_bucket_tags(self._client, request, **kwargs)


    def delete_bucket_tags(self, request: vector_models.DeleteBucketTagsRequest, **kwargs
                           ) -> vector_models.DeleteBucketTagsResult:
        """
        Deletes tags configured for a bucket.

        Args:
            request (DeleteBucketTagsRequest): Request parameters for DeleteBucketTags operation.

        Returns:
            DeleteBucketTagsResult: Response result for DeleteBucketTags operation.
        """
        return vectors_operation.delete_bucket_tags(self._client, request, **kwargs)


    # bucket resource group
    def put_bucket_resource_group(self, request: models.PutBucketResourceGroupRequest, **kwargs
                                  ) -> models.PutBucketResourceGroupResult:
        """
        Modifies the ID of the resource group to which a bucket belongs.

        Args:
            request (PutBucketResourceGroupRequest): Request parameters for PutBucketResourceGroup operation.

        Returns:
            PutBucketResourceGroupResult: Response result for PutBucketResourceGroup operation.
        """
        return vectors_operation.put_bucket_resource_group(self._client, request, **kwargs)

    def get_bucket_resource_group(self, request: models.GetBucketResourceGroupRequest, **kwargs
                                  ) -> models.GetBucketResourceGroupResult:
        """
        Queries the ID of the resource group to which a bucket belongs.

        Args:
            request (GetBucketResourceGroupRequest): Request parameters for GetBucketResourceGroup operation.

        Returns:
            GetBucketResourceGroupResult: Response result for GetBucketResourceGroup operation.
        """
        return vectors_operation.get_bucket_resource_group(self._client, request, **kwargs)

    
    # vector index
    def put_vector_index(self, request: vector_models.PutVectorIndexRequest, **kwargs) -> vector_models.PutVectorIndexResult:
        """
        Create or update a vector index.

        Args:
            request (PutVectorIndexRequest): The request for the PutVectorIndex operation.

        Returns:
            PutVectorIndexResult: The result for the PutVectorIndex operation.
        """
        return vectors_operation.put_vector_index(client=self._client, request=request, **kwargs)

    def get_vector_index(self, request: vector_models.GetVectorIndexRequest, **kwargs) -> vector_models.GetVectorIndexResult:
        """
        Get information about a specific vector index.

        Args:
            request (GetVectorIndexRequest): The request for the GetVectorIndex operation.

        Returns:
            GetVectorIndexResult: The result for the GetVectorIndex operation.
        """
        return vectors_operation.get_vector_index(client=self._client, request=request, **kwargs)

    def list_vector_index(self, request: vector_models.ListVectorsIndexRequest, **kwargs) -> vector_models.ListVectorsIndexResult:
        """
        List vector indexes in a bucket.

        Args:
            request (ListVectorsIndexRequest): The request for the ListVectorIndex operation.

        Returns:
            ListVectorsIndexResult: The result for the ListVectorIndex operation.
        """
        return vectors_operation.list_vector_index(client=self._client, request=request, **kwargs)

    def delete_vector_index(self, request: vector_models.DeleteVectorIndexRequest, **kwargs) -> vector_models.DeleteVectorIndexResult:
        """
        Delete a vector index.

        Args:
            request (DeleteVectorIndexRequest): The request for the DeleteVectorIndex operation.

        Returns:
            DeleteVectorIndexResult: The result for the DeleteVectorIndex operation.
        """
        return vectors_operation.delete_vector_index(client=self._client, request=request, **kwargs)

    # vector basic
    def put_vectors(self, request: vector_models.PutVectorsRequest, **kwargs) -> vector_models.PutVectorsResult:
        """
        Put vectors into an index.

        Args:
            request (PutVectorsRequest): The request for the PutVectors operation.

        Returns:
            PutVectorsResult: The result for the PutVectors operation.
        """
        return vectors_operation.put_vectors(client=self._client, request=request, **kwargs)

    def get_vectors(self, request: vector_models.GetVectorsRequest, **kwargs) -> vector_models.GetVectorsResult:
        """
        Get vectors from an index.

        Args:
            request (GetVectorsRequest): The request for the GetVectors operation.

        Returns:
            GetVectorsResult: The result for the GetVectors operation.
        """
        return vectors_operation.get_vectors(client=self._client, request=request, **kwargs)

    def list_vectors(self, request: vector_models.ListVectorsRequest, **kwargs) -> vector_models.ListVectorsResult:
        """
        List vectors in an index.

        Args:
            request (ListVectorsRequest): The request for the ListVectors operation.

        Returns:
            ListVectorsResult: The result for the ListVectors operation.
        """
        return vectors_operation.list_vectors(client=self._client, request=request, **kwargs)

    def delete_vectors(self, request: vector_models.DeleteVectorsRequest, **kwargs) -> vector_models.DeleteVectorsResult:
        """
        Delete vectors from an index.

        Args:
            request (DeleteVectorsRequest): The request for the DeleteVectors operation.

        Returns:
            DeleteVectorsResult: The result for the DeleteVectors operation.
        """
        return vectors_operation.delete_vectors(client=self._client, request=request, **kwargs)

    def query_vectors(self, request: vector_models.QueryVectorsRequest, **kwargs) -> vector_models.QueryVectorsResult:
        """
        Query vectors in an index.

        Args:
            request (QueryVectorsRequest): The request for the QueryVectors operation.

        Returns:
            QueryVectorsResult: The result for the QueryVectors operation.
        """
        return vectors_operation.query_vectors(client=self._client, request=request, **kwargs)
