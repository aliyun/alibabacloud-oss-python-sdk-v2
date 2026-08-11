# pylint: skip-file

import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic
from . import TestIntegrationAgentic, USER_ID, get_path_style_agentic_client


class TestAgenticBucketAttribute(TestIntegrationAgentic):
    """Agentic bucket attribute integration tests (ACL, encryption, versioning, policy, public access block)."""

    def test_agentic_bucket_acl(self):
        """Test put and get agentic bucket ACL."""
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        # Put ACL
        result = client.put_agentic_bucket_acl(
            oss_agentic.models.PutAgenticBucketAclRequest(
                bucket=bucket,
                acl='private',
            )
        )
        self.assertEqual(200, result.status_code)

        # Get ACL
        result = client.get_agentic_bucket_acl(
            oss_agentic.models.GetAgenticBucketAclRequest(bucket=bucket)
        )
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.acl)
        self.assertEqual('private', result.acl)

    def test_agentic_bucket_encryption(self):
        """Test put, get, and delete agentic bucket encryption."""
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        # Put encryption
        result = client.put_agentic_bucket_encryption(
            oss_agentic.models.PutAgenticBucketEncryptionRequest(
                bucket=bucket,
                server_side_encryption_rule=oss.models.ServerSideEncryptionRule(
                    apply_server_side_encryption_by_default=oss.models.ApplyServerSideEncryptionByDefault(
                        sse_algorithm='AES256'
                    )
                ),
            )
        )
        self.assertEqual(200, result.status_code)

        # Get encryption
        result = client.get_agentic_bucket_encryption(
            oss_agentic.models.GetAgenticBucketEncryptionRequest(bucket=bucket)
        )
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.server_side_encryption_rule)
        self.assertIsNotNone(result.server_side_encryption_rule.apply_server_side_encryption_by_default)
        self.assertEqual('AES256', result.server_side_encryption_rule.apply_server_side_encryption_by_default.sse_algorithm)

        # Delete encryption
        result = client.delete_agentic_bucket_encryption(
            oss_agentic.models.DeleteAgenticBucketEncryptionRequest(bucket=bucket)
        )
        self.assertIn(result.status_code, [200, 204])

    def test_agentic_bucket_versioning(self):
        """Test put and get agentic bucket versioning."""
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        # Put versioning
        result = client.put_agentic_bucket_versioning(
            oss_agentic.models.PutAgenticBucketVersioningRequest(
                bucket=bucket,
                versioning_configuration=oss.models.VersioningConfiguration(
                    status='Enabled'
                ),
            )
        )
        self.assertEqual(200, result.status_code)

        # Get versioning
        result = client.get_agentic_bucket_versioning(
            oss_agentic.models.GetAgenticBucketVersioningRequest(bucket=bucket)
        )
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.version_status)
        self.assertEqual('Enabled', result.version_status)

    def test_agentic_bucket_policy(self):
        """Test put, get, and delete agentic bucket policy."""
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        policy = '{"Version":"1","Statement":[{"Effect":"Allow",' \
                 '"Action":["oss:GetObject"],"Principal":["' + USER_ID + '"],' \
                 '"Resource":["acs:oss:*:' + USER_ID + ':*"]}]}'

        # Put policy
        result = client.put_agentic_bucket_policy(
            oss_agentic.models.PutAgenticBucketPolicyRequest(
                bucket=bucket,
                body=policy.encode('utf-8'),
            )
        )
        self.assertEqual(200, result.status_code)

        # Get policy
        result = client.get_agentic_bucket_policy(
            oss_agentic.models.GetAgenticBucketPolicyRequest(bucket=bucket)
        )
        self.assertEqual(200, result.status_code)
        self.assertIn('oss:GetObject', result.body)

        # Delete policy
        result = client.delete_agentic_bucket_policy(
            oss_agentic.models.DeleteAgenticBucketPolicyRequest(bucket=bucket)
        )
        self.assertIn(result.status_code, [200, 204])

    def test_agentic_bucket_public_access_block(self):
        """Test put, get, and delete agentic bucket public access block."""
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        # Put public access block
        result = client.put_agentic_bucket_public_access_block(
            oss_agentic.models.PutAgenticBucketPublicAccessBlockRequest(
                bucket=bucket,
                public_access_block_configuration=oss.models.PublicAccessBlockConfiguration(
                    block_public_access=True
                ),
            )
        )
        self.assertEqual(200, result.status_code)

        # Get public access block
        result = client.get_agentic_bucket_public_access_block(
            oss_agentic.models.GetAgenticBucketPublicAccessBlockRequest(bucket=bucket)
        )
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.public_access_block_configuration)

        # Delete public access block
        result = client.delete_agentic_bucket_public_access_block(
            oss_agentic.models.DeleteAgenticBucketPublicAccessBlockRequest(bucket=bucket)
        )
        self.assertIn(result.status_code, [200, 204])

    def test_agentic_bucket_acl_path_style(self):
        """Test put and get agentic bucket ACL using path-style addressing.

        Mirrors Go TestAgenticPathStyle probe: if the endpoint rejects path-style
        (SecondLevelDomainForbidden), skip rather than fail.
        """
        client = get_path_style_agentic_client()
        bucket = self.agentic_bucket_name

        # Probe: Put ACL via path-style client
        try:
            result = client.put_agentic_bucket_acl(
                oss_agentic.models.PutAgenticBucketAclRequest(
                    bucket=bucket,
                    acl='private',
                )
            )
        except oss.exceptions.OperationError as e:
            if 'SecondLevelDomainForbidden' in str(e):
                print(f'path-style addressing not allowed on this endpoint: {e}')
                return
            raise
        self.assertEqual(200, result.status_code)

        # Get ACL via path-style client
        result = client.get_agentic_bucket_acl(
            oss_agentic.models.GetAgenticBucketAclRequest(bucket=bucket)
        )
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.acl)
        self.assertEqual('private', result.acl)
