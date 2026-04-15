# -*- coding: utf-8 -*-
"""Unit tests for tables endpoints provider."""

import unittest
from urllib.parse import urlparse

from alibabacloud_oss_v2.tables.endpoints import TablesEndpointProvider, from_region
from alibabacloud_oss_v2._client import AddressStyle
from alibabacloud_oss_v2.types import OperationInput


class TestFromRegion(unittest.TestCase):
    """Test cases for from_region function."""

    def test_default_endpoint(self):
        """Test default endpoint generation."""
        endpoint = from_region("cn-hangzhou", "default")
        self.assertEqual(endpoint, "cn-hangzhou.oss-tables.aliyuncs.com")

    def test_internal_endpoint(self):
        """Test internal endpoint generation."""
        endpoint = from_region("cn-shanghai", "internal")
        self.assertEqual(endpoint, "cn-shanghai-internal.oss-tables.aliyuncs.com")

    def test_other_region(self):
        """Test endpoint generation for other regions."""
        endpoint = from_region("cn-beijing", "default")
        self.assertEqual(endpoint, "cn-beijing.oss-tables.aliyuncs.com")


class TestTablesEndpointProviderVirtualHosted(unittest.TestCase):
    """Test cases for TablesEndpointProvider with VirtualHosted address style."""

    def setUp(self):
        """Set up test fixtures."""
        self.endpoint = urlparse("https://oss-cn-hangzhou.oss-tables.aliyuncs.com")
        self.provider = TablesEndpointProvider(self.endpoint, AddressStyle.Virtual)

    def test_no_bucket_no_key(self):
        """Test build URL with neither bucket nor key."""
        op_input = OperationInput(op_name="ListBuckets", method="GET")
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://oss-cn-hangzhou.oss-tables.aliyuncs.com/")

    def test_key_only(self):
        """Test build URL with key only."""
        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            key="test-key"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://oss-cn-hangzhou.oss-tables.aliyuncs.com/test-key")

    def test_bucket_arn_only(self):
        """Test build URL with bucket ARN only."""
        op_input = OperationInput(
            op_name="GetTableBucket",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://test-bucket-123456789012.oss-cn-hangzhou.oss-tables.aliyuncs.com/")

    def test_bucket_arn_with_key(self):
        """Test build URL with bucket ARN and key."""
        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            key="test-key"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://test-bucket-123456789012.oss-cn-hangzhou.oss-tables.aliyuncs.com/test-key")

    def test_bucket_arn_with_special_chars_key(self):
        """Test build URL with bucket ARN and special characters in key."""
        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            key="test%20key"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://test-bucket-123456789012.oss-cn-hangzhou.oss-tables.aliyuncs.com/test%20key")

    def test_java_style_bucket_arn(self):
        """Test build URL with Java-style ARN format (without arn: prefix)."""
        op_input = OperationInput(
            op_name="GetTableBucket",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:test-account:test-bucket/table"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://table-test-account.oss-cn-hangzhou.oss-tables.aliyuncs.com/")

    def test_java_style_bucket_arn_with_key(self):
        """Test build URL with Java-style ARN and key."""
        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:test-account:test-bucket/table",
            key="test-key"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://table-test-account.oss-cn-hangzhou.oss-tables.aliyuncs.com/test-key")

    def test_invalid_bucket_arn_too_few_parts(self):
        """Test build URL with invalid ARN (too few parts)."""
        op_input = OperationInput(
            op_name="GetTableBucket",
            method="GET",
            bucket="invalid-bucket-arn"
        )
        with self.assertRaises(ValueError) as context:
            self.provider.build_url(op_input)
        self.assertIn("not bucket arn", str(context.exception))

    def test_invalid_bucket_arn_missing_slash(self):
        """Test build URL with invalid ARN (missing slash in last part)."""
        op_input = OperationInput(
            op_name="GetTableBucket",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket"
        )
        with self.assertRaises(ValueError) as context:
            self.provider.build_url(op_input)
        self.assertIn("not bucket arn", str(context.exception))


class TestTablesEndpointProviderWithPath(unittest.TestCase):
    """Test cases for TablesEndpointProvider with Path address style."""

    def setUp(self):
        """Set up test fixtures."""
        self.endpoint = urlparse("https://oss-cn-hangzhou.oss-tables.aliyuncs.com")
        self.provider = TablesEndpointProvider(self.endpoint, AddressStyle.Path)

    def test_no_bucket_no_key(self):
        """Test build URL with neither bucket nor key."""
        op_input = OperationInput(op_name="ListBuckets", method="GET")
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://oss-cn-hangzhou.oss-tables.aliyuncs.com/")

    def test_key_only(self):
        """Test build URL with key only."""
        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            key="test-key"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://oss-cn-hangzhou.oss-tables.aliyuncs.com/test-key")

    def test_bucket_arn_only(self):
        """Test build URL with bucket ARN only (host unchanged in Path style)."""
        op_input = OperationInput(
            op_name="GetTableBucket",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://oss-cn-hangzhou.oss-tables.aliyuncs.com/")

    def test_bucket_arn_with_key(self):
        """Test build URL with bucket ARN and key."""
        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            key="test-key"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://oss-cn-hangzhou.oss-tables.aliyuncs.com/test-key")


class TestTablesEndpointProviderWithCName(unittest.TestCase):
    """Test cases for TablesEndpointProvider with CName address style."""

    def setUp(self):
        """Set up test fixtures."""
        self.endpoint = urlparse("https://custom-domain.example.com")
        self.provider = TablesEndpointProvider(self.endpoint, AddressStyle.CName)

    def test_no_bucket_no_key(self):
        """Test build URL with neither bucket nor key."""
        op_input = OperationInput(op_name="ListBuckets", method="GET")
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://custom-domain.example.com/")

    def test_key_only(self):
        """Test build URL with key only."""
        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            key="test-key"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://custom-domain.example.com/test-key")

    def test_bucket_arn_only(self):
        """Test build URL with bucket ARN only (host unchanged in CName style)."""
        op_input = OperationInput(
            op_name="GetTableBucket",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://custom-domain.example.com/")

    def test_bucket_arn_with_key(self):
        """Test build URL with bucket ARN and key."""
        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            key="test-key"
        )
        url = self.provider.build_url(op_input)
        self.assertEqual(url, "https://custom-domain.example.com/test-key")


class TestTablesEndpointProviderInternalEndpoint(unittest.TestCase):
    """Test cases for TablesEndpointProvider with internal endpoints."""

    def test_internal_endpoint_no_bucket(self):
        """Test build URL with internal endpoint."""
        endpoint = urlparse("https://oss-cn-shanghai-internal.oss-tables.aliyuncs.com")
        provider = TablesEndpointProvider(endpoint, AddressStyle.Virtual)

        op_input = OperationInput(op_name="ListBuckets", method="GET")
        url = provider.build_url(op_input)
        self.assertEqual(url, "https://oss-cn-shanghai-internal.oss-tables.aliyuncs.com/")

    def test_internal_endpoint_with_bucket(self):
        """Test build URL with internal endpoint and bucket ARN."""
        endpoint = urlparse("https://oss-cn-shanghai-internal.oss-tables.aliyuncs.com")
        provider = TablesEndpointProvider(endpoint, AddressStyle.Virtual)

        op_input = OperationInput(
            op_name="GetTableBucket",
            method="GET",
            bucket="acs:oss-tables:cn-shanghai:123456789012:bucket/test-bucket"
        )
        url = provider.build_url(op_input)
        self.assertEqual(url, "https://test-bucket-123456789012.oss-cn-shanghai-internal.oss-tables.aliyuncs.com/")


class TestTablesEndpointProviderDefaultAddressStyle(unittest.TestCase):
    """Test cases for TablesEndpointProvider default address style."""

    def test_default_is_virtual(self):
        """Test that default address style is Virtual."""
        endpoint = urlparse("https://oss-cn-hangzhou.oss-tables.aliyuncs.com")
        provider = TablesEndpointProvider(endpoint)

        op_input = OperationInput(
            op_name="GetTableBucket",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket"
        )
        url = provider.build_url(op_input)
        self.assertEqual(url, "https://test-bucket-123456789012.oss-cn-hangzhou.oss-tables.aliyuncs.com/")


class TestTablesEndpointProviderEdgeCases(unittest.TestCase):
    """Test cases for TablesEndpointProvider edge cases."""

    def test_http_endpoint(self):
        """Test build URL with HTTP endpoint."""
        endpoint = urlparse("http://oss-cn-shenzhen.aliyuncs.com")
        provider = TablesEndpointProvider(endpoint, AddressStyle.Virtual)

        op_input = OperationInput(op_name="ListBuckets", method="GET")
        url = provider.build_url(op_input)
        self.assertEqual(url, "http://oss-cn-shenzhen.aliyuncs.com/")

    def test_nested_path_key(self):
        """Test build URL with nested path in key."""
        endpoint = urlparse("https://oss-cn-hangzhou.oss-tables.aliyuncs.com")
        provider = TablesEndpointProvider(endpoint, AddressStyle.Virtual)

        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            key="path/to/nested/object"
        )
        url = provider.build_url(op_input)
        self.assertEqual(url, "https://test-bucket-123456789012.oss-cn-hangzhou.oss-tables.aliyuncs.com/path/to/nested/object")

    def test_empty_key(self):
        """Test build URL with empty key."""
        endpoint = urlparse("https://oss-cn-hangzhou.oss-tables.aliyuncs.com")
        provider = TablesEndpointProvider(endpoint, AddressStyle.Virtual)

        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            bucket="acs:oss-tables:cn-hangzhou:123456789012:bucket/test-bucket",
            key=""
        )
        url = provider.build_url(op_input)
        self.assertEqual(url, "https://test-bucket-123456789012.oss-cn-hangzhou.oss-tables.aliyuncs.com/")


if __name__ == '__main__':
    unittest.main()
