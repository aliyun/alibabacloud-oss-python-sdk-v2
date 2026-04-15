# pylint: skip-file

import json
import alibabacloud_oss_v2.tables as oss_tables
from . import TestIntegrationTables


class TestTableBucketConfig(TestIntegrationTables):

    def test_table_bucket_encryption(self):
        # Put table bucket encryption
        result = self.tables_client.put_table_bucket_encryption(
            oss_tables.models.PutTableBucketEncryptionRequest(
                table_bucket_arn=self.table_bucket_arn,
                encryption_configuration=oss_tables.models.EncryptionConfiguration(
                    sse_algorithm='AES256',
                ),
            )
        )

        self.assertEqual(200, result.status_code)

        # Get table bucket encryption
        result = self.tables_client.get_table_bucket_encryption(
            oss_tables.models.GetTableBucketEncryptionRequest(
                table_bucket_arn=self.table_bucket_arn,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.encryption_configuration)

        # Delete table bucket encryption
        result = self.tables_client.delete_table_bucket_encryption(
            oss_tables.models.DeleteTableBucketEncryptionRequest(
                table_bucket_arn=self.table_bucket_arn,
            )
        )

        self.assertEqual(204, result.status_code)



    def test_table_bucket_policy(self):
        policy_document = "{\"Version\":\"1\",\"Statement\":[{\"Action\":[\"oss:GetTable\"],\"Effect\":\"Deny\",\"Principal\":[\"1234567890\"],\"Resource\":[\"acs:osstable:cn-hangzhou:1234567890:bucket/" + self.table_bucket_name + "\"]}]}"

        # Put table bucket policy
        result = self.tables_client.put_table_bucket_policy(
            oss_tables.models.PutTableBucketPolicyRequest(
                table_bucket_arn=self.table_bucket_arn,
                resource_policy=policy_document,
            )
        )

        self.assertEqual(200, result.status_code)

        # Get table bucket policy
        result = self.tables_client.get_table_bucket_policy(
            oss_tables.models.GetTableBucketPolicyRequest(
                table_bucket_arn=self.table_bucket_arn,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.resource_policy)

        # Delete table bucket policy
        result = self.tables_client.delete_table_bucket_policy(
            oss_tables.models.DeleteTableBucketPolicyRequest(
                table_bucket_arn=self.table_bucket_arn,
            )
        )

        self.assertEqual(204, result.status_code)

    def test_table_bucket_maintenance_configuration(self):
        # Put table bucket maintenance configuration
        result = self.tables_client.put_table_bucket_maintenance_configuration(
            oss_tables.models.PutTableBucketMaintenanceConfigurationRequest(
                table_bucket_arn=self.table_bucket_arn,
                type='icebergUnreferencedFileRemoval',
                value={
                    'status': 'enabled',
                    'settings': {
                        'icebergUnreferencedFileRemoval': {
                            'unreferencedDays': 7,
                            'nonCurrentDays': 30
                        }
                    }
                }
            )
        )

        self.assertEqual(204, result.status_code)

        # Get table bucket maintenance configuration
        result = self.tables_client.get_table_bucket_maintenance_configuration(
            oss_tables.models.GetTableBucketMaintenanceConfigurationRequest(
                table_bucket_arn=self.table_bucket_arn,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.configuration)

