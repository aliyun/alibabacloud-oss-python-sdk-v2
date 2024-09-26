# pylint: skip-file

import unittest
from alibabacloud_oss_v2.config import Config
from alibabacloud_oss_v2.credentials import AnonymousCredentialsProvider
from alibabacloud_oss_v2.retry import NopRetryer
from alibabacloud_oss_v2.transport import RequestsHttpClient


class TestConfig(unittest.TestCase):
    def test_config_with_required_args(self):
        region = 'cn-hangzhou'
        config = Config(region=region)
        self.assertEqual(config.region, region)

    def test_config_with_optional_args(self):
        region = 'cn-hangzhou'
        endpoint = 'oss-cn-hangzhou.aliyuncs.com'
        signature_version = 'v4'
        credentials_provider = AnonymousCredentialsProvider()
        retry_max_attempts = 3
        retryer = NopRetryer()
        http_client = RequestsHttpClient()
        connect_timeout = 10.0
        readwrite_timeout = 20.0
        use_dualstack_endpoint = True
        use_accelerate_endpoint = False
        use_internal_endpoint = True
        disable_ssl = False
        insecure_skip_verify = True
        enabled_redirect = True
        use_cname = False
        use_path_style = True
        proxy_host = 'http://127.0.0.1:8080'
        disable_upload_crc64_check = False
        disable_download_crc64_check = True
        additional_headers = ['host']
        user_agent = 'test'

        config = Config(
            region=region,
            endpoint=endpoint,
            signature_version=signature_version,
            credentials_provider=credentials_provider,
            retry_max_attempts=retry_max_attempts,
            retryer=retryer,
            http_client=http_client,
            connect_timeout=connect_timeout,
            readwrite_timeout=readwrite_timeout,
            use_dualstack_endpoint=use_dualstack_endpoint,
            use_accelerate_endpoint=use_accelerate_endpoint,
            use_internal_endpoint=use_internal_endpoint,
            disable_ssl=disable_ssl,
            insecure_skip_verify=insecure_skip_verify,
            enabled_redirect=enabled_redirect,
            use_cname=use_cname,
            use_path_style=use_path_style,
            proxy_host=proxy_host,
            disable_upload_crc64_check=disable_upload_crc64_check,
            disable_download_crc64_check=disable_download_crc64_check,
            additional_headers=additional_headers,
            user_agent=user_agent
        )

        self.assertEqual(config.region, region)
        self.assertEqual(config.endpoint, endpoint)
        self.assertEqual(config.signature_version, signature_version)
        self.assertEqual(config.credentials_provider, credentials_provider)
        self.assertEqual(config.retry_max_attempts, retry_max_attempts)
        self.assertEqual(config.retryer, retryer)
        self.assertEqual(config.http_client, http_client)
        self.assertEqual(config.connect_timeout, connect_timeout)
        self.assertEqual(config.readwrite_timeout, readwrite_timeout)
        self.assertEqual(config.use_dualstack_endpoint, use_dualstack_endpoint)
        self.assertEqual(config.use_accelerate_endpoint, use_accelerate_endpoint)
        self.assertEqual(config.use_internal_endpoint, use_internal_endpoint)
        self.assertEqual(config.disable_ssl, disable_ssl)
        self.assertEqual(config.insecure_skip_verify, insecure_skip_verify)
        self.assertEqual(config.enabled_redirect, enabled_redirect)
        self.assertEqual(config.use_cname, use_cname)
        self.assertEqual(config.proxy_host, proxy_host)
        self.assertEqual(config.disable_upload_crc64_check, disable_upload_crc64_check)
        self.assertEqual(config.disable_download_crc64_check, disable_download_crc64_check)
        self.assertEqual(config.additional_headers, additional_headers)
        self.assertEqual(config.user_agent, user_agent)


    def test_config_with_default_values(self):
        region = 'cn-shanghai'
        config = Config(region=region)
        self.assertEqual(config.region, region)
        self.assertIsNone(config.endpoint)
        self.assertIsNone(config.signature_version)
        self.assertIsNone(config.credentials_provider)
        self.assertIsNone(config.retry_max_attempts)
        self.assertIsNone(config.retryer)
        self.assertIsNone(config.http_client)
        self.assertIsNone(config.connect_timeout)
        self.assertIsNone(config.readwrite_timeout)
        self.assertIsNone(config.use_dualstack_endpoint)
        self.assertIsNone(config.use_accelerate_endpoint)
        self.assertIsNone(config.use_internal_endpoint)
        self.assertIsNone(config.disable_ssl)
        self.assertIsNone(config.insecure_skip_verify)
        self.assertIsNone(config.enabled_redirect)
        self.assertIsNone(config.use_cname)
        self.assertIsNone(config.proxy_host)
        self.assertIsNone(config.disable_upload_crc64_check)
        self.assertIsNone(config.disable_download_crc64_check)
        self.assertIsNone(config.additional_headers)
        self.assertIsNone(config.user_agent)

