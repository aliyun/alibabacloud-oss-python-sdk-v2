# pylint: skip-file
import time
from typing import cast
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.aio as oss_aio
from . import TestIntegration, random_bucket_name


class TestBucketObjectWormConfigurationAsync(TestIntegration):

    def setUp(self):
        """Set up test fixtures."""
        # Load credentials from environment variables
        credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
        
        # Using the SDK's default configuration
        self.cfg = oss.config.load_default()
        self.cfg.credentials_provider = credentials_provider
        self.cfg.region = 'cn-hangzhou'  # Default region for testing
        
        self.async_client = oss_aio.AsyncClient(self.cfg)

    async def asyncTearDown(self):
        """Tear down test fixtures."""
        if hasattr(self, 'async_client'):
            await self.async_client.close()

    async def test_bucket_object_worm_configuration(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
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

        # enable versioning
        result = await self.async_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        time.sleep(1)

        # put bucket object worm configuration with GOVERNANCE mode and 1 day
        result = await self.async_client.put_bucket_object_worm_configuration(oss.PutBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
            object_worm_configuration=oss.ObjectWormConfiguration(
                object_worm_enabled='Enabled',
                rule=oss.ObjectWormConfigurationRule(
                    default_retention=oss.ObjectWormConfigurationRuleDefaultRetention(
                        mode=oss.ObjectWormConfigurationModeType.GOVERNANCE,
                        days=1,
                    ),
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        time.sleep(5)

        # get bucket object worm configuration
        result = await self.async_client.get_bucket_object_worm_configuration(oss.GetBucketObjectWormConfigurationRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('Enabled', result.object_worm_configuration.object_worm_enabled)
        self.assertEqual(oss.ObjectWormConfigurationModeType.GOVERNANCE, result.object_worm_configuration.rule.default_retention.mode)
        self.assertEqual(1, result.object_worm_configuration.rule.default_retention.days)
