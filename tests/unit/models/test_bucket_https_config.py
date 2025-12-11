# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_https_config as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketHttpsConfig(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketHttpsConfigRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.https_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketHttpsConfigRequest(
            bucket='bucketexampletest',
            https_configuration=model.HttpsConfiguration(
                tls=model.TLS(
                    enable=True,
                    tls_versions=['TLSv1.2', 'TLSv1.3'],
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(True, request.https_configuration.tls.enable)
        self.assertEqual('TLSv1.2', request.https_configuration.tls.tls_versions[0])
        self.assertEqual('TLSv1.3', request.https_configuration.tls.tls_versions[1])

    def test_serialize_request(self):
        request = model.PutBucketHttpsConfigRequest(
            bucket='bucketexampletest',
            https_configuration=model.HttpsConfiguration(
                tls=model.TLS(
                    enable=False,
                    tls_versions=['TLSv1.2', 'TLSv1.2'],
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketHttpsConfig',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketHttpsConfig', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketHttpsConfigResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketHttpsConfigResult()
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


class TestGetBucketHttpsConfig(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketHttpsConfigRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketHttpsConfigRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketHttpsConfigRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketHttpsConfig',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketHttpsConfig', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketHttpsConfigResult()
        self.assertIsNone(result.https_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketHttpsConfigResult(
            https_configuration=model.HttpsConfiguration(
                tls=model.TLS(
                    enable=True,
                    tls_versions=['TLSv1.2', 'TLSv1.3'],
                ),
            ),
        )
        self.assertEqual(True, result.https_configuration.tls.enable)
        self.assertEqual('TLSv1.2', result.https_configuration.tls.tls_versions[0])
        self.assertEqual('TLSv1.3', result.https_configuration.tls.tls_versions[1])

    def test_deserialize_result(self):
        xml_data = r'''
        <HttpsConfiguration>
        </HttpsConfiguration>'''

        result = model.GetBucketHttpsConfigResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <HttpsConfiguration>
          <TLS>
            <Enable>true</Enable>
            <TLSVersion>TLSv1.2</TLSVersion>
            <TLSVersion>TLSv1.3</TLSVersion>
          </TLS>
        </HttpsConfiguration>
        '''

        result = model.GetBucketHttpsConfigResult()
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
        self.assertEqual(True, result.https_configuration.tls.enable)
        self.assertEqual('TLSv1.2', result.https_configuration.tls.tls_versions[0])
        self.assertEqual('TLSv1.3', result.https_configuration.tls.tls_versions[1])

    def test_cipher_suite_fields(self):
        xml_str = '<HttpsConfiguration><TLS><Enable>true</Enable><TLSVersion>TLSv1.2</TLSVersion></TLS><CipherSuite><Enable>true</Enable><StrongCipherSuite>false</StrongCipherSuite><CustomCipherSuite>ECDHE-RSA-AES128-SHA</CustomCipherSuite><CustomCipherSuite>AES256-SHA</CustomCipherSuite><TLS13CustomCipherSuite>TLS_AES_128_GCM_SHA256</TLS13CustomCipherSuite><TLS13CustomCipherSuite>TLS_CHACHA20_POLY1305_SHA256</TLS13CustomCipherSuite></CipherSuite></HttpsConfiguration>'

        https_config = model.HttpsConfiguration(
            tls=model.TLS(
                enable=True,
                tls_versions=['TLSv1.2'],
            ),
            cipher_suite=model.CipherSuite(
                enable=True,
                strong_cipher_suite=False,
                custom_cipher_suites=['ECDHE-RSA-AES128-SHA', 'AES256-SHA'],
                tls13_custom_cipher_suites=['TLS_AES_128_GCM_SHA256', 'TLS_CHACHA20_POLY1305_SHA256']
            )
        )

        request = model.PutBucketHttpsConfigRequest(
            bucket='bucketexampletest',
            https_configuration=https_config
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketHttpsConfig',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketHttpsConfig', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual(True, https_config.tls.enable)
        self.assertEqual(['TLSv1.2'], https_config.tls.tls_versions)
        self.assertEqual(True, https_config.cipher_suite.enable)
        self.assertEqual(False, https_config.cipher_suite.strong_cipher_suite)
        self.assertEqual(['ECDHE-RSA-AES128-SHA', 'AES256-SHA'], https_config.cipher_suite.custom_cipher_suites)
        self.assertEqual(['TLS_AES_128_GCM_SHA256', 'TLS_CHACHA20_POLY1305_SHA256'], https_config.cipher_suite.tls13_custom_cipher_suites)
        self.assertEqual(xml_str, op_input.body.decode().replace('\n', '').replace('\r', '').replace(' ', ''))