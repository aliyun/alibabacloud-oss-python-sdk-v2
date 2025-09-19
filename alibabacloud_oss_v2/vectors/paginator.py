"""Paginator for list operation."""
import abc
import copy
from typing import Iterator, Any
from . import models


class ListVectorBucketsAPIClient(abc.ABC):
    """Abstract base class for list_vector_buckets client."""

    @abc.abstractmethod
    def list_vector_buckets(self, request: models.ListVectorBucketsRequest, **kwargs) -> models.ListVectorBucketsResult:
        """Lists all vector buckets that belong to your Alibaba Cloud account."""


class ListVectorBucketsPaginator:
    """A paginator for ListVectorBuckets"""

    def __init__(
        self,
        client: ListVectorBucketsAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (ListVectorBucketsAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListVectorBucketsRequest, **kwargs: Any) -> Iterator[models.ListVectorBucketsResult]:
        """Iterates over the vector buckets.

        Args:
            request (models.ListVectorBucketsRequest): The request for the ListVectorBuckets operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListVectorBucketsResult]: An iterator of ListVectorBucketsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_keys = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_vector_buckets(req)
            yield result

            first_page = False
            is_truncated = result.is_truncated
            req.marker = result.next_marker

    def __repr__(self) -> str:
        return "<ListVectorBucketsPaginator>"


class ListVectorIndexesAPIClient(abc.ABC):
    """Abstract base class for list_vector_indexes client."""

    @abc.abstractmethod
    def list_vector_indexes(self, request: models.ListVectorIndexesRequest, **kwargs) -> models.ListVectorIndexesResult:
        """Lists vector indexes in a bucket."""


class ListVectorIndexesPaginator:
    """A paginator for ListVectorIndexes"""

    def __init__(
            self,
            client: ListVectorIndexesAPIClient,
            **kwargs: Any
    ) -> None:
        """
            client (ListVectorIndexesAPIClient): A agent that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListVectorIndexesRequest, **kwargs: Any) -> Iterator[models.ListVectorIndexesResult]:
        """Iterates over the vector indexes.

        Args:
            request (models.ListVectorIndexesRequest): The request for the ListVectorIndexes operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListVectorIndexesResult]: An iterator of ListVectorIndexes from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_results = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_vector_indexes(req)
            yield result

            first_page = False
            if next_token := getattr(result, 'next_token', None):
                req.next_token = next_token
            is_truncated = bool(next_token)

    def __repr__(self) -> str:
        return "<ListVectorIndexesPaginator>"



class ListVectorsAPIClient(abc.ABC):
    """Abstract base class for list_vectors client."""

    @abc.abstractmethod
    def list_vectors(self, request: models.ListVectorsRequest, **kwargs) -> models.ListVectorsResult:
        """Lists vectors in a bucket."""

class ListVectorsPaginator:
    """A paginator for ListVectors"""

    def __init__(
        self,
        client: ListVectorsAPIClient,
        **kwargs: Any
    ) -> None:
        """
        client (ListVectorsAPIClient): A agent that sends the request.
        limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListVectorsRequest, **kwargs: Any) -> Iterator[models.ListVectorsResult]:
        """Iterates over the vectors.

        Args:
            request (vectors.models.ListVectorsRequest): The request for the ListVectors operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[vectors.models.ListVectorsResult]: An iterator of ListVectorsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_results = limit

        first_page = True
        is_truncated = False

        while first_page or is_truncated:
            result = self._client.list_vectors(req)
            yield result

            first_page = False
            if next_token := getattr(result, 'next_token', None):
                req.next_token = next_token
            is_truncated = bool(next_token)

    def __repr__(self) -> str:
        return "<ListVectorsPaginator>"