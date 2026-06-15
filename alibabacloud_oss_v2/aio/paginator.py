"""Async Paginator for list operations."""
import abc
import copy
from typing import AsyncIterator, Any
from .. import models


class AsyncListObjectsAPIClient(abc.ABC):
    """Abstract base class for async list_objects client."""

    @abc.abstractmethod
    async def list_objects(self, request: models.ListObjectsRequest, **kwargs) -> models.ListObjectsResult:
        """Lists information about all objects in an Object Storage Service (OSS) bucket."""


class AsyncListObjectsPaginator:
    """An async paginator for ListObjects"""

    def __init__(
        self,
        client: AsyncListObjectsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (AsyncListObjectsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    async def iter_page(self, request: models.ListObjectsRequest, **kwargs: Any) -> AsyncIterator[models.ListObjectsResult]:
        """Iterates over the objects.

        Args:
            request (models.ListObjectsRequest): The request for the ListObjects operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            AsyncIterator[models.ListObjectsResult]: An async iterator of ListObjectsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = await self._client.list_objects(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.marker = result.next_marker

    def __repr__(self) -> str:
        return "<AsyncListObjectsPaginator>"


class AsyncListObjectsV2APIClient(abc.ABC):
    """Abstract base class for async list_objects_v2 client."""

    @abc.abstractmethod
    async def list_objects_v2(self, request: models.ListObjectsV2Request, **kwargs) -> models.ListObjectsV2Result:
        """Lists information about all objects in an Object Storage Service (OSS) bucket."""


class AsyncListObjectsV2Paginator:
    """An async paginator for ListObjectsV2"""

    def __init__(
        self,
        client: AsyncListObjectsV2APIClient,
        **kwargs: Any
    ) -> None:
        """
            client (AsyncListObjectsV2APIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    async def iter_page(self, request: models.ListObjectsV2Request, **kwargs: Any) -> AsyncIterator[models.ListObjectsV2Result]:
        """Iterates over the objects with v2.

        Args:
            request (models.ListObjectsV2Request): The request for the ListObjectsV2 operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            AsyncIterator[models.ListObjectsV2Result]: An async iterator of ListObjectsV2Result from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = await self._client.list_objects_v2(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.continuation_token = result.next_continuation_token

    def __repr__(self) -> str:
        return "<AsyncListObjectsV2Paginator>"


class AsyncListObjectVersionsAPIClient(abc.ABC):
    """Abstract base class for async list_object_versions client."""

    @abc.abstractmethod
    async def list_object_versions(self, request: models.ListObjectVersionsRequest, **kwargs) -> models.ListObjectVersionsResult:
        """Lists the versions of all objects in a bucket, including delete markers."""


class AsyncListObjectVersionsPaginator:
    """An async paginator for ListObjectVersions"""

    def __init__(
        self,
        client: AsyncListObjectVersionsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (AsyncListObjectVersionsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    async def iter_page(self, request: models.ListObjectVersionsRequest, **kwargs: Any) -> AsyncIterator[models.ListObjectVersionsResult]:
        """Iterates over the object versions.

        Args:
            request (models.ListObjectVersionsRequest): The request for the ListObjectVersions operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            AsyncIterator[models.ListObjectVersionsResult]: An async iterator of ListObjectVersionsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = await self._client.list_object_versions(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.key_marker = result.next_key_marker
            req.version_id_marker = result.next_version_id_marker

    def __repr__(self) -> str:
        return "<AsyncListObjectVersionsPaginator>"


class AsyncListBucketsAPIClient(abc.ABC):
    """Abstract base class for async list_buckets client."""

    @abc.abstractmethod
    async def list_buckets(self, request: models.ListBucketsRequest, **kwargs) -> models.ListBucketsResult:
        """Lists all buckets that belong to your Alibaba Cloud account."""


class AsyncListBucketsPaginator:
    """An async paginator for ListBuckets"""

    def __init__(
        self,
        client: AsyncListBucketsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (AsyncListBucketsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    async def iter_page(self, request: models.ListBucketsRequest, **kwargs: Any) -> AsyncIterator[models.ListBucketsResult]:
        """Iterates over the buckets.

        Args:
            request (models.ListBucketsRequest): The request for the ListBuckets operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            AsyncIterator[models.ListBucketsResult]: An async iterator of ListBucketsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = await self._client.list_buckets(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.marker = result.next_marker

    def __repr__(self) -> str:
        return "<AsyncListBucketsPaginator>"


class AsyncListPartsAPIClient(abc.ABC):
    """Abstract base class for async list_parts client."""

    @abc.abstractmethod
    async def list_parts(self, request: models.ListPartsRequest, **kwargs) -> models.ListPartsResult:
        """Lists all parts that are uploaded by using a specified upload ID."""


class AsyncListPartsPaginator:
    """An async paginator for ListParts"""

    def __init__(
        self,
        client: AsyncListPartsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (AsyncListPartsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    async def iter_page(self, request: models.ListPartsRequest, **kwargs: Any) -> AsyncIterator[models.ListPartsResult]:
        """Iterates over the parts.

        Args:
            request (models.ListPartsRequest): The request for the ListParts operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            AsyncIterator[models.ListPartsResult]: An async iterator of ListPartsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_parts = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = await self._client.list_parts(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.part_number_marker = result.next_part_number_marker

    def __repr__(self) -> str:
        return "<AsyncListPartsPaginator>"


class AsyncListMultipartUploadsAPIClient(abc.ABC):
    """Abstract base class for async list_multipart_uploads client."""

    @abc.abstractmethod
    async def list_multipart_uploads(self, request: models.ListMultipartUploadsRequest, **kwargs) -> models.ListMultipartUploadsResult:
        """Lists all multipart upload tasks in progress. The tasks are not completed or canceled."""


class AsyncListMultipartUploadsPaginator:
    """An async paginator for ListMultipartUploads"""

    def __init__(
        self,
        client: AsyncListMultipartUploadsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (AsyncListMultipartUploadsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    async def iter_page(self, request: models.ListMultipartUploadsRequest, **kwargs: Any) -> AsyncIterator[models.ListMultipartUploadsResult]:
        """Iterates over the objects.

        Args:
            request (models.ListMultipartUploadsRequest): The request for the ListMultipartUploads operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            AsyncIterator[models.ListMultipartUploadsResult]: An async iterator of ListMultipartUploadsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_uploads = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = await self._client.list_multipart_uploads(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.key_marker = result.next_key_marker
            req.upload_id_marker = result.next_upload_id_marker

    def __repr__(self) -> str:
        return "<AsyncListMultipartUploadsPaginator>"
