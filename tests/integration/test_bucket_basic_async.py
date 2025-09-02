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

class TestBucketBasicAsync(TestIntegration, unittest.IsolatedAsyncioTestCase):

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

    async def test_put_bucket(self):

        bucket_name = random_bucket_name()
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    async def test_put_bucket_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.put_bucket(oss.PutBucketRequest(
                bucket=bucket_name,
                acl='private',
                create_bucket_configuration=oss.CreateBucketConfiguration(
                    storage_class='IA'
                )
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)


    async def test_bucket_acl(self):
        bucket_name = random_bucket_name()
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket acl
        result = await self.async_client.get_bucket_acl(oss.GetBucketAclRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket acl
        result = await self.async_client.put_bucket_acl(oss.PutBucketAclRequest(
            bucket=bucket_name,
            acl='public-read-write'
        ))
        self.assertEqual(200, result.status_code)

        # get bucket acl
        result = await self.async_client.get_bucket_acl(oss.GetBucketAclRequest(
            bucket=bucket_name,
        ))
        self.assertEqual('public-read-write', result.acl)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    async def test_put_bucket_acl_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.put_bucket_acl(oss.PutBucketAclRequest(
                bucket=bucket_name,
                acl='public-read-write'
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

    async def test_get_bucket_acl_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.get_bucket_acl(oss.GetBucketAclRequest(
            bucket=bucket_name,
        ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)


    async def test_list_objects_v2(self):
        bucket_name = random_bucket_name()
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        result = await self.async_client.list_objects_v2(oss.ListObjectsV2Request(
            bucket=bucket_name,
            delimiter='/',
            start_after='b',
            encoding_type='url',
            continuation_token='',
            max_keys=10,
            prefix='aaa',
            fetch_owner=True,
            request_payer='requester',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        self.assertEqual(bucket_name, result.name)
        self.assertEqual('/', result.delimiter)
        self.assertEqual('b', result.start_after)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual(10, result.max_keys)
        self.assertEqual('aaa', result.prefix)


    async def test_list_objects_v2_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.list_objects_v2(oss.ListObjectsV2Request(
                bucket=bucket_name,))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

        try:
            await self.invalid_async_client.list_objects_v2(oss.ListObjectsV2Request(
                bucket=bucket_name,
                delimiter='/',
                start_after='b',
                encoding_type='url',
                continuation_token='',
                max_keys=10,
                prefix='aaa',
                fetch_owner=True,
                request_payer='requester',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

    async def test_get_bucket_stat(self):
        bucket_name = random_bucket_name()
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket stat
        result = await self.async_client.get_bucket_stat(oss.models.GetBucketStatRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertTrue(result.storage==0)
        self.assertTrue(result.object_count==0)
        self.assertTrue(result.multi_part_upload_count==0)
        self.assertTrue(result.live_channel_count==0)
        self.assertTrue(result.last_modified_time==0)
        self.assertTrue(result.standard_storage==0)
        self.assertTrue(result.standard_object_count==0)
        self.assertTrue(result.infrequent_access_storage==0)
        self.assertTrue(result.infrequent_access_real_storage==0)
        self.assertTrue(result.infrequent_access_object_count==0)
        self.assertTrue(result.archive_storage==0)
        self.assertTrue(result.archive_real_storage==0)
        self.assertTrue(result.archive_object_count==0)
        self.assertTrue(result.cold_archive_storage==0)
        self.assertTrue(result.cold_archive_real_storage==0)
        self.assertTrue(result.cold_archive_object_count==0)
        self.assertTrue(result.deep_cold_archive_storage==0)
        self.assertTrue(result.deep_cold_archive_real_storage==0)
        self.assertTrue(result.deep_cold_archive_object_count==0)
        self.assertTrue(result.delete_marker_count==0)

    async def test_get_bucket_stat_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.get_bucket_stat(oss.models.GetBucketStatRequest(
            bucket=bucket_name,
        ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

    async def test_get_bucket_location(self):
        bucket_name = random_bucket_name()
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket location
        result = await self.async_client.get_bucket_location(oss.models.GetBucketLocationRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(f'oss-{REGION}', result.location)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    async def test_get_bucket_location_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.get_bucket_location(oss.models.GetBucketLocationRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

    async def test_get_bucket_info(self):
        bucket_name = random_bucket_name()
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket into
        result = await self.async_client.get_bucket_info(oss.models.GetBucketInfoRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        self.assertEqual('private', result.bucket_info.acl)
        self.assertEqual('Disabled', result.bucket_info.access_monitor)
        self.assertEqual(False, result.bucket_info.block_public_access)
        self.assertEqual('LRS', result.bucket_info.data_redundancy_type)
        self.assertEqual('Disabled', result.bucket_info.cross_region_replication)
        self.assertIsNotNone(result.bucket_info.resource_group_id)
        self.assertIsNotNone(result.bucket_info.creation_date)
        self.assertIsNotNone(result.bucket_info.extranet_endpoint)
        self.assertIsNotNone(result.bucket_info.intranet_endpoint)
        self.assertIsNotNone(result.bucket_info.location)
        self.assertIsNotNone(result.bucket_info.transfer_acceleration)
        self.assertEqual('IA', result.bucket_info.storage_class)
        self.assertIsNotNone(result.bucket_info.owner.id)
        self.assertIsNotNone(result.bucket_info.owner.display_name)
        self.assertIsNotNone(result.bucket_info.sse_rule.sse_algorithm)


    async def test_get_bucket_info_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.get_bucket_info(oss.models.GetBucketInfoRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)


    async def test_bucket_versions(self):
        bucket_name = random_bucket_name()
        result = await self.async_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket versioning
        result = await self.async_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket versioning
        result = await self.async_client.get_bucket_versioning(oss.GetBucketVersioningRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('Enabled', result.version_status)

        # list object versions
        result = await self.async_client.list_object_versions(oss.ListObjectVersionsRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.name)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual(100, result.max_keys)

        # list object versions case 2
        result = await self.async_client.list_object_versions(oss.ListObjectVersionsRequest(
            bucket=bucket_name,
            delimiter='/',
            key_marker='MARKER',
            max_keys=999,
            prefix='AA/a',
            encoding_type='url',
        ))
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.name)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual(999, result.max_keys)
        self.assertEqual('/', result.delimiter)
        self.assertEqual('MARKER', result.key_marker)
        self.assertEqual('AA/a', result.prefix)
        self.assertEqual('url', result.encoding_type)

    async def test_put_bucket_versioning_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

    async def test_get_bucket_versioning_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.get_bucket_versioning(oss.GetBucketVersioningRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)

    async def test_list_object_versions_fail(self):
        bucket_name = random_bucket_name()
        try:
            await self.invalid_async_client.list_object_versions(oss.ListObjectVersionsRequest(
            bucket=bucket_name,
        ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(404, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('NoSuchBucket', serr.code)
