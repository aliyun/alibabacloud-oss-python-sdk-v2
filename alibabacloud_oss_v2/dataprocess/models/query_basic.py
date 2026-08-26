# -*- coding: utf-8 -*-
"""Query models for OSS DataProcess module."""

import json
from typing import Optional, List, Any
from ... import serde
from ...serde import RequestModel
from .file import Files


class Aggregation(serde.Model):
    """Aggregation definition."""

    _attribute_map = {
        'field': {'tag': 'xml', 'rename': 'Field', 'type': 'str'},
        'operation': {'tag': 'xml', 'rename': 'Operation', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Aggregation'
    }

    def __init__(
            self,
            field: Optional[str] = None,
            operation: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            field (str, optional): The field name for aggregation.
            operation (str, optional): The aggregation operation type.
        """
        super().__init__(**kwargs)
        self.field = field
        self.operation = operation


class AggregationGroup(serde.Model):
    """Aggregation group result."""

    _attribute_map = {
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
        'count': {'tag': 'xml', 'rename': 'Count', 'type': 'int'},
    }

    _xml_map = {
        'name': 'AggregationGroup'
    }

    def __init__(
            self,
            value: Optional[str] = None,
            count: Optional[int] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            value (str, optional): The group value.
            count (int, optional): The count of items in this group.
        """
        super().__init__(**kwargs)
        self.value = value
        self.count = count


class Groups(serde.Model):
    """The list of aggregation groups."""

    _attribute_map = {
        'group': {'tag': 'xml', 'rename': 'Group', 'type': '[AggregationGroup]'},
    }

    _xml_map = {
        'name': 'Groups'
    }

    def __init__(
            self,
            group: Optional[List[AggregationGroup]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            group (List[AggregationGroup], optional): The list of aggregation groups.
        """
        super().__init__(**kwargs)
        self.group = group


class AggregationInfo(serde.Model):
    """Aggregation result info."""

    _attribute_map = {
        'field': {'tag': 'xml', 'rename': 'Field', 'type': 'str'},
        'operation': {'tag': 'xml', 'rename': 'Operation', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'float'},
        'groups': {'tag': 'xml', 'rename': 'Groups', 'type': 'Groups'},
    }

    _xml_map = {
        'name': 'AggregationInfo'
    }

    def __init__(
            self,
            field: Optional[str] = None,
            operation: Optional[str] = None,
            value: Optional[float] = None,
            groups: Optional[Groups] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            field (str, optional): The field name for aggregation.
            operation (str, optional): The aggregation operation type.
            value (float, optional): The aggregation result value.
            groups (Groups, optional): The aggregation groups.
        """
        super().__init__(**kwargs)
        self.field = field
        self.operation = operation
        self.value = value
        self.groups = groups


class Aggregations(serde.Model):
    """The list of aggregation results."""

    _attribute_map = {
        'aggregation': {'tag': 'xml', 'rename': 'Aggregation', 'type': '[AggregationInfo]'},
    }

    _xml_map = {
        'name': 'Aggregations'
    }

    def __init__(
            self,
            aggregation: Optional[List[AggregationInfo]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            aggregation (List[AggregationInfo], optional): The list of aggregation results.
        """
        super().__init__(**kwargs)
        self.aggregation = aggregation


class SimpleQuery(serde.Model):
    """Simple query structure with nested sub-queries."""

    _attribute_map = {
        'field': {'tag': 'xml', 'rename': 'Field', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
        'operation': {'tag': 'xml', 'rename': 'Operation', 'type': 'str'},
        'sub_queries': {'tag': 'xml', 'rename': 'SimpleQuery', 'type': '[SimpleQuery]'},
    }

    _xml_map = {
        'name': 'SimpleQuery'
    }

    def __init__(
            self,
            field: Optional[str] = None,
            value: Optional[str] = None,
            operation: Optional[str] = None,
            sub_queries: Optional[List['SimpleQuery']] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            field (str, optional): The field name to query.
            value (str, optional): The value to compare.
            operation (str, optional): The query operation type.
            sub_queries (List[SimpleQuery], optional): The list of nested sub-queries.
        """
        super().__init__(**kwargs)
        self.field = field
        self.value = value
        self.operation = operation
        self.sub_queries = sub_queries


def _simple_query_to_dict(query):
    """Recursively convert a SimpleQuery instance to a JSON-serializable dict."""
    result = {}
    if query.field is not None:
        result['Field'] = query.field
    if query.value is not None:
        result['Value'] = query.value
    if query.operation is not None:
        result['Operation'] = query.operation
    if query.sub_queries is not None:
        result['SubQueries'] = [_simple_query_to_dict(sub) for sub in query.sub_queries]
    return result


class SimpleQueryRequest(RequestModel):
    """The request for the SimpleQuery operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'max_results': {'tag': 'input', 'position': 'query', 'rename': 'maxResults', 'type': 'int'},
        'next_token': {'tag': 'input', 'position': 'query', 'rename': 'nextToken', 'type': 'str'},
        'sort': {'tag': 'input', 'position': 'query', 'rename': 'sort', 'type': 'str'},
        'order': {'tag': 'input', 'position': 'query', 'rename': 'order', 'type': 'str'},
        'with_fields': {'tag': 'input', 'position': 'query', 'rename': 'withFields', 'type': 'str'},
        'aggregations': {'tag': 'input', 'position': 'query', 'rename': 'aggregations', 'type': 'str'},
        'query': {'tag': 'input', 'position': 'query', 'rename': 'query', 'type': 'str'},
        'without_total_hits': {'tag': 'input', 'position': 'query', 'rename': 'withoutTotalHits', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            max_results: Optional[int] = None,
            next_token: Optional[str] = None,
            sort: Optional[str] = None,
            order: Optional[str] = None,
            with_fields: Any = None,
            aggregations: Any = None,
            query: Any = None,
            without_total_hits: Any = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            max_results (int, optional): The maximum number of results to return.
            next_token (str, optional): The token for the next page of results.
            sort (str, optional): The field to sort by.
            order (str, optional): The sort order (asc or desc).
            with_fields: The fields to include in the response. Can be a list of strings or a JSON string.
            aggregations: The aggregation definitions. Can be a list of Aggregation or a JSON string.
            query: The query definition. Can be a SimpleQuery or a JSON string.
            without_total_hits: Whether to skip computing total hits. Can be a bool or a string.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.max_results = max_results
        self.next_token = next_token
        self.sort = sort
        self.order = order
        if isinstance(with_fields, list):
            self.with_fields = json.dumps(with_fields)
        else:
            self.with_fields = with_fields
        if isinstance(aggregations, list):
            self.aggregations = json.dumps(
                [{'Field': a.field, 'Operation': a.operation} for a in aggregations if a.field is not None]
            )
        else:
            self.aggregations = aggregations
        if isinstance(query, SimpleQuery):
            self.query = json.dumps(_simple_query_to_dict(query))
        else:
            self.query = query
        if isinstance(without_total_hits, bool):
            self.without_total_hits = str(without_total_hits).lower()
        else:
            self.without_total_hits = without_total_hits


class SimpleQueryResponseBody(serde.Model):
    """The response body for the SimpleQuery operation."""

    _attribute_map = {
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
        'total_hits': {'tag': 'xml', 'rename': 'TotalHits', 'type': 'int'},
        'files': {'tag': 'xml', 'rename': 'Files', 'type': 'Files'},
        'aggregations': {'tag': 'xml', 'rename': 'Aggregations', 'type': 'Aggregations'},
    }

    _xml_map = {
        'name': 'MetaQuery'
    }

    def __init__(
            self,
            next_token: Optional[str] = None,
            total_hits: Optional[int] = None,
            files: Optional[Files] = None,
            aggregations: Optional[Aggregations] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            next_token (str, optional): The token for the next page of results.
            total_hits (int, optional): The total number of matching results.
            files (Files, optional): The query result files.
            aggregations (Aggregations, optional): The aggregation results.
        """
        super().__init__(**kwargs)
        self.next_token = next_token
        self.total_hits = total_hits
        self.files = files
        self.aggregations = aggregations


class SimpleQueryResult(serde.ResultModel):
    """The result for the SimpleQuery operation."""

    _attribute_map = {
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
        'total_hits': {'tag': 'xml', 'rename': 'TotalHits', 'type': 'int'},
        'files': {'tag': 'xml', 'rename': 'Files', 'type': 'Files'},
        'aggregations': {'tag': 'xml', 'rename': 'Aggregations', 'type': 'Aggregations'},
    }

    _xml_map = {
        'name': 'MetaQuery'
    }

    def __init__(
            self,
            next_token: Optional[str] = None,
            total_hits: Optional[int] = None,
            files: Optional[Files] = None,
            aggregations: Optional[Aggregations] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            next_token (str, optional): The token for the next page of results.
            total_hits (int, optional): The total number of matching results.
            files (Files, optional): The query result files.
            aggregations (Aggregations, optional): The aggregation results.
        """
        super().__init__(**kwargs)
        self.next_token = next_token
        self.total_hits = total_hits
        self.files = files
        self.aggregations = aggregations


class SemanticQueryRequest(RequestModel):
    """The request for the SemanticQuery operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'max_results': {'tag': 'input', 'position': 'query', 'rename': 'maxResults', 'type': 'int'},
        'query': {'tag': 'input', 'position': 'query', 'rename': 'query', 'type': 'str'},
        'with_fields': {'tag': 'input', 'position': 'query', 'rename': 'withFields', 'type': 'str'},
        'media_types': {'tag': 'input', 'position': 'query', 'rename': 'mediaTypes', 'type': 'str'},
        'source_uri': {'tag': 'input', 'position': 'query', 'rename': 'sourceURI', 'type': 'str'},
        'simple_query': {'tag': 'input', 'position': 'query', 'rename': 'simpleQuery', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            max_results: Optional[int] = None,
            query: Optional[str] = None,
            with_fields: Any = None,
            media_types: Any = None,
            source_uri: Optional[str] = None,
            simple_query: Any = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            max_results (int, optional): The maximum number of results to return.
            query (str, optional): The semantic query string.
            with_fields: The fields to include in the response. Can be a list of strings or a JSON string.
            media_types: The media type filters. Can be a list of strings or a JSON string.
            source_uri (str, optional): The source URI filter.
            simple_query: The simple query definition. Can be a SimpleQuery or a JSON string.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.max_results = max_results
        self.query = query
        if isinstance(with_fields, list):
            self.with_fields = json.dumps(with_fields)
        else:
            self.with_fields = with_fields
        if isinstance(media_types, list):
            self.media_types = json.dumps(media_types)
        else:
            self.media_types = media_types
        self.source_uri = source_uri
        if isinstance(simple_query, SimpleQuery):
            self.simple_query = json.dumps(_simple_query_to_dict(simple_query))
        else:
            self.simple_query = simple_query


class SemanticQueryResponseBody(serde.Model):
    """The response body for the SemanticQuery operation."""

    _attribute_map = {
        'files': {'tag': 'xml', 'rename': 'Files', 'type': 'Files'},
    }

    _xml_map = {
        'name': 'MetaQuery'
    }

    def __init__(
            self,
            files: Optional[Files] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            files (Files, optional): The query result files.
        """
        super().__init__(**kwargs)
        self.files = files


class SemanticQueryResult(serde.ResultModel):
    """The result for the SemanticQuery operation."""

    _attribute_map = {
        'files': {'tag': 'xml', 'rename': 'Files', 'type': 'Files'},
    }

    _xml_map = {
        'name': 'MetaQuery'
    }

    def __init__(
            self,
            files: Optional[Files] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            files (Files, optional): The query result files.
        """
        super().__init__(**kwargs)
        self.files = files
