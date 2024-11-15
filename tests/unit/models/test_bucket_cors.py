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
                    allowed_origins=['ZhmN8g;4rI', '<xYf.;SQs<'],
                    allowed_methods=['l/2)-T kQB', 'e+Pb%0xZul'],
                    allowed_headers=['Alb,\l~C$*', 'b%K+F*G$9)'],
                    expose_headers=[' 2mx&UqAK,', '%VI.HG@J+6'],
                    max_age_seconds=49678,
                ), model.CORSRule(
                    allowed_origins=['QqtP*bW1YV', ' Cr~f+#CMh'],
                    allowed_methods=['@vdSFJW8t^', 't52+Q?Tn|J'],
                    allowed_headers=['mj68#8%DS#', 'Q-##L5hH/('],
                    expose_headers=['+^;Y1A?U>D', 'fsE3_#FDr '],
                    max_age_seconds=49678,
                )],
                response_vary=True,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(['ZhmN8g;4rI', '<xYf.;SQs<'], request.cors_configuration.cors_rules[0].allowed_origins)
        self.assertEqual(['l/2)-T kQB', 'e+Pb%0xZul'], request.cors_configuration.cors_rules[0].allowed_methods)
        self.assertEqual(['Alb,\l~C$*', 'b%K+F*G$9)'], request.cors_configuration.cors_rules[0].allowed_headers)
        self.assertEqual([' 2mx&UqAK,', '%VI.HG@J+6'], request.cors_configuration.cors_rules[0].expose_headers)
        self.assertEqual(49678, request.cors_configuration.cors_rules[0].max_age_seconds)
        self.assertEqual(['QqtP*bW1YV', ' Cr~f+#CMh'], request.cors_configuration.cors_rules[1].allowed_origins)
        self.assertEqual(['@vdSFJW8t^', 't52+Q?Tn|J'], request.cors_configuration.cors_rules[1].allowed_methods)
        self.assertEqual(['mj68#8%DS#', 'Q-##L5hH/('], request.cors_configuration.cors_rules[1].allowed_headers)
        self.assertEqual(['+^;Y1A?U>D', 'fsE3_#FDr '], request.cors_configuration.cors_rules[1].expose_headers)
        self.assertEqual(49678, request.cors_configuration.cors_rules[1].max_age_seconds)
        self.assertEqual(True, request.cors_configuration.response_vary)


    def test_serialize_request(self):
        request = model.PutBucketCorsRequest(
            bucket='bucketexampletest',
            cors_configuration=model.CORSConfiguration(
                cors_rules=[model.CORSRule(
                    allowed_origins=['>CzNlFJ1Kw', 'oo7y^shp+?'],
                    allowed_methods=['9efB;Y3;Zf', '>g(GkiVKg^'],
                    allowed_headers=['9m~iHMaJtH', '9hRnY5vu&5'],
                    expose_headers=['PXMN0ZjAM6', '#|M3OiQd4/'],
                    max_age_seconds=49678,
                ), model.CORSRule(
                    allowed_origins=['?bz-S$Spds', '4@M!RPizW+'],
                    allowed_methods=['Zav2M$ IUl', 'zB\3kjA-S&'],
                    allowed_headers=['zbz6xI<cF7', 'G/hF2,2? D'],
                    expose_headers=['VweEXi71(h', '*eQJ1^aM.X'],
                    max_age_seconds=49678,
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
                    allowed_origins=['mwo2j+*<o~', 'O+AT%e)jk+'],
                    allowed_methods=['/P;ezd7e8s', 'tkOsCBE!LD'],
                    allowed_headers=['_+$J9U0.F3', 'KvWV(8fS+6'],
                    expose_headers=['MdUVh#sZ)p', ' >Nbqt(JzL'],
                    max_age_seconds=77759,
                ), model.CORSRule(
                    allowed_origins=[' $\^xJY>@n', '7!rK1(S5*A'],
                    allowed_methods=['H/Li8w&4%T', 'lX@d&Ne:T/'],
                    allowed_headers=['n1NV@ggVq<', 's&xaqbcNy0'],
                    expose_headers=[',J>Q+F97xb', 'o$%TvALPXm'],
                    max_age_seconds=77759,
                )],
                response_vary=True,
            ),
        )
        self.assertEqual(['mwo2j+*<o~', 'O+AT%e)jk+'], result.cors_configuration.cors_rules[0].allowed_origins)
        self.assertEqual(['/P;ezd7e8s', 'tkOsCBE!LD'], result.cors_configuration.cors_rules[0].allowed_methods)
        self.assertEqual(['_+$J9U0.F3', 'KvWV(8fS+6'], result.cors_configuration.cors_rules[0].allowed_headers)
        self.assertEqual(['MdUVh#sZ)p', ' >Nbqt(JzL'], result.cors_configuration.cors_rules[0].expose_headers)
        self.assertEqual(77759, result.cors_configuration.cors_rules[0].max_age_seconds)
        self.assertEqual([' $\^xJY>@n', '7!rK1(S5*A'], result.cors_configuration.cors_rules[1].allowed_origins)
        self.assertEqual(['H/Li8w&4%T', 'lX@d&Ne:T/'], result.cors_configuration.cors_rules[1].allowed_methods)
        self.assertEqual(['n1NV@ggVq<', 's&xaqbcNy0'], result.cors_configuration.cors_rules[1].allowed_headers)
        self.assertEqual([',J>Q+F97xb', 'o$%TvALPXm'], result.cors_configuration.cors_rules[1].expose_headers)
        self.assertEqual(77759, result.cors_configuration.cors_rules[1].max_age_seconds)
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
            origin='5@gXwKIDg7',
            access_control_request_method=' ^nSO9vzfT',
            access_control_request_headers='V!P;r)+3>G',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('example-object-2.jpg', request.key)
        self.assertEqual('5@gXwKIDg7', request.origin)
        self.assertEqual(' ^nSO9vzfT', request.access_control_request_method)
        self.assertEqual('V!P;r)+3>G', request.access_control_request_headers)


    def test_serialize_request(self):
        request = model.OptionObjectRequest(
            bucket='bucketexampletest',
            key='example-object-2.jpg',
            origin='5@gXwKIDg7',
            access_control_request_method=' ^nSO9vzfT',
            access_control_request_headers='V!P;r)+3>G',
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
            access_control_allow_origin='X%d* 3Tfav',
            access_control_allow_methods='WRWxtYLGp~',
            access_control_allow_headers='K7&)LMq-wB',
            access_control_expose_headers='U|cd8J^Fy8',
            access_control_max_age=81306,
        )
        self.assertEqual('X%d* 3Tfav', result.access_control_allow_origin)
        self.assertEqual('WRWxtYLGp~', result.access_control_allow_methods)
        self.assertEqual('K7&)LMq-wB', result.access_control_allow_headers)
        self.assertEqual('U|cd8J^Fy8', result.access_control_expose_headers)
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
                    'Access-Control-Allow-Origin': '$WK5+C/suC',
                    'Access-Control-Allow-Credentials': 'true',
                    'Access-Control-Allow-Methods': 'GET, HEAD',
                    'Access-Control-Allow-Headers': 'sgj|4n_ujl',
                    'Access-Control-Expose-Headers': 'n@_1\Spz#5, f xq)N)O;E',
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
        self.assertEqual('$WK5+C/suC', result.access_control_allow_origin)
        self.assertEqual('GET, HEAD', result.access_control_allow_methods)
        self.assertEqual('sgj|4n_ujl', result.access_control_allow_headers)
        self.assertEqual('n@_1\Spz#5, f xq)N)O;E', result.access_control_expose_headers)
        self.assertEqual(100, result.access_control_max_age)