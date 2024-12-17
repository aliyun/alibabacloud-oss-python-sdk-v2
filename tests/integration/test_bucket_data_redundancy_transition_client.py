# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketDataRedundancyTransition(TestIntegration):

    def test_bucket_data_redundancy_transition(self):
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

        # create bucket data redundancy transition
        result = self.client.create_bucket_data_redundancy_transition(oss.CreateBucketDataRedundancyTransitionRequest(
            bucket=bucket_name,
            target_redundancy_type='ZRS',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        redundancy_transition_taskid = result.bucket_data_redundancy_transition.task_id;

        # get bucket data redundancy transition
        result = self.client.get_bucket_data_redundancy_transition(oss.GetBucketDataRedundancyTransitionRequest(
            bucket=bucket_name,
            redundancy_transition_taskid=redundancy_transition_taskid,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.bucket_data_redundancy_transition.bucket)
        self.assertEqual(redundancy_transition_taskid, result.bucket_data_redundancy_transition.task_id)
        self.assertIsNotNone(result.bucket_data_redundancy_transition.status)
        self.assertIsNotNone(result.bucket_data_redundancy_transition.create_time)

        # list bucket data redundancy transition
        result = self.client.list_bucket_data_redundancy_transition(oss.ListBucketDataRedundancyTransitionRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].bucket)
        self.assertEqual(redundancy_transition_taskid, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].task_id)
        self.assertIsNotNone(result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].status)
        self.assertIsNotNone(result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].create_time)

        # list user data redundancy transition
        result = self.client.list_user_data_redundancy_transition(oss.ListUserDataRedundancyTransitionRequest(
            max_keys=10,
            continuation_token='',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].bucket)
        self.assertEqual(redundancy_transition_taskid, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].task_id)
        self.assertIsNotNone(result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].status)
        self.assertIsNotNone(result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].create_time)

        # delete bucket data redundancy transition
        result = self.client.delete_bucket_data_redundancy_transition(oss.DeleteBucketDataRedundancyTransitionRequest(
            bucket=bucket_name,
            redundancy_transition_taskid=redundancy_transition_taskid,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_data_redundancy_transition_v1(self):
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


        # create bucket data redundancy transition
        result = self.signv1_client.create_bucket_data_redundancy_transition(oss.CreateBucketDataRedundancyTransitionRequest(
            bucket=bucket_name,
            target_redundancy_type='ZRS',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        redundancy_transition_taskid = result.bucket_data_redundancy_transition.task_id;

        # get bucket data redundancy transition
        result = self.signv1_client.get_bucket_data_redundancy_transition(oss.GetBucketDataRedundancyTransitionRequest(
            bucket=bucket_name,
            redundancy_transition_taskid=redundancy_transition_taskid,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.bucket_data_redundancy_transition.bucket)
        self.assertEqual(redundancy_transition_taskid, result.bucket_data_redundancy_transition.task_id)
        self.assertIsNotNone(result.bucket_data_redundancy_transition.status)
        self.assertIsNotNone(result.bucket_data_redundancy_transition.create_time)

        # list bucket data redundancy transition
        result = self.signv1_client.list_bucket_data_redundancy_transition(oss.ListBucketDataRedundancyTransitionRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].bucket)
        self.assertEqual(redundancy_transition_taskid, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].task_id)
        self.assertIsNotNone(result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].status)
        self.assertIsNotNone(result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].create_time)

        # list user data redundancy transition
        result = self.signv1_client.list_user_data_redundancy_transition(oss.ListUserDataRedundancyTransitionRequest(
            max_keys=10,
            continuation_token='',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].bucket)
        self.assertEqual(redundancy_transition_taskid, result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].task_id)
        self.assertIsNotNone(result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].status)
        self.assertIsNotNone(result.list_bucket_data_redundancy_transition.bucket_data_redundancy_transition[0].create_time)

        # delete bucket data redundancy transition
        result = self.signv1_client.delete_bucket_data_redundancy_transition(oss.DeleteBucketDataRedundancyTransitionRequest(
            bucket=bucket_name,
            redundancy_transition_taskid=redundancy_transition_taskid,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_bucket_data_redundancy_transition_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # create bucket data redundancy transition
        try:
            self.invalid_client.create_bucket_data_redundancy_transition(oss.CreateBucketDataRedundancyTransitionRequest(
                bucket=bucket_name,
                target_redundancy_type='test_target_redundancy_type',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # get bucket data redundancy transition
        try:
            self.invalid_client.get_bucket_data_redundancy_transition(oss.GetBucketDataRedundancyTransitionRequest(
                bucket=bucket_name,
                redundancy_transition_taskid='test_redundancy_transition_taskid',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # list bucket data redundancy transition
        try:
            self.invalid_client.list_bucket_data_redundancy_transition(oss.ListBucketDataRedundancyTransitionRequest(
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

        # list user data redundancy transition
        try:
            self.invalid_client.list_user_data_redundancy_transition(oss.ListUserDataRedundancyTransitionRequest(
                max_keys=10,
                continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # delete bucket data redundancy transition
        try:
            self.invalid_client.delete_bucket_data_redundancy_transition(oss.DeleteBucketDataRedundancyTransitionRequest(
                bucket=bucket_name,
                redundancy_transition_taskid='test_redundancy_transition_taskid',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)