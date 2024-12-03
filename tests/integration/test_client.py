# pylint: skip-file
from typing import cast
import os
import tempfile
import datetime
import requests
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name, random_str, REGION, OBJECTNAME_PREFIX, get_client


class TestBucketBasic(TestIntegration):

    def test_put_bucket(self):
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
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

    def test_put_bucket_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.put_bucket(oss.PutBucketRequest(
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


    def test_bucket_acl(self):
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
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
        result = self.client.get_bucket_acl(oss.GetBucketAclRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket acl
        result = self.client.put_bucket_acl(oss.PutBucketAclRequest(
            bucket=bucket_name,
            acl='public-read-write'
        ))
        self.assertEqual(200, result.status_code)

        # get bucket acl
        result = self.client.get_bucket_acl(oss.GetBucketAclRequest(
            bucket=bucket_name,
        ))
        self.assertEqual('public-read-write', result.acl)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_put_bucket_acl_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.put_bucket_acl(oss.PutBucketAclRequest(
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

    def test_get_bucket_acl_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.get_bucket_acl(oss.GetBucketAclRequest(
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


    def test_list_objects_v2(self):
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
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

        result = self.client.list_objects_v2(oss.ListObjectsV2Request(
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


    def test_list_objects_v2_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.list_objects_v2(oss.ListObjectsV2Request(
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
            self.invalid_client.list_objects_v2(oss.ListObjectsV2Request(
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

    def test_get_bucket_stat(self):
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
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
        result = self.client.get_bucket_stat(oss.models.GetBucketStatRequest(
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

    def test_get_bucket_stat_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.get_bucket_stat(oss.models.GetBucketStatRequest(
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

    def test_get_bucket_location(self):
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
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
        result = self.client.get_bucket_location(oss.models.GetBucketLocationRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(f'oss-{REGION}', result.location)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_get_bucket_location_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.get_bucket_location(oss.models.GetBucketLocationRequest(
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

    def test_get_bucket_info(self):
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
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
        result = self.client.get_bucket_info(oss.models.GetBucketInfoRequest(
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


    def test_get_bucket_info_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.get_bucket_info(oss.models.GetBucketInfoRequest(
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


    def test_bucket_versions(self):
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
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
        result = self.client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket versioning
        result = self.client.get_bucket_versioning(oss.GetBucketVersioningRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('Enabled', result.version_status)

        # list object versions
        result = self.client.list_object_versions(oss.ListObjectVersionsRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(bucket_name, result.name)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual(100, result.max_keys)

        # list object versions case 2
        result = self.client.list_object_versions(oss.ListObjectVersionsRequest(
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

    def test_put_bucket_versioning_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.put_bucket_versioning(oss.PutBucketVersioningRequest(
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

    def test_get_bucket_versioning_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.get_bucket_versioning(oss.GetBucketVersioningRequest(
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

    def test_list_object_versions_fail(self):
        bucket_name = random_bucket_name()
        try:
            self.invalid_client.list_object_versions(oss.ListObjectVersionsRequest(
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


class TestRegion(TestIntegration):
    def test_describe_regions(self):
        result = self.client.describe_regions(oss.DescribeRegionsRequest(
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertTrue(result.region_info.__len__()>1)


        result = self.client.describe_regions(oss.DescribeRegionsRequest(
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

    def test_describe_regions_fail(self):
        try:
            self.invalid_client.describe_regions(oss.DescribeRegionsRequest())
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        try:
            self.invalid_client.describe_regions(oss.DescribeRegionsRequest(
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


class TestObjectBasic(TestIntegration):
    def test_object_basic(self):
        len = 1 * 1024 * 1024 + 1234
        #len = 1234
        data = random_str(len)
        key = 'test-key'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)

        result = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)

        rdata = b''.join(result.body.iter_bytes()) or b''
        self.assertEqual(data.encode(), rdata)
        result.body.close()

        result = self.client.get_object_meta(oss.GetObjectMetaRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectMetaResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)

    def test_put_object_fail(self):
        try:
            self.invalid_client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                body=b'hello world',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('PutObject', str(e))
            self.assertIn('Endpoint: PUT', str(e))

    def test_get_object_fail(self):
        try:
            self.invalid_client.get_object(oss.GetObjectRequest(
                bucket=self.bucket_name,
                key='invalid-key',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('GetObject', str(e))
            self.assertIn('Endpoint: GET', str(e))

    def test_head_object_fail(self):
        try:
            self.invalid_client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key='invalid-key',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('HeadObject', str(e))
            self.assertIn('Endpoint: HEAD', str(e))

    def test_get_object_meta_fail(self):
        try:
            self.invalid_client.get_object_meta(oss.GetObjectMetaRequest(
                bucket=self.bucket_name,
                key='invalid-key',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('GetObjectMeta', str(e))
            self.assertIn('Endpoint: HEAD', str(e))

    def test_get_object_range(self):
        len = 12345
        step = 2512
        data = random_str(len)
        key = 'test-key-range'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        rdata = b''
        for r in range(0, len, step):
            gresult = self.client.get_object(oss.GetObjectRequest(
                bucket=self.bucket_name,
                key=key,
                range_header=f'bytes={r}-{r+step-1}',
                range_behavior='standard'
            ))
            self.assertIsNotNone(gresult)
            self.assertEqual(206, gresult.status_code)
            self.assertLessEqual(gresult.content_length, step)
            got = b''.join(gresult.body.iter_bytes()) or b''
            rdata += got

        self.assertEqual(data.encode(), rdata)
        gresult.body.close()

    def test_append_object(self):
        data1 = b'hello'
        data2 = b' world'

        key = 'append_object'
        result = self.client.append_object(oss.AppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=0,
            body=data1,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(5, result.next_position)

        result = self.client.append_object(oss.AppendObjectRequest(
            bucket=self.bucket_name,
            key=key,
            position=result.next_position,
            body=data2,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(11, result.next_position)

        gresult = self.client.get_object(oss.GetObjectRequest(
                bucket=self.bucket_name,
                key=key,
        ))

        got = b''.join(gresult.body.iter_bytes()) or b''
        self.assertEqual(b'hello world', got)

    def test_append_object_fail(self):
        try:
            self.invalid_client.append_object(oss.AppendObjectRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                position=0,
                body=b'hello world',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

    def test_delete_object(self):
        length = 1234
        data = random_str(length)
        key = f'test-key-delete-object-{random_str(16)}'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(length, result.content_length)

        result = self.client.delete_object(oss.DeleteObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(204, result.status_code)
        self.assertIsInstance(result, oss.DeleteObjectResult)

        try:
            result = self.client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
        except Exception as err:
            self.assertIsNotNone(result)
            self.assertIn('NoSuchKey', str(err))


        key = f'test-key-delete-object-no-exist-{random_str(16)}'
        result = self.client.delete_object(oss.DeleteObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(204, result.status_code)
        self.assertIsNone(result.version_id)
        self.assertIsNone(result.delete_marker)
        self.assertIsInstance(result, oss.DeleteObjectResult)


    def test_delete_object_fail(self):
        try:
            self.invalid_client.delete_object(oss.DeleteObjectRequest(
                bucket=self.bucket_name,
                key='invalid-key',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)


    def test_delete_multiple_objects(self):
        length = 1234
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
            bucket=self.bucket_name,
            objects=[oss.DeleteObject(key=key)],
        ))
        self.assertIsInstance(result, oss.DeleteMultipleObjectsResult)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.headers.get('x-oss-request-id'))
        self.assertEqual(1, len(result.deleted_objects))
        self.assertEqual(key, result.deleted_objects[0].key)

        str1  = b'\x01\x02\x03\x04\x05\x06\a\b\t\n\v\f\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        key = OBJECTNAME_PREFIX + random_str(16) + str1.decode()
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(length, result.content_length)

        result = self.client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
            bucket=self.bucket_name,
            encoding_type='url',
            objects=[oss.DeleteObject(key=key)],
        ))
        self.assertIsInstance(result, oss.DeleteMultipleObjectsResult)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.headers.get('x-oss-request-id'))
        self.assertEqual(1, len(result.deleted_objects))
        self.assertEqual(key, result.deleted_objects[0].key)

        try:
            result = self.client.head_object(oss.HeadObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
        except Exception as err:
            self.assertIsInstance(err, oss.exceptions.OperationError)
            err = cast(oss.exceptions.OperationError, err)
            serr = err.unwrap()
            self.assertIsInstance(serr, oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, serr)
            self.assertIn('NoSuchKey', serr.code)

    def test_restore_object(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            storage_class=oss.StorageClassType.ARCHIVE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.restore_object(oss.RestoreObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.RestoreObjectResult)
        self.assertEqual(202, result.status_code)

        try:
            result = self.client.restore_object(oss.RestoreObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ))
            self.fail("should not here")
        except Exception as err:
            self.assertIsInstance(err, oss.exceptions.OperationError)
            err = cast(oss.exceptions.OperationError, err)
            serr = err.unwrap()
            self.assertIsInstance(serr, oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, serr)
            self.assertIn('RestoreAlreadyInProgress', serr.code)
            self.assertIn('The restore operation is in progress.', serr.message)

    def test_object_acl(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PRIVATE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('private', result.acl)

        result = self.client.put_object_acl(oss.PutObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PUBLICREAD
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectAclResult)
        self.assertEqual(200, result.status_code)

        result = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.GetObjectAclResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual('public-read', result.acl)

    def test_get_object_acl_fail(self):
        try:
            self.invalid_client.get_object_acl(oss.GetObjectAclRequest(
                bucket=self.bucket_name,
                key='invalid-key',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('GetObjectAcl', str(e))
            self.assertIn('Endpoint: GET', str(e))

    def test_put_object_acl_fail(self):
        try:
            self.invalid_client.put_object_acl(oss.PutObjectAclRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                acl='private',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertIn('PutObjectAcl', str(e))
            self.assertIn('Endpoint: PUT', str(e))

class TestMultipartUpload(TestIntegration):
    def test_multipart_upload_object(self):
        length1 = 100*1024
        data1 = random_str(length1)
        length2 = 1234
        data2 = random_str(length2)
        key = OBJECTNAME_PREFIX + random_str(16)

        result = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(self.bucket_name, result.bucket)
        self.assertEqual(key, result.key)
        self.assertIsNotNone(key, result.upload_id)

        presult1 = self.client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=1,
            upload_id=result.upload_id,
            body=data1,
        ))
        self.assertIsNotNone(presult1)
        self.assertIsInstance(presult1, oss.UploadPartResult)
        self.assertEqual(200, presult1.status_code)
        self.assertIsNotNone(presult1.content_md5)
        self.assertIsNotNone(presult1.etag)
        self.assertIsNotNone(presult1.hash_crc64)

        presult2 = self.client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=2,
            upload_id=result.upload_id,
            body=data2,
        ))
        self.assertIsNotNone(presult2)
        self.assertIsInstance(presult2, oss.UploadPartResult)
        self.assertEqual(200, presult2.status_code)
        self.assertIsNotNone(presult2.content_md5)
        self.assertIsNotNone(presult2.etag)
        self.assertIsNotNone(presult2.hash_crc64)

        lpresult = self.client.list_parts(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
        ))
        self.assertIsNotNone(lpresult)
        self.assertIsInstance(lpresult, oss.ListPartsResult)
        self.assertEqual(200, lpresult.status_code)
        self.assertEqual(self.bucket_name, lpresult.bucket)
        self.assertEqual(key, lpresult.key)
        self.assertEqual(2, lpresult.next_part_number_marker)
        self.assertEqual(0, lpresult.part_number_marker)
        self.assertEqual(False, lpresult.is_truncated)
        self.assertEqual(1000, lpresult.max_parts)
        self.assertEqual('Standard', lpresult.storage_class)
        self.assertEqual(2, len(lpresult.parts))
        self.assertEqual(1, lpresult.parts[0].part_number)
        self.assertEqual(length1, lpresult.parts[0].size)
        self.assertEqual(presult1.etag, lpresult.parts[0].etag)
        self.assertEqual(presult1.hash_crc64, lpresult.parts[0].hash_crc64)
        self.assertEqual(2, lpresult.parts[1].part_number)
        self.assertEqual(length2, lpresult.parts[1].size)
        self.assertEqual(presult2.etag, lpresult.parts[1].etag)
        self.assertEqual(presult2.hash_crc64, lpresult.parts[1].hash_crc64)

        cresult = self.client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
            body=data2,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=[
                    oss.UploadPart(part_number=1, etag=presult1.etag),
                    oss.UploadPart(part_number=2, etag=presult2.etag),                    
                ]
            )
        ))
        self.assertIsNotNone(cresult)
        self.assertIsInstance(cresult, oss.CompleteMultipartUploadResult)
        self.assertEqual(200, cresult.status_code)
        self.assertEqual(self.bucket_name, cresult.bucket)
        self.assertEqual(key, cresult.key)
        self.assertIsNotNone(cresult.etag)
        self.assertIsNotNone(cresult.hash_crc64)

        gresult = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(gresult)
        self.assertEqual(200, gresult.status_code)
        self.assertEqual(length1 + length2, gresult.content_length)
        rdata = b''.join(gresult.body.iter_bytes()) or b''
        self.assertEqual(data1 + data2, rdata.decode())

    def test_multipart_upload_object_special_key(self):
        length1 = 100*1024
        data1 = random_str(length1)
        length2 = 1234
        data2 = random_str(length2)        
        str1  = b'\x01\x02\x03\x04\x05\x06\a\b\t\n\v\f\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        key = OBJECTNAME_PREFIX + random_str(16) + str1.decode()

        result = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(self.bucket_name, result.bucket)
        self.assertEqual(key, result.key)
        self.assertIsNotNone(key, result.upload_id)

        presult1 = self.client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=1,
            upload_id=result.upload_id,
            body=data1,
        ))
        self.assertIsNotNone(presult1)
        self.assertIsInstance(presult1, oss.UploadPartResult)
        self.assertEqual(200, presult1.status_code)
        self.assertIsNotNone(presult1.content_md5)
        self.assertIsNotNone(presult1.etag)
        self.assertIsNotNone(presult1.hash_crc64)

        presult2 = self.client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=2,
            upload_id=result.upload_id,
            body=data2,
        ))
        self.assertIsNotNone(presult2)
        self.assertIsInstance(presult2, oss.UploadPartResult)
        self.assertEqual(200, presult2.status_code)
        self.assertIsNotNone(presult2.content_md5)
        self.assertIsNotNone(presult2.etag)
        self.assertIsNotNone(presult2.hash_crc64)

        cresult = self.client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
            body=data2,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=[
                    oss.UploadPart(part_number=1, etag=presult1.etag),
                    oss.UploadPart(part_number=2, etag=presult2.etag),                    
                ]
            )
        ))
        self.assertIsNotNone(cresult)
        self.assertIsInstance(cresult, oss.CompleteMultipartUploadResult)
        self.assertEqual(200, cresult.status_code)
        self.assertEqual(self.bucket_name, cresult.bucket)
        self.assertEqual(key, cresult.key)
        self.assertIsNotNone(cresult.etag)
        self.assertIsNotNone(cresult.hash_crc64)

        gresult = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(gresult)
        self.assertEqual(200, gresult.status_code)
        self.assertEqual(length1 + length2, gresult.content_length)
        rdata = b''.join(gresult.body.iter_bytes()) or b''
        self.assertEqual(data1 + data2, rdata.decode())


    def test_multipart_upload_object_encoding_type(self):
        str1  = b'\x01\x02\x03\x04\x05\x06\a\b\t\n\v\f\r\x0e\x0f\x10'
        key = OBJECTNAME_PREFIX + random_str(16) + str1.decode()

        result = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(self.bucket_name, result.bucket)
        self.assertEqual(key, result.key)
        self.assertIsNotNone(key, result.upload_id)

        presult1 = self.client.upload_part(oss.UploadPartRequest(
            bucket=self.bucket_name,
            key=key,
            part_number=1,
            upload_id=result.upload_id,
            body='hello world',
        ))
        self.assertIsNotNone(presult1)
        self.assertIsInstance(presult1, oss.UploadPartResult)
        self.assertEqual(200, presult1.status_code)
        self.assertIsNotNone(presult1.content_md5)
        self.assertIsNotNone(presult1.etag)
        self.assertIsNotNone(presult1.hash_crc64)

        lpresult = self.client.list_parts(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
        ))
        self.assertIsNotNone(lpresult)
        self.assertIsInstance(lpresult, oss.ListPartsResult)
        self.assertEqual(200, lpresult.status_code)
        self.assertEqual(self.bucket_name, lpresult.bucket)
        self.assertEqual(key, lpresult.key)

        luresult = self.client.list_multipart_uploads(oss.ListMultipartUploadsRequest(
            bucket=self.bucket_name,
        ))
        self.assertIsNotNone(luresult)
        self.assertIsInstance(luresult, oss.ListMultipartUploadsResult)
        self.assertEqual(200, luresult.status_code)
        self.assertEqual(self.bucket_name, luresult.bucket)
        self.assertEqual(False, luresult.is_truncated)
        self.assertEqual(None, luresult.key_marker)
        self.assertEqual(key, luresult.next_key_marker)
        self.assertEqual(1, len(luresult.uploads))
        self.assertEqual(key, luresult.uploads[0].key)
        self.assertEqual(result.upload_id, luresult.uploads[0].upload_id)

        abresult = self.client.abort_multipart_upload(oss.AbortMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=result.upload_id,
        ))
        self.assertIsNotNone(abresult)
        self.assertIsInstance(abresult, oss.AbortMultipartUploadResult)
        self.assertEqual(204, abresult.status_code)

    def test_multipart_upload_from_file(self):
        part_size = 100 * 1024
        data_size = 3 * part_size + 1245
        data = random_str(data_size).encode()
        key = 'multipart-file.bin'

        #init
        initresult = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(initresult)
        self.assertIsInstance(initresult, oss.InitiateMultipartUploadResult)
        self.assertEqual(200, initresult.status_code)

        #upload part
        part_number = 1
        upload_parts = []
        with tempfile.TemporaryFile('w+b') as f:
            f.write(data)
            for start in range(0, data_size, part_size):
                n = part_size
                if start + n > data_size:
                    n =  data_size - start
                reader = oss.io_utils.SectionReader(oss.io_utils.ReadAtReader(f), start, n)
                upresult = self.client.upload_part(oss.UploadPartRequest(
                    bucket=self.bucket_name,
                    key=key,
                    upload_id=initresult.upload_id,
                    part_number=part_number,
                    body=reader
                ))
                self.assertIsNotNone(upresult)
                self.assertIsInstance(upresult, oss.UploadPartResult)
                self.assertEqual(200, upresult.status_code)
                upload_parts.append(oss.UploadPart(part_number=part_number, etag=upresult.etag))
                part_number += 1

            self.assertEqual(4, len(upload_parts))

        #listpart
        lpresult = self.client.list_parts(oss.ListPartsRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=initresult.upload_id
        ))
        self.assertIsNotNone(lpresult)
        self.assertIsInstance(lpresult, oss.ListPartsResult)
        self.assertEqual(200, lpresult.status_code)

        #complete
        parts = sorted(upload_parts, key=lambda p: p.part_number)
        cmresult = self.client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            upload_id=initresult.upload_id,
            complete_multipart_upload=oss.CompleteMultipartUpload(
                parts=parts
            )
        ))
        self.assertIsNotNone(cmresult)
        self.assertIsInstance(cmresult, oss.CompleteMultipartUploadResult)
        self.assertEqual(200, cmresult.status_code)

        # get object and check
        gowresult = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertIsNotNone(gowresult)
        self.assertIsInstance(gowresult, oss.GetObjectResult)
        self.assertEqual(200, gowresult.status_code)
        self.assertEqual(data_size, len(gowresult.body.content))
        self.assertEqual(data, gowresult.body.content)

    def test_initiate_multipart_upload_fail(self):
        try:
            self.invalid_client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
                bucket=self.bucket_name,
                key='invalid-key',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('InitiateMultipartUpload', str(e))
            self.assertIn('Endpoint: POST', str(e))

    def test_upload_part_fail(self):
        try:
            self.invalid_client.upload_part(oss.UploadPartRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                upload_id='upload-id',
                part_number=1,
                body='hello world'
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('UploadPart', str(e))
            self.assertIn('Endpoint: PUT', str(e))

    def test_upload_part_copy_fail(self):
        try:
            self.invalid_client.upload_part_copy(oss.UploadPartCopyRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                source_key='source-invalid-key',
                upload_id='upload-id',
                part_number=1,
                body='hello world'
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('UploadPartCopy', str(e))
            self.assertIn('Endpoint: PUT', str(e))

    def test_complete_multipart_upload_fail(self):
        try:
            self.invalid_client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                upload_id='upload-id',
                complete_all='yes'
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('CompleteMultipartUpload', str(e))
            self.assertIn('Endpoint: POST', str(e))

    def test_abort_multipart_upload_fail(self):
        try:
            self.invalid_client.abort_multipart_upload(oss.AbortMultipartUploadRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                upload_id='upload-id',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('AbortMultipartUpload', str(e))
            self.assertIn('Endpoint: DELETE', str(e))

    def test_list_multipart_uploads_fail(self):
        try:
            self.invalid_client.list_multipart_uploads(oss.ListMultipartUploadsRequest(
                bucket=self.bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('ListMultipartUploads', str(e))
            self.assertIn('Endpoint: GET', str(e))

    def test_list_parts_fail(self):
        try:
            self.invalid_client.list_parts(oss.ListPartsRequest(
                bucket=self.bucket_name,
                key='invalid-key',
                upload_id='upload-id',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
            self.assertIn('ListParts', str(e))
            self.assertIn('Endpoint: GET', str(e))


class TestPresign(TestIntegration):
    def test_presign_get_object(self):
        len = 1234
        data = random_str(len)
        key = 'presign-get-test-key'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        preresult = self.client.presign(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        with requests.get(preresult.url) as resp:
            self.assertEqual(data.encode(), resp.content)
            self.assertEqual(200, resp.status_code)

    def test_presign_put_object(self):
        len = 1234
        data = random_str(len)
        key = 'presign-put-test-key'
        preresult = self.client.presign(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            content_type='text/txt'
        ))

        with requests.put(preresult.url, headers=preresult.signed_headers, data=data) as resp:
            self.assertEqual(200, resp.status_code)

        result = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        result.body.read()
        self.assertEqual(200, result.status_code)
        self.assertEqual(data.encode(), result.body.content)
        self.assertEqual('text/txt', result.headers.get('content-type'))

    def test_presign_without_signed_headers(self):
        len = 1234
        data = random_str(len)
        key = 'presign-put-test-key-fail'
        preresult = self.client.presign(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            content_type='text/txt'
        ))

        with requests.put(preresult.url, data=data) as resp:
            self.assertEqual(403, resp.status_code)

    def test_presign_fail(self):
	    # unsupport request
        request = oss.ListObjectsV2Request(
            bucket='bucket'
        )

        try:
            self.client.presign(request)
            self.fail("should not here")
        except Exception as err:
            self.assertIsInstance(err, oss.exceptions.ParamInvalidError)

        # greater than 7 days
        request = oss.GetObjectRequest(
            bucket='bucket',
            key='key+123',
            version_id='versionId'
        )
        try:
            timedelta = datetime.timedelta(days=8)
            datetime_now = datetime.datetime.now(datetime.timezone.utc)
            expiration = datetime_now + timedelta
            self.client.presign(request, expiration=expiration)
            self.fail("should not here")
        except Exception as err:
            self.assertIsInstance(err, oss.exceptions.PresignExpirationError)

    def test_presign_head_object(self):
        len = 1234
        data = random_str(len)
        key = 'presign-head-test-key'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        preresult = self.client.presign(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        with requests.head(preresult.url) as resp:
            self.assertEqual(200, resp.status_code)
            self.assertEqual('1234', resp.headers.get('content-length'))

    def test_presign_initiate_multipart_upload(self):

        key = 'presign-initiate-multipart-upload-test-key'
        preresult = self.client.presign(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        with requests.post(preresult.url) as resp:
            self.assertEqual(200, resp.status_code)
            obj = oss.InitiateMultipartUploadResult()
            oss.serde.deserialize_xml(xml_data=resp.content, obj=obj)
            self.assertEqual(self.bucket_name, obj.bucket)
            self.assertEqual(key, obj.key)
            self.assertIsNotNone(obj.upload_id)

    def test_presign_upload_part(self):
        len = 1234
        data = random_str(len)
        key = 'presign-upload-part-test-key'
        init_pre_result = self.client.presign(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        with requests.post(init_pre_result.url) as resp:
            self.assertEqual(200, resp.status_code)
            obj = oss.InitiateMultipartUploadResult()
            oss.serde.deserialize_xml(xml_data=resp.content, obj=obj)
            self.assertEqual(self.bucket_name, obj.bucket)
            self.assertEqual(key, obj.key)
            self.assertIsNotNone(obj.upload_id)

            for i in range(1, 4):
                up_pre_result = self.client.presign(oss.UploadPartRequest(
                    bucket=self.bucket_name,
                    key=key,
                    upload_id=obj.upload_id,
                    part_number=i,
                    content_type='text/txt'
                ))

                with requests.put(up_pre_result.url, headers=up_pre_result.signed_headers, data=data) as resp:
                    self.assertEqual(200, resp.status_code)



    def test_presign_complete_multipart_upload(self):
        len = 200 * 1024
        data = random_str(len)
        key = 'presign-complete-multipart-upload-test-key'
        init_pre_result = self.client.presign(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            content_type='text/txt'
        ))

        with requests.post(init_pre_result.url, headers=init_pre_result.signed_headers) as resp:
            self.assertEqual(200, resp.status_code)
            obj = oss.InitiateMultipartUploadResult()
            oss.serde.deserialize_xml(xml_data=resp.content, obj=obj)
            self.assertEqual(self.bucket_name, obj.bucket)
            self.assertEqual(key, obj.key)
            self.assertIsNotNone(obj.upload_id)

            for i in range(1, 4):
                up_pre_result = self.client.presign(oss.UploadPartRequest(
                    bucket=self.bucket_name,
                    key=key,
                    upload_id=obj.upload_id,
                    part_number=i,
                ))

                with requests.put(up_pre_result.url, headers=up_pre_result.signed_headers, data=data) as resp:
                    self.assertEqual(200, resp.status_code)

            complete_pre_result = self.client.presign(oss.CompleteMultipartUploadRequest(
                bucket=self.bucket_name,
                key=key,
                upload_id=obj.upload_id,
                complete_all='yes'
            ))

            with requests.post(complete_pre_result.url, headers=complete_pre_result.signed_headers) as resp:
                self.assertEqual(200, resp.status_code)
                obj = oss.CompleteMultipartUploadResult()
                oss.serde.deserialize_xml(xml_data=resp.content, obj=obj)
                self.assertEqual(self.bucket_name, obj.bucket)
                self.assertEqual(key, obj.key)

        result = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        result.body.read()
        self.assertEqual(200, result.status_code)
        self.assertEqual(3 * 200 * 1024, result.content_length)
        self.assertEqual('text/txt', result.headers.get('content-type'))

    def test_presign_abort_multipart_upload(self):
        len = 200 * 1024
        data = random_str(len)
        key = 'presign-abort-multipart-upload-test-key'

        init_pre_result = self.client.presign(oss.InitiateMultipartUploadRequest(
            bucket=self.bucket_name,
            key=key,
            content_type='text/txt'
        ))

        with requests.post(init_pre_result.url, headers=init_pre_result.signed_headers) as resp:
            self.assertEqual(200, resp.status_code)
            obj = oss.InitiateMultipartUploadResult()
            oss.serde.deserialize_xml(xml_data=resp.content, obj=obj)
            self.assertEqual(self.bucket_name, obj.bucket)
            self.assertEqual(key, obj.key)
            self.assertIsNotNone(obj.upload_id)

            for i in range(1, 4):
                up_pre_result = self.client.presign(oss.UploadPartRequest(
                    bucket=self.bucket_name,
                    key=key,
                    upload_id=obj.upload_id,
                    part_number=i,
                ))

                with requests.put(up_pre_result.url, headers=up_pre_result.signed_headers, data=data) as resp:
                    self.assertEqual(200, resp.status_code)


            list_result = self.client.list_parts(oss.ListPartsRequest(
                bucket=self.bucket_name,
                key=key,
                upload_id=obj.upload_id,
            ))
            self.assertIsNotNone(list_result)
            self.assertEqual(200, list_result.status_code)
            self.assertEqual(self.bucket_name, list_result.bucket)
            self.assertEqual(key, list_result.key)
            self.assertEqual(3, list_result.parts.__len__())


            abort_result = self.client.presign(oss.AbortMultipartUploadRequest(
                bucket=self.bucket_name,
                key=key,
                upload_id=obj.upload_id,
            ))

            with requests.delete(abort_result.url, headers=abort_result.signed_headers) as resp:
                self.assertEqual(204, resp.status_code)

            try:
                self.client.list_parts(oss.ListPartsRequest(
                    bucket=self.bucket_name,
                    key=key,
                    upload_id=obj.upload_id,
                ))
            except Exception as e:
                ope = cast(oss.exceptions.OperationError, e)
                self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
                serr = cast(oss.exceptions.ServiceError, ope.unwrap())
                self.assertEqual(404, serr.status_code)
                self.assertEqual('NoSuchUpload', serr.code)


class TestPaginator(TestIntegration):
    def test_list_objects_paginator(self):
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name))

        for i in range(9):
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=bucket_name,
                key=f'key-{i}'
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        paginator = self.client.list_objects_paginator(limit=1)
        request = oss.ListObjectsRequest(bucket=bucket_name)
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1, len(p.contents))
            self.assertEqual(f'key-{j}', p.contents[0].key)
            self.assertEqual(0, p.contents[0].size)
            j += 1
        self.assertIsNone(request.marker)

        iterator = paginator.iter_page(request, limit=3)
        j = 0
        for p in iterator:
            self.assertEqual(3, p.max_keys)
            self.assertEqual(3, len(p.contents))
            self.assertEqual(f'key-{j*3}', p.contents[0].key)
            self.assertEqual(0, p.contents[0].size)
            j += 1
        self.assertIsNone(request.marker)

        paginator = self.client.list_objects_paginator()
        request = oss.ListObjectsRequest(bucket=bucket_name, prefix='key-1')
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(100, p.max_keys)
            self.assertEqual(1, len(p.contents))
            self.assertEqual(f'key-1', p.contents[0].key)
            j += 1
        self.assertEqual(1, j)

        #encoding
        for i in range(3):
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=bucket_name,
                key=f'url-%123-/?#:key-{i}'
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        request = oss.ListObjectsRequest(bucket=bucket_name, prefix='url-')
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(100, p.max_keys)
            self.assertEqual(3, len(p.contents))
            self.assertEqual(f'url-%123-/?#:key-0', p.contents[0].key)
            self.assertEqual(f'url-%123-/?#:key-1', p.contents[1].key)
            self.assertEqual(f'url-%123-/?#:key-2', p.contents[2].key)
            j += 1
        self.assertEqual(1, j)

    def test_list_v2_objects_paginator(self):
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name))

        for i in range(9):
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=bucket_name,
                key=f'key-{i}'
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        paginator = self.client.list_objects_v2_paginator(limit=1)
        request = oss.ListObjectsV2Request(bucket=bucket_name)
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1, len(p.contents))
            self.assertEqual(f'key-{j}', p.contents[0].key)
            self.assertEqual(0, p.contents[0].size)
            j += 1
        self.assertIsNone(request.continuation_token)

        iterator = paginator.iter_page(request, limit=3)
        j = 0
        for p in iterator:
            self.assertEqual(3, p.max_keys)
            self.assertEqual(3, len(p.contents))
            self.assertEqual(f'key-{j*3}', p.contents[0].key)
            self.assertEqual(0, p.contents[0].size)
            j += 1
        self.assertIsNone(request.continuation_token)

        paginator = self.client.list_objects_v2_paginator()
        request = oss.ListObjectsV2Request(bucket=bucket_name, prefix='key-1')
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(100, p.max_keys)
            self.assertEqual(1, len(p.contents))
            self.assertEqual(f'key-1', p.contents[0].key)
            j += 1
        self.assertEqual(1, j)

        #encoding
        for i in range(3):
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=bucket_name,
                key=f'url-%123-/?#:key-{i}'
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        request = oss.ListObjectsV2Request(bucket=bucket_name, prefix='url-')
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(100, p.max_keys)
            self.assertEqual(3, len(p.contents))
            self.assertEqual(f'url-%123-/?#:key-0', p.contents[0].key)
            self.assertEqual(f'url-%123-/?#:key-1', p.contents[1].key)
            self.assertEqual(f'url-%123-/?#:key-2', p.contents[2].key)
            j += 1
        self.assertEqual(1, j)

    def test_list_object_versions_paginator(self):
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name))

        for i in range(9):
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=bucket_name,
                key=f'key-{i}'
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        paginator = self.client.list_object_versions_paginator(limit=1)
        request = oss.ListObjectVersionsRequest(bucket=bucket_name)
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1, len(p.version))
            self.assertEqual(f'key-{j}', p.version[0].key)
            self.assertEqual(0, p.version[0].size)
            j += 1
        self.assertIsNone(request.key_marker)
        self.assertIsNone(request.version_id_marker)

        iterator = paginator.iter_page(request, limit=3)
        j = 0
        for p in iterator:
            self.assertEqual(3, p.max_keys)
            self.assertEqual(3, len(p.version))
            self.assertEqual(f'key-{j*3}', p.version[0].key)
            self.assertEqual(0, p.version[0].size)
            j += 1
        self.assertIsNone(request.key_marker)
        self.assertIsNone(request.version_id_marker)

        paginator = self.client.list_object_versions_paginator()
        request = oss.ListObjectVersionsRequest(bucket=bucket_name, prefix='key-1')
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(100, p.max_keys)
            self.assertEqual(1, len(p.version))
            self.assertEqual(f'key-1', p.version[0].key)
            j += 1
        self.assertEqual(1, j)

        # encoding
        for i in range(3):
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=bucket_name,
                key=f'url-%123-/?#:key-{i}'
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        request = oss.ListObjectVersionsRequest(bucket=bucket_name, prefix='url-')
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(100, p.max_keys)
            self.assertEqual(3, len(p.version))
            self.assertEqual(f'url-%123-/?#:key-0', p.version[0].key)
            self.assertEqual(f'url-%123-/?#:key-1', p.version[1].key)
            self.assertEqual(f'url-%123-/?#:key-2', p.version[2].key)
            j += 1
        self.assertEqual(1, j)

        result = self.client.put_bucket_versioning(oss.PutBucketVersioningRequest(
            bucket=bucket_name,
            versioning_configuration=oss.VersioningConfiguration(
                status='Enabled'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # version_id
        for i in range(3):
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=bucket_name,
                key=f'version_id-%123-/?#:key-{i}'
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        request = oss.ListObjectVersionsRequest(bucket=bucket_name, prefix='version_id-')
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(100, p.max_keys)
            self.assertEqual(3, len(p.version))
            self.assertEqual(f'version_id-%123-/?#:key-0', p.version[0].key)
            self.assertEqual(f'version_id-%123-/?#:key-1', p.version[1].key)
            self.assertEqual(f'version_id-%123-/?#:key-2', p.version[2].key)
            self.assertIsNotNone(p.version[j].version_id)
            j += 1
        self.assertEqual(1, j)

        # delete all version files
        request = oss.ListObjectVersionsRequest(bucket=bucket_name)
        iterator = paginator.iter_page(request, limit=1)
        delete_object = []
        for p in iterator:
            delete_object.append(oss.DeleteObject(key=p.version[0].key, version_id=p.version[0].version_id))

        result = self.client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
            bucket=bucket_name,
            objects=delete_object))
        self.assertEqual(200, result.status_code)


    def test_list_buckets_paginator(self):
        bucket_name_prefix = random_bucket_name()
        bucket_name1 = bucket_name_prefix + '-1'
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name1))
        bucket_name2 = bucket_name_prefix + '-2'
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name2))
        bucket_name3 = bucket_name_prefix + '-3'
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name3))

        paginator = self.client.list_buckets_paginator(limit=1)
        request = oss.ListBucketsRequest(
            prefix=bucket_name_prefix
        )
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1, len(p.buckets))
            j += 1
        self.assertIsNone(request.marker)

        iterator = paginator.iter_page(request, limit=3)
        for p in iterator:
            if p.is_truncated:
                self.assertEqual(3, p.max_keys)
            self.assertEqual(3, len(p.buckets))

        self.assertIsNone(request.marker)

        paginator = self.client.list_buckets_paginator()
        request = oss.ListBucketsRequest(prefix=bucket_name_prefix)
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(3, len(p.buckets))
            j += 1
        self.assertEqual(1, j)


    def test_list_parts_paginator(self):
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name))

        key = OBJECTNAME_PREFIX + random_str(16)

        init_result = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=bucket_name,
            key=key,
        ))

        for i in range(1,4):
            result = self.client.upload_part(oss.UploadPartRequest(
                bucket=bucket_name,
                key=key,
                part_number=i,
                upload_id=init_result.upload_id,
                body="data-test",
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        paginator = self.client.list_parts_paginator(limit=1)
        request = oss.ListPartsRequest(
            bucket=bucket_name,
            key=key,
            upload_id=init_result.upload_id)
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1, len(p.parts))
            self.assertEqual(j+1, p.parts[0].part_number)
            self.assertEqual(9, p.parts[0].size)
            j += 1
        self.assertIsNone(request.part_number_marker)

        iterator = paginator.iter_page(request, limit=3)
        j = 0
        for p in iterator:
            self.assertEqual(3, p.max_parts)
            self.assertEqual(3, len(p.parts))
            self.assertEqual(1, p.parts[0].part_number)
            self.assertEqual(9, p.parts[0].size)
            j += 1
        self.assertIsNone(request.part_number_marker)

        #encoding
        encoding_key = 'url-%123-/?#:key-'
        init_result2 = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
            bucket=bucket_name,
            key=encoding_key,
        ))

        for i in range(1,4):
            result = self.client.upload_part(oss.UploadPartRequest(
                bucket=bucket_name,
                key=encoding_key,
                part_number=i,
                upload_id=init_result2.upload_id,
                body=f'data{i}',
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        request = oss.ListPartsRequest(
            bucket=bucket_name,
            key=encoding_key,
            upload_id=init_result2.upload_id)
        paginator = self.client.list_parts_paginator()
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1000, p.max_parts)
            self.assertEqual(3, len(p.parts))
            self.assertEqual(j+1, p.parts[0].part_number)
            self.assertEqual(5, p.parts[0].size)
            j += 1
        self.assertEqual(1, j)

    def test_list_multipart_uploads_paginator(self):
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name))

        for i in range(3):
            result = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
                bucket=bucket_name,
                key=f'key-{i}',
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        paginator = self.client.list_multipart_uploads_paginator(limit=1)
        request = oss.ListMultipartUploadsRequest(bucket=bucket_name)
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1, len(p.uploads))
            self.assertEqual(f'key-{j}', p.uploads[0].key)
            j += 1
        self.assertIsNone(request.key_marker)
        self.assertIsNone(request.upload_id_marker)

        iterator = paginator.iter_page(request, limit=3)
        j = 0
        for p in iterator:
            self.assertEqual(3, p.max_uploads)
            self.assertEqual(3, len(p.uploads))
            self.assertEqual(f'key-{j*3}', p.uploads[0].key)
            j += 1
        self.assertIsNone(request.key_marker)
        self.assertIsNone(request.upload_id_marker)

        paginator = self.client.list_multipart_uploads_paginator()
        request = oss.ListMultipartUploadsRequest(bucket=bucket_name, prefix='key-1')
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1000, p.max_uploads)
            self.assertEqual(1, len(p.uploads))
            self.assertEqual(f'key-1', p.uploads[0].key)
            j += 1
        self.assertEqual(1, j)

        #encoding
        for i in range(3):
            result = self.client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
                bucket=bucket_name,
                key=f'upload-%123-/?#:key-{i}'
            ))
            self.assertIsNotNone(result)
            self.assertEqual(200, result.status_code)

        request = oss.ListMultipartUploadsRequest(bucket=bucket_name, prefix='upload-%123-')
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1000, p.max_uploads)
            self.assertEqual(3, len(p.uploads))
            self.assertEqual(f'upload-%123-/?#:key-0', p.uploads[0].key)
            self.assertEqual(f'upload-%123-/?#:key-1', p.uploads[1].key)
            self.assertEqual(f'upload-%123-/?#:key-2', p.uploads[2].key)
            j += 1
        self.assertEqual(1, j)


class TestExtension(TestIntegration):
    def test_is_bucket_exist(self):
        no_perm_client = self.invalid_client
        err_client = get_client("", "")

        bucket_name_no_exist = self.bucket_name + "-no-exist"

        exist = self.client.is_bucket_exist(self.bucket_name)
        self.assertTrue(exist)

        exist = self.client.is_bucket_exist(bucket_name_no_exist)
        self.assertFalse(exist)

        exist = no_perm_client.is_bucket_exist(self.bucket_name)
        self.assertTrue(exist)

        exist = no_perm_client.is_bucket_exist(bucket_name_no_exist)
        self.assertFalse(exist)

        try:
            exist = err_client.is_bucket_exist(self.bucket_name)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('invalid field, endpoint', str(err))

    def test_is_object_exist(self):
        bucket_name_no_exist = self.bucket_name + "-no-exist"
        object_name = 'object-exist'
        object_name_no_exist = "object-no-exist"
        no_perm_client = self.invalid_client
        err_client = get_client("", "")

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=object_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        exist = self.client.is_object_exist(self.bucket_name, object_name)
        self.assertTrue(exist)

        exist = self.client.is_object_exist(self.bucket_name, object_name_no_exist)
        self.assertFalse(exist)

        try:
            exist = self.client.is_object_exist(bucket_name_no_exist, object_name)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('NoSuchBucket', str(err))

        try:
            exist = self.client.is_object_exist(bucket_name_no_exist, object_name_no_exist)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('NoSuchBucket', str(err))


        try:
            exist = no_perm_client.is_object_exist(self.bucket_name, object_name)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('InvalidAccessKeyId', str(err))

        try:
            exist = no_perm_client.is_object_exist(bucket_name_no_exist, object_name_no_exist)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('NoSuchBucket', str(err))

        try:
            exist = err_client.is_object_exist(self.bucket_name, object_name)
            self.fail("shoud not here")
        except oss.exceptions.OperationError as err:
            self.assertIn('invalid field, endpoint', str(err))

    def test_put_object_from_file(self):
        example_data = b''
        with open("./tests/data/example.jpg", 'rb') as f:
            example_data = f.read()

        key = 'object_from_file.jpg'
        result = self.client.put_object_from_file(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key
        ), "./tests/data/example.jpg")
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        gresult = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertEqual(200, gresult.status_code)
        self.assertEqual('OK', gresult.status)
        self.assertEqual(example_data, gresult.body.content)

    def test_put_object_from_file_fail(self):
        key = 'object_from_file.jpg'
        try:
            self.client.put_object_from_file(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key
            ), "./tests/data/invalid-example.jpg")
            self.fail("shoud not here")
        except FileNotFoundError as err:
            self.assertIn("No such file or directory", str(err))

    def test_get_object_to_file(self):
        key = 'get_object_to_file.jpg'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body='hello world'
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        filename = tempfile.gettempprefix()

        gresult = self.client.get_object_to_file(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ), filename)
        self.assertEqual(200, gresult.status_code)
        self.assertEqual('OK', gresult.status)

        os.remove(filename)

    def test_get_object_to_file_fail(self):
        key = 'get_object_to_file_fail.jpg'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body='hello world'
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        filename = tempfile.gettempprefix()

        try:
            self.invalid_client.get_object_to_file(oss.GetObjectRequest(
                bucket=self.bucket_name,
                key=key,
            ), filename)
            self.fail("shoud not here")
        except Exception as err:
            self.assertIn("InvalidAccessKeyId", str(err))

        os.remove(filename)
