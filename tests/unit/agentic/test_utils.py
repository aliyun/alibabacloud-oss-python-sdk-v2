# pylint: skip-file
import unittest
from urllib.parse import urlparse
from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.agentic.utils import AgenticProvider, BucketSpaceHelper
from alibabacloud_oss_v2.config import Config
from alibabacloud_oss_v2.types import OperationInput
from alibabacloud_oss_v2._client import AddressStyle


class TestAgenticProvider(unittest.TestCase):
    def _provider(self, suffix="ab-apsr"):
        endpoint = urlparse("https://oss-cn-hangzhou.aliyuncs.com")
        return AgenticProvider(
            endpoint=endpoint,
            account_id="1234567890123456",
            region="cn-hangzhou",
            suffix=suffix,
        )

    def test_init(self):
        provider = AgenticProvider(
            endpoint=urlparse("https://oss-cn-hangzhou.aliyuncs.com"),
            account_id=None,
            region=None,
            suffix="ab-apsr",
        )
        self.assertEqual("", provider._account_id)
        self.assertEqual("", provider._region)
        self.assertEqual("ab-apsr", provider._suffix)

    def test_build_bucket_name(self):
        provider = self._provider()
        op_input = OperationInput(op_name="GetAgenticBucket", method="GET", bucket="my-agentic")
        self.assertEqual(
            "my-agentic-1234567890123456-cn-hangzhou-ab-apsr",
            provider.build_bucket_name(op_input),
        )

    def test_build_bucket_name_none(self):
        provider = self._provider()
        op_input = OperationInput(op_name="ListAgenticBuckets", method="GET")
        self.assertIsNone(provider.build_bucket_name(op_input))

    def test_build_bucket_name_bs_suffix(self):
        provider = self._provider(suffix="bs-apsr")
        op_input = OperationInput(op_name="GetBucket", method="GET", bucket="my-agent")
        self.assertEqual(
            "my-agent-1234567890123456-cn-hangzhou-bs-apsr",
            provider.build_bucket_name(op_input),
        )

    def test_build_url_no_bucket(self):
        provider = self._provider()
        op_input = OperationInput(op_name="ListAgenticBuckets", method="GET")
        self.assertEqual(
            "https://oss-cn-hangzhou.aliyuncs.com/",
            provider.build_url(op_input),
        )

    def test_build_url_with_bucket(self):
        provider = self._provider()
        # build_url re-derives the full name from the logical prefix.
        op_input = OperationInput(
            op_name="GetAgenticBucket",
            method="GET",
            bucket="my-agentic",
        )
        self.assertEqual(
            "https://my-agentic-1234567890123456-cn-hangzhou-ab-apsr.oss-cn-hangzhou.aliyuncs.com/",
            provider.build_url(op_input),
        )

    def test_build_url_with_key(self):
        provider = self._provider()
        op_input = OperationInput(
            op_name="GetObject",
            method="GET",
            bucket="my-agentic",
            key="dir/obj key+value",
        )
        self.assertEqual(
            "https://my-agentic-1234567890123456-cn-hangzhou-ab-apsr.oss-cn-hangzhou.aliyuncs.com/dir/obj%20key%2Bvalue",
            provider.build_url(op_input),
        )


    def test_build_url_path_style_with_bucket(self):
        endpoint = urlparse("https://oss-cn-hangzhou.aliyuncs.com")
        provider = AgenticProvider(
            endpoint=endpoint,
            account_id="1234567890123456",
            region="cn-hangzhou",
            suffix="ab-apsr",
            address_style=AddressStyle.Path,
        )
        op_input = OperationInput(op_name="GetAgenticBucket", method="GET", bucket="my-agentic")
        self.assertEqual(
            "https://oss-cn-hangzhou.aliyuncs.com/my-agentic-1234567890123456-cn-hangzhou-ab-apsr/",
            provider.build_url(op_input),
        )

    def test_build_url_path_style_with_key(self):
        endpoint = urlparse("https://oss-cn-hangzhou.aliyuncs.com")
        provider = AgenticProvider(
            endpoint=endpoint,
            account_id="1234567890123456",
            region="cn-hangzhou",
            suffix="bs-apsr",
            address_style=AddressStyle.Path,
        )
        op_input = OperationInput(
            op_name="GetObject", method="GET", bucket="my-space", key="dir/obj key+value")
        self.assertEqual(
            "https://oss-cn-hangzhou.aliyuncs.com/my-space-1234567890123456-cn-hangzhou-bs-apsr/dir/obj%20key%2Bvalue",
            provider.build_url(op_input),
        )

    def test_build_url_path_style_no_bucket(self):
        endpoint = urlparse("https://oss-cn-hangzhou.aliyuncs.com")
        provider = AgenticProvider(
            endpoint=endpoint,
            account_id="1234567890123456",
            region="cn-hangzhou",
            suffix="ab-apsr",
            address_style=AddressStyle.Path,
        )
        op_input = OperationInput(op_name="ListAgenticBuckets", method="GET")
        self.assertEqual(
            "https://oss-cn-hangzhou.aliyuncs.com/",
            provider.build_url(op_input),
        )

    def test_missing_required_fields(self):
        endpoint = urlparse("https://oss-cn-hangzhou.aliyuncs.com")
        op_input = OperationInput(op_name="GetAgenticBucket", method="GET", bucket="my-agentic")

        # Missing account_id
        p = AgenticProvider(endpoint=endpoint, account_id="", region="cn-hangzhou", suffix="ab-apsr")
        with self.assertRaises(exceptions.ParamRequiredError) as ctx:
            p.build_url(op_input)
        self.assertIn("AccountId", str(ctx.exception))
        with self.assertRaises(exceptions.ParamRequiredError) as ctx:
            p.build_bucket_name(op_input)
        self.assertIn("AccountId", str(ctx.exception))

        # Missing region
        p = AgenticProvider(endpoint=endpoint, account_id="1234567890123456", region="", suffix="ab-apsr")
        with self.assertRaises(exceptions.ParamRequiredError) as ctx:
            p.build_url(op_input)
        self.assertIn("Region", str(ctx.exception))
        with self.assertRaises(exceptions.ParamRequiredError) as ctx:
            p.build_bucket_name(op_input)
        self.assertIn("Region", str(ctx.exception))

        # No bucket: validation is skipped, no error
        self.assertIsNone(
            p.build_bucket_name(OperationInput(op_name="ListAgenticBuckets", method="GET")))

    def test_host_label_too_long(self):
        endpoint = urlparse("https://oss-cn-hangzhou.aliyuncs.com")
        # full name = "{bucket}-1234567890123456-cn-hangzhou-ab-apsr" -> len(bucket) + 37
        suffix_part = "-1234567890123456-cn-hangzhou-ab-apsr"
        p = AgenticProvider(
            endpoint=endpoint, account_id="1234567890123456", region="cn-hangzhou", suffix="ab-apsr")

        # Boundary: full name == 63 (bucket 26) is allowed in virtual-hosted style
        ok_name = "a" * 26
        self.assertEqual(63, len(ok_name + suffix_part))
        self.assertEqual(
            f"https://{ok_name}{suffix_part}.oss-cn-hangzhou.aliyuncs.com/",
            p.build_url(OperationInput(op_name="GetAgenticBucket", method="GET", bucket=ok_name)),
        )

        # Over limit: full name == 64 (bucket 27) is rejected in virtual-hosted style
        long_name = "a" * 27
        self.assertEqual(64, len(long_name + suffix_part))
        with self.assertRaises(ValueError) as ctx:
            p.build_url(OperationInput(op_name="GetAgenticBucket", method="GET", bucket=long_name))
        self.assertIn("exceeds the maximum length of 63 characters", str(ctx.exception))

        # Path style has no DNS label limit, so the same long name is fine
        path_p = AgenticProvider(
            endpoint=endpoint, account_id="1234567890123456", region="cn-hangzhou",
            suffix="ab-apsr", address_style=AddressStyle.Path)
        self.assertEqual(
            f"https://oss-cn-hangzhou.aliyuncs.com/{long_name}{suffix_part}/",
            path_p.build_url(OperationInput(op_name="GetAgenticBucket", method="GET", bucket=long_name)),
        )


class TestBucketSpaceHelper(unittest.TestCase):
    def test_to_bucket_name(self):
        cfg = Config(account_id="1234567890123456", region="cn-hangzhou")
        helper = BucketSpaceHelper(cfg)
        self.assertEqual(
            "my-agent-1234567890123456-cn-hangzhou-bs-apsr",
            helper.to_bucket_name("my-agent"),
        )

    def test_to_bucket_name_empty(self):
        cfg = Config()
        helper = BucketSpaceHelper(cfg)
        self.assertEqual("my-agent---bs-apsr", helper.to_bucket_name("my-agent"))


if __name__ == '__main__':
    unittest.main()
