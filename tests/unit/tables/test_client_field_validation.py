# -*- coding: utf-8 -*-
"""Client-level field validation tests for Tables API."""

import unittest
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables
from alibabacloud_oss_v2 import credentials


def new_test_tables_client():
    """Create a test tables client with anonymous credentials."""
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
    cfg.region = 'cn-hangzhou'
    return oss_tables.Client(cfg)


class TestClientFieldValidation(unittest.TestCase):
    """Field validation tests for Tables API operations."""

    # ==================== Table Bucket API ====================

    def test_create_table_bucket_field_validation(self):
        """Test CreateTableBucket field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # CreateTableBucket has no required fields (name is optional)
        # Test with invalid bucket name in ARN format
        try:
            client.create_table_bucket(
                oss_tables.models.CreateTableBucketRequest(
                    name="valid-bucket"
                )
            )
        except Exception as e:
            # Should fail due to network/auth, but not validation
            self.assertNotIn("Malformed ARN", str(e))

    def test_get_table_bucket_field_validation(self):
        """Test GetTableBucket field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_table_bucket(
                oss_tables.models.GetTableBucketRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_table_bucket(
                oss_tables.models.GetTableBucketRequest(
                    table_bucket_arn="bucket-name"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_table_bucket(
                oss_tables.models.GetTableBucketRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_delete_table_bucket_field_validation(self):
        """Test DeleteTableBucket field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.delete_table_bucket(
                oss_tables.models.DeleteTableBucketRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.delete_table_bucket(
                oss_tables.models.DeleteTableBucketRequest(
                    table_bucket_arn="bucket-name"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.delete_table_bucket(
                oss_tables.models.DeleteTableBucketRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_list_table_buckets_field_validation(self):
        """Test ListTableBuckets field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # ListTableBuckets has no required fields
        # Just verify it doesn't crash on empty request
        try:
            client.list_table_buckets(
                oss_tables.models.ListTableBucketsRequest()
            )
        except Exception as e:
            # Should fail due to network/auth, but not validation
            self.assertNotIn("missing required field", str(e))

    # ==================== Namespace API ====================

    def test_create_namespace_field_validation(self):
        """Test CreateNamespace field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.create_namespace(
                oss_tables.models.CreateNamespaceRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN - must provide required fields first
        try:
            client.create_namespace(
                oss_tables.models.CreateNamespaceRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.create_namespace(
                oss_tables.models.CreateNamespaceRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-ns?1234",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_get_namespace_field_validation(self):
        """Test GetNamespace field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_namespace(
                oss_tables.models.GetNamespaceRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Namespace
        try:
            client.get_namespace(
                oss_tables.models.GetNamespaceRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_namespace(
                oss_tables.models.GetNamespaceRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_namespace(
                oss_tables.models.GetNamespaceRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-ns?1234",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_delete_namespace_field_validation(self):
        """Test DeleteNamespace field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.delete_namespace(
                oss_tables.models.DeleteNamespaceRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Namespace
        try:
            client.delete_namespace(
                oss_tables.models.DeleteNamespaceRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.delete_namespace(
                oss_tables.models.DeleteNamespaceRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.delete_namespace(
                oss_tables.models.DeleteNamespaceRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-ns?1234",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_list_namespaces_field_validation(self):
        """Test ListNamespaces field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.list_namespaces(
                oss_tables.models.ListNamespacesRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.list_namespaces(
                oss_tables.models.ListNamespacesRequest(
                    table_bucket_arn="bucket-name"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.list_namespaces(
                oss_tables.models.ListNamespacesRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-ns?1234"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    # ==================== Table API ====================

    def test_create_table_field_validation(self):
        """Test CreateTable field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.create_table(
                oss_tables.models.CreateTableRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN - must provide required fields first
        try:
            client.create_table(
                oss_tables.models.CreateTableRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table",
                    format="iceberg"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.create_table(
                oss_tables.models.CreateTableRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table",
                    format="iceberg"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_get_table_field_validation(self):
        """Test GetTable field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # GetTable can use either table_bucket_arn+namespace+name OR table_arn
        # Test with invalid table_arn
        try:
            client.get_table(
                oss_tables.models.GetTableRequest(
                    table_arn="invalid-arn"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Test with table_arn containing invalid bucket name
        try:
            client.get_table(
                oss_tables.models.GetTableRequest(
                    table_arn="acs:osstables:cn-beijing:123456:bucket/invalid?bucket/table/test"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

        # Test without any required field - Python SDK validates table_bucket_arn first
        try:
            client.get_table(
                oss_tables.models.GetTableRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

    def test_delete_table_field_validation(self):
        """Test DeleteTable field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.delete_table(
                oss_tables.models.DeleteTableRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Namespace
        try:
            client.delete_table(
                oss_tables.models.DeleteTableRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Name
        try:
            client.delete_table(
                oss_tables.models.DeleteTableRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.delete_table(
                oss_tables.models.DeleteTableRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.delete_table(
                oss_tables.models.DeleteTableRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_list_tables_field_validation(self):
        """Test ListTables field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.list_tables(
                oss_tables.models.ListTablesRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Namespace
        try:
            client.list_tables(
                oss_tables.models.ListTablesRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.list_tables(
                oss_tables.models.ListTablesRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.list_tables(
                oss_tables.models.ListTablesRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-ns?1234",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_rename_table_field_validation(self):
        """Test RenameTable field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.rename_table(
                oss_tables.models.RenameTableRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Namespace
        try:
            client.rename_table(
                oss_tables.models.RenameTableRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.rename_table(
                oss_tables.models.RenameTableRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN - must provide all required fields first
        try:
            client.rename_table(
                oss_tables.models.RenameTableRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table",
                    new_name="new-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.rename_table(
                oss_tables.models.RenameTableRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table",
                    new_name="new-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    # ==================== Table Bucket Config API ====================

    def test_put_table_bucket_encryption_field_validation(self):
        """Test PutTableBucketEncryption field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.put_table_bucket_encryption(
                oss_tables.models.PutTableBucketEncryptionRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.put_table_bucket_encryption(
                oss_tables.models.PutTableBucketEncryptionRequest(
                    table_bucket_arn="bucket-name"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.put_table_bucket_encryption(
                oss_tables.models.PutTableBucketEncryptionRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_get_table_bucket_encryption_field_validation(self):
        """Test GetTableBucketEncryption field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_table_bucket_encryption(
                oss_tables.models.GetTableBucketEncryptionRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_table_bucket_encryption(
                oss_tables.models.GetTableBucketEncryptionRequest(
                    table_bucket_arn="bucket-name"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_table_bucket_encryption(
                oss_tables.models.GetTableBucketEncryptionRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_delete_table_bucket_encryption_field_validation(self):
        """Test DeleteTableBucketEncryption field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.delete_table_bucket_encryption(
                oss_tables.models.DeleteTableBucketEncryptionRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.delete_table_bucket_encryption(
                oss_tables.models.DeleteTableBucketEncryptionRequest(
                    table_bucket_arn="bucket-name"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.delete_table_bucket_encryption(
                oss_tables.models.DeleteTableBucketEncryptionRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_put_table_bucket_policy_field_validation(self):
        """Test PutTableBucketPolicy field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.put_table_bucket_policy(
                oss_tables.models.PutTableBucketPolicyRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.put_table_bucket_policy(
                oss_tables.models.PutTableBucketPolicyRequest(
                    table_bucket_arn="bucket-name",
                    resource_policy='{"Version":"1"}'
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.put_table_bucket_policy(
                oss_tables.models.PutTableBucketPolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    resource_policy='{"Version":"1"}'
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_get_table_bucket_policy_field_validation(self):
        """Test GetTableBucketPolicy field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_table_bucket_policy(
                oss_tables.models.GetTableBucketPolicyRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_table_bucket_policy(
                oss_tables.models.GetTableBucketPolicyRequest(
                    table_bucket_arn="bucket-name"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_table_bucket_policy(
                oss_tables.models.GetTableBucketPolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_delete_table_bucket_policy_field_validation(self):
        """Test DeleteTableBucketPolicy field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.delete_table_bucket_policy(
                oss_tables.models.DeleteTableBucketPolicyRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.delete_table_bucket_policy(
                oss_tables.models.DeleteTableBucketPolicyRequest(
                    table_bucket_arn="bucket-name"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.delete_table_bucket_policy(
                oss_tables.models.DeleteTableBucketPolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_put_table_bucket_maintenance_configuration_field_validation(self):
        """Test PutTableBucketMaintenanceConfiguration field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.put_table_bucket_maintenance_configuration(
                oss_tables.models.PutTableBucketMaintenanceConfigurationRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.put_table_bucket_maintenance_configuration(
                oss_tables.models.PutTableBucketMaintenanceConfigurationRequest(
                    table_bucket_arn="bucket-name",
                    type="icebergCompaction"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.put_table_bucket_maintenance_configuration(
                oss_tables.models.PutTableBucketMaintenanceConfigurationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    type="icebergCompaction"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_get_table_bucket_maintenance_configuration_field_validation(self):
        """Test GetTableBucketMaintenanceConfiguration field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_table_bucket_maintenance_configuration(
                oss_tables.models.GetTableBucketMaintenanceConfigurationRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_table_bucket_maintenance_configuration(
                oss_tables.models.GetTableBucketMaintenanceConfigurationRequest(
                    table_bucket_arn="bucket-name"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_table_bucket_maintenance_configuration(
                oss_tables.models.GetTableBucketMaintenanceConfigurationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    # ==================== Table Config API ====================

    def test_get_table_encryption_field_validation(self):
        """Test GetTableEncryption field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_table_encryption(
                oss_tables.models.GetTableEncryptionRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Tablespace
        try:
            client.get_table_encryption(
                oss_tables.models.GetTableEncryptionRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.get_table_encryption(
                oss_tables.models.GetTableEncryptionRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_table_encryption(
                oss_tables.models.GetTableEncryptionRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_table_encryption(
                oss_tables.models.GetTableEncryptionRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_put_table_policy_field_validation(self):
        """Test PutTablePolicy field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.put_table_policy(
                oss_tables.models.PutTablePolicyRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Tablespace
        try:
            client.put_table_policy(
                oss_tables.models.PutTablePolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.put_table_policy(
                oss_tables.models.PutTablePolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.put_table_policy(
                oss_tables.models.PutTablePolicyRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table",
                    resource_policy='{"Version":"1"}'
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.put_table_policy(
                oss_tables.models.PutTablePolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table",
                    resource_policy='{"Version":"1"}'
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_get_table_policy_field_validation(self):
        """Test GetTablePolicy field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_table_policy(
                oss_tables.models.GetTablePolicyRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Tablespace
        try:
            client.get_table_policy(
                oss_tables.models.GetTablePolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.get_table_policy(
                oss_tables.models.GetTablePolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_table_policy(
                oss_tables.models.GetTablePolicyRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_table_policy(
                oss_tables.models.GetTablePolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_delete_table_policy_field_validation(self):
        """Test DeleteTablePolicy field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.delete_table_policy(
                oss_tables.models.DeleteTablePolicyRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Tablespace
        try:
            client.delete_table_policy(
                oss_tables.models.DeleteTablePolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.delete_table_policy(
                oss_tables.models.DeleteTablePolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.delete_table_policy(
                oss_tables.models.DeleteTablePolicyRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.delete_table_policy(
                oss_tables.models.DeleteTablePolicyRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_put_table_maintenance_configuration_field_validation(self):
        """Test PutTableMaintenanceConfiguration field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.put_table_maintenance_configuration(
                oss_tables.models.PutTableMaintenanceConfigurationRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Tablespace
        try:
            client.put_table_maintenance_configuration(
                oss_tables.models.PutTableMaintenanceConfigurationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.put_table_maintenance_configuration(
                oss_tables.models.PutTableMaintenanceConfigurationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.put_table_maintenance_configuration(
                oss_tables.models.PutTableMaintenanceConfigurationRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table",
                    type="icebergCompaction"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.put_table_maintenance_configuration(
                oss_tables.models.PutTableMaintenanceConfigurationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table",
                    type="icebergCompaction"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_get_table_maintenance_configuration_field_validation(self):
        """Test GetTableMaintenanceConfiguration field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_table_maintenance_configuration(
                oss_tables.models.GetTableMaintenanceConfigurationRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Tablespace
        try:
            client.get_table_maintenance_configuration(
                oss_tables.models.GetTableMaintenanceConfigurationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.get_table_maintenance_configuration(
                oss_tables.models.GetTableMaintenanceConfigurationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_table_maintenance_configuration(
                oss_tables.models.GetTableMaintenanceConfigurationRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_table_maintenance_configuration(
                oss_tables.models.GetTableMaintenanceConfigurationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_get_table_maintenance_job_status_field_validation(self):
        """Test GetTableMaintenanceJobStatus field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_table_maintenance_job_status(
                oss_tables.models.GetTableMaintenanceJobStatusRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Tablespace
        try:
            client.get_table_maintenance_job_status(
                oss_tables.models.GetTableMaintenanceJobStatusRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.get_table_maintenance_job_status(
                oss_tables.models.GetTableMaintenanceJobStatusRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_table_maintenance_job_status(
                oss_tables.models.GetTableMaintenanceJobStatusRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_table_maintenance_job_status(
                oss_tables.models.GetTableMaintenanceJobStatusRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_get_table_metadata_location_field_validation(self):
        """Test GetTableMetadataLocation field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.get_table_metadata_location(
                oss_tables.models.GetTableMetadataLocationRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Tablespace
        try:
            client.get_table_metadata_location(
                oss_tables.models.GetTableMetadataLocationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.get_table_metadata_location(
                oss_tables.models.GetTableMetadataLocationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.get_table_metadata_location(
                oss_tables.models.GetTableMetadataLocationRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.get_table_metadata_location(
                oss_tables.models.GetTableMetadataLocationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))

    def test_update_table_metadata_location_field_validation(self):
        """Test UpdateTableMetadataLocation field validation."""
        client = new_test_tables_client()
        self.assertIsNotNone(client)

        # Required field - TableBucketARN
        try:
            client.update_table_metadata_location(
                oss_tables.models.UpdateTableMetadataLocationRequest()
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Tablespace
        try:
            client.update_table_metadata_location(
                oss_tables.models.UpdateTableMetadataLocationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Required field - Table
        try:
            client.update_table_metadata_location(
                oss_tables.models.UpdateTableMetadataLocationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/valid-bucket",
                    namespace="test-ns"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("missing required field", str(e))

        # Malformed ARN
        try:
            client.update_table_metadata_location(
                oss_tables.models.UpdateTableMetadataLocationRequest(
                    table_bucket_arn="bucket-name",
                    namespace="test-ns",
                    name="test-table"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("Malformed ARN", str(e))

        # Invalid bucket name in ARN
        try:
            client.update_table_metadata_location(
                oss_tables.models.UpdateTableMetadataLocationRequest(
                    table_bucket_arn="acs:osstables:cn-beijing:123456:bucket/test-table?1234",
                    namespace="test-ns",
                    name="test-table",
                    metadata_location="oss://bucket/path",
                    version_token="v1"
                )
            )
            self.fail("should raise exception")
        except Exception as e:
            self.assertIn("bucket resource is invalid", str(e))


if __name__ == '__main__':
    unittest.main()
