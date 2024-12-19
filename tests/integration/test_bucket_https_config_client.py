# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketHttpsConfig(TestIntegration):

    def test_bucket_https_config(self):
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

        # put bucket https config
        result = self.client.put_bucket_https_config(oss.PutBucketHttpsConfigRequest(
            bucket=bucket_name,
            https_configuration=oss.HttpsConfiguration(
                tls=oss.TLS(
                    enable=True,
                    tls_versions=['TLSv1.2', 'TLSv1.3'],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket https config
        result = self.client.get_bucket_https_config(oss.GetBucketHttpsConfigRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(True, result.https_configuration.tls.enable)
        self.assertEqual('TLSv1.2', result.https_configuration.tls.tls_versions[0])
        self.assertEqual('TLSv1.3', result.https_configuration.tls.tls_versions[1])

    def test_bucket_https_config_v1(self):
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

        # put bucket https config
        result = self.signv1_client.put_bucket_https_config(oss.PutBucketHttpsConfigRequest(
            bucket=bucket_name,
            https_configuration=oss.HttpsConfiguration(
                tls=oss.TLS(
                    enable=True,
                    tls_versions=['TLSv1.2', 'TLSv1.3'],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket https config
        result = self.signv1_client.get_bucket_https_config(oss.GetBucketHttpsConfigRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(True, result.https_configuration.tls.enable)
        self.assertEqual('TLSv1.2', result.https_configuration.tls.tls_versions[0])
        self.assertEqual('TLSv1.3', result.https_configuration.tls.tls_versions[1])

    def test_bucket_https_config_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put bucket https config
        try:
            self.invalid_client.put_bucket_https_config(oss.PutBucketHttpsConfigRequest(
                bucket=bucket_name,
                https_configuration=oss.HttpsConfiguration(
                    tls=oss.TLS(
                        enable=True,
                        tls_versions=['TLSv1.2', 'TLSv1.3'],
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

        # get bucket https config
        try:
            self.invalid_client.get_bucket_https_config(oss.GetBucketHttpsConfigRequest(
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