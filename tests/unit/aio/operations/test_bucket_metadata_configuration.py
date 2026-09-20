# pylint: skip-file

import xml.etree.ElementTree as ET
from typing import cast

from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.aio.operations.bucket_metadata_configuration import (
    create_bucket_metadata_configuration,
    delete_bucket_metadata_configuration,
    get_bucket_metadata_configuration,
    update_bucket_metadata_inventory_table_configuration,
    update_bucket_metadata_journal_table_configuration,
)
from alibabacloud_oss_v2.models import bucket_metadata_configuration as model
from ... import MockAsyncHttpResponse
from . import TestOperations


class TestBucketMetadataConfigurationOperations(TestOperations):

    @classmethod
    def response_204_no_content(cls) -> MockAsyncHttpResponse:
        return MockAsyncHttpResponse(
            status_code=204,
            reason='No Content',
            headers={'x-oss-request-id': 'id-1234'},
            body=''
        )

    async def test_create_bucket_metadata_configuration(self):
        result = await create_bucket_metadata_configuration(
            self.client,
            model.CreateBucketMetadataConfigurationRequest(
                bucket='bucketexampletest',
                metadata_configuration=model.MetadataConfiguration(
                    journal_table_configuration=model.JournalTableConfiguration(
                        record_expiration=model.RecordExpiration(expiration='ENABLED', days=7),
                    ),
                ),
            ),
        )
        self.assertEqual('POST', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataConfiguration=', self.request_dump.url)

        root = ET.fromstring(self.request_dump.body)
        self.assertEqual('MetadataConfiguration', root.tag)
        self.assertEqual('ENABLED', root.findtext('JournalTableConfiguration/RecordExpiration/Expiration'))
        self.assertEqual('7', root.findtext('JournalTableConfiguration/RecordExpiration/Days'))

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual('id-1234', result.request_id)

    async def test_create_bucket_metadata_configuration_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        try:
            await create_bucket_metadata_configuration(
                self.client,
                model.CreateBucketMetadataConfigurationRequest(
                    bucket='bucketexampletest',
                    metadata_configuration=model.MetadataConfiguration(
                        journal_table_configuration=model.JournalTableConfiguration(
                            record_expiration=model.RecordExpiration(expiration='ENABLED', days=7),
                        ),
                    ),
                ),
            )
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('POST', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataConfiguration=', self.request_dump.url)

    async def test_get_bucket_metadata_configuration(self):
        result = await get_bucket_metadata_configuration(
            self.client,
            model.GetBucketMetadataConfigurationRequest(bucket='bucketexampletest'),
        )
        self.assertEqual('GET', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataConfiguration=', self.request_dump.url)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual('id-1234', result.request_id)

    async def test_get_bucket_metadata_configuration_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        try:
            await get_bucket_metadata_configuration(
                self.client,
                model.GetBucketMetadataConfigurationRequest(bucket='bucketexampletest'),
            )
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('GET', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataConfiguration=', self.request_dump.url)

    async def test_delete_bucket_metadata_configuration(self):
        # The DeleteBucketMetadataConfiguration operation responds 204 No Content.
        self.set_responseFunc(self.response_204_no_content)
        result = await delete_bucket_metadata_configuration(
            self.client,
            model.DeleteBucketMetadataConfigurationRequest(bucket='bucketexampletest'),
        )
        self.assertEqual('DELETE', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataConfiguration=', self.request_dump.url)

        self.assertEqual(204, result.status_code)
        self.assertEqual('No Content', result.status)
        self.assertEqual('id-1234', result.request_id)

    async def test_delete_bucket_metadata_configuration_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        try:
            await delete_bucket_metadata_configuration(
                self.client,
                model.DeleteBucketMetadataConfigurationRequest(bucket='bucketexampletest'),
            )
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('DELETE', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataConfiguration=', self.request_dump.url)

    async def test_update_bucket_metadata_inventory_table_configuration(self):
        result = await update_bucket_metadata_inventory_table_configuration(
            self.client,
            model.UpdateBucketMetadataInventoryTableConfigurationRequest(
                bucket='bucketexampletest',
                inventory_table_configuration=model.InventoryTableConfiguration(
                    configuration_state='ENABLED',
                ),
            ),
        )
        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataInventoryTable=', self.request_dump.url)

        root = ET.fromstring(self.request_dump.body)
        self.assertEqual('InventoryTableConfiguration', root.tag)
        self.assertEqual('ENABLED', root.findtext('ConfigurationState'))

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual('id-1234', result.request_id)

    async def test_update_bucket_metadata_inventory_table_configuration_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        try:
            await update_bucket_metadata_inventory_table_configuration(
                self.client,
                model.UpdateBucketMetadataInventoryTableConfigurationRequest(
                    bucket='bucketexampletest',
                    inventory_table_configuration=model.InventoryTableConfiguration(
                        configuration_state='ENABLED',
                    ),
                ),
            )
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataInventoryTable=', self.request_dump.url)

    async def test_update_bucket_metadata_journal_table_configuration(self):
        result = await update_bucket_metadata_journal_table_configuration(
            self.client,
            model.UpdateBucketMetadataJournalTableConfigurationRequest(
                bucket='bucketexampletest',
                journal_table_configuration=model.JournalTableConfiguration(
                    record_expiration=model.RecordExpiration(expiration='DISABLED'),
                ),
            ),
        )
        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataJournalTable=', self.request_dump.url)

        root = ET.fromstring(self.request_dump.body)
        self.assertEqual('JournalTableConfiguration', root.tag)
        self.assertEqual('DISABLED', root.findtext('RecordExpiration/Expiration'))

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual('id-1234', result.request_id)

    async def test_update_bucket_metadata_journal_table_configuration_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        try:
            await update_bucket_metadata_journal_table_configuration(
                self.client,
                model.UpdateBucketMetadataJournalTableConfigurationRequest(
                    bucket='bucketexampletest',
                    journal_table_configuration=model.JournalTableConfiguration(
                        record_expiration=model.RecordExpiration(expiration='DISABLED'),
                    ),
                ),
            )
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual('https://bucketexampletest.oss-cn-hangzhou.aliyuncs.com/?metadataJournalTable=', self.request_dump.url)
