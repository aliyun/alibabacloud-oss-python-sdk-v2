# -*- coding: utf-8 -*-
"""Unit tests for tables table_config_basic models."""

import unittest
from alibabacloud_oss_v2.tables.models.table_config_basic import (
    GetTableEncryptionRequest,
    GetTableEncryptionResult,
    GetTableMaintenanceConfigurationRequest,
    GetTableMaintenanceConfigurationResult,
    PutTableMaintenanceConfigurationRequest,
    PutTableMaintenanceConfigurationResult,
    GetTableMaintenanceJobStatusRequest,
    GetTableMaintenanceJobStatusResult,
    GetTableMetadataLocationRequest,
    GetTableMetadataLocationResult,
    UpdateTableMetadataLocationRequest,
    UpdateTableMetadataLocationResult,
    DeleteTablePolicyRequest,
    DeleteTablePolicyResult,
    GetTablePolicyRequest,
    GetTablePolicyResult,
    PutTablePolicyRequest,
    PutTablePolicyResult,
)
from alibabacloud_oss_v2.tables.models.common import EncryptionConfiguration


class TestGetTableEncryptionRequest(unittest.TestCase):
    """Test cases for GetTableEncryptionRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTableEncryptionRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = GetTableEncryptionRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            namespace="test_namespace",
            table="test_table"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "test_table")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", GetTableEncryptionRequest._attribute_map)
        self.assertIn("namespace", GetTableEncryptionRequest._attribute_map)
        self.assertIn("table", GetTableEncryptionRequest._attribute_map)
        self.assertEqual(GetTableEncryptionRequest._attribute_map["table_bucket_arn"]["position"], "header")
        self.assertEqual(GetTableEncryptionRequest._attribute_map["namespace"]["position"], "path")
        self.assertEqual(GetTableEncryptionRequest._attribute_map["table"]["position"], "path")


class TestGetTableEncryptionResult(unittest.TestCase):
    """Test cases for GetTableEncryptionResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTableEncryptionResult()
        self.assertIsNone(result.encryption_configuration)

    def test_init_with_encryption_configuration(self):
        """Test initialization with encryption configuration."""
        encryption_config = EncryptionConfiguration(
            sse_algorithm="AES256",
            kms_key_arn="arn:acs:kms:cn-hangzhou:123456789012:key/12345678-1234-1234-1234-123456789012"
        )
        result = GetTableEncryptionResult(encryption_configuration=encryption_config)
        self.assertIsNotNone(result.encryption_configuration)
        self.assertEqual(result.encryption_configuration.sse_algorithm, "AES256")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("encryption_configuration", GetTableEncryptionResult._attribute_map)
        self.assertEqual(GetTableEncryptionResult._attribute_map["encryption_configuration"]["rename"], "encryptionConfiguration")


