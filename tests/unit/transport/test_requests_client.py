import unittest
from alibabacloud_oss_v2.transport.requests_client import convert_proxy_host
from alibabacloud_oss_v2 import exceptions


class TestRequestsClient(unittest.TestCase):
    def test_TC01_proxy_host_none(self):
        """TC01: When proxy_host is None, return None"""
        result = convert_proxy_host(None)
        self.assertIsNone(result)

    def test_TC02_str_no_scheme_disable_ssl_none(self):
        """TC02: proxy_host is a string with no scheme and disable_ssl is None, return both HTTP and HTTPS"""
        result = convert_proxy_host("127.0.0.1:8080")
        expected = {"http://": "127.0.0.1:8080", "https://": "127.0.0.1:8080"}
        self.assertEqual(result, expected)

    def test_TC03_str_with_http_scheme_disable_ssl_true(self):
        """TC03: proxy_host has http:// scheme and disable_ssl=True, return HTTP only"""
        result = convert_proxy_host("http://127.0.0.1:8080", disable_ssl=True)
        expected = {"http://": "http://127.0.0.1:8080"}
        self.assertEqual(result, expected)

    def test_TC04_str_with_https_scheme_disable_ssl_false(self):
        """TC04: proxy_host has https:// scheme and disable_ssl=False, return HTTPS only"""
        result = convert_proxy_host("https://127.0.0.1:8080", disable_ssl=False)
        expected = {"https://": "https://127.0.0.1:8080"}
        self.assertEqual(result, expected)

    def test_TC05_str_no_scheme_disable_ssl_true(self):
        """TC05: proxy_host has no scheme, disable_ssl=True → auto-prepend http://"""
        result = convert_proxy_host("127.0.0.1:8080", disable_ssl=True)
        expected = {"http://": "http://127.0.0.1:8080"}
        self.assertEqual(result, expected)

    def test_TC06_str_no_scheme_disable_ssl_false(self):
        """TC06: proxy_host has no scheme, disable_ssl=False → auto-prepend https://"""
        result = convert_proxy_host("127.0.0.1:8080", disable_ssl=False)
        expected = {"https://": "https://127.0.0.1:8080"}
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
