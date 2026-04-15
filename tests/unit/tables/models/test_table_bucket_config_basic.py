# -*- coding: utf-8 -*-
"""Unit tests for tables table_bucket_config_basic models."""

import unittest
from alibabacloud_oss_v2.tables.models.table_bucket_config_basic import (
    DeleteTableBucketEncryptionRequest,
    DeleteTableBucketEncryptionResult,
    GetTableBucketEncryptionRequest,
    GetTableBucketEncryptionResult,
    PutTableBucketEncryptionRequest,
    PutTableBucketEncryptionResult,
    GetTableBucketMaintenanceConfigurationRequest,
    GetTableBucketMaintenanceConfigurationResult,
    PutTableBucketMaintenanceConfigurationRequest,
    PutTableBucketMaintenanceConfigurationResult,
    DeleteTableBucketPolicyRequest,
    DeleteTableBucketPolicyResult,
    GetTableBucketPolicyRequest,
    GetTableBucketPolicyResult,
    PutTableBucketPolicyRequest,
    PutTableBucketPolicyResult,
)
from alibabacloud_oss_v2.tables.models.common import EncryptionConfiguration


class TestDeleteTableBucketEncryptionRequest(unittest.TestCase):
    """Test cases for DeleteTableBucketEncryptionRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = DeleteTableBucketEncryptionRequest()
        self.assertIsNone(request.table_bucket_arn)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = DeleteTableBucketEncryptionRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", DeleteTableBucketEncryptionRequest._attribute_map)
        self.assertEqual(DeleteTableBucketEncryptionRequest._attribute_map["table_bucket_arn"]["position"], "header")
        self.assertEqual(DeleteTableBucketEncryptionRequest._attribute_map["table_bucket_arn"]["rename"], "x-oss-table-bucket-arn")


class TestDeleteTableBucketEncryptionResult(unittest.TestCase):
    """Test cases for DeleteTableBucketEncryptionResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = DeleteTableBucketEncryptionResult()


class TestGetTableBucketEncryptionRequest(unittest.TestCase):
    """Test cases for GetTableBucketEncryptionRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTableBucketEncryptionRequest()
        self.assertIsNone(request.table_bucket_arn)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = GetTableBucketEncryptionRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")


class TestGetTableBucketEncryptionResult(unittest.TestCase):
    """Test cases for GetTableBucketEncryptionResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTableBucketEncryptionResult()
        self.assertIsNone(result.encryption_configuration)

    def test_init_with_encryption_configuration(self):
        """Test initialization with encryption configuration."""
        encryption_config = EncryptionConfiguration(
            sse_algorithm="AES256",
            kms_key_arn="arn:acs:kms:cn-hangzhou:123456789012:key/12345678-1234-1234-1234-123456789012"
        )
        result = GetTableBucketEncryptionResult(encryption_configuration=encryption_config)
        self.assertIsNotNone(result.encryption_configuration)
        self.assertEqual(result.encryption_configuration.sse_algorithm, "AES256")
        self.assertEqual(result.encryption_configuration.kms_key_arn, "arn:acs:kms:cn-hangzhou:123456789012:key/12345678-1234-1234-1234-123456789012")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("encryption_configuration", GetTableBucketEncryptionResult._attribute_map)
        self.assertEqual(GetTableBucketEncryptionResult._attribute_map["encryption_configuration"]["rename"], "encryptionConfiguration")


class TestPutTableBucketEncryptionRequest(unittest.TestCase):
    """Test cases for PutTableBucketEncryptionRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = PutTableBucketEncryptionRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.encryption_configuration)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = PutTableBucketEncryptionRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertIsNone(request.encryption_configuration)

    def test_init_with_encryption_configuration(self):
        """Test initialization with encryption configuration."""
        encryption_config = EncryptionConfiguration(sse_algorithm="KMS")
        request = PutTableBucketEncryptionRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            encryption_configuration=encryption_config
        )
        self.assertIsNotNone(request.encryption_configuration)
        self.assertEqual(request.encryption_configuration.sse_algorithm, "KMS")

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        encryption_config = EncryptionConfiguration(
            sse_algorithm="KMS",
            kms_key_arn="arn:acs:kms:cn-hangzhou:123456789012:key/key-id"
        )
        request = PutTableBucketEncryptionRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            encryption_configuration=encryption_config
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.encryption_configuration.sse_algorithm, "KMS")
        self.assertEqual(request.encryption_configuration.kms_key_arn, "arn:acs:kms:cn-hangzhou:123456789012:key/key-id")


class TestPutTableBucketEncryptionResult(unittest.TestCase):
    """Test cases for PutTableBucketEncryptionResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = PutTableBucketEncryptionResult()


