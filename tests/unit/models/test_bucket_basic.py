# pylint: skip-file
import unittest
import xml.etree.ElementTree as ET
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_basic as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from .. import MockHttpResponse
import datetime

class TestPutBucket(unittest.TestCase):
    def test_constructor_types(self):
        cfg = model.CreateBucketConfiguration()
        self.assertIsNone(cfg.storage_class)
        self.assertIsNone(cfg.data_redundancy_type)
        self.assertIsInstance(cfg, serde.Model)

        cfg = model.CreateBucketConfiguration(
            storage_class='IA',
            data_redundancy_type='LZR'
        )
        self.assertEqual('IA', cfg.storage_class)
        self.assertEqual('LZR', cfg.data_redundancy_type)

        cfg = model.CreateBucketConfiguration(
            storage_class='Cold',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(cfg, 'storage_class'))
        self.assertEqual('Cold', cfg.storage_class)
        self.assertFalse(hasattr(cfg, 'invalid_field'))

    def test_serialize_types(self):
        cfg = model.CreateBucketConfiguration()
        xml_data = serde.serialize_xml(cfg)
        root = ET.fromstring(xml_data)
        self.assertEqual('CreateBucketConfiguration', root.tag)
        self.assertEqual(None, root.findtext('StorageClass'))
        self.assertEqual(None, root.findtext('DataRedundancyType'))

        cfg = model.CreateBucketConfiguration(
            storage_class='Standard',
        )
        xml_data = serde.serialize_xml(cfg)
        root = ET.fromstring(xml_data)
        self.assertEqual('CreateBucketConfiguration', root.tag)
        self.assertEqual('Standard', root.findtext('StorageClass'))
        self.assertEqual(None, root.findtext('DataRedundancyType'))

        cfg = model.CreateBucketConfiguration(
            storage_class='Standard',
            data_redundancy_type='LRS'
        )
        xml_data = serde.serialize_xml(cfg)
        root = ET.fromstring(xml_data)
        self.assertEqual('CreateBucketConfiguration', root.tag)
        self.assertEqual('Standard', root.findtext('StorageClass'))
        self.assertEqual('LRS', root.findtext('DataRedundancyType'))

    def test_deserialize_types(self):
        xml_data = r'''
        <CreateBucketConfiguration>
            <StorageClass>Standard</StorageClass>
            <DataRedundancyType>LRS</DataRedundancyType>    
        </CreateBucketConfiguration>'''

        cfg = model.CreateBucketConfiguration()
        serde.deserialize_xml(xml_data=xml_data, obj=cfg)
        self.assertEqual('Standard', cfg.storage_class)
        self.assertEqual('LRS', cfg.data_redundancy_type)

    def test_constructor_request(self):
        request = model.PutBucketRequest(bucket=None)
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.acl)
        self.assertIsNone(request.resource_group_id)
        self.assertIsNone(request.create_bucket_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketRequest(
            bucket='bucket',
            acl='acl',
            resource_group_id='rg-id',
            create_bucket_configuration=model.CreateBucketConfiguration(
                storage_class='Standard'
            ),
        )
        self.assertEqual('bucket', request.bucket)
        self.assertEqual('acl', request.acl)
        self.assertEqual('rg-id', request.resource_group_id)
        self.assertEqual(
            'Standard', request.create_bucket_configuration.storage_class)
        self.assertEqual(
            None, request.create_bucket_configuration.data_redundancy_type)

        # common headers & parameters & payload
        request = model.PutBucketRequest(
            bucket='bucket',
            acl='acl',
            headers={'key1': 'value1'},
            parameters={'parm1': 'value1'},
            payload='hello world',
        )
        self.assertEqual('bucket', request.bucket)
        self.assertEqual('acl', request.acl)
        self.assertDictEqual({'key1': 'value1'}, request.headers)
        self.assertDictEqual({'parm1': 'value1'}, request.parameters)
        self.assertEqual('hello world', request.payload)

    def test_serialize_request(self):
        request = model.PutBucketRequest(
            bucket='bucket',
            acl='acl',
            resource_group_id='rg-id',
            create_bucket_configuration=model.CreateBucketConfiguration(
                storage_class='Standard'
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucket',
            method='PUT',
            bucket=request.bucket,
        ))

        self.assertEqual('PutBucket', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucket', op_input.bucket)

        self.assertEqual('acl', op_input.headers.get('x-oss-acl'))
        self.assertEqual(
            'rg-id', op_input.headers.get('x-oss-resource-group-id'))
        self.assertEqual(0, len(op_input.parameters.items()))

        root = ET.fromstring(op_input.body)
        self.assertEqual('CreateBucketConfiguration', root.tag)
        self.assertEqual('Standard', root.findtext('StorageClass'))
        self.assertEqual(None, root.findtext('DataRedundancyType'))

    def test_constructor_result(self):
        result = model.PutBucketResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123'
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)


class TestPutBucketAcl(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketAclRequest(bucket='example-bucket')
        self.assertIsNotNone(request.bucket)
        self.assertIsNone(request.acl)
        self.assertIsInstance(request, serde.Model)

        request = model.PutBucketAclRequest(
            bucket='example-bucket',
            acl='private'
        )
        self.assertEqual('example-bucket', request.bucket)
        self.assertEqual('private', request.acl)

        request = model.PutBucketAclRequest(
            bucket='example-bucket',
            acl='public-read-write',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('example-bucket', request.bucket)
        self.assertTrue(hasattr(request, 'acl'))
        self.assertEqual('public-read-write', request.acl)
        self.assertFalse(hasattr(request, 'invalid_field'))


    def test_serialize_request(self):
        request = model.PutBucketAclRequest(
            bucket='example-bucket',
            acl='public-read-write',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketAcl',
            method='PUT',
            bucket=request.bucket,
        ))

        self.assertEqual('PutBucketAcl', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual('public-read-write', op_input.headers.get('x-oss-acl'))
        self.assertEqual(0, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.PutBucketAclResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketAclResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123'
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)

class TestGetBucketAcl(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketAclRequest(bucket='example-bucket')
        self.assertIsNotNone(request.bucket)
        self.assertIsInstance(request, serde.Model)

        request = model.GetBucketAclRequest(
            bucket='example-bucket',
        )
        self.assertEqual('example-bucket', request.bucket)

        request = model.GetBucketAclRequest(
            bucket='example-bucket',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('example-bucket', request.bucket)
        self.assertFalse(hasattr(request, 'invalid_field'))

    def test_serialize_request(self):
        request = model.GetBucketAclRequest(
            bucket='example-bucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketAcl',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('GetBucketAcl', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(0, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.GetBucketAclResult()
        self.assertIsNone(result.acl)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketAclResult(
            acl='public-read-write',
            owner=model.Owner(
                id='0022012****',
                display_name='user_example',
            ),
        )
        self.assertEqual('public-read-write', result.acl)
        self.assertEqual('0022012****', result.owner.id)
        self.assertEqual('user_example', result.owner.display_name)

        result = model.GetBucketAclResult(
            acl='public-read-write',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(result, 'acl'))
        self.assertEqual('public-read-write', result.acl)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
        <AccessControlPolicy>
            <Owner>
                <ID>0022012****</ID>
                <DisplayName>user_example</DisplayName>
            </Owner>
            <AccessControlList>
                <Grant>public-read</Grant>
            </AccessControlList>
        </AccessControlPolicy>'''

        result = model.GetBucketAclResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual('0022012****', result.owner.id)
        self.assertEqual('user_example', result.owner.display_name)
        self.assertEqual('public-read', result.acl)


class TestListObjectsV2(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListObjectsV2Request(bucket='example-bucket')
        self.assertIsNotNone(request.bucket)
        self.assertIsInstance(request, serde.Model)

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
        self.assertEqual('example-bucket', request.bucket)
        self.assertEqual('/', request.delimiter)
        self.assertEqual('b', request.start_after)
        self.assertEqual('url', request.encoding_type)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', request.continuation_token)
        self.assertEqual(10, request.max_keys)
        self.assertEqual('aaa', request.prefix)
        self.assertEqual(True, request.fetch_owner)
        self.assertEqual('requester', request.request_payer)

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
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertTrue(hasattr(request, 'delimiter'))
        self.assertTrue(hasattr(request, 'start_after'))
        self.assertTrue(hasattr(request, 'encoding_type'))
        self.assertTrue(hasattr(request, 'continuation_token'))
        self.assertTrue(hasattr(request, 'max_keys'))
        self.assertTrue(hasattr(request, 'prefix'))
        self.assertTrue(hasattr(request, 'fetch_owner'))
        self.assertTrue(hasattr(request, 'request_payer'))
        self.assertFalse(hasattr(request, 'invalid_field'))
        self.assertEqual('example-bucket', request.bucket)



    def test_serialize_request(self):
        request = model.ListObjectsV2Request(
            bucket='example-bucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListObjectsV2',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('ListObjectsV2', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(0, len(op_input.parameters.items()))

        request = model.ListObjectsV2Request(
            bucket='example-bucket',
            delimiter='/',
            start_after='b',
            encoding_type='url',
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            fetch_owner=True,
            request_payer='requester'
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListObjectsV2',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('ListObjectsV2', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(7, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.ListObjectsV2Result()
        self.assertIsNone(result.name)
        self.assertIsNone(result.prefix)
        self.assertIsNone(result.continuation_token)
        self.assertIsNone(result.max_keys)
        self.assertIsNone(result.delimiter)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.next_continuation_token)
        self.assertIsNone(result.encoding_type)
        self.assertIsNone(result.contents)
        self.assertIsNone(result.common_prefixes)
        self.assertIsNone(result.key_count)
        self.assertIsNone(result.start_after)
        self.assertIsInstance(result, serde.Model)

        result = model.ListObjectsV2Result(
            name='example-bucket',
            prefix='aaa',
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=998,
            delimiter='/',
            is_truncated=True,
            next_continuation_token='NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            encoding_type='url',
            contents=[model.ObjectProperties(
                key='fun/movie/001.avi',
                object_type='Normal',
                size=344606,
                etag='5B3C1A2E053D763E1B002CC607C5A0FE1****',
                last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
                storage_class='ColdArchive',
                owner=model.Owner(
                    id='0022012****',
                    display_name='user_example',
                ),
                restore_info='ongoing-request="false", expiry-date="Sat, 05 Nov 2022 07:38:08 GMT"',
                transition_time='2023-12-17T00:20:57.000Z',
            )],
            common_prefixes=[model.CommonPrefix(
                prefix='<Prefix>fun/movie/</Prefix>',
            )],
            start_after='b',
            key_count=20,
        )
        self.assertEqual('example-bucket', result.name)
        self.assertEqual('aaa', result.prefix)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.continuation_token)
        self.assertEqual(998, result.max_keys)
        self.assertEqual('/', result.delimiter)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.next_continuation_token)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual('b', result.start_after)
        self.assertEqual(20, result.key_count)
        self.assertEqual('fun/movie/001.avi', result.contents[0].key)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.contents[0].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual("5B3C1A2E053D763E1B002CC607C5A0FE1****", result.contents[0].etag)
        self.assertEqual('Normal', result.contents[0].object_type)
        self.assertEqual(344606, result.contents[0].size)
        self.assertEqual('ColdArchive', result.contents[0].storage_class)
        self.assertEqual('ongoing-request="false", expiry-date="Sat, 05 Nov 2022 07:38:08 GMT"', result.contents[0].restore_info)
        self.assertEqual('0022012****', result.contents[0].owner.id)
        self.assertEqual('user_example', result.contents[0].owner.display_name)
        self.assertEqual('<Prefix>fun/movie/</Prefix>', result.common_prefixes[0].prefix)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.contents[0].transition_time)

        result = model.ListObjectsV2Result(
            name='example-bucket',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(result, 'name'))
        self.assertEqual('example-bucket', result.name)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<ListBucketResult>
  <Name>examplebucket</Name>
  <Prefix>aaa</Prefix>
  <ContinuationToken>CgJiYw--</ContinuationToken>
  <MaxKeys>100</MaxKeys>
  <Delimiter>/</Delimiter>
  <StartAfter>b</StartAfter>
  <EncodingType>url</EncodingType>
  <IsTruncated>false</IsTruncated>
  <NextContinuationToken>NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA</NextContinuationToken>
  <Contents>
        <Key>exampleobject11.txt</Key>
        <LastModified>2020-06-22T11:42:32.000Z</LastModified>
        <ETag>"5B3C1A2E053D763E1B002CC607C5A0FE1****"</ETag>
        <Type>Normal</Type>
        <Size>344606</Size>
        <StorageClass>ColdArchive</StorageClass>
        <Owner>
            <ID>0022012****</ID>
            <DisplayName>user-example</DisplayName>
        </Owner>
        <RestoreInfo>ongoing-request="true"</RestoreInfo>
  </Contents>
  <Contents>
        <Key>exampleobject2.txt</Key>
        <LastModified>2023-12-08T08:12:20.000Z</LastModified>
        <ETag>"5B3C1A2E053D763E1B002CC607C5A0FE1****"</ETag>
        <Type>Normal2</Type>
        <Size>344607</Size>
        <StorageClass>DeepColdArchive</StorageClass>
        <Owner>
            <ID>0022012****22</ID>
            <DisplayName>user-example22</DisplayName>
        </Owner>
        <RestoreInfo>ongoing-request="false", expiry-date="Sat, 05 Nov 2022 07:38:08 GMT"</RestoreInfo>
        <TransitionTime>2023-12-08T08:12:20.000Z</TransitionTime>
  </Contents>
  <CommonPrefixes>
        <Prefix>a/b/</Prefix>
  </CommonPrefixes>
  <KeyCount>3</KeyCount>
</ListBucketResult>'''

        result = model.ListObjectsV2Result()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        self.assertEqual('examplebucket', result.name)
        self.assertEqual('aaa', result.prefix)
        self.assertEqual('CgJiYw--', result.continuation_token)
        self.assertEqual(100, result.max_keys)
        self.assertEqual('/', result.delimiter)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.next_continuation_token)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual('b', result.start_after)
        self.assertEqual(3, result.key_count)
        self.assertEqual('exampleobject11.txt', result.contents[0].key)
        self.assertEqual('2020-06-22T11:42:32.000Z', result.contents[0].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"5B3C1A2E053D763E1B002CC607C5A0FE1****"', result.contents[0].etag)
        self.assertEqual('Normal', result.contents[0].object_type)
        self.assertEqual(344606, result.contents[0].size)
        self.assertEqual('ColdArchive', result.contents[0].storage_class)
        self.assertEqual('ongoing-request="true"', result.contents[0].restore_info)
        self.assertEqual('0022012****', result.contents[0].owner.id)
        self.assertEqual('user-example', result.contents[0].owner.display_name)
        self.assertEqual('exampleobject2.txt', result.contents[1].key)
        self.assertEqual('2023-12-08T08:12:20.000Z', result.contents[1].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"5B3C1A2E053D763E1B002CC607C5A0FE1****"', result.contents[1].etag)
        self.assertEqual('Normal2', result.contents[1].object_type)
        self.assertEqual(344607, result.contents[1].size)
        self.assertEqual('DeepColdArchive', result.contents[1].storage_class)
        self.assertEqual('ongoing-request="false", expiry-date="Sat, 05 Nov 2022 07:38:08 GMT"', result.contents[1].restore_info)
        self.assertEqual('0022012****22', result.contents[1].owner.id)
        self.assertEqual('user-example22', result.contents[1].owner.display_name)
        self.assertEqual('2023-12-08T08:12:20.000Z', result.contents[1].transition_time)


class TestGetBucketStat(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketStatRequest(
            bucket='example-bucket'
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsInstance(request, serde.Model)
        self.assertEqual('example-bucket', request.bucket)

        request = model.GetBucketStatRequest(
            bucket='example-bucket',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('example-bucket', request.bucket)
        self.assertFalse(hasattr(request, 'invalid_field'))

    def test_serialize_request(self):
        request = model.GetBucketStatRequest(
            bucket='example-bucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketStat',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('GetBucketStat', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(0, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.GetBucketStatResult()
        self.assertIsNone(result.storage)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketStatResult(
            storage=1600,
            object_count=230,
            multi_part_upload_count=40,
            live_channel_count=4,
            last_modified_time=1643341269,
            standard_storage=430,
            standard_object_count=66,
            infrequent_access_storage=2359296,
            infrequent_access_real_storage=360,
            infrequent_access_object_count=54,
            archive_storage=2949120,
            archive_real_storage=450,
            archive_object_count=74,
            cold_archive_storage=2359496,
            cold_archive_real_storage=3610,
            cold_archive_object_count=36,
            deep_cold_archive_storage=23594961,
            deep_cold_archive_real_storage=10,
            deep_cold_archive_object_count=16,
            delete_marker_count=1234355467575856878,
        )
        self.assertEqual(1600, result.storage)
        self.assertEqual(230, result.object_count)
        self.assertEqual(40, result.multi_part_upload_count)
        self.assertEqual(4, result.live_channel_count)
        self.assertEqual(1643341269, result.last_modified_time)
        self.assertEqual(430, result.standard_storage)
        self.assertEqual(66, result.standard_object_count)
        self.assertEqual(2359296, result.infrequent_access_storage)
        self.assertEqual(360, result.infrequent_access_real_storage)
        self.assertEqual(54, result.infrequent_access_object_count)
        self.assertEqual(2949120, result.archive_storage)
        self.assertEqual(450, result.archive_real_storage)
        self.assertEqual(74, result.archive_object_count)
        self.assertEqual(2359496, result.cold_archive_storage)
        self.assertEqual(3610, result.cold_archive_real_storage)
        self.assertEqual(36, result.cold_archive_object_count)
        self.assertEqual(23594961, result.deep_cold_archive_storage)
        self.assertEqual(10, result.deep_cold_archive_real_storage)
        self.assertEqual(16, result.deep_cold_archive_object_count)
        self.assertEqual(1234355467575856878, result.delete_marker_count)

        result = model.GetBucketStatResult(
            storage=1600,
            object_count=230,
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(result, 'storage'))
        self.assertTrue(hasattr(result, 'object_count'))
        self.assertEqual(1600, result.storage)
        self.assertEqual(230, result.object_count)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<BucketStat>
  <Storage>1600</Storage>
  <ObjectCount>230</ObjectCount>
  <MultipartUploadCount>40</MultipartUploadCount>
  <LiveChannelCount>4</LiveChannelCount>
  <LastModifiedTime>1643341269</LastModifiedTime>
  <StandardStorage>430</StandardStorage>
  <StandardObjectCount>66</StandardObjectCount>
  <InfrequentAccessStorage>2359296</InfrequentAccessStorage>
  <InfrequentAccessRealStorage>360</InfrequentAccessRealStorage>
  <InfrequentAccessObjectCount>54</InfrequentAccessObjectCount>
  <ArchiveStorage>2949120</ArchiveStorage>
  <ArchiveRealStorage>450</ArchiveRealStorage>
  <ArchiveObjectCount>74</ArchiveObjectCount>
  <ColdArchiveStorage>2359296</ColdArchiveStorage>
  <ColdArchiveRealStorage>3610</ColdArchiveRealStorage>
  <ColdArchiveObjectCount>36</ColdArchiveObjectCount>
  <ColdArchiveStorage>2359296</ColdArchiveStorage>
  <DeepColdArchiveStorage>23594961</DeepColdArchiveStorage>
  <DeepColdArchiveRealStorage>10</DeepColdArchiveRealStorage>
  <DeepColdArchiveObjectCount>16</DeepColdArchiveObjectCount>
  <DeleteMarkerCount>1234355467575856878</DeleteMarkerCount>
</BucketStat>'''

        result = model.GetBucketStatResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual(1600, result.storage)
        self.assertEqual(230, result.object_count)
        self.assertEqual(40, result.multi_part_upload_count)
        self.assertEqual(4, result.live_channel_count)
        self.assertEqual(1643341269, result.last_modified_time)
        self.assertEqual(430, result.standard_storage)
        self.assertEqual(66, result.standard_object_count)
        self.assertEqual(2359296, result.infrequent_access_storage)
        self.assertEqual(360, result.infrequent_access_real_storage)
        self.assertEqual(54, result.infrequent_access_object_count)
        self.assertEqual(2949120, result.archive_storage)
        self.assertEqual(450, result.archive_real_storage)
        self.assertEqual(74, result.archive_object_count)
        self.assertEqual(2359296, result.cold_archive_storage)
        self.assertEqual(3610, result.cold_archive_real_storage)
        self.assertEqual(36, result.cold_archive_object_count)
        self.assertEqual(23594961, result.deep_cold_archive_storage)
        self.assertEqual(10, result.deep_cold_archive_real_storage)
        self.assertEqual(16, result.deep_cold_archive_object_count)
        self.assertEqual(1234355467575856878, result.delete_marker_count)


class TestListObjects(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListObjectsRequest(bucket='example-bucket')
        self.assertIsNotNone(request.bucket)
        self.assertIsInstance(request, serde.Model)

        request = model.ListObjectsRequest(
            bucket='example-bucket',
            delimiter='/',
            encoding_type='url',
            marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            request_payer='requester',
        )
        self.assertEqual('example-bucket', request.bucket)
        self.assertEqual('/', request.delimiter)
        self.assertEqual('url', request.encoding_type)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', request.marker)
        self.assertEqual(10, request.max_keys)
        self.assertEqual('aaa', request.prefix)
        self.assertEqual('requester', request.request_payer)

        request = model.ListObjectsRequest(
            bucket='example-bucket',
            delimiter='/',
            encoding_type='url',
            marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            request_payer='requester',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertTrue(hasattr(request, 'delimiter'))
        self.assertTrue(hasattr(request, 'encoding_type'))
        self.assertTrue(hasattr(request, 'marker'))
        self.assertTrue(hasattr(request, 'max_keys'))
        self.assertTrue(hasattr(request, 'prefix'))
        self.assertTrue(hasattr(request, 'request_payer'))
        self.assertFalse(hasattr(request, 'invalid_field'))
        self.assertEqual('example-bucket', request.bucket)



    def test_serialize_request(self):
        request = model.ListObjectsRequest(
            bucket='example-bucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListObjects',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('ListObjects', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(0, len(op_input.parameters.items()))

        request = model.ListObjectsRequest(
            bucket='example-bucket',
            delimiter='/',
            encoding_type='url',
            marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa',
            request_payer='requester'
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListObjects',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('ListObjects', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(5, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.ListObjectsResult()
        self.assertIsNone(result.name)
        self.assertIsNone(result.prefix)
        self.assertIsNone(result.marker)
        self.assertIsNone(result.max_keys)
        self.assertIsNone(result.delimiter)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.next_marker)
        self.assertIsNone(result.encoding_type)
        self.assertIsNone(result.contents)
        self.assertIsNone(result.common_prefixes)
        self.assertIsInstance(result, serde.Model)

        result = model.ListObjectsResult(
            name='example-bucket',
            prefix='aaa',
            marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=998,
            delimiter='/',
            is_truncated=True,
            next_marker='NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            encoding_type='url',
            contents=[model.ObjectProperties(
                key='fun/movie/001.avi',
                object_type='Normal',
                size=344606,
                etag='5B3C1A2E053D763E1B002CC607C5A0FE1****',
                last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
                storage_class='ColdArchive',
                owner=model.Owner(
                    id='0022012****',
                    display_name='user_example',
                ),
                restore_info='ongoing-request="false", expiry-date="Sat, 05 Nov 2022 07:38:08 GMT"',
                transition_time='2023-12-17T00:20:57.000Z',
            )],
            common_prefixes=[model.CommonPrefix(
                prefix='<Prefix>fun/movie/</Prefix>',
            )],
        )
        self.assertEqual('example-bucket', result.name)
        self.assertEqual('aaa', result.prefix)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.marker)
        self.assertEqual(998, result.max_keys)
        self.assertEqual('/', result.delimiter)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.next_marker)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual('fun/movie/001.avi', result.contents[0].key)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.contents[0].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual("5B3C1A2E053D763E1B002CC607C5A0FE1****", result.contents[0].etag)
        self.assertEqual('Normal', result.contents[0].object_type)
        self.assertEqual(344606, result.contents[0].size)
        self.assertEqual('ColdArchive', result.contents[0].storage_class)
        self.assertEqual('ongoing-request="false", expiry-date="Sat, 05 Nov 2022 07:38:08 GMT"', result.contents[0].restore_info)
        self.assertEqual('0022012****', result.contents[0].owner.id)
        self.assertEqual('user_example', result.contents[0].owner.display_name)
        self.assertEqual('<Prefix>fun/movie/</Prefix>', result.common_prefixes[0].prefix)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.contents[0].transition_time)

        result = model.ListObjectsV2Result(
            name='example-bucket',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(result, 'name'))
        self.assertEqual('example-bucket', result.name)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<ListBucketResult>
  <Name>examplebucket</Name>
  <Prefix>aaa</Prefix>
  <Marker>CgJiYw--</Marker>
  <MaxKeys>100</MaxKeys>
  <Delimiter>/</Delimiter>
  <EncodingType>url</EncodingType>
  <IsTruncated>false</IsTruncated>
  <NextMarker>NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA</NextMarker>
  <Contents>
        <Key>exampleobject11.txt</Key>
        <LastModified>2020-06-22T11:42:32.000Z</LastModified>
        <ETag>"5B3C1A2E053D763E1B002CC607C5A0FE1****"</ETag>
        <Type>Normal</Type>
        <Size>344606</Size>
        <StorageClass>ColdArchive</StorageClass>
        <Owner>
            <ID>0022012****</ID>
            <DisplayName>user-example</DisplayName>
        </Owner>
        <RestoreInfo>ongoing-request="true"</RestoreInfo>
  </Contents>
  <Contents>
        <Key>exampleobject2.txt</Key>
        <LastModified>2023-12-08T08:12:20.000Z</LastModified>
        <ETag>"5B3C1A2E053D763E1B002CC607C5A0FE1****"</ETag>
        <Type>Normal2</Type>
        <Size>344607</Size>
        <StorageClass>DeepColdArchive</StorageClass>
        <Owner>
            <ID>0022012****22</ID>
            <DisplayName>user-example22</DisplayName>
        </Owner>
        <RestoreInfo>ongoing-request="false", expiry-date="Sat, 05 Nov 2022 07:38:08 GMT"</RestoreInfo>
        <TransitionTime>2023-12-08T08:12:20.000Z</TransitionTime>
  </Contents>
  <CommonPrefixes>
        <Prefix>a/b/</Prefix>
  </CommonPrefixes>
</ListBucketResult>'''

        result = model.ListObjectsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        self.assertEqual('examplebucket', result.name)
        self.assertEqual('aaa', result.prefix)
        self.assertEqual('CgJiYw--', result.marker)
        self.assertEqual(100, result.max_keys)
        self.assertEqual('/', result.delimiter)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.next_marker)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual('exampleobject11.txt', result.contents[0].key)
        self.assertEqual('2020-06-22T11:42:32.000Z', result.contents[0].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"5B3C1A2E053D763E1B002CC607C5A0FE1****"', result.contents[0].etag)
        self.assertEqual('Normal', result.contents[0].object_type)
        self.assertEqual(344606, result.contents[0].size)
        self.assertEqual('ColdArchive', result.contents[0].storage_class)
        self.assertEqual('ongoing-request="true"', result.contents[0].restore_info)
        self.assertEqual('0022012****', result.contents[0].owner.id)
        self.assertEqual('user-example', result.contents[0].owner.display_name)
        self.assertEqual('exampleobject2.txt', result.contents[1].key)
        self.assertEqual('2023-12-08T08:12:20.000Z', result.contents[1].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"5B3C1A2E053D763E1B002CC607C5A0FE1****"', result.contents[1].etag)
        self.assertEqual('Normal2', result.contents[1].object_type)
        self.assertEqual(344607, result.contents[1].size)
        self.assertEqual('DeepColdArchive', result.contents[1].storage_class)
        self.assertEqual('ongoing-request="false", expiry-date="Sat, 05 Nov 2022 07:38:08 GMT"', result.contents[1].restore_info)
        self.assertEqual('0022012****22', result.contents[1].owner.id)
        self.assertEqual('user-example22', result.contents[1].owner.display_name)
        self.assertEqual('2023-12-08T08:12:20.000Z', result.contents[1].transition_time)


class TestGetBucketInfo(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketInfoRequest(
            bucket='example-bucket'
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsInstance(request, serde.Model)
        self.assertEqual('example-bucket', request.bucket)

        request = model.GetBucketInfoRequest(
            bucket='example-bucket',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('example-bucket', request.bucket)
        self.assertFalse(hasattr(request, 'invalid_field'))

    def test_serialize_request(self):
        request = model.GetBucketInfoRequest(
            bucket='example-bucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketInfo',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('GetBucketInfo', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(0, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.GetBucketInfoResult()
        self.assertIsNone(result.bucket_info)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketInfoResult(
            bucket_info=model.BucketInfo(
                name='oss-example',
                access_monitor='Enabled',
                location='oss-cn-hangzhou',
                creation_date='2013-07-31T10:56:21.000Z',
                extranet_endpoint='oss-cn-hangzhou.aliyuncs.com',
                intranet_endpoint='oss-cn-hangzhou-internal.aliyuncs.com',
                acl='private',
                data_redundancy_type='LRS',
                owner=model.Owner(
                    id='0022012****',
                    display_name='user_example',
                ),
                storage_class='Standard',
                resource_group_id='rg-aek27tc********',
                sse_rule=model.SSERule(
                    kms_master_key_id='0022012****',
                    sse_algorithm='user_example',
                    kms_data_encryption='user_example',
                ),
                versioning='Enabled',
                transfer_acceleration='Disabled',
                cross_region_replication='Disabled',
                bucket_policy=model.BucketPolicy(
                    log_bucket='0022012****',
                    log_prefix='user_example',
                ),
                comment='comment test',
                block_public_access=True,
            ),
        )

        self.assertEqual('oss-example', result.bucket_info.name)
        self.assertEqual('Enabled', result.bucket_info.access_monitor)
        self.assertEqual('oss-cn-hangzhou', result.bucket_info.location)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.bucket_info.creation_date)
        self.assertEqual('oss-cn-hangzhou.aliyuncs.com', result.bucket_info.extranet_endpoint)
        self.assertEqual('oss-cn-hangzhou-internal.aliyuncs.com', result.bucket_info.intranet_endpoint)
        self.assertEqual('private', result.bucket_info.acl)
        self.assertEqual('LRS', result.bucket_info.data_redundancy_type)
        self.assertEqual('0022012****', result.bucket_info.owner.id)
        self.assertEqual('user_example', result.bucket_info.owner.display_name)
        self.assertEqual('Standard', result.bucket_info.storage_class)
        self.assertEqual('rg-aek27tc********', result.bucket_info.resource_group_id)
        self.assertEqual('0022012****', result.bucket_info.sse_rule.kms_master_key_id)
        self.assertEqual('user_example', result.bucket_info.sse_rule.sse_algorithm)
        self.assertEqual('user_example', result.bucket_info.sse_rule.kms_data_encryption)
        self.assertEqual('Enabled', result.bucket_info.versioning)
        self.assertEqual('Disabled', result.bucket_info.transfer_acceleration)
        self.assertEqual('Disabled', result.bucket_info.cross_region_replication)
        self.assertEqual('0022012****', result.bucket_info.bucket_policy.log_bucket)
        self.assertEqual('user_example', result.bucket_info.bucket_policy.log_prefix)
        self.assertEqual('comment test', result.bucket_info.comment)
        self.assertEqual(True, result.bucket_info.block_public_access)

        result = model.GetBucketInfoResult(
            bucket_info=model.BucketInfo(
                name='oss-example',
                access_monitor='Enabled',
                invalid_field='invalid_field'
            )
        )
        self.assertTrue(hasattr(result.bucket_info, 'name'))
        self.assertTrue(hasattr(result.bucket_info, 'access_monitor'))
        self.assertEqual('oss-example', result.bucket_info.name)
        self.assertEqual('Enabled', result.bucket_info.access_monitor)
        self.assertFalse(hasattr(result.bucket_info, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<BucketInfo>
  <Bucket>
    <AccessMonitor>Enabled</AccessMonitor>
    <CreationDate>2013-07-31T10:56:21.000Z</CreationDate>
    <ExtranetEndpoint>oss-cn-hangzhou.aliyuncs.com</ExtranetEndpoint>
    <IntranetEndpoint>oss-cn-hangzhou-internal.aliyuncs.com</IntranetEndpoint>
    <Location>oss-cn-hangzhou</Location>
    <StorageClass>Standard</StorageClass>
    <TransferAcceleration>Disabled</TransferAcceleration>
    <CrossRegionReplication>Disabled</CrossRegionReplication>
    <DataRedundancyType>LRS</DataRedundancyType>
    <Name>oss-example</Name>
    <ResourceGroupId>rg-aek27tc********</ResourceGroupId>
    <Owner>
      <DisplayName>username</DisplayName>
      <ID>27183473914****</ID>
    </Owner>
    <AccessControlList>
      <Grant>private</Grant>
    </AccessControlList> 
    <ServerSideEncryptionRule>
        <SSEAlgorithm>KMS</SSEAlgorithm>
        <KMSMasterKeyID>shUhih687675***32edghadg</KMSMasterKeyID>
        <KMSDataEncryption>SM4</KMSDataEncryption>
    </ServerSideEncryptionRule>
    <BucketPolicy>
      <LogBucket>examplebucket</LogBucket>
      <LogPrefix>log/</LogPrefix>
    </BucketPolicy>
    <Comment>test</Comment>
    <Versioning>Enabled</Versioning>
    <BlockPublicAccess>true</BlockPublicAccess>
  </Bucket>
</BucketInfo>'''

        result = model.GetBucketInfoResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual('oss-example', result.bucket_info.name)
        self.assertEqual('Enabled', result.bucket_info.access_monitor)
        self.assertEqual('oss-cn-hangzhou', result.bucket_info.location)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.bucket_info.creation_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('oss-cn-hangzhou.aliyuncs.com', result.bucket_info.extranet_endpoint)
        self.assertEqual('oss-cn-hangzhou-internal.aliyuncs.com', result.bucket_info.intranet_endpoint)
        self.assertEqual('private', result.bucket_info.acl)
        self.assertEqual('LRS', result.bucket_info.data_redundancy_type)
        self.assertEqual('27183473914****', result.bucket_info.owner.id)
        self.assertEqual('username', result.bucket_info.owner.display_name)
        self.assertEqual('Standard', result.bucket_info.storage_class)
        self.assertEqual('rg-aek27tc********', result.bucket_info.resource_group_id)
        self.assertEqual('shUhih687675***32edghadg', result.bucket_info.sse_rule.kms_master_key_id)
        self.assertEqual('KMS', result.bucket_info.sse_rule.sse_algorithm)
        self.assertEqual('SM4', result.bucket_info.sse_rule.kms_data_encryption)
        self.assertEqual('Enabled', result.bucket_info.versioning)
        self.assertEqual('Disabled', result.bucket_info.transfer_acceleration)
        self.assertEqual('Disabled', result.bucket_info.cross_region_replication)
        self.assertEqual('KMS', result.bucket_info.sse_rule.sse_algorithm)
        self.assertEqual('shUhih687675***32edghadg', result.bucket_info.sse_rule.kms_master_key_id)
        self.assertEqual('SM4', result.bucket_info.sse_rule.kms_data_encryption)
        self.assertEqual('examplebucket', result.bucket_info.bucket_policy.log_bucket)
        self.assertEqual('log/', result.bucket_info.bucket_policy.log_prefix)
        self.assertEqual('test', result.bucket_info.comment)
        self.assertEqual(True, result.bucket_info.block_public_access)


class TestGetBucketLocation(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketLocationRequest(
            bucket='example-bucket'
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsInstance(request, serde.Model)
        self.assertEqual('example-bucket', request.bucket)

        request = model.GetBucketLocationRequest(
            bucket='example-bucket',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('example-bucket', request.bucket)
        self.assertFalse(hasattr(request, 'invalid_field'))

    def test_serialize_request(self):
        request = model.GetBucketLocationRequest(
            bucket='example-bucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketLocation',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('GetBucketLocation', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(0, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.GetBucketLocationResult()
        self.assertIsNone(result.location)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketLocationResult(
            location='oss-cn-hangzhou',
        )

        self.assertEqual('oss-cn-hangzhou', result.location)

        result = model.GetBucketLocationResult(
            location='oss-cn-hangzhou',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(result, 'location'))
        self.assertEqual('oss-cn-hangzhou', result.location)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<LocationConstraint>oss-cn-hangzhou</LocationConstraint >'''

        result = model.GetBucketLocationResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual('oss-cn-hangzhou', result.location)


class TestPutBucketVersioning(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketVersioningRequest(bucket='example-bucket')
        self.assertIsNotNone(request.bucket)
        self.assertIsNone(request.versioning_configuration)
        self.assertIsInstance(request, serde.Model)

        request = model.PutBucketVersioningRequest(
            bucket='example-bucket',
            versioning_configuration=model.VersioningConfiguration(
                status='Enabled'
            )
        )
        self.assertEqual('example-bucket', request.bucket)
        self.assertEqual('Enabled', request.versioning_configuration.status)

        request = model.PutBucketVersioningRequest(
            bucket='example-bucket',
            versioning_configuration=model.VersioningConfiguration(
                status='Enabled'
            ),
            invalid_field='invalid_field',
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('example-bucket', request.bucket)
        self.assertTrue(hasattr(request.versioning_configuration, 'status'))
        self.assertEqual('Enabled', request.versioning_configuration.status)
        self.assertFalse(hasattr(request, 'invalid_field'))


    def test_serialize_request(self):
        request = model.PutBucketVersioningRequest(
            bucket='example-bucket',
            versioning_configuration=model.VersioningConfiguration(
                status='Enabled'
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketVersioning',
            method='PUT',
            bucket=request.bucket,
        ))

        xml_data = r'''<VersioningConfiguration><Status>Enabled</Status></VersioningConfiguration>'''

        self.assertEqual('PutBucketVersioning', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(xml_data.encode(), op_input.body)
        self.assertEqual(0, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.PutBucketVersioningResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketVersioningResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123'
                }),
                http_response=MockHttpResponse(
                    status_code=200,
                    reason='OK',
                    headers={'x-oss-request-id': 'id-1234'},
                    body=xml_data,
                )
            )
        )
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)


class TestGetBucketVersioning(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketVersioningRequest(
            bucket='example-bucket'
        )
        self.assertIsNotNone(request.bucket)
        self.assertIsInstance(request, serde.Model)
        self.assertEqual('example-bucket', request.bucket)

        request = model.GetBucketVersioningRequest(
            bucket='example-bucket',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertEqual('example-bucket', request.bucket)
        self.assertFalse(hasattr(request, 'invalid_field'))

    def test_serialize_request(self):
        request = model.GetBucketVersioningRequest(
            bucket='example-bucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketVersioning',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('GetBucketVersioning', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(0, len(op_input.parameters.items()))

    def test_constructor_result(self):
        result = model.GetBucketVersioningResult()
        self.assertIsNone(result.version_status)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketVersioningResult(
            version_status='Enabled',
        )

        self.assertEqual('Enabled', result.version_status)

        result = model.GetBucketVersioningResult(
            version_status='Enabled',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(result, 'version_status'))
        self.assertEqual('Enabled', result.version_status)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<VersioningConfiguration>
    <Status>Enabled</Status>
</VersioningConfiguration>'''

        result = model.GetBucketVersioningResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual('Enabled', result.version_status)


class TestListObjectVersions(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListObjectVersionsRequest(
            bucket='example-bucket',
            delimiter='/',
            encoding_type='url',
            key_marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            version_id_marker='CAEQMxiBgICbof2D0BYiIGRhZjgwMzJiMjA3MjQ0ODE5MWYxZDYwMzJlZjU1****',
            max_keys=10,
            prefix='aaa',
            request_payer='requester',
        )
        self.assertEqual('example-bucket', request.bucket)
        self.assertEqual('/', request.delimiter)
        self.assertEqual('url', request.encoding_type)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', request.key_marker)
        self.assertEqual('CAEQMxiBgICbof2D0BYiIGRhZjgwMzJiMjA3MjQ0ODE5MWYxZDYwMzJlZjU1****', request.version_id_marker)
        self.assertEqual(10, request.max_keys)
        self.assertEqual('aaa', request.prefix)
        self.assertEqual('requester', request.request_payer)

        request = model.ListObjectVersionsRequest(
            bucket='example-bucket',
            delimiter='/',
            encoding_type='url',
            key_marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            version_id_marker='CAEQMxiBgICbof2D0BYiIGRhZjgwMzJiMjA3MjQ0ODE5MWYxZDYwMzJlZjU1****',
            max_keys=10,
            prefix='aaa',
            request_payer='requester',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(request, 'bucket'))
        self.assertTrue(hasattr(request, 'delimiter'))
        self.assertTrue(hasattr(request, 'encoding_type'))
        self.assertTrue(hasattr(request, 'key_marker'))
        self.assertTrue(hasattr(request, 'version_id_marker'))
        self.assertTrue(hasattr(request, 'max_keys'))
        self.assertTrue(hasattr(request, 'prefix'))
        self.assertTrue(hasattr(request, 'request_payer'))
        self.assertFalse(hasattr(request, 'invalid_field'))
        self.assertEqual('example-bucket', request.bucket)

    def test_serialize_request(self):
        request = model.ListObjectVersionsRequest(
            bucket='example-bucket',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListObjectVersions',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('ListObjectVersions', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(0, len(op_input.parameters.items()))

        request = model.ListObjectVersionsRequest(
            bucket='example-bucket',
            delimiter='/',
            encoding_type='url',
            key_marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            version_id_marker='CAEQMxiBgICbof2D0BYiIGRhZjgwMzJiMjA3MjQ0ODE5MWYxZDYwMzJlZjU1****',
            max_keys=10,
            prefix='aaa',
            request_payer='requester'
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListObjectVersions',
            method='GET',
            bucket=request.bucket,
        ))

        self.assertEqual('ListObjectVersions', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('example-bucket', op_input.bucket)
        self.assertEqual(6, len(op_input.parameters.items()))


    def test_constructor_result(self):
        result = model.ListObjectVersionsResult()
        self.assertIsNone(result.name)
        self.assertIsNone(result.key_marker)
        self.assertIsNone(result.next_key_marker)
        self.assertIsNone(result.version_id_marker)
        self.assertIsNone(result.next_version_id_marker)
        self.assertIsNone(result.prefix)
        self.assertIsNone(result.delimiter)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.encoding_type)
        self.assertIsNone(result.version)
        self.assertIsNone(result.delete_marker)
        self.assertIsNone(result.common_prefixes)
        self.assertIsInstance(result, serde.Model)

        result = model.ListObjectVersionsResult(
            name='demo-bucket',
            prefix='demo%2F',
            key_marker='',
            version_id_marker='',
            max_keys=20,
            delimiter='%2F',
            encoding_type='url',
            is_truncated=True,
            next_key_marker='demo%2FREADME-CN.md',
            next_version_id_marker='CAEQEhiBgICDzK6NnBgiIGRlZWJhYmNlMGUxZDQ4YTZhNTU2MzM4Mzk5NDBl****',
            version=[model.ObjectVersionProperties(
                key='demo%2FREADME-CN.md',
                version_id='CAEQEhiBgICDzK6NnBgiIGRlZWJhYmNlMGUxZDQ4YTZhNTU2MzM4Mzk5NDBl****',
                is_latest=False,
                last_modified=datetime.datetime.fromtimestamp(1702743657, datetime.timezone.utc),
                etag='"E317049B40462DE37C422CE4FC1B****"',
                object_type='Normal',
                size=2943,
                storage_class='Standard',
                owner=model.Owner(
                    id='150692521021****',
                    display_name='160692521021****',
                ),
                restore_info='ongoing-request="false", expiry-date="Thu, 24 Sep 2020 12:40:33 GMT"',
            ),
            model.ObjectVersionProperties(
                key='example-object-2.jpg',
                version_id='',
                is_latest=True,
                last_modified=datetime.datetime.fromtimestamp(1702733657, datetime.timezone.utc),
                etag='5B3C1A2E053D763E1B002CC607C5A0FE1****',
                size=20,
                storage_class='STANDARD',
                owner=model.Owner(
                    id='1250000000',
                    display_name='1250000000',
                ),
                restore_info='ongoing-request="true"',
                transition_time='2023-12-17T00:20:57.000Z',
            )],
            delete_marker=[model.DeleteMarkerProperties(
                key='demo%2FREADME-CN.md',
                version_id='CAEQFBiCgID3.86GohgiIDc4ZTE0NTNhZTc5MDQxYzBhYTU5MjY1ZDFjNGJm****',
                is_latest=True,
                last_modified=datetime.datetime.fromtimestamp(1702755657, datetime.timezone.utc),
                owner=model.Owner(
                    id='150692521021****',
                    display_name='350692521021****',
                ),
            ),
            model.DeleteMarkerProperties(
                key='demo%2FLICENSE',
                version_id='CAEQFBiBgMD0.86GohgiIGZmMmFlM2UwNjdlMzRiMGFhYjk4MjM1ZGUyZDY0****',
                is_latest=True,
                last_modified=datetime.datetime.fromtimestamp(1702743377, datetime.timezone.utc),
                owner=model.Owner(
                    id='150692521021****',
                    display_name='250692521021****',
                ),
            )],
            common_prefixes=[model.CommonPrefix(
                prefix='demo%2F.git%2F',
            ),
            model.CommonPrefix(
                prefix='demo%2F.idea%2F',
            )],
        )

        self.assertEqual('demo-bucket', result.name)
        self.assertEqual('demo%2F', result.prefix)
        self.assertEqual('', result.key_marker)
        self.assertEqual('', result.version_id_marker)
        self.assertEqual(20, result.max_keys)
        self.assertEqual('%2F', result.delimiter)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('demo%2FREADME-CN.md', result.next_key_marker)
        self.assertEqual('CAEQEhiBgICDzK6NnBgiIGRlZWJhYmNlMGUxZDQ4YTZhNTU2MzM4Mzk5NDBl****',result.next_version_id_marker)
        self.assertEqual('demo%2FREADME-CN.md', result.version[0].key)
        self.assertEqual('CAEQEhiBgICDzK6NnBgiIGRlZWJhYmNlMGUxZDQ4YTZhNTU2MzM4Mzk5NDBl****',result.version[0].version_id)
        self.assertEqual(False, result.version[0].is_latest)
        self.assertEqual('2023-12-16T16:20:57.000Z', result.version[0].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"E317049B40462DE37C422CE4FC1B****"', result.version[0].etag)
        self.assertEqual('Normal', result.version[0].object_type)
        self.assertEqual(2943, result.version[0].size)
        self.assertEqual('Standard', result.version[0].storage_class)
        self.assertEqual('150692521021****', result.version[0].owner.id)
        self.assertEqual('160692521021****', result.version[0].owner.display_name)
        self.assertEqual('ongoing-request="false", expiry-date="Thu, 24 Sep 2020 12:40:33 GMT"',result.version[0].restore_info)
        self.assertEqual('example-object-2.jpg', result.version[1].key)
        self.assertEqual('', result.version[1].version_id)
        self.assertEqual(True, result.version[1].is_latest)
        self.assertEqual('2023-12-16T13:34:17.000Z', result.version[1].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('5B3C1A2E053D763E1B002CC607C5A0FE1****', result.version[1].etag)
        self.assertEqual(20, result.version[1].size)
        self.assertEqual('STANDARD', result.version[1].storage_class)
        self.assertEqual('1250000000', result.version[1].owner.id)
        self.assertEqual('1250000000', result.version[1].owner.display_name)
        self.assertEqual('ongoing-request="true"',result.version[1].restore_info)
        self.assertEqual('demo%2FREADME-CN.md', result.delete_marker[0].key)
        self.assertEqual('CAEQFBiCgID3.86GohgiIDc4ZTE0NTNhZTc5MDQxYzBhYTU5MjY1ZDFjNGJm****',result.delete_marker[0].version_id)
        self.assertEqual(True, result.delete_marker[0].is_latest)
        self.assertEqual('2023-12-16T19:40:57.000Z', result.delete_marker[0].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('150692521021****', result.delete_marker[0].owner.id)
        self.assertEqual('350692521021****', result.delete_marker[0].owner.display_name)
        self.assertEqual('demo%2FLICENSE', result.delete_marker[1].key)
        self.assertEqual('CAEQFBiBgMD0.86GohgiIGZmMmFlM2UwNjdlMzRiMGFhYjk4MjM1ZGUyZDY0****',result.delete_marker[1].version_id)
        self.assertEqual(True, result.delete_marker[1].is_latest)
        self.assertEqual('2023-12-16T16:16:17.000Z', result.delete_marker[1].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('150692521021****', result.delete_marker[1].owner.id)
        self.assertEqual('250692521021****', result.delete_marker[1].owner.display_name)
        self.assertEqual('demo%2F.git%2F', result.common_prefixes[0].prefix)
        self.assertEqual('demo%2F.idea%2F', result.common_prefixes[1].prefix)
        self.assertEqual('2023-12-17T00:20:57.000Z', result.version[1].transition_time)

        result = model.ListObjectVersionsResult(
            version_id_marker='BgICDzK6NnBgiIGRlZWJhY',
            invalid_field='invalid_field'
        )
        self.assertTrue(hasattr(result, 'version_id_marker'))
        self.assertEqual('BgICDzK6NnBgiIGRlZWJhY', result.version_id_marker)
        self.assertFalse(hasattr(result, 'invalid_field'))

    def test_deserialize_result(self):
        xml_data = r'''
<ListVersionsResult>
<Name>demo-bucket</Name>
  <Prefix>demo%2F</Prefix>
  <KeyMarker></KeyMarker>
  <VersionIdMarker></VersionIdMarker>
  <MaxKeys>20</MaxKeys>
  <Delimiter>%2F</Delimiter>
  <EncodingType>url</EncodingType>
  <IsTruncated>true</IsTruncated>
  <NextKeyMarker>demo%2FREADME-CN.md</NextKeyMarker>
  <NextVersionIdMarker>CAEQEhiBgICDzK6NnBgiIGRlZWJhYmNlMGUxZDQ4YTZhNTU2MzM4Mzk5NDBl****</NextVersionIdMarker>
    <Version>
    <Key>demo%2FREADME-CN.md</Key>
    <VersionId>CAEQEhiBgICDzK6NnBgiIGRlZWJhYmNlMGUxZDQ4YTZhNTU2MzM4Mzk5NDBl****</VersionId>
    <IsLatest>false</IsLatest>
    <LastModified>2022-09-28T09:04:39.000Z</LastModified>
    <ETag>"E317049B40462DE37C422CE4FC1B****"</ETag>
    <Type>Normal</Type>
    <Size>2943</Size>
    <StorageClass>Standard</StorageClass>
    <Owner>
      <ID>150692521021****</ID>
      <DisplayName>160692521021****</DisplayName>
    </Owner>
    <RestoreInfo>ongoing-request="false", expiry-date="Thu, 24 Sep 2020 12:40:33 GMT"</RestoreInfo>
    </Version>
    <Version>
        <Key>example-object-2.jpg</Key>
        <VersionId/>
        <IsLatest>true</IsLatest>
        <LastModified>2019-08-09T12:03:09.000Z</LastModified>
        <ETag>5B3C1A2E053D763E1B002CC607C5A0FE1****</ETag>
        <Size>20</Size>
        <StorageClass>STANDARD</StorageClass>
        <Owner>
            <ID>1250000000</ID>
            <DisplayName>1250000000</DisplayName>
        </Owner>
        <RestoreInfo>ongoing-request="true"</RestoreInfo>
        <TransitionTime>2023-12-08T08:12:20.000Z</TransitionTime>
    </Version>
  <DeleteMarker>
    <Key>demo%2FREADME-CN.md</Key>
    <VersionId>CAEQFBiCgID3.86GohgiIDc4ZTE0NTNhZTc5MDQxYzBhYTU5MjY1ZDFjNGJm****</VersionId>
    <IsLatest>true</IsLatest>
    <LastModified>2022-11-04T08:00:06.000Z</LastModified>
    <Owner>
      <ID>150692521021****</ID>
      <DisplayName>350692521021****</DisplayName>
    </Owner>
  </DeleteMarker>
  <DeleteMarker>
      <Key>demo%2FLICENSE</Key>
      <VersionId>CAEQFBiBgMD0.86GohgiIGZmMmFlM2UwNjdlMzRiMGFhYjk4MjM1ZGUyZDY0****</VersionId>
      <IsLatest>true</IsLatest>
      <LastModified>2022-11-04T08:00:06.000Z</LastModified>
      <Owner>
        <ID>150692521021****</ID>
        <DisplayName>250692521021****</DisplayName>
      </Owner>
  </DeleteMarker>
    <CommonPrefixes>
      <Prefix>demo%2F.git%2F</Prefix>
    </CommonPrefixes>
    <CommonPrefixes>
      <Prefix>demo%2F.idea%2F</Prefix>
    </CommonPrefixes>

</ListVersionsResult>'''

        result = model.ListObjectVersionsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual('demo-bucket', result.name)
        self.assertEqual('demo%2F', result.prefix)
        self.assertEqual(None, result.key_marker)
        self.assertEqual(None, result.version_id_marker)
        self.assertEqual(20, result.max_keys)
        self.assertEqual('%2F', result.delimiter)
        self.assertEqual('url', result.encoding_type)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('demo%2FREADME-CN.md', result.next_key_marker)
        self.assertEqual('CAEQEhiBgICDzK6NnBgiIGRlZWJhYmNlMGUxZDQ4YTZhNTU2MzM4Mzk5NDBl****',result.next_version_id_marker)
        self.assertEqual('demo%2FREADME-CN.md', result.version[0].key)
        self.assertEqual('CAEQEhiBgICDzK6NnBgiIGRlZWJhYmNlMGUxZDQ4YTZhNTU2MzM4Mzk5NDBl****',result.version[0].version_id)
        self.assertEqual(False, result.version[0].is_latest)
        self.assertEqual('2022-09-28T09:04:39.000Z', result.version[0].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('"E317049B40462DE37C422CE4FC1B****"', result.version[0].etag)
        self.assertEqual('Normal', result.version[0].object_type)
        self.assertEqual(2943, result.version[0].size)
        self.assertEqual('Standard', result.version[0].storage_class)
        self.assertEqual('150692521021****', result.version[0].owner.id)
        self.assertEqual('160692521021****', result.version[0].owner.display_name)
        self.assertEqual('ongoing-request="false", expiry-date="Thu, 24 Sep 2020 12:40:33 GMT"',result.version[0].restore_info)
        self.assertEqual('example-object-2.jpg', result.version[1].key)
        self.assertEqual(None, result.version[1].version_id)
        self.assertEqual(True, result.version[1].is_latest)
        self.assertEqual('2019-08-09T12:03:09.000Z', result.version[1].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('5B3C1A2E053D763E1B002CC607C5A0FE1****', result.version[1].etag)
        self.assertEqual(20, result.version[1].size)
        self.assertEqual('STANDARD', result.version[1].storage_class)
        self.assertEqual('1250000000', result.version[1].owner.id)
        self.assertEqual('1250000000', result.version[1].owner.display_name)
        self.assertEqual('ongoing-request="true"', result.version[1].restore_info)
        self.assertEqual('demo%2FREADME-CN.md', result.delete_marker[0].key)
        self.assertEqual('CAEQFBiCgID3.86GohgiIDc4ZTE0NTNhZTc5MDQxYzBhYTU5MjY1ZDFjNGJm****',result.delete_marker[0].version_id)
        self.assertEqual(True, result.delete_marker[0].is_latest)
        self.assertEqual('2022-11-04T08:00:06.000Z',result.delete_marker[0].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('150692521021****', result.delete_marker[0].owner.id)
        self.assertEqual('350692521021****', result.delete_marker[0].owner.display_name)
        self.assertEqual('demo%2FLICENSE', result.delete_marker[1].key)
        self.assertEqual('CAEQFBiBgMD0.86GohgiIGZmMmFlM2UwNjdlMzRiMGFhYjk4MjM1ZGUyZDY0****',result.delete_marker[1].version_id)
        self.assertEqual(True, result.delete_marker[1].is_latest)
        self.assertEqual('2022-11-04T08:00:06.000Z',result.delete_marker[1].last_modified.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        self.assertEqual('150692521021****', result.delete_marker[1].owner.id)
        self.assertEqual('250692521021****', result.delete_marker[1].owner.display_name)
        self.assertEqual('demo%2F.git%2F', result.common_prefixes[0].prefix)
        self.assertEqual('demo%2F.idea%2F', result.common_prefixes[1].prefix)
        self.assertEqual('2023-12-08T08:12:20.000Z', result.version[1].transition_time)