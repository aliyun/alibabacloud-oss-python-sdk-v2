# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketEncryption(TestIntegration):

    def test_bucket_encryption(self):
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

        # put bucket encryption
        result = self.client.put_bucket_encryption(oss.PutBucketEncryptionRequest(
            bucket=bucket_name,
            server_side_encryption_rule=oss.ServerSideEncryptionRule(
                apply_server_side_encryption_by_default=oss.ApplyServerSideEncryptionByDefault(
                    kms_master_key_id='0022012****',
                    kms_data_encryption='SM4',
                    sse_algorithm='KMS',
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        # get bucket encryption
        result = self.client.get_bucket_encryption(oss.GetBucketEncryptionRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('0022012****', result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_master_key_id)
        self.assertEqual('SM4', result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_data_encryption)
        self.assertEqual('KMS', result.server_side_encryption_rule.apply_server_side_encryption_by_default.sse_algorithm)

        # delete bucket encryption
        result = self.client.delete_bucket_encryption(oss.DeleteBucketEncryptionRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_encryption_v1(self):
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

        # put bucket encryption
        result = self.signv1_client.put_bucket_encryption(oss.PutBucketEncryptionRequest(
            bucket=bucket_name,
            server_side_encryption_rule=oss.ServerSideEncryptionRule(
                apply_server_side_encryption_by_default=oss.ApplyServerSideEncryptionByDefault(
                    kms_master_key_id='0022012****',
                    kms_data_encryption='SM4',
                    sse_algorithm='KMS',
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket encryption
        result = self.signv1_client.get_bucket_encryption(oss.GetBucketEncryptionRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('0022012****', result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_master_key_id)
        self.assertEqual('SM4', result.server_side_encryption_rule.apply_server_side_encryption_by_default.kms_data_encryption)
        self.assertEqual('KMS', result.server_side_encryption_rule.apply_server_side_encryption_by_default.sse_algorithm)

        # delete bucket encryption
        result = self.signv1_client.delete_bucket_encryption(oss.DeleteBucketEncryptionRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


    def test_bucket_encryption_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put bucket encryption
        try:
            self.invalid_client.put_bucket_encryption(oss.PutBucketEncryptionRequest(
                bucket=bucket_name,
                server_side_encryption_rule=oss.ServerSideEncryptionRule(
                    apply_server_side_encryption_by_default=oss.ApplyServerSideEncryptionByDefault(
                        kms_master_key_id='0022012****',
                        kms_data_encryption='SM4',
                        sse_algorithm='KMS',
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

        # get bucket encryption
        try:
            self.invalid_client.get_bucket_encryption(oss.GetBucketEncryptionRequest(
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

        # delete bucket encryption
        try:
            self.invalid_client.delete_bucket_encryption(oss.DeleteBucketEncryptionRequest(
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