"""Paginator for tables list operations."""
import abc
import copy
from typing import Iterator, Any
from . import models


class ListNamespacesAPIClient(abc.ABC):
    """Abstract base class for list_namespaces client."""

    @abc.abstractmethod
    def list_namespaces(self, request: models.ListNamespacesRequest, **kwargs) -> models.ListNamespacesResult:
        """Lists namespaces in a table bucket."""


class ListNamespacesPaginator:
    """A paginator for ListNamespaces"""

    def __init__(
        self,
        client: ListNamespacesAPIClient,
        **kwargs: Any
    ) -> None:
        """
        Args:
            client (ListNamespacesAPIClient): A client that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListNamespacesRequest, **kwargs: Any) -> Iterator[models.ListNamespacesResult]:
        """Iterates over the namespaces.

        Args:
            request (models.ListNamespacesRequest): The request for the ListNamespaces operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListNamespacesResult]: An iterator of ListNamespacesResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_namespaces = limit

        first_page = True
        has_more = False

        while first_page or has_more:
            result = self._client.list_namespaces(req)
            yield result

            first_page = False
            next_token = getattr(result, 'continuation_token', None)
            if next_token:
                req.continuation_token = next_token
                has_more = True
            else:
                has_more = False

    def __repr__(self) -> str:
        return "<ListNamespacesPaginator>"


class ListTableBucketsAPIClient(abc.ABC):
    """Abstract base class for list_table_buckets client."""

    @abc.abstractmethod
    def list_table_buckets(self, request: models.ListTableBucketsRequest, **kwargs) -> models.ListTableBucketsResult:
        """Lists table buckets that belong to your Alibaba Cloud account."""


class ListTableBucketsPaginator:
    """A paginator for ListTableBuckets"""

    def __init__(
        self,
        client: ListTableBucketsAPIClient,
        **kwargs: Any
    ) -> None:
        """
        Args:
            client (ListTableBucketsAPIClient): A client that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListTableBucketsRequest, **kwargs: Any) -> Iterator[models.ListTableBucketsResult]:
        """Iterates over the table buckets.

        Args:
            request (models.ListTableBucketsRequest): The request for the ListTableBuckets operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListTableBucketsResult]: An iterator of ListTableBucketsResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_table_buckets = str(limit)

        first_page = True
        has_more = False

        while first_page or has_more:
            result = self._client.list_table_buckets(req)
            yield result

            first_page = False
            next_token = getattr(result, 'continuation_token', None)
            if next_token:
                req.continuation_token = next_token
                has_more = True
            else:
                has_more = False

    def __repr__(self) -> str:
        return "<ListTableBucketsPaginator>"


class ListTablesAPIClient(abc.ABC):
    """Abstract base class for list_tables client."""

    @abc.abstractmethod
    def list_tables(self, request: models.ListTablesRequest, **kwargs) -> models.ListTablesResult:
        """Lists tables in a namespace."""


class ListTablesPaginator:
    """A paginator for ListTables"""

    def __init__(
        self,
        client: ListTablesAPIClient,
        **kwargs: Any
    ) -> None:
        """
        Args:
            client (ListTablesAPIClient): A client that sends the request.
            limit (int, optional): The maximum number of items in the response.
        """
        self._client = client
        self._limit = kwargs.get('limit', None)

    def iter_page(self, request: models.ListTablesRequest, **kwargs: Any) -> Iterator[models.ListTablesResult]:
        """Iterates over the tables.

        Args:
            request (models.ListTablesRequest): The request for the ListTables operation.
            limit (int, optional): The maximum number of items in the response.

        Yields:
            Iterator[models.ListTablesResult]: An iterator of ListTablesResult from the response
        """
        limit = kwargs.get('limit', self._limit)
        req = copy.copy(request)
        if limit is not None:
            req.max_tables = limit

        first_page = True
        has_more = False

        while first_page or has_more:
            result = self._client.list_tables(req)
            yield result

            first_page = False
            next_token = getattr(result, 'continuation_token', None)
            if next_token:
                req.continuation_token = next_token
                has_more = True
            else:
                has_more = False

    def __repr__(self) -> str:
        return "<ListTablesPaginator>"
