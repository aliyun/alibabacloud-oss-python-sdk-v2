from typing import Optional, List, Any, Dict
from alibabacloud_oss_v2 import serde


class VectorData(serde.Model):
    """
    The container that stores vector data.
    """

    _attribute_map = {
        'float32': {'tag': 'xml', 'rename': 'float32', 'type': '[float]'},
    }

    def __init__(
            self,
            float32: Optional[List[float]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            float32 (List[float], optional): The float32 vector data.
        """
        super().__init__(**kwargs)
        self.float32 = float32


class Vector(serde.Model):
    """
    The container that stores vector information.
    """

    _attribute_map = {
        'data': {'tag': 'xml', 'rename': 'data', 'type': 'VectorData'},
        'key': {'tag': 'xml', 'rename': 'key', 'type': 'str'},
        'metadata': {'tag': 'xml', 'rename': 'metadata', 'type': 'dict'},
    }

    def __init__(
            self,
            data: Optional[VectorData] = None,
            key: Optional[str] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            data (VectorData, optional): The vector data.
            key (str, optional): The vector key.
            metadata (Dict[str, Any], optional): The metadata as key-value pairs.
        """
        super().__init__(**kwargs)
        self.data = data
        self.key = key
        self.metadata = metadata


class QueryVector(serde.Model):
    """
    The container that stores query result vector information.
    """

    _attribute_map = {
        'data': {'tag': 'xml', 'rename': 'data', 'type': 'VectorData'},
        'distance': {'tag': 'xml', 'rename': 'distance', 'type': 'float'},
        'key': {'tag': 'xml', 'rename': 'key', 'type': 'str'},
        'metadata': {'tag': 'xml', 'rename': 'metadata', 'type': 'dict'},
    }

    _dependency_map = {
        'VectorData': {'new': lambda: VectorData()},
    }

    def __init__(
        self,
        data: Optional[VectorData] = None,
        distance: Optional[float] = None,
        key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            data (VectorData, optional): The vector data.
            distance (float, optional): The distance value.
            key (str, optional): The vector key.
            metadata (Dict[str, Any], optional): The metadata as key-value pairs.
        """
        super().__init__(**kwargs)
        self.data = data
        self.distance = distance
        self.key = key
        self.metadata = metadata



class PutVectorsRequest(serde.RequestModel):
    """
    The request for the PutVectors operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'vectors': {'tag': 'input', 'position': 'body', 'rename': 'vectors', 'type': '[Vector,json]'},
    }

    _dependency_map = {
        'Vector': {'new': lambda: Vector()},
        'VectorData': {'new': lambda: VectorData()},
    }

    def __init__(
            self,
            bucket: Optional[str] = None,
            index_name: Optional[str] = None,
            vectors: Optional[List[Vector]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            index_name (str, optional): The name of the index.
            vectors (List[Vector], optional): The list of vectors to put.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name
        self.vectors = vectors


class PutVectorsResult(serde.ResultModel):
    """
    The result for the PutVectors operation.
    """

    # Empty result class as no specific fields are defined in the structure
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)



class GetVectorsRequest(serde.RequestModel):
    """
    The request for the GetVectors operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'keys': {'tag': 'input', 'position': 'body', 'rename': 'keys', 'type': '[str]'},
        'return_data': {'tag': 'input', 'position': 'body', 'rename': 'returnData', 'type': 'bool'},
        'return_metadata': {'tag': 'input', 'position': 'body', 'rename': 'returnMetadata', 'type': 'bool'},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        index_name: Optional[str] = None,
        keys: Optional[List[str]] = None,
        return_data: Optional[bool] = None,
        return_metadata: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            index_name (str, optional): The name of the index.
            keys (List[str], optional): The list of vector keys to retrieve.
            return_data (bool, optional): Whether to return vector data.
            return_metadata (bool, optional): Whether to return vector metadata.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name
        self.keys = keys
        self.return_data = return_data
        self.return_metadata = return_metadata


class GetVectorsResult(serde.ResultModel):
    """
    The result for the GetVectors operation.
    """

    _attribute_map = {
        'vectors': {'tag': 'output', 'position': 'body', 'rename': 'vectors', 'type': '[Vector,json]'},
    }

    _dependency_map = {
        'Vector': {'new': lambda: Vector()},
        'VectorData': {'new': lambda: VectorData()},
    }

    def __init__(
        self,
        vectors: Optional[List[Vector]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            vectors (List[Vector], optional): The list of vectors retrieved.
        """
        super().__init__(**kwargs)
        self.vectors = vectors



class ListVectorsRequest(serde.RequestModel):
    """
    The request for the ListVectors operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'max_results': {'tag': 'input', 'position': 'body', 'rename': 'maxResults', 'type': 'int'},
        'next_token': {'tag': 'input', 'position': 'body', 'rename': 'nextToken', 'type': 'str'},
        'return_data': {'tag': 'input', 'position': 'body', 'rename': 'returnData', 'type': 'bool'},
        'return_metadata': {'tag': 'input', 'position': 'body', 'rename': 'returnMetadata', 'type': 'bool'},
        'segment_count': {'tag': 'input', 'position': 'body', 'rename': 'segmentCount', 'type': 'int'},
        'segment_index': {'tag': 'input', 'position': 'body', 'rename': 'segmentIndex', 'type': 'int'},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        index_name: Optional[str] = None,
        max_results: Optional[int] = None,
        next_token: Optional[str] = None,
        return_data: Optional[bool] = None,
        return_metadata: Optional[bool] = None,
        segment_count: Optional[int] = None,
        segment_index: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            index_name (str, optional): The name of the index.
            max_results (int, optional): The maximum number of vectors to return.
            next_token (str, optional): The token for the next page of vectors.
            return_data (bool, optional): Whether to return vector data.
            return_metadata (bool, optional): Whether to return vector metadata.
            segment_count (int, optional): Number of concurrent segments.
            segment_index (int, optional): Current segment index.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name
        self.max_results = max_results
        self.next_token = next_token
        self.return_data = return_data
        self.return_metadata = return_metadata
        self.segment_count = segment_count
        self.segment_index = segment_index


class ListVectorsResult(serde.ResultModel):
    """
    The result for the ListVectors operation.
    """

    _attribute_map = {
        'next_token': {'tag': 'output', 'position': 'body', 'rename': 'nextToken', 'type': 'str'},
        'vectors': {'tag': 'output', 'position': 'body', 'rename': 'vectors', 'type': '[Vector,json]'},
    }

    _dependency_map = {
        'Vector': {'new': lambda: Vector()},
        'VectorData': {'new': lambda: VectorData()},
    }

    def __init__(
        self,
        next_token: Optional[str] = None,
        vectors: Optional[List[Vector]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            next_token (str, optional): The token for the next page of vectors.
            vectors (List[Vector], optional): The list of vectors retrieved.
        """
        super().__init__(**kwargs)
        self.next_token = next_token
        self.vectors = vectors



class DeleteVectorsRequest(serde.RequestModel):
    """
    The request for the DeleteVectors operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'keys': {'tag': 'input', 'position': 'body', 'rename': 'keys', 'type': '[str]'},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        index_name: Optional[str] = None,
        keys: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            index_name (str, optional): The name of the index.
            keys (List[str], optional): The list of vector keys to delete.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name
        self.keys = keys


class DeleteVectorsResult(serde.ResultModel):
    """
    The result for the DeleteVectors operation.
    """



class QueryVectorsRequest(serde.RequestModel):
    """
    The request for the QueryVectors operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str'},
        'filter': {'tag': 'input', 'position': 'body', 'rename': 'filter', 'type': 'dict'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'query_vector': {'tag': 'input', 'position': 'body', 'rename': 'queryVector', 'type': 'VectorData,json'},
        'return_distance': {'tag': 'input', 'position': 'body', 'rename': 'returnDistance', 'type': 'bool'},
        'return_metadata': {'tag': 'input', 'position': 'body', 'rename': 'returnMetadata', 'type': 'bool'},
        'top_k': {'tag': 'input', 'position': 'body', 'rename': 'topK', 'type': 'int'},
    }

    _dependency_map = {
        'VectorData': {'new': lambda: VectorData()},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        index_name: Optional[str] = None,
        query_vector: Optional[VectorData] = None,
        return_distance: Optional[bool] = None,
        return_metadata: Optional[bool] = None,
        top_k: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            filter (Dict[str, Any], optional): The filter conditions for querying vectors.
            index_name (str, optional): The name of the index.
            query_vector (VectorData, optional): The query vector data.
            return_distance (bool, optional): Whether to return distance values.
            return_metadata (bool, optional): Whether to return vector metadata.
            top_k (int, optional): The number of nearest neighbors to return.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.filter = filter
        self.index_name = index_name
        self.query_vector = query_vector
        self.return_distance = return_distance
        self.return_metadata = return_metadata
        self.top_k = top_k


class QueryVectorsResult(serde.ResultModel):
    """
    The result for the QueryVectors operation.
    """

    _attribute_map = {
        'vectors': {'tag': 'output', 'position': 'body', 'rename': 'vectors', 'type': '[QueryVector,json]'},
    }

    _dependency_map = {
        'QueryVector': {'new': lambda: QueryVector()},
        'VectorData': {'new': lambda: VectorData()},
    }

    def __init__(
        self,
        vectors: Optional[List[QueryVector]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            vectors (List[QueryVector], optional): The list of query result vectors.
        """
        super().__init__(**kwargs)
        self.vectors = vectors

