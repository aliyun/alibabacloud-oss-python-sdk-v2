# pylint: skip-file

import time
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic
from . import (
    TestIntegrationAgentic,
    get_bucket_space_client,
    get_path_style_bucket_space_client,
    gen_bucket_space_prefix,
    REGION,
    USER_ID,
)


class TestAgenticBucketSpace(TestIntegrationAgentic):
    """BucketSpace lifecycle integration tests."""

    def test_bucket_space_lifecycle_via_bucket_space_client(self):
        """
        BucketSpace lifecycle via BucketSpaceClient:
        Pass the short prefix only; BucketSpaceClient auto-expands to
        {prefix}-{uid}-{region}-bs-apsr.

        Note: BucketSpaceClient returns a standard OSSClient, so list_bucket_spaces
        (an AgenticBucketClient-only operation) is NOT available through it.
        """
        bs_prefix = gen_bucket_space_prefix()
        expected_full_name = f"{bs_prefix}-{USER_ID}-{REGION}-bs-apsr"

        bs_client = get_bucket_space_client()
        try:
            # 1. PutBucket (reused) - BucketSpaceClient auto-expands prefix to full name
            result = bs_client.put_bucket(
                oss.models.PutBucketRequest(
                    bucket=bs_prefix,
                    agentic_bucket=self.full_agentic_bucket_name,
                )
            )
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)
            time.sleep(1)

            # 2. GetBucketInfo (reused) - verify via BucketSpaceClient
            result = bs_client.get_bucket_info(
                oss.models.GetBucketInfoRequest(bucket=bs_prefix)
            )
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)
            self.assertEqual("AgenticBucketSpace", result.bucket_info.bucket_resource_type)
            self.assertIsNotNone(result.bucket_info.agentic_bucket_name)

            # 3. ListBucketSpaces - cross-verify the created BucketSpace via agentic_client
            result = self.agentic_client.list_bucket_spaces(
                oss_agentic.models.ListBucketSpacesRequest(
                    bucket=self.agentic_bucket_name,
                    prefix=bs_prefix,
                )
            )
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)
            found = False
            if result.bucket_spaces is not None:
                for bs in result.bucket_spaces:
                    if expected_full_name == bs.name:
                        found = True
                        break
            self.assertTrue(found, "BucketSpaceClient-created BucketSpace should appear in list")

        finally:
            # 4. DeleteBucket (reused) - cleanup via BucketSpaceClient
            try:
                bs_client.delete_bucket(
                    oss.models.DeleteBucketRequest(bucket=bs_prefix)
                )
            except Exception:
                pass

    def test_bucket_space_lifecycle_via_standard_client(self):
        """
        BucketSpace lifecycle via standard OSSClient:
        Pass the full BucketSpace name {prefix}-{uid}-{region}-bs-apsr directly.

        This test requires manually constructing the full bucket name.
        """
        bs_prefix = gen_bucket_space_prefix()
        bs_full_name = f"{bs_prefix}-{USER_ID}-{REGION}-bs-apsr"

        try:
            # 1. PutBucket - standard OSSClient with full BucketSpace name
            result = self.client.put_bucket(
                oss.models.PutBucketRequest(
                    bucket=bs_full_name,
                    agentic_bucket=self.full_agentic_bucket_name,
                )
            )
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)
            time.sleep(1)

            # 2. GetBucketInfo - verify BucketResourceType
            result = self.client.get_bucket_info(
                oss.models.GetBucketInfoRequest(bucket=bs_full_name)
            )
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)
            # Note: bucket_resource_type may not be set when not using BucketSpaceClient
            # so we just verify the bucket exists

            # 3. ListBucketSpaces - verify the created BucketSpace via AgenticBucketClient
            result = self.agentic_client.list_bucket_spaces(
                oss_agentic.models.ListBucketSpacesRequest(
                    bucket=self.agentic_bucket_name,
                    prefix=bs_prefix,
                )
            )
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)
            found = False
            if result.bucket_spaces is not None:
                for bs in result.bucket_spaces:
                    if bs_full_name == bs.name:
                        found = True
                        break
            self.assertTrue(found, "Created BucketSpace should appear in list")

        finally:
            # 4. DeleteBucket - cleanup
            try:
                self.client.delete_bucket(
                    oss.models.DeleteBucketRequest(bucket=bs_full_name)
                )
            except Exception:
                pass

    def test_bucket_space_object_operations_path_style(self):
        """
        BucketSpace object operations via path-style BucketSpaceClient:
        Verifies put_object / get_object / delete_object work correctly
        with use_path_style=True, mirroring TestBucketSpaceClientMockPathStyle.
        """
        bs_prefix = gen_bucket_space_prefix()

        # Create BucketSpace via standard client first
        std_client = get_bucket_space_client()
        result = std_client.put_bucket(
            oss.models.PutBucketRequest(
                bucket=bs_prefix,
                agentic_bucket=self.full_agentic_bucket_name,
            )
        )
        self.assertEqual(200, result.status_code)
        time.sleep(1)

        try:
            # Use path-style client for object operations
            path_client = get_path_style_bucket_space_client()
            key = 'path-style-test.txt'
            body = b'hello path style'

            # put_object via path-style
            try:
                result = path_client.put_object(
                    oss.models.PutObjectRequest(
                        bucket=bs_prefix,
                        key=key,
                        body=body,
                    )
                )
                self.assertEqual(200, result.status_code)
            except oss.exceptions.OperationError as e:
                if 'SecondLevelDomainForbidden' in str(e):
                    print(f'put_object path-style not supported: {e}')
                else:
                    raise

            # get_object via path-style
            try:
                result = path_client.get_object(
                    oss.models.GetObjectRequest(
                        bucket=bs_prefix,
                        key=key,
                    )
                )
                self.assertEqual(200, result.status_code)
                self.assertEqual(body, result.body.content.read())
            except oss.exceptions.OperationError as e:
                if 'SecondLevelDomainForbidden' in str(e):
                    print(f'get_object path-style not supported: {e}')
                else:
                    raise

            # delete_object via path-style
            try:
                result = path_client.delete_object(
                    oss.models.DeleteObjectRequest(
                        bucket=bs_prefix,
                        key=key,
                    )
                )
                self.assertEqual(204, result.status_code)
            except oss.exceptions.OperationError as e:
                if 'SecondLevelDomainForbidden' in str(e):
                    print(f'delete_object path-style not supported: {e}')
                else:
                    raise

            # get_bucket_acl via path-style
            try:
                result = path_client.get_bucket_acl(
                    oss.models.GetBucketAclRequest(bucket=bs_prefix)
                )
                self.assertEqual(200, result.status_code)
                self.assertIsNotNone(result.acl)
            except oss.exceptions.OperationError as e:
                if 'SecondLevelDomainForbidden' in str(e):
                    print(f'get_bucket_acl path-style not supported: {e}')
                else:
                    raise

        finally:
            # Cleanup BucketSpace
            try:
                std_client.delete_bucket(
                    oss.models.DeleteBucketRequest(bucket=bs_prefix)
                )
            except Exception:
                pass
