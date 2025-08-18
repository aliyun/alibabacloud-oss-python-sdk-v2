# pylint: disable=line-too-long
"""Client used to interact with **Alibaba Cloud Object Storage Service (OSS)**."""
import copy
from typing import Optional
from .config import Config
from .types import OperationInput, OperationOutput
from ._client import _SyncClientImpl, _SyncVectorClientImpl
from .defaults import FF_ENABLE_CRC64_CHECK_DOWNLOAD
from . import models
from . import operations


class VectorClient:
    """Client
    """

    def __init__(self, config: Config, **kwargs) -> None:
        """Initialize Vector Client

        Args:
            config (Config): _description_
        """
        self._client = _SyncVectorClientImpl(config, **kwargs)

    def __repr__(self) -> str:
        return "<OssVectorClient>"

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
    def put_vector_bucket(self, request: models.PutBucketRequest, **kwargs
                   ) -> models.PutBucketResult:
        """
        Creates a bucket.

        Args:
            request (PutBucketRequest): Request parameters for PutBucket operation.

        Returns:
            PutBucketResult: Response result for PutBucket operation.
        """

        return operations.put_vector_bucket(self._client, request, **kwargs)

    def get_vector_bucket(self, request: models.GetBucketInfoRequest, **kwargs
                        ) -> models.GetBucketInfoResult:
        """
        GetBucketInfo Queries information about a bucket.

        Args:
            request (GetBucketInfoRequest): Request parameters for GetBucketInfo operation.

        Returns:
            GetBucketInfoResult: Response result for GetBucketInfo operation.
        """

        return operations.get_vector_bucket(self._client, request, **kwargs)

    def delete_vector_bucket(self, request: models.DeleteBucketRequest, **kwargs
                      ) -> models.DeleteBucketResult:
        """
        Deletes a bucket.

        Args:
            request (DeleteBucketRequest): Request parameters for DeleteBucket operation.

        Returns:
            DeleteBucketResult: Response result for DeleteBucket operation.
        """

        return operations.delete_vector_bucket(self._client, request, **kwargs)

    def list_vector_buckets(self, request: models.ListBucketsRequest, **kwargs
                     ) -> models.ListBucketsResult:
        """
        Lists all buckets that belong to your Alibaba Cloud account.

        Args:
            request (ListBucketsRequest): Request parameters for ListBuckets operation.

        Returns:
            ListBucketsResult: Response result for ListBuckets operation.
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
        return operations.put_bucket_policy_vector(self._client, request, **kwargs)

    def get_bucket_policy(self, request: models.GetBucketPolicyRequest, **kwargs
                          ) -> models.GetBucketPolicyResult:
        """
        Queries the policies configured for a bucket.

        Args:
            request (GetBucketPolicyRequest): Request parameters for GetBucketPolicy operation.

        Returns:
            GetBucketPolicyResult: Response result for GetBucketPolicy operation.
        """
        return operations.get_bucket_policy_vector(self._client, request, **kwargs)

    def delete_bucket_policy(self, request: models.DeleteBucketPolicyRequest, **kwargs
                             ) -> models.DeleteBucketPolicyResult:
        """
        Deletes a policy for a bucket.

        Args:
            request (DeleteBucketPolicyRequest): Request parameters for DeleteBucketPolicy operation.

        Returns:
            DeleteBucketPolicyResult: Response result for DeleteBucketPolicy operation.
        """
        return operations.delete_bucket_policy_vector(self._client, request, **kwargs)


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
        return operations.put_public_access_block_vector(self._client, request, **kwargs)


    def get_public_access_block(self, request: models.GetPublicAccessBlockRequest, **kwargs
                                ) -> models.GetPublicAccessBlockResult:
        """
        Queries the Block Public Access configurations of OSS resources.

        Args:
            request (GetPublicAccessBlockRequest): Request parameters for GetPublicAccessBlock operation.

        Returns:
            GetPublicAccessBlockResult: Response result for GetPublicAccessBlock operation.
        """
        return operations.get_public_access_block_vector(self._client, request, **kwargs)

    def delete_public_access_block(self, request: models.DeletePublicAccessBlockRequest, **kwargs
                                   ) -> models.DeletePublicAccessBlockResult:
        """
        Deletes the Block Public Access configurations of OSS resources.

        Args:
            request (DeletePublicAccessBlockRequest): Request parameters for DeletePublicAccessBlock operation.

        Returns:
            DeletePublicAccessBlockResult: Response result for DeletePublicAccessBlock operation.
        """
        return operations.delete_public_access_block_vector(self._client, request, **kwargs)

    # bucket tags
    def put_bucket_tags(self, request: models.PutBucketTagsRequest, **kwargs
                        ) -> models.PutBucketTagsResult:
        """
        Adds tags to or modifies the existing tags of a bucket.

        Args:
            request (PutBucketTagsRequest): Request parameters for PutBucketTags operation.

        Returns:
            PutBucketTagsResult: Response result for PutBucketTags operation.
        """
        return operations.put_bucket_tags_vector(self._client, request, **kwargs)


    def get_bucket_tags(self, request: models.GetBucketTagsRequest, **kwargs
                        ) -> models.GetBucketTagsResult:
        """
        Queries the tags of a bucket.

        Args:
            request (GetBucketTagsRequest): Request parameters for GetBucketTags operation.

        Returns:
            GetBucketTagsResult: Response result for GetBucketTags operation.
        """
        return operations.get_bucket_tags_vector(self._client, request, **kwargs)


    def delete_bucket_tags(self, request: models.DeleteBucketTagsRequest, **kwargs
                           ) -> models.DeleteBucketTagsResult:
        """
        Deletes tags configured for a bucket.

        Args:
            request (DeleteBucketTagsRequest): Request parameters for DeleteBucketTags operation.

        Returns:
            DeleteBucketTagsResult: Response result for DeleteBucketTags operation.
        """
        return operations.delete_bucket_tags_vector(self._client, request, **kwargs)


    # bucket resource group
    def get_bucket_resource_group(self, request: models.GetBucketResourceGroupRequest, **kwargs
                                  ) -> models.GetBucketResourceGroupResult:
        """
        Queries the ID of the resource group to which a bucket belongs.

        Args:
            request (GetBucketResourceGroupRequest): Request parameters for GetBucketResourceGroup operation.

        Returns:
            GetBucketResourceGroupResult: Response result for GetBucketResourceGroup operation.
        """
        return operations.get_bucket_resource_group_vector(self._client, request, **kwargs)


    def put_bucket_resource_group(self, request: models.PutBucketResourceGroupRequest, **kwargs
                                  ) -> models.PutBucketResourceGroupResult:
        """
        Modifies the ID of the resource group to which a bucket belongs.

        Args:
            request (PutBucketResourceGroupRequest): Request parameters for PutBucketResourceGroup operation.

        Returns:
            PutBucketResourceGroupResult: Response result for PutBucketResourceGroup operation.
        """
        return operations.put_bucket_resource_group_vector(self._client, request, **kwargs)