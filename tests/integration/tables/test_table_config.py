# pylint: skip-file

import alibabacloud_oss_v2.tables as oss_tables
from . import TestIntegrationTables


class TestTableConfig(TestIntegrationTables):

    def test_table_encryption(self):
        table_name = "test_table_enc_" + str(hash(self.table_bucket_arn))[-8:]
        namespace_name = "test_ns_enc_" + str(hash(self.table_bucket_arn))[-8:]

        # Create namespace first
        self.tables_client.create_namespace(
            oss_tables.models.CreateNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=[namespace_name],
            )
        )

        # Create table
        self.tables_client.create_table(
            oss_tables.models.CreateTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                format='ICEBERG',
            )
        )

        # Get table encryption
        result = self.tables_client.get_table_encryption(
            oss_tables.models.GetTableEncryptionRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(200, result.status_code)

        # Clean up
        self.tables_client.delete_table(
            oss_tables.models.DeleteTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )
        self.tables_client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

    def test_table_maintenance_configuration(self):
        table_name = "test_table_maint_" + str(hash(self.table_bucket_arn))[-8:]
        namespace_name = "test_ns_maint_" + str(hash(self.table_bucket_arn))[-8:]

        # Create namespace first
        self.tables_client.create_namespace(
            oss_tables.models.CreateNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=[namespace_name],
            )
        )

        # Create table
        self.tables_client.create_table(
            oss_tables.models.CreateTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                format='ICEBERG',
            )
        )

        # Put table maintenance configuration
        result = self.tables_client.put_table_maintenance_configuration(
            oss_tables.models.PutTableMaintenanceConfigurationRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                type='icebergCompaction',
                value={
                    'status': 'enabled',
                    'settings': {
                        'icebergCompaction': {
                            'targetFileSizeMB': 100,
                            'strategy': 'auto'
                        }
                    }
                }
            )
        )

        # Check if the status code is either 200 or 204 (both indicate success)
        self.assertIn(result.status_code, [200, 204])

        # Get table maintenance configuration
        result = self.tables_client.get_table_maintenance_configuration(
            oss_tables.models.GetTableMaintenanceConfigurationRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.configuration)

        # Clean up
        self.tables_client.delete_table(
            oss_tables.models.DeleteTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )
        self.tables_client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

    def test_table_policy(self):
        table_name = "test_table_pol_" + str(hash(self.table_bucket_arn))[-8:]
        namespace_name = "test_ns_pol_" + str(hash(self.table_bucket_arn))[-8:]

        # Create namespace first
        self.tables_client.create_namespace(
            oss_tables.models.CreateNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=[namespace_name],
            )
        )

        # Create table
        self.tables_client.create_table(
            oss_tables.models.CreateTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                format='ICEBERG',
            )
        )

        # Put table policy
        result = self.tables_client.put_table_policy(
            oss_tables.models.PutTablePolicyRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                resource_policy='{"Version":"1","Statement":[{"Action":["oss:GetTable"],"Effect":"Allow","Principal":["1234567890"],"Resource":["' + self.table_bucket_arn + ':table/' + table_name + '"]}]}',
            )
        )

        # Check if the status code is either 200 or 204 (both indicate success)
        self.assertIn(result.status_code, [200, 204])

        # Get table policy
        result = self.tables_client.get_table_policy(
            oss_tables.models.GetTablePolicyRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.resource_policy)

        # Delete table policy
        result = self.tables_client.delete_table_policy(
            oss_tables.models.DeleteTablePolicyRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(204, result.status_code)

        # Clean up
        self.tables_client.delete_table(
            oss_tables.models.DeleteTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )
        self.tables_client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

    def test_table_maintenance_job_status(self):
        table_name = "test_table_mjs_" + str(hash(self.table_bucket_arn))[-8:]
        namespace_name = "test_ns_mjs_" + str(hash(self.table_bucket_arn))[-8:]

        # Create namespace first
        self.tables_client.create_namespace(
            oss_tables.models.CreateNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=[namespace_name],
            )
        )

        # Create table
        self.tables_client.create_table(
            oss_tables.models.CreateTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                format='ICEBERG',
            )
        )

        # Get table maintenance job status
        result = self.tables_client.get_table_maintenance_job_status(
            oss_tables.models.GetTableMaintenanceJobStatusRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(200, result.status_code)

        # Clean up
        self.tables_client.delete_table(
            oss_tables.models.DeleteTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )
        self.tables_client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

    def test_table_metadata_location(self):
        table_name = "test_table_md_" + str(hash(self.table_bucket_arn))[-8:]
        namespace_name = "test_ns_md_" + str(hash(self.table_bucket_arn))[-8:]

        # Create namespace first
        self.tables_client.create_namespace(
            oss_tables.models.CreateNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=[namespace_name],
            )
        )

        # Create table
        self.tables_client.create_table(
            oss_tables.models.CreateTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                format='ICEBERG',
                metadata=oss_tables.models.TableMetadata(
                    iceberg=oss_tables.models.IcebergMetadata(
                        schema=oss_tables.models.IcebergSchema(
                            fields=[
                                oss_tables.models.SchemaField(name="id", type="long", required=True),
                                oss_tables.models.SchemaField(name="ts", type="timestamptz", required=True),
                                oss_tables.models.SchemaField(name="region", type="string"),
                                oss_tables.models.SchemaField(name="amount", type="double")
                            ]
                        ),
                        partition_spec=oss_tables.models.IcebergPartitionSpec(
                            spec_id=0,
                            fields=[
                                oss_tables.models.IcebergPartitionField(source_id=2, transform="day", name="ts_day"),
                                oss_tables.models.IcebergPartitionField(source_id=3, transform="identity", name="region")
                            ]
                        ),
                        sort_order=oss_tables.models.IcebergSortOrder(
                            fields=[
                                oss_tables.models.IcebergSortField(source_id=2, transform="identity", direction="desc", null_order="nulls-last"),
                                oss_tables.models.IcebergSortField(source_id=1, transform="identity", direction="asc", null_order="nulls-first")
                            ]
                        ),
                        properties={
                            "format-version": "2",
                            "write.format.default": "parquet"
                        }
                    )
                )
            )
        )

        # Get table metadata location
        result = self.tables_client.get_table_metadata_location(
            oss_tables.models.GetTableMetadataLocationRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.metadata_location)


        # Update table metadata location
        update_result = self.tables_client.update_table_metadata_location(
            oss_tables.models.UpdateTableMetadataLocationRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
                metadata_location=result.metadata_location,
                version_token=result.version_token,
            )
        )

        self.assertEqual(200, update_result.status_code)
        self.assertIsNotNone(update_result.metadata_location)

        # Clean up
        self.tables_client.delete_table(
            oss_tables.models.DeleteTableRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
                name=table_name,
            )
        )
        self.tables_client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )


