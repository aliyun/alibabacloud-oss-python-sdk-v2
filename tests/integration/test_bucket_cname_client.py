# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestCnameToken(TestIntegration):

    def test_cname_token(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # create cname token
        result = self.client.create_cname_token(oss.CreateCnameTokenRequest(
            bucket=bucket_name,
            bucket_cname_configuration=oss.BucketCnameConfiguration(
                cname=oss.Cname(
                    domain='example.com',
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get cname token
        result = self.client.get_cname_token(oss.GetCnameTokenRequest(
            bucket=bucket_name,
            cname='example.com',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put cname
        try:
            self.client.put_cname(oss.PutCnameRequest(
                bucket=bucket_name,
                bucket_cname_configuration=oss.BucketCnameConfiguration(
                    cname=oss.Cname(
                        domain='example.com',
                        certificate_configuration=oss.CertificateConfiguration(
                            certificate='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                            private_key='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                            previous_cert_id='493****-cn-hangzhou',
                            force=True,
                            cert_id='493****-cn-hangzhou',
                        ),
                    ),
                ),
            ))
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NeedVerifyDomainOwnership', serr.code)

        try:
            self.client.put_cname(oss.PutCnameRequest(
                bucket=bucket_name,
                bucket_cname_configuration=oss.BucketCnameConfiguration(
                    cname=oss.Cname(
                        domain='example.com',
                        certificate_configuration=oss.CertificateConfiguration(
                            delete_certificate=True,
                        ),
                    ),
                ),
            ))
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NeedVerifyDomainOwnership', serr.code)

        # list cname
        result = self.client.list_cname(oss.ListCnameRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.bucket)
        self.assertIsNotNone(result.owner)

        # delete cname
        result = self.client.delete_cname(oss.DeleteCnameRequest(
            bucket=bucket_name,
            bucket_cname_configuration=oss.BucketCnameConfiguration(
                cname=oss.Cname(
                    domain='example.com',
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_cname_token_v1(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.signv1_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # create cname token
        result = self.signv1_client.create_cname_token(oss.CreateCnameTokenRequest(
            bucket=bucket_name,
            bucket_cname_configuration=oss.BucketCnameConfiguration(
                cname=oss.Cname(
                    domain='example.com',
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get cname token
        result = self.signv1_client.get_cname_token(oss.GetCnameTokenRequest(
            bucket=bucket_name,
            cname='example.com',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put cname
        try:
            self.signv1_client.put_cname(oss.PutCnameRequest(
                bucket=bucket_name,
                bucket_cname_configuration=oss.BucketCnameConfiguration(
                    cname=oss.Cname(
                        domain='example.com',
                        certificate_configuration=oss.CertificateConfiguration(
                            certificate='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                            private_key='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                            previous_cert_id='493****-cn-hangzhou',
                            force=True,
                            cert_id='493****-cn-hangzhou',
                        ),
                    ),
                ),
            ))
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NeedVerifyDomainOwnership', serr.code)

        try:
            self.signv1_client.put_cname(oss.PutCnameRequest(
                bucket=bucket_name,
                bucket_cname_configuration=oss.BucketCnameConfiguration(
                    cname=oss.Cname(
                        domain='example.com',
                        certificate_configuration=oss.CertificateConfiguration(
                            delete_certificate=True,
                        ),
                    ),
                ),
            ))
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NeedVerifyDomainOwnership', serr.code)

        # list cname
        result = self.signv1_client.list_cname(oss.ListCnameRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.bucket)
        self.assertIsNotNone(result.owner)

        # delete cname
        result = self.signv1_client.delete_cname(oss.DeleteCnameRequest(
            bucket=bucket_name,
            bucket_cname_configuration=oss.BucketCnameConfiguration(
                cname=oss.Cname(
                    domain='example.com',
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_cname_token_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        try:
            self.invalid_client.create_cname_token(oss.CreateCnameTokenRequest(
                bucket=bucket_name,
                bucket_cname_configuration=oss.BucketCnameConfiguration(
                    cname=oss.Cname(
                        domain='example.com',
                    ),
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        try:
            self.invalid_client.put_cname(oss.PutCnameRequest(
                bucket=bucket_name,
                bucket_cname_configuration=oss.BucketCnameConfiguration(
                    cname=oss.Cname(
                        domain='@d5;hctd1|',
                        certificate_configuration=oss.CertificateConfiguration(
                            certificate='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                            private_key='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----',
                            previous_cert_id='493****-cn-hangzhou',
                            force=True,
                            cert_id='493****-cn-hangzhou',
                        ),
                    ),
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        try:
            self.invalid_client.list_cname(oss.ListCnameRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        try:
            self.invalid_client.delete_cname(oss.DeleteCnameRequest(
                bucket=bucket_name,
                bucket_cname_configuration=oss.BucketCnameConfiguration(
                    cname=oss.Cname(
                        domain='example.com',
                    ),
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
