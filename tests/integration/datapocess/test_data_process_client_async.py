# pylint: skip-file

from typing import cast
import unittest
import alibabacloud_oss_v2 as oss
from .. import (
    TestIntegration,
    REGION,
    ENDPOINT,
    get_async_client,
)


class TestDataProcessAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.async_client = get_async_client(REGION, ENDPOINT)

    async def asyncTearDown(self):
        await self.async_client.close()

    async def test_do_meta_query_action(self):
        # null body
        try:
            await self.async_client.do_meta_query_action(oss.DoMetaQueryActionRequest(
                bucket=self.bucket_name,
                action='createDataset',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(405, serr.status_code)
            self.assertEqual('MethodNotAllowed', serr.code)
            self.assertIn('MetaQuery=&action=createDataset', serr.request_target)
            self.assertIn(self.bucket_name + '.', serr.request_target)

        # non-null body
        try:
            await self.async_client.do_meta_query_action(oss.DoMetaQueryActionRequest(
                bucket=self.bucket_name,
                action='createDataset',
                body=b'',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(405, serr.status_code)
            self.assertEqual('MethodNotAllowed', serr.code)
            self.assertIn('MetaQuery=&action=createDataset', serr.request_target)
            self.assertIn(self.bucket_name + '.', serr.request_target)

    async def test_do_meta_query_action_required_field(self):
        # bucket
        try:
            await self.async_client.do_meta_query_action(oss.DoMetaQueryActionRequest())
            self.fail("should not here")
        except oss.exceptions.ParamRequiredError as e:
            self.assertIn('missing required field, bucket', str(e))

        # action
        try:
            await self.async_client.do_meta_query_action(oss.DoMetaQueryActionRequest(
                bucket=self.bucket_name,
            ))
            self.fail("should not here")
        except oss.exceptions.ParamRequiredError as e:
            self.assertIn('missing required field, action', str(e))

    async def test_do_data_pipeline_action(self):
        # null body
        try:
            await self.async_client.do_data_pipeline_action(oss.DoDataPipelineActionRequest(
                action='putDataPipelineConfiguration',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertIn('dataPipeline=&action=putDataPipelineConfiguration', serr.request_target)
            self.assertNotIn(self.bucket_name, serr.request_target)

        # non-null body
        try:
            await self.async_client.do_data_pipeline_action(oss.DoDataPipelineActionRequest(
                action='putDataPipelineConfiguration',
                body=b'',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertIn('dataPipeline=&action=putDataPipelineConfiguration', serr.request_target)
            self.assertNotIn(self.bucket_name, serr.request_target)

    async def test_do_data_pipeline_action_required_field(self):
        # action
        try:
            await self.async_client.do_data_pipeline_action(oss.DoDataPipelineActionRequest())
            self.fail("should not here")
        except oss.exceptions.ParamRequiredError as e:
            self.assertIn('missing required field, action', str(e))
