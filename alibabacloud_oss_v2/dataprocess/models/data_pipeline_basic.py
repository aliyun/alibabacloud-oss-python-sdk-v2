# -*- coding: utf-8 -*-
"""DataPipeline models for OSS DataProcess module."""

from typing import Optional, List, Any
from ... import serde
from ...serde import RequestModel


class DataPipelineSourceFilterConfiguration(serde.Model):
    """Configuration for filtering data pipeline sources."""

    _attribute_map = {
        'prefix_set': {'tag': 'xml', 'rename': 'PrefixSet', 'type': '[str]'},
        'object_media_types': {'tag': 'xml', 'rename': 'ObjectMediaTypes', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'FilterConfiguration'
    }

    def __init__(
            self,
            prefix_set: Optional[List[str]] = None,
            object_media_types: Optional[List[str]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            prefix_set (List[str], optional): The list of prefix filters.
            object_media_types (List[str], optional): The list of object media types.
        """
        super().__init__(**kwargs)
        self.prefix_set = prefix_set
        self.object_media_types = object_media_types


class DataPipelineSource(serde.Model):
    """Source configuration for data pipeline."""

    _attribute_map = {
        'input_bucket': {'tag': 'xml', 'rename': 'InputBucket', 'type': 'str'},
        'input_data_scope': {'tag': 'xml', 'rename': 'InputDataScope', 'type': 'str'},
        'ignore_delete': {'tag': 'xml', 'rename': 'IgnoreDelete', 'type': 'bool'},
        'filter_configuration': {'tag': 'xml', 'rename': 'FilterConfiguration', 'type': 'DataPipelineSourceFilterConfiguration'},
    }

    # Aligned with Java: the serialized wrapper element is <Sources>,
    # whose children are the source fields directly (no nested <Source>).
    _xml_map = {
        'name': 'Sources'
    }

    def __init__(
            self,
            input_bucket: Optional[str] = None,
            input_data_scope: Optional[str] = None,
            ignore_delete: Optional[bool] = None,
            filter_configuration: Optional[DataPipelineSourceFilterConfiguration] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            input_bucket (str, optional): The input bucket name.
            input_data_scope (str, optional): The input data scope.
            ignore_delete (bool, optional): Whether to ignore delete events.
            filter_configuration (DataPipelineSourceFilterConfiguration, optional): The filter configuration.
        """
        super().__init__(**kwargs)
        self.input_bucket = input_bucket
        self.input_data_scope = input_data_scope
        self.ignore_delete = ignore_delete
        self.filter_configuration = filter_configuration


class DataPipelineVectorDestination(serde.Model):
    """Vector destination for a V2 data pipeline output."""

    _attribute_map = {
        'bucket': {'tag': 'xml', 'rename': 'Bucket', 'type': 'str'},
        'index_name': {'tag': 'xml', 'rename': 'IndexName', 'type': 'str'},
        'prefix': {'tag': 'xml', 'rename': 'Prefix', 'type': 'str'},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            index_name: Optional[str] = None,
            prefix: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The vector bucket name.
            index_name (str, optional): The vector index name.
            prefix (str, optional): The vector key prefix.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name
        self.prefix = prefix


class ImageEmbedding(DataPipelineVectorDestination):
    """Destination for image embeddings."""

    _xml_map = {
        'name': 'ImageEmbedding'
    }


class ImageTextEmbedding(DataPipelineVectorDestination):
    """Destination for image text embeddings."""

    _xml_map = {
        'name': 'ImageTextEmbedding'
    }


class VideoFrameEmbedding(DataPipelineVectorDestination):
    """Destination for video frame embeddings."""

    _xml_map = {
        'name': 'VideoFrameEmbedding'
    }


class VideoTextEmbedding(DataPipelineVectorDestination):
    """Destination for video text embeddings."""

    _xml_map = {
        'name': 'VideoTextEmbedding'
    }


class DocumentChunkEmbedding(DataPipelineVectorDestination):
    """Destination for document chunk embeddings."""

    _xml_map = {
        'name': 'DocumentChunkEmbedding'
    }




class InsightsCaption(serde.Model):
    """Caption prompt configuration for V2 data pipeline insights."""

    _attribute_map = {
        'prompt': {'tag': 'xml', 'rename': 'Prompt', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Caption'
    }

    def __init__(
            self,
            prompt: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            prompt (str, optional): The prompt used to generate captions.
        """
        super().__init__(**kwargs)
        self.prompt = prompt


class InsightsSnapshot(serde.Model):
    """Video snapshot configuration for V2 data pipeline insights."""

    _attribute_map = {
        'mode': {'tag': 'xml', 'rename': 'Mode', 'type': 'str'},
        'interval': {'tag': 'xml', 'rename': 'Interval', 'type': 'float'},
        'number': {'tag': 'xml', 'rename': 'Number', 'type': 'int'},
    }

    _xml_map = {
        'name': 'Snapshot'
    }

    def __init__(
            self,
            mode: Optional[str] = None,
            interval: Optional[float] = None,
            number: Optional[int] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            mode (str, optional): The snapshot mode, interval or dhash.
            interval (float, optional): The snapshot interval in seconds.
            number (int, optional): The maximum number of snapshots.
        """
        super().__init__(**kwargs)
        self.mode = mode
        self.interval = interval
        self.number = number


class InsightsFrameEmbedding(serde.Model):
    """Video frame embedding configuration for V2 data pipeline insights."""

    _attribute_map = {
        'snapshot': {'tag': 'xml', 'rename': 'Snapshot', 'type': 'InsightsSnapshot'},
    }

    _xml_map = {
        'name': 'FrameEmbedding'
    }

    def __init__(
            self,
            snapshot: Optional[InsightsSnapshot] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            snapshot (InsightsSnapshot, optional): The video snapshot configuration.
        """
        super().__init__(**kwargs)
        self.snapshot = snapshot


class InsightsImage(serde.Model):
    """Image configuration for V2 data pipeline insights."""

    _attribute_map = {
        'caption': {'tag': 'xml', 'rename': 'Caption', 'type': 'InsightsCaption'},
    }

    _xml_map = {
        'name': 'Image'
    }

    def __init__(
            self,
            caption: Optional[InsightsCaption] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            caption (InsightsCaption, optional): The image caption configuration.
        """
        super().__init__(**kwargs)
        self.caption = caption


class InsightsVideo(serde.Model):
    """Video configuration for V2 data pipeline insights."""

    _attribute_map = {
        'caption': {'tag': 'xml', 'rename': 'Caption', 'type': 'InsightsCaption'},
        'frame_embedding': {'tag': 'xml', 'rename': 'FrameEmbedding', 'type': 'InsightsFrameEmbedding'},
    }

    _xml_map = {
        'name': 'Video'
    }

    def __init__(
            self,
            caption: Optional[InsightsCaption] = None,
            frame_embedding: Optional[InsightsFrameEmbedding] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            caption (InsightsCaption, optional): The video caption configuration.
            frame_embedding (InsightsFrameEmbedding, optional): The video frame embedding configuration.
        """
        super().__init__(**kwargs)
        self.caption = caption
        self.frame_embedding = frame_embedding


class DataPipelineInsights(serde.Model):
    """Insights configuration for a V2 data pipeline."""

    _attribute_map = {
        'image': {'tag': 'xml', 'rename': 'Image', 'type': 'InsightsImage'},
        'video': {'tag': 'xml', 'rename': 'Video', 'type': 'InsightsVideo'},
    }

    _xml_map = {
        'name': 'Insights'
    }

    def __init__(
            self,
            image: Optional[InsightsImage] = None,
            video: Optional[InsightsVideo] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            image (InsightsImage, optional): The image insights configuration.
            video (InsightsVideo, optional): The video insights configuration.
        """
        super().__init__(**kwargs)
        self.image = image
        self.video = video


class DataPipelineDataProcessConfiguration(serde.Model):
    """Data process configuration for a V2 data pipeline."""

    _attribute_map = {
        'search_mode': {'tag': 'xml', 'rename': 'SearchMode', 'type': 'str'},
        'insights': {'tag': 'xml', 'rename': 'Insights', 'type': 'DataPipelineInsights'},
    }

    _xml_map = {
        'name': 'DataPipelineDataProcessConfiguration'
    }

    def __init__(
            self,
            search_mode: Optional[str] = None,
            insights: Optional[DataPipelineInsights] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            search_mode (str, optional): The search mode, fast or balanced.
            insights (DataPipelineInsights, optional): The insights configuration.
        """
        super().__init__(**kwargs)
        self.search_mode = search_mode
        self.insights = insights


class DataPipelineDestination(serde.Model):
    """Destination configuration for data pipeline."""

    _attribute_map = {
        'vector_bucket_name': {'tag': 'xml', 'rename': 'VectorBucketName', 'type': 'str'},
        'vector_key_prefix': {'tag': 'xml', 'rename': 'VectorKeyPrefix', 'type': 'str'},
        'vector_index_names': {'tag': 'xml', 'rename': 'VectorIndexNames', 'type': '[str]'},
        'object_tag_to_metadata': {'tag': 'xml', 'rename': 'ObjectTagToMetadata', 'type': '[str]'},
        'usermeta_to_metadata': {'tag': 'xml', 'rename': 'UsermetaToMetadata', 'type': '[str]'},
        'image_embedding': {'tag': 'xml', 'rename': 'ImageEmbedding', 'type': 'ImageEmbedding'},
        'image_text_embedding': {'tag': 'xml', 'rename': 'ImageTextEmbedding', 'type': 'ImageTextEmbedding'},
        'video_frame_embedding': {'tag': 'xml', 'rename': 'VideoFrameEmbedding', 'type': 'VideoFrameEmbedding'},
        'video_text_embedding': {'tag': 'xml', 'rename': 'VideoTextEmbedding', 'type': 'VideoTextEmbedding'},
        'document_chunk_embedding': {'tag': 'xml', 'rename': 'DocumentChunkEmbedding', 'type': 'DocumentChunkEmbedding'},
    }

    _xml_map = {
        'name': 'Destination'
    }

    def __init__(
            self,
            vector_bucket_name: Optional[str] = None,
            vector_key_prefix: Optional[str] = None,
            vector_index_names: Optional[List[str]] = None,
            object_tag_to_metadata: Optional[List[str]] = None,
            usermeta_to_metadata: Optional[List[str]] = None,
            image_embedding: Optional[ImageEmbedding] = None,
            image_text_embedding: Optional[ImageTextEmbedding] = None,
            video_frame_embedding: Optional[VideoFrameEmbedding] = None,
            video_text_embedding: Optional[VideoTextEmbedding] = None,
            document_chunk_embedding: Optional[DocumentChunkEmbedding] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            vector_bucket_name (str, optional): The vector bucket name.
            vector_key_prefix (str, optional): The vector key prefix.
            vector_index_names (List[str], optional): The list of vector index names.
            object_tag_to_metadata (List[str], optional): The list of object tag to metadata mappings.
            usermeta_to_metadata (List[str], optional): The list of user meta to metadata mappings.
            image_embedding (ImageEmbedding, optional): The image embedding destination.
            image_text_embedding (ImageTextEmbedding, optional): The image text embedding destination.
            video_frame_embedding (VideoFrameEmbedding, optional): The video frame embedding destination.
            video_text_embedding (VideoTextEmbedding, optional): The video text embedding destination.
            document_chunk_embedding (DocumentChunkEmbedding, optional): The document chunk embedding destination.
        """
        super().__init__(**kwargs)
        self.vector_bucket_name = vector_bucket_name
        self.vector_key_prefix = vector_key_prefix
        self.vector_index_names = vector_index_names
        self.object_tag_to_metadata = object_tag_to_metadata
        self.usermeta_to_metadata = usermeta_to_metadata
        self.image_embedding = image_embedding
        self.image_text_embedding = image_text_embedding
        self.video_frame_embedding = video_frame_embedding
        self.video_text_embedding = video_text_embedding
        self.document_chunk_embedding = document_chunk_embedding


class DataPipelineEmbeddingConfiguration(serde.Model):
    """Embedding configuration for data pipeline."""

    _attribute_map = {
        'embedding_provider': {'tag': 'xml', 'rename': 'EmbeddingProvider', 'type': 'str'},
        'api_key': {'tag': 'xml', 'rename': 'ApiKey', 'type': 'str'},
        'model': {'tag': 'xml', 'rename': 'Model', 'type': 'str'},
        'fps': {'tag': 'xml', 'rename': 'FPS', 'type': 'float'},
    }

    _xml_map = {
        'name': 'DataPipelineEmbeddingConfiguration'
    }

    def __init__(
            self,
            embedding_provider: Optional[str] = None,
            api_key: Optional[str] = None,
            model: Optional[str] = None,
            fps: Optional[float] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            embedding_provider (str, optional): The embedding provider name.
            api_key (str, optional): The API key for the embedding provider.
            model (str, optional): The embedding model name.
            fps (float, optional): The frames per second for video embedding.
        """
        super().__init__(**kwargs)
        self.embedding_provider = embedding_provider
        self.api_key = api_key
        self.model = model
        self.fps = fps


class DataPipelineError(serde.Model):
    """Error configuration for data pipeline."""

    _attribute_map = {
        'error_mode': {'tag': 'xml', 'rename': 'ErrorMode', 'type': 'str'},
        'error_bucket': {'tag': 'xml', 'rename': 'ErrorBucket', 'type': 'str'},
        'error_prefix': {'tag': 'xml', 'rename': 'ErrorPrefix', 'type': 'str'},
    }

    _xml_map = {
        'name': 'DataPipelineError'
    }

    def __init__(
            self,
            error_mode: Optional[str] = None,
            error_bucket: Optional[str] = None,
            error_prefix: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            error_mode (str, optional): The error handling mode.
            error_bucket (str, optional): The bucket for error output.
            error_prefix (str, optional): The prefix for error output.
        """
        super().__init__(**kwargs)
        self.error_mode = error_mode
        self.error_bucket = error_bucket
        self.error_prefix = error_prefix


class DataPipelineConfiguration(serde.Model):
    """Data pipeline configuration."""

    _attribute_map = {
        'data_pipeline_name': {'tag': 'xml', 'rename': 'DataPipelineName', 'type': 'str'},
        'data_pipeline_description': {'tag': 'xml', 'rename': 'DataPipelineDescription', 'type': 'str'},
        'data_pipeline_role': {'tag': 'xml', 'rename': 'DataPipelineRole', 'type': 'str'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'phase': {'tag': 'xml', 'rename': 'Phase', 'type': 'str'},
        'data_pipeline_embedding_configuration': {'tag': 'xml', 'rename': 'DataPipelineEmbeddingConfiguration', 'type': 'DataPipelineEmbeddingConfiguration'},
        'destination': {'tag': 'xml', 'rename': 'Destination', 'type': 'DataPipelineDestination'},
        'data_pipeline_error': {'tag': 'xml', 'rename': 'DataPipelineError', 'type': 'DataPipelineError'},
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'sources': {'tag': 'xml', 'rename': 'Sources', 'type': '[DataPipelineSource]'},
        'model_tier': {'tag': 'xml', 'rename': 'ModelTier', 'type': 'str'},
        'data_pipeline_data_process_configuration': {'tag': 'xml', 'rename': 'DataPipelineDataProcessConfiguration', 'type': 'DataPipelineDataProcessConfiguration'},
    }

    _xml_map = {
        'name': 'DataPipelineConfiguration'
    }

    def __init__(
            self,
            data_pipeline_name: Optional[str] = None,
            data_pipeline_description: Optional[str] = None,
            data_pipeline_role: Optional[str] = None,
            status: Optional[str] = None,
            phase: Optional[str] = None,
            data_pipeline_embedding_configuration: Optional[DataPipelineEmbeddingConfiguration] = None,
            destination: Optional[DataPipelineDestination] = None,
            data_pipeline_error: Optional[DataPipelineError] = None,
            create_time: Optional[str] = None,
            sources: Optional[List[DataPipelineSource]] = None,
            model_tier: Optional[str] = None,
            data_pipeline_data_process_configuration: Optional[DataPipelineDataProcessConfiguration] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_name (str, optional): The name of the data pipeline.
            data_pipeline_description (str, optional): The description of the data pipeline.
            data_pipeline_role (str, optional): The role for the data pipeline.
            status (str, optional): The status of the data pipeline.
            phase (str, optional): The phase of the data pipeline.
            data_pipeline_embedding_configuration (DataPipelineEmbeddingConfiguration, optional): The embedding configuration.
            destination (DataPipelineDestination, optional): The destination configuration.
            data_pipeline_error (DataPipelineError, optional): The error configuration.
            create_time (str, optional): The time when the data pipeline was created.
            sources (List[DataPipelineSource], optional): The list of data sources.
            model_tier (str, optional): The V2 model tier. Currently only standard is supported.
            data_pipeline_data_process_configuration (DataPipelineDataProcessConfiguration, optional): The V2 data process configuration.
        """
        super().__init__(**kwargs)
        self.data_pipeline_name = data_pipeline_name
        self.data_pipeline_description = data_pipeline_description
        self.data_pipeline_role = data_pipeline_role
        self.status = status
        self.phase = phase
        self.data_pipeline_embedding_configuration = data_pipeline_embedding_configuration
        self.destination = destination
        self.data_pipeline_error = data_pipeline_error
        self.create_time = create_time
        self.sources = sources
        self.model_tier = model_tier
        self.data_pipeline_data_process_configuration = data_pipeline_data_process_configuration


class DataPipelineConfigurations(serde.Model):
    """The list of data pipeline configurations."""

    _attribute_map = {
        'data_pipeline_configuration': {'tag': 'xml', 'rename': 'DataPipelineConfiguration', 'type': '[DataPipelineConfiguration]'},
    }

    _xml_map = {
        'name': 'DataPipelineConfigurations'
    }

    def __init__(
            self,
            data_pipeline_configuration: Optional[List[DataPipelineConfiguration]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_configuration (List[DataPipelineConfiguration], optional): The list of data pipeline configurations.
        """
        super().__init__(**kwargs)
        self.data_pipeline_configuration = data_pipeline_configuration


class PutDataPipelineConfigurationConfiguration(serde.Model):
    """The configuration body for the PutDataPipelineConfiguration operation."""

    _attribute_map = {
        'data_pipeline_description': {'tag': 'xml', 'rename': 'DataPipelineDescription', 'type': 'str'},
        'sources': {'tag': 'xml', 'rename': 'Sources', 'type': '[DataPipelineSource]'},
        'data_pipeline_embedding_configuration': {'tag': 'xml', 'rename': 'DataPipelineEmbeddingConfiguration', 'type': 'DataPipelineEmbeddingConfiguration'},
        'destination': {'tag': 'xml', 'rename': 'Destination', 'type': 'DataPipelineDestination'},
        'data_pipeline_error': {'tag': 'xml', 'rename': 'DataPipelineError', 'type': 'DataPipelineError'},
        'model_tier': {'tag': 'xml', 'rename': 'ModelTier', 'type': 'str'},
        'data_pipeline_data_process_configuration': {'tag': 'xml', 'rename': 'DataPipelineDataProcessConfiguration', 'type': 'DataPipelineDataProcessConfiguration'},
    }

    _xml_map = {
        'name': 'DataPipelineConfiguration'
    }

    def __init__(
            self,
            data_pipeline_description: Optional[str] = None,
            sources: Optional[List[DataPipelineSource]] = None,
            data_pipeline_embedding_configuration: Optional[DataPipelineEmbeddingConfiguration] = None,
            destination: Optional[DataPipelineDestination] = None,
            data_pipeline_error: Optional[DataPipelineError] = None,
            model_tier: Optional[str] = None,
            data_pipeline_data_process_configuration: Optional[DataPipelineDataProcessConfiguration] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_description (str, optional): The description of the data pipeline.
            sources (List[DataPipelineSource], optional): The list of data sources.
            data_pipeline_embedding_configuration (DataPipelineEmbeddingConfiguration, optional): The embedding configuration.
            destination (DataPipelineDestination, optional): The destination configuration.
            data_pipeline_error (DataPipelineError, optional): The error information.
            model_tier (str, optional): The V2 model tier. Currently only standard is supported.
            data_pipeline_data_process_configuration (DataPipelineDataProcessConfiguration, optional): The V2 data process configuration.
        """
        super().__init__(**kwargs)
        self.data_pipeline_description = data_pipeline_description
        self.sources = sources
        self.data_pipeline_embedding_configuration = data_pipeline_embedding_configuration
        self.destination = destination
        self.data_pipeline_error = data_pipeline_error
        self.model_tier = model_tier
        self.data_pipeline_data_process_configuration = data_pipeline_data_process_configuration


class PutDataPipelineConfigurationRequest(RequestModel):
    """The request for the PutDataPipelineConfiguration operation."""

    _attribute_map = {
        'data_pipeline_name': {'tag': 'input', 'position': 'query', 'rename': 'dataPipelineName', 'type': 'str'},
        'role': {'tag': 'input', 'position': 'query', 'rename': 'role', 'type': 'str'},
    }

    def __init__(
            self,
            data_pipeline_name: Optional[str] = None,
            role: Optional[str] = None,
            configuration: Optional[PutDataPipelineConfigurationConfiguration] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_name (str, optional): The name of the data pipeline.
            role (str, optional): The role for the data pipeline.
            configuration (PutDataPipelineConfigurationConfiguration, optional): The configuration body.
        """
        super().__init__(**kwargs)
        self.data_pipeline_name = data_pipeline_name
        self.role = role
        self.configuration = configuration


class PutDataPipelineConfigurationResult(serde.ResultModel):
    """The result for the PutDataPipelineConfiguration operation."""
    pass


class GetDataPipelineConfigurationRequest(RequestModel):
    """The request for the GetDataPipelineConfiguration operation."""

    _attribute_map = {
        'data_pipeline_name': {'tag': 'input', 'position': 'query', 'rename': 'dataPipelineName', 'type': 'str'},
    }

    def __init__(
            self,
            data_pipeline_name: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_name (str, optional): The name of the data pipeline.
        """
        super().__init__(**kwargs)
        self.data_pipeline_name = data_pipeline_name


class GetDataPipelineConfigurationResult(serde.ResultModel):
    """The result for the GetDataPipelineConfiguration operation."""

    _attribute_map = {
        'configuration': {'tag': 'output', 'position': 'body', 'rename': 'DataPipelineConfiguration', 'type': 'DataPipelineConfiguration,xml'},
    }

    def __init__(
            self,
            configuration: Optional[DataPipelineConfiguration] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            configuration (DataPipelineConfiguration, optional): The data pipeline configuration.
        """
        super().__init__(**kwargs)
        self.configuration = configuration


class DeleteDataPipelineConfigurationRequest(RequestModel):
    """The request for the DeleteDataPipelineConfiguration operation."""

    _attribute_map = {
        'data_pipeline_name': {'tag': 'input', 'position': 'query', 'rename': 'dataPipelineName', 'type': 'str'},
    }

    def __init__(
            self,
            data_pipeline_name: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_name (str, optional): The name of the data pipeline to delete.
        """
        super().__init__(**kwargs)
        self.data_pipeline_name = data_pipeline_name


class DeleteDataPipelineConfigurationResult(serde.ResultModel):
    """The result for the DeleteDataPipelineConfiguration operation."""
    pass


class ListDataPipelineConfigurationsRequest(RequestModel):
    """The request for the ListDataPipelineConfigurations operation."""

    _attribute_map = {
        'max_results': {'tag': 'input', 'position': 'query', 'rename': 'maxResults', 'type': 'int'},
        'prefix': {'tag': 'input', 'position': 'query', 'rename': 'prefix', 'type': 'str'},
        'next_token': {'tag': 'input', 'position': 'query', 'rename': 'nextToken', 'type': 'str'},
        'input_bucket': {'tag': 'input', 'position': 'query', 'rename': 'inputBucket', 'type': 'str'},
    }

    def __init__(
            self,
            max_results: Optional[int] = None,
            prefix: Optional[str] = None,
            next_token: Optional[str] = None,
            input_bucket: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            max_results (int, optional): The maximum number of results to return.
            prefix (str, optional): The prefix filter for data pipeline names.
            next_token (str, optional): The token for the next page of results.
            input_bucket (str, optional): The source bucket name used to filter data pipelines.
        """
        super().__init__(**kwargs)
        self.max_results = max_results
        self.prefix = prefix
        self.next_token = next_token
        self.input_bucket = input_bucket


class ListDataPipelineConfigurationsResponseBody(serde.Model):
    """The response body for the ListDataPipelineConfigurations operation."""

    _attribute_map = {
        'data_pipeline_configurations': {'tag': 'xml', 'rename': 'DataPipelineConfigurations', 'type': 'DataPipelineConfigurations'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ListDataPipelineConfigurationsResult'
    }

    def __init__(
            self,
            data_pipeline_configurations: Optional[DataPipelineConfigurations] = None,
            next_token: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_configurations (DataPipelineConfigurations, optional): The list of data pipeline configurations.
            next_token (str, optional): The token for the next page of results.
        """
        super().__init__(**kwargs)
        self.data_pipeline_configurations = data_pipeline_configurations
        self.next_token = next_token


class ListDataPipelineConfigurationsResult(serde.ResultModel):
    """The result for the ListDataPipelineConfigurations operation."""

    _attribute_map = {
        'data_pipeline_configurations': {'tag': 'xml', 'rename': 'DataPipelineConfigurations', 'type': 'DataPipelineConfigurations'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ListDataPipelineConfigurationsResult'
    }

    def __init__(
            self,
            data_pipeline_configurations: Optional[DataPipelineConfigurations] = None,
            next_token: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_configurations (DataPipelineConfigurations, optional): The list of data pipeline configurations.
            next_token (str, optional): The token for the next page of results.
        """
        super().__init__(**kwargs)
        self.data_pipeline_configurations = data_pipeline_configurations
        self.next_token = next_token


class PauseDataPipelineRequest(RequestModel):
    """The request for the PauseDataPipeline operation."""

    _attribute_map = {
        'data_pipeline_name': {'tag': 'input', 'position': 'query', 'rename': 'dataPipelineName', 'type': 'str'},
    }

    def __init__(
            self,
            data_pipeline_name: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_name (str, optional): The name of the data pipeline to pause.
        """
        super().__init__(**kwargs)
        self.data_pipeline_name = data_pipeline_name


class PauseDataPipelineResult(serde.ResultModel):
    """The result for the PauseDataPipeline operation."""
    pass


class RestartDataPipelineRequest(RequestModel):
    """The request for the RestartDataPipeline operation."""

    _attribute_map = {
        'data_pipeline_name': {'tag': 'input', 'position': 'query', 'rename': 'dataPipelineName', 'type': 'str'},
    }

    def __init__(
            self,
            data_pipeline_name: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data_pipeline_name (str, optional): The name of the data pipeline to restart.
        """
        super().__init__(**kwargs)
        self.data_pipeline_name = data_pipeline_name


class RestartDataPipelineResult(serde.ResultModel):
    """The result for the RestartDataPipeline operation."""
    pass
