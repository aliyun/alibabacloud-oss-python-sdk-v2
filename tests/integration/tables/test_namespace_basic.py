# pylint: skip-file

import alibabacloud_oss_v2.tables as oss_tables
from . import TestIntegrationTables


class TestNamespaceBasic(TestIntegrationTables):

    def test_create_namespace(self):
        namespace_name = "test_namespace_" + str(hash(self.table_bucket_arn))[-8:]

        # Create namespace
        result = self.tables_client.create_namespace(
            oss_tables.models.CreateNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=[namespace_name],
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.table_bucket_arn)
        self.assertIn("acs:", result.table_bucket_arn)
        self.assertIsNotNone(result.namespace)
        self.assertEqual(1, len(result.namespace))
        self.assertEqual(namespace_name, result.namespace[0])

        # Get namespace
        result = self.tables_client.get_namespace(
            oss_tables.models.GetNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.namespace)
        self.assertEqual(1, len(result.namespace))
        self.assertEqual(namespace_name, result.namespace[0])
        self.assertIn("-", result.namespace_id)
        self.assertIn("-", result.table_bucket_id)
        self.assertIsNotNone(result.owner_account_id)
        self.assertIsNotNone(result.created_at)
        self.assertIsNotNone(result.created_by)


        # List namespaces
        result = self.tables_client.list_namespaces(
            oss_tables.models.ListNamespacesRequest(
                table_bucket_arn=self.table_bucket_arn,
                max_namespaces=100,
            )
        )

        self.assertEqual(200, result.status_code)

        self.assertIsNotNone(result.namespaces)
        self.assertEqual(1, len(result.namespaces))
        summary = result.namespaces[0]
        self.assertEqual(1, len(summary.namespace))
        self.assertEqual(namespace_name, summary.namespace[0])
        self.assertIn("-", summary.namespace_id)
        self.assertIsNotNone(summary.owner_account_id)
        self.assertIsNotNone(summary.created_at)
        self.assertIsNotNone(summary.created_by)


        # Delete namespace
        result = self.tables_client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=self.table_bucket_arn,
                namespace=namespace_name,
            )
        )

        self.assertEqual(204, result.status_code)
