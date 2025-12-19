# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketPolicy(TestIntegration):

    def test_bucket_policy(self):
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

        self.client.put_bucket_public_access_block(oss.PutBucketPublicAccessBlockRequest(
            bucket=bucket_name,
            public_access_block_configuration=oss.PublicAccessBlockConfiguration(
                block_public_access=False
            )
        ))

        policy_text = ''
        policy_text += '{'
        policy_text += '"Version":"1",'
        policy_text += '"Statement":[{'
        policy_text += '"Action":["oss:PutObject"],'
        policy_text += '"Effect":"Allow",'
        policy_text += f'"Resource": ["acs:oss:*:*:{bucket_name}","acs:oss:*:*:{bucket_name}/*"]'
        policy_text += '}]}'

        # put bucket policy
        result = self.client.put_bucket_policy(oss.PutBucketPolicyRequest(
            bucket=bucket_name,
            body=policy_text,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket policy
        result = self.client.get_bucket_policy(oss.GetBucketPolicyRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(policy_text, result.body)

        # get bucket policy status
        result = self.client.get_bucket_policy_status(oss.GetBucketPolicyStatusRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(True, result.policy_status.is_public)

        # delete bucket policy
        result = self.client.delete_bucket_policy(oss.DeleteBucketPolicyRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket policy status
        result = self.client.get_bucket_policy_status(oss.GetBucketPolicyStatusRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(False, result.policy_status.is_public)

    def test_bucket_policy_v1(self):
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
        
        self.signv1_client.put_bucket_public_access_block(oss.PutBucketPublicAccessBlockRequest(
            bucket=bucket_name,
            public_access_block_configuration=oss.PublicAccessBlockConfiguration(
                block_public_access=False
            )
        ))

        policy_text = ''
        policy_text += '{'
        policy_text += '"Version":"1",'
        policy_text += '"Statement":[{'
        policy_text += '"Action":["oss:PutObject"],'
        policy_text += '"Effect":"Allow",'
        policy_text += f'"Resource": ["acs:oss:*:*:{bucket_name}","acs:oss:*:*:{bucket_name}/*"]'
        policy_text += '}]}'

        # put bucket policy
        result = self.signv1_client.put_bucket_policy(oss.PutBucketPolicyRequest(
            bucket=bucket_name,
            body=policy_text,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket policy
        result = self.signv1_client.get_bucket_policy(oss.GetBucketPolicyRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(policy_text, result.body)

        # get bucket policy status
        result = self.signv1_client.get_bucket_policy_status(oss.GetBucketPolicyStatusRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(True, result.policy_status.is_public)

        # delete bucket policy
        result = self.signv1_client.delete_bucket_policy(oss.DeleteBucketPolicyRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket policy status
        result = self.client.get_bucket_policy_status(oss.GetBucketPolicyStatusRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(False, result.policy_status.is_public)

    def test_bucket_policy_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        self.client.put_bucket_public_access_block(oss.PutBucketPublicAccessBlockRequest(
            bucket=bucket_name,
            public_access_block_configuration=oss.PublicAccessBlockConfiguration(
                block_public_access=False
            )
        ))

        policy = '{"Version":"1","Statement":[]}'

        # put bucket policy
        try:
            self.invalid_client.put_bucket_policy(oss.PutBucketPolicyRequest(
                bucket=bucket_name,
                body=policy,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # get bucket policy
        try:
            self.invalid_client.get_bucket_policy(oss.GetBucketPolicyRequest(
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

        # get bucket policy status
        try:
            self.invalid_client.get_bucket_policy_status(oss.GetBucketPolicyStatusRequest(
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

        # delete bucket policy
        try:
            self.invalid_client.delete_bucket_policy(oss.DeleteBucketPolicyRequest(
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
