# pylint: skip-file

import time
from typing import cast

import alibabacloud_oss_v2 as oss
from . import TestIntegration


class TestBucketMetadataConfiguration(TestIntegration):
    client: oss.Client
    invalid_client: oss.Client
    bucket_name: str

    def test_bucket_metadata_configuration(self):
        created = False
        try:
            # create bucket metadata configuration
            result = self.client.create_bucket_metadata_configuration(
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
            self.assertEqual(24, len(result.request_id))
            created = True

            # get bucket metadata configuration until the journal table is active
            configuration = None
            for _ in range(24):
                result = self.client.get_bucket_metadata_configuration(
                    oss.GetBucketMetadataConfigurationRequest(bucket=self.bucket_name)
                )
                self.assertEqual(200, result.status_code)
                configuration = result.metadata_configuration_result
                if configuration.journal_table_configuration_result.table_status == oss.TableStatusType.ACTIVE:
                    break
                time.sleep(5)

            self.assertIsNotNone(configuration)
            self.assertEqual('oss', configuration.destination_result.table_bucket_type)
            self.assertEqual('journal', configuration.journal_table_configuration_result.table_name)
            self.assertEqual(oss.TableStatusType.ACTIVE,
                             configuration.journal_table_configuration_result.table_status)

            # update bucket metadata journal table configuration
            result = self.client.update_bucket_metadata_journal_table_configuration(
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
            result = self.client.update_bucket_metadata_inventory_table_configuration(
                oss.UpdateBucketMetadataInventoryTableConfigurationRequest(
                    bucket=self.bucket_name,
                    inventory_table_configuration=oss.InventoryTableConfiguration(
                        configuration_state=oss.ConfigurationStateType.ENABLED,
                    ),
                )
            )
            self.assertEqual(200, result.status_code)

            # get bucket metadata configuration again to verify the updates took effect
            result = self.client.get_bucket_metadata_configuration(
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
                result = self.client.delete_bucket_metadata_configuration(
                    oss.DeleteBucketMetadataConfigurationRequest(bucket=self.bucket_name)
                )
                self.assertEqual(204, result.status_code)

    def test_bucket_metadata_configuration_fail(self):
        try:
            # create bucket metadata configuration with an invalid client should fail
            self.invalid_client.create_bucket_metadata_configuration(
                oss.CreateBucketMetadataConfigurationRequest(
                    bucket=self.bucket_name,
                    metadata_configuration=oss.MetadataConfiguration(
                        journal_table_configuration=oss.JournalTableConfiguration(
                            record_expiration=oss.RecordExpiration(
                                expiration=oss.RecordExpirationType.DISABLED,
                            ),
                        ),
                    ),
                )
            )
            self.fail('should not here')
        except Exception as error:
            operation_error = cast(oss.exceptions.OperationError, error)
            self.assertIsInstance(operation_error.unwrap(), oss.exceptions.ServiceError)
            service_error = cast(oss.exceptions.ServiceError, operation_error.unwrap())
            self.assertEqual(403, service_error.status_code)
            self.assertEqual('InvalidAccessKeyId', service_error.code)
