# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketAccessMonitor(TestIntegration):

    def test_bucket_access_monitor(self):
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

        # put bucket access monitor
        result = self.client.put_bucket_access_monitor(oss.PutBucketAccessMonitorRequest(
                bucket=bucket_name,
                access_monitor_configuration=oss.AccessMonitorConfiguration(
                    status=oss.AccessMonitorStatusType.ENABLED
                ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket access monitor
        result = self.client.get_bucket_access_monitor(oss.GetBucketAccessMonitorRequest(
                bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(oss.AccessMonitorStatusType.ENABLED, result.access_monitor_configuration.status)

    def test_bucket_access_monitor_v1(self):
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

        # put bucket access monitor
        result = self.signv1_client.put_bucket_access_monitor(oss.PutBucketAccessMonitorRequest(
                bucket=bucket_name,
                access_monitor_configuration=oss.AccessMonitorConfiguration(
                    status=oss.AccessMonitorStatusType.ENABLED
                ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket access monitor
        result = self.signv1_client.get_bucket_access_monitor(oss.GetBucketAccessMonitorRequest(
                bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(oss.AccessMonitorStatusType.ENABLED, result.access_monitor_configuration.status)


    def test_bucket_access_monitor_fail(self):
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        try:
            self.invalid_client.put_bucket_access_monitor(oss.PutBucketAccessMonitorRequest(
                bucket=bucket_name,
                access_monitor_configuration=oss.AccessMonitorConfiguration(
                    status=oss.AccessMonitorStatusType.ENABLED
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
            self.invalid_client.get_bucket_access_monitor(oss.GetBucketAccessMonitorRequest(
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