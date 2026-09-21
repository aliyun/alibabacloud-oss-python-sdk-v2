from typing import Optional, Any, Dict
from ... import serde


class PutVectorIndexFusionRequest(serde.RequestModel):
    """
    The request for the PutVectorIndexFusion operation.

    Creates a fusion index. A fusion index is described by a schema covering
    every field of the index, instead of the single vector field that
    PutVectorIndex configures.

    The schema is a plain dict rather than a typed model on purpose:

    - serde.Model silently drops every constructor keyword argument that is
      not listed in _attribute_map, so a typed schema would not report a
      misspelled property, it would just send a smaller schema and let the
      service complain about a missing field instead.
    - the JSON serializer of this module hands body values straight to
      json.dumps, which cannot encode a nested Model.
    - a dict also carries properties a future service version adds, without
      waiting for an SDK release.

    The wire format looks like this, an e-commerce product index carrying two
    vector fields, scalar filter fields and a tokenized title::

        {
            "fields": [
                {
                    "name": "text_vector",
                    "type": "vector",
                    "dataType": "float32",
                    "dimension": 768,
                    "distanceMetric": "euclidean"
                },
                {
                    "name": "image_vector",
                    "type": "vector",
                    "dataType": "float32",
                    "dimension": 512,
                    "distanceMetric": "euclidean"
                },
                {
                    "name": "title",
                    "type": "string",
                    "exactMatch": True,
                    "text": {
                        "enabled": True,
                        "analyzer": "standard"
                    }
                },
                {
                    "name": "brand",
                    "type": "string"
                },
                {
                    "name": "price",
                    "type": "double"
                },
                {
                    "name": "on_sale",
                    "type": "bool"
                }
            ]
        }

    A text field defaults to the "standard" analyzer, English by word and
    Chinese by single character. The other built-in analyzer is "split", which
    cuts on a business delimiter and requires a "delimiter" inside
    "analyzerParameters". Write booleans out explicitly whenever false is what
    you mean. An omitted property and a property set to false are not the same
    thing to the service, so exactMatch=False and text.enabled=False both have
    to appear in the dict to take effect.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str', 'required': True},
        'mode': {'tag': 'input', 'position': 'body', 'rename': 'mode', 'type': 'str'},
        'schema_configuration': {'tag': 'input', 'position': 'body', 'rename': 'schemaConfiguration', 'type': 'dict', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        index_name: Optional[str] = None,
        mode: Optional[str] = 'fusion',
        schema_configuration: Optional[Dict] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            index_name (str, required): The name of the fusion index.
            mode (str, optional): The mode of the index. Defaults to "fusion".
            schema_configuration (Dict, required): The schema of the fusion
                index, a dict holding a "fields" list. See the class
                docstring for the shape of every field entry.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name
        self.mode = mode
        self.schema_configuration = schema_configuration


class PutVectorIndexFusionResult(serde.ResultModel):
    """
    The result for the PutVectorIndexFusion operation.
    """
