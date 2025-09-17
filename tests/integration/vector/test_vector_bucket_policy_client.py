# pylint: skip-file
import time
import alibabacloud_oss_v2.vectors as oss_vectors
from tests.integration import TestIntegrationVectors, random_short_bucket_name


class TestVectorBucketBasic(TestIntegrationVectors):

    def test_vector_bucket_policy(self):
        # create bucket
        bucket_name = random_short_bucket_name()
        result = self.vector_client.put_vector_bucket(oss_vectors.models.PutVectorBucketRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        policy_text = ''
        policy_text += '{'
        policy_text += '"Version":"1",'
        policy_text += '"Statement":[{'
        policy_text += '"Action":["ossvector:PutVectors","ossvector:GetVectors"],'
        policy_text += '"Effect":"Deny",'
        policy_text += '"Principal":["1234567890"],'
        policy_text += f'"Resource": ["acs:ossvector:*:*:{bucket_name}","acs:oss:*:*:{bucket_name}/*"]'
        policy_text += '}]}'

        # put bucket policy
        result = self.vector_client.put_bucket_policy(oss_vectors.models.PutBucketPolicyRequest(
            bucket=bucket_name,
            body=policy_text,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        time.sleep(1)

        # get bucket policy
        result = self.vector_client.get_bucket_policy(oss_vectors.models.GetBucketPolicyRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(policy_text, result.body)

        # delete bucket policy
        result = self.vector_client.delete_bucket_policy(oss_vectors.models.DeleteBucketPolicyRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # delete bucket (cleanup)
        result = self.vector_client.delete_vector_bucket(oss_vectors.models.DeleteVectorBucketRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

