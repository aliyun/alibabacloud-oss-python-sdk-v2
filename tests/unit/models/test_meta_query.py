# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_meta_query as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestOpenMetaQuery(unittest.TestCase):
    def test_constructor_request(self):
        request = model.OpenMetaQueryRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.OpenMetaQueryRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.OpenMetaQueryRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='OpenMetaQuery',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('OpenMetaQuery', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.OpenMetaQueryResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.OpenMetaQueryResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
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
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestGetMetaQueryStatus(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetMetaQueryStatusRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetMetaQueryStatusRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetMetaQueryStatusRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetMetaQueryStatus',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetMetaQueryStatus', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetMetaQueryStatusResult()
        self.assertIsNone(result.meta_query_status)
        self.assertIsInstance(result, serde.Model)

        result = model.GetMetaQueryStatusResult(
            meta_query_status=model.MetaQueryStatus(
                create_time='2024-09-11T10:49:17.289372919+08:00',
                update_time='2024-09-11T10:49:17.289372919+08:00',
                state='Running',
                phase='FullScanning',
            ),
        )
        self.assertEqual('2024-09-11T10:49:17.289372919+08:00', result.meta_query_status.create_time)
        self.assertEqual('2024-09-11T10:49:17.289372919+08:00', result.meta_query_status.update_time)
        self.assertEqual('Running', result.meta_query_status.state)
        self.assertEqual('FullScanning', result.meta_query_status.phase)

    def test_deserialize_result(self):
        xml_data = r'''
        <MetaQueryStatus>
        </MetaQueryStatus>'''

        result = model.GetMetaQueryStatusResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <MetaQueryStatus>
          <State>Running</State>
          <Phase>FullScanning</Phase>
          <CreateTime>2024-09-11T10:49:17.289372919+08:00</CreateTime>
          <UpdateTime>2024-09-11T10:49:17.289372919+08:00</UpdateTime>
          <MetaQueryMode>basic</MetaQueryMode>
        </MetaQueryStatus>
        '''

        result = model.GetMetaQueryStatusResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('Running', result.meta_query_status.state)
        self.assertEqual('FullScanning', result.meta_query_status.phase)
        self.assertEqual('2024-09-11T10:49:17.289372919+08:00', result.meta_query_status.create_time)
        self.assertEqual('2024-09-11T10:49:17.289372919+08:00', result.meta_query_status.update_time)
        self.assertEqual('basic', result.meta_query_status.meta_query_mode)



class TestCloseMetaQuery(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CloseMetaQueryRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CloseMetaQueryRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.CloseMetaQueryRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CloseMetaQuery',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CloseMetaQuery', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.CloseMetaQueryResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.CloseMetaQueryResult()
        serde.deserialize_output(
            result,
            OperationOutput(
                status='OK',
                status_code=200,
                headers=CaseInsensitiveDict({
                    'x-oss-request-id': '123',
                    'x-oss-hash-crc64ecma': '316181249502703****',
                    'x-oss-version-id': 'CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****',
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
        self.assertEqual('316181249502703****', result.headers.get('x-oss-hash-crc64ecma'))
        self.assertEqual('CAEQNhiBgMDJgZCA0BYiIDc4MGZjZGI2OTBjOTRmNTE5NmU5NmFhZjhjYmY0****', result.headers.get('x-oss-version-id'))


class TestDoMetaQuery(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DoMetaQueryRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.meta_query)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DoMetaQueryRequest(
            bucket='bucketexampletest',
            meta_query=model.MetaQuery(
                aggregations=model.MetaQueryAggregations(
                    aggregations=[model.MetaQueryAggregation(
                        field='Size',
                        operation='sum',
                    ), model.MetaQueryAggregation(
                        field='Size',
                        operation='max',
                    )],
                ),
                next_token='MTIzNDU2Nzg6aW1tdGVzdDpleGFtcGxlYnVja2V0OmRhdGFzZXQwMDE6b3NzOi8vZXhhbXBsZWJ1Y2tldC9zYW1wbGVvYmplY3QxLmpw****',
                max_results=78520,
                query='{"Field": "Size","Value": "1048576","Operation": "gt"}',
                sort='Size',
                order=model.MetaQueryOrderType.DESC,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('Size', request.meta_query.aggregations.aggregations[0].field)
        self.assertEqual('sum', request.meta_query.aggregations.aggregations[0].operation)
        self.assertEqual('Size', request.meta_query.aggregations.aggregations[1].field)
        self.assertEqual('max', request.meta_query.aggregations.aggregations[1].operation)
        self.assertEqual('MTIzNDU2Nzg6aW1tdGVzdDpleGFtcGxlYnVja2V0OmRhdGFzZXQwMDE6b3NzOi8vZXhhbXBsZWJ1Y2tldC9zYW1wbGVvYmplY3QxLmpw****', request.meta_query.next_token)
        self.assertEqual(78520, request.meta_query.max_results)
        self.assertEqual('{"Field": "Size","Value": "1048576","Operation": "gt"}', request.meta_query.query)
        self.assertEqual('Size', request.meta_query.sort)
        self.assertEqual('desc', request.meta_query.order)

        request = model.DoMetaQueryRequest(
            bucket='bucketexampletest2',
            meta_query=model.MetaQuery(
                aggregations=model.MetaQueryAggregations(
                    aggregations=[model.MetaQueryAggregation(
                        field='Filename',
                        operation='group',
                    ), model.MetaQueryAggregation(
                        field='FileModifiedTime',
                        operation='min',
                    )],
                ),
                next_token='MTIzNDU2Nzg6aW1tdGVzdDpleGFtcGxlYnVja2V0OmRhdGFzZXQwMDE6b3NzOi8vZXhhbXBsZWJ1Y2tldC9zYW1wbGVvYmplY3QxLmpw****',
                max_results=25119,
                query='{"Operation":"gt", "Field": "Size", "Value": "30"}',
                sort='OSSStorageClass',
                order='desc',
            ),
        )
        self.assertEqual('bucketexampletest2', request.bucket)
        self.assertEqual('Filename', request.meta_query.aggregations.aggregations[0].field)
        self.assertEqual('group', request.meta_query.aggregations.aggregations[0].operation)
        self.assertEqual('FileModifiedTime', request.meta_query.aggregations.aggregations[1].field)
        self.assertEqual('min', request.meta_query.aggregations.aggregations[1].operation)
        self.assertEqual('MTIzNDU2Nzg6aW1tdGVzdDpleGFtcGxlYnVja2V0OmRhdGFzZXQwMDE6b3NzOi8vZXhhbXBsZWJ1Y2tldC9zYW1wbGVvYmplY3QxLmpw****', request.meta_query.next_token)
        self.assertEqual(25119, request.meta_query.max_results)
        self.assertEqual('{"Operation":"gt", "Field": "Size", "Value": "30"}', request.meta_query.query)
        self.assertEqual('OSSStorageClass', request.meta_query.sort)
        self.assertEqual('desc', request.meta_query.order)

    def test_serialize_request(self):
        request = model.DoMetaQueryRequest(
            bucket='bucketexampletest',
            meta_query=model.MetaQuery(
                aggregations=model.MetaQueryAggregations(
                    aggregations=[model.MetaQueryAggregation(
                        field='Size',
                        operation='sum',
                    ), model.MetaQueryAggregation(
                        field='Size',
                        operation='max',
                    )],
                ),
                next_token='MTIzNDU2Nzg6aW1tdGVzdDpleGFtcGxlYnVja2V0OmRhdGFzZXQwMDE6b3NzOi8vZXhhbXBsZWJ1Y2tldC9zYW1wbGVvYmplY3QxLmpw****',
                max_results=78520,
                query='{"Field": "Size","Value": "1048576","Operation": "gt"}',
                sort='Size',
                order=model.MetaQueryOrderType.ASC,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DoMetaQuery',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('DoMetaQuery', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DoMetaQueryResult()
        self.assertIsNone(result.files)
        self.assertIsNone(result.aggregations)
        self.assertIsNone(result.next_token)
        self.assertIsInstance(result, serde.Model)

        result = model.DoMetaQueryResult(
            files=model.MetaQueryFiles(
                file=model.MetaQueryFile(
                    file_modified_time='2021-06-29T15:04:05.000000000Z07:00',
                    etag='"fba9dede5f27731c9771645a3986****"',
                    server_side_encryption='SM4',
                    oss_tagging_count=4993,
                    oss_tagging=model.MetaQueryOSSTagging(
                        taggings=[model.MetaQueryTagging(
                            key='owner',
                            value='John',
                        ), model.MetaQueryTagging(
                            key='owner',
                            value='Jack',
                        )],
                    ),
                    oss_user_meta=model.MetaQueryOSSUserMeta(
                        user_metas=[model.MetaQueryUserMeta(
                            key='x-oss-meta-location',
                            value='hangzhou',
                        ), model.MetaQueryUserMeta(
                            key='x-oss-meta-location',
                            value='shanghai',
                        )],
                    ),
                    filename='exampleobject.txt',
                    size=344606,
                    oss_object_type='Normal',
                    oss_storage_class='Standard',
                    object_acl='default',
                    oss_crc64='4858A48BD1466884',
                    server_side_encryption_customer_algorithm='SM4',
                ),
            ),
            aggregations=model.MetaQueryAggregations(
                aggregations=[model.MetaQueryAggregation(
                    field='Size',
                    operation='sum',
                ), model.MetaQueryAggregation(
                    field='Size',
                    operation='max',
                )],
            ),
            next_token='MTIzNDU2Nzg6aW1tdGVzdDpleGFtcGxlYnVja2V0OmRhdGFzZXQwMDE6b3NzOi8vZXhhbXBsZWJ1Y2tldC9zYW1wbGVvYmplY3QxLmpw****',
        )
        self.assertEqual('2021-06-29T15:04:05.000000000Z07:00', result.files.file.file_modified_time)
        self.assertEqual('"fba9dede5f27731c9771645a3986****"', result.files.file.etag)
        self.assertEqual('SM4', result.files.file.server_side_encryption)
        self.assertEqual(4993, result.files.file.oss_tagging_count)
        self.assertEqual('owner', result.files.file.oss_tagging.taggings[0].key)
        self.assertEqual('John', result.files.file.oss_tagging.taggings[0].value)
        self.assertEqual('owner', result.files.file.oss_tagging.taggings[1].key)
        self.assertEqual('Jack', result.files.file.oss_tagging.taggings[1].value)
        self.assertEqual('x-oss-meta-location', result.files.file.oss_user_meta.user_metas[0].key)
        self.assertEqual('hangzhou', result.files.file.oss_user_meta.user_metas[0].value)
        self.assertEqual('x-oss-meta-location', result.files.file.oss_user_meta.user_metas[1].key)
        self.assertEqual('shanghai', result.files.file.oss_user_meta.user_metas[1].value)
        self.assertEqual('exampleobject.txt', result.files.file.filename)
        self.assertEqual(344606, result.files.file.size)
        self.assertEqual('Normal', result.files.file.oss_object_type)
        self.assertEqual('Standard', result.files.file.oss_storage_class)
        self.assertEqual('default', result.files.file.object_acl)
        self.assertEqual('4858A48BD1466884', result.files.file.oss_crc64)
        self.assertEqual('SM4', result.files.file.server_side_encryption_customer_algorithm)
        self.assertEqual('Size', result.aggregations.aggregations[0].field)
        self.assertEqual('sum', result.aggregations.aggregations[0].operation)
        self.assertEqual('Size', result.aggregations.aggregations[1].field)
        self.assertEqual('max', result.aggregations.aggregations[1].operation)
        self.assertEqual('MTIzNDU2Nzg6aW1tdGVzdDpleGFtcGxlYnVja2V0OmRhdGFzZXQwMDE6b3NzOi8vZXhhbXBsZWJ1Y2tldC9zYW1wbGVvYmplY3QxLmpw****', result.next_token)

    def test_deserialize_result(self):
        xml_data = r'''
        <MetaQuery>
        </MetaQuery>'''

        result = model.DoMetaQueryResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <MetaQuery>
          <NextToken>MTIzNDU2Nzg6aW1tdGVzdDpleGFtcGxlYnVja2V0OmRhdGFzZXQwMDE6b3NzOi8vZXhhbXBsZWJ1Y2tldC9zYW1wbGVvYmplY3QxLmpw****</NextToken>
          <Files>
            <File>
              <Filename>exampleobject.txt</Filename>
              <Size>120</Size>
              <FileModifiedTime>2021-06-29T15:04:05.000000000Z07:00</FileModifiedTime>
              <OSSObjectType>Normal</OSSObjectType>
              <OSSStorageClass>Standard</OSSStorageClass>
              <ObjectACL>default</ObjectACL>
              <ETag>"fba9dede5f27731c9771645a3986****"</ETag>
              <OSSCRC64>4858A48BD1466884</OSSCRC64>
              <OSSTaggingCount>2</OSSTaggingCount>
              <OSSTagging>
                <Tagging>
                  <Key>owner</Key>
                  <Value>John</Value>
                </Tagging>
                <Tagging>
                  <Key>type</Key>
                  <Value>document</Value>
                </Tagging>
              </OSSTagging>
              <OSSUserMeta>
                <UserMeta>
                  <Key>x-oss-meta-location</Key>
                  <Value>hangzhou</Value>
                </UserMeta>
              </OSSUserMeta>
            </File>
          </Files>
        </MetaQuery>
        '''

        result = model.DoMetaQueryResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=xml_data,
            )
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('MTIzNDU2Nzg6aW1tdGVzdDpleGFtcGxlYnVja2V0OmRhdGFzZXQwMDE6b3NzOi8vZXhhbXBsZWJ1Y2tldC9zYW1wbGVvYmplY3QxLmpw****', result.next_token)
        self.assertEqual('exampleobject.txt', result.files.file.filename)
        self.assertEqual(120, result.files.file.size)
        self.assertEqual('2021-06-29T15:04:05.000000000Z07:00', result.files.file.file_modified_time)
        self.assertEqual('Normal', result.files.file.oss_object_type)
        self.assertEqual('Standard', result.files.file.oss_storage_class)
        self.assertEqual('default', result.files.file.object_acl)
        self.assertEqual('"fba9dede5f27731c9771645a3986****"', result.files.file.etag)
        self.assertEqual('4858A48BD1466884', result.files.file.oss_crc64)
        self.assertEqual(2, result.files.file.oss_tagging_count)
        self.assertEqual('owner', result.files.file.oss_tagging.taggings[0].key)
        self.assertEqual('John', result.files.file.oss_tagging.taggings[0].value)
        self.assertEqual('type', result.files.file.oss_tagging.taggings[1].key)
        self.assertEqual('document', result.files.file.oss_tagging.taggings[1].value)
        self.assertEqual('x-oss-meta-location', result.files.file.oss_user_meta.user_metas[0].key)
        self.assertEqual('hangzhou', result.files.file.oss_user_meta.user_metas[0].value)