class TestGetTableMaintenanceConfigurationRequest(unittest.TestCase):
    """Test cases for GetTableMaintenanceConfigurationRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTableMaintenanceConfigurationRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = GetTableMaintenanceConfigurationRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            namespace="test_namespace",
            table="test_table"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "test_table")


class TestGetTableMaintenanceConfigurationResult(unittest.TestCase):
    """Test cases for GetTableMaintenanceConfigurationResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTableMaintenanceConfigurationResult()
        self.assertIsNone(result.table_arn)
        self.assertIsNone(result.maintenance_configuration)

    def test_init_with_table_arn(self):
        """Test initialization with table_arn."""
        result = GetTableMaintenanceConfigurationResult(
            table_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id"
        )
        self.assertEqual(result.table_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id")
        self.assertIsNone(result.maintenance_configuration)

    def test_init_with_maintenance_configuration(self):
        """Test initialization with maintenance configuration."""
        config = {
            "compaction": {"enabled": True},
            "snapshotManagement": {"minSnapshotsToKeep": 10}
        }
        result = GetTableMaintenanceConfigurationResult(
            table_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id",
            maintenance_configuration=config
        )
        self.assertEqual(result.maintenance_configuration, config)
        self.assertEqual(result.maintenance_configuration["compaction"]["enabled"], True)

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_arn", GetTableMaintenanceConfigurationResult._attribute_map)
        self.assertIn("maintenance_configuration", GetTableMaintenanceConfigurationResult._attribute_map)
        self.assertEqual(GetTableMaintenanceConfigurationResult._attribute_map["table_arn"]["rename"], "tableARN")


class TestPutTableMaintenanceConfigurationRequest(unittest.TestCase):
    """Test cases for PutTableMaintenanceConfigurationRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = PutTableMaintenanceConfigurationRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)
        self.assertIsNone(request.maintenance_configuration)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        config = {"compaction": {"enabled": True}}
        request = PutTableMaintenanceConfigurationRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            namespace="test_namespace",
            table="test_table",
            maintenance_configuration=config
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "test_table")
        self.assertEqual(request.maintenance_configuration, config)


class TestPutTableMaintenanceConfigurationResult(unittest.TestCase):
    """Test cases for PutTableMaintenanceConfigurationResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = PutTableMaintenanceConfigurationResult()


class TestGetTableMaintenanceJobStatusRequest(unittest.TestCase):
    """Test cases for GetTableMaintenanceJobStatusRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTableMaintenanceJobStatusRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = GetTableMaintenanceJobStatusRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            namespace="test_namespace",
            table="test_table"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "test_table")


class TestGetTableMaintenanceJobStatusResult(unittest.TestCase):
    """Test cases for GetTableMaintenanceJobStatusResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTableMaintenanceJobStatusResult()
        self.assertIsNone(result.table_arn)
        self.assertIsNone(result.status)

    def test_init_with_table_arn(self):
        """Test initialization with table_arn."""
        result = GetTableMaintenanceJobStatusResult(
            table_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id"
        )
        self.assertEqual(result.table_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id")
        self.assertIsNone(result.status)

    def test_init_with_status(self):
        """Test initialization with status dict."""
        status = {
            "compaction": {
                "status": "RUNNING",
                "lastRunTimestamp": "2024-01-01T00:00:00Z",
                "failureMessage": None
            },
            "snapshotManagement": {
                "status": "COMPLETED",
                "lastRunTimestamp": "2024-01-01T00:00:00Z"
            }
        }
        result = GetTableMaintenanceJobStatusResult(
            table_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket/table/table_id",
            status=status
        )
        self.assertEqual(result.status, status)
        self.assertEqual(result.status["compaction"]["status"], "RUNNING")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_arn", GetTableMaintenanceJobStatusResult._attribute_map)
        self.assertIn("status", GetTableMaintenanceJobStatusResult._attribute_map)
        self.assertEqual(GetTableMaintenanceJobStatusResult._attribute_map["table_arn"]["rename"], "tableARN")
        self.assertEqual(GetTableMaintenanceJobStatusResult._attribute_map["status"]["rename"], "status")


class TestGetTableMetadataLocationRequest(unittest.TestCase):
    """Test cases for GetTableMetadataLocationRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTableMetadataLocationRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = GetTableMetadataLocationRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            namespace="test_namespace",
            table="test_table"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "test_table")


class TestGetTableMetadataLocationResult(unittest.TestCase):
    """Test cases for GetTableMetadataLocationResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTableMetadataLocationResult()
        self.assertIsNone(result.metadata_location)

    def test_init_with_metadata_location(self):
        """Test initialization with metadata_location."""
        result = GetTableMetadataLocationResult(
            metadata_location="oss://data-bucket/metadata/00000-xxx.metadata.json"
        )
        self.assertEqual(result.metadata_location, "oss://data-bucket/metadata/00000-xxx.metadata.json")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("metadata_location", GetTableMetadataLocationResult._attribute_map)
        self.assertEqual(GetTableMetadataLocationResult._attribute_map["metadata_location"]["rename"], "metadataLocation")


class TestUpdateTableMetadataLocationRequest(unittest.TestCase):
    """Test cases for UpdateTableMetadataLocationRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = UpdateTableMetadataLocationRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)
        self.assertIsNone(request.metadata_location)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = UpdateTableMetadataLocationRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            namespace="test_namespace",
            table="test_table",
            metadata_location="oss://data-bucket/metadata/new-location.metadata.json"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "test_table")
        self.assertEqual(request.metadata_location, "oss://data-bucket/metadata/new-location.metadata.json")


class TestUpdateTableMetadataLocationResult(unittest.TestCase):
    """Test cases for UpdateTableMetadataLocationResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = UpdateTableMetadataLocationResult()


class TestDeleteTablePolicyRequest(unittest.TestCase):
    """Test cases for DeleteTablePolicyRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = DeleteTablePolicyRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = DeleteTablePolicyRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            namespace="test_namespace",
            table="test_table"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "test_table")


class TestDeleteTablePolicyResult(unittest.TestCase):
    """Test cases for DeleteTablePolicyResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = DeleteTablePolicyResult()


class TestGetTablePolicyRequest(unittest.TestCase):
    """Test cases for GetTablePolicyRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTablePolicyRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = GetTablePolicyRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            namespace="test_namespace",
            table="test_table"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "test_table")


class TestGetTablePolicyResult(unittest.TestCase):
    """Test cases for GetTablePolicyResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTablePolicyResult()
        self.assertIsNone(result.policy)

    def test_init_with_policy(self):
        """Test initialization with policy."""
        policy = {
            "Version": "1",
            "Statement": [{
                "Effect": "Allow",
                "Action": "oss:*",
                "Resource": "arn:acs:oss:*:*:*"
            }]
        }
        result = GetTablePolicyResult(policy=policy)
        self.assertEqual(result.policy, policy)
        self.assertEqual(result.policy["Version"], "1")


class TestPutTablePolicyRequest(unittest.TestCase):
    """Test cases for PutTablePolicyRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = PutTablePolicyRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)
        self.assertIsNone(request.table)
        self.assertIsNone(request.policy)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        policy = {"Version": "1", "Statement": []}
        request = PutTablePolicyRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            namespace="test_namespace",
            table="test_table",
            policy=policy
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.namespace, "test_namespace")
        self.assertEqual(request.table, "test_table")
        self.assertEqual(request.policy, policy)


class TestPutTablePolicyResult(unittest.TestCase):
    """Test cases for PutTablePolicyResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = PutTablePolicyResult()


if __name__ == '__main__':
    unittest.main()
