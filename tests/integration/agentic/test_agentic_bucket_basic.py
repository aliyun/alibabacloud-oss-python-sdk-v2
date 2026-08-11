# pylint: skip-file
from typing import cast
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic
from . import (
    TestIntegrationAgentic,
    get_invalid_ak_agentic_client,
    get_path_style_agentic_client,
)


class TestAgenticBucketBasic(TestIntegrationAgentic):
    """Basic agentic bucket integration tests."""

    def test_agentic_bucket_lifecycle(self):
        """Test get agentic bucket and list agentic buckets via paginator."""
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        # 1. Get agentic bucket
        result = client.get_agentic_bucket(
            oss_agentic.models.GetAgenticBucketRequest(bucket=bucket)
        )
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.agentic_bucket_info)
        self.assertIn(bucket, result.agentic_bucket_info.name)

        # 2. List agentic buckets via paginator, verify the created bucket appears
        found = False
        paginator = client.list_agentic_buckets_paginator()
        for page in paginator.iter_page(oss_agentic.models.ListAgenticBucketsRequest()):
            self.assertEqual(200, page.status_code)
            if page.agentic_buckets is None:
                continue
            for summary in page.agentic_buckets:
                if summary.name is not None and bucket in summary.name:
                    found = True
        self.assertTrue(found, "created agentic bucket should appear in list")

    def test_put_agentic_bucket_status(self):
        """Test put agentic bucket status."""
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        result = client.put_agentic_bucket_status(
            oss_agentic.models.PutAgenticBucketStatusRequest(
                bucket=bucket,
                agentic_bucket_status=oss_agentic.models.AgenticBucketStatus(
                    status='Enabled'
                ),
            )
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

    def test_get_agentic_bucket_not_exist(self):
        """Test get agentic bucket that does not exist returns 404."""
        client = self.agentic_client
        bucket = "oss-sdk-test-not-exist"

        try:
            client.get_agentic_bucket(
                oss_agentic.models.GetAgenticBucketRequest(bucket=bucket)
            )
            self.fail("Expected exception not thrown")

        except Exception as ec:
            ope = cast(oss.exceptions.OperationError, ec)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual("0015-00000101", serr.ec)
            self.assertEqual("NoSuchAgenticBucket", serr.code)

    def test_agentic_bucket_invalid_credentials(self):
        """Test agentic bucket operations with invalid credentials."""
        client = get_invalid_ak_agentic_client()
        bucket = "oss-sdk-test-invalid-cred"

        # Create with invalid AK
        try:
            client.create_agentic_bucket(
                oss_agentic.models.CreateAgenticBucketRequest(bucket=bucket)
            )
            self.fail("Expected exception not thrown")
        except Exception as ec:
            ope = cast(oss.exceptions.OperationError, ec)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual("0002-00000902", serr.ec)
            self.assertEqual("InvalidAccessKeyId", serr.code)
            self.assertTrue(serr.request_id)

        # Get with invalid AK
        try:
            client.get_agentic_bucket(
                oss_agentic.models.GetAgenticBucketRequest(bucket=bucket)
            )
            self.fail("Expected exception not thrown")
        except Exception as ec:
            ope = cast(oss.exceptions.OperationError, ec)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual("0015-00000101", serr.ec)
            self.assertEqual("NoSuchAgenticBucket", serr.code)

        # List with invalid AK
        try:
            client.list_agentic_buckets(
                oss_agentic.models.ListAgenticBucketsRequest()
            )
            self.fail("Expected exception not thrown")
        except Exception as ec:
            ope = cast(oss.exceptions.OperationError, ec)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual("0002-00000902", serr.ec)
            self.assertEqual("InvalidAccessKeyId", serr.code)

    @staticmethod
    def _find_cause(exc, exc_type):
        """Traverse exception chain to find the first instance of exc_type."""
        cause = exc
        while cause is not None:
            if isinstance(cause, exc_type):
                return cause
            cause = cause.__cause__
        return None

    def test_agentic_bucket_path_style(self):
        """Test agentic bucket operations using path-style addressing.

        Mirrors Go TestAgenticPathStyle: probe with GetAgenticBucket first;
        if the endpoint rejects path-style (SecondLevelDomainForbidden), skip
        rather than fail.
        """
        client = get_path_style_agentic_client()
        bucket = self.agentic_bucket_name

        # Probe: GetAgenticBucket via path-style
        try:
            result = client.get_agentic_bucket(
                oss_agentic.models.GetAgenticBucketRequest(bucket=bucket)
            )
        except oss.exceptions.OperationError as e:
            if 'SecondLevelDomainForbidden' in str(e):
                print(f'path-style addressing not allowed on this endpoint: {e}')
                return
            raise
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.agentic_bucket_info)
        self.assertIn(bucket, result.agentic_bucket_info.name)

        # ListAgenticBuckets via path-style client (URL is identical to virtual-hosted
        # since this is a service-level op with no bucket label)
        found = False
        paginator = client.list_agentic_buckets_paginator()
        for page in paginator.iter_page(oss_agentic.models.ListAgenticBucketsRequest()):
            self.assertEqual(200, page.status_code)
            if page.agentic_buckets is None:
                continue
            for summary in page.agentic_buckets:
                if summary.name is not None and bucket in summary.name:
                    found = True
        self.assertTrue(found, "agentic bucket should appear in list via path-style client")

        # ListBucketSpaces via path-style AgenticBucketClient
        result = client.list_bucket_spaces(
            oss_agentic.models.ListBucketSpacesRequest(bucket=bucket)
        )
        self.assertEqual(200, result.status_code)
