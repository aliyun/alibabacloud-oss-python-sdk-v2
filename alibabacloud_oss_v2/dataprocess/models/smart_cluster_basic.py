# -*- coding: utf-8 -*-
"""SmartCluster models for OSS DataProcess module."""

import json
from typing import Optional, List, Any
from ... import serde
from ...serde import RequestModel


class SmartClusterRule(serde.Model):
    """SmartCluster rule model."""

    _attribute_map = {
        'rule_type': {'tag': 'xml', 'rename': 'RuleType', 'type': 'str'},
        'base_uris': {'tag': 'xml', 'rename': 'BaseURIs', 'type': '[str]'},
        'keywords': {'tag': 'xml', 'rename': 'Keywords', 'type': '[str]'},
        'sensitivity': {'tag': 'xml', 'rename': 'Sensitivity', 'type': 'float'},
    }

    _xml_map = {
        'name': 'Rule'
    }

    def __init__(
            self,
            rule_type: Optional[str] = None,
            base_uris: Optional[List[str]] = None,
            keywords: Optional[List[str]] = None,
            sensitivity: Optional[float] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            rule_type (str, optional): The type of the rule.
            base_uris (List[str], optional): The list of base URIs for the rule.
            keywords (List[str], optional): The list of keywords for the rule.
            sensitivity (float, optional): The sensitivity level of the rule.
        """
        super().__init__(**kwargs)
        self.rule_type = rule_type
        self.base_uris = base_uris
        self.keywords = keywords
        self.sensitivity = sensitivity


class SmartClusterMNS(serde.Model):
    """MNS configuration for SmartCluster notification."""

    _attribute_map = {
        'topic_name': {'tag': 'xml', 'rename': 'TopicName', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MNS'
    }

    def __init__(
            self,
            topic_name: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            topic_name (str, optional): The MNS topic name.
        """
        super().__init__(**kwargs)
        self.topic_name = topic_name


class SmartClusterNotificationInfo(serde.Model):
    """SmartCluster notification configuration."""

    _attribute_map = {
        'mns': {'tag': 'xml', 'rename': 'MNS', 'type': 'SmartClusterMNS'},
    }

    _xml_map = {
        'name': 'Notification'
    }

    def __init__(
            self,
            mns: Optional[SmartClusterMNS] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            mns (SmartClusterMNS, optional): The MNS configuration.
        """
        super().__init__(**kwargs)
        self.mns = mns


class Rules(serde.Model):
    """The list of smart cluster rules."""

    _attribute_map = {
        'rule': {'tag': 'xml', 'rename': 'Rule', 'type': '[SmartClusterRule]'},
    }

    _xml_map = {
        'name': 'Rules'
    }

    def __init__(
            self,
            rule: Optional[List[SmartClusterRule]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            rule (List[SmartClusterRule], optional): The list of rules.
        """
        super().__init__(**kwargs)
        self.rule = rule


class SmartClusterInfo(serde.Model):
    """SmartCluster information."""

    _attribute_map = {
        'object_id': {'tag': 'xml', 'rename': 'ObjectId', 'type': 'str'},
        'cluster_type': {'tag': 'xml', 'rename': 'ClusterType', 'type': 'str'},
        'name': {'tag': 'xml', 'rename': 'Name', 'type': 'str'},
        'description': {'tag': 'xml', 'rename': 'Description', 'type': 'str'},
        'reason': {'tag': 'xml', 'rename': 'Reason', 'type': 'str'},
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'update_time': {'tag': 'xml', 'rename': 'UpdateTime', 'type': 'str'},
        'rules': {'tag': 'xml', 'rename': 'Rules', 'type': 'Rules'},
        'notification': {'tag': 'xml', 'rename': 'Notification', 'type': 'SmartClusterNotificationInfo'},
    }

    _xml_map = {
        'name': 'SmartCluster'
    }

    def __init__(
            self,
            object_id: Optional[str] = None,
            cluster_type: Optional[str] = None,
            name: Optional[str] = None,
            description: Optional[str] = None,
            reason: Optional[str] = None,
            create_time: Optional[str] = None,
            update_time: Optional[str] = None,
            rules: Optional[Rules] = None,
            notification: Optional[SmartClusterNotificationInfo] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            object_id (str, optional): The object ID of the smart cluster.
            cluster_type (str, optional): The type of the smart cluster.
            name (str, optional): The name of the smart cluster.
            description (str, optional): The description of the smart cluster.
            reason (str, optional): The reason for creating the smart cluster.
            create_time (str, optional): The time when the smart cluster was created.
            update_time (str, optional): The time when the smart cluster was last updated.
            rules (Rules, optional): The rules for the smart cluster.
            notification (SmartClusterNotificationInfo, optional): The notification configuration.
        """
        super().__init__(**kwargs)
        self.object_id = object_id
        self.cluster_type = cluster_type
        self.name = name
        self.description = description
        self.reason = reason
        self.create_time = create_time
        self.update_time = update_time
        self.rules = rules
        self.notification = notification


class CreateSmartClusterRequest(RequestModel):
    """The request for the CreateSmartCluster operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'name': {'tag': 'input', 'position': 'query', 'rename': 'name', 'type': 'str'},
        'description': {'tag': 'input', 'position': 'query', 'rename': 'description', 'type': 'str'},
        'cluster_type': {'tag': 'input', 'position': 'query', 'rename': 'clusterType', 'type': 'str'},
        'rules': {'tag': 'input', 'position': 'query', 'rename': 'rules', 'type': 'str'},
        'notification': {'tag': 'input', 'position': 'query', 'rename': 'notification', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            name: Optional[str] = None,
            description: Optional[str] = None,
            cluster_type: Optional[str] = None,
            rules: Any = None,
            notification: Any = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            name (str, optional): The name of the smart cluster.
            description (str, optional): The description of the smart cluster.
            cluster_type (str, optional): The type of the smart cluster.
            rules: The rules for the smart cluster. Can be a list of SmartClusterRule or a JSON string.
            notification: The notification configuration. Can be a SmartClusterNotificationInfo or a JSON string.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.name = name
        self.description = description
        self.cluster_type = cluster_type
        if isinstance(rules, list):
            self.rules = json.dumps(
                [_smart_cluster_rule_to_dict(r) for r in rules]
            )
        else:
            self.rules = rules
        if isinstance(notification, SmartClusterNotificationInfo):
            mns_dict = {}
            if notification.mns is not None and notification.mns.topic_name is not None:
                mns_dict = {'TopicName': notification.mns.topic_name}
            self.notification = json.dumps({'MNS': mns_dict} if mns_dict else {})
        else:
            self.notification = notification


class CreateSmartClusterResponseBody(serde.Model):
    """The response body for the CreateSmartCluster operation."""

    _attribute_map = {
        'object_id': {'tag': 'xml', 'rename': 'ObjectId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'CreateSmartClusterResponse'
    }

    def __init__(
            self,
            object_id: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            object_id (str, optional): The object ID of the created smart cluster.
        """
        super().__init__(**kwargs)
        self.object_id = object_id


class CreateSmartClusterResult(serde.ResultModel):
    """The result for the CreateSmartCluster operation."""

    _attribute_map = {
        'object_id': {'tag': 'xml', 'rename': 'ObjectId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'CreateSmartClusterResponse'
    }

    def __init__(
            self,
            object_id: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            object_id (str, optional): The object ID of the created smart cluster.
        """
        super().__init__(**kwargs)
        self.object_id = object_id


class GetSmartClusterRequest(RequestModel):
    """The request for the GetSmartCluster operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'object_id': {'tag': 'input', 'position': 'query', 'rename': 'objectId', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            object_id: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            object_id (str, optional): The object ID of the smart cluster.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.object_id = object_id


class GetSmartClusterResponseBody(serde.Model):
    """The response body for the GetSmartCluster operation."""

    _attribute_map = {
        'smart_cluster': {'tag': 'xml', 'rename': 'SmartCluster', 'type': 'SmartClusterInfo'},
    }

    _xml_map = {
        'name': 'GetSmartClusterResponse'
    }

    def __init__(
            self,
            smart_cluster: Optional[SmartClusterInfo] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            smart_cluster (SmartClusterInfo, optional): The smart cluster information.
        """
        super().__init__(**kwargs)
        self.smart_cluster = smart_cluster


class GetSmartClusterResult(serde.ResultModel):
    """The result for the GetSmartCluster operation."""

    _attribute_map = {
        'smart_cluster': {'tag': 'xml', 'rename': 'SmartCluster', 'type': 'SmartClusterInfo'},
    }

    _xml_map = {
        'name': 'GetSmartClusterResponse'
    }

    def __init__(
            self,
            smart_cluster: Optional[SmartClusterInfo] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            smart_cluster (SmartClusterInfo, optional): The smart cluster information.
        """
        super().__init__(**kwargs)
        self.smart_cluster = smart_cluster


class UpdateSmartClusterRequest(RequestModel):
    """The request for the UpdateSmartCluster operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'object_id': {'tag': 'input', 'position': 'query', 'rename': 'objectId', 'type': 'str'},
        'name': {'tag': 'input', 'position': 'query', 'rename': 'name', 'type': 'str'},
        'description': {'tag': 'input', 'position': 'query', 'rename': 'description', 'type': 'str'},
        'rules': {'tag': 'input', 'position': 'query', 'rename': 'rules', 'type': 'str'},
        'rule': {'tag': 'input', 'position': 'query', 'rename': 'rule', 'type': 'str'},
        'notification': {'tag': 'input', 'position': 'query', 'rename': 'notification', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            object_id: Optional[str] = None,
            name: Optional[str] = None,
            description: Optional[str] = None,
            rules: Any = None,
            rule: Any = None,
            notification: Any = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            object_id (str, optional): The object ID of the smart cluster.
            name (str, optional): The new name of the smart cluster.
            description (str, optional): The new description of the smart cluster.
            rules: The new rules for the smart cluster. Can be a list of SmartClusterRule or a JSON string.
            rule: A single rule for the smart cluster. Can be a SmartClusterRule or a JSON string.
            notification: The notification configuration. Can be a SmartClusterNotificationInfo or a JSON string.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.object_id = object_id
        self.name = name
        self.description = description
        if isinstance(rules, list):
            self.rules = json.dumps(
                [_smart_cluster_rule_to_dict(r) for r in rules]
            )
        else:
            self.rules = rules
        if isinstance(rule, SmartClusterRule):
            self.rule = json.dumps(_smart_cluster_rule_to_dict(rule))
        else:
            self.rule = rule
        if isinstance(notification, SmartClusterNotificationInfo):
            mns_dict = {}
            if notification.mns is not None and notification.mns.topic_name is not None:
                mns_dict = {'TopicName': notification.mns.topic_name}
            self.notification = json.dumps({'MNS': mns_dict} if mns_dict else {})
        else:
            self.notification = notification


class UpdateSmartClusterResponseBody(serde.Model):
    """The response body for the UpdateSmartCluster operation."""

    _attribute_map = {
        'object_id': {'tag': 'xml', 'rename': 'ObjectId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'UpdateSmartClusterResponse'
    }

    def __init__(
            self,
            object_id: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            object_id (str, optional): The object ID of the updated smart cluster.
        """
        super().__init__(**kwargs)
        self.object_id = object_id


class UpdateSmartClusterResult(serde.ResultModel):
    """The result for the UpdateSmartCluster operation."""

    _attribute_map = {
        'object_id': {'tag': 'xml', 'rename': 'ObjectId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'UpdateSmartClusterResponse'
    }

    def __init__(
            self,
            object_id: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            object_id (str, optional): The object ID of the updated smart cluster.
        """
        super().__init__(**kwargs)
        self.object_id = object_id


class DeleteSmartClusterRequest(RequestModel):
    """The request for the DeleteSmartCluster operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'object_id': {'tag': 'input', 'position': 'query', 'rename': 'objectId', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            object_id: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            object_id (str, optional): The object ID of the smart cluster to delete.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.object_id = object_id


class DeleteSmartClusterResult(serde.ResultModel):
    """The result for the DeleteSmartCluster operation."""
    pass


class ListSmartClustersRequest(RequestModel):
    """The request for the ListSmartClusters operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'max_results': {'tag': 'input', 'position': 'query', 'rename': 'maxResults', 'type': 'int'},
        'next_token': {'tag': 'input', 'position': 'query', 'rename': 'nextToken', 'type': 'str'},
        'cluster_type': {'tag': 'input', 'position': 'query', 'rename': 'clusterType', 'type': 'str'},
        'rule_types': {'tag': 'input', 'position': 'query', 'rename': 'ruleTypes', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            max_results: Optional[int] = None,
            next_token: Optional[str] = None,
            cluster_type: Optional[str] = None,
            rule_types: Any = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            max_results (int, optional): The maximum number of results to return.
            next_token (str, optional): The token for the next page of results.
            cluster_type (str, optional): The type of smart clusters to filter.
            rule_types: The rule types to filter. Can be a list of strings or a JSON array string.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.max_results = max_results
        self.next_token = next_token
        self.cluster_type = cluster_type
        if isinstance(rule_types, list):
            self.rule_types = json.dumps(rule_types)
        else:
            self.rule_types = rule_types


class SmartClusters(serde.Model):
    """The list of smart clusters."""

    _attribute_map = {
        'smart_cluster': {'tag': 'xml', 'rename': 'SmartCluster', 'type': '[SmartClusterInfo]'},
    }

    _xml_map = {
        'name': 'SmartClusters'
    }

    def __init__(
            self,
            smart_cluster: Optional[List[SmartClusterInfo]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            smart_cluster (List[SmartClusterInfo], optional): The list of smart clusters.
        """
        super().__init__(**kwargs)
        self.smart_cluster = smart_cluster


class ListSmartClustersResponseBody(serde.Model):
    """The response body for the ListSmartClusters operation."""

    _attribute_map = {
        'smart_clusters': {'tag': 'xml', 'rename': 'SmartClusters', 'type': 'SmartClusters'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ListSmartClustersResponse'
    }

    def __init__(
            self,
            smart_clusters: Optional[SmartClusters] = None,
            next_token: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            smart_clusters (SmartClusters, optional): The list of smart clusters.
            next_token (str, optional): The token for the next page of results.
        """
        super().__init__(**kwargs)
        self.smart_clusters = smart_clusters
        self.next_token = next_token


class ListSmartClustersResult(serde.ResultModel):
    """The result for the ListSmartClusters operation."""

    _attribute_map = {
        'smart_clusters': {'tag': 'xml', 'rename': 'SmartClusters', 'type': 'SmartClusters'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ListSmartClustersResponse'
    }

    def __init__(
            self,
            smart_clusters: Optional[SmartClusters] = None,
            next_token: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            smart_clusters (SmartClusters, optional): The list of smart clusters.
            next_token (str, optional): The token for the next page of results.
        """
        super().__init__(**kwargs)
        self.smart_clusters = smart_clusters
        self.next_token = next_token


def _smart_cluster_rule_to_dict(rule: SmartClusterRule) -> dict:
    """Helper to convert SmartClusterRule to a dictionary for JSON serialization."""
    result = {}
    if rule.rule_type is not None:
        result['RuleType'] = rule.rule_type
    if rule.base_uris is not None:
        result['BaseURIs'] = rule.base_uris
    if rule.keywords is not None:
        result['Keywords'] = rule.keywords
    if rule.sensitivity is not None:
        result['Sensitivity'] = rule.sensitivity
    return result
