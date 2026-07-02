# pylint: skip-file
from typing import cast
import xml.etree.ElementTree as ET
from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.models import bucket_basic as model
from alibabacloud_oss_v2.aio.operations import bucket_basic as operations
from ... import MockAsyncHttpResponse
from . import TestOperations

class TestBucketBasic(TestOperations):

    async def test_put_bucket(self):
        request = model.PutBucketRequest(
            bucket='bucket',
            acl='private',
            resource_group_id='rg-id',
            create_bucket_configuration=model.CreateBucketConfiguration(
                storage_class='Standard'
            ),
        )

        result = await operations.put_bucket(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertIn('private', self.request_dump.headers.get('x-oss-acl'))
        self.assertIn('rg-id', self.request_dump.headers.get('x-oss-resource-group-id'))

        root = ET.fromstring(self.request_dump.body)
        self.assertEqual('CreateBucketConfiguration', root.tag)
        self.assertEqual('Standard', root.findtext('StorageClass'))
        self.assertEqual(None, root.findtext('DataRedundancyType'))

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual('id-1234', result.request_id)

    async def test_put_bucket_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.PutBucketRequest(
            bucket='bucket',
            acl='private',
            resource_group_id='rg-id',
        )

        try:
            result = await operations.put_bucket(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertIn('private', self.request_dump.headers.get('x-oss-acl'))
        self.assertIn('rg-id', self.request_dump.headers.get('x-oss-resource-group-id'))

    async def test_put_bucket_acl(self):
        request = model.PutBucketAclRequest(
            bucket='bucket',
            acl='private',
        )

        result = await operations.put_bucket_acl(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?acl=', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertIn('private', self.request_dump.headers.get('x-oss-acl'))


        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_put_bucket_acl_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.PutBucketAclRequest(
            bucket='bucket',
            acl='private',
        )

        try:
            result = await operations.put_bucket_acl(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?acl=', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertIn('private', self.request_dump.headers.get('x-oss-acl'))

    async def test_get_bucket_acl(self):
        request = model.GetBucketAclRequest(
            bucket='bucket',
        )

        result = await operations.get_bucket_acl(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?acl=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_get_bucket_acl_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.GetBucketAclRequest(
            bucket='bucket',
        )

        try:
            result = await operations.get_bucket_acl(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?acl=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

    async def test_list_objects_v2(self):
        request = model.ListObjectsV2Request(
            bucket='example-bucket',
            delimiter='/',
            start_after='b',
            encoding_type='url',
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            fetch_owner=True,
            request_payer='requester',
        )

        result = await operations.list_objects_v2(self.client, request)
        self.assertEqual('https://example-bucket.oss-cn-hangzhou.aliyuncs.com/?encoding-type=url&list-type=2&delimiter=%2F&start-after=b&continuation-token=ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA&max-keys=10&prefix=aaa&fetch-owner=true', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_list_objects_v2_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.ListObjectsV2Request(
            bucket='example-bucket',
            delimiter='/',
            start_after='b',
            encoding_type='url',
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            fetch_owner=True,
            request_payer='requester',
        )

        try:
            result = await operations.list_objects_v2(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://example-bucket.oss-cn-hangzhou.aliyuncs.com/?encoding-type=url&list-type=2&delimiter=%2F&start-after=b&continuation-token=ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA&max-keys=10&prefix=aaa&fetch-owner=true', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

    async def test_get_bucket_stat(self):
        request = model.GetBucketStatRequest(
            bucket='bucket',
        )

        result = await operations.get_bucket_stat(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?stat=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_get_bucket_stat_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.GetBucketStatRequest(
            bucket='bucket',
        )

        try:
            result = await operations.get_bucket_stat(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?stat=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

    async def test_list_objects(self):
        request = model.ListObjectsRequest(
            bucket='example-bucket',
            delimiter='/',
            encoding_type='url',
            marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            request_payer='requester',
        )

        result = await operations.list_objects(self.client, request)
        self.assertEqual('https://example-bucket.oss-cn-hangzhou.aliyuncs.com/?encoding-type=url&delimiter=%2F&marker=ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA&max-keys=10&prefix=aaa', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)
        self.assertIn('requester', self.request_dump.headers.get('x-oss-request-payer'))

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_list_objects_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.ListObjectsRequest(
            bucket='example-bucket',
            delimiter='/',
            encoding_type='url',
            marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            request_payer='requester',
        )

        try:
            result = await operations.list_objects(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://example-bucket.oss-cn-hangzhou.aliyuncs.com/?encoding-type=url&delimiter=%2F&marker=ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA&max-keys=10&prefix=aaa', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)
        self.assertIn('requester', self.request_dump.headers.get('x-oss-request-payer'))

    async def test_get_bucket_info(self):
        request = model.GetBucketInfoRequest(
            bucket='bucket',
        )

        result = await operations.get_bucket_info(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?bucketInfo=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_get_bucket_info_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.GetBucketInfoRequest(
            bucket='bucket',
        )

        try:
            result = await operations.get_bucket_info(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?bucketInfo=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

    async def test_get_bucket_location(self):
        request = model.GetBucketInfoRequest(
            bucket='bucket',
        )

        result = await operations.get_bucket_location(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?location=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_get_bucket_location_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.GetBucketInfoRequest(
            bucket='bucket',
        )

        try:
            result = await operations.get_bucket_location(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?location=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

    async def test_put_bucket_versioning(self):
        request = model.PutBucketVersioningRequest(
            bucket='bucket',
            versioning_configuration=model.VersioningConfiguration(
                status='Enabled'
            )
        )

        xml_data = r'''<VersioningConfiguration><Status>Enabled</Status></VersioningConfiguration>'''

        result = await operations.put_bucket_versioning(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?versioning=', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)
        self.assertEqual(xml_data.encode(), self.request_dump.body)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_put_bucket_versioning_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.PutBucketVersioningRequest(
            bucket='bucket',
        )

        try:
            result = await operations.put_bucket_versioning(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?versioning=', self.request_dump.url)
        self.assertEqual('PUT', self.request_dump.method)

    async def test_get_bucket_versioning(self):
        request = model.GetBucketVersioningRequest(
            bucket='bucket',
        )

        result = await operations.get_bucket_versioning(self.client, request)
        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?versioning=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_get_bucket_versioning_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.GetBucketVersioningRequest(
            bucket='bucket',
        )

        try:
            result = await operations.get_bucket_versioning(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://bucket.oss-cn-hangzhou.aliyuncs.com/?versioning=', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)


    async def test_list_object_versions(self):
        request = model.ListObjectVersionsRequest(
            bucket='example-bucket',
            encoding_type='url',
            delimiter='/',
            key_marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            version_id_marker='CAEQMxiBgICbof2D0BYiIGRhZjgwMzJiMjA3MjQ0ODE5MWYxZDYwMzJlZjU1',
            request_payer='requester',
        )

        result = await operations.list_object_versions(self.client, request)
        self.assertEqual('https://example-bucket.oss-cn-hangzhou.aliyuncs.com/?encoding-type=url&versions=&delimiter=%2F&key-marker=ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA&version-id-marker=CAEQMxiBgICbof2D0BYiIGRhZjgwMzJiMjA3MjQ0ODE5MWYxZDYwMzJlZjU1&max-keys=10&prefix=aaa', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

    async def test_list_object_versions_fail(self):
        self.set_responseFunc(self.response_403_InvalidAccessKeyId)
        request = model.ListObjectVersionsRequest(
            bucket='example-bucket',
            encoding_type='url',
            delimiter='/',
            key_marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            version_id_marker='CAEQMxiBgICbof2D0BYiIGRhZjgwMzJiMjA3MjQ0ODE5MWYxZDYwMzJlZjU1',
            request_payer='requester',
        )

        try:
            result = await operations.list_object_versions(self.client, request)
            self.fail('should not here')
        except exceptions.OperationError as ope:
            self.assertIsInstance(ope.unwrap(), exceptions.ServiceError)
            serr = cast(exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual('id-1234', serr.request_id)
            self.assertEqual('InvalidAccessKeyId', serr.code)

        self.assertEqual('https://example-bucket.oss-cn-hangzhou.aliyuncs.com/?encoding-type=url&versions=&delimiter=%2F&key-marker=ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA&version-id-marker=CAEQMxiBgICbof2D0BYiIGRhZjgwMzJiMjA3MjQ0ODE5MWYxZDYwMzJlZjU1&max-keys=10&prefix=aaa', self.request_dump.url)
        self.assertEqual('GET', self.request_dump.method)

    async def test_list_object_versions_encoding_type(self):
        xml_data = r'''<?xml version="1.0" encoding="UTF-8"?>
<ListVersionsResult>
  <Name>demo-bucket</Name>
  <Prefix>demo%2F</Prefix>
  <KeyMarker>demo%2Fkey-marker</KeyMarker>
  <MaxKeys>20</MaxKeys>
  <Delimiter>%2F</Delimiter>
  <EncodingType>url</EncodingType>
  <IsTruncated>true</IsTruncated>
  <NextKeyMarker>demo%2FREADME-CN.md</NextKeyMarker>
  <Version>
    <Key>demo%2FREADME-CN.md</Key>
    <VersionId>id-1</VersionId>
  </Version>
  <DeleteMarker>
    <Key>demo%2FLICENSE</Key>
    <VersionId>id-2</VersionId>
  </DeleteMarker>
  <CommonPrefixes>
    <Prefix>demo%2F.git%2F</Prefix>
  </CommonPrefixes>
</ListVersionsResult>'''

        def response_func():
            return MockAsyncHttpResponse(
                status_code=200,
                reason='OK',
                headers={'x-oss-request-id': 'id-1234', 'Content-Type': 'application/xml'},
                body=xml_data.encode(),
            )
        self.set_responseFunc(response_func)

        request = model.ListObjectVersionsRequest(
            bucket='bucket',
        )

        result = await operations.list_object_versions(self.client, request)
        self.assertEqual(200, result.status_code)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual('demo/', result.prefix)
        self.assertEqual('demo/key-marker', result.key_marker)
        self.assertEqual('/', result.delimiter)
        self.assertEqual('demo/README-CN.md', result.next_key_marker)
        self.assertEqual('demo/README-CN.md', result.version[0].key)
        self.assertEqual('demo/LICENSE', result.delete_marker[0].key)
        self.assertEqual('demo/.git/', result.common_prefixes[0].prefix)
