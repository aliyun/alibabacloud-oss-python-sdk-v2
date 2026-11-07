# pylint: skip-file
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables
from . import TestIntegrationTables, ACCESS_ID, ACCESS_KEY, REGION, TABLES_ENDPOINT


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

    def test_create_table_schema_v2(self):
        namespace_name = "test_schema_v2_" + str(hash(self.table_bucket_arn))[-8:]
        result = self.tables_client.create_namespace(oss_tables.models.CreateNamespaceRequest(
            table_bucket_arn=self.table_bucket_arn, namespace=[namespace_name],
        ))
        self.assertEqual(200, result.status_code)
        self.addCleanup(self.tables_client.delete_namespace, oss_tables.models.DeleteNamespaceRequest(
            table_bucket_arn=self.table_bucket_arn, namespace=namespace_name,
        ))

        schema_v2 = {
            "type": "struct", "schema-id": 0, "identifier-field-ids": [10],
            "fields": [
                {"id": 10, "name": "order_id", "type": "long", "required": True, "doc": "订单号"},
                {
                    "id": 20, "name": "customer", "required": False,
                    "type": {"type": "struct", "fields": [
                        {"id": 21, "name": "name", "type": "string", "required": False},
                        {"id": 22, "name": "level", "type": "int", "required": False},
                    ]},
                },
                {
                    "id": 30, "name": "tags", "required": False,
                    "type": {"type": "list", "element-id": 31, "element": "string", "element-required": False},
                },
                {
                    "id": 40, "name": "attributes", "required": False,
                    "type": {"type": "map", "key-id": 41, "key": "string",
                             "value-id": 42, "value": "string", "value-required": False},
                },
            ],
        }
        nested_schema_v2 = {
            "type": "struct",
            "fields": [
                {"id": 10, "name": "order_id", "type": "long", "required": True},
                {
                    "id": 20, "name": "items",
                    "type": {
                        "type": "list", "element-id": 21, "element-required": False,
                        "element": {"type": "struct", "fields": [
                            {"id": 22, "name": "product", "type": "string"},
                            {
                                "id": 23, "name": "attributes",
                                "type": {
                                    "type": "map", "key-id": 24, "key": "string",
                                    "value-id": 25, "value-required": False,
                                    "value": {"type": "list", "element-id": 26,
                                              "element": "string", "element-required": False},
                                },
                            },
                        ]},
                    },
                },
            ],
        }
        for name, metadata in (
            ("orders_nested", oss_tables.models.TableMetadata(iceberg=oss_tables.models.IcebergMetadata(
                schema_v2=schema_v2, properties={"format-version": "2"}))),
            ("orders_nested_dict", {"iceberg": {
                "schemaV2": nested_schema_v2, "properties": {"format-version": "2"},
            }}),
        ):
            with self.subTest(name=name):
                result = self.tables_client.create_table(oss_tables.models.CreateTableRequest(
                    table_bucket_arn=self.table_bucket_arn, namespace=namespace_name,
                    name=name, format="ICEBERG", metadata=metadata,
                ))
                self.addCleanup(self.tables_client.delete_table, oss_tables.models.DeleteTableRequest(
                    table_bucket_arn=self.table_bucket_arn, namespace=namespace_name, name=name,
                ))
                self.assertEqual(200, result.status_code)
                self.assertTrue(result.table_arn)
                self.assertTrue(result.version_token)

                get_result = self.tables_client.get_table(oss_tables.models.GetTableRequest(
                    table_bucket_arn=self.table_bucket_arn, namespace=namespace_name, name=name,
                ))
                self.assertEqual(200, get_result.status_code)
                self.assertEqual(name, get_result.name)
                self.assertEqual("ICEBERG", get_result.format)
                self.assertEqual(result.table_arn, get_result.table_arn)
                self.assertTrue(get_result.metadata_location)

                get_by_arn = self.tables_client.get_table(oss_tables.models.GetTableRequest(table_arn=result.table_arn))
                self.assertEqual(200, get_by_arn.status_code)
                self.assertEqual(name, get_by_arn.name)
                self.assertEqual("ICEBERG", get_by_arn.format)

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

        cfg = oss.config.load_default()
        cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
        cfg.region = REGION
        if TABLES_ENDPOINT:
            cfg.endpoint = TABLES_ENDPOINT
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
