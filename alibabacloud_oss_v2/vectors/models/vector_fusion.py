from typing import Optional, List, Any, Dict
from ... import serde


class QueryVectorsFusionRequest(serde.RequestModel):
    """
    The request for the QueryVectorsFusion operation.

    Queries a fusion index. On top of the nearest neighbour search that
    QueryVectors offers, this operation also carries scalar and full text
    query expressions, several retrievers combined into one ranked result,
    and an explicit sort order.

    knn, query, retriever and sort are plain dicts and lists for the same
    reasons given in PutVectorIndexFusionRequest: the query expression uses
    dynamic field names, dynamic operator names and recursive nesting, so a
    fully typed expression tree would be large and would lag behind every
    change of the syntax.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'path', 'rename': 'bucket', 'type': 'str', 'required': True},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str', 'required': True},
        'knn': {'tag': 'input', 'position': 'body', 'rename': 'knn', 'type': 'any'},
        'limit': {'tag': 'input', 'position': 'body', 'rename': 'limit', 'type': 'int'},
        'next_token': {'tag': 'input', 'position': 'body', 'rename': 'nextToken', 'type': 'str'},
        'partition_keys': {'tag': 'input', 'position': 'body', 'rename': 'partitionKeys', 'type': '[str]'},
        'query': {'tag': 'input', 'position': 'body', 'rename': 'query', 'type': 'dict'},
        'retriever': {'tag': 'input', 'position': 'body', 'rename': 'retriever', 'type': 'dict'},
        'return_metadata': {'tag': 'input', 'position': 'body', 'rename': 'returnMetadata', 'type': 'bool'},
        'return_metadata_fields': {'tag': 'input', 'position': 'body', 'rename': 'returnMetadataFields', 'type': '[str]'},
        'sort': {'tag': 'input', 'position': 'body', 'rename': 'sort', 'type': '[dict]'},
    }

    def __init__(
        self,
        bucket: str = None,
        index_name: Optional[str] = None,
        knn: Optional[Any] = None,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        partition_keys: Optional[List[str]] = None,
        query: Optional[Dict] = None,
        retriever: Optional[Dict] = None,
        return_metadata: Optional[bool] = None,
        return_metadata_fields: Optional[List[str]] = None,
        sort: Optional[List[Dict]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            index_name (str, required): The name of the fusion index.
            knn (Any, optional): The nearest neighbour clause. A dict for a
                single query, for example
                {"field": "text_vector", "queryVector": [0.1, 0.2],
                 "topK": 10, "numCandidates": 100}, or a list of such dicts
                for several of them. Both shapes are valid on the wire and
                json.dumps encodes them as an object and an array, so no
                wrapper type is needed. Any other type is rejected before the
                request is signed.
            limit (int, optional): The maximum number of results to return.
            next_token (str, optional): The token for the next page of
                results.
            partition_keys (List[str], optional): The partition keys to
                restrict the query to.
            query (Dict, optional): The scalar or full text query expression.
                A logical operator takes the object form {"$and": {"clauses":
                [...]}}, for example {"$and": {"clauses": [{"category":
                {"$in": {"value": ["phone", "audio"]}}}]}} or {"title":
                {"$textMatch": {"value": "cloud storage"}}}.
            retriever (Dict, optional): A retriever tree. Exactly one of the
                "simple", "knn", "rrf" and "weight" keys is set per node. The
                combining nodes hold a list of components, and each component
                carries a nested "retriever" with its "weight" or "normalizer"
                as a sibling of that key, so a tree can nest as deep as the
                service allows.
            return_metadata (bool, optional): Whether to return metadata with
                every hit.
            return_metadata_fields (List[str], optional): The metadata fields
                to return. None leaves the property out of the body, an empty
                list sends it as []. The serializer of this module skips every
                attribute set to None, so sending an explicit JSON null is not
                expressible and only those two states exist here.
            sort (List[Dict], optional): The sort order. The list order is the
                priority and every entry holds a single field, for example
                [{"_score": {"order": "desc"}}, {"title": {"order": "asc"}}].
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name
        self.knn = knn
        self.limit = limit
        self.next_token = next_token
        self.partition_keys = partition_keys
        self.query = query
        self.retriever = retriever
        self.return_metadata = return_metadata
        self.return_metadata_fields = return_metadata_fields
        self.sort = sort


class QueryVectorsFusionResult(serde.ResultModel):
    """
    The result for the QueryVectorsFusion operation.

    Every entry of vectors is a dict holding "key", "metadata" and "score".
    The score belongs to this result only. QueryVectorsResult keeps reporting
    "distance", and the two meanings are never mixed, so code reading a
    standard query result is unaffected by this operation.
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
            next_token (str, optional): The token for the next page of
                results.
            vectors (List[Dict], optional): The query hits, each holding
                "key", "metadata" and "score".
        """
        super().__init__(**kwargs)
        self.next_token = next_token
        self.vectors = vectors
