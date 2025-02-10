# pylint: skip-file
import time
from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestCleanRestoredObject(TestIntegration):

    def test_clean_restored_object(self):
        key = 'demo.txt'
        data = b'hello world'
        bucket_name = random_bucket_name()

        # create bucket
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA',
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=key,
            storage_class='ColdArchive',
            body=data,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # clean restored object
        try:
            self.client.clean_restored_object(oss.CleanRestoredObjectRequest(
                bucket=bucket_name,
                key=key,
            ))
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(409, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('ArchiveRestoreFileStale', serr.code)

        # restore object
        self.client.restore_object(oss.RestoreObjectRequest(
            bucket=bucket_name,
            key=key,
            restore_request=oss.RestoreRequest(
                days=1,
                tier="Expedited",
            )
        ))

        time.sleep(1)

        # clean restored object
        try:
            self.client.clean_restored_object(oss.CleanRestoredObjectRequest(
                bucket=bucket_name,
                key=key,
            ))
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(409, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('ArchiveRestoreNotFinished', serr.code)


    def test_clean_restored_object_v1(self):
        key = 'demo.txt'
        data = b'hello world'
        bucket_name = random_bucket_name()

        # create bucket
        result = self.signv1_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA',
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        result = self.signv1_client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=key,
            storage_class='ColdArchive',
            body=data,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # clean restored object
        try:
            self.signv1_client.clean_restored_object(oss.CleanRestoredObjectRequest(
                bucket=bucket_name,
                key=key,
            ))
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(409, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('ArchiveRestoreFileStale', serr.code)

        # restore object
        self.signv1_client.restore_object(oss.RestoreObjectRequest(
            bucket=bucket_name,
            key=key,
            restore_request=oss.RestoreRequest(
                days=1,
                tier="Expedited",
            )
        ))

        time.sleep(1)

        # clean restored object
        try:
            self.signv1_client.clean_restored_object(oss.CleanRestoredObjectRequest(
                bucket=bucket_name,
                key=key,
            ))
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(409, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('ArchiveRestoreNotFinished', serr.code)


    def test_clean_restored_object_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # clean restored object
        try:
            self.invalid_client.clean_restored_object(oss.CleanRestoredObjectRequest(
                bucket=bucket_name,
                key='demo.jpg',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
