# pylint: skip-file
import os
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables
from . import TestIntegrationTables


class TestTableBasic(TestIntegrationTables):

    def test_create_table(self):
        table_name = "test_table_" + str(hash(self.table_bucket_arn))[-8:]
        namespace_name = "test_ns_" + str(hash(self.table_bucket_arn))[-8:]

        # Create namespace first
        self.tables_client.create_namespace(
            oss_tables.models.CreateNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=[namespace_name],
            )
        )

        # Create table
        result = self.tables_client.create_table(
            oss_tables.models.CreateTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                format='ICEBERG',
            )
        )

        table_arn = result.table_arn

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.table_arn)
        self.assertIn("acs:", result.table_arn)
        self.assertIsNotNone(result.version_token)

        # Get table
        result = self.tables_client.get_table(
            oss_tables.models.GetTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertEqual(table_name, result.name)
        self.assertEqual('ICEBERG', result.format)

        # Get table by tableArn
        result = self.tables_client.get_table(
            oss_tables.models.GetTableRequest(
                table_arn=table_arn,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertEqual(table_name, result.name)
        self.assertEqual('ICEBERG', result.format)

        # List tables
        result = self.tables_client.list_tables(
            oss_tables.models.ListTablesRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

        self.assertEqual(200, result.status_code)


        # Delete table
        result = self.tables_client.delete_table(
            oss_tables.models.DeleteTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(204, result.status_code)

        # Delete namespace
        self.tables_client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

    def test_rename_table(self):
        table_name = "test_table_" + str(hash(self.table_bucket_arn))[-8:]
        new_table_name = "renamed_table_" + str(hash(self.table_bucket_arn))[-8:]
        namespace_name = "test_ns_" + str(hash(self.table_bucket_arn))[-8:]

        # Create namespace first
        self.tables_client.create_namespace(
            oss_tables.models.CreateNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=[namespace_name],
            )
        )

        # Create table
        result = self.tables_client.create_table(
            oss_tables.models.CreateTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                format='ICEBERG',
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.table_arn)

        # Rename table
        rename_result = self.tables_client.rename_table(
            oss_tables.models.RenameTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                new_name=new_table_name,
            )
        )

        self.assertEqual(204, rename_result.status_code)

        # Verify the table has been renamed by attempting to get it with the new name
        get_result = self.tables_client.get_table(
            oss_tables.models.GetTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=new_table_name,
            )
        )

        self.assertEqual(200, get_result.status_code)
        self.assertEqual(new_table_name, get_result.name)

        # Clean up - delete renamed table
        delete_result = self.tables_client.delete_table(
            oss_tables.models.DeleteTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=new_table_name,
            )
        )

        self.assertEqual(204, delete_result.status_code)

        # Delete namespace
        self.tables_client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

    def test_create_table_use_path_style(self):
        table_name = "test_table_" + str(hash(self.table_bucket_arn))[-8:]
        namespace_name = "test_ns_" + str(hash(self.table_bucket_arn))[-8:]

        ak = os.getenv("OSS_TEST_ACCESS_KEY_ID")
        sk = os.getenv("OSS_TEST_ACCESS_KEY_SECRET")
        region = os.getenv("OSS_TEST_REGION", "cn-hangzhou")
        endpoint = os.getenv("OSS_TEST_TABLES_ENDPOINT")


        cfg = oss.config.load_default()
        cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ak, sk)
        cfg.region = region
        cfg.endpoint = endpoint
        cfg.use_path_style = True
        tables_client = oss_tables.Client(cfg)

        # Create namespace first
        tables_client.create_namespace(
            oss_tables.models.CreateNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=[namespace_name],
            )
        )

        # Create table
        result = tables_client.create_table(
            oss_tables.models.CreateTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                format='ICEBERG',
            )
        )

        table_arn = result.table_arn

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.table_arn)
        self.assertIn("acs:", result.table_arn)
        self.assertIsNotNone(result.version_token)

        # Get table
        result = tables_client.get_table(
            oss_tables.models.GetTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertEqual(table_name, result.name)
        self.assertEqual('ICEBERG', result.format)

        # Get table by tableArn
        result = tables_client.get_table(
            oss_tables.models.GetTableRequest(
                table_arn=table_arn,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertEqual(table_name, result.name)
        self.assertEqual('ICEBERG', result.format)

        # List tables
        result = tables_client.list_tables(
            oss_tables.models.ListTablesRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

        self.assertEqual(200, result.status_code)


        # Delete table
        result = tables_client.delete_table(
            oss_tables.models.DeleteTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(204, result.status_code)

        # Delete namespace
        tables_client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )
