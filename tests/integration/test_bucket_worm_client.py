# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestInitiateBucketWorm(TestIntegration):

    def test_initiate_bucket_worm(self):
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

        # initiate bucket worm
        result = self.client.initiate_bucket_worm(oss.InitiateBucketWormRequest(
            bucket=bucket_name,
            initiate_worm_configuration=oss.InitiateWormConfiguration(
                retention_period_in_days=1,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # abort bucket worm
        result = self.client.abort_bucket_worm(oss.AbortBucketWormRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # initiate bucket worm
        result = self.client.initiate_bucket_worm(oss.InitiateBucketWormRequest(
            bucket=bucket_name,
            initiate_worm_configuration=oss.InitiateWormConfiguration(
                retention_period_in_days=1,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        worm_id = result.worm_id

        # get bucket worm
        result = self.client.get_bucket_worm(oss.GetBucketWormRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(1, result.worm_configuration.retention_period_in_days)
        self.assertEqual(worm_id, result.worm_configuration.worm_id)
        self.assertEqual('InProgress', result.worm_configuration.state)
        self.assertIsNotNone(result.worm_configuration.creation_date)

        # complete bucket worm
        result = self.client.complete_bucket_worm(oss.CompleteBucketWormRequest(
            bucket=bucket_name,
            worm_id=worm_id,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # extend bucket worm
        result = self.client.extend_bucket_worm(oss.ExtendBucketWormRequest(
            bucket=bucket_name,
            worm_id=worm_id,
            extend_worm_configuration=oss.ExtendWormConfiguration(
                retention_period_in_days=2,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


    def test_initiate_bucket_worm_v1(self):
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

        # initiate bucket worm
        result = self.signv1_client.initiate_bucket_worm(oss.InitiateBucketWormRequest(
            bucket=bucket_name,
            initiate_worm_configuration=oss.InitiateWormConfiguration(
                retention_period_in_days=1,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # abort bucket worm
        result = self.signv1_client.abort_bucket_worm(oss.AbortBucketWormRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # initiate bucket worm
        result = self.signv1_client.initiate_bucket_worm(oss.InitiateBucketWormRequest(
            bucket=bucket_name,
            initiate_worm_configuration=oss.InitiateWormConfiguration(
                retention_period_in_days=1,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        worm_id = result.worm_id

        # get bucket worm
        result = self.signv1_client.get_bucket_worm(oss.GetBucketWormRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(1, result.worm_configuration.retention_period_in_days)
        self.assertEqual(worm_id, result.worm_configuration.worm_id)
        self.assertEqual('InProgress', result.worm_configuration.state)
        self.assertIsNotNone(result.worm_configuration.creation_date)

        # complete bucket worm
        result = self.signv1_client.complete_bucket_worm(oss.CompleteBucketWormRequest(
            bucket=bucket_name,
            worm_id=worm_id,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # extend bucket worm
        result = self.signv1_client.extend_bucket_worm(oss.ExtendBucketWormRequest(
            bucket=bucket_name,
            worm_id=worm_id,
            extend_worm_configuration=oss.ExtendWormConfiguration(
                retention_period_in_days=2,
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_initiate_bucket_worm_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # initiate bucket worm
        try:
            self.invalid_client.initiate_bucket_worm(oss.InitiateBucketWormRequest(
                bucket=bucket_name,
                initiate_worm_configuration=oss.InitiateWormConfiguration(
                    retention_period_in_days=1,
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

        # get bucket worm
        try:
            self.invalid_client.get_bucket_worm(oss.GetBucketWormRequest(
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

        # complete bucket worm
        try:
            self.invalid_client.complete_bucket_worm(oss.CompleteBucketWormRequest(
                bucket=bucket_name,
                worm_id='1666E2CFB2B3418****',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # extend bucket worm
        try:
            self.invalid_client.extend_bucket_worm(oss.ExtendBucketWormRequest(
                bucket=bucket_name,
                worm_id='1666E2CFB2B3418****',
                extend_worm_configuration=oss.ExtendWormConfiguration(
                    retention_period_in_days=24657,
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

        # abort bucket worm
        try:
            self.invalid_client.abort_bucket_worm(oss.AbortBucketWormRequest(
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