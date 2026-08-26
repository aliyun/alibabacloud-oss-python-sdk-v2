# pylint: skip-file
"""The two-phase deletion of an agentic bucket.

put_agentic_bucket_status(Disabled) succeeds, but the bucket only becomes deletable roughly 24 hours
later, so the delete_agentic_bucket that follows immediately is answered with
409 / AgenticBucketNotReady. A create-then-delete round trip is therefore impossible within a single
run and the 409 is what gets asserted; the reaper reclaims the bucket in a later run.

The scenario runs against the bucket created by the setUpClass of this class only, so that disabling
it cannot disturb the scenarios of the sibling test classes: unittest guarantees no order between
classes, and every class gets its own bucket.
"""

from typing import cast
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic
from . import TestIntegrationAgentic


class TestAgenticBucketLifecycle(TestIntegrationAgentic):
    """Agentic bucket two-phase deletion integration test."""

    def test_disable_then_delete_not_ready(self):
        """Test disable then delete agentic bucket returns 409 AgenticBucketNotReady."""
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        result = client.put_agentic_bucket_status(
            oss_agentic.models.PutAgenticBucketStatusRequest(
                bucket=bucket,
                agentic_bucket_status=oss_agentic.models.AgenticBucketStatus(status='Disabled'),
            )
        )
        self.assertEqual(200, result.status_code)

        try:
            client.delete_agentic_bucket(
                oss_agentic.models.DeleteAgenticBucketRequest(bucket=bucket)
            )
            self.fail("Expected exception not thrown")
        except Exception as ec:
            ope = cast(oss.exceptions.OperationError, ec)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertTrue(
                serr.status_code == 409 or serr.code == 'AgenticBucketNotReady',
                f'expected 409/AgenticBucketNotReady, got status={serr.status_code} code={serr.code}'
            )
