# -*- coding: utf-8 -*-
"""User-Agent marker tests for the sub-clients."""

import unittest
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess
import alibabacloud_oss_v2.tables as oss_tables
import alibabacloud_oss_v2.vectors as oss_vectors
from alibabacloud_oss_v2 import credentials


def _config(user_agent=None):
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials.AnonymousCredentialsProvider()
    cfg.region = 'cn-hangzhou'
    cfg.account_id = '1234567890123456'
    cfg.user_agent = user_agent
    return cfg


class TestSubClientUserAgent(unittest.TestCase):
    """The marker sits right after the base SDK UA, the caller's UA comes last."""

    def _assert_marker(self, client, marker):
        ua = client._client._inner.user_agent
        self.assertTrue(ua.startswith('alibabacloud-python-sdk-v2/'))
        self.assertTrue(ua.endswith(f'/{marker}'), ua)

    def _assert_marker_then_custom(self, client, marker):
        ua = client._client._inner.user_agent
        self.assertTrue(ua.startswith('alibabacloud-python-sdk-v2/'))
        self.assertIn(f'/{marker}/mytool/1.0', ua)

    def test_dataprocess_marker(self):
        self._assert_marker(oss_dataprocess.Client(_config()), 'dataprocess-client')

    def test_dataprocess_marker_then_custom(self):
        client = oss_dataprocess.Client(_config('mytool/1.0'))
        self._assert_marker_then_custom(client, 'dataprocess-client')

    def test_tables_marker(self):
        self._assert_marker(oss_tables.Client(_config()), 'tables-client')

    def test_tables_marker_then_custom(self):
        self._assert_marker_then_custom(oss_tables.Client(_config('mytool/1.0')), 'tables-client')

    def test_vectors_marker(self):
        self._assert_marker(oss_vectors.Client(_config()), 'vector-client')

    def test_vectors_marker_then_custom(self):
        self._assert_marker_then_custom(oss_vectors.Client(_config('mytool/1.0')), 'vector-client')


if __name__ == '__main__':
    unittest.main()
