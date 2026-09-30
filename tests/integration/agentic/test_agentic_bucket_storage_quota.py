# pylint: skip-file

import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic
from . import TestIntegrationAgentic


def _quota_disabled(err) -> bool:
    """The storage quota feature must be enabled per account; when it is not, the service
    answers 403 BucketStorageQuotaDisabled and the scenario should be skipped, not failed.
    """
    return 'BucketStorageQuotaDisabled' in str(err)


class TestAgenticBucketStorageQuota(TestIntegrationAgentic):
    """Agent Bucket level default storage quota integration tests.

    The quota set on an Agent Bucket is only the default value applied to bucket spaces
    created afterwards; it is not a capacity cap of the Agent Bucket itself.
    """

    def test_agentic_bucket_storage_quota(self):
        """Create -> get -> delete the Agent Bucket default storage quota."""
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        try:
            # 1. PutAgenticBucketStorageQuota - set the default quota (Strict mode).
            result = client.put_agentic_bucket_storage_quota(
                oss_agentic.models.PutAgenticBucketStorageQuotaRequest(
                    bucket=bucket,
                    quota_configuration=oss.QuotaConfiguration(
                        storage_quota=104857600,
                        mode='Strict',
                    ),
                )
            )
            self.assertEqual(200, result.status_code)

            # 2. GetAgenticBucketStorageQuota - read the configuration back.
            #    The Agent Bucket level result carries no CurrentUsage.
            result = client.get_agentic_bucket_storage_quota(
                oss_agentic.models.GetAgenticBucketStorageQuotaRequest(bucket=bucket)
            )
            self.assertEqual(200, result.status_code)
            self.assertIsNotNone(result.quota_configuration)
            self.assertEqual('Strict', result.quota_configuration.mode)
            self.assertEqual(104857600, result.quota_configuration.storage_quota)
            self.assertIsNone(result.quota_configuration.current_usage)

            # 3. PutAgenticBucketStorageQuota again - a repeat call overwrites the previous
            #    configuration, switch to Warning mode to verify the overwrite behaviour.
            result = client.put_agentic_bucket_storage_quota(
                oss_agentic.models.PutAgenticBucketStorageQuotaRequest(
                    bucket=bucket,
                    quota_configuration=oss.QuotaConfiguration(
                        storage_quota=209715200,
                        mode='Warning',
                    ),
                )
            )
            self.assertEqual(200, result.status_code)

            result = client.get_agentic_bucket_storage_quota(
                oss_agentic.models.GetAgenticBucketStorageQuotaRequest(bucket=bucket)
            )
            self.assertEqual(200, result.status_code)
            self.assertEqual('Warning', result.quota_configuration.mode)
            self.assertEqual(209715200, result.quota_configuration.storage_quota)

            # 4. DeleteAgenticBucketStorageQuota - remove the default quota.
            result = client.delete_agentic_bucket_storage_quota(
                oss_agentic.models.DeleteAgenticBucketStorageQuotaRequest(bucket=bucket)
            )
            self.assertIn(result.status_code, [200, 204])

            # 5. GetAgenticBucketStorageQuota after delete - the configuration is gone (404).
            try:
                client.get_agentic_bucket_storage_quota(
                    oss_agentic.models.GetAgenticBucketStorageQuotaRequest(bucket=bucket)
                )
                self.fail('expected NoSuchBucketStorageQuotaConfiguration after delete')
            except oss.exceptions.OperationError as e:
                self.assertIn('NoSuchBucketStorageQuotaConfiguration', str(e))

        except oss.exceptions.OperationError as e:
            if _quota_disabled(e):
                print(f'storage quota feature disabled, skip: {e}')
                return
            raise
        finally:
            # Best-effort cleanup so the shared Agent Bucket is left without a default quota.
            try:
                client.delete_agentic_bucket_storage_quota(
                    oss_agentic.models.DeleteAgenticBucketStorageQuotaRequest(bucket=bucket)
                )
            except Exception:
                pass

    def test_agentic_bucket_storage_quota_delete_idempotent(self):
        """DeleteAgenticBucketStorageQuota is idempotent: deleting a non-existent
        configuration still returns 204.
        """
        client = self.agentic_client
        bucket = self.agentic_bucket_name

        try:
            # Make sure no default quota is configured, then delete twice.
            client.delete_agentic_bucket_storage_quota(
                oss_agentic.models.DeleteAgenticBucketStorageQuotaRequest(bucket=bucket)
            )
            result = client.delete_agentic_bucket_storage_quota(
                oss_agentic.models.DeleteAgenticBucketStorageQuotaRequest(bucket=bucket)
            )
            self.assertIn(result.status_code, [200, 204])
        except oss.exceptions.OperationError as e:
            if _quota_disabled(e):
                print(f'storage quota feature disabled, skip: {e}')
                return
            raise
