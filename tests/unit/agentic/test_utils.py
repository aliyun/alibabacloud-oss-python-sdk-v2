# pylint: skip-file
import unittest
from urllib.parse import urlparse
from alibabacloud_oss_v2.agentic.utils import AgenticProvider, BucketSpaceHelper
from alibabacloud_oss_v2.config import Config
from alibabacloud_oss_v2.types import OperationInput


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
