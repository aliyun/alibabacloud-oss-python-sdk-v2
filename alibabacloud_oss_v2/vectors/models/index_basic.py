import datetime
from typing import Optional, List, Any, Dict
from ... import serde


# Put
class PutVectorIndexRequest(serde.RequestModel):
    """
    The request for the vector index operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'data_type': {'tag': 'input', 'position': 'body', 'rename': 'dataType', 'type': 'str'},
        'dimension': {'tag': 'input', 'position': 'body', 'rename': 'dimension', 'type': 'int'},
        'distance_metric': {'tag': 'input', 'position': 'body', 'rename': 'distanceMetric', 'type': 'str'},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
        'metadata': {'tag': 'input', 'position': 'body', 'rename': 'metadata', 'type': 'dict'},
    }


    def __init__(
        self,
        bucket: str = None,
        data_type: Optional[str] = None,
        dimension: Optional[int] = None,
        distance_metric: Optional[str] = None,
        index_name: Optional[str] = None,
        metadata: Optional[Dict] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            data_type (str, optional): The type of data for the vector index.
            dimension (int, optional): The dimension of the vector data.
            distance_metric (str, optional): The distance measurement function has the following optional values:
                Euclidean distance: Euclidean distance
                Cosine: cosine distance
            index_name (str, optional): The name of the index.
            metadata (Dict, optional): The metadata configuration.
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
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str', "required": True},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        index_name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
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
        'index': {'tag': 'output', 'position': 'body', 'rename': 'index', 'type': 'dict'},
    }


    def __init__(
        self,
        index: Optional[Dict] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            index (Dict, optional): The vector index information.
        """
        super().__init__(**kwargs)
        self.index = index


# List
class ListVectorIndexesRequest(serde.RequestModel):
    """
    The request for the ListVectorIndexes operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str', "required": True},
        'max_results': {'tag': 'input', 'position': 'body', 'rename': 'maxResults', 'type': 'int'},
        'next_token': {'tag': 'input', 'position': 'body', 'rename': 'nextToken', 'type': 'str'},
        'prefix': {'tag': 'input', 'position': 'body', 'rename': 'prefix', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        max_results: Optional[int] = None,
        next_token: Optional[str] = None,
        prefix: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            max_results (int, optional): The maximum number of indexes to return.
            next_token (str, optional): The token for the next page of indexes.
            prefix (str, optional): The prefix to filter indexes by name.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.max_results = max_results
        self.next_token = next_token
        self.prefix = prefix


class ListVectorIndexesResult(serde.ResultModel):
    """
    The result for the ListVectorIndexes operation.
    """

    _attribute_map = {
        'indexes': {'tag': 'output', 'position': 'body', 'rename': 'indexes', 'type': '[dict]'},
        'next_token': {'tag': 'output', 'position': 'body', 'rename': 'nextToken', 'type': 'str'},
    }


    def __init__(
        self,
        indexes: Optional[List[Dict]] = None,
        next_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            indexes (List[Dict], optional): The list of vector index summaries.
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
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str', "required": True},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        index_name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            index_name (str, optional): The name of the index to delete.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name


class DeleteVectorIndexResult(serde.ResultModel):
    """
    The result for the DeleteVectorIndex operation.
    """
