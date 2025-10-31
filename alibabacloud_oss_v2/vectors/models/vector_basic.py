from typing import Optional, List, Any, Dict
from ... import serde

class PutVectorsRequest(serde.RequestModel):
    """
    The request for the PutVectors operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str', 'required': True},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'vectors': {'tag': 'input', 'position': 'body', 'rename': 'vectors', 'type': '[dict]'},
    }

    def __init__(
            self,
            bucket: str = None,
            index_name: Optional[str] = None,
            vectors: Optional[List[Dict]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            index_name (str, optional): The name of the index.
            vectors (List[Dict], optional): The list of vectors to put.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name
        self.vectors = vectors


class PutVectorsResult(serde.ResultModel):
    """
    The result for the PutVectors operation.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)



class GetVectorsRequest(serde.RequestModel):
    """
    The request for the GetVectors operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str', 'required': True},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'keys': {'tag': 'input', 'position': 'body', 'rename': 'keys', 'type': '[str]'},
        'return_data': {'tag': 'input', 'position': 'body', 'rename': 'returnData', 'type': 'bool'},
        'return_metadata': {'tag': 'input', 'position': 'body', 'rename': 'returnMetadata', 'type': 'bool'},
    }

    def __init__(
        self,
        bucket: str = None,
        index_name: Optional[str] = None,
        keys: Optional[List[str]] = None,
        return_data: Optional[bool] = None,
        return_metadata: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
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
        'vectors': {'tag': 'output', 'position': 'body', 'rename': 'vectors', 'type': '[dict]'},
    }

    def __init__(
        self,
        vectors: Optional[List[Dict]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            vectors (List[Dict], optional): The list of vectors retrieved.
        """
        super().__init__(**kwargs)
        self.vectors = vectors



class ListVectorsRequest(serde.RequestModel):
    """
    The request for the ListVectors operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str', 'required': True},
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
        bucket: str = None,
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
            bucket (str, required): The name of the bucket.
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
        'vectors': {'tag': 'output', 'position': 'body', 'rename': 'vectors', 'type': '[dict]'},
    }

    def __init__(
        self,
        next_token: Optional[str] = None,
        vectors: Optional[List[Dict]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            next_token (str, optional): The token for the next page of vectors.
            vectors (List[Dict], optional): The list of vectors retrieved.
        """
        super().__init__(**kwargs)
        self.next_token = next_token
        self.vectors = vectors



class DeleteVectorsRequest(serde.RequestModel):
    """
    The request for the DeleteVectors operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str', 'required': True},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'keys': {'tag': 'input', 'position': 'body', 'rename': 'keys', 'type': '[str]'},
    }

    def __init__(
        self,
        bucket: str = None,
        index_name: Optional[str] = None,
        keys: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
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
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str', 'required': True},
        'filter': {'tag': 'input', 'position': 'body', 'rename': 'filter', 'type': 'dict'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'query_vector': {'tag': 'input', 'position': 'body', 'rename': 'queryVector', 'type': 'dict'},
        'return_distance': {'tag': 'input', 'position': 'body', 'rename': 'returnDistance', 'type': 'bool'},
        'return_metadata': {'tag': 'input', 'position': 'body', 'rename': 'returnMetadata', 'type': 'bool'},
        'top_k': {'tag': 'input', 'position': 'body', 'rename': 'topK', 'type': 'int'},
    }

    def __init__(
        self,
        bucket: str = None,
        filter: Optional[Dict] = None,
        index_name: Optional[str] = None,
        query_vector: Optional[Dict] = None,
        return_distance: Optional[bool] = None,
        return_metadata: Optional[bool] = None,
        top_k: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            filter (Dict, optional): The filter conditions for querying vectors.
            index_name (str, optional): The name of the index.
            query_vector (Dict, optional): The query vector data.
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
        'vectors': {'tag': 'output', 'position': 'body', 'rename': 'vectors', 'type': '[dict]'},
    }

    def __init__(
        self,
        vectors: Optional[List[Dict]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            vectors (List[Dict], optional): The list of query result vectors.
        """
        super().__init__(**kwargs)
        self.vectors = vectors

