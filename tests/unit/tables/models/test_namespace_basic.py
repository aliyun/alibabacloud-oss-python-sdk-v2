# -*- coding: utf-8 -*-
"""Unit tests for tables namespace_basic models."""

import unittest
from alibabacloud_oss_v2.tables.models.namespace_basic import (
    CreateNamespaceRequest,
    CreateNamespaceResult,
    DeleteNamespaceRequest,
    DeleteNamespaceResult,
    GetNamespaceRequest,
    GetNamespaceResult,
    ListNamespacesRequest,
    ListNamespacesResult,
)
from alibabacloud_oss_v2.tables.models.common import NamespaceSummary


class TestCreateNamespaceRequest(unittest.TestCase):
    """Test cases for CreateNamespaceRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = CreateNamespaceRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = CreateNamespaceRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace=["my_namespace"]
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.namespace, ["my_namespace"])

    def test_init_with_multi_level_namespace(self):
        """Test initialization with multi-level namespace."""
        request = CreateNamespaceRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace=["level1", "level2", "level3"]
        )
        self.assertEqual(len(request.namespace), 3)
        self.assertEqual(request.namespace[0], "level1")
        self.assertEqual(request.namespace[2], "level3")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", CreateNamespaceRequest._attribute_map)
        self.assertIn("namespace", CreateNamespaceRequest._attribute_map)
        self.assertTrue(CreateNamespaceRequest._attribute_map["table_bucket_arn"]["required"])
        self.assertEqual(CreateNamespaceRequest._attribute_map["table_bucket_arn"]["position"], "host")
        self.assertEqual(CreateNamespaceRequest._attribute_map["namespace"]["position"], "body")


class TestCreateNamespaceResult(unittest.TestCase):
    """Test cases for CreateNamespaceResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = CreateNamespaceResult()
        self.assertIsNone(result.table_bucket_arn)
        self.assertIsNone(result.namespace)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        result = CreateNamespaceResult(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace=["my_namespace"]
        )
        self.assertEqual(result.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(result.namespace, ["my_namespace"])

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", CreateNamespaceResult._attribute_map)
        self.assertIn("namespace", CreateNamespaceResult._attribute_map)
        self.assertEqual(CreateNamespaceResult._attribute_map["table_bucket_arn"]["rename"], "tableBucketARN")
        self.assertEqual(CreateNamespaceResult._attribute_map["namespace"]["rename"], "namespace")


class TestDeleteNamespaceRequest(unittest.TestCase):
    """Test cases for DeleteNamespaceRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = DeleteNamespaceRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = DeleteNamespaceRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="my_namespace"
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.namespace, "my_namespace")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", DeleteNamespaceRequest._attribute_map)
        self.assertIn("namespace", DeleteNamespaceRequest._attribute_map)
        self.assertTrue(DeleteNamespaceRequest._attribute_map["table_bucket_arn"]["required"])
        self.assertTrue(DeleteNamespaceRequest._attribute_map["namespace"]["required"])
        self.assertEqual(DeleteNamespaceRequest._attribute_map["namespace"]["position"], "path")


class TestDeleteNamespaceResult(unittest.TestCase):
    """Test cases for DeleteNamespaceResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = DeleteNamespaceResult()


class TestGetNamespaceRequest(unittest.TestCase):
    """Test cases for GetNamespaceRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = GetNamespaceRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.namespace)

    def test_init_with_fields(self):
        """Test initialization with fields."""
        request = GetNamespaceRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            namespace="my_namespace"
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.namespace, "my_namespace")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", GetNamespaceRequest._attribute_map)
        self.assertIn("namespace", GetNamespaceRequest._attribute_map)
        self.assertTrue(GetNamespaceRequest._attribute_map["table_bucket_arn"]["required"])
        self.assertTrue(GetNamespaceRequest._attribute_map["namespace"]["required"])
        self.assertEqual(GetNamespaceRequest._attribute_map["table_bucket_arn"]["position"], "host")
        self.assertEqual(GetNamespaceRequest._attribute_map["namespace"]["position"], "path")


class TestGetNamespaceResult(unittest.TestCase):
    """Test cases for GetNamespaceResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = GetNamespaceResult()
        self.assertIsNone(result.namespace)
        self.assertIsNone(result.namespace_id)
        self.assertIsNone(result.table_bucket_id)
        self.assertIsNone(result.owner_account_id)
        self.assertIsNone(result.created_at)
        self.assertIsNone(result.created_by)

    def test_init_with_basic_fields(self):
        """Test initialization with basic fields."""
        result = GetNamespaceResult(
            namespace=["my_namespace"],
            namespace_id="ns-xxxxxxxx",
            table_bucket_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            owner_account_id="1234567890",
            created_at="2024-01-01T00:00:00Z",
            created_by="1234567890"
        )
        self.assertEqual(result.namespace, ["my_namespace"])
        self.assertEqual(result.namespace_id, "ns-xxxxxxxx")
        self.assertEqual(result.table_bucket_id, "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.assertEqual(result.owner_account_id, "1234567890")
        self.assertEqual(result.created_at, "2024-01-01T00:00:00Z")
        self.assertEqual(result.created_by, "1234567890")

    def test_init_with_multi_level_namespace(self):
        """Test initialization with multi-level namespace."""
        result = GetNamespaceResult(
            namespace=["level1", "level2"]
        )
        self.assertEqual(len(result.namespace), 2)
        self.assertEqual(result.namespace[0], "level1")
        self.assertEqual(result.namespace[1], "level2")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("namespace", GetNamespaceResult._attribute_map)
        self.assertIn("namespace_id", GetNamespaceResult._attribute_map)
        self.assertIn("table_bucket_id", GetNamespaceResult._attribute_map)
        self.assertIn("owner_account_id", GetNamespaceResult._attribute_map)
        self.assertIn("created_at", GetNamespaceResult._attribute_map)
        self.assertIn("created_by", GetNamespaceResult._attribute_map)
        self.assertEqual(GetNamespaceResult._attribute_map["namespace_id"]["rename"], "namespaceId")
        self.assertEqual(GetNamespaceResult._attribute_map["table_bucket_id"]["rename"], "tableBucketId")
        self.assertEqual(GetNamespaceResult._attribute_map["owner_account_id"]["rename"], "ownerAccountId")


class TestListNamespacesRequest(unittest.TestCase):
    """Test cases for ListNamespacesRequest model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        request = ListNamespacesRequest()
        self.assertIsNone(request.table_bucket_arn)
        self.assertIsNone(request.prefix)
        self.assertIsNone(request.continuation_token)
        self.assertIsNone(request.max_namespaces)

    def test_init_with_required_fields(self):
        """Test initialization with required fields."""
        request = ListNamespacesRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket"
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertIsNone(request.prefix)
        self.assertIsNone(request.continuation_token)
        self.assertIsNone(request.max_namespaces)

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        request = ListNamespacesRequest(
            table_bucket_arn="acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket",
            prefix="test_",
            continuation_token="abc123",
            max_namespaces=100
        )
        self.assertEqual(request.table_bucket_arn, "acs:osstable:cn-hangzhou:1234567890:bucket/test-table-bucket")
        self.assertEqual(request.prefix, "test_")
        self.assertEqual(request.continuation_token, "abc123")
        self.assertEqual(request.max_namespaces, 100)

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("table_bucket_arn", ListNamespacesRequest._attribute_map)
        self.assertIn("prefix", ListNamespacesRequest._attribute_map)
        self.assertIn("continuation_token", ListNamespacesRequest._attribute_map)
        self.assertIn("max_namespaces", ListNamespacesRequest._attribute_map)
        self.assertTrue(ListNamespacesRequest._attribute_map["table_bucket_arn"]["required"])
        self.assertEqual(ListNamespacesRequest._attribute_map["prefix"]["position"], "query")
        self.assertEqual(ListNamespacesRequest._attribute_map["continuation_token"]["rename"], "continuationToken")
        self.assertEqual(ListNamespacesRequest._attribute_map["max_namespaces"]["rename"], "maxNamespaces")


class TestListNamespacesResult(unittest.TestCase):
    """Test cases for ListNamespacesResult model."""

    def test_empty_init(self):
        """Test initialization with no parameters."""
        result = ListNamespacesResult()
        self.assertIsNone(result.namespaces)
        self.assertIsNone(result.continuation_token)

    def test_init_with_continuation_token(self):
        """Test initialization with continuation_token."""
        result = ListNamespacesResult(continuation_token="abc123")
        self.assertIsNone(result.namespaces)
        self.assertEqual(result.continuation_token, "abc123")

    def test_init_with_namespaces(self):
        """Test initialization with namespace summaries."""
        ns1 = NamespaceSummary(
            namespace=["ns1"],
            namespace_id="ns-001",
            owner_account_id="1234567890",
            created_by="1234567890"
        )
        ns2 = NamespaceSummary(
            namespace=["ns2"],
            namespace_id="ns-002",
            owner_account_id="1234567890",
            created_by="1234567890"
        )
        result = ListNamespacesResult(
            namespaces=[ns1, ns2],
            continuation_token="next_token"
        )
        self.assertEqual(len(result.namespaces), 2)
        self.assertEqual(result.namespaces[0].namespace, ["ns1"])
        self.assertEqual(result.namespaces[0].namespace_id, "ns-001")
        self.assertEqual(result.namespaces[1].namespace, ["ns2"])
        self.assertEqual(result.continuation_token, "next_token")

    def test_attribute_map(self):
        """Test _attribute_map contains correct mappings."""
        self.assertIn("namespaces", ListNamespacesResult._attribute_map)
        self.assertIn("continuation_token", ListNamespacesResult._attribute_map)
        self.assertEqual(ListNamespacesResult._attribute_map["namespaces"]["rename"], "namespaces")
        self.assertEqual(ListNamespacesResult._attribute_map["continuation_token"]["rename"], "continuationToken")


if __name__ == '__main__':
    unittest.main()
