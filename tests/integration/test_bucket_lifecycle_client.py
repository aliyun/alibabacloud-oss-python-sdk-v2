# pylint: skip-file
import datetime
from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketLifecycle(TestIntegration):

    def test_bucket_lifecycle(self):
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

        # put bucket lifecycle
        request = oss.PutBucketLifecycleRequest(
            bucket=bucket_name,
            lifecycle_configuration=oss.LifecycleConfiguration(
                rules=[oss.LifecycleRule(
                    transitions=[oss.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        storage_class='IA',
                        is_access_time=False,
                    )],
                    prefix='python-test',
                    status='Enabled',
                )],
            ),
        )
        result = self.client.put_bucket_lifecycle(request)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))


        # get bucket lifecycle
        result = self.client.get_bucket_lifecycle(oss.GetBucketLifecycleRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('2023-12-17T00:00:00.000Z', result.lifecycle_configuration.rules[0].transitions[0].created_before_date.strftime('%Y-%m-%dT00:00:00.000Z'))
        self.assertEqual('IA', result.lifecycle_configuration.rules[0].transitions[0].storage_class)
        self.assertEqual(False, result.lifecycle_configuration.rules[0].transitions[0].is_access_time)


        # delete bucket lifecycle
        result = self.client.delete_bucket_lifecycle(oss.DeleteBucketLifecycleRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_lifecycle_v1(self):
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

        # put bucket lifecycle
        result = self.signv1_client.put_bucket_lifecycle(oss.PutBucketLifecycleRequest(
            bucket=bucket_name,
            lifecycle_configuration=oss.LifecycleConfiguration(
                rules=[oss.LifecycleRule(
                    transitions=[oss.LifecycleRuleTransition(
                        created_before_date=datetime.datetime.fromtimestamp(1702743657),
                        storage_class='IA',
                        is_access_time=False,
                    )],
                    prefix='python-test',
                    status='Enabled',
                )],
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket lifecycle
        result = self.signv1_client.get_bucket_lifecycle(oss.GetBucketLifecycleRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('2023-12-17T00:00:00.000Z', result.lifecycle_configuration.rules[0].transitions[0].created_before_date.strftime('%Y-%m-%dT00:00:00.000Z'))
        self.assertEqual('IA', result.lifecycle_configuration.rules[0].transitions[0].storage_class)
        self.assertEqual(False, result.lifecycle_configuration.rules[0].transitions[0].is_access_time)

        # delete bucket lifecycle
        result = self.signv1_client.delete_bucket_lifecycle(oss.DeleteBucketLifecycleRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_lifecycle_fail(self):
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
            self.invalid_client.put_bucket_lifecycle(oss.PutBucketLifecycleRequest(
                bucket=bucket_name,
                lifecycle_configuration=oss.LifecycleConfiguration(
                    rules=[oss.LifecycleRule(
                        transitions=[oss.LifecycleRuleTransition(
                            created_before_date=datetime.datetime.fromtimestamp(1702743657),
                            storage_class='IA',
                            is_access_time=False,
                        )],
                        prefix='python-test',
                        status='Enabled',
                    )],
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
            self.invalid_client.get_bucket_lifecycle(oss.GetBucketLifecycleRequest(
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
            self.invalid_client.delete_bucket_lifecycle(oss.DeleteBucketLifecycleRequest(
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
