# pylint: skip-file

import json
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.vectors.operations import _serde
from alibabacloud_oss_v2.vectors.models import index_basic as index_model
from alibabacloud_oss_v2.vectors.models import vector_basic as vector_model
from alibabacloud_oss_v2.vectors.models import vector_fusion as model
from alibabacloud_oss_v2.vectors.operations.vector_fusion import _validate_query_vectors_fusion_request
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from ... import MockHttpResponse


class TestQueryVectorsFusion(unittest.TestCase):
    def test_constructor_request(self):
        request = model.QueryVectorsFusionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.index_name)
        self.assertIsNone(request.knn)
        self.assertIsNone(request.limit)
        self.assertIsNone(request.next_token)
        self.assertIsNone(request.partition_keys)
        self.assertIsNone(request.query)
        self.assertIsNone(request.retriever)
        self.assertIsNone(request.return_metadata)
        self.assertIsNone(request.return_metadata_fields)
        self.assertIsNone(request.sort)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

    def test_constructor_request_with_parameters(self):
        knn = {'field': 'text_vector', 'queryVector': [0.1, 0.2], 'topK': 10}
        query = {'title': {'$textMatch': 'cloud storage'}}
        retriever = {'simple': {'query': query}}
        sort = [{'score': {'order': 'desc'}}]
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            knn=knn,
            limit=10,
            next_token='test-token',
            partition_keys=['2024'],
            query=query,
            retriever=retriever,
            return_metadata=True,
            return_metadata_fields=['title'],
            sort=sort
        )
        self.assertEqual(request.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-fusion-index')
        self.assertEqual(request.knn, knn)
        self.assertEqual(request.limit, 10)
        self.assertEqual(request.next_token, 'test-token')
        self.assertEqual(request.partition_keys, ['2024'])
        self.assertEqual(request.query, query)
        self.assertEqual(request.retriever, retriever)
        self.assertEqual(request.return_metadata, True)
        self.assertEqual(request.return_metadata_fields, ['title'])
        self.assertEqual(request.sort, sort)
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request_minimal(self):
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index'
        )

        json_str = '{"indexName": "test-fusion-index"}'

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'queryVectorsFusion': '',
            },
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'QueryVectorsFusion')
        self.assertEqual(op_input.method, 'POST')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(op_input.headers['Content-Type'], 'application/json')
        self.assertEqual(op_input.parameters['queryVectorsFusion'], '')
        self.assertEqual(json_str, op_input.body.decode())

        # bucket sits in the path, it must never leak into the request body
        self.assertNotIn('bucket', json.loads(op_input.body.decode()))

    def test_serialize_request_knn_object(self):
        # A single nearest neighbour clause is a JSON object on the wire.
        knn = {
            'field': 'text_vector',
            'queryVector': [0.1, 0.2, 0.3, 0.4],
            'topK': 10,
            'numCandidates': 100,
            'boost': 1.5,
            'filter': {'year': {'$gte': 2000}}
        }
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            knn=knn
        )

        json_str = (
            '{"indexName": "test-fusion-index", '
            '"knn": {"field": "text_vector", "queryVector": [0.1, 0.2, 0.3, 0.4], '
            '"topK": 10, "numCandidates": 100, "boost": 1.5, '
            '"filter": {"year": {"$gte": 2000}}}}'
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(json_str, op_input.body.decode())
        self.assertIsInstance(json.loads(op_input.body.decode())['knn'], dict)

    def test_serialize_request_knn_array(self):
        # Several nearest neighbour clauses are a JSON array on the wire. The
        # two shapes share one attribute, json.dumps picks object or array
        # from the Python type, which is why no wrapper type is needed here.
        knn = [
            {'field': 'text_vector', 'queryVector': [0.1, 0.2], 'topK': 10},
            {'field': 'image_vector', 'queryVector': [0.3, 0.4], 'topK': 5}
        ]
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            knn=knn
        )

        json_str = (
            '{"indexName": "test-fusion-index", '
            '"knn": [{"field": "text_vector", "queryVector": [0.1, 0.2], "topK": 10}, '
            '{"field": "image_vector", "queryVector": [0.3, 0.4], "topK": 5}]}'
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(json_str, op_input.body.decode())
        self.assertIsInstance(json.loads(op_input.body.decode())['knn'], list)

    def test_serialize_request_query_dsl(self):
        # The expression uses dynamic field names, dynamic operator names and
        # recursive nesting. All of it travels through as the caller wrote it,
        # the SDK never interprets a key inside query.
        query = {
            '$and': [
                {'type': {'$nin': ['comedy']}},
                {'year': {'$gte': 2000, '$lte': 2024}},
                {'title': {'$textMatch': 'cloud storage'}},
                {'$or': [
                    {'rating': {'$range': {'gte': 5, 'lt': 10}}},
                    {'votes': {'$gt': 100}}
                ]}
            ]
        }
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            query=query
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(query, json.loads(op_input.body.decode())['query'])

    def test_serialize_request_retriever_rrf(self):
        # rrf combines ranked lists. Every component holds a nested retriever,
        # and its weight is a sibling of that key rather than a child of it.
        retriever = {
            'rrf': {
                'components': [
                    {
                        'retriever': {
                            'knn': {'field': 'text_vector', 'queryVector': [0.1, 0.2], 'topK': 10}
                        },
                        'weight': 1
                    },
                    {
                        'retriever': {
                            'simple': {'query': {'title': {'$textMatch': 'cloud storage'}}}
                        },
                        'weight': 2
                    }
                ]
            }
        }
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            retriever=retriever,
            limit=10
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))

        body = json.loads(op_input.body.decode())
        self.assertEqual(retriever, body['retriever'])
        # weight and normalizer stay next to retriever, not inside it
        component = body['retriever']['rrf']['components'][0]
        self.assertEqual(['retriever', 'weight'], list(component.keys()))
        self.assertEqual(1, component['weight'])

    def test_serialize_request_retriever_weight_nested(self):
        # A tree two levels deep, to show the recursion is not capped by the
        # SDK even if the service only supports one level today.
        retriever = {
            'weight': {
                'normalizer': 'arithmetic_mean',
                'components': [
                    {
                        'retriever': {
                            'rrf': {
                                'components': [
                                    {
                                        'retriever': {
                                            'knn': {'field': 'text_vector', 'queryVector': [0.1], 'topK': 3}
                                        },
                                        'weight': 1
                                    },
                                    {
                                        'retriever': {
                                            'knn': {'field': 'image_vector', 'queryVector': [0.2], 'topK': 3}
                                        },
                                        'weight': 1
                                    }
                                ]
                            }
                        },
                        'weight': 3
                    },
                    {
                        'retriever': {
                            'simple': {'query': {'type': {'$nin': ['comedy']}}}
                        },
                        'weight': 1
                    }
                ]
            }
        }
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            retriever=retriever
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))

        body = json.loads(op_input.body.decode())
        self.assertEqual(retriever, body['retriever'])
        inner = body['retriever']['weight']['components'][0]['retriever']['rrf']['components'][1]
        self.assertEqual('image_vector', inner['retriever']['knn']['field'])

    def test_serialize_request_sort(self):
        # The list order is the priority and every entry holds a single field.
        sort = [
            {'score': {'order': 'desc'}},
            {'title': {'order': 'asc'}},
            {'year': {}}
        ]
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            sort=sort
        )

        json_str = (
            '{"indexName": "test-fusion-index", '
            '"sort": [{"score": {"order": "desc"}}, {"title": {"order": "asc"}}, {"year": {}}]}'
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(json_str, op_input.body.decode())
        self.assertEqual(['score', 'title', 'year'],
                         [list(item.keys())[0] for item in json.loads(op_input.body.decode())['sort']])

    def test_serialize_request_return_metadata_fields_states(self):
        # None leaves the property out, an empty list sends []. Sending an
        # explicit JSON null is not expressible, because the serializer of
        # this module skips every attribute set to None.
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            return_metadata_fields=None
        )
        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))
        self.assertEqual('{"indexName": "test-fusion-index"}', op_input.body.decode())
        self.assertNotIn('returnMetadataFields', json.loads(op_input.body.decode()))

        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            return_metadata_fields=[]
        )
        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))
        self.assertEqual('{"indexName": "test-fusion-index", "returnMetadataFields": []}',
                         op_input.body.decode())

        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            return_metadata_fields=['title', 'year']
        )
        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))
        self.assertEqual('{"indexName": "test-fusion-index", "returnMetadataFields": ["title", "year"]}',
                         op_input.body.decode())

    def test_serialize_request_body_key_order(self):
        # The body follows _attribute_map order. Locking it keeps a reorder of
        # that map from silently changing the wire format.
        request = model.QueryVectorsFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            knn={'field': 'text_vector', 'queryVector': [0.1], 'topK': 1},
            limit=1,
            next_token='test-token',
            partition_keys=['2024'],
            query={'type': {'$nin': ['comedy']}},
            retriever={'simple': {'query': {}}},
            return_metadata=True,
            return_metadata_fields=['title'],
            sort=[{'score': {'order': 'desc'}}]
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='QueryVectorsFusion',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(
            ['indexName', 'knn', 'limit', 'nextToken', 'partitionKeys', 'query',
             'retriever', 'returnMetadata', 'returnMetadataFields', 'sort'],
            list(json.loads(op_input.body.decode()).keys()))

    def test_serialize_request_missing_required(self):
        for bucket, index_name, expected in [
            (None, 'test-fusion-index', 'bucket'),
            ('test-bucket', None, 'index_name'),
        ]:
            with self.subTest(field=expected):
                request = model.QueryVectorsFusionRequest(
                    bucket=bucket,
                    index_name=index_name
                )
                with self.assertRaises(exceptions.ParamRequiredError) as cm:
                    _serde.serialize_input_vector_json_model(request, OperationInput(
                        op_name='QueryVectorsFusion',
                        method='POST',
                        bucket=request.bucket
                    ))
                self.assertIn(expected, str(cm.exception))

    def test_validate_knn_shape(self):
        # knn is the one clause whose shape the wire format itself fixes, so
        # it is checked before the request is signed.
        for knn in [
            None,
            {},
            {'field': 'text_vector', 'queryVector': [0.1], 'topK': 1},
            [],
            [{'field': 'text_vector'}, {'field': 'image_vector'}],
        ]:
            with self.subTest(knn=knn):
                request = model.QueryVectorsFusionRequest(
                    bucket='test-bucket',
                    index_name='test-fusion-index',
                    knn=knn
                )
                self.assertIsNone(_validate_query_vectors_fusion_request(request))

    def test_validate_knn_rejects_other_types(self):
        for knn, expected in [
            ('text_vector', 'str'),
            (10, 'int'),
            (1.5, 'float'),
            (True, 'bool'),
            ([{'field': 'text_vector'}, 'image_vector'], 'str'),
            (({'field': 'text_vector'},), 'tuple'),
        ]:
            with self.subTest(knn=knn):
                request = model.QueryVectorsFusionRequest(
                    bucket='test-bucket',
                    index_name='test-fusion-index',
                    knn=knn
                )
                with self.assertRaises(exceptions.ParamInvalidError) as cm:
                    _validate_query_vectors_fusion_request(request)
                self.assertIn('knn', str(cm.exception))
                self.assertIn(expected, str(cm.exception))

    def test_constructor_result(self):
        result = model.QueryVectorsFusionResult()
        self.assertIsNone(result.next_token)
        self.assertIsNone(result.vectors)
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = '''
        {
            "vectors": [
                {
                    "key": "vector-1",
                    "metadata": {"title": "cloud storage", "year": 2024},
                    "score": 0.98
                },
                {
                    "key": "vector-2",
                    "metadata": {"title": "object storage"},
                    "score": 0.75
                }
            ],
            "nextToken": "next-token"
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.QueryVectorsFusionResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.next_token, 'next-token')
        self.assertIsNotNone(result.vectors)
        self.assertEqual(len(result.vectors), 2)
        self.assertEqual(result.vectors[0].get('key'), 'vector-1')
        self.assertEqual(result.vectors[0].get('score'), 0.98)
        self.assertEqual(result.vectors[0].get('metadata').get('title'), 'cloud storage')
        self.assertEqual(result.vectors[0].get('metadata').get('year'), 2024)
        self.assertEqual(result.vectors[1].get('key'), 'vector-2')
        self.assertEqual(result.vectors[1].get('score'), 0.75)
        self.assertEqual(result.vectors[1].get('metadata').get('title'), 'object storage')

    def test_deserialize_result_without_next_token(self):
        # nextToken is not settled by the protocol yet, so a response without
        # it has to leave the attribute at None instead of failing.
        json_data = '''
        {
            "vectors": [
                {"key": "vector-1", "score": 0.5}
            ]
        }
        '''

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        result = model.QueryVectorsFusionResult()
        deserializer = [_serde.deserialize_output_vector_json_model]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)

        self.assertEqual(result.status_code, 200)
        self.assertIsNone(result.next_token)
        self.assertEqual(len(result.vectors), 1)
        self.assertEqual(result.vectors[0].get('score'), 0.5)
        self.assertIsNone(result.vectors[0].get('metadata'))

    def test_deserialize_result_empty_body(self):
        result = model.QueryVectorsFusionResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=None,
                )
            ),
            custom_deserializer=[_serde.deserialize_output_vector_json_model]
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertIsNone(result.next_token)
        self.assertIsNone(result.vectors)

    def test_result_does_not_reuse_distance(self):
        # score belongs to this result only. The old QueryVectorsResult keeps
        # reporting distance and its shape is untouched by this operation.
        self.assertEqual(['next_token', 'vectors'],
                         list(model.QueryVectorsFusionResult._attribute_map.keys()))
        self.assertEqual(['vectors'],
                         list(vector_model.QueryVectorsResult._attribute_map.keys()))
        self.assertNotIn('next_token', vector_model.QueryVectorsResult._attribute_map)

    def test_old_models_are_unchanged(self):
        # The two new operations only add models. Nothing in the existing
        # request shapes moved, which is the compatibility promise of the
        # acceptance criteria.
        self.assertEqual(
            ['bucket', 'data_type', 'dimension', 'distance_metric', 'index_name', 'metadata'],
            list(index_model.PutVectorIndexRequest._attribute_map.keys()))
        self.assertEqual(
            ['bucket', 'filter', 'index_name', 'query_vector', 'return_distance',
             'return_metadata', 'top_k'],
            list(vector_model.QueryVectorsRequest._attribute_map.keys()))
        self.assertEqual(['index'], list(index_model.GetVectorIndexResult._attribute_map.keys()))
        self.assertEqual(['indexes', 'next_token'],
                         list(index_model.ListVectorIndexesResult._attribute_map.keys()))
