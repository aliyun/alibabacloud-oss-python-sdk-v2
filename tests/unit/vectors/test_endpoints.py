import unittest
from urllib.parse import urlparse
from alibabacloud_oss_v2.vectors.endpoints import VectorsEndpointProvider, from_region
from alibabacloud_oss_v2.types import OperationInput

class TestVectorsEndpoints(unittest.TestCase):

    def test_from_region(self):
        result = from_region("cn-hangzhou", "")
        self.assertEqual("cn-hangzhou.oss-vectors.aliyuncs.com", result)

        result = from_region("cn-hangzhou", "internal")
        self.assertEqual("cn-hangzhou-internal.oss-vectors.aliyuncs.com", result)

    def test_vectors_endpoint_provider_init(self):
        endpoint = urlparse("https://oss-cn-hangzhou.oss-vectors.aliyuncs.com")
        provider = VectorsEndpointProvider(endpoint, "123456")

        self.assertEqual(endpoint, provider._endpoint)
        self.assertEqual("123456", provider._account_id)

        provider = VectorsEndpointProvider(endpoint, None)
        self.assertEqual("", provider._account_id)

    def test_vectors_endpoint_provider_build_url(self):
        endpoint = urlparse("https://oss-cn-hangzhou.oss-vectors.aliyuncs.com")
        provider = VectorsEndpointProvider(endpoint, "123456")

        op_input = OperationInput(
            op_name="TestOperation",
            method="GET"
        )
        url = provider.build_url(op_input)
        self.assertEqual("https://oss-cn-hangzhou.oss-vectors.aliyuncs.com/", url)

        op_input = OperationInput(
            op_name="TestOperation",
            method="GET",
            bucket="test-bucket"
        )
        url = provider.build_url(op_input)
        self.assertEqual("https://test-bucket-123456.oss-cn-hangzhou.oss-vectors.aliyuncs.com/", url)

        op_input = OperationInput(
            op_name="TestOperation",
            method="GET",
            bucket="test-bucket",
            key="test-key"
        )
        url = provider.build_url(op_input)
        self.assertEqual("https://test-bucket-123456.oss-cn-hangzhou.oss-vectors.aliyuncs.com/test-key", url)

        op_input = OperationInput(
            op_name="TestOperation",
            method="GET",
            bucket="test-bucket",
            key="test key+value"
        )
        url = provider.build_url(op_input)
        self.assertEqual("https://test-bucket-123456.oss-cn-hangzhou.oss-vectors.aliyuncs.com/test%20key%2Bvalue", url)


if __name__ == '__main__':
    unittest.main()
