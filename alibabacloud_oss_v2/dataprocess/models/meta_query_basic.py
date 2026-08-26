# -*- coding: utf-8 -*-
"""MetaQuery models for OSS DataProcess module."""

import json
from typing import Optional, List, Any
from ... import serde
from ...serde import RequestModel
from .dataset_basic import DatasetConfig, WorkflowParameters
from .query_basic import Aggregation, Aggregations
from .file import Files
from ._json_util import to_list


class IgnoreEvents(serde.Model):
    """The list of event types to ignore."""

    _attribute_map = {
        'ignore_event': {'tag': 'xml', 'rename': 'IgnoreEvent', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'IgnoreEvents'
    }

    def __init__(
            self,
            ignore_event: Optional[List[str]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            ignore_event (List[str], optional): The list of event types to ignore.
        """
        super().__init__(**kwargs)
        self.ignore_event = ignore_event


class WithFields(serde.Model):
    """The list of fields to include."""

    _attribute_map = {
        'with_field': {'tag': 'xml', 'rename': 'WithField', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'WithFields'
    }

    def __init__(
            self,
            with_field: Optional[List[str]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            with_field (List[str], optional): The list of fields to include.
        """
        super().__init__(**kwargs)
        self.with_field = with_field

    def to_parameter_value(self) -> str:
        """Serializes to the JSON value of the withFields query parameter."""
        return json.dumps(self.with_field or [])


class Filters(serde.Model):
    """The list of filters for meta query."""

    _attribute_map = {
        'filter': {'tag': 'xml', 'rename': 'Filter', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'Filters'
    }

    def __init__(
            self,
            filter: Optional[List[str]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            filter (List[str], optional): The list of filters.
        """
        super().__init__(**kwargs)
        self.filter = filter


class MediaTypes(serde.Model):
    """The list of media type filters."""

    _attribute_map = {
        'media_type': {'tag': 'xml', 'rename': 'MediaType', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'MediaTypes'
    }

    def __init__(
            self,
            media_type: Optional[List[str]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            media_type (List[str], optional): The list of media type filters.
        """
        super().__init__(**kwargs)
        self.media_type = media_type

    def to_parameter_value(self) -> str:
        """Serializes to the JSON value of the mediaTypes query parameter."""
        return json.dumps(self.media_type or [])


class SmartClusterIds(serde.Model):
    """The list of smart cluster IDs to filter."""

    _attribute_map = {
        'smart_cluster_id': {'tag': 'xml', 'rename': 'SmartClusterId', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'SmartClusterIds'
    }

    def __init__(
            self,
            smart_cluster_id: Optional[List[str]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            smart_cluster_id (List[str], optional): The list of smart cluster IDs.
        """
        super().__init__(**kwargs)
        self.smart_cluster_id = smart_cluster_id


class MetaQueryAggregations(serde.Model):
    """The list of aggregation definitions for DoMetaQuery request."""

    _attribute_map = {
        'aggregation': {'tag': 'xml', 'rename': 'Aggregation', 'type': '[Aggregation]'},
    }

    _xml_map = {
        'name': 'Aggregations'
    }

    def __init__(
            self,
            aggregation: Optional[List[Aggregation]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            aggregation (List[Aggregation], optional): The list of aggregation definitions.
        """
        super().__init__(**kwargs)
        self.aggregation = aggregation

    def to_parameter_value(self) -> str:
        """Serializes to the JSON value of the aggregations query parameter."""
        return json.dumps(to_list(self.aggregation) or [])


class IndexOptions(serde.Model):
    """Index options for MetaQuery."""

    _attribute_map = {
        'ignore_object_delete': {'tag': 'xml', 'rename': 'IgnoreObjectDelete', 'type': 'str'},
        'ignore_events': {'tag': 'xml', 'rename': 'IgnoreEvents', 'type': 'IgnoreEvents'},
    }

    _xml_map = {
        'name': 'IndexOptions'
    }

    def __init__(
            self,
            ignore_object_delete: Optional[str] = None,
            ignore_events: Optional[IgnoreEvents] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            ignore_object_delete (str, optional): Whether to ignore object delete events.
            ignore_events (IgnoreEvents, optional): The event types to ignore.
        """
        super().__init__(**kwargs)
        self.ignore_object_delete = ignore_object_delete
        self.ignore_events = ignore_events


class RouteRule(serde.Model):
    """Route rule for MetaQuery."""

    _attribute_map = {
        'type': {'tag': 'xml', 'rename': 'Type', 'type': 'str'},
        'auto_create_dataset': {'tag': 'xml', 'rename': 'AutoCreateDataset', 'type': 'str'},
        'oss_tag_key': {'tag': 'xml', 'rename': 'OSSTagKey', 'type': 'str'},
    }

    _xml_map = {
        'name': 'RouteRule'
    }

    def __init__(
            self,
            type: Optional[str] = None,
            auto_create_dataset: Optional[str] = None,
            oss_tag_key: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            type (str, optional): The type of the route rule.
            auto_create_dataset (str, optional): Whether to auto-create the dataset.
            oss_tag_key (str, optional): The OSS tag key for routing.
        """
        super().__init__(**kwargs)
        self.type = type
        self.auto_create_dataset = auto_create_dataset
        self.oss_tag_key = oss_tag_key


class MetaQueryNotification(serde.Model):
    """MetaQuery notification configuration."""

    _attribute_map = {
        'mns': {'tag': 'xml', 'rename': 'MNS', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Notification'
    }

    def __init__(
            self,
            mns: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            mns (str, optional): The MNS topic ARN for notification.
        """
        super().__init__(**kwargs)
        self.mns = mns


class MetaQueryNotifications(serde.Model):
    """MetaQuery notifications list."""

    _attribute_map = {
        'notifications': {'tag': 'xml', 'rename': 'Notification', 'type': '[MetaQueryNotification]'},
    }

    _xml_map = {
        'name': 'Notifications'
    }

    def __init__(
            self,
            notifications: Optional[List[MetaQueryNotification]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            notifications (List[MetaQueryNotification], optional): The list of notification configurations.
        """
        super().__init__(**kwargs)
        self.notifications = notifications


class NotificationAttributes(serde.Model):
    """Notification attributes for MetaQuery."""

    _attribute_map = {
        'notifications': {'tag': 'xml', 'rename': 'Notifications', 'type': 'MetaQueryNotifications'},
        'with_fields': {'tag': 'xml', 'rename': 'WithFields', 'type': 'WithFields'},
    }

    _xml_map = {
        'name': 'NotificationAttributes'
    }

    def __init__(
            self,
            notifications: Optional[MetaQueryNotifications] = None,
            with_fields: Optional[WithFields] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            notifications (MetaQueryNotifications, optional): The notifications configuration.
            with_fields (WithFields, optional): The fields to include in notifications.
        """
        super().__init__(**kwargs)
        self.notifications = notifications
        self.with_fields = with_fields


class MetaQueryOpenBody(serde.Model):
    """Body for OpenMetaQuery request."""

    _attribute_map = {
        'workflow_parameters': {'tag': 'xml', 'rename': 'WorkflowParameters', 'type': 'WorkflowParameters'},
        'filters': {'tag': 'xml', 'rename': 'Filters', 'type': 'Filters'},
        'notification_attributes': {'tag': 'xml', 'rename': 'NotificationAttributes', 'type': 'NotificationAttributes'},
        'dataset_config': {'tag': 'xml', 'rename': 'DatasetConfig', 'type': 'DatasetConfig'},
        'index_options': {'tag': 'xml', 'rename': 'IndexOptions', 'type': 'IndexOptions'},
        'route_rule': {'tag': 'xml', 'rename': 'RouteRule', 'type': 'RouteRule'},
    }

    _xml_map = {
        'name': 'MetaQuery'
    }

    def __init__(
            self,
            workflow_parameters: Optional[WorkflowParameters] = None,
            filters: Optional[Filters] = None,
            notification_attributes: Optional[NotificationAttributes] = None,
            dataset_config: Optional[DatasetConfig] = None,
            index_options: Optional[IndexOptions] = None,
            route_rule: Optional[RouteRule] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            workflow_parameters (WorkflowParameters, optional): The workflow parameters.
            filters (Filters, optional): The filters for meta query.
            notification_attributes (NotificationAttributes, optional): The notification attributes configuration.
            dataset_config (DatasetConfig, optional): The dataset configuration.
            index_options (IndexOptions, optional): The index options configuration.
            route_rule (RouteRule, optional): The route rule configuration.
        """
        super().__init__(**kwargs)
        self.workflow_parameters = workflow_parameters
        self.filters = filters
        self.notification_attributes = notification_attributes
        self.dataset_config = dataset_config
        self.index_options = index_options
        self.route_rule = route_rule


class MetaQueryDoBody(serde.Model):
    """Body for DoMetaQuery request."""

    _attribute_map = {
        'query': {'tag': 'xml', 'rename': 'Query', 'type': 'str'},
        'sort': {'tag': 'xml', 'rename': 'Sort', 'type': 'str'},
        'order': {'tag': 'xml', 'rename': 'Order', 'type': 'str'},
        'aggregations': {'tag': 'xml', 'rename': 'Aggregations', 'type': 'MetaQueryAggregations'},
        'max_results': {'tag': 'xml', 'rename': 'MaxResults', 'type': 'int'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
        'with_fields': {'tag': 'xml', 'rename': 'WithFields', 'type': 'WithFields'},
        'without_total_hits': {'tag': 'xml', 'rename': 'WithoutTotalHits', 'type': 'str'},
        'source_uri': {'tag': 'xml', 'rename': 'SourceURI', 'type': 'str'},
        'media_types': {'tag': 'xml', 'rename': 'MediaTypes', 'type': 'MediaTypes'},
        'simple_query': {'tag': 'xml', 'rename': 'SimpleQuery', 'type': 'str'},
        'smart_cluster_ids': {'tag': 'xml', 'rename': 'SmartClusterIds', 'type': 'SmartClusterIds'},
    }

    _xml_map = {
        'name': 'MetaQuery'
    }

    def __init__(
            self,
            query: Optional[str] = None,
            sort: Optional[str] = None,
            order: Optional[str] = None,
            aggregations: Optional[MetaQueryAggregations] = None,
            max_results: Optional[int] = None,
            next_token: Optional[str] = None,
            with_fields: Optional[WithFields] = None,
            without_total_hits: Optional[str] = None,
            source_uri: Optional[str] = None,
            media_types: Optional[MediaTypes] = None,
            simple_query: Optional[str] = None,
            smart_cluster_ids: Optional[SmartClusterIds] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            query (str, optional): The query expression.
            sort (str, optional): The field to sort by.
            order (str, optional): The sort order (asc or desc).
            aggregations (MetaQueryAggregations, optional): The aggregation definitions.
            max_results (int, optional): The maximum number of results to return.
            next_token (str, optional): The token for the next page of results.
            with_fields (WithFields, optional): The fields to include in the response.
            without_total_hits (str, optional): Whether to skip computing total hits.
            source_uri (str, optional): The source URI filter.
            media_types (MediaTypes, optional): The media type filters.
            simple_query (str, optional): The simple query expression.
            smart_cluster_ids (SmartClusterIds, optional): The smart cluster IDs to filter.
        """
        super().__init__(**kwargs)
        self.query = query
        self.sort = sort
        self.order = order
        self.aggregations = aggregations
        self.max_results = max_results
        self.next_token = next_token
        self.with_fields = with_fields
        self.without_total_hits = without_total_hits
        self.source_uri = source_uri
        self.media_types = media_types
        self.simple_query = simple_query
        self.smart_cluster_ids = smart_cluster_ids


class MetaQueryStatus(serde.Model):
    """MetaQuery status information."""

    _attribute_map = {
        'state': {'tag': 'xml', 'rename': 'State', 'type': 'str'},
        'phase': {'tag': 'xml', 'rename': 'Phase', 'type': 'str'},
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'update_time': {'tag': 'xml', 'rename': 'UpdateTime', 'type': 'str'},
        'meta_query_mode': {'tag': 'xml', 'rename': 'MetaQueryMode', 'type': 'str'},
        'workflow_parameters': {'tag': 'xml', 'rename': 'WorkflowParameters', 'type': 'WorkflowParameters'},
        'index_options': {'tag': 'xml', 'rename': 'IndexOptions', 'type': 'IndexOptions'},
        'route_rule': {'tag': 'xml', 'rename': 'RouteRule', 'type': 'RouteRule'},
        'notification_attributes': {'tag': 'xml', 'rename': 'NotificationAttributes', 'type': 'NotificationAttributes'},
        'dataset_config': {'tag': 'xml', 'rename': 'DatasetConfig', 'type': 'DatasetConfig'},
        'filters': {'tag': 'xml', 'rename': 'Filters', 'type': 'Filters'},
    }

    _xml_map = {
        'name': 'MetaQueryStatus'
    }

    def __init__(
            self,
            state: Optional[str] = None,
            phase: Optional[str] = None,
            create_time: Optional[str] = None,
            update_time: Optional[str] = None,
            meta_query_mode: Optional[str] = None,
            workflow_parameters: Optional[WorkflowParameters] = None,
            index_options: Optional[IndexOptions] = None,
            route_rule: Optional[RouteRule] = None,
            notification_attributes: Optional[NotificationAttributes] = None,
            dataset_config: Optional[DatasetConfig] = None,
            filters: Optional[Filters] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            state (str, optional): The state of the meta query.
            phase (str, optional): The phase of the meta query.
            create_time (str, optional): The time when the meta query was created.
            update_time (str, optional): The time when the meta query was last updated.
            meta_query_mode (str, optional): The mode of the meta query.
            workflow_parameters (WorkflowParameters, optional): The workflow parameters.
            index_options (IndexOptions, optional): The index options configuration.
            route_rule (RouteRule, optional): The route rule configuration.
            notification_attributes (NotificationAttributes, optional): The notification attributes.
            dataset_config (DatasetConfig, optional): The dataset configuration.
            filters (Filters, optional): The filters for meta query.
        """
        super().__init__(**kwargs)
        self.state = state
        self.phase = phase
        self.create_time = create_time
        self.update_time = update_time
        self.meta_query_mode = meta_query_mode
        self.workflow_parameters = workflow_parameters
        self.index_options = index_options
        self.route_rule = route_rule
        self.notification_attributes = notification_attributes
        self.dataset_config = dataset_config
        self.filters = filters


class OpenMetaQueryRequest(RequestModel):
    """The request for the OpenMetaQuery operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'mode': {'tag': 'input', 'position': 'query', 'rename': 'mode', 'type': 'str'},
        'role': {'tag': 'input', 'position': 'query', 'rename': 'role', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            mode: Optional[str] = None,
            role: Optional[str] = None,
            meta_query_body: Optional[MetaQueryOpenBody] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            mode (str, optional): The mode of the meta query.
            role (str, optional): The role for the meta query.
            meta_query_body (MetaQueryOpenBody, optional): The request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.mode = mode
        self.role = role
        self.meta_query_body = meta_query_body


class OpenMetaQueryResult(serde.ResultModel):
    """The result for the OpenMetaQuery operation."""
    pass


class GetMetaQueryStatusRequest(RequestModel):
    """The request for the GetMetaQueryStatus operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetMetaQueryStatusResult(serde.ResultModel):
    """The result for the GetMetaQueryStatus operation."""

    _attribute_map = {
        'status': {'tag': 'output', 'position': 'body', 'rename': 'MetaQueryStatus', 'type': 'MetaQueryStatus,xml'},
    }

    def __init__(
            self,
            status: Optional[MetaQueryStatus] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            status (MetaQueryStatus, optional): The meta query status information.
        """
        super().__init__(**kwargs)
        self.status = status


class CloseMetaQueryRequest(RequestModel):
    """The request for the CloseMetaQuery operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class CloseMetaQueryResult(serde.ResultModel):
    """The result for the CloseMetaQuery operation."""
    pass


class DoMetaQueryRequest(RequestModel):
    """The request for the DoMetaQuery operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'mode': {'tag': 'input', 'position': 'query', 'rename': 'mode', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            mode: Optional[str] = None,
            meta_query_body: Optional[MetaQueryDoBody] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            mode (str, optional): The mode of the meta query.
            meta_query_body (MetaQueryDoBody, optional): The request body.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.mode = mode
        self.meta_query_body = meta_query_body


class DoMetaQueryResponseBody(serde.Model):
    """The response body for the DoMetaQuery operation."""

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


class DoMetaQueryResult(serde.ResultModel):
    """The result for the DoMetaQuery operation."""

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
