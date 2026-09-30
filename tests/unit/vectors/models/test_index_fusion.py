# pylint: skip-file

import json
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.vectors.operations import _serde
from alibabacloud_oss_v2.vectors.models import index_fusion as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from ... import MockHttpResponse


class TestPutVectorIndexFusion(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutVectorIndexFusionRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.index_name)
        self.assertEqual(request.mode, 'fusion')
        self.assertIsNone(request.schema_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

    def test_constructor_request_with_parameters(self):
        schema = {
            'fields': [
                {'name': 'text_vector', 'type': 'vector', 'dataType': 'float32', 'dimension': 4}
            ]
        }
        request = model.PutVectorIndexFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            mode='fusion',
            schema_configuration=schema
        )
        self.assertEqual(request.bucket, 'test-bucket')
        self.assertEqual(request.index_name, 'test-fusion-index')
        self.assertEqual(request.mode, 'fusion')
        self.assertEqual(request.schema_configuration, schema)
        self.assertIsInstance(request, serde.RequestModel)

    def test_serialize_request(self):
        # Two vector fields plus one full text field, so the golden body below
        # covers the multi vector field shape of section 2.4 and the nested
        # text configuration of section 2.1 in one wire format.
        schema = {
            'fields': [
                {
                    'name': 'text_vector',
                    'type': 'vector',
                    'dataType': 'float32',
                    'dimension': 4,
                    'distanceMetric': 'cosine'
                },
                {
                    'name': 'image_vector',
                    'type': 'vector',
                    'dataType': 'float32',
                    'dimension': 2,
                    'distanceMetric': 'cosine'
                },
                {
                    'name': 'title',
                    'type': 'string',
                    'exactMatch': False,
                    'text': {
                        'enabled': True,
                        'analyzer': 'standard',
                        'analyzerParameters': {
                            'caseSensitive': False,
                            'delimitWord': False,
                            'delimiter': ''
                        }
                    }
                }
            ]
        }

        request = model.PutVectorIndexFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            mode='fusion',
            schema_configuration=schema
        )

        json_str = (
            '{"indexName": "test-fusion-index", "mode": "fusion", "schemaConfiguration": {"fields": ['
            '{"name": "text_vector", "type": "vector", "dataType": "float32", "dimension": 4, "distanceMetric": "cosine"}, '
            '{"name": "image_vector", "type": "vector", "dataType": "float32", "dimension": 2, "distanceMetric": "cosine"}, '
            '{"name": "title", "type": "string", "exactMatch": false, '
            '"text": {"enabled": true, "analyzer": "standard", '
            '"analyzerParameters": {"caseSensitive": false, "delimitWord": false, "delimiter": ""}}}'
            ']}}'
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='PutVectorIndexFusion',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'putVectorIndexFusion': '',
            },
            bucket=request.bucket
        ))

        self.assertEqual(op_input.op_name, 'PutVectorIndexFusion')
        self.assertEqual(op_input.method, 'POST')
        self.assertEqual(op_input.bucket, 'test-bucket')
        self.assertEqual(op_input.headers['Content-Type'], 'application/json')
        self.assertEqual(op_input.parameters['putVectorIndexFusion'], '')
        self.assertEqual(json_str, op_input.body.decode())

        # bucket sits in the host, it must never leak into the request body
        self.assertNotIn('bucket', json.loads(op_input.body.decode()))

    def test_serialize_request_without_mode(self):
        # mode defaults to "fusion"; passing None explicitly keeps the property
        # out of the body instead of sending it as null, which is what lets the
        # service apply its own default.
        schema = {
            'fields': [
                {'name': 'text_vector', 'type': 'vector', 'dataType': 'float32', 'dimension': 4}
            ]
        }

        request = model.PutVectorIndexFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            mode=None,
            schema_configuration=schema
        )

        json_str = (
            '{"indexName": "test-fusion-index", "schemaConfiguration": {"fields": ['
            '{"name": "text_vector", "type": "vector", "dataType": "float32", "dimension": 4}'
            ']}}'
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='PutVectorIndexFusion',
            method='POST',
            bucket=request.bucket
        ))

        self.assertEqual(json_str, op_input.body.decode())
        self.assertNotIn('mode', json.loads(op_input.body.decode()))

    def test_serialize_request_keeps_explicit_false(self):
        # The point of section 2.1: "omitted" and "false" are different to the
        # service, so every boolean written out as False has to survive on the
        # wire. A dict schema keeps them, a typed model with omitempty would
        # not be able to tell the two apart.
        schema = {
            'fields': [
                {
                    'name': 'text_vector',
                    'type': 'vector',
                    'dataType': 'float32',
                    'dimension': 4,
                    'isArray': False,
                    'isPartitionKey': False
                },
                {
                    'name': 'title',
                    'type': 'string',
                    'exactMatch': False,
                    'text': {
                        'enabled': False,
                        'analyzerParameters': {
                            'caseSensitive': False,
                            'delimitWord': False
                        }
                    }
                }
            ]
        }

        request = model.PutVectorIndexFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            schema_configuration=schema
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='PutVectorIndexFusion',
            method='POST',
            bucket=request.bucket
        ))

        body = json.loads(op_input.body.decode())
        fields = body['schemaConfiguration']['fields']
        self.assertEqual(schema['fields'], fields)
        self.assertIs(fields[0]['isArray'], False)
        self.assertIs(fields[0]['isPartitionKey'], False)
        self.assertIs(fields[1]['exactMatch'], False)
        self.assertIs(fields[1]['text']['enabled'], False)
        self.assertIs(fields[1]['text']['analyzerParameters']['caseSensitive'], False)
        self.assertIs(fields[1]['text']['analyzerParameters']['delimitWord'], False)
        # json.dumps, not Python repr, so the wire carries the JSON literals
        self.assertIn('"exactMatch": false', op_input.body.decode())
        self.assertIn('"enabled": false', op_input.body.decode())

    def test_serialize_request_keeps_unknown_property(self):
        # A property a future service version adds travels through unchanged,
        # without waiting for an SDK release. This is the reason the schema is
        # a dict rather than a typed model.
        schema = {
            'fields': [
                {
                    'name': 'text_vector',
                    'type': 'vector',
                    'dataType': 'float32',
                    'dimension': 4,
                    'someFutureProperty': {'nested': [1, 2]}
                }
            ]
        }

        request = model.PutVectorIndexFusionRequest(
            bucket='test-bucket',
            index_name='test-fusion-index',
            schema_configuration=schema
        )

        op_input = _serde.serialize_input_vector_json_model(request, OperationInput(
            op_name='PutVectorIndexFusion',
            method='POST',
            bucket=request.bucket
        ))

        body = json.loads(op_input.body.decode())
        self.assertEqual({'nested': [1, 2]}, body['schemaConfiguration']['fields'][0]['someFutureProperty'])

    def test_serialize_request_missing_required(self):
        schema = {'fields': []}

        cases = [
            # bucket, index_name, schema_configuration
            (None, 'test-fusion-index', schema, 'bucket'),
            ('test-bucket', None, schema, 'index_name'),
            ('test-bucket', 'test-fusion-index', None, 'schema_configuration'),
        ]

        for bucket, index_name, schema_configuration, expected in cases:
            with self.subTest(field=expected):
                request = model.PutVectorIndexFusionRequest(
                    bucket=bucket,
                    index_name=index_name,
                    schema_configuration=schema_configuration
                )
                with self.assertRaises(exceptions.ParamRequiredError) as cm:
                    _serde.serialize_input_vector_json_model(request, OperationInput(
                        op_name='PutVectorIndexFusion',
                        method='POST',
                        bucket=request.bucket
                    ))
                self.assertIn(expected, str(cm.exception))

    def test_constructor_result(self):
        result = model.PutVectorIndexFusionResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        json_data = None
        result = model.PutVectorIndexFusionResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=json_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))
