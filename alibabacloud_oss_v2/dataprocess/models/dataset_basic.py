# -*- coding: utf-8 -*-
"""Dataset models for OSS DataProcess module."""

import json
from typing import Optional, List, Any
from ... import serde
from ...serde import RequestModel
from ._json_util import compact, to_obj, to_list


class WorkflowParameter(serde.Model):
    """A workflow parameter with name-value pair."""

    _attribute_map = {
        'name': {'tag': 'xml', 'rename': 'Name', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
    }

    _xml_map = {
        'name': 'WorkflowParameter'
    }

    def __init__(
            self,
            name: Optional[str] = None,
            value: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the workflow parameter.
            value (str, optional): The value of the workflow parameter.
        """
        super().__init__(**kwargs)
        self.name = name
        self.value = value

    def _to_json_obj(self) -> dict:
        return compact({
            'Name': self.name,
            'Value': self.value,
        })


class WorkflowParameters(serde.Model):
    """A list of workflow parameters."""

    _attribute_map = {
        'workflow_parameters': {'tag': 'xml', 'rename': 'WorkflowParameter', 'type': '[WorkflowParameter]'},
    }

    _xml_map = {
        'name': 'WorkflowParameters'
    }

    def __init__(
            self,
            workflow_parameters: Optional[List[WorkflowParameter]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            workflow_parameters (List[WorkflowParameter], optional): The list of workflow parameters.
        """
        super().__init__(**kwargs)
        self.workflow_parameters = workflow_parameters

    def _to_json_obj(self) -> list:
        return to_list(self.workflow_parameters) or []

    def to_parameter_value(self) -> str:
        """Serializes to the JSON value of the workflowParameters query parameter."""
        return json.dumps(self._to_json_obj())


class EnableConfig(serde.Model):
    """A generic configuration model containing a single Enable field."""

    _attribute_map = {
        'enable': {'tag': 'xml', 'rename': 'Enable', 'type': 'str'},
    }

    _xml_map = {
        'name': 'EnableConfig'
    }

    def __init__(
            self,
            enable: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            enable (str, optional): Whether to enable this configuration.
        """
        super().__init__(**kwargs)
        self.enable = enable

    def _to_json_obj(self) -> dict:
        return compact({'Enable': self.enable})


class InsightsLabelItem(serde.Model):
    """Label item for InsightsConfig."""

    _attribute_map = {
        'name': {'tag': 'xml', 'rename': 'Name', 'type': 'str'},
        'description': {'tag': 'xml', 'rename': 'Description', 'type': 'str'},
    }

    # Aligned with Java: serialized as <Label> within the <Labels> wrapper.
    _xml_map = {
        'name': 'Label'
    }

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the label item.
            description (str, optional): The description of the label item.
        """
        super().__init__(**kwargs)
        self.name = name
        self.description = description

    def _to_json_obj(self) -> dict:
        return compact({
            'Name': self.name,
            'Description': self.description,
        })


class InsightsLabels(serde.Model):
    """The list of insights label items."""

    _attribute_map = {
        'label': {'tag': 'xml', 'rename': 'Label', 'type': '[InsightsLabelItem]'},
    }

    _xml_map = {
        'name': 'Labels'
    }

    def __init__(
            self,
            label: Optional[List[InsightsLabelItem]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            label (List[InsightsLabelItem], optional): The list of label items.
        """
        super().__init__(**kwargs)
        self.label = label

    # The <Label> wrapper element exists only in XML; JSON carries a flat array.
    def _to_json_obj(self) -> list:
        return to_list(self.label) or []


class InsightsCaptionConfig(serde.Model):
    """Caption configuration for Insights.Image/Video."""

    _attribute_map = {
        'enable': {'tag': 'xml', 'rename': 'Enable', 'type': 'str'},
        'prompt': {'tag': 'xml', 'rename': 'Prompt', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Caption'
    }

    def __init__(
            self,
            enable: Optional[str] = None,
            prompt: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            enable (str, optional): Whether to enable caption generation.
            prompt (str, optional): The prompt for caption generation.
        """
        super().__init__(**kwargs)
        self.enable = enable
        self.prompt = prompt

    def _to_json_obj(self) -> dict:
        return compact({
            'Enable': self.enable,
            'Prompt': self.prompt,
        })


class InsightsImageConfig(serde.Model):
    """Insights.Image configuration within InsightsConfig."""

    _attribute_map = {
        'caption': {'tag': 'xml', 'rename': 'Caption', 'type': 'InsightsCaptionConfig'},
        'label': {'tag': 'xml', 'rename': 'Label', 'type': 'InsightsImageLabelConfig'},
    }

    _xml_map = {
        'name': 'Image'
    }

    def __init__(
            self,
            caption: Optional[InsightsCaptionConfig] = None,
            label: Optional['InsightsImageLabelConfig'] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            caption (InsightsCaptionConfig, optional): The caption configuration for image insights.
            label (InsightsImageLabelConfig, optional): The label configuration for image insights.
        """
        super().__init__(**kwargs)
        self.caption = caption
        self.label = label

    def _to_json_obj(self) -> dict:
        return compact({
            'Caption': to_obj(self.caption),
            'Label': to_obj(self.label),
        })


class InsightsVideoCaptionConfig(serde.Model):
    """Video Caption configuration within InsightsConfig."""

    _attribute_map = {
        'enable': {'tag': 'xml', 'rename': 'Enable', 'type': 'str'},
        'prompt': {'tag': 'xml', 'rename': 'Prompt', 'type': 'str'},
        'person_reference': {'tag': 'xml', 'rename': 'PersonReference', 'type': 'EnableConfig'},
    }

    _xml_map = {
        'name': 'Caption'
    }

    def __init__(
            self,
            enable: Optional[str] = None,
            prompt: Optional[str] = None,
            person_reference: Optional[EnableConfig] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            enable (str, optional): Whether to enable video caption.
            prompt (str, optional): The prompt for video caption.
            person_reference (EnableConfig, optional): Whether to enable person reference.
        """
        super().__init__(**kwargs)
        self.enable = enable
        self.prompt = prompt
        self.person_reference = person_reference

    def _to_json_obj(self) -> dict:
        return compact({
            'Enable': self.enable,
            'Prompt': self.prompt,
            'PersonReference': to_obj(self.person_reference),
        })


class InsightsLabelUserDefinedConfig(serde.Model):
    """User defined label configuration."""

    _attribute_map = {
        'enable': {'tag': 'xml', 'rename': 'Enable', 'type': 'str'},
        'mode': {'tag': 'xml', 'rename': 'Mode', 'type': 'str'},
        'labels': {'tag': 'xml', 'rename': 'Labels', 'type': 'InsightsLabels'},
    }

    _xml_map = {
        'name': 'UserDefined'
    }

    def __init__(
            self,
            enable: Optional[str] = None,
            mode: Optional[str] = None,
            labels: Optional[InsightsLabels] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            enable (str, optional): Whether to enable user defined labels.
            mode (str, optional): The mode of user defined labels.
            labels (InsightsLabels, optional): The user defined label items.
        """
        super().__init__(**kwargs)
        self.enable = enable
        self.mode = mode
        self.labels = labels

    def _to_json_obj(self) -> dict:
        return compact({
            'Enable': self.enable,
            'Mode': self.mode,
            'Labels': to_obj(self.labels),
        })


class InsightsLabelHighlightConfig(serde.Model):
    """Highlight label configuration within Insights.Video.Label."""

    _attribute_map = {
        'enable': {'tag': 'xml', 'rename': 'Enable', 'type': 'str'},
        'labels': {'tag': 'xml', 'rename': 'Labels', 'type': 'InsightsLabels'},
    }

    _xml_map = {
        'name': 'Highlight'
    }

    def __init__(
            self,
            enable: Optional[str] = None,
            labels: Optional[InsightsLabels] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            enable (str, optional): Whether to enable label highlight.
            labels (InsightsLabels, optional): The highlight label items.
        """
        super().__init__(**kwargs)
        self.enable = enable
        self.labels = labels

    def _to_json_obj(self) -> dict:
        return compact({
            'Enable': self.enable,
            'Labels': to_obj(self.labels),
        })


class InsightsImageLabelConfig(serde.Model):
    """Image Label configuration within InsightsConfig."""

    _attribute_map = {
        'system': {'tag': 'xml', 'rename': 'System', 'type': 'EnableConfig'},
        'user_defined': {'tag': 'xml', 'rename': 'UserDefined', 'type': 'InsightsLabelUserDefinedConfig'},
    }

    _xml_map = {
        'name': 'Label'
    }

    def __init__(
            self,
            system: Optional[EnableConfig] = None,
            user_defined: Optional[InsightsLabelUserDefinedConfig] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            system (EnableConfig, optional): The system label configuration.
            user_defined (InsightsLabelUserDefinedConfig, optional): The user defined label configuration.
        """
        super().__init__(**kwargs)
        self.system = system
        self.user_defined = user_defined

    def _to_json_obj(self) -> dict:
        return compact({
            'System': to_obj(self.system),
            'UserDefined': to_obj(self.user_defined),
        })


class InsightsVideoLabelConfig(serde.Model):
    """Video Label configuration within InsightsConfig."""

    _attribute_map = {
        'system': {'tag': 'xml', 'rename': 'System', 'type': 'EnableConfig'},
        'user_defined': {'tag': 'xml', 'rename': 'UserDefined', 'type': 'InsightsLabelUserDefinedConfig'},
        'highlight': {'tag': 'xml', 'rename': 'Highlight', 'type': 'InsightsLabelHighlightConfig'},
    }

    _xml_map = {
        'name': 'Label'
    }

    def __init__(
            self,
            system: Optional[EnableConfig] = None,
            user_defined: Optional[InsightsLabelUserDefinedConfig] = None,
            highlight: Optional[InsightsLabelHighlightConfig] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            system (EnableConfig, optional): The system label configuration.
            user_defined (InsightsLabelUserDefinedConfig, optional): The user defined label configuration.
            highlight (InsightsLabelHighlightConfig, optional): The highlight label configuration.
        """
        super().__init__(**kwargs)
        self.system = system
        self.user_defined = user_defined
        self.highlight = highlight

    def _to_json_obj(self) -> dict:
        return compact({
            'System': to_obj(self.system),
            'UserDefined': to_obj(self.user_defined),
            'Highlight': to_obj(self.highlight),
        })


class InsightsVideoConfig(serde.Model):
    """Insights.Video configuration within InsightsConfig."""

    _attribute_map = {
        'caption': {'tag': 'xml', 'rename': 'Caption', 'type': 'InsightsVideoCaptionConfig'},
        'label': {'tag': 'xml', 'rename': 'Label', 'type': 'InsightsVideoLabelConfig'},
        'multi_stream': {'tag': 'xml', 'rename': 'MultiStream', 'type': 'EnableConfig'},
    }

    _xml_map = {
        'name': 'Video'
    }

    def __init__(
            self,
            caption: Optional[InsightsVideoCaptionConfig] = None,
            label: Optional[InsightsVideoLabelConfig] = None,
            multi_stream: Optional[EnableConfig] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            caption (InsightsVideoCaptionConfig, optional): The video caption configuration.
            label (InsightsVideoLabelConfig, optional): The video label configuration.
            multi_stream (EnableConfig, optional): Whether to enable multi-stream video processing.
        """
        super().__init__(**kwargs)
        self.caption = caption
        self.label = label
        self.multi_stream = multi_stream

    def _to_json_obj(self) -> dict:
        return compact({
            'Caption': to_obj(self.caption),
            'Label': to_obj(self.label),
            'MultiStream': to_obj(self.multi_stream),
        })


class ReverseImageConfig(serde.Model):
    """ReverseImage configuration within DatasetConfig."""

    _attribute_map = {
        'image': {'tag': 'xml', 'rename': 'Image', 'type': 'EnableConfig'},
        'video': {'tag': 'xml', 'rename': 'Video', 'type': 'EnableConfig'},
    }

    _xml_map = {
        'name': 'ReverseImage'
    }

    def __init__(
            self,
            image: Optional[EnableConfig] = None,
            video: Optional[EnableConfig] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            image (EnableConfig, optional): Whether to enable reverse image search for images.
            video (EnableConfig, optional): Whether to enable reverse image search for videos.
        """
        super().__init__(**kwargs)
        self.image = image
        self.video = video

    def _to_json_obj(self) -> dict:
        return compact({
            'Image': to_obj(self.image),
            'Video': to_obj(self.video),
        })


class InsightsConfig(serde.Model):
    """Insights configuration within DatasetConfig."""

    _attribute_map = {
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'image': {'tag': 'xml', 'rename': 'Image', 'type': 'InsightsImageConfig'},
        'video': {'tag': 'xml', 'rename': 'Video', 'type': 'InsightsVideoConfig'},
    }

    _xml_map = {
        'name': 'Insights'
    }

    def __init__(
            self,
            language: Optional[str] = None,
            image: Optional[InsightsImageConfig] = None,
            video: Optional[InsightsVideoConfig] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            language (str, optional): The language for insights processing.
            image (InsightsImageConfig, optional): The image insights configuration.
            video (InsightsVideoConfig, optional): The video insights configuration.
        """
        super().__init__(**kwargs)
        self.language = language
        self.image = image
        self.video = video

    def _to_json_obj(self) -> dict:
        return compact({
            'Language': self.language,
            'Image': to_obj(self.image),
            'Video': to_obj(self.video),
        })


class SmartClusterFigureConfig(serde.Model):
    """SmartCluster.Figure configuration within DatasetConfig."""

    _attribute_map = {
        'auto_generate': {'tag': 'xml', 'rename': 'AutoGenerate', 'type': 'str'},
        'auto_clustering': {'tag': 'xml', 'rename': 'AutoClustering', 'type': 'str'},
        'min_entity_count': {'tag': 'xml', 'rename': 'MinEntityCount', 'type': 'int'},
        'enabled_features': {'tag': 'xml', 'rename': 'EnabledFeatures', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'Figure'
    }

    def __init__(
            self,
            auto_generate: Optional[str] = None,
            auto_clustering: Optional[str] = None,
            min_entity_count: Optional[int] = None,
            enabled_features: Optional[List[str]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            auto_generate (str, optional): Whether to auto-generate smart clusters.
            auto_clustering (str, optional): Whether to enable auto clustering.
            min_entity_count (int, optional): The minimum entity count for clustering.
            enabled_features (List[str], optional): The list of enabled features.
        """
        super().__init__(**kwargs)
        self.auto_generate = auto_generate
        self.auto_clustering = auto_clustering
        self.min_entity_count = min_entity_count
        self.enabled_features = enabled_features

    def _to_json_obj(self) -> dict:
        return compact({
            'AutoGenerate': self.auto_generate,
            'AutoClustering': self.auto_clustering,
            'MinEntityCount': self.min_entity_count,
            'EnabledFeatures': self.enabled_features,
        })


class SmartClusterConfig(serde.Model):
    """SmartCluster configuration within DatasetConfig."""

    _attribute_map = {
        'figure': {'tag': 'xml', 'rename': 'Figure', 'type': 'SmartClusterFigureConfig'},
    }

    _xml_map = {
        'name': 'SmartCluster'
    }

    def __init__(
            self,
            figure: Optional[SmartClusterFigureConfig] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            figure (SmartClusterFigureConfig, optional): The figure configuration for smart cluster.
        """
        super().__init__(**kwargs)
        self.figure = figure

    def _to_json_obj(self) -> dict:
        return compact({'Figure': to_obj(self.figure)})


class DatasetConfig(serde.Model):
    """Dataset configuration."""

    _attribute_map = {
        'reverse_image': {'tag': 'xml', 'rename': 'ReverseImage', 'type': 'ReverseImageConfig'},
        'insights': {'tag': 'xml', 'rename': 'Insights', 'type': 'InsightsConfig'},
        'smart_cluster': {'tag': 'xml', 'rename': 'SmartCluster', 'type': 'SmartClusterConfig'},
    }

    _xml_map = {
        'name': 'DatasetConfig'
    }

    def __init__(
            self,
            reverse_image: Optional[ReverseImageConfig] = None,
            insights: Optional[InsightsConfig] = None,
            smart_cluster: Optional[SmartClusterConfig] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            reverse_image (ReverseImageConfig, optional): The reverse image search configuration.
            insights (InsightsConfig, optional): The insights configuration for data processing.
            smart_cluster (SmartClusterConfig, optional): The smart cluster configuration.
        """
        super().__init__(**kwargs)
        self.reverse_image = reverse_image
        self.insights = insights
        self.smart_cluster = smart_cluster

    def _to_json_obj(self) -> dict:
        return compact({
            'Insights': to_obj(self.insights),
            'SmartCluster': to_obj(self.smart_cluster),
            'ReverseImage': to_obj(self.reverse_image),
        })

    def to_parameter_value(self) -> str:
        """Serializes to the JSON value of the datasetConfig query parameter."""
        return json.dumps(self._to_json_obj())


class Dataset(serde.Model):
    """Dataset information."""

    _attribute_map = {
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'dataset_max_bind_count': {'tag': 'xml', 'rename': 'DatasetMaxBindCount', 'type': 'int'},
        'dataset_max_entity_count': {'tag': 'xml', 'rename': 'DatasetMaxEntityCount', 'type': 'int'},
        'dataset_max_file_count': {'tag': 'xml', 'rename': 'DatasetMaxFileCount', 'type': 'int'},
        'dataset_max_relation_count': {'tag': 'xml', 'rename': 'DatasetMaxRelationCount', 'type': 'int'},
        'dataset_max_total_file_size': {'tag': 'xml', 'rename': 'DatasetMaxTotalFileSize', 'type': 'int'},
        'dataset_name': {'tag': 'xml', 'rename': 'DatasetName', 'type': 'str'},
        'description': {'tag': 'xml', 'rename': 'Description', 'type': 'str'},
        'file_count': {'tag': 'xml', 'rename': 'FileCount', 'type': 'int'},
        'total_file_size': {'tag': 'xml', 'rename': 'TotalFileSize', 'type': 'int'},
        'update_time': {'tag': 'xml', 'rename': 'UpdateTime', 'type': 'str'},
        'workflow_parameters': {'tag': 'xml', 'rename': 'WorkflowParameters', 'type': 'WorkflowParameters'},
        'dataset_config': {'tag': 'xml', 'rename': 'DatasetConfig', 'type': 'DatasetConfig'},
    }

    _xml_map = {
        'name': 'Dataset'
    }

    def __init__(
            self,
            create_time: Optional[str] = None,
            dataset_max_bind_count: Optional[int] = None,
            dataset_max_entity_count: Optional[int] = None,
            dataset_max_file_count: Optional[int] = None,
            dataset_max_relation_count: Optional[int] = None,
            dataset_max_total_file_size: Optional[int] = None,
            dataset_name: Optional[str] = None,
            description: Optional[str] = None,
            file_count: Optional[int] = None,
            total_file_size: Optional[int] = None,
            update_time: Optional[str] = None,
            workflow_parameters: Optional[WorkflowParameters] = None,
            dataset_config: Optional[DatasetConfig] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            create_time (str, optional): The time when the dataset was created.
            dataset_max_bind_count (int, optional): The maximum number of bindings for the dataset.
            dataset_max_entity_count (int, optional): The maximum number of entities in the dataset.
            dataset_max_file_count (int, optional): The maximum number of files in the dataset.
            dataset_max_relation_count (int, optional): The maximum number of relations in the dataset.
            dataset_max_total_file_size (int, optional): The maximum total file size in bytes.
            dataset_name (str, optional): The name of the dataset.
            description (str, optional): The description of the dataset.
            file_count (int, optional): The number of files in the dataset.
            total_file_size (int, optional): The total file size in bytes.
            update_time (str, optional): The time when the dataset was last updated.
            workflow_parameters (WorkflowParameters, optional): The workflow parameters.
            dataset_config (DatasetConfig, optional): The dataset configuration.
        """
        super().__init__(**kwargs)
        self.create_time = create_time
        self.dataset_max_bind_count = dataset_max_bind_count
        self.dataset_max_entity_count = dataset_max_entity_count
        self.dataset_max_file_count = dataset_max_file_count
        self.dataset_max_relation_count = dataset_max_relation_count
        self.dataset_max_total_file_size = dataset_max_total_file_size
        self.dataset_name = dataset_name
        self.description = description
        self.file_count = file_count
        self.total_file_size = total_file_size
        self.update_time = update_time
        self.workflow_parameters = workflow_parameters
        self.dataset_config = dataset_config


class Datasets(serde.Model):
    """The list of datasets."""

    _attribute_map = {
        'dataset': {'tag': 'xml', 'rename': 'Dataset', 'type': '[Dataset]'},
    }

    _xml_map = {
        'name': 'Datasets'
    }

    def __init__(
            self,
            dataset: Optional[List[Dataset]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            dataset (List[Dataset], optional): The list of datasets.
        """
        super().__init__(**kwargs)
        self.dataset = dataset


class CreateDatasetRequest(RequestModel):
    """The request for the CreateDataset operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'description': {'tag': 'input', 'position': 'query', 'rename': 'description', 'type': 'str'},
        'workflow_parameters': {'tag': 'input', 'position': 'query', 'rename': 'workflowParameters', 'type': 'str'},
        'dataset_config': {'tag': 'input', 'position': 'query', 'rename': 'datasetConfig', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            description: Optional[str] = None,
            workflow_parameters: Optional[str] = None,
            dataset_config: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            description (str, optional): The description of the dataset.
            workflow_parameters (str, optional): The workflow parameters.
                The value can be built through WorkflowParameters.to_parameter_value().
            dataset_config (str, optional): The dataset configuration.
                The value can be built through DatasetConfig.to_parameter_value().
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.description = description
        self.workflow_parameters = workflow_parameters
        self.dataset_config = dataset_config


class CreateDatasetResponseBody(serde.Model):
    """The response body for the CreateDataset operation."""

    _attribute_map = {
        'dataset': {'tag': 'xml', 'rename': 'Dataset', 'type': 'Dataset'},
    }

    _xml_map = {
        'name': 'CreateDatasetResponse'
    }

    def __init__(
            self,
            dataset: Optional[Dataset] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            dataset (Dataset, optional): The dataset information.
        """
        super().__init__(**kwargs)
        self.dataset = dataset


class CreateDatasetResult(serde.ResultModel):
    """The result for the CreateDataset operation."""

    _attribute_map = {
        'dataset': {'tag': 'xml', 'rename': 'Dataset', 'type': 'Dataset'},
    }

    _xml_map = {
        'name': 'CreateDatasetResponse'
    }

    def __init__(
            self,
            dataset: Optional[Dataset] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            dataset (Dataset, optional): The dataset information.
        """
        super().__init__(**kwargs)
        self.dataset = dataset


class GetDatasetRequest(RequestModel):
    """The request for the GetDataset operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'with_statistics': {'tag': 'input', 'position': 'query', 'rename': 'withStatistics', 'type': 'bool'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            with_statistics: Optional[bool] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            with_statistics (bool, optional): Whether to include statistics in the response.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.with_statistics = with_statistics


class GetDatasetResponseBody(serde.Model):
    """The response body for the GetDataset operation."""

    _attribute_map = {
        'dataset': {'tag': 'xml', 'rename': 'Dataset', 'type': 'Dataset'},
    }

    _xml_map = {
        'name': 'GetDatasetResponse'
    }

    def __init__(
            self,
            dataset: Optional[Dataset] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            dataset (Dataset, optional): The dataset information.
        """
        super().__init__(**kwargs)
        self.dataset = dataset


class GetDatasetResult(serde.ResultModel):
    """The result for the GetDataset operation."""

    _attribute_map = {
        'dataset': {'tag': 'xml', 'rename': 'Dataset', 'type': 'Dataset'},
    }

    _xml_map = {
        'name': 'GetDatasetResponse'
    }

    def __init__(
            self,
            dataset: Optional[Dataset] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            dataset (Dataset, optional): The dataset information.
        """
        super().__init__(**kwargs)
        self.dataset = dataset


class UpdateDatasetRequest(RequestModel):
    """The request for the UpdateDataset operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'description': {'tag': 'input', 'position': 'query', 'rename': 'description', 'type': 'str'},
        'workflow_parameters': {'tag': 'input', 'position': 'query', 'rename': 'workflowParameters', 'type': 'str'},
        'dataset_config': {'tag': 'input', 'position': 'query', 'rename': 'datasetConfig', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            description: Optional[str] = None,
            workflow_parameters: Optional[str] = None,
            dataset_config: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            description (str, optional): The description of the dataset.
            workflow_parameters (str, optional): The workflow parameters.
                The value can be built through WorkflowParameters.to_parameter_value().
            dataset_config (str, optional): The dataset configuration.
                The value can be built through DatasetConfig.to_parameter_value().
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.description = description
        self.workflow_parameters = workflow_parameters
        self.dataset_config = dataset_config


class UpdateDatasetResponseBody(serde.Model):
    """The response body for the UpdateDataset operation."""

    _attribute_map = {
        'dataset': {'tag': 'xml', 'rename': 'Dataset', 'type': 'Dataset'},
    }

    _xml_map = {
        'name': 'UpdateDatasetResponse'
    }

    def __init__(
            self,
            dataset: Optional[Dataset] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            dataset (Dataset, optional): The dataset information.
        """
        super().__init__(**kwargs)
        self.dataset = dataset


class UpdateDatasetResult(serde.ResultModel):
    """The result for the UpdateDataset operation."""

    _attribute_map = {
        'dataset': {'tag': 'xml', 'rename': 'Dataset', 'type': 'Dataset'},
    }

    _xml_map = {
        'name': 'UpdateDatasetResponse'
    }

    def __init__(
            self,
            dataset: Optional[Dataset] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            dataset (Dataset, optional): The dataset information.
        """
        super().__init__(**kwargs)
        self.dataset = dataset


class DeleteDatasetRequest(RequestModel):
    """The request for the DeleteDataset operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name


class DeleteDatasetResult(serde.ResultModel):
    """The result for the DeleteDataset operation."""
    pass


class ListDatasetsRequest(RequestModel):
    """The request for the ListDatasets operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'max_results': {'tag': 'input', 'position': 'query', 'rename': 'maxResults', 'type': 'int'},
        'next_token': {'tag': 'input', 'position': 'query', 'rename': 'nextToken', 'type': 'str'},
        'prefix': {'tag': 'input', 'position': 'query', 'rename': 'prefix', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            max_results: Optional[int] = None,
            next_token: Optional[str] = None,
            prefix: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            max_results (int, optional): The maximum number of results to return.
            next_token (str, optional): The token for the next page of results.
            prefix (str, optional): The prefix filter for dataset names.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.max_results = max_results
        self.next_token = next_token
        self.prefix = prefix


class ListDatasetsResponseBody(serde.Model):
    """The response body for the ListDatasets operation."""

    _attribute_map = {
        'datasets': {'tag': 'xml', 'rename': 'Datasets', 'type': 'Datasets'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ListDatasetsResponse'
    }

    def __init__(
            self,
            datasets: Optional[Datasets] = None,
            next_token: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            datasets (Datasets, optional): The datasets.
            next_token (str, optional): The token for the next page of results.
        """
        super().__init__(**kwargs)
        self.datasets = datasets
        self.next_token = next_token


class ListDatasetsResult(serde.ResultModel):
    """The result for the ListDatasets operation."""

    _attribute_map = {
        'datasets': {'tag': 'xml', 'rename': 'Datasets', 'type': 'Datasets'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ListDatasetsResponse'
    }

    def __init__(
            self,
            datasets: Optional[Datasets] = None,
            next_token: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            datasets (Datasets, optional): The datasets.
            next_token (str, optional): The token for the next page of results.
        """
        super().__init__(**kwargs)
        self.datasets = datasets
        self.next_token = next_token


class DeleteFileMetaRequest(RequestModel):
    """The request for the DeleteFileMeta operation."""

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'dataset_name': {'tag': 'input', 'position': 'query', 'rename': 'datasetName', 'type': 'str'},
        'uri': {'tag': 'input', 'position': 'query', 'rename': 'uri', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            dataset_name: Optional[str] = None,
            uri: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            dataset_name (str, optional): The name of the dataset.
            uri (str, optional): The URI of the file whose metadata is deleted.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.dataset_name = dataset_name
        self.uri = uri


class DeleteFileMetaResult(serde.ResultModel):
    """The result for the DeleteFileMeta operation."""
    pass
