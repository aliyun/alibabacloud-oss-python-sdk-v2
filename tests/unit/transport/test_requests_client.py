import unittest
from alibabacloud_oss_v2.transport.requests_client import convert_proxy_host
from alibabacloud_oss_v2 import exceptions


class TestRequestsClient(unittest.TestCase):
    def test_TC01_proxy_host_none(self):
        """TC01: When proxy_host is None, return None"""
        result = convert_proxy_host(None)
        self.assertIsNone(result)

    def test_TC02_str_no_scheme(self):
        """TC02: proxy_host is a string with no scheme, return both HTTP and HTTPS"""
        result = convert_proxy_host("127.0.0.1:8080")
        expected = {"http://": "127.0.0.1:8080", "https://": "127.0.0.1:8080"}
        self.assertEqual(result, expected)

    def test_TC02_str_with_scheme(self):
        """TC02: proxy_host is a string with scheme, return both HTTP and HTTPS"""
        result = convert_proxy_host("http://127.0.0.1:8080")
        expected = {"http://": "http://127.0.0.1:8080", "https://": "http://127.0.0.1:8080"}
        self.assertEqual(result, expected)

    def test_TC07_dict_input(self):
        """TC07: proxy_host is a dict → return it directly"""
        input_dict = {"http://": "http://127.0.0.1:8080"}
        result = convert_proxy_host(input_dict)
        self.assertEqual(result, input_dict)

    def test_TC08_invalid_type(self):
        """TC08: Invalid input type → raise RequestError"""
        with self.assertRaises(exceptions.RequestError) as cm:
            convert_proxy_host(12345)
        self.assertIn("proxy_host must be str or dict", str(cm.exception))
