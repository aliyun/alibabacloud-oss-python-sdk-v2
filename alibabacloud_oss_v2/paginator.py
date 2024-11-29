"""Paginator for list operation."""
import abc
import copy
from typing import Iterator, Any
from . import models


class ListObjectsAPIClient(abc.ABC):
    """Abstract base class for list_objects client."""

    @abc.abstractmethod
    def list_objects(self, request: models.ListObjectsRequest, **kwargs) -> models.ListObjectsResult:
        """Lists information about all objects in an Object Storage Service (OSS) bucket."""


class ListObjectsPaginator:
    """A paginator for ListObjects"""

    def __init__(
        self,
        client: ListObjectsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (ListObjectsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListObjectsRequest, **kwargs: Any) -> Iterator[models.ListObjectsResult]:
        """Iterates over the objects.

        Args:
            request (models.ListObjectsRequest): The request for the ListObjects operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListObjectsResult]: An iterator of ListObjectsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_objects(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.marker = result.next_marker

    def __repr__(self) -> str:
        return "<ListObjectsPaginator>"


class ListObjectsV2APIClient(abc.ABC):
    """Abstract base class for list_objects_v2 client."""

    @abc.abstractmethod
    def list_objects_v2(self, request: models.ListObjectsV2Request, **kwargs) -> models.ListObjectsV2Result:
        """Lists information about all objects in an Object Storage Service (OSS) bucket."""


class ListObjectsV2Paginator:
    """A paginator for ListObjectsV2"""

    def __init__(
        self,
        client: ListObjectsV2APIClient,
        **kwargs: Any
    ) -> None:
        """
            client (ListObjectsV2APIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListObjectsV2Request, **kwargs: Any) -> Iterator[models.ListObjectsV2Result]:
        """Iterates over the objects with v2.

        Args:
            request (models.ListObjectsV2Request): The request for the ListObjectsV2 operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListObjectsV2Result]: An iterator of ListObjectsV2Result from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_objects_v2(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.continuation_token = result.next_continuation_token

    def __repr__(self) -> str:
        return "<ListObjectsV2Paginator>"

class ListObjectVersionsAPIClient(abc.ABC):
    """Abstract base class for list_object_versions client."""

    @abc.abstractmethod
    def list_object_versions(self, request: models.ListObjectVersionsRequest, **kwargs) -> models.ListObjectVersionsResult:
        """Lists the versions of all objects in a bucket, including delete markers."""


class ListObjectVersionsPaginator:
    """A paginator for ListObjectVersions"""

    def __init__(
        self,
        client: ListObjectVersionsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (ListObjectVersionsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListObjectVersionsRequest, **kwargs: Any) -> Iterator[models.ListObjectVersionsResult]:
        """Iterates over the object versions.

        Args:
            request (models.ListObjectVersionsRequest): The request for the ListObjectVersions operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListObjectVersionsResult]: An iterator of ListObjectVersionsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_object_versions(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.key_marker = result.next_key_marker
            req.version_id_marker = result.next_version_id_marker

    def __repr__(self) -> str:
        return "<ListObjectVersionsPaginator>"

class ListBucketsAPIClient(abc.ABC):
    """Abstract base class for list_buckets client."""

    @abc.abstractmethod
    def list_buckets(self, request: models.ListBucketsRequest, **kwargs) -> models.ListBucketsResult:
        """Lists all buckets that belong to your Alibaba Cloud account."""


class ListBucketsPaginator:
    """A paginator for ListBuckets"""

    def __init__(
        self,
        client: ListBucketsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (ListBucketsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListBucketsRequest, **kwargs: Any) -> Iterator[models.ListBucketsResult]:
        """Iterates over the buckets.

        Args:
            request (models.ListBucketsRequest): The request for the ListBuckets operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListBucketsResult]: An iterator of ListBucketsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_buckets(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.marker = result.next_marker

    def __repr__(self) -> str:
        return "<ListBucketsPaginator>"


class ListPartsAPIClient(abc.ABC):
    """Abstract base class for list_parts client."""

    @abc.abstractmethod
    def list_parts(self, request: models.ListPartsRequest, **kwargs) -> models.ListPartsResult:
        """Lists all parts that are uploaded by using a specified upload ID."""

class ListPartsPaginator:
    """A paginator for ListParts"""

    def __init__(
        self,
        client: ListPartsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (_SyncClientImpl): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListPartsRequest, **kwargs: Any) -> Iterator[models.ListPartsResult]:
        """Iterates over the parts.

        Args:
            request (models.ListPartsRequest): The request for the ListParts operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListPartsResult]: An iterator of ListPartsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_parts = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_parts(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.part_number_marker = result.next_part_number_marker

    def __repr__(self) -> str:
        return "<ListPartsPaginator>"

class ListMultipartUploadsAPIClient(abc.ABC):
    """Abstract base class for list_multipart_uploads client."""

    @abc.abstractmethod
    def list_multipart_uploads(self, request: models.ListMultipartUploadsRequest, **kwargs) -> models.ListMultipartUploadsResult:
        """Lists all multipart upload tasks in progress. The tasks are not completed or canceled."""


class ListMultipartUploadsPaginator:
    """A paginator for ListMultipartUploads"""

    def __init__(
        self,
        client: ListMultipartUploadsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (ListMultipartUploadsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListMultipartUploadsRequest, **kwargs: Any) -> Iterator[models.ListMultipartUploadsResult]:
        """Iterates over the objects.

        Args:
            request (models.ListMultipartUploadsRequest): The request for the ListMultipartUploads operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListMultipartUploadsResult]: An iterator of ListMultipartUploadsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_uploads = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_multipart_uploads(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.key_marker = result.next_key_marker
            req.upload_id_marker = result.next_upload_id_marker

    def __repr__(self) -> str:
        return "<ListMultipartUploadsPaginator>"