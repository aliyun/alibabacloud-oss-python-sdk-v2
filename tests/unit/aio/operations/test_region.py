# pylint: skip-file
from typing import cast
from alibabacloud_oss_v2.models import region as model
from alibabacloud_oss_v2.aio.operations import region as operations
from . import TestOperations

class TestRegion(TestOperations):
    async def test_describe_regions(self):
        request = model.DescribeRegionsRequest()
        result = await operations.describe_regions(self.client, request)
        self.assertEqual('https://oss-cn-hangzhou.aliyuncs.com/?regions=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)