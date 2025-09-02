# pylint: skip-file
from typing import cast
import unittest
import alibabacloud_oss_v2 as oss
from . import (
    TestIntegration, 
    random_bucket_name, 
    random_str, 
    REGION,
    ENDPOINT, 
    OBJECTNAME_PREFIX, 
    get_async_client,
)

class TestRegionAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.async_client = get_async_client(REGION, ENDPOINT)
        self.invalid_async_client = get_async_client(
            REGION, 
            ENDPOINT,
            oss.credentials.StaticCredentialsProvider('invalid-ak', 'invalid')
        )

    async def asyncTearDown(self):
        await self.async_client.close() 
        await self.invalid_async_client.close() 

    async def test_describe_regions(self):
        result = await self.async_client.describe_regions(oss.DescribeRegionsRequest(
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertTrue(result.region_info.__len__()>1)


        result = await self.async_client.describe_regions(oss.DescribeRegionsRequest(
            regions='oss-cn-hangzhou',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertTrue(result.region_info.__len__()==1)
        self.assertEqual('oss-accelerate.aliyuncs.com', result.region_info[0].accelerate_endpoint)
        self.assertEqual('oss-cn-hangzhou-internal.aliyuncs.com', result.region_info[0].internal_endpoint)
        self.assertEqual('oss-cn-hangzhou.aliyuncs.com', result.region_info[0].internet_endpoint)
        self.assertEqual('oss-cn-hangzhou', result.region_info[0].region)

    async def test_describe_regions_fail(self):
        try:
            await self.invalid_async_client.describe_regions(oss.DescribeRegionsRequest())
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        try:
            await self.invalid_async_client.describe_regions(oss.DescribeRegionsRequest(
                regions='oss-cn-hangzhou',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
