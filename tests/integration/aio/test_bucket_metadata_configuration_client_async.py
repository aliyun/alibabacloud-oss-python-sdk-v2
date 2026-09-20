# pylint: skip-file

import asyncio
import unittest
from typing import cast

import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.aio as oss_aio
from .. import ENDPOINT, REGION, TestIntegration, get_async_client


class TestBucketMetadataConfigurationAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):
    async_client: oss_aio.AsyncClient
    invalid_async_client: oss_aio.AsyncClient
    bucket_name: str

    async def asyncSetUp(self):
        self.async_client = get_async_client(REGION, ENDPOINT)
        self.invalid_async_client = get_async_client(
            REGION,
            ENDPOINT,
            oss.credentials.StaticCredentialsProvider('invalid-ak', 'invalid'),
        )

    async def asyncTearDown(self):
        await self.async_client.close()
        await self.invalid_async_client.close()
        await asyncio.sleep(0.25)

    async def test_bucket_metadata_configuration(self):
        created = False
        try:
            # create bucket metadata configuration
            result = await self.async_client.create_bucket_metadata_configuration(
                oss.CreateBucketMetadataConfigurationRequest(
                    bucket=self.bucket_name,
                    metadata_configuration=oss.MetadataConfiguration(
                        journal_table_configuration=oss.JournalTableConfiguration(
                            record_expiration=oss.RecordExpiration(
                                expiration=oss.RecordExpirationType.ENABLED,
                                days=7,
                            ),
                        ),
                        inventory_table_configuration=oss.InventoryTableConfiguration(
                            configuration_state=oss.ConfigurationStateType.DISABLED,
                        ),
                    ),
                )
            )
            self.assertEqual(200, result.status_code)
            created = True

            # get bucket metadata configuration until the journal table is active
            configuration = None
            for _ in range(24):
                result = await self.async_client.get_bucket_metadata_configuration(
                    oss.GetBucketMetadataConfigurationRequest(bucket=self.bucket_name)
                )
                configuration = result.metadata_configuration_result
                if configuration.journal_table_configuration_result.table_status == oss.TableStatusType.ACTIVE:
                    break
                await asyncio.sleep(5)

            self.assertIsNotNone(configuration)
            self.assertEqual(oss.TableStatusType.ACTIVE,
                             configuration.journal_table_configuration_result.table_status)

            # update bucket metadata journal table configuration
            result = await self.async_client.update_bucket_metadata_journal_table_configuration(
                oss.UpdateBucketMetadataJournalTableConfigurationRequest(
                    bucket=self.bucket_name,
                    journal_table_configuration=oss.JournalTableConfiguration(
                        record_expiration=oss.RecordExpiration(
                            expiration=oss.RecordExpirationType.DISABLED,
                        ),
                    ),
                )
            )
            self.assertEqual(200, result.status_code)

            # update bucket metadata inventory table configuration
            result = await self.async_client.update_bucket_metadata_inventory_table_configuration(
                oss.UpdateBucketMetadataInventoryTableConfigurationRequest(
                    bucket=self.bucket_name,
                    inventory_table_configuration=oss.InventoryTableConfiguration(
                        configuration_state=oss.ConfigurationStateType.ENABLED,
                    ),
                )
            )
            self.assertEqual(200, result.status_code)

            # get bucket metadata configuration again to verify the updates took effect
            result = await self.async_client.get_bucket_metadata_configuration(
                oss.GetBucketMetadataConfigurationRequest(bucket=self.bucket_name)
            )
            self.assertEqual(200, result.status_code)
            configuration = result.metadata_configuration_result
            self.assertEqual(oss.RecordExpirationType.DISABLED,
                             configuration.journal_table_configuration_result.record_expiration.expiration)
            self.assertEqual(oss.ConfigurationStateType.ENABLED,
                             configuration.inventory_table_configuration_result.configuration_state)
        finally:
            if created:
                # delete bucket metadata configuration
                result = await self.async_client.delete_bucket_metadata_configuration(
                    oss.DeleteBucketMetadataConfigurationRequest(bucket=self.bucket_name)
                )
                self.assertEqual(204, result.status_code)

    async def test_bucket_metadata_configuration_fail(self):
        try:
            # get bucket metadata configuration with an invalid client should fail
            await self.invalid_async_client.get_bucket_metadata_configuration(
                oss.GetBucketMetadataConfigurationRequest(bucket=self.bucket_name)
            )
            self.fail('should not here')
        except Exception as error:
            operation_error = cast(oss.exceptions.OperationError, error)
            self.assertIsInstance(operation_error.unwrap(), oss.exceptions.ServiceError)
            service_error = cast(oss.exceptions.ServiceError, operation_error.unwrap())
            self.assertEqual(403, service_error.status_code)
            self.assertEqual('InvalidAccessKeyId', service_error.code)
