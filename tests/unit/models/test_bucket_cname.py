# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_cname as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestCreateCnameToken(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CreateCnameTokenRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.bucket_cname_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CreateCnameTokenRequest(
            bucket='bucket-name-test',
            bucket_cname_configuration=model.BucketCnameConfiguration(
                cname=model.Cname(
                    domain='example.com',
                    certificate_configuration=model.CertificateConfiguration(
                        certificate='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                        private_key='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                        previous_cert_id='493****-cn-hangzhou',
                        force=True,
                        cert_id='493****-cn-hangzhou',
                    ),
                ),
            ),
        )
        self.assertEqual('bucket-name-test', request.bucket)
        self.assertEqual('example.com', request.bucket_cname_configuration.cname.domain)
        self.assertEqual('-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----', request.bucket_cname_configuration.cname.certificate_configuration.certificate)
        self.assertEqual('-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----', request.bucket_cname_configuration.cname.certificate_configuration.private_key)
        self.assertEqual('493****-cn-hangzhou', request.bucket_cname_configuration.cname.certificate_configuration.previous_cert_id)
        self.assertEqual(True, request.bucket_cname_configuration.cname.certificate_configuration.force)
        self.assertEqual('493****-cn-hangzhou', request.bucket_cname_configuration.cname.certificate_configuration.cert_id)

    def test_serialize_request(self):
        request = model.CreateCnameTokenRequest(
            bucket='bucket-name-test',
            bucket_cname_configuration=model.BucketCnameConfiguration(
                cname=model.Cname(
                    domain='example.com',
                    certificate_configuration=model.CertificateConfiguration(
                        certificate='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                        private_key='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                        previous_cert_id='493****-cn-hangzhou',
                        force=True,
                        delete_certificate=True,
                        cert_id='493****-cn-hangzhou',
                    ),
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CreateCnameToken',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CreateCnameToken', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket-name-test', op_input.bucket)

    def test_constructor_result(self):
        result = model.CreateCnameTokenResult()
        self.assertIsNone(result.cname_token)
        self.assertIsInstance(result, serde.Model)

        result = model.CreateCnameTokenResult(
            cname_token=model.CnameToken(
                cname='example.com',
                token='be1d49d863dea9ffeff3df7d6455****',
                expire_time='Wed, 23 Feb 2022 21:39:42 GMT',
                bucket='bucket-name-test',
            ),
        )
        self.assertEqual('example.com', result.cname_token.cname)
        self.assertEqual('be1d49d863dea9ffeff3df7d6455****', result.cname_token.token)
        self.assertEqual('Wed, 23 Feb 2022 21:39:42 GMT', result.cname_token.expire_time)
        self.assertEqual('bucket-name-test', result.cname_token.bucket)

    def test_deserialize_result(self):
        xml_data = r'''
        <CnameToken>
        </CnameToken>'''

        result = model.CreateCnameTokenResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <CnameToken>
          <Bucket>examplebucket</Bucket>
          <Cname>example.com</Cname>;
          <Token>be1d49d863dea9ffeff3df7d6455****</Token>
          <ExpireTime>Wed, 23 Feb 2022 21:16:37 GMT</ExpireTime>
        </CnameToken>
        '''

        result = model.CreateCnameTokenResult()
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
        self.assertEqual('examplebucket', result.cname_token.bucket)
        self.assertEqual('example.com', result.cname_token.cname)
        self.assertEqual('be1d49d863dea9ffeff3df7d6455****', result.cname_token.token)
        self.assertEqual('Wed, 23 Feb 2022 21:16:37 GMT', result.cname_token.expire_time)


class TestGetCnameToken(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetCnameTokenRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.cname)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetCnameTokenRequest(
            bucket='bucketexampletest',
            cname='example.com',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('example.com', request.cname)

    def test_serialize_request(self):
        request = model.GetCnameTokenRequest(
            bucket='bucketexampletest',
            cname='example.com',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetCnameToken',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetCnameToken', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('example.com', op_input.parameters.get('cname'))

    def test_constructor_result(self):
        result = model.GetCnameTokenResult()
        self.assertIsNone(result.cname_token)
        self.assertIsInstance(result, serde.Model)

        result = model.GetCnameTokenResult(
            cname_token=model.CnameToken(
                cname='example.com',
                token='be1d49d863dea9ffeff3df7d6455****',
                expire_time='Wed, 23 Feb 2022 21:39:42 GMT',
                bucket='bucketexampletest',
            ),
        )
        self.assertEqual('example.com', result.cname_token.cname)
        self.assertEqual('be1d49d863dea9ffeff3df7d6455****', result.cname_token.token)
        self.assertEqual('Wed, 23 Feb 2022 21:39:42 GMT', result.cname_token.expire_time)
        self.assertEqual('bucketexampletest', result.cname_token.bucket)

    def test_deserialize_result(self):
        xml_data = r'''
        <CnameToken>
        </CnameToken>'''

        result = model.GetCnameTokenResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <CnameToken>
          <Bucket>mybucket</Bucket>
          <Cname>example.com</Cname>
          <Token>be1d49d863dea9ffeff3df7d6455****</Token>
          <ExpireTime>Wed, 23 Feb 2022 21:39:42 GMT</ExpireTime>
        </CnameToken>
        '''

        result = model.GetCnameTokenResult()
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
        self.assertEqual('mybucket', result.cname_token.bucket)
        self.assertEqual('example.com', result.cname_token.cname)
        self.assertEqual('be1d49d863dea9ffeff3df7d6455****', result.cname_token.token)
        self.assertEqual('Wed, 23 Feb 2022 21:39:42 GMT', result.cname_token.expire_time)


class TestPutCname(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutCnameRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.bucket_cname_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutCnameRequest(
            bucket='bucketexampletest',
            bucket_cname_configuration=model.BucketCnameConfiguration(
                cname=model.Cname(
                    domain='example.com',
                    certificate_configuration=model.CertificateConfiguration(
                        certificate='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                        private_key='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                        previous_cert_id='493****-cn-hangzhou',
                        force=False,
                        delete_certificate=True,
                        cert_id='493****-cn-hangzhou',
                    ),
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('example.com', request.bucket_cname_configuration.cname.domain)
        self.assertEqual('-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
            request.bucket_cname_configuration.cname.certificate_configuration.certificate)
        self.assertEqual('-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
            request.bucket_cname_configuration.cname.certificate_configuration.private_key)
        self.assertEqual('493****-cn-hangzhou', request.bucket_cname_configuration.cname.certificate_configuration.previous_cert_id)
        self.assertEqual(False, request.bucket_cname_configuration.cname.certificate_configuration.force)
        self.assertEqual(True, request.bucket_cname_configuration.cname.certificate_configuration.delete_certificate)
        self.assertEqual('493****-cn-hangzhou', request.bucket_cname_configuration.cname.certificate_configuration.cert_id)

    def test_serialize_request(self):
        request = model.PutCnameRequest(
            bucket='bucketexampletest',
            bucket_cname_configuration=model.BucketCnameConfiguration(
                cname=model.Cname(
                    domain='example.com',
                    certificate_configuration=model.CertificateConfiguration(
                        certificate='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                        private_key='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                        previous_cert_id='493****-cn-hangzhou',
                        force=True,
                        delete_certificate=True,
                        cert_id='493****-cn-hangzhou',
                    ),
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutCname',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutCname', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutCnameResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutCnameResult()
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


class TestListCname(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListCnameRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListCnameRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.ListCnameRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListCname',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('ListCname', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.ListCnameResult()
        self.assertIsNone(result.cnames)
        self.assertIsNone(result.bucket)
        self.assertIsNone(result.owner)
        self.assertIsInstance(result, serde.Model)

        result = model.ListCnameResult(
            cnames=[model.CnameInfo(
                domain='example.com',
                last_modified='2024-12-17T00:20:57.000Z',
                status='OK',
                certificate=model.CnameCertificate(
                    fingerprint='DE:01:CF:EC:7C:A7:98:CB:D8:6E:FB:1D:97:EB:A9:64:1D:4E:**:**',
                    valid_start_date='Wed, 12 Apr 2023 10:14:51 GMT',
                    valid_end_date='Mon, 4 May 2048 10:14:51 GMT',
                    type='CAS',
                    cert_id='493****-cn-hangzhou',
                    status='OK',
                    creation_date='2013-07-31T10:56:21.000Z',
                ),
            ), model.CnameInfo(
                domain='example.com',
                last_modified='2014-07-31T10:56:21.000Z',
                status='OK',
                certificate=model.CnameCertificate(
                    fingerprint='98:CB:D8:6E:FB:1D:97:EB:A9:64:1D:4E:**:**',
                    valid_start_date='Wed, 12 Apr 2021 10:14:51 GMT',
                    valid_end_date='Mon, 5 May 2048 10:14:51 GMT',
                    type='CAS',
                    cert_id='493****-cn-hangzhou',
                    status='OK',
                    creation_date='2013-07-31T10:56:21.000Z',
                ),
            )],
            bucket='bucketexampletest',
            owner='owner',
        )
        self.assertEqual('example.com', result.cnames[0].domain)
        self.assertEqual('2024-12-17T00:20:57.000Z', result.cnames[0].last_modified)
        self.assertEqual('OK', result.cnames[0].status)
        self.assertEqual('DE:01:CF:EC:7C:A7:98:CB:D8:6E:FB:1D:97:EB:A9:64:1D:4E:**:**', result.cnames[0].certificate.fingerprint)
        self.assertEqual('Wed, 12 Apr 2023 10:14:51 GMT', result.cnames[0].certificate.valid_start_date)
        self.assertEqual('Mon, 4 May 2048 10:14:51 GMT', result.cnames[0].certificate.valid_end_date)
        self.assertEqual('CAS', result.cnames[0].certificate.type)
        self.assertEqual('493****-cn-hangzhou', result.cnames[0].certificate.cert_id)
        self.assertEqual('OK', result.cnames[0].certificate.status)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.cnames[0].certificate.creation_date)
        self.assertEqual('example.com', result.cnames[1].domain)
        self.assertEqual('2014-07-31T10:56:21.000Z', result.cnames[1].last_modified)
        self.assertEqual('OK', result.cnames[1].status)
        self.assertEqual('98:CB:D8:6E:FB:1D:97:EB:A9:64:1D:4E:**:**', result.cnames[1].certificate.fingerprint)
        self.assertEqual('Wed, 12 Apr 2021 10:14:51 GMT', result.cnames[1].certificate.valid_start_date)
        self.assertEqual('Mon, 5 May 2048 10:14:51 GMT', result.cnames[1].certificate.valid_end_date)
        self.assertEqual('CAS', result.cnames[1].certificate.type)
        self.assertEqual('493****-cn-hangzhou', result.cnames[1].certificate.cert_id)
        self.assertEqual('OK', result.cnames[1].certificate.status)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.cnames[1].certificate.creation_date)
        self.assertEqual('bucketexampletest', result.bucket)
        self.assertEqual('owner', result.owner)


    def test_deserialize_result(self):
        xml_data = r'''
        <ListCnameResult>
        </ListCnameResult>'''

        result = model.ListCnameResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ListCnameResult>
          <Bucket>targetbucket</Bucket>
          <Owner>testowner</Owner>
          <Cname>
            <Domain>example.com</Domain>
            <LastModified>2021-09-15T02:35:07.000Z</LastModified>
            <Status>Enabled</Status>
            <Certificate>
              <Type>CAS</Type>
              <CertId>493****-cn-hangzhou</CertId>
              <Status>Enabled</Status>
              <CreationDate>Wed, 15 Sep 2021 02:35:06 GMT</CreationDate>
              <Fingerprint>DE:01:CF:EC:7C:A7:98:CB:D8:6E:FB:1D:97:EB:A9:64:1D:4E:**:**</Fingerprint>
              <ValidStartDate>Wed, 12 Apr 2023 10:14:51 GMT</ValidStartDate>
              <ValidEndDate>Mon, 4 May 2048 10:14:51 GMT</ValidEndDate>
            </Certificate>
          </Cname>
          <Cname>
            <Domain>example.org</Domain>
            <LastModified>2021-09-15T02:34:58.000Z</LastModified>
            <Status>Enabled</Status>
          </Cname>
          <Cname>
            <Domain>example.edu</Domain>
            <LastModified>2021-09-15T02:50:34.000Z</LastModified>
            <Status>Enabled</Status>
          </Cname>
        </ListCnameResult>
        '''

        result = model.ListCnameResult()
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
        self.assertEqual('targetbucket', result.bucket)
        self.assertEqual('testowner', result.owner)
        self.assertEqual('example.com', result.cnames[0].domain)
        self.assertEqual('2021-09-15T02:35:07.000Z', result.cnames[0].last_modified)
        self.assertEqual('Enabled', result.cnames[0].status)
        self.assertEqual('CAS', result.cnames[0].certificate.type)
        self.assertEqual('493****-cn-hangzhou', result.cnames[0].certificate.cert_id)
        self.assertEqual('Enabled', result.cnames[0].certificate.status)
        self.assertEqual('Wed, 15 Sep 2021 02:35:06 GMT', result.cnames[0].certificate.creation_date)
        self.assertEqual('DE:01:CF:EC:7C:A7:98:CB:D8:6E:FB:1D:97:EB:A9:64:1D:4E:**:**', result.cnames[0].certificate.fingerprint)
        self.assertEqual('Wed, 12 Apr 2023 10:14:51 GMT', result.cnames[0].certificate.valid_start_date)
        self.assertEqual('Mon, 4 May 2048 10:14:51 GMT', result.cnames[0].certificate.valid_end_date)
        self.assertEqual('example.org', result.cnames[1].domain)
        self.assertEqual('2021-09-15T02:34:58.000Z', result.cnames[1].last_modified)
        self.assertEqual('Enabled', result.cnames[1].status)
        self.assertEqual('example.edu', result.cnames[2].domain)
        self.assertEqual('2021-09-15T02:50:34.000Z', result.cnames[2].last_modified)
        self.assertEqual('Enabled', result.cnames[2].status)


class TestDeleteCname(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteCnameRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.bucket_cname_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteCnameRequest(
            bucket='bucketexampletest',
            bucket_cname_configuration=model.BucketCnameConfiguration(
                cname=model.Cname(
                    domain='example.com',
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('example.com', request.bucket_cname_configuration.cname.domain)


    def test_serialize_request(self):
        request = model.DeleteCnameRequest(
            bucket='bucketexampletest',
            bucket_cname_configuration=model.BucketCnameConfiguration(
                cname=model.Cname(
                    domain='example.com',
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteCname',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteCname', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteCnameResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteCnameResult()
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
