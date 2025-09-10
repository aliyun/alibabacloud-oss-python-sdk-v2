# pylint: skip-file
from typing import cast
import tempfile
import datetime
import requests
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

class TestExtensionAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):

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


    async def test_is_bucket_exist(self):
        no_perm_client = self.invalid_async_client
        err_client = get_async_client("", "")

        bucket_name_no_exist = self.bucket_name + "-no-exist"

        exist = await self.async_client.is_bucket_exist(self.bucket_name)
        self.assertTrue(exist)

        exist = await self.async_client.is_bucket_exist(bucket_name_no_exist)
        self.assertFalse(exist)

        exist = await no_perm_client.is_bucket_exist(self.bucket_name)
        self.assertTrue(exist)

        exist = await no_perm_client.is_bucket_exist(bucket_name_no_exist)
        self.assertFalse(exist)

        try:
            exist = await err_client.is_bucket_exist(self.bucket_name)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('invalid field, endpoint', str(err))

    async def test_is_object_exist(self):
        bucket_name_no_exist = self.bucket_name + "-no-exist"
        object_name = 'object-exist'
        object_name_no_exist = "object-no-exist"
        no_perm_client = self.invalid_async_client
        err_client = get_async_client("", "")

        result = await self.async_client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=object_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        exist = await self.async_client.is_object_exist(self.bucket_name, object_name)
        self.assertTrue(exist)

        exist = await self.async_client.is_object_exist(self.bucket_name, object_name_no_exist)
        self.assertFalse(exist)

        try:
            exist = await self.async_client.is_object_exist(bucket_name_no_exist, object_name)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('NoSuchBucket', str(err))

        try:
            exist = await self.async_client.is_object_exist(bucket_name_no_exist, object_name_no_exist)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('NoSuchBucket', str(err))


        try:
            exist = await no_perm_client.is_object_exist(self.bucket_name, object_name)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('InvalidAccessKeyId', str(err))

        try:
            exist = await no_perm_client.is_object_exist(bucket_name_no_exist, object_name_no_exist)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('NoSuchBucket', str(err))

        try:
            exist = await err_client.is_object_exist(self.bucket_name, object_name)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('invalid field, endpoint', str(err))

