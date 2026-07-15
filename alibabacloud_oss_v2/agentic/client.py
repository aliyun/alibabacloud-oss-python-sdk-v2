# pylint: disable=line-too-long
"""AgenticBucket / BucketSpace client."""
import copy
from alibabacloud_oss_v2._client import _SyncClientImpl
from alibabacloud_oss_v2.config import Config
from alibabacloud_oss_v2.types import OperationInput, OperationOutput
from alibabacloud_oss_v2.client import Client
from alibabacloud_oss_v2 import utils as base_utils

from . import models
from . import operations
from . import utils
from .paginator import ListAgenticBucketsPaginator, ListBucketSpacesPaginator


class AgenticBucketClient:
    """Client for the AgenticBucket management APIs.

    Bucket name resolution:
        The ``bucket`` field of every request is a *prefix*, not the full bucket
        name. Internally it is resolved to::

            {prefix}-{account_id}-{region}-ab-apsr

        so ``config.account_id`` and ``config.region`` are required. APIs that
        carry no bucket (e.g. ``list_agentic_buckets``) are routed to the
        region-level host instead of a bucket-level host.

    Endpoint modes (resolved by the base Config):
        - ``config.endpoint`` set: used as-is (custom domain / CNAME).
        - otherwise derived from ``config.region``:
            - public:   oss-{region}.aliyuncs.com (default)
            - internal: oss-{region}-internal.aliyuncs.com
              (set ``config.use_internal_endpoint=True``)
    """

    def __init__(self, config: Config, **kwargs) -> None:
        _config = copy.copy(config)
        _config.user_agent = self._build_agentic_user_agent(_config)

        self._client = _SyncClientImpl(_config, **kwargs)

        account_id = config.account_id or ""
        region = config.region or ""

        provider = utils.AgenticProvider(
            endpoint=self._client._options.endpoint,
            account_id=account_id,
            region=region,
            suffix="ab-apsr",
        )
        self._client._options.endpoint_provider = provider
        self._client._options.bucket_name_resolver = provider

    def __repr__(self) -> str:
        return "<OssAgenticBucketClient>"

    def _build_agentic_user_agent(self, config: Config) -> str:
        if config.user_agent:
            return f'{base_utils.get_agentic_user_agent()}/{config.user_agent}'

        return base_utils.get_agentic_user_agent()

    def invoke_operation(self, op_input: OperationInput, **kwargs) -> OperationOutput:
        return self._client.invoke_operation(op_input, **kwargs)

    # --- base APIs ---
    def create_agentic_bucket(self, request: models.CreateAgenticBucketRequest, **kwargs
                              ) -> models.CreateAgenticBucketResult:
        """
        Creates an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (CreateAgenticBucketRequest): Request parameters for CreateAgenticBucket operation.

        Returns:
            CreateAgenticBucketResult: Response result for CreateAgenticBucket operation.
        """

        return operations.create_agentic_bucket(self._client, request, **kwargs)

    def delete_agentic_bucket(self, request: models.DeleteAgenticBucketRequest, **kwargs
                              ) -> models.DeleteAgenticBucketResult:
        """
        Deletes an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (DeleteAgenticBucketRequest): Request parameters for DeleteAgenticBucket operation.

        Returns:
            DeleteAgenticBucketResult: Response result for DeleteAgenticBucket operation.
        """

        return operations.delete_agentic_bucket(self._client, request, **kwargs)

    def get_agentic_bucket(self, request: models.GetAgenticBucketRequest, **kwargs
                           ) -> models.GetAgenticBucketResult:
        """
        Queries information about an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (GetAgenticBucketRequest): Request parameters for GetAgenticBucket operation.

        Returns:
            GetAgenticBucketResult: Response result for GetAgenticBucket operation.
        """

        return operations.get_agentic_bucket(self._client, request, **kwargs)

    def list_agentic_buckets(self, request: models.ListAgenticBucketsRequest, **kwargs
                             ) -> models.ListAgenticBucketsResult:
        """
        Lists AgenticBuckets. Carries no bucket, so it is routed to the region-level host.

        Args:
            request (ListAgenticBucketsRequest): Request parameters for ListAgenticBuckets operation.

        Returns:
            ListAgenticBucketsResult: Response result for ListAgenticBuckets operation.
        """

        return operations.list_agentic_buckets(self._client, request, **kwargs)

    def put_agentic_bucket_status(self, request: models.PutAgenticBucketStatusRequest, **kwargs
                                  ) -> models.PutAgenticBucketStatusResult:
        """
        Configures the status of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (PutAgenticBucketStatusRequest): Request parameters for PutAgenticBucketStatus operation.

        Returns:
            PutAgenticBucketStatusResult: Response result for PutAgenticBucketStatus operation.
        """

        return operations.put_agentic_bucket_status(self._client, request, **kwargs)

    def list_bucket_spaces(self, request: models.ListBucketSpacesRequest, **kwargs
                           ) -> models.ListBucketSpacesResult:
        """
        Lists BucketSpaces under an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (ListBucketSpacesRequest): Request parameters for ListBucketSpaces operation.

        Returns:
            ListBucketSpacesResult: Response result for ListBucketSpaces operation.
        """

        return operations.list_bucket_spaces(self._client, request, **kwargs)

    # --- acl ---
    def put_agentic_bucket_acl(self, request: models.PutAgenticBucketAclRequest, **kwargs
                               ) -> models.PutAgenticBucketAclResult:
        """
        Configures the ACL of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (PutAgenticBucketAclRequest): Request parameters for PutAgenticBucketAcl operation.

        Returns:
            PutAgenticBucketAclResult: Response result for PutAgenticBucketAcl operation.
        """

        return operations.put_agentic_bucket_acl(self._client, request, **kwargs)

    def get_agentic_bucket_acl(self, request: models.GetAgenticBucketAclRequest, **kwargs
                               ) -> models.GetAgenticBucketAclResult:
        """
        Queries the ACL of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (GetAgenticBucketAclRequest): Request parameters for GetAgenticBucketAcl operation.

        Returns:
            GetAgenticBucketAclResult: Response result for GetAgenticBucketAcl operation.
        """

        return operations.get_agentic_bucket_acl(self._client, request, **kwargs)

    # --- encryption ---
    def put_agentic_bucket_encryption(self, request: models.PutAgenticBucketEncryptionRequest, **kwargs
                                      ) -> models.PutAgenticBucketEncryptionResult:
        """
        Configures the encryption rule of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (PutAgenticBucketEncryptionRequest): Request parameters for PutAgenticBucketEncryption operation.

        Returns:
            PutAgenticBucketEncryptionResult: Response result for PutAgenticBucketEncryption operation.
        """

        return operations.put_agentic_bucket_encryption(self._client, request, **kwargs)

    def get_agentic_bucket_encryption(self, request: models.GetAgenticBucketEncryptionRequest, **kwargs
                                      ) -> models.GetAgenticBucketEncryptionResult:
        """
        Queries the encryption rule of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (GetAgenticBucketEncryptionRequest): Request parameters for GetAgenticBucketEncryption operation.

        Returns:
            GetAgenticBucketEncryptionResult: Response result for GetAgenticBucketEncryption operation.
        """

        return operations.get_agentic_bucket_encryption(self._client, request, **kwargs)

    def delete_agentic_bucket_encryption(self, request: models.DeleteAgenticBucketEncryptionRequest, **kwargs
                                         ) -> models.DeleteAgenticBucketEncryptionResult:
        """
        Deletes the encryption rule of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (DeleteAgenticBucketEncryptionRequest): Request parameters for DeleteAgenticBucketEncryption operation.

        Returns:
            DeleteAgenticBucketEncryptionResult: Response result for DeleteAgenticBucketEncryption operation.
        """

        return operations.delete_agentic_bucket_encryption(self._client, request, **kwargs)

    # --- versioning ---
    def put_agentic_bucket_versioning(self, request: models.PutAgenticBucketVersioningRequest, **kwargs
                                      ) -> models.PutAgenticBucketVersioningResult:
        """
        Configures the versioning state of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (PutAgenticBucketVersioningRequest): Request parameters for PutAgenticBucketVersioning operation.

        Returns:
            PutAgenticBucketVersioningResult: Response result for PutAgenticBucketVersioning operation.
        """

        return operations.put_agentic_bucket_versioning(self._client, request, **kwargs)

    def get_agentic_bucket_versioning(self, request: models.GetAgenticBucketVersioningRequest, **kwargs
                                      ) -> models.GetAgenticBucketVersioningResult:
        """
        Queries the versioning state of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (GetAgenticBucketVersioningRequest): Request parameters for GetAgenticBucketVersioning operation.

        Returns:
            GetAgenticBucketVersioningResult: Response result for GetAgenticBucketVersioning operation.
        """

        return operations.get_agentic_bucket_versioning(self._client, request, **kwargs)

    # --- policy ---
    def put_agentic_bucket_policy(self, request: models.PutAgenticBucketPolicyRequest, **kwargs
                                  ) -> models.PutAgenticBucketPolicyResult:
        """
        Configures the policy of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (PutAgenticBucketPolicyRequest): Request parameters for PutAgenticBucketPolicy operation.

        Returns:
            PutAgenticBucketPolicyResult: Response result for PutAgenticBucketPolicy operation.
        """

        return operations.put_agentic_bucket_policy(self._client, request, **kwargs)

    def get_agentic_bucket_policy(self, request: models.GetAgenticBucketPolicyRequest, **kwargs
                                  ) -> models.GetAgenticBucketPolicyResult:
        """
        Queries the policy of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (GetAgenticBucketPolicyRequest): Request parameters for GetAgenticBucketPolicy operation.

        Returns:
            GetAgenticBucketPolicyResult: Response result for GetAgenticBucketPolicy operation.
        """

        return operations.get_agentic_bucket_policy(self._client, request, **kwargs)

    def delete_agentic_bucket_policy(self, request: models.DeleteAgenticBucketPolicyRequest, **kwargs
                                     ) -> models.DeleteAgenticBucketPolicyResult:
        """
        Deletes the policy of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (DeleteAgenticBucketPolicyRequest): Request parameters for DeleteAgenticBucketPolicy operation.

        Returns:
            DeleteAgenticBucketPolicyResult: Response result for DeleteAgenticBucketPolicy operation.
        """

        return operations.delete_agentic_bucket_policy(self._client, request, **kwargs)

    # --- public access block ---
    def put_agentic_bucket_public_access_block(self, request: models.PutAgenticBucketPublicAccessBlockRequest, **kwargs
                                               ) -> models.PutAgenticBucketPublicAccessBlockResult:
        """
        Configures the public access block of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (PutAgenticBucketPublicAccessBlockRequest): Request parameters for PutAgenticBucketPublicAccessBlock operation.

        Returns:
            PutAgenticBucketPublicAccessBlockResult: Response result for PutAgenticBucketPublicAccessBlock operation.
        """

        return operations.put_agentic_bucket_public_access_block(self._client, request, **kwargs)

    def get_agentic_bucket_public_access_block(self, request: models.GetAgenticBucketPublicAccessBlockRequest, **kwargs
                                               ) -> models.GetAgenticBucketPublicAccessBlockResult:
        """
        Queries the public access block of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (GetAgenticBucketPublicAccessBlockRequest): Request parameters for GetAgenticBucketPublicAccessBlock operation.

        Returns:
            GetAgenticBucketPublicAccessBlockResult: Response result for GetAgenticBucketPublicAccessBlock operation.
        """

        return operations.get_agentic_bucket_public_access_block(self._client, request, **kwargs)

    def delete_agentic_bucket_public_access_block(self, request: models.DeleteAgenticBucketPublicAccessBlockRequest, **kwargs
                                                  ) -> models.DeleteAgenticBucketPublicAccessBlockResult:
        """
        Deletes the public access block of an AgenticBucket. ``request.bucket`` is the prefix.

        Args:
            request (DeleteAgenticBucketPublicAccessBlockRequest): Request parameters for DeleteAgenticBucketPublicAccessBlock operation.

        Returns:
            DeleteAgenticBucketPublicAccessBlockResult: Response result for DeleteAgenticBucketPublicAccessBlock operation.
        """

        return operations.delete_agentic_bucket_public_access_block(self._client, request, **kwargs)

    # --- paginators ---
    def list_agentic_buckets_paginator(self, **kwargs) -> ListAgenticBucketsPaginator:
        """
        Returns a paginator that iterates over ListAgenticBuckets results.

        Returns:
            ListAgenticBucketsPaginator: A paginator for the ListAgenticBuckets operation.
        """

        return ListAgenticBucketsPaginator(self, **kwargs)

    def list_bucket_spaces_paginator(self, **kwargs) -> ListBucketSpacesPaginator:
        """
        Returns a paginator that iterates over ListBucketSpaces results.

        Returns:
            ListBucketSpacesPaginator: A paginator for the ListBucketSpaces operation.
        """

        return ListBucketSpacesPaginator(self, **kwargs)


