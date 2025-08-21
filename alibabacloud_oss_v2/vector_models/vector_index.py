import datetime
from typing import Optional, List, Any
from alibabacloud_oss_v2 import serde


class VectorMetadata(serde.Model):
    """
    The container that stores metadata configuration.
    """

    _attribute_map = {
        'non_filterable_metadata_keys': {'tag': 'json', 'rename': 'nonFilterableMetadataKeys', 'type': '[str]'},
    }

    _json_map = {
        'name': 'metadata'
    }

    def __init__(
        self,
        non_filterable_metadata_keys: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            non_filterable_metadata_keys (List[str], optional): List of metadata keys that are not filterable.
        """
        super().__init__(**kwargs)
        self.non_filterable_metadata_keys = non_filterable_metadata_keys


class VectorIndexInfo(serde.Model):
    """
    The container that stores vector index information.
    """

    _attribute_map = {
        'create_time': {'tag': 'json', 'rename': 'createTime', 'type': 'datetime'},
        'data_type': {'tag': 'json', 'rename': 'dataType', 'type': 'str'},
        'dimension': {'tag': 'json', 'rename': 'dimension', 'type': 'int'},
        'distance_metric': {'tag': 'json', 'rename': 'distanceMetric', 'type': 'str'},
        'index_name': {'tag': 'json', 'rename': 'indexName', 'type': 'str'},
        'metadata': {'tag': 'json', 'rename': 'metadata', 'type': 'VectorMetadata'},
        'status': {'tag': 'json', 'rename': 'status', 'type': 'str'},
    }

    _json_map = {
        'name': 'index'
    }

    def __init__(
        self,
        create_time: Optional[datetime.datetime] = None,
        data_type: Optional[str] = None,
        dimension: Optional[int] = None,
        distance_metric: Optional[str] = None,
        index_name: Optional[str] = None,
        metadata: Optional[VectorMetadata] = None,
        status: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            create_time (datetime, optional): The creation time of the index.
            data_type (str, optional): The type of data for the vector index.
            dimension (int, optional): The dimension of the vector data.
            distance_metric (str, optional): The distance measurement function.
            index_name (str, optional): The name of the index.
            metadata (VectorMetadata, optional): The metadata configuration.
            status (str, optional): The status of the index.
        """
        super().__init__(**kwargs)
        self.create_time = create_time
        self.data_type = data_type
        self.dimension = dimension
        self.distance_metric = distance_metric
        self.index_name = index_name
        self.metadata = metadata
        self.status = status


class VectorIndexSummary(serde.Model):
    """
    The container that stores summary information for a vector index.
    """

    _attribute_map = {
        'create_time': {'tag': 'json', 'rename': 'createTime', 'type': 'datetime'},
        'index_name': {'tag': 'json', 'rename': 'indexName', 'type': 'str'},
        'data_type': {'tag': 'json', 'rename': 'dataType', 'type': 'str'},
        'dimension': {'tag': 'json', 'rename': 'dimension', 'type': 'int'},
        'distance_metric': {'tag': 'json', 'rename': 'distanceMetric', 'type': 'str'},
        'metadata': {'tag': 'json', 'rename': 'metadata', 'type': 'VectorMetadata'},
        'vector_bucket_name': {'tag': 'json', 'rename': 'vectorBucketName', 'type': 'str'},
        'status': {'tag': 'json', 'rename': 'status', 'type': 'str'},
    }

    def __init__(
        self,
        create_time: Optional[datetime.datetime] = None,
        index_name: Optional[str] = None,
        data_type: Optional[str] = None,
        dimension: Optional[int] = None,
        distance_metric: Optional[str] = None,
        metadata: Optional[VectorMetadata] = None,
        vector_bucket_name: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            create_time (datetime, optional): The creation time of the index.
            index_name (str, optional): The name of the index.
            data_type (str, optional): The type of data for the vector index.
            dimension (int, optional): The dimension of the vector data.
            distance_metric (str, optional): The distance measurement function.
            metadata (VectorMetadata, optional): The metadata configuration.
            vector_bucket_name (str, optional): The name of the vector bucket.
            status (str, optional): The status of the index.
        """
        super().__init__(**kwargs)
        self.create_time = create_time
        self.index_name = index_name
        self.data_type = data_type
        self.dimension = dimension
        self.distance_metric = distance_metric
        self.metadata = metadata
        self.vector_bucket_name = vector_bucket_name
        self.status = status


# Put
class PutVectorIndexRequest(serde.RequestModel):
    """
    The request for the vector index operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str'},
        'data_type': {'tag': 'input', 'position': 'body', 'rename': 'dataType', 'type': 'str'},
        'dimension': {'tag': 'input', 'position': 'body', 'rename': 'dimension', 'type': 'int'},
        'distance_metric': {'tag': 'input', 'position': 'body', 'rename': 'distanceMetric', 'type': 'str'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'metadata': {'tag': 'input', 'position': 'body', 'rename': 'metadata', 'type': 'VectorMetadata'},
    }

    _dependency_map = {
        'Metadata': {'new': lambda: VectorMetadata()},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        data_type: Optional[str] = None,
        dimension: Optional[int] = None,
        distance_metric: Optional[str] = None,
        index_name: Optional[str] = None,
        metadata: Optional[VectorMetadata] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            data_type (str, optional): The type of data for the vector index.
            dimension (int, optional): The dimension of the vector data.
            distance_metric (str, optional): The distance measurement function has the following optional values:
                Euclidean distance: Euclidean distance
                Cosine: cosine distance
            index_name (str, optional): The name of the index.
            metadata (VectorMetadata, optional): The metadata configuration.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.data_type = data_type
        self.dimension = dimension
        self.distance_metric = distance_metric
        self.index_name = index_name
        self.metadata = metadata


class PutVectorIndexResult(serde.ResultModel):
    """
    The result for the PutVectorIndex operation.
    """


# Get
class GetVectorIndexRequest(serde.RequestModel):
    """
    The request for the GetVectorIndex operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        index_name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            index_name (str, optional): The name of the index.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name


class GetVectorIndexResult(serde.ResultModel):
    """
    The result for the GetVectorIndex operation.
    """

    _attribute_map = {
        'index': {'tag': 'output', 'position': 'body', 'rename': 'index', 'type': 'VectorIndexInfo,json'},
        'vector_bucket_name': {'tag': 'output', 'position': 'body', 'rename': 'vectorBucketName', 'type': 'str'},
    }

    _dependency_map = {
        'VectorIndexInfo': {'new': lambda: VectorIndexInfo()},
        'Metadata': {'new': lambda: VectorMetadata()},
    }

    def __init__(
        self,
        index: Optional[VectorIndexInfo] = None,
        vector_bucket_name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            index (VectorIndexInfo, optional): The vector index information.
            vector_bucket_name (str, optional): The name of the vector bucket.
        """
        super().__init__(**kwargs)
        self.index = index
        self.vector_bucket_name = vector_bucket_name


# List
class ListVectorsIndexRequest(serde.RequestModel):
    """
    The request for the ListVectorsIndex operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str'},
        'max_results': {'tag': 'input', 'position': 'body', 'rename': 'maxResults', 'type': 'int'},
        'next_token': {'tag': 'input', 'position': 'body', 'rename': 'nextToken', 'type': 'str'},
        'prefix': {'tag': 'input', 'position': 'body', 'rename': 'prefix', 'type': 'str'},
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
            max_results (int, optional): The maximum number of indexes to return.
            next_token (str, optional): The token for the next page of indexes.
            prefix (str, optional): The prefix to filter indexes by name.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.max_results = max_results
        self.next_token = next_token
        self.prefix = prefix


class ListVectorsIndexResult(serde.ResultModel):
    """
    The result for the ListVectorsIndex operation.
    """

    _attribute_map = {
        'indexes': {'tag': 'output', 'position': 'body', 'rename': 'indexes', 'type': '[VectorIndexSummary,json]'},
        'next_token': {'tag': 'output', 'position': 'body', 'rename': 'nextToken', 'type': 'str'},
    }

    _dependency_map = {
        'VectorIndexSummary': {'new': lambda: VectorIndexSummary()},
        'Metadata': {'new': lambda: VectorMetadata()},
    }

    def __init__(
        self,
        indexes: Optional[List[VectorIndexSummary]] = None,
        next_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            indexes (List[VectorIndexSummary], optional): The list of vector index summaries.
            next_token (str, optional): The token for the next page of indexes.
        """
        super().__init__(**kwargs)
        self.indexes = indexes
        self.next_token = next_token


# Delete
class DeleteVectorIndexRequest(serde.RequestModel):
    """
    The request for the DeleteVectorIndex operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        index_name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            index_name (str, optional): The name of the index to delete.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name


class DeleteVectorIndexResult(serde.ResultModel):
    """
    The result for the DeleteVectorIndex operation.
    """
