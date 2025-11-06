# pylint: skip-file
from typing import cast
import os
import io
import tempfile
import datetime
import requests
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.crc as osscrc
from . import (
    TestIntegration, 
    random_bucket_name, 
    random_str, 
    REGION,
    OBJECTNAME_PREFIX,
    ENDPOINT,
    ACCESS_ID,
    ACCESS_KEY,
    get_client
)
from urllib.parse import quote, unquote

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


    def test_put_object_with_defferent_body_type(self):
        len = 300 * 1024 + 1234
        data = random_str(len)

        crc64 = osscrc.Crc64(0)
        crc64.update(data.encode())
        ccrc = str(crc64.sum64())

        # str
        key = 'test-key-defferent_body-str'
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
        self.assertEqual(ccrc, result.hash_crc64)

        # bytes
        key = 'test-key-defferent_body-bytes'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data.encode(),
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
        self.assertEqual(ccrc, result.hash_crc64)

        # IO[str]
        key = 'test-key-defferent_body-io-str'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=io.StringIO(data),
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
        self.assertEqual(ccrc, result.hash_crc64)

        # IO[bytes]
        key = 'test-key-defferent_body-io-bytes'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=io.BytesIO(data.encode()),
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
        self.assertEqual(ccrc, result.hash_crc64)

    def test_put_object_with_defferent_body_type_disable_crc(self):
        len = 350 * 1024 + 1234
        data = random_str(len)

        crc64 = osscrc.Crc64(0)
        crc64.update(data.encode())
        ccrc = str(crc64.sum64())

        cfg = oss.config.load_default()
        cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
        cfg.region = REGION
        cfg.endpoint = ENDPOINT
        cfg.disable_upload_crc64_check = True
        client = oss.Client(cfg)

        # str
        key = 'test-key-defferent_body-no-crc-str'
        result = client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)
        self.assertEqual(ccrc, result.hash_crc64)

        # bytes
        key = 'test-key-defferent_body-no-crc-bytes'
        result = client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data.encode(),
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)
        self.assertEqual(ccrc, result.hash_crc64)

        # IO[str]
        key = 'test-key-defferent_body-io-no-crc-str'
        result = client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=io.StringIO(data),
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)
        self.assertEqual(ccrc, result.hash_crc64)

        # IO[bytes]
        key = 'test-key-defferent_body-io-no-crc-bytes'
        result = client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=io.BytesIO(data.encode()),
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.PutObjectResult)
        self.assertEqual(200, result.status_code)

        result = client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.HeadObjectResult)
        self.assertEqual(200, result.status_code)
        self.assertEqual(len, result.content_length)
        self.assertEqual(ccrc, result.hash_crc64)


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

    def test_restore_object_tier(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            storage_class=oss.StorageClassType.COLDARCHIVE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.restore_object(oss.RestoreObjectRequest(
            bucket=self.bucket_name,
            key=key,
            restore_request=oss.RestoreRequest(
                days=1,
                tier='Expedited',
            ),
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.RestoreObjectResult)
        self.assertEqual(202, result.status_code)
        self.assertEqual('Expedited', result.restore_priority)

        try:
            result = self.client.restore_object(oss.RestoreObjectRequest(
                bucket=self.bucket_name,
                key=key,
                restore_request=oss.RestoreRequest(
                    days=1,
                    tier='Expedited',
                ),
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

    def test_restore_object_job_parameters(self):
        length = 123
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            storage_class=oss.StorageClassType.COLDARCHIVE,
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result = self.client.restore_object(oss.RestoreObjectRequest(
            bucket=self.bucket_name,
            key=key,
            restore_request=oss.RestoreRequest(
                days=7,
                job_parameters=oss.JobParameters(
                    tier="Bulk"
                )
            ),
        ))
        self.assertIsNotNone(result)
        self.assertIsInstance(result, oss.RestoreObjectResult)
        self.assertEqual(202, result.status_code)
        self.assertEqual('Bulk', result.restore_priority)

        try:
            result = self.client.restore_object(oss.RestoreObjectRequest(
                bucket=self.bucket_name,
                key=key,
                restore_request=oss.RestoreRequest(
                    days=7,
                    job_parameters=oss.JobParameters(
                        tier="Bulk"
                    )
                ),
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

    def test_list_buckets_with_tag_filter(self):
        # Create buckets with different tags
        bucket_name_prefix = random_bucket_name()
        bucket_name1 = bucket_name_prefix + '-tag1'
        bucket_name2 = bucket_name_prefix + '-tag2'
        bucket_name3 = bucket_name_prefix + '-tag3'
        
        # Create buckets
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name1))
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name2))
        self.client.put_bucket(oss.PutBucketRequest(bucket=bucket_name3))
        
        # Add tags to buckets
        self.client.put_bucket_tags(oss.PutBucketTagsRequest(
            bucket=bucket_name1,
            tagging=oss.Tagging(
                tag_set=oss.TagSet(
                    tags=[oss.Tag(
                        key='env',
                        value='test',
                    )],
                ),
            ),
        ))
        
        self.client.put_bucket_tags(oss.PutBucketTagsRequest(
            bucket=bucket_name2,
            tagging=oss.Tagging(
                tag_set=oss.TagSet(
                    tags=[oss.Tag(
                        key='env',
                        value='test',
                    ), oss.Tag(
                        key='team',
                        value='dev',
                    )],
                ),
            ),
        ))
        
        self.client.put_bucket_tags(oss.PutBucketTagsRequest(
            bucket=bucket_name3,
            tagging=oss.Tagging(
                tag_set=oss.TagSet(
                    tags=[oss.Tag(
                        key='env',
                        value='prod',
                    )],
                ),
            ),
        ))
        
        # Test tag-key filter
        request = oss.ListBucketsRequest(
            prefix=bucket_name_prefix,
            tag_key='env'
        )
        result = self.client.list_buckets(request)
        # Should return all 3 buckets since they all have 'env' tag
        self.assertEqual(3, len(result.buckets))
        
        # Test tag-value filter
        request = oss.ListBucketsRequest(
            prefix=bucket_name_prefix,
            tag_key='env',
            tag_value='test'
        )
        result = self.client.list_buckets(request)
        # Should return 2 buckets (bucket_name1 and bucket_name2) which have 'env=test'
        self.assertEqual(2, len(result.buckets))
        
        # Test tagging filter
        request = oss.ListBucketsRequest(
            prefix=bucket_name_prefix,
            tagging='"env":"test","team":"dev"'
        )
        result = self.client.list_buckets(request)
        # Should return 1 bucket (bucket_name2) which has both tags
        self.assertEqual(1, len(result.buckets))

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

class TestCopier(TestIntegration):
    def test_same_bucket(self):
        length = 100 * 1024 + 123
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)

        # put object data
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            body=src_data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hreasult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hreasult.hash_crc64
        src_etag = hreasult.etag
        self.assertIsNotNone(src_crc64)

        copier = self.client.copier()

        # case 1: Copy a single part from the same bucket
        dst_key = 'single_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
            source_bucket=self.bucket_name,
            source_key=src_key
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

        # case 2: Copy a single part from the same bucket, not set source_bucket
        dst_key = 'single_key-1'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
            source_key=src_key
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

        # case 3: use shallow copy
        dst_key = 'shallow_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
            source_bucket=self.bucket_name,
            source_key=src_key
        ), multipart_copy_threshold=100*1024)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

        # case 4: use shallow copy, not set source_bucket
        dst_key = 'shallow_key-1'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
            source_key=src_key
        ), multipart_copy_threshold=100*1024)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)
        
        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

        # case 5: Copy a multipart from the same bucket
        dst_key = 'multipart_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
            source_bucket=self.bucket_name,
            source_key=src_key
        ), multipart_copy_threshold=100*1024, disable_shallow_copy=True)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertNotEqual(src_etag, result.etag)
        self.assertIsNotNone(result.upload_id)
        self.assertIsNone(result.version_id)
   
        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

        # case 6: Copy a multipart from the same bucket, not set source_bucket
        dst_key = 'multipart_key-1'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
            source_key=src_key
        ), multipart_copy_threshold=100*1024, disable_shallow_copy=True)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertNotEqual(src_etag, result.etag)
        self.assertIsNotNone(result.upload_id)
        self.assertIsNone(result.version_id)
   
        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

    def test_cross_bucket(self):
        length = 100 * 1024 + 123
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)
        
        # put bucket
        dst_bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=dst_bucket_name,
            acl='private',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put object data
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            body=src_data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hreasult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hreasult.hash_crc64
        src_etag = hreasult.etag
        self.assertIsNotNone(src_crc64)

        copier = self.client.copier()

        # case 1: Copy a single part
        dst_key = 'single_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=self.bucket_name,
            source_key=src_key
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

        # case 2: no-use shallow copy
        dst_key = 'multipart_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=self.bucket_name,
            source_key=src_key
        ), multipart_copy_threshold=100*1024)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertNotEqual(src_etag, result.etag)
        self.assertIsNotNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

    def test_metadata_tagging_directive_none(self):
        length = 200 * 1024 + 1234
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)
        src_bucket_name = self.bucket_name

        # put object data
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            metadata={
                "auth": "owner",
                "version": "1.01",
            },
            content_type="text/plain",
            content_disposition="attachment;filename=aaa.txt",
            content_encoding="deflate",
            cache_control="no-cache",
            expires="Wed, 08 Jul 2022 16:57:01 GMT",
            tagging='TagA=A&TagB=B',
            body=src_data,
            headers={
                "Content-Language": "zh"
            }
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hreasult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hreasult.hash_crc64
        src_etag = hreasult.etag
        self.assertIsNotNone(src_crc64)

        dst_bucket_name = self.bucket_name
        self.assertEqual(src_bucket_name, dst_bucket_name)
    
        copier = self.client.copier()

        # case 1: Copy a single part
        dst_key = 'single_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertEqual("1.01", hresult.metadata.get('version'))
        self.assertEqual("owner", hresult.metadata.get('auth'))
        self.assertEqual("text/plain", hresult.content_type)
        self.assertEqual("attachment;filename=aaa.txt", hresult.content_disposition)
        self.assertEqual("deflate", hresult.content_encoding)
        self.assertEqual("no-cache", hresult.cache_control)
        self.assertEqual("Wed, 08 Jul 2022 16:57:01 GMT", hresult.expires)
        self.assertEqual(2, hresult.tagging_count)
        self.assertEqual("zh", hresult.headers["Content-Language"])

        # case 2: shallow copy
        dst_key = 'shallow_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key
        ), multipart_copy_threshold=100*1024)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertEqual("1.01", hresult.metadata.get('version'))
        self.assertEqual("owner", hresult.metadata.get('auth'))
        self.assertEqual("text/plain", hresult.content_type)
        self.assertEqual("attachment;filename=aaa.txt", hresult.content_disposition)
        self.assertEqual("deflate", hresult.content_encoding)
        self.assertEqual("no-cache", hresult.cache_control)
        self.assertEqual("Wed, 08 Jul 2022 16:57:01 GMT", hresult.expires)
        self.assertEqual(2, hresult.tagging_count)
        self.assertEqual("zh", hresult.headers["Content-Language"])

        # case 3: multipart copy
        dst_key = 'multipart_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key
        ), multipart_copy_threshold=100*1024, disable_shallow_copy=True)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertNotEqual(src_etag, result.etag)
        self.assertIsNotNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertEqual("1.01", hresult.metadata.get('version'))
        self.assertEqual("owner", hresult.metadata.get('auth'))
        self.assertEqual("text/plain", hresult.content_type)
        self.assertEqual("attachment;filename=aaa.txt", hresult.content_disposition)
        self.assertEqual("deflate", hresult.content_encoding)
        self.assertEqual("no-cache", hresult.cache_control)
        self.assertEqual("Wed, 08 Jul 2022 16:57:01 GMT", hresult.expires)
        self.assertEqual(2, hresult.tagging_count)
        self.assertEqual("zh", hresult.headers["Content-Language"])

        # compare tags
        tresult = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        tags = []
        tags_str = ''
        for o in tresult.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA=A&TagB=B", tags_str)

    def test_metadata_tagging_directive_copy(self):
        length = 200 * 1024 + 1234
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)
        src_bucket_name = self.bucket_name

        # put object data
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            metadata={
                "auth": "owner",
                "version": "1.01",
            },
            content_type="text/plain",
            content_disposition="attachment;filename=aaa.txt",
            content_encoding="deflate",
            cache_control="no-cache",
            expires="Wed, 08 Jul 2022 16:57:01 GMT",
            tagging='TagA=A&TagB=B',
            body=src_data,
            headers={
                "Content-Language": "en-US"
            }
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hreasult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hreasult.hash_crc64
        src_etag = hreasult.etag
        self.assertIsNotNone(src_crc64)

        dst_bucket_name = self.bucket_name
        self.assertEqual(src_bucket_name, dst_bucket_name)
    
        copier = self.client.copier()

        # case 1: Copy a single part
        dst_key = 'single_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key,
            metadata_directive="COPY",
            tagging_directive="COPY"
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertEqual("1.01", hresult.metadata.get('version'))
        self.assertEqual("owner", hresult.metadata.get('auth'))
        self.assertEqual("text/plain", hresult.content_type)
        self.assertEqual("attachment;filename=aaa.txt", hresult.content_disposition)
        self.assertEqual("deflate", hresult.content_encoding)
        self.assertEqual("no-cache", hresult.cache_control)
        self.assertEqual("Wed, 08 Jul 2022 16:57:01 GMT", hresult.expires)
        self.assertEqual(2, hresult.tagging_count)
        self.assertEqual("en-US", hresult.headers["Content-Language"])

        # case 2: shallow copy
        dst_key = 'shallow_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key,
            metadata_directive="COPY",
            tagging_directive="COPY"
        ), multipart_copy_threshold=100*1024)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertEqual("1.01", hresult.metadata.get('version'))
        self.assertEqual("owner", hresult.metadata.get('auth'))
        self.assertEqual("text/plain", hresult.content_type)
        self.assertEqual("attachment;filename=aaa.txt", hresult.content_disposition)
        self.assertEqual("deflate", hresult.content_encoding)
        self.assertEqual("no-cache", hresult.cache_control)
        self.assertEqual("Wed, 08 Jul 2022 16:57:01 GMT", hresult.expires)
        self.assertEqual(2, hresult.tagging_count)
        self.assertEqual("en-US", hresult.headers["Content-Language"])

        # case 3: multipart copy
        dst_key = 'multipart_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key,
            metadata_directive="COPY",
            tagging_directive="COPY"
        ), multipart_copy_threshold=100*1024, disable_shallow_copy=True)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertNotEqual(src_etag, result.etag)
        self.assertIsNotNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertEqual("1.01", hresult.metadata.get('version'))
        self.assertEqual("owner", hresult.metadata.get('auth'))
        self.assertEqual("text/plain", hresult.content_type)
        self.assertEqual("attachment;filename=aaa.txt", hresult.content_disposition)
        self.assertEqual("deflate", hresult.content_encoding)
        self.assertEqual("no-cache", hresult.cache_control)
        self.assertEqual("Wed, 08 Jul 2022 16:57:01 GMT", hresult.expires)
        self.assertEqual(2, hresult.tagging_count)
        self.assertEqual("en-US", hresult.headers["Content-Language"])

        # compare tags
        tresult = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        tags = []
        tags_str = ''
        for o in tresult.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA=A&TagB=B", tags_str)

    def test_metadata_tagging_directive_replace(self):
        length = 200 * 1024 + 1234
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)
        src_bucket_name = self.bucket_name

        # put object data
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            metadata={
                "auth": "owner",
                "version": "1.01",
            },
            content_type="text/plain",
            content_disposition="attachment;filename=aaa.txt",
            content_encoding="deflate",
            cache_control="no-cache",
            expires="Wed, 08 Jul 2022 16:57:01 GMT",
            tagging='TagA=A&TagB=B',
            body=src_data,
            headers={
                "Content-Language": "en-US"
            }
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hreasult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hreasult.hash_crc64
        src_etag = hreasult.etag
        self.assertIsNotNone(src_crc64)

        dst_bucket_name = self.bucket_name
        self.assertEqual(src_bucket_name, dst_bucket_name)
    
        copier = self.client.copier()

        # case 1: Copy a single part
        dst_key = 'single_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key,
            metadata_directive="REPLACE",
            tagging_directive="REPLACE"
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertIsNone(hresult.metadata)
        # content-type no change
        self.assertEqual("text/plain", hresult.content_type)
        self.assertIsNone(hresult.content_disposition)
        self.assertIsNone(hresult.content_encoding)
        self.assertIsNone(hresult.cache_control)
        self.assertIsNone(hresult.expires)
        self.assertIsNone(hresult.tagging_count)
        self.assertIsNone(hresult.headers.get("Content-Language"), None)

        # case 2: shallow copy
        dst_key = 'shallow_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key,
            metadata_directive="REPLACE",
            tagging_directive="REPLACE"
        ), multipart_copy_threshold=100*1024)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertIsNone(hresult.metadata)
        # content-type no change
        self.assertEqual("text/plain", hresult.content_type)
        self.assertIsNone(hresult.content_disposition)
        self.assertIsNone(hresult.content_encoding)
        self.assertIsNone(hresult.cache_control)
        self.assertIsNone(hresult.expires)
        self.assertIsNone(hresult.tagging_count)
        self.assertIsNone(hresult.headers.get("Content-Language"), None)

        # case 3: multipart copy
        dst_key = 'multipart_key.jpg'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key,
            metadata_directive="REPLACE",
            tagging_directive="REPLACE"
        ), multipart_copy_threshold=100*1024, disable_shallow_copy=True)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertNotEqual(src_etag, result.etag)
        self.assertIsNotNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertIsNone(hresult.metadata)
        self.assertEqual("application/octet-stream", hresult.content_type)
        self.assertIsNone(hresult.content_disposition)
        self.assertIsNone(hresult.content_encoding)
        self.assertIsNone(hresult.cache_control)
        self.assertIsNone(hresult.expires)
        self.assertIsNone(hresult.tagging_count)
        self.assertIsNone(hresult.headers.get("Content-Language"), None)

    def test_header(self):
        length = 12
        data = random_str(length)
        length_2 = 1000 * 1024
        data_2 = random_str(length_2)
        key = OBJECTNAME_PREFIX + random_str(16)
        key_2 = OBJECTNAME_PREFIX + random_str(16)
        bucket_name = random_bucket_name()

        # put bucket
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put object data
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            headers={
                'Content-Type': 'text/plain',
                'Cache-Control': 'no-cache',
                'content-language': 'zh-CN',
                'content-encoding': 'gzip',
                'Content-Disposition': 'attachment;filename='+quote('世界')+'.txt',
                'Expires': '2022-10-12T00:00:00.000Z',
                'auth': 'owner',
                'x-oss-auth': 'owner2',
                'x-oss-meta-auth': 'owner3',
            },
            tagging='TagA=A&TagB=B',
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        # put object data2
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key_2,
            headers={
                'Content-Type': 'text/plain',
                'Cache-Control': 'no-cache',
                'content-language': 'zh-CN',
                'content-encoding': 'gzip',
                'Content-Disposition': 'attachment;filename='+quote('世界')+'.txt',
                'Expires': '2022-10-12T00:00:00.000Z',
                'auth': 'owner',
                'x-oss-auth': 'owner2',
                'x-oss-meta-auth': 'owner3',
            },
            tagging='TagA=A&TagB=B',
            body=data_2,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        # case 1: Copy a single part from the same bucket
        single_key = 'single_key'
        result = self.client.copier().copy(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=single_key,
            source_bucket=self.bucket_name,
            source_key=key
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)


        result_single_same_bucket_1 = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        result_single_same_bucket_2 = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=single_key,
        ))
        self.assertEqual("Normal", result_single_same_bucket_2.object_type)
        self.assertEqual(12, result_single_same_bucket_1.content_length)
        self.assertEqual(12, result_single_same_bucket_2.content_length)
        self.assertEqual('text/plain', result_single_same_bucket_1.headers.get('Content-Type'))
        self.assertEqual('no-cache', result_single_same_bucket_1.headers.get('Cache-Control'))
        self.assertEqual('zh-CN', result_single_same_bucket_1.headers.get('Content-Language'))
        self.assertEqual('gzip', result_single_same_bucket_1.headers.get('Content-Encoding'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_single_same_bucket_1.headers.get('Content-Disposition'))
        self.assertEqual('2022-10-12T00:00:00.000Z', result_single_same_bucket_1.headers.get('Expires'))
        self.assertEqual('owner3', result_single_same_bucket_1.headers.get('x-oss-meta-auth'))
        self.assertEqual('owner3', result_single_same_bucket_1.metadata.get('auth'))
        self.assertEqual('text/plain', result_single_same_bucket_2.headers.get('Content-Type'))
        self.assertEqual('no-cache', result_single_same_bucket_2.headers.get('Cache-Control'))
        self.assertEqual('zh-CN', result_single_same_bucket_2.headers.get('Content-Language'))
        self.assertEqual('gzip', result_single_same_bucket_2.headers.get('Content-Encoding'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_single_same_bucket_2.headers.get('Content-Disposition'))
        self.assertEqual('2022-10-12T00:00:00.000Z', result_single_same_bucket_2.headers.get('Expires'))
        self.assertEqual('owner3', result_single_same_bucket_2.headers.get('x-oss-meta-auth'))
        self.assertEqual('owner3', result_single_same_bucket_2.metadata.get('auth'))
        self.assertEqual(None, result_single_same_bucket_1.metadata.get('x-oss-auth'))
        self.assertEqual(None, result_single_same_bucket_1.metadata.get('x-oss-meta-auth'))
        self.assertEqual(None, result_single_same_bucket_2.metadata.get('x-oss-auth'))
        self.assertEqual(None, result_single_same_bucket_2.metadata.get('x-oss-meta-auth'))

        result_tag_single_same_bucket_1 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        result_tag_single_same_bucket_2 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=self.bucket_name,
            key=single_key,
        ))
        self.assertEqual(result_tag_single_same_bucket_1.tag_set.tags, result_tag_single_same_bucket_2.tag_set.tags)

        # compare tags
        tags = []
        tags_str = ''
        for o in result_tag_single_same_bucket_2.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA=A&TagB=B", tags_str)

        # case 2: Copy a multipart from the same bucket
        multi_key = 'multipart_key'
        result = self.client.copier(
            part_size=100*1024,
            parallel_num=5,
            leave_parts_on_error=True,
            disable_shallow_copy=True,
            multipart_copy_threshold=100*1024
        ).copy(oss.CopyObjectRequest(
            bucket=self.bucket_name,
            key=multi_key,
            source_bucket=self.bucket_name,
            source_key=key_2
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result_multi_same_bucket_1 = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key_2,
        ))

        result_multi_same_bucket_2 = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=multi_key,
        ))
        self.assertEqual("Multipart", result_multi_same_bucket_2.object_type)
        self.assertEqual(1000 * 1024, result_multi_same_bucket_1.content_length)
        self.assertEqual(1000 * 1024, result_multi_same_bucket_2.content_length)
        self.assertEqual("Multipart", result_multi_same_bucket_2.object_type)
        self.assertEqual('text/plain', result_multi_same_bucket_1.headers.get('Content-Type'))
        self.assertEqual('no-cache', result_multi_same_bucket_1.headers.get('Cache-Control'))
        self.assertEqual('zh-CN', result_multi_same_bucket_1.headers.get('Content-Language'))
        self.assertEqual('gzip', result_multi_same_bucket_1.headers.get('Content-Encoding'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_multi_same_bucket_1.headers.get('Content-Disposition'))
        self.assertEqual('2022-10-12T00:00:00.000Z', result_multi_same_bucket_1.headers.get('Expires'))
        self.assertEqual('owner3', result_multi_same_bucket_1.headers.get('x-oss-meta-auth'))
        self.assertEqual('owner3', result_multi_same_bucket_1.metadata.get('auth'))
        self.assertEqual('text/plain', result_multi_same_bucket_2.headers.get('Content-Type'))
        self.assertEqual('no-cache', result_multi_same_bucket_2.headers.get('Cache-Control'))
        self.assertEqual('zh-CN', result_multi_same_bucket_2.headers.get('Content-Language'))
        self.assertEqual('gzip', result_multi_same_bucket_2.headers.get('Content-Encoding'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_multi_same_bucket_2.headers.get('Content-Disposition'))
        self.assertEqual('2022-10-12T00:00:00.000Z', result_multi_same_bucket_2.headers.get('Expires'))
        self.assertEqual('owner3', result_multi_same_bucket_2.headers.get('x-oss-meta-auth'))
        self.assertEqual('owner3', result_multi_same_bucket_2.metadata.get('auth'))
        self.assertEqual(None, result_multi_same_bucket_1.metadata.get('x-oss-auth'))
        self.assertEqual(None, result_multi_same_bucket_1.metadata.get('x-oss-meta-auth'))
        self.assertEqual(None, result_multi_same_bucket_2.metadata.get('x-oss-auth'))
        self.assertEqual(None, result_multi_same_bucket_2.metadata.get('x-oss-meta-auth'))

        result_tag_multi_same_bucket_1 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=self.bucket_name,
            key=key_2,
        ))

        result_tag_multi_same_bucket_2 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=self.bucket_name,
            key=multi_key,
        ))
        self.assertEqual(result_tag_multi_same_bucket_1.tag_set.tags, result_tag_multi_same_bucket_2.tag_set.tags)

        # compare tags
        tags = []
        tags_str = ''
        for o in result_tag_multi_same_bucket_2.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA=A&TagB=B", tags_str)


        # case 3: Copy a single part from the different bucket
        single_key_different_bucket = 'single_key_different_bucket'
        result = self.client.copier(
            parallel_num=5,
            leave_parts_on_error=True,
        ).copy(oss.CopyObjectRequest(
            bucket=bucket_name,
            key=single_key_different_bucket,
            source_bucket=self.bucket_name,
            source_key=key
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result_single_key_different_bucket_1 = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        result_single_key_different_bucket_2 = self.client.head_object(oss.HeadObjectRequest(
            bucket=bucket_name,
            key=single_key_different_bucket,
        ))
        self.assertEqual("Normal", result_single_key_different_bucket_2.object_type)
        self.assertEqual(12, result_single_key_different_bucket_1.content_length)
        self.assertEqual(12, result_single_key_different_bucket_2.content_length)
        self.assertEqual('text/plain', result_single_key_different_bucket_1.headers.get('Content-Type'))
        self.assertEqual('no-cache', result_single_key_different_bucket_1.headers.get('Cache-Control'))
        self.assertEqual('zh-CN', result_single_key_different_bucket_1.headers.get('Content-Language'))
        self.assertEqual('gzip', result_single_key_different_bucket_1.headers.get('Content-Encoding'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_single_key_different_bucket_1.headers.get('Content-Disposition'))
        self.assertEqual('2022-10-12T00:00:00.000Z', result_single_key_different_bucket_1.headers.get('Expires'))
        self.assertEqual('owner3', result_single_key_different_bucket_1.headers.get('x-oss-meta-auth'))
        self.assertEqual('owner3', result_single_key_different_bucket_1.metadata.get('auth'))
        self.assertEqual('text/plain', result_single_key_different_bucket_2.headers.get('Content-Type'))
        self.assertEqual('no-cache', result_single_key_different_bucket_2.headers.get('Cache-Control'))
        self.assertEqual('zh-CN', result_single_key_different_bucket_2.headers.get('Content-Language'))
        self.assertEqual('gzip', result_single_key_different_bucket_2.headers.get('Content-Encoding'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_single_key_different_bucket_2.headers.get('Content-Disposition'))
        self.assertEqual('2022-10-12T00:00:00.000Z', result_single_key_different_bucket_2.headers.get('Expires'))
        self.assertEqual('owner3', result_single_key_different_bucket_2.headers.get('x-oss-meta-auth'))
        self.assertEqual('owner3', result_single_key_different_bucket_2.metadata.get('auth'))
        self.assertEqual(None, result_single_key_different_bucket_1.metadata.get('x-oss-auth'))
        self.assertEqual(None, result_single_key_different_bucket_1.metadata.get('x-oss-meta-auth'))
        self.assertEqual(None, result_single_key_different_bucket_2.metadata.get('x-oss-auth'))
        self.assertEqual(None, result_single_key_different_bucket_2.metadata.get('x-oss-meta-auth'))

        result_tag_single_key_different_bucket_1 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        result_tag_single_key_different_bucket_2 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=bucket_name,
            key=single_key_different_bucket,
        ))
        self.assertEqual(result_tag_single_key_different_bucket_1.tag_set.tags, result_tag_single_key_different_bucket_2.tag_set.tags)

        # compare tags
        tags = []
        tags_str = ''
        for o in result_tag_single_key_different_bucket_2.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA=A&TagB=B", tags_str)

        # case 4: Copy a multipart from the different bucket
        multi_key_different_bucket = 'multipart_key_different_bucket'
        result = self.client.copier(
            part_size=100*1024,
            parallel_num=5,
            leave_parts_on_error=True,
            multipart_copy_threshold=100*1024
        ).copy(oss.CopyObjectRequest(
            bucket=bucket_name,
            key=multi_key_different_bucket,
            source_bucket=self.bucket_name,
            source_key=key_2
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result_multi_key_different_bucket_1 = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key_2,
        ))

        result_multi_key_different_bucket_2 = self.client.head_object(oss.HeadObjectRequest(
            bucket=bucket_name,
            key=multi_key_different_bucket,
        ))
        self.assertEqual("Multipart", result_multi_key_different_bucket_2.object_type)
        self.assertEqual(1000 * 1024, result_multi_key_different_bucket_1.content_length)
        self.assertEqual(1000 * 1024, result_multi_key_different_bucket_2.content_length)
        self.assertEqual('text/plain', result_multi_key_different_bucket_1.headers.get('Content-Type'))
        self.assertEqual('no-cache', result_multi_key_different_bucket_1.headers.get('Cache-Control'))
        self.assertEqual('zh-CN', result_multi_key_different_bucket_1.headers.get('Content-Language'))
        self.assertEqual('gzip', result_multi_key_different_bucket_1.headers.get('Content-Encoding'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_multi_key_different_bucket_1.headers.get('Content-Disposition'))
        self.assertEqual('2022-10-12T00:00:00.000Z', result_multi_key_different_bucket_1.headers.get('Expires'))
        self.assertEqual('owner3', result_multi_key_different_bucket_1.headers.get('x-oss-meta-auth'))
        self.assertEqual('owner3', result_multi_key_different_bucket_1.metadata.get('auth'))
        self.assertEqual('text/plain', result_multi_key_different_bucket_2.headers.get('Content-Type'))
        self.assertEqual('no-cache', result_single_key_different_bucket_2.headers.get('Cache-Control'))
        self.assertEqual('zh-CN', result_multi_key_different_bucket_2.headers.get('Content-Language'))
        self.assertEqual('gzip', result_multi_key_different_bucket_2.headers.get('Content-Encoding'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_multi_key_different_bucket_2.headers.get('Content-Disposition'))
        self.assertEqual('2022-10-12T00:00:00.000Z', result_multi_key_different_bucket_2.headers.get('Expires'))
        self.assertEqual('owner3', result_multi_key_different_bucket_2.headers.get('x-oss-meta-auth'))
        self.assertEqual('owner3', result_multi_key_different_bucket_2.metadata.get('auth'))
        self.assertEqual(None, result_multi_key_different_bucket_1.metadata.get('x-oss-auth'))
        self.assertEqual(None, result_multi_key_different_bucket_1.metadata.get('x-oss-meta-auth'))
        self.assertEqual(None, result_multi_key_different_bucket_2.metadata.get('x-oss-auth'))
        self.assertEqual(None, result_multi_key_different_bucket_2.metadata.get('x-oss-meta-auth'))

        result_tag_multi_key_different_bucket_1 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=self.bucket_name,
            key=key_2,
        ))

        result_tag_multi_key_different_bucket_2 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=bucket_name,
            key=multi_key_different_bucket,
        ))
        self.assertEqual(result_tag_multi_key_different_bucket_1.tag_set.tags, result_tag_multi_key_different_bucket_2.tag_set.tags)

        # compare tags
        tags = []
        tags_str = ''
        for o in result_tag_multi_key_different_bucket_2.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA=A&TagB=B", tags_str)

    def test_different_bucket_single_replace_meta_and_tag(self):
        length = 12
        data = random_str(length)
        key = OBJECTNAME_PREFIX + random_str(16)
        bucket_name = random_bucket_name()

        # put bucket
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put object data
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            metadata={
                "client-side-encryption-key": "nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "AES/CTR/NoPadding",
                "client-side-encryption-wrap-alg": "RSA/NONE/PKCS1Padding",
                "x-oss-auth": "owner",
                "x-oss-meta-version": "1.01",
                "flag": "false",
                "content-type": "utf-8",
                "Content-Disposition": "attachment;filename=aaa.txt",
                "Content-Length": "344606",
            },
            tagging='TagA=A&TagB=B',
            body=data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        # case 3: Copy a single part from the different bucket
        single_key_different_bucket = 'single_key_different_bucket'
        result = self.client.copier(
            leave_parts_on_error=True,
        ).copy(oss.CopyObjectRequest(
            bucket=bucket_name,
            key=single_key_different_bucket,
            source_bucket=self.bucket_name,
            source_key=key,
            metadata_directive='replace',
            metadata={
                "x-oss-auth": "customer-owner",
                "x-oss-meta-version": "1.23",
                "flag": "true",
                "content-type": "text/txt",
                'Content-Disposition': 'attachment;filename='+quote('世界')+'.txt',
                "Content-Length": "116",
            },
            tagging='TagA3=A3&TagB3=B3',
            tagging_directive='replace'
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result_single_key_different_bucket_1 = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ))

        result_single_key_different_bucket_2 = self.client.head_object(oss.HeadObjectRequest(
            bucket=bucket_name,
            key=single_key_different_bucket,
        ))
        self.assertEqual("Normal", result_single_key_different_bucket_2.object_type)
        self.assertEqual(12, result_single_key_different_bucket_1.content_length)
        self.assertEqual(12, result_single_key_different_bucket_2.content_length)
        self.assertEqual("nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=", result_single_key_different_bucket_1.metadata.get('client-side-encryption-key'))
        self.assertEqual("De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=", result_single_key_different_bucket_1.metadata.get('client-side-encryption-start'))
        self.assertEqual("AES/CTR/NoPadding", result_single_key_different_bucket_1.metadata.get('client-side-encryption-cek-alg'))
        self.assertEqual("RSA/NONE/PKCS1Padding", result_single_key_different_bucket_1.metadata.get('client-side-encryption-wrap-alg'))
        self.assertEqual("1.01", result_single_key_different_bucket_1.metadata.get('x-oss-meta-version'))
        self.assertEqual("false", result_single_key_different_bucket_1.metadata.get('flag'))
        self.assertEqual("utf-8", result_single_key_different_bucket_1.metadata.get('content-type'))
        self.assertEqual("attachment;filename=aaa.txt", result_single_key_different_bucket_1.metadata.get('Content-Disposition'))
        self.assertEqual("344606", result_single_key_different_bucket_1.metadata.get('Content-Length'))
        self.assertEqual("nyXOp7delQ/MQLjKQMhHLaTHIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=", result_single_key_different_bucket_2.metadata.get('client-side-encryption-key'))
        self.assertEqual("De/S3T8wFjx7QPxAAFl7h7TeI2EsZlfCwovrHyoSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=", result_single_key_different_bucket_2.metadata.get('client-side-encryption-start'))
        self.assertEqual("AES/CTR/NoPadding", result_single_key_different_bucket_2.metadata.get('client-side-encryption-cek-alg'))
        self.assertEqual("RSA/NONE/PKCS1Padding", result_single_key_different_bucket_2.metadata.get('client-side-encryption-wrap-alg'))
        self.assertEqual("1.23", result_single_key_different_bucket_2.metadata.get('x-oss-meta-version'))
        self.assertEqual("true", result_single_key_different_bucket_2.metadata.get('flag'))
        self.assertEqual("text/txt", result_single_key_different_bucket_2.metadata.get('content-type'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_single_key_different_bucket_2.metadata.get('Content-Disposition'))
        self.assertEqual("116", result_single_key_different_bucket_2.metadata.get('Content-Length'))

        result_tag_single_key_different_bucket_1 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=self.bucket_name,
            key=key,
        ))
        tags = []
        tags_str = ''
        for o in result_tag_single_key_different_bucket_1.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA=A&TagB=B", tags_str)

        result_tag_single_key_different_bucket_2 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=bucket_name,
            key=single_key_different_bucket,
        ))

        # compare tags
        tags = []
        tags_str = ''
        for o in result_tag_single_key_different_bucket_2.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA3=A3&TagB3=B3", tags_str)

    def test_different_bucket_multi_replace_meta_and_tag(self):
        length_2 = 1000 * 1024
        data_2 = random_str(length_2)
        key_2 = OBJECTNAME_PREFIX + random_str(16)
        bucket_name = random_bucket_name()

        # put bucket
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put object data2
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key_2,
            metadata={
                "x-oss-auth": "owner",
                "x-oss-meta-version": "1.01",
                "flag": "false",
                "content-type": "utf-8",
                "Content-Disposition": "attachment;filename=aaa.txt",
                "Content-Length": "344606",
            },
            tagging='TagA2=A2&TagB2=B2',
            body=data_2,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        # case 4: Copy a multipart from the different bucket
        multi_key_different_bucket = 'multipart_key_different_bucket'
        result = self.client.copier(
            part_size=100*1024,
            parallel_num=5,
            leave_parts_on_error=True,
            multipart_copy_threshold = 100*1024
        ).copy(oss.CopyObjectRequest(
            bucket=bucket_name,
            key=multi_key_different_bucket,
            source_bucket=self.bucket_name,
            source_key=key_2,
            metadata_directive='REPLACE',
            metadata={
                "client-side-encryption-key": "THIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=",
                "client-side-encryption-start": "oSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=",
                "client-side-encryption-cek-alg": "CTR",
                "client-side-encryption-wrap-alg": "PKCS1Padding",
                "client-side-encryption-data-size": "1024000",
                "client-side-encryption-part-size": "102400",
                "x-oss-auth": "customer-owner",
                "x-oss-meta-version": "1.23",
                "flag": "true",
                "content-type": "text/txt",
                'Content-Disposition': 'attachment;filename=' + quote('世界') + '.txt',
                "Content-Length": "116",
            },
            tagging='TagA3=A3&TagB3=B3',
            tagging_directive='REPLACE'
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        result_multi_key_different_bucket_1 = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=key_2,
        ))

        result_multi_key_different_bucket_2 = self.client.head_object(oss.HeadObjectRequest(
            bucket=bucket_name,
            key=multi_key_different_bucket,
        ))

        self.assertEqual("Multipart", result_multi_key_different_bucket_2.object_type)
        self.assertEqual(1000 * 1024, result_multi_key_different_bucket_1.content_length)
        self.assertEqual(1000 * 1024, result_multi_key_different_bucket_2.content_length)
        self.assertEqual("1.01", result_multi_key_different_bucket_1.metadata.get('x-oss-meta-version'))
        self.assertEqual("false", result_multi_key_different_bucket_1.metadata.get('flag'))
        self.assertEqual("utf-8", result_multi_key_different_bucket_1.metadata.get('content-type'))
        self.assertEqual("attachment;filename=aaa.txt", result_multi_key_different_bucket_1.metadata.get('Content-Disposition'))
        self.assertEqual("344606", result_multi_key_different_bucket_1.metadata.get('Content-Length'))
        self.assertEqual("THIB6q+C+RA6lGwqqYVa+n3aV5uWhygyv1MWmESurppg=", result_multi_key_different_bucket_2.metadata.get('client-side-encryption-key'))
        self.assertEqual("oSZGr343NxCUGIp6fQ9sSuOLMoJg7hNw=", result_multi_key_different_bucket_2.metadata.get('client-side-encryption-start'))
        self.assertEqual("CTR", result_multi_key_different_bucket_2.metadata.get('client-side-encryption-cek-alg'))
        self.assertEqual("PKCS1Padding", result_multi_key_different_bucket_2.metadata.get('client-side-encryption-wrap-alg'))
        self.assertEqual("1024000", result_multi_key_different_bucket_2.metadata.get('client-side-encryption-data-size'))
        self.assertEqual("102400", result_multi_key_different_bucket_2.metadata.get('client-side-encryption-part-size'))
        self.assertEqual("1.23", result_multi_key_different_bucket_2.metadata.get('x-oss-meta-version'))
        self.assertEqual("true", result_multi_key_different_bucket_2.metadata.get('flag'))
        self.assertEqual("text/txt", result_multi_key_different_bucket_2.metadata.get('content-type'))
        self.assertEqual('attachment;filename='+quote('世界')+'.txt', result_multi_key_different_bucket_2.metadata.get('Content-Disposition'))
        self.assertEqual("116", result_multi_key_different_bucket_2.metadata.get('Content-Length'))

        result_tag_multi_key_different_bucket_1 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=self.bucket_name,
            key=key_2,
        ))
        tags = []
        tags_str = ''
        for o in result_tag_multi_key_different_bucket_1.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA2=A2&TagB2=B2", tags_str)

        result_tag_multi_key_different_bucket_2 = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=bucket_name,
            key=multi_key_different_bucket,
        ))

        # compare tags
        tags = []
        tags_str = ''
        for o in result_tag_multi_key_different_bucket_2.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA3=A3&TagB3=B3", tags_str)

    def test_multipart_misc(self):
        length = 200 * 1024 + 1234
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)
        src_bucket_name = self.bucket_name

        # put object data
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            metadata={
                "auth": "owner",
                "version": "1.01",
            },
            content_type="text/plain",
            content_disposition="attachment;filename=aaa.txt",
            content_encoding="deflate",
            cache_control="no-cache",
            expires="Wed, 08 Jul 2022 16:57:01 GMT",
            tagging='TagA=A&TagB=B',
            body=src_data,
            headers={
                "Content-Language": "en-US"
            }
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hreasult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hreasult.hash_crc64
        src_etag = hreasult.etag
        self.assertIsNotNone(src_crc64)

        dst_bucket_name = self.bucket_name
        self.assertEqual(src_bucket_name, dst_bucket_name)
    
        copier = self.client.copier()

        # multipart copy with storage_class & acl
        dst_key = 'multipart_key'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key,
            metadata_directive="COPY",
            tagging_directive="REPLACE",
            acl="public-read",
            storage_class="IA"
        ), multipart_copy_threshold=100*1024)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertNotEqual(src_etag, result.etag)
        self.assertIsNotNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertEqual("1.01", hresult.metadata.get('version'))
        self.assertEqual("owner", hresult.metadata.get('auth'))
        self.assertEqual("text/plain", hresult.content_type)
        self.assertEqual("attachment;filename=aaa.txt", hresult.content_disposition)
        self.assertEqual("deflate", hresult.content_encoding)
        self.assertEqual("no-cache", hresult.cache_control)
        self.assertEqual("Wed, 08 Jul 2022 16:57:01 GMT", hresult.expires)
        self.assertIsNone(hresult.tagging_count)
        self.assertEqual("en-US", hresult.headers["Content-Language"])
        self.assertEqual("IA", hresult.storage_class)

        aresult = self.client.get_object_acl(oss.GetObjectAclRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("public-read", aresult.acl)

        # multipart parallel_num = 1
        dst_key = 'multipart_key-1'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key,
            storage_class="IA",
            metadata_directive="REPLACE",
            tagging_directive="COPY",
            metadata={
                "auth": "jack",
                "version": "2.01",
                "comment": "just test",
            },
            content_type="text/js",
            content_disposition="attachment;filename=bbb.txt",
            cache_control="no-cache,123",
            body=src_data,
        ), multipart_copy_threshold=100*1024, parallel_num=1)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertNotEqual(src_etag, result.etag)
        self.assertIsNotNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertEqual("2.01", hresult.metadata.get('version'))
        self.assertEqual("jack", hresult.metadata.get('auth'))
        self.assertEqual("just test", hresult.metadata.get('comment'))
        self.assertEqual("text/js", hresult.content_type)
        self.assertEqual("attachment;filename=bbb.txt", hresult.content_disposition)
        self.assertIsNone(hresult.content_encoding)
        self.assertEqual("no-cache,123", hresult.cache_control)
        self.assertIsNone(hresult.expires)
        self.assertEqual(2, hresult.tagging_count)

        # compare tags
        tresult = self.client.get_object_tagging(oss.GetObjectTaggingRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        tags = []
        tags_str = ''
        for o in tresult.tag_set.tags:
            tags.append(f"{str(o.key)}={str(o.value)}")
        if tags:
            tags_str = '&'.join(tags)
        self.assertEqual("TagA=A&TagB=B", tags_str)

        #invalid part-size, parallel_num, multipart_copy_threshold
        dst_key = 'key-invalid-arg'
        result = copier.copy(oss.CopyObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
            source_bucket=src_bucket_name,
            source_key=src_key,
            storage_class="IA",
            metadata_directive="REPLACE",
            tagging_directive="COPY",
            metadata={
                "auth": "jack",
                "version": "2.01",
                "comment": "just test",
            },
            content_type="text/js",
            content_disposition="attachment;filename=bbb.txt",
            cache_control="no-cache,123",
            body=src_data,
        ), multipart_copy_threshold=-1, parallel_num=-1, part_size=-1)
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(src_crc64, result.hash_crc64)
        self.assertEqual(src_etag, result.etag)
        self.assertIsNone(result.upload_id)
        self.assertIsNone(result.version_id)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=dst_bucket_name,
            key=dst_key,
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)
        self.assertEqual(length, hresult.content_length)
        self.assertEqual("2.01", hresult.metadata.get('version'))
        self.assertEqual("jack", hresult.metadata.get('auth'))
        self.assertEqual("just test", hresult.metadata.get('comment'))
        self.assertEqual("text/js", hresult.content_type)
        self.assertEqual("attachment;filename=bbb.txt", hresult.content_disposition)
        self.assertIsNone(hresult.content_encoding)
        self.assertEqual("no-cache,123", hresult.cache_control)
        self.assertIsNone(hresult.expires)
        self.assertEqual(2, hresult.tagging_count)

    def test_with_error(self):
        length = 100 * 1024 + 123
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)
        src_bucket_name = self.bucket_name

        copier = self.client.copier()

        dst_key = "dst-key"
        dst_bucket_name = src_bucket_name

        # case 1: bucket not set
        dst_key = "dst-key"
        try:
            copier.copy(oss.CopyObjectRequest(
                #bucket=dst_bucket_name,
                key=dst_key,
                source_key=src_key
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIsInstance(e, oss.exceptions.ParamInvalidError)
            self.assertIn('invalid field, request.bucket', str(e))

        # case 2: key not set
        dst_key = "dst-key"
        try:
            copier.copy(oss.CopyObjectRequest(
                bucket=dst_bucket_name,
                #key=dst_key,
                source_key=src_key
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIsInstance(e, oss.exceptions.ParamInvalidError)
            self.assertIn('invalid field, request.key', str(e))

        # case 3: source key not set
        dst_key = "dst-key"
        try:
            copier.copy(oss.CopyObjectRequest(
                bucket=dst_bucket_name,
                key=dst_key,
                #source_key=src_key
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIsInstance(e, oss.exceptions.ParamInvalidError)
            self.assertIn('invalid field, request.source_key', str(e))

        # case 4: head object failed
        dst_key = "dst-key"
        try:
            copier.copy(oss.CopyObjectRequest(
                bucket=dst_bucket_name,
                key=dst_key,
                source_key=src_key
            ))
            self.fail("should not here")
        except Exception as e:
            self.assertIsInstance(e, oss.exceptions.OperationError)
            self.assertIn('HeadObject', str(e))

        # case 5: copy object failed
        fake_metadata_prop = oss.HeadObjectResult(content_length=length)
        dst_key = "dst-key"
        try:
            copier.copy(oss.CopyObjectRequest(
                bucket=dst_bucket_name,
                key=dst_key,
                source_key=src_key
            ), metadata_properties=fake_metadata_prop)
            self.fail("should not here")
        except Exception as e:
            self.assertIsInstance(e, oss.CopyError)
            self.assertIn('CopyObject', str(e))

        # case 6: copy object failed with shallow copy
        fake_metadata_prop = oss.HeadObjectResult(content_length=length)
        dst_key = "dst-key"
        try:
            copier.copy(oss.CopyObjectRequest(
                bucket=dst_bucket_name,
                key=dst_key,
                source_key=src_key
            ), metadata_properties=fake_metadata_prop, multipart_copy_threshold=100*1024)
            self.fail("should not here")
        except oss.CopyError as e:
            self.assertIn('CopyObject', str(e))

        # case 7: multipart upload-part-copy failed
        fake_metadata_prop = oss.HeadObjectResult(content_length=length)
        dst_key = "dst-key-abort-upload-id"
        try:
            copier.copy(oss.CopyObjectRequest(
                bucket=dst_bucket_name,
                key=dst_key,
                source_key=src_key
            ), 
            metadata_properties=fake_metadata_prop,
            multipart_copy_threshold=100*1024,
            disable_shallow_copy=True)
            self.fail("should not here")
        except oss.CopyError as e:
            self.assertIsInstance(e, oss.CopyError)
            self.assertIn('UploadPartCopy', str(e))
            self.assertIsNotNone(e.upload_id)

            lmresult = self.client.list_multipart_uploads(oss.ListMultipartUploadsRequest(
                bucket=dst_bucket_name,
                prefix=dst_key,
            ))
            self.assertIsNone(lmresult.uploads)

        # case 8: multipart upload-part-copy failed, not abort
        fake_metadata_prop = oss.HeadObjectResult(content_length=length)
        dst_key = "dst-key-not-abort-upload-id"
        try:
            copier.copy(oss.CopyObjectRequest(
                bucket=dst_bucket_name,
                key=dst_key,
                source_key=src_key
            ), 
            metadata_properties=fake_metadata_prop,
            multipart_copy_threshold=100*1024,
            disable_shallow_copy=True,
            leave_parts_on_error=True)
            self.fail("should not here")
        except oss.CopyError as e:
            self.assertIsInstance(e, oss.CopyError)
            self.assertIn('UploadPartCopy', str(e))
            self.assertIsNotNone(e.upload_id)

            lmresult = self.client.list_multipart_uploads(oss.ListMultipartUploadsRequest(
                bucket=dst_bucket_name,
                prefix=dst_key
            ))
            self.assertIsNotNone(lmresult.uploads)
            self.assertEqual(1, len(lmresult.uploads))
            self.assertEqual(e.upload_id, lmresult.uploads[0].upload_id)

        # case 9: crc check failed
        # put object data
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=src_bucket_name,
            key=src_key,
            body=src_data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        fake_metadata_prop = oss.HeadObjectResult(content_length=length, hash_crc64="invalid crc")
        dst_key = "dst-key-crc-check-fail"
        try:
            copier.copy(oss.CopyObjectRequest(
                bucket=dst_bucket_name,
                key=dst_key,
                source_key=src_key
            ), 
            metadata_properties=fake_metadata_prop,
            multipart_copy_threshold=100*1024,
            disable_shallow_copy=True)
            self.fail("should not here")
        except oss.CopyError as e:
            self.assertIsInstance(e, oss.CopyError)
            self.assertIn('crc is inconsistent, ', str(e))
            self.assertIn('dst-key-crc-check-fail, ', str(e))


    def test_copier_progress_with_single_copy(self):
        length = 100 * 1024 + 123
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)

        global bytes_added, total_bytes_transferred, total_bytes_expected, last_written
        bytes_added = 0
        total_bytes_transferred = 0
        total_bytes_expected = 0
        last_written = 0

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            body=src_data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hresult.hash_crc64
        self.assertIsNotNone(src_crc64)

        def _progress_fn(n, written, total):
            global last_written
            global bytes_added
            global total_bytes_transferred
            global total_bytes_expected

            n = written - last_written
            bytes_added += n
            total_bytes_transferred = written
            last_written = written
            total_bytes_expected = total


        copier = self.client.copier()

        dst_key = 'single_copy_key'
        result = copier.copy(oss.CopyObjectRequest(
                bucket=self.bucket_name,
                key=dst_key,
                source_bucket=self.bucket_name,
                source_key=src_key,
                progress_fn=_progress_fn
            ),
                part_size=10 * 1024,
                parallel_num=5,
                leave_parts_on_error=True
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(bytes_added, length)
        self.assertEqual(total_bytes_transferred, length)
        self.assertEqual(total_bytes_expected, length)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=dst_key
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

    def test_copier_progress_with_shallow_copy(self):
        length = 100 * 1024 + 123
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)

        global bytes_added, total_bytes_transferred, total_bytes_expected, last_written
        bytes_added = 0
        total_bytes_transferred = 0
        total_bytes_expected = 0
        last_written = 0

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            body=src_data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hresult.hash_crc64
        self.assertIsNotNone(src_crc64)

        def _progress_fn(n, written, total):
            global last_written
            global bytes_added
            global total_bytes_transferred
            global total_bytes_expected

            n = written - last_written
            bytes_added += n
            total_bytes_transferred = written
            last_written = written
            total_bytes_expected = total


        copier = self.client.copier()

        dst_key = 'shallow_copy_key'
        result = copier.copy(oss.CopyObjectRequest(
                bucket=self.bucket_name,
                key=dst_key,
                source_bucket=self.bucket_name,
                source_key=src_key,
                progress_fn=_progress_fn
            ),
                part_size=10 * 1024,
                parallel_num=5,
                leave_parts_on_error=True,
                multipart_copy_threshold=100 * 1024,
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(bytes_added, length)
        self.assertEqual(total_bytes_transferred, length)
        self.assertEqual(total_bytes_expected, length)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=dst_key
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

    def test_copier_progress_with_single_multipart_copy(self):
        length = 100 * 1024 + 123
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)
        bucket_name = random_bucket_name()

        global bytes_added, total_bytes_transferred, total_bytes_expected, last_written
        bytes_added = 0
        total_bytes_transferred = 0
        total_bytes_expected = 0
        last_written = 0

        # put bucket
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            body=src_data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hresult.hash_crc64
        self.assertIsNotNone(src_crc64)

        def _progress_fn(n, written, total):
            global last_written
            global bytes_added
            global total_bytes_transferred
            global total_bytes_expected

            n = written - last_written
            bytes_added += n
            total_bytes_transferred = written
            last_written = written
            total_bytes_expected = total


        copier = self.client.copier()

        dst_key = 'single_multipart_copy_key'
        result = copier.copy(oss.CopyObjectRequest(
                bucket=bucket_name,
                key=dst_key,
                source_bucket=self.bucket_name,
                source_key=src_key,
                progress_fn=_progress_fn
            ),
                part_size=100 * 1024,
                parallel_num=1,
                leave_parts_on_error=True,
                multipart_copy_threshold=100 * 1024,
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(bytes_added, length)
        self.assertEqual(total_bytes_transferred, length)
        self.assertEqual(total_bytes_expected, length)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=bucket_name,
            key=dst_key
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)

    def test_copier_progress_with_thread_multipart_copy(self):
        length = 500 * 1024 + 123
        src_data = random_str(length)
        src_key = OBJECTNAME_PREFIX + random_str(16)
        bucket_name = random_bucket_name()

        global bytes_added, total_bytes_transferred, total_bytes_expected, last_written
        bytes_added = 0
        total_bytes_transferred = 0
        total_bytes_expected = 0
        last_written = 0

        # put bucket
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
            body=src_data,
        ))
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=src_key,
        ))
        src_crc64 = hresult.hash_crc64
        self.assertIsNotNone(src_crc64)

        def _progress_fn(n, written, total):
            global last_written
            global bytes_added
            global total_bytes_transferred
            global total_bytes_expected

            n = written - last_written
            bytes_added += n
            total_bytes_transferred = written
            last_written = written
            total_bytes_expected = total


        copier = self.client.copier()

        dst_key = 'thread_multipart_copy_key'
        result = copier.copy(oss.CopyObjectRequest(
                bucket=bucket_name,
                key=dst_key,
                source_bucket=self.bucket_name,
                source_key=src_key,
                progress_fn=_progress_fn
            ),
                part_size=100 * 1024,
                parallel_num=5,
                leave_parts_on_error=True,
                multipart_copy_threshold=100 * 1024,
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(bytes_added, length)
        self.assertEqual(total_bytes_transferred, length)
        self.assertEqual(total_bytes_expected, length)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=bucket_name,
            key=dst_key
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(src_crc64, hresult.hash_crc64)


class TestUploader(TestIntegration):
    def test_uploader_progress_with_single_upload(self):
        length = 100 * 1024 + 123
        data = random_str(length)
        object_name = OBJECTNAME_PREFIX + random_str(16)

        global bytes_added, total_bytes_transferred, total_bytes_expected, last_written
        bytes_added = 0
        total_bytes_transferred = 0
        total_bytes_expected = 0
        last_written = 0

        def _progress_fn(n, written, total):
            global last_written
            global bytes_added
            global total_bytes_transferred
            global total_bytes_expected

            n = written - last_written
            bytes_added += n
            total_bytes_transferred = written
            last_written = written
            total_bytes_expected = total

        uploader = self.client.uploader()

        result = uploader.upload_from(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=object_name,
                progress_fn=_progress_fn
            ), io.StringIO(data),
                part_size=500 * 1024,
                parallel_num=5,
                leave_parts_on_error=True
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(total_bytes_transferred, length)
        self.assertEqual(total_bytes_expected, length)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=object_name
        ))
        self.assertEqual("Normal", hresult.object_type)
        self.assertEqual(length, hresult.content_length)

    def test_uploader_progress_with_single_multipart(self):
        length = 500 * 1024 + 123
        data = random_str(length)
        object_name = OBJECTNAME_PREFIX + random_str(16)

        global bytes_added, total_bytes_transferred, total_bytes_expected, last_written
        bytes_added = 0
        total_bytes_transferred = 0
        total_bytes_expected = 0
        last_written = 0

        def _progress_fn(n, written, total):
            global last_written
            global bytes_added
            global total_bytes_transferred
            global total_bytes_expected

            n = written - last_written
            bytes_added += n
            total_bytes_transferred = written
            last_written = written
            total_bytes_expected = total

        uploader = self.client.uploader()
        result = uploader.upload_from(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=object_name,
                progress_fn=_progress_fn
            ), io.StringIO(data),
                part_size=100 * 1024,
                parallel_num=1,
                leave_parts_on_error=True,
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(total_bytes_transferred, length)
        self.assertEqual(total_bytes_expected, length)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=object_name
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(length, hresult.content_length)

    def test_uploader_progress_with_thread_multipart(self):
        length = 500 * 1024 + 123
        data = random_str(length)
        object_name = OBJECTNAME_PREFIX + random_str(16)

        global bytes_added, total_bytes_transferred, total_bytes_expected, last_written
        bytes_added = 0
        total_bytes_transferred = 0
        total_bytes_expected = 0
        last_written = 0

        def _progress_fn(n, written, total):
            global last_written
            global bytes_added
            global total_bytes_transferred
            global total_bytes_expected

            n = written - last_written
            bytes_added += n
            total_bytes_transferred = written
            last_written = written
            total_bytes_expected = total

        uploader = self.client.uploader()
        result = uploader.upload_from(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=object_name,
                progress_fn=_progress_fn
            ), io.StringIO(data),
                part_size=100 * 1024,
                parallel_num=3,
                leave_parts_on_error=True,
        )
        self.assertIsNotNone(result)
        self.assertEqual(200, result.status_code)
        self.assertEqual(total_bytes_transferred, length)
        self.assertEqual(total_bytes_expected, length)

        hresult = self.client.head_object(oss.HeadObjectRequest(
            bucket=self.bucket_name,
            key=object_name
        ))
        self.assertEqual("Multipart", hresult.object_type)
        self.assertEqual(length, hresult.content_length)