class BucketSpaceClient:
    """Factory for a standard OSS Client wired for BucketSpace-level Bucket/Object APIs."""

    @staticmethod
    def create(config: Config, **kwargs) -> Client:
        """Create a standard OSS Client for BucketSpace-level Bucket/Object APIs.

        Bucket name resolution:
            The ``bucket`` passed to any Bucket/Object API is a *prefix* and is
            resolved to::

                {prefix}-{account_id}-{region}-bs-apsr

            so ``config.account_id`` and ``config.region`` are required. Only
            bucket-scoped APIs are supported (service-level APIs like
            ``list_buckets`` have no bucket to resolve).

        Endpoint modes (BucketSpace is typically reached via one of):
            - custom domain / CNAME: set ``config.endpoint``, used as-is.
            - internal endpoint: set ``config.use_internal_endpoint=True``,
              which derives oss-{region}-internal.aliyuncs.com from
              ``config.region``.
        """
        _config = copy.copy(config)
        _config.user_agent = BucketSpaceClient._build_user_agent(_config)

        client = Client(_config, **kwargs)

        account_id = config.account_id or ""
        region = config.region or ""

        provider = utils.AgenticProvider(
            endpoint=client._client._options.endpoint,
            account_id=account_id,
            region=region,
            suffix="bs-apsr",
        )
        client._client._options.endpoint_provider = provider
        client._client._options.bucket_name_resolver = provider

        return client

    @staticmethod
    def _build_user_agent(config: Config) -> str:
        if config.user_agent:
            return f'{base_utils.get_bucket_space_user_agent()}/{config.user_agent}'

        return base_utils.get_bucket_space_user_agent()
