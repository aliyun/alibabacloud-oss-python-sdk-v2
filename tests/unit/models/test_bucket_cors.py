# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_cors as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketCors(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketCorsRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.cors_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketCorsRequest(
            bucket='bucketexampletest',
            cors_configuration=model.CORSConfiguration(
                cors_rules=[model.CORSRule(
                    allowed_origins=['*'],
                    allowed_methods=['GET', 'HEAD'],
                    allowed_headers=['GET'],
                    expose_headers=['x-oss-test', 'x-oss-test1'],
                    max_age_seconds=33012,
                ), model.CORSRule(
                    allowed_origins=['http://www.example.com'],
                    allowed_methods=['PUT', 'POST'],
                    allowed_headers=['*'],
                    expose_headers=['x-oss-test2', 'x-oss-test3'],
                    max_age_seconds=33012,
                )],
                response_vary=True,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('*', request.cors_configuration.cors_rules[0].allowed_origins[0])
        self.assertEqual('GET', request.cors_configuration.cors_rules[0].allowed_methods[0])
        self.assertEqual('HEAD', request.cors_configuration.cors_rules[0].allowed_methods[1])
        self.assertEqual('GET', request.cors_configuration.cors_rules[0].allowed_headers[0])
        self.assertEqual('x-oss-test', request.cors_configuration.cors_rules[0].expose_headers[0])
        self.assertEqual('x-oss-test1', request.cors_configuration.cors_rules[0].expose_headers[1])
        self.assertEqual(33012, request.cors_configuration.cors_rules[0].max_age_seconds)
        self.assertEqual('http://www.example.com', request.cors_configuration.cors_rules[1].allowed_origins[0])
        self.assertEqual('PUT', request.cors_configuration.cors_rules[1].allowed_methods[0])
        self.assertEqual('POST', request.cors_configuration.cors_rules[1].allowed_methods[1])
        self.assertEqual('*', request.cors_configuration.cors_rules[1].allowed_headers[0])
        self.assertEqual('x-oss-test2', request.cors_configuration.cors_rules[1].expose_headers[0])
        self.assertEqual('x-oss-test3', request.cors_configuration.cors_rules[1].expose_headers[1])
        self.assertEqual(33012, request.cors_configuration.cors_rules[1].max_age_seconds)
        self.assertEqual(True, request.cors_configuration.response_vary)


    def test_serialize_request(self):
        request = model.PutBucketCorsRequest(
            bucket='bucketexampletest',
            cors_configuration=model.CORSConfiguration(
                cors_rules=[model.CORSRule(
                    allowed_origins=['*'],
                    allowed_methods=['GET', 'HEAD'],
                    allowed_headers=['GET'],
                    expose_headers=['x-oss-test', 'x-oss-test1'],
                    max_age_seconds=33012,
                ), model.CORSRule(
                    allowed_origins=['http://www.example.com'],
                    allowed_methods=['PUT', 'POST'],
                    allowed_headers=['*'],
                    expose_headers=['x-oss-test2', 'x-oss-test3'],
                    max_age_seconds=33012,
                )],
                response_vary=True,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketCors',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketCors', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketCorsResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketCorsResult()
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
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestGetBucketCors(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketCorsRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketCorsRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketCorsRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketCors',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketCors', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketCorsResult()
        self.assertIsNone(result.cors_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketCorsResult(
            cors_configuration=model.CORSConfiguration(
                cors_rules=[model.CORSRule(
                    allowed_origins=['*'],
                    allowed_methods=['GET', 'HEAD'],
                    allowed_headers=['GET'],
                    expose_headers=['x-oss-test', 'x-oss-test1'],
                    max_age_seconds=33012,
                ), model.CORSRule(
                    allowed_origins=['http://www.example.com'],
                    allowed_methods=['PUT', 'POST'],
                    allowed_headers=['*'],
                    expose_headers=['x-oss-test2', 'x-oss-test3'],
                    max_age_seconds=33012,
                )],
                response_vary=True,
            ),
        )
        self.assertEqual('*', result.cors_configuration.cors_rules[0].allowed_origins[0])
        self.assertEqual('GET', result.cors_configuration.cors_rules[0].allowed_methods[0])
        self.assertEqual('HEAD', result.cors_configuration.cors_rules[0].allowed_methods[1])
        self.assertEqual('GET', result.cors_configuration.cors_rules[0].allowed_headers[0])
        self.assertEqual('x-oss-test', result.cors_configuration.cors_rules[0].expose_headers[0])
        self.assertEqual('x-oss-test1', result.cors_configuration.cors_rules[0].expose_headers[1])
        self.assertEqual(33012, result.cors_configuration.cors_rules[0].max_age_seconds)
        self.assertEqual('http://www.example.com', result.cors_configuration.cors_rules[1].allowed_origins[0])
        self.assertEqual('PUT', result.cors_configuration.cors_rules[1].allowed_methods[0])
        self.assertEqual('POST', result.cors_configuration.cors_rules[1].allowed_methods[1])
        self.assertEqual('*', result.cors_configuration.cors_rules[1].allowed_headers[0])
        self.assertEqual('x-oss-test2', result.cors_configuration.cors_rules[1].expose_headers[0])
        self.assertEqual('x-oss-test3', result.cors_configuration.cors_rules[1].expose_headers[1])
        self.assertEqual(33012, result.cors_configuration.cors_rules[1].max_age_seconds)
        self.assertEqual(True, result.cors_configuration.response_vary)

    def test_deserialize_result(self):
        xml_data = r'''
        <CORSConfiguration>
        </CORSConfiguration>'''

        result = model.GetBucketCorsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <CORSConfiguration>
            <CORSRule>
                <AllowedOrigin>*</AllowedOrigin>
                <AllowedMethod>PUT</AllowedMethod>
                <AllowedMethod>GET</AllowedMethod>
                <AllowedHeader>Authorization</AllowedHeader>
            </CORSRule>
            <CORSRule>
                <AllowedOrigin>http://www.a.com</AllowedOrigin>
                <AllowedOrigin>www.b.com</AllowedOrigin>
                <AllowedMethod>GET</AllowedMethod>
                <AllowedHeader>Authorization</AllowedHeader>
                <ExposeHeader>x-oss-test</ExposeHeader>
                <ExposeHeader>x-oss-test1</ExposeHeader>
                <MaxAgeSeconds>100</MaxAgeSeconds>
            </CORSRule>
        </CORSConfiguration>
        '''

        result = model.GetBucketCorsResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(['*'], result.cors_configuration.cors_rules[0].allowed_origins)
        self.assertEqual(['PUT', 'GET'], result.cors_configuration.cors_rules[0].allowed_methods)
        self.assertEqual(['Authorization'], result.cors_configuration.cors_rules[0].allowed_headers)
        self.assertEqual(['http://www.a.com', 'www.b.com'], result.cors_configuration.cors_rules[1].allowed_origins)
        self.assertEqual(['GET'], result.cors_configuration.cors_rules[1].allowed_methods)
        self.assertEqual(['Authorization'], result.cors_configuration.cors_rules[1].allowed_headers)
        self.assertEqual(['x-oss-test', 'x-oss-test1'], result.cors_configuration.cors_rules[1].expose_headers)
        self.assertEqual(100, result.cors_configuration.cors_rules[1].max_age_seconds)


class TestDeleteBucketCors(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketCorsRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketCorsRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)


    def test_serialize_request(self):
        request = model.DeleteBucketCorsRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketCors',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketCors', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketCorsResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketCorsResult()
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
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestOptionObject(unittest.TestCase):
    def test_constructor_request(self):
        request = model.OptionObjectRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.key)
        self.assertIsNone(request.origin)
        self.assertIsNone(request.access_control_request_method)
        self.assertIsNone(request.access_control_request_headers)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.OptionObjectRequest(
            bucket='bucketexampletest',
            key='example-object-2.jpg',
            origin='http://www.example.com',
            access_control_request_method='PUT',
            access_control_request_headers='x-oss-test2',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('http://www.example.com', request.origin)
        self.assertEqual('PUT', request.access_control_request_method)
        self.assertEqual('x-oss-test2', request.access_control_request_headers)


    def test_serialize_request(self):
        request = model.OptionObjectRequest(
            bucket='bucketexampletest',
            key='example-object-2.jpg',
            origin='http://www.example.com',
            access_control_request_method='PUT',
            access_control_request_headers='x-oss-test2',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='OptionObject',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('OptionObject', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.OptionObjectResult()
        self.assertIsNone(result.access_control_allow_origin)
        self.assertIsNone(result.access_control_allow_methods)
        self.assertIsNone(result.access_control_allow_headers)
        self.assertIsNone(result.access_control_expose_headers)
        self.assertIsNone(result.access_control_max_age)
        self.assertIsInstance(result, serde.Model)

        result = model.OptionObjectResult(
            access_control_allow_origin='http://www.example.com',
            access_control_allow_methods='PUT, POST',
            access_control_allow_headers='x-oss-test2',
            access_control_expose_headers='x-oss-test3',
            access_control_max_age=81306,
        )
        self.assertEqual('http://www.example.com', result.access_control_allow_origin)
        self.assertEqual('PUT, POST', result.access_control_allow_methods)
        self.assertEqual('x-oss-test2', result.access_control_allow_headers)
        self.assertEqual('x-oss-test3', result.access_control_expose_headers)
        self.assertEqual(81306, result.access_control_max_age)

    def test_deserialize_result(self):
        xml_data = None
        result = model.OptionObjectResult()
        serde.deserialize_output_headers(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
                    'Access-Control-Allow-Origin': 'https://example.com',
                    'Access-Control-Allow-Credentials': 'true',
                    'Access-Control-Allow-Methods': 'GET, HEAD',
                    'Access-Control-Allow-Headers': 'x-oss-test1,x-oss-test2',
                    'Access-Control-Expose-Headers': 'x-oss-test3,x-oss-test4',
                    'Access-Control-Max-Age': '100',
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('https://example.com', result.access_control_allow_origin)
        self.assertEqual('GET, HEAD', result.access_control_allow_methods)
        self.assertEqual('x-oss-test1,x-oss-test2', result.access_control_allow_headers)
        self.assertEqual('x-oss-test3,x-oss-test4', result.access_control_expose_headers)
        self.assertEqual(100, result.access_control_max_age)