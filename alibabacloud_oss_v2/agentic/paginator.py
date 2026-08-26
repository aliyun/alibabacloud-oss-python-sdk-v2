"""Paginator for AgenticBucket list operations."""
import abc
import copy
from typing import Iterator, Any
from . import models


class ListAgenticBucketsAPIClient(abc.ABC):
    """Abstract base class for list_agentic_buckets client."""

    @abc.abstractmethod
    def list_agentic_buckets(self, request: models.ListAgenticBucketsRequest, **kwargs) -> models.ListAgenticBucketsResult:
        """Lists all AgenticBuckets that belong to your Alibaba Cloud account."""


class ListAgenticBucketsPaginator:
    """A paginator for ListAgenticBuckets"""

    def __init__(
        self,
        client: ListAgenticBucketsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (ListAgenticBucketsAPIClient): An agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListAgenticBucketsRequest, **kwargs: Any) -> Iterator[models.ListAgenticBucketsResult]:
        """Iterates over the AgenticBuckets.

        Args:
            request (models.ListAgenticBucketsRequest): The request for the ListAgenticBuckets operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListAgenticBucketsResult]: An iterator of ListAgenticBucketsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_agentic_buckets(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.continuation_token = result.next_continuation_token

    def __repr__(self) -> str:
        return "<ListAgenticBucketsPaginator>"


class ListBucketSpacesAPIClient(abc.ABC):
    """Abstract base class for list_bucket_spaces client."""

    @abc.abstractmethod
    def list_bucket_spaces(self, request: models.ListBucketSpacesRequest, **kwargs) -> models.ListBucketSpacesResult:
        """Lists all BucketSpaces under an AgenticBucket."""


class ListBucketSpacesPaginator:
    """A paginator for ListBucketSpaces"""

    def __init__(
        self,
        client: ListBucketSpacesAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (ListBucketSpacesAPIClient): An agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListBucketSpacesRequest, **kwargs: Any) -> Iterator[models.ListBucketSpacesResult]:
        """Iterates over the BucketSpaces.

        Args:
            request (models.ListBucketSpacesRequest): The request for the ListBucketSpaces operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListBucketSpacesResult]: An iterator of ListBucketSpacesResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_bucket_spaces(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.continuation_token = result.next_continuation_token

    def __repr__(self) -> str:
        return "<ListBucketSpacesPaginator>"
