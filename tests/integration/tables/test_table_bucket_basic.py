# pylint: skip-file

import alibabacloud_oss_v2.tables as oss_tables
from . import TestIntegrationTables, REGION


class TestTableBucketBasic(TestIntegrationTables):

    def test_list_table_buckets(self):
        # List table buckets
        result = self.tables_client.list_table_buckets(
            oss_tables.models.ListTableBucketsRequest(
                max_buckets=100,  # Increase max_buckets to see more results
            )
        )


        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.table_buckets)
        self.assertGreater(len(result.table_buckets), 0)
        self.assertEqual(self.table_bucket_name, result.table_buckets[0].name)
        self.assertIn("acs:", result.table_buckets[0].arn)
        self.assertIsNotNone(result.table_buckets[0].type)
        self.assertIsNotNone(result.table_buckets[0].owner_account_id)
        self.assertIsNotNone(result.table_buckets[0].table_bucket_id)
        self.assertIsNotNone(result.table_buckets[0].created_at)

        # Get table bucket
        bucket_info = result.table_buckets[0]
        result = self.tables_client.get_table_bucket(
            oss_tables.models.GetTableBucketRequest(
                table_bucket_arn=bucket_info.arn
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertEqual(self.table_bucket_name, result.name)
        self.assertIn("acs:", result.arn)
        self.assertEqual('customer', result.type)
        self.assertIsNotNone(result.owner_account_id)
        self.assertIsNotNone(result.table_bucket_id)
        self.assertIsNotNone(result.created_at)

    def test_create_table_bucket(self):
        bucket_name = self.table_bucket_name + '1'

        result = self.tables_client.create_table_bucket(
            oss_tables.models.CreateTableBucketRequest(
                name=bucket_name,
                encryption_configuration=oss_tables.models.EncryptionConfiguration(
                    sse_algorithm='AES256',
                ),
            )
        )
        self.assertEqual(200, result.status_code)

    def test_delete_table_bucket(self):
        # Create a new table bucket for testing delete
        bucket_name = self.table_bucket_name + '2'
        create_result = self.tables_client.create_table_bucket(
            oss_tables.models.CreateTableBucketRequest(
                name=bucket_name,
                encryption_configuration=oss_tables.models.EncryptionConfiguration(
                    sse_algorithm='AES256',
                ),
            )
        )
        self.assertEqual(200, create_result.status_code)
        temp_bucket_arn = create_result.arn

        # Delete table bucket
        result = self.tables_client.delete_table_bucket(
            oss_tables.models.DeleteTableBucketRequest(
                table_bucket_arn=temp_bucket_arn
            )
        )
        self.assertEqual(204, result.status_code)