class TestGetTableBucketMaintenanceConfigurationRequest(unittest.TestCase):
    """Test cases for GetTableBucketMaintenanceConfigurationRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTableBucketMaintenanceConfigurationRequest()
        self.assertIsNone(request.table_bucket_arn)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = GetTableBucketMaintenanceConfigurationRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", GetTableBucketMaintenanceConfigurationRequest._attribute_map)
        self.assertEqual(GetTableBucketMaintenanceConfigurationRequest._attribute_map["table_bucket_arn"]["position"], "header")
        self.assertEqual(GetTableBucketMaintenanceConfigurationRequest._attribute_map["table_bucket_arn"]["rename"], "x-oss-table-bucket-arn")


class TestGetTableBucketMaintenanceConfigurationResult(unittest.TestCase):
    """Test cases for GetTableBucketMaintenanceConfigurationResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTableBucketMaintenanceConfigurationResult()
        self.assertIsNone(result.maintenance_configuration)

    def test_init_with_maintenance_configuration(self):
        """Test initialization with maintenance configuration."""
        config = {
            "icebergUnreferencedFileRemoval": {
                "enabled": True,
                "unreferencedDays": 30
            }
        }
        result = GetTableBucketMaintenanceConfigurationResult(maintenance_configuration=config)
        self.assertEqual(result.maintenance_configuration, config)
        self.assertEqual(result.maintenance_configuration["icebergUnreferencedFileRemoval"]["enabled"], True)


class TestPutTableBucketMaintenanceConfigurationRequest(unittest.TestCase):
    """Test cases for PutTableBucketMaintenanceConfigurationRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = PutTableBucketMaintenanceConfigurationRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.maintenance_configuration)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = PutTableBucketMaintenanceConfigurationRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertIsNone(request.maintenance_configuration)

    def test_init_with_maintenance_configuration(self):
        """Test initialization with maintenance configuration."""
        config = {"icebergUnreferencedFileRemoval": {"enabled": True}}
        request = PutTableBucketMaintenanceConfigurationRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            maintenance_configuration=config
        )
        self.assertEqual(request.maintenance_configuration, config)

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        config = {
            "icebergUnreferencedFileRemoval": {
                "enabled": True,
                "unreferencedDays": 30,
                "nonCurrentDays": 7
            }
        }
        request = PutTableBucketMaintenanceConfigurationRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            maintenance_configuration=config
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.maintenance_configuration["icebergUnreferencedFileRemoval"]["unreferencedDays"], 30)


class TestPutTableBucketMaintenanceConfigurationResult(unittest.TestCase):
    """Test cases for PutTableBucketMaintenanceConfigurationResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = PutTableBucketMaintenanceConfigurationResult()


class TestDeleteTableBucketPolicyRequest(unittest.TestCase):
    """Test cases for DeleteTableBucketPolicyRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = DeleteTableBucketPolicyRequest()
        self.assertIsNone(request.table_bucket_arn)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = DeleteTableBucketPolicyRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")


class TestDeleteTableBucketPolicyResult(unittest.TestCase):
    """Test cases for DeleteTableBucketPolicyResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = DeleteTableBucketPolicyResult()


class TestGetTableBucketPolicyRequest(unittest.TestCase):
    """Test cases for GetTableBucketPolicyRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetTableBucketPolicyRequest()
        self.assertIsNone(request.table_bucket_arn)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = GetTableBucketPolicyRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")


class TestGetTableBucketPolicyResult(unittest.TestCase):
    """Test cases for GetTableBucketPolicyResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetTableBucketPolicyResult()
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
        result = GetTableBucketPolicyResult(policy=policy)
        self.assertEqual(result.policy, policy)
        self.assertEqual(result.policy["Version"], "1")


class TestPutTableBucketPolicyRequest(unittest.TestCase):
    """Test cases for PutTableBucketPolicyRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = PutTableBucketPolicyRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.policy)

    def test_init_with_table_bucket_arn(self):
        """Test initialization with table_bucket_arn."""
        request = PutTableBucketPolicyRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertIsNone(request.policy)

    def test_init_with_policy(self):
        """Test initialization with policy."""
        policy = {"Version": "1", "Statement": []}
        request = PutTableBucketPolicyRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            policy=policy
        )
        self.assertEqual(request.policy, policy)

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        policy = {
            "Version": "1",
            "Statement": [{
                "Effect": "Allow",
                "Action": "oss:*",
                "Resource": "*"
            }]
        }
        request = PutTableBucketPolicyRequest(
            table_bucket_arn="arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            policy=policy
        )
        self.assertEqual(request.table_bucket_arn, "arn:acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket")
        self.assertEqual(request.policy["Statement"][0]["Effect"], "Allow")


class TestPutTableBucketPolicyResult(unittest.TestCase):
    """Test cases for PutTableBucketPolicyResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = PutTableBucketPolicyResult()


if __name__ == '__main__':
    unittest.main()
