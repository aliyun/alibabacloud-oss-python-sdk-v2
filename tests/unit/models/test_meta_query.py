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
        self.assertEqual('exampleobject.txt', result.files.file[0].filename)
        self.assertEqual(120, result.files.file[0].size)
        self.assertEqual('2021-06-29T15:04:05.000000000Z07:00', result.files.file[0].file_modified_time)
        self.assertEqual('Normal', result.files.file[0].oss_object_type)
        self.assertEqual('Standard', result.files.file[0].oss_storage_class)
        self.assertEqual('default', result.files.file[0].object_acl)
        self.assertEqual('"fba9dede5f27731c9771645a3986****"', result.files.file[0].etag)
        self.assertEqual('4858A48BD1466884', result.files.file[0].oss_crc64)
        self.assertEqual(2, result.files.file[0].oss_tagging_count)
        self.assertEqual('owner', result.files.file[0].oss_tagging.taggings[0].key)
        self.assertEqual('John', result.files.file[0].oss_tagging.taggings[0].value)
        self.assertEqual('type', result.files.file[0].oss_tagging.taggings[1].key)
        self.assertEqual('document', result.files.file[0].oss_tagging.taggings[1].value)
        self.assertEqual('x-oss-meta-location', result.files.file[0].oss_user_meta.user_metas[0].key)
        self.assertEqual('hangzhou', result.files.file[0].oss_user_meta.user_metas[0].value)


class TestOpenMetaQueryWithSemantic(unittest.TestCase):
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
            mode='semantic',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('semantic', request.mode)

    def test_serialize_request(self):
        request = model.OpenMetaQueryRequest(
            bucket='bucketexampletest',
            mode='semantic',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='OpenMetaQuery',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('OpenMetaQuery', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('semantic', op_input.parameters.get('mode'))


class TestDoMetaQueryWithSemantic(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DoMetaQueryRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.mode)
        self.assertIsNone(request.meta_query)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DoMetaQueryRequest(
            bucket='bucketexampletest',
            mode='semantic',
            meta_query=model.MetaQuery(
                max_results=29847,
                query='俯瞰白雪覆盖的森林',
                order=model.MetaQueryOrderType.DESC,
                media_types=model.MetaQueryMediaTypes(
                    media_type=['image', 'doc']
                ),
                simple_query='{"Operation":"gt", "Field": "Size", "Value": "30"}',
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('semantic', request.mode)
        self.assertEqual(29847, request.meta_query.max_results)
        self.assertEqual('俯瞰白雪覆盖的森林', request.meta_query.query)
        self.assertEqual(model.MetaQueryOrderType.DESC, request.meta_query.order)
        self.assertEqual('image', request.meta_query.media_types.media_type[0])
        self.assertEqual('doc', request.meta_query.media_types.media_type[1])
        self.assertEqual('{"Operation":"gt", "Field": "Size", "Value": "30"}', request.meta_query.simple_query)


    def test_serialize_request(self):
        request = model.DoMetaQueryRequest(
            bucket='bucketexampletest',
            mode='semantic',
            meta_query=model.MetaQuery(
                max_results=29847,
                query='俯瞰白雪覆盖的森林',
                order=model.MetaQueryOrderType.DESC,
                media_types=model.MetaQueryMediaTypes(
                    media_type=['image', 'doc']
                ),
                simple_query='{"Operation":"gt", "Field": "Size", "Value": "30"}',
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
        self.assertEqual('semantic', op_input.parameters.get('mode'))


    def test_constructor_result(self):
        result = model.DoMetaQueryResult()
        self.assertIsNone(result.files)
        self.assertIsNone(result.aggregations)
        self.assertIsNone(result.next_token)
        self.assertIsInstance(result, serde.Model)


        result = model.DoMetaQueryResult(
            files=model.MetaQueryFiles(
                file=[model.MetaQueryFile(
                    file_modified_time='2021-06-29T14:50:14.011643661+08:00',
                    etag='"D41D8CD98F00B204E9800998ECF8****"',
                    server_side_encryption='SM4',
                    oss_tagging_count=57479,
                    oss_tagging=model.MetaQueryOSSTagging(
                        taggings=[model.MetaQueryTagging(
                            key='key2',
                            value='test_value',
                        ), model.MetaQueryTagging(
                            key='key2',
                            value='test_value',
                        )],
                    ),
                    oss_user_meta=model.MetaQueryOSSUserMeta(
                        user_metas=[model.MetaQueryUserMeta(
                            key='key2',
                            value='test_value',
                        ), model.MetaQueryUserMeta(
                            key='key2',
                            value='test_value',
                        )],
                    ),
                    filename='sampleobject.jpg',
                    size=344606,
                    oss_object_type='Normal',
                    oss_storage_class='Standard',
                    object_acl='default',
                    oss_crc64='559890638950338001',
                    server_side_encryption_customer_algorithm='SM4',
                    cache_control='no-cache',
                    content_disposition='attachment',
                    content_type='application/octet-stream',
                    lat_long='30.134390,120.074997',
                    server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
                    video_height=58285,
                    bitrate=60081,
                    meta_query_audio_streams=model.MetaQueryAudioStreams(
                        audio_stream=[model.MetaQueryAudioStream(
                            bitrate=75124,
                            sample_rate=53102,
                            start_time=0,
                            duration=71.378,
                            channels=42345,
                            language='zh-Hans',
                            codec_name='mov_text',
                        ), model.MetaQueryAudioStream(
                            bitrate=83626,
                            sample_rate=43727,
                            start_time=0.0235,
                            duration=22.88,
                            channels=80953,
                            language='zh-Hans',
                            codec_name='h264',
                        )],
                    ),
                    meta_query_addresses=model.MetaQueryAddresses(
                        address=[model.MetaQueryAddress(
                            township='文一西路',
                            address_line='中国浙江省杭州市余杭区文一西路969号',
                            city='杭州市',
                            country='中国',
                            district='余杭区',
                            language='en',
                            province='浙江省',
                        ), model.MetaQueryAddress(
                            township='文一西路',
                            address_line='中国浙江省杭州市余杭区文一西路970号',
                            city='杭州市',
                            country='中国',
                            district='余杭区',
                            language='en',
                            province='浙江省',
                        )],
                    ),
                    uri='oss://examplebucket/test-object.jpg',
                    access_control_request_method='PUT',
                    image_width=72709,
                    title='test',
                    access_control_allow_origin='https://aliyundoc.com',
                    image_height=38039,
                    album_artist='Jenny',
                    content_encoding='utf-8',
                    content_language='zh-CN',
                    artist='Jane',
                    performer='Jane',
                    meta_query_video_streams=model.MetaQueryVideoStreams(
                        video_stream=[model.MetaQueryVideoStream(
                            bitrate=94326,
                            frame_rate='25/1',
                            start_time=72,
                            duration=22.88,
                            frame_count=33053,
                            height=87074,
                            width=52909,
                            codec_name='mov_text',
                            language='en',
                            bit_depth=63855,
                            pixel_format='yuv420p',
                            color_space='bt709',
                        ), model.MetaQueryVideoStream(
                            bitrate=83277,
                            frame_rate='25/1',
                            start_time=0,
                            duration=71.378,
                            frame_count=19299,
                            height=84086,
                            width=68865,
                            codec_name='h264',
                            language='en',
                            bit_depth=50011,
                            pixel_format='yuv420p',
                            color_space='bt709',
                        )],
                    ),
                    produce_time='2021-06-29T14:50:15.011643661+08:00',
                    video_width=93628,
                    album='FirstAlbum',
                    media_type='image',
                    oss_expiration='2024-12-01T12:00:00.000Z',
                    server_side_data_encryption='KMS',
                    composer='Jane',
                    duration=22.88,
                    meta_query_subtitles=model.MetaQuerySubtitles(
                        subtitle=[model.MetaQuerySubtitle(
                            codec_name='aac',
                            language='zh-Hans',
                            start_time=0,
                            duration=71.378,
                        ), model.MetaQuerySubtitle(
                            codec_name='h264',
                            language='en',
                            start_time=72,
                            duration=22.88,
                        )],
                    ),
                ), model.MetaQueryFile(
                    file_modified_time='2021-06-29T14:50:14.011643661+08:00',
                    etag='"D41D8CD98F00B204E9800998ECF8****"',
                    server_side_encryption='SM4',
                    oss_tagging_count=30421,
                    oss_tagging=model.MetaQueryOSSTagging(
                        taggings=[model.MetaQueryTagging(
                            key='key2',
                            value='test_value',
                        ), model.MetaQueryTagging(
                            key='key',
                            value='test_value',
                        )],
                    ),
                    oss_user_meta=model.MetaQueryOSSUserMeta(
                        user_metas=[model.MetaQueryUserMeta(
                            key='key',
                            value='test_value',
                        ), model.MetaQueryUserMeta(
                            key='key2',
                            value='test_value',
                        )],
                    ),
                    filename='sampleobject.jpg',
                    size=344606,
                    oss_object_type='Normal',
                    oss_storage_class='Standard',
                    object_acl='default',
                    oss_crc64='559890638950338001',
                    server_side_encryption_customer_algorithm='SM4',
                    cache_control='no-cache',
                    content_disposition='attachment',
                    content_type='application/octet-stream',
                    lat_long='30.134390,120.074997',
                    server_side_encryption_key_id='9468da86-3509-4f8d-a61e-6eab1eac****',
                    video_height=59064,
                    bitrate=28466,
                    meta_query_audio_streams=model.MetaQueryAudioStreams(
                        audio_stream=[model.MetaQueryAudioStream(
                            bitrate=75567,
                            sample_rate=52507,
                            start_time=0,
                            duration=71.378,
                            channels=49205,
                            language='en',
                            codec_name='mov_text',
                        ), model.MetaQueryAudioStream(
                            bitrate=63776,
                            sample_rate=26988,
                            start_time=72,
                            duration=71.378,
                            channels=38490,
                            language='en',
                            codec_name='h264',
                        )],
                    ),
                    meta_query_addresses=model.MetaQueryAddresses(
                        address=[model.MetaQueryAddress(
                            township='文一西路',
                            address_line='中国浙江省杭州市余杭区文一西路970号',
                            city='杭州市',
                            country='中国',
                            district='余杭区',
                            language='zh-Hans',
                            province='浙江省',
                        ), model.MetaQueryAddress(
                            township='文一西路',
                            address_line='中国浙江省杭州市余杭区文一西路970号',
                            city='杭州市',
                            country='中国',
                            district='余杭区',
                            language='zh-Hans',
                            province='浙江省',
                        )],
                    ),
                    uri='oss://examplebucket/test-object.jpg',
                    access_control_request_method='PUT',
                    image_width=38435,
                    title='test',
                    access_control_allow_origin='https://aliyundoc.com',
                    image_height=28765,
                    album_artist='Jenny',
                    content_encoding='utf-8',
                    content_language='zh-CN',
                    artist='Jane',
                    performer='Jane',
                    meta_query_video_streams=model.MetaQueryVideoStreams(
                        video_stream=[model.MetaQueryVideoStream(
                            bitrate=29068,
                            frame_rate='25/1',
                            start_time=0.0235,
                            duration=3.690667,
                            frame_count=57140,
                            height=30443,
                            width=69926,
                            codec_name='mov_text',
                            language='en',
                            bit_depth=84791,
                            pixel_format='yuv420p',
                            color_space='bt709',
                        ), model.MetaQueryVideoStream(
                            bitrate=44804,
                            frame_rate='25/1',
                            start_time=0.0235,
                            duration=22.88,
                            frame_count=47752,
                            height=21376,
                            width=746,
                            codec_name='mov_text',
                            language='en',
                            bit_depth=82631,
                            pixel_format='yuv420p',
                            color_space='bt709',
                        )],
                    ),
                    produce_time='2021-06-29T14:50:15.011643661+08:00',
                    video_width=65306,
                    album='FirstAlbum',
                    media_type='image',
                    oss_expiration='2024-12-01T12:00:00.000Z',
                    server_side_data_encryption='KMS',
                    composer='Jane',
                    duration=22.88,
                    meta_query_subtitles=model.MetaQuerySubtitles(
                        subtitle=[model.MetaQuerySubtitle(
                            codec_name='mov_text',
                            language='en',
                            start_time=0,
                            duration=3.690667,
                        ), model.MetaQuerySubtitle(
                            codec_name='mov_text',
                            language='zh-Hans',
                            start_time=0.0235,
                            duration=71.378,
                        )],
                    ),
                )],
            ),
            aggregations=model.MetaQueryAggregations(
                aggregations=[model.MetaQueryAggregation(
                    field='test_field',
                    operation='test_operation',
                    value=11.12,
                    groups=model.MetaQueryGroups(
                        groups=[model.MetaQueryGroup(
                            value='test_value',
                            count=80169,
                        ), model.MetaQueryGroup(
                            value='test_value',
                            count=35599,
                        )],
                    ),
                ), model.MetaQueryAggregation(
                    field='test_field',
                    operation='test_operation',
                    value=12.21,
                    groups=model.MetaQueryGroups(
                        groups=[model.MetaQueryGroup(
                            value='test_value',
                            count=29768,
                        ), model.MetaQueryGroup(
                            value='test_value',
                            count=19056,
                        )],
                    ),
                )],
            ),
            next_token='test_next_token',
        )
        self.assertEqual('2021-06-29T14:50:14.011643661+08:00', result.files.file[0].file_modified_time)
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.files.file[0].etag)
        self.assertEqual('SM4', result.files.file[0].server_side_encryption)
        self.assertEqual(57479, result.files.file[0].oss_tagging_count)
        self.assertEqual('key2', result.files.file[0].oss_tagging.taggings[0].key)
        self.assertEqual('test_value', result.files.file[0].oss_tagging.taggings[0].value)
        self.assertEqual('key2', result.files.file[0].oss_tagging.taggings[1].key)
        self.assertEqual('test_value', result.files.file[0].oss_tagging.taggings[1].value)
        self.assertEqual('key2', result.files.file[0].oss_user_meta.user_metas[0].key)
        self.assertEqual('test_value', result.files.file[0].oss_user_meta.user_metas[0].value)
        self.assertEqual('key2', result.files.file[0].oss_user_meta.user_metas[1].key)
        self.assertEqual('test_value', result.files.file[0].oss_user_meta.user_metas[1].value)
        self.assertEqual('sampleobject.jpg', result.files.file[0].filename)
        self.assertEqual(344606, result.files.file[0].size)
        self.assertEqual('Normal', result.files.file[0].oss_object_type)
        self.assertEqual('Standard', result.files.file[0].oss_storage_class)
        self.assertEqual('default', result.files.file[0].object_acl)
        self.assertEqual('559890638950338001', result.files.file[0].oss_crc64)
        self.assertEqual('SM4', result.files.file[0].server_side_encryption_customer_algorithm)
        self.assertEqual('no-cache', result.files.file[0].cache_control)
        self.assertEqual('attachment', result.files.file[0].content_disposition)
        self.assertEqual('application/octet-stream', result.files.file[0].content_type)
        self.assertEqual('30.134390,120.074997', result.files.file[0].lat_long)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.files.file[0].server_side_encryption_key_id)
        self.assertEqual(58285, result.files.file[0].video_height)
        self.assertEqual(60081, result.files.file[0].bitrate)
        self.assertEqual(75124, result.files.file[0].meta_query_audio_streams.audio_stream[0].bitrate)
        self.assertEqual(53102, result.files.file[0].meta_query_audio_streams.audio_stream[0].sample_rate)
        self.assertEqual(0, result.files.file[0].meta_query_audio_streams.audio_stream[0].start_time)
        self.assertEqual(71.378, result.files.file[0].meta_query_audio_streams.audio_stream[0].duration)
        self.assertEqual(42345, result.files.file[0].meta_query_audio_streams.audio_stream[0].channels)
        self.assertEqual('zh-Hans', result.files.file[0].meta_query_audio_streams.audio_stream[0].language)
        self.assertEqual('mov_text', result.files.file[0].meta_query_audio_streams.audio_stream[0].codec_name)
        self.assertEqual(83626, result.files.file[0].meta_query_audio_streams.audio_stream[1].bitrate)
        self.assertEqual(43727, result.files.file[0].meta_query_audio_streams.audio_stream[1].sample_rate)
        self.assertEqual(0.0235, result.files.file[0].meta_query_audio_streams.audio_stream[1].start_time)
        self.assertEqual(22.88, result.files.file[0].meta_query_audio_streams.audio_stream[1].duration)
        self.assertEqual(80953, result.files.file[0].meta_query_audio_streams.audio_stream[1].channels)
        self.assertEqual('zh-Hans', result.files.file[0].meta_query_audio_streams.audio_stream[1].language)
        self.assertEqual('h264', result.files.file[0].meta_query_audio_streams.audio_stream[1].codec_name)
        self.assertEqual('文一西路', result.files.file[0].meta_query_addresses.address[0].township)
        self.assertEqual('中国浙江省杭州市余杭区文一西路969号', result.files.file[0].meta_query_addresses.address[0].address_line)
        self.assertEqual('杭州市', result.files.file[0].meta_query_addresses.address[0].city)
        self.assertEqual('中国', result.files.file[0].meta_query_addresses.address[0].country)
        self.assertEqual('余杭区', result.files.file[0].meta_query_addresses.address[0].district)
        self.assertEqual('en', result.files.file[0].meta_query_addresses.address[0].language)
        self.assertEqual('浙江省', result.files.file[0].meta_query_addresses.address[0].province)
        self.assertEqual('文一西路', result.files.file[0].meta_query_addresses.address[1].township)
        self.assertEqual('中国浙江省杭州市余杭区文一西路970号', result.files.file[0].meta_query_addresses.address[1].address_line)
        self.assertEqual('杭州市', result.files.file[0].meta_query_addresses.address[1].city)
        self.assertEqual('中国', result.files.file[0].meta_query_addresses.address[1].country)
        self.assertEqual('余杭区', result.files.file[0].meta_query_addresses.address[1].district)
        self.assertEqual('en', result.files.file[0].meta_query_addresses.address[1].language)
        self.assertEqual('浙江省', result.files.file[0].meta_query_addresses.address[1].province)
        self.assertEqual('oss://examplebucket/test-object.jpg', result.files.file[0].uri)
        self.assertEqual('PUT', result.files.file[0].access_control_request_method)
        self.assertEqual(72709, result.files.file[0].image_width)
        self.assertEqual('test', result.files.file[0].title)
        self.assertEqual('https://aliyundoc.com', result.files.file[0].access_control_allow_origin)
        self.assertEqual(38039, result.files.file[0].image_height)
        self.assertEqual('Jenny', result.files.file[0].album_artist)
        self.assertEqual('utf-8', result.files.file[0].content_encoding)
        self.assertEqual('zh-CN', result.files.file[0].content_language)
        self.assertEqual('Jane', result.files.file[0].artist)
        self.assertEqual('Jane', result.files.file[0].performer)
        self.assertEqual(94326, result.files.file[0].meta_query_video_streams.video_stream[0].bitrate)
        self.assertEqual('25/1', result.files.file[0].meta_query_video_streams.video_stream[0].frame_rate)
        self.assertEqual(72, result.files.file[0].meta_query_video_streams.video_stream[0].start_time)
        self.assertEqual(22.88, result.files.file[0].meta_query_video_streams.video_stream[0].duration)
        self.assertEqual(33053, result.files.file[0].meta_query_video_streams.video_stream[0].frame_count)
        self.assertEqual(87074, result.files.file[0].meta_query_video_streams.video_stream[0].height)
        self.assertEqual(52909, result.files.file[0].meta_query_video_streams.video_stream[0].width)
        self.assertEqual('mov_text', result.files.file[0].meta_query_video_streams.video_stream[0].codec_name)
        self.assertEqual('en', result.files.file[0].meta_query_video_streams.video_stream[0].language)
        self.assertEqual(63855, result.files.file[0].meta_query_video_streams.video_stream[0].bit_depth)
        self.assertEqual('yuv420p', result.files.file[0].meta_query_video_streams.video_stream[0].pixel_format)
        self.assertEqual('bt709', result.files.file[0].meta_query_video_streams.video_stream[0].color_space)
        self.assertEqual(83277, result.files.file[0].meta_query_video_streams.video_stream[1].bitrate)
        self.assertEqual('25/1', result.files.file[0].meta_query_video_streams.video_stream[1].frame_rate)
        self.assertEqual(0, result.files.file[0].meta_query_video_streams.video_stream[1].start_time)
        self.assertEqual(71.378, result.files.file[0].meta_query_video_streams.video_stream[1].duration)
        self.assertEqual(19299, result.files.file[0].meta_query_video_streams.video_stream[1].frame_count)
        self.assertEqual(84086, result.files.file[0].meta_query_video_streams.video_stream[1].height)
        self.assertEqual(68865, result.files.file[0].meta_query_video_streams.video_stream[1].width)
        self.assertEqual('h264', result.files.file[0].meta_query_video_streams.video_stream[1].codec_name)
        self.assertEqual('en', result.files.file[0].meta_query_video_streams.video_stream[1].language)
        self.assertEqual(50011, result.files.file[0].meta_query_video_streams.video_stream[1].bit_depth)
        self.assertEqual('yuv420p', result.files.file[0].meta_query_video_streams.video_stream[1].pixel_format)
        self.assertEqual('bt709', result.files.file[0].meta_query_video_streams.video_stream[1].color_space)
        self.assertEqual('2021-06-29T14:50:15.011643661+08:00', result.files.file[0].produce_time)
        self.assertEqual(93628, result.files.file[0].video_width)
        self.assertEqual('FirstAlbum', result.files.file[0].album)
        self.assertEqual('image', result.files.file[0].media_type)
        self.assertEqual('2024-12-01T12:00:00.000Z', result.files.file[0].oss_expiration)
        self.assertEqual('KMS', result.files.file[0].server_side_data_encryption)
        self.assertEqual('Jane', result.files.file[0].composer)
        self.assertEqual(22.88, result.files.file[0].duration)
        self.assertEqual('aac', result.files.file[0].meta_query_subtitles.subtitle[0].codec_name)
        self.assertEqual('zh-Hans', result.files.file[0].meta_query_subtitles.subtitle[0].language)
        self.assertEqual(0, result.files.file[0].meta_query_subtitles.subtitle[0].start_time)
        self.assertEqual(71.378, result.files.file[0].meta_query_subtitles.subtitle[0].duration)
        self.assertEqual('h264', result.files.file[0].meta_query_subtitles.subtitle[1].codec_name)
        self.assertEqual('en', result.files.file[0].meta_query_subtitles.subtitle[1].language)
        self.assertEqual(72, result.files.file[0].meta_query_subtitles.subtitle[1].start_time)
        self.assertEqual(22.88, result.files.file[0].meta_query_subtitles.subtitle[1].duration)
        self.assertEqual('2021-06-29T14:50:14.011643661+08:00', result.files.file[1].file_modified_time)
        self.assertEqual('"D41D8CD98F00B204E9800998ECF8****"', result.files.file[1].etag)
        self.assertEqual('SM4', result.files.file[1].server_side_encryption)
        self.assertEqual(30421, result.files.file[1].oss_tagging_count)
        self.assertEqual('key2', result.files.file[1].oss_tagging.taggings[0].key)
        self.assertEqual('test_value', result.files.file[1].oss_tagging.taggings[0].value)
        self.assertEqual('key', result.files.file[1].oss_tagging.taggings[1].key)
        self.assertEqual('test_value', result.files.file[1].oss_tagging.taggings[1].value)
        self.assertEqual('key', result.files.file[1].oss_user_meta.user_metas[0].key)
        self.assertEqual('test_value', result.files.file[1].oss_user_meta.user_metas[0].value)
        self.assertEqual('key2', result.files.file[1].oss_user_meta.user_metas[1].key)
        self.assertEqual('test_value', result.files.file[1].oss_user_meta.user_metas[1].value)
        self.assertEqual('sampleobject.jpg', result.files.file[1].filename)
        self.assertEqual(344606, result.files.file[1].size)
        self.assertEqual('Normal', result.files.file[1].oss_object_type)
        self.assertEqual('Standard', result.files.file[1].oss_storage_class)
        self.assertEqual('default', result.files.file[1].object_acl)
        self.assertEqual('559890638950338001', result.files.file[1].oss_crc64)
        self.assertEqual('SM4', result.files.file[1].server_side_encryption_customer_algorithm)
        self.assertEqual('no-cache', result.files.file[1].cache_control)
        self.assertEqual('attachment', result.files.file[1].content_disposition)
        self.assertEqual('application/octet-stream', result.files.file[1].content_type)
        self.assertEqual('30.134390,120.074997', result.files.file[1].lat_long)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.files.file[1].server_side_encryption_key_id)
        self.assertEqual(59064, result.files.file[1].video_height)
        self.assertEqual(28466, result.files.file[1].bitrate)
        self.assertEqual(75567, result.files.file[1].meta_query_audio_streams.audio_stream[0].bitrate)
        self.assertEqual(52507, result.files.file[1].meta_query_audio_streams.audio_stream[0].sample_rate)
        self.assertEqual(0, result.files.file[1].meta_query_audio_streams.audio_stream[0].start_time)
        self.assertEqual(71.378, result.files.file[1].meta_query_audio_streams.audio_stream[0].duration)
        self.assertEqual(49205, result.files.file[1].meta_query_audio_streams.audio_stream[0].channels)
        self.assertEqual('en', result.files.file[1].meta_query_audio_streams.audio_stream[0].language)
        self.assertEqual('mov_text', result.files.file[1].meta_query_audio_streams.audio_stream[0].codec_name)
        self.assertEqual(63776, result.files.file[1].meta_query_audio_streams.audio_stream[1].bitrate)
        self.assertEqual(26988, result.files.file[1].meta_query_audio_streams.audio_stream[1].sample_rate)
        self.assertEqual(72, result.files.file[1].meta_query_audio_streams.audio_stream[1].start_time)
        self.assertEqual(71.378, result.files.file[1].meta_query_audio_streams.audio_stream[1].duration)
        self.assertEqual(38490, result.files.file[1].meta_query_audio_streams.audio_stream[1].channels)
        self.assertEqual('en', result.files.file[1].meta_query_audio_streams.audio_stream[1].language)
        self.assertEqual('h264', result.files.file[1].meta_query_audio_streams.audio_stream[1].codec_name)
        self.assertEqual('文一西路', result.files.file[1].meta_query_addresses.address[0].township)
        self.assertEqual('中国浙江省杭州市余杭区文一西路970号', result.files.file[1].meta_query_addresses.address[0].address_line)
        self.assertEqual('杭州市', result.files.file[1].meta_query_addresses.address[0].city)
        self.assertEqual('中国', result.files.file[1].meta_query_addresses.address[0].country)
        self.assertEqual('余杭区', result.files.file[1].meta_query_addresses.address[0].district)
        self.assertEqual('zh-Hans', result.files.file[1].meta_query_addresses.address[0].language)
        self.assertEqual('浙江省', result.files.file[1].meta_query_addresses.address[0].province)
        self.assertEqual('文一西路', result.files.file[1].meta_query_addresses.address[1].township)
        self.assertEqual('中国浙江省杭州市余杭区文一西路970号', result.files.file[1].meta_query_addresses.address[1].address_line)
        self.assertEqual('杭州市', result.files.file[1].meta_query_addresses.address[1].city)
        self.assertEqual('中国', result.files.file[1].meta_query_addresses.address[1].country)
        self.assertEqual('余杭区', result.files.file[1].meta_query_addresses.address[1].district)
        self.assertEqual('zh-Hans', result.files.file[1].meta_query_addresses.address[1].language)
        self.assertEqual('浙江省', result.files.file[1].meta_query_addresses.address[1].province)
        self.assertEqual('oss://examplebucket/test-object.jpg', result.files.file[1].uri)
        self.assertEqual('PUT', result.files.file[1].access_control_request_method)
        self.assertEqual(38435, result.files.file[1].image_width)
        self.assertEqual('test', result.files.file[1].title)
        self.assertEqual('https://aliyundoc.com', result.files.file[1].access_control_allow_origin)
        self.assertEqual(28765, result.files.file[1].image_height)
        self.assertEqual('Jenny', result.files.file[1].album_artist)
        self.assertEqual('utf-8', result.files.file[1].content_encoding)
        self.assertEqual('zh-CN', result.files.file[1].content_language)
        self.assertEqual('Jane', result.files.file[1].artist)
        self.assertEqual('Jane', result.files.file[1].performer)
        self.assertEqual(29068, result.files.file[1].meta_query_video_streams.video_stream[0].bitrate)
        self.assertEqual('25/1', result.files.file[1].meta_query_video_streams.video_stream[0].frame_rate)
        self.assertEqual(0.0235, result.files.file[1].meta_query_video_streams.video_stream[0].start_time)
        self.assertEqual(3.690667, result.files.file[1].meta_query_video_streams.video_stream[0].duration)
        self.assertEqual(57140, result.files.file[1].meta_query_video_streams.video_stream[0].frame_count)
        self.assertEqual(30443, result.files.file[1].meta_query_video_streams.video_stream[0].height)
        self.assertEqual(69926, result.files.file[1].meta_query_video_streams.video_stream[0].width)
        self.assertEqual('mov_text', result.files.file[1].meta_query_video_streams.video_stream[0].codec_name)
        self.assertEqual('en', result.files.file[1].meta_query_video_streams.video_stream[0].language)
        self.assertEqual(84791, result.files.file[1].meta_query_video_streams.video_stream[0].bit_depth)
        self.assertEqual('yuv420p', result.files.file[1].meta_query_video_streams.video_stream[0].pixel_format)
        self.assertEqual('bt709', result.files.file[1].meta_query_video_streams.video_stream[0].color_space)
        self.assertEqual(44804, result.files.file[1].meta_query_video_streams.video_stream[1].bitrate)
        self.assertEqual('25/1', result.files.file[1].meta_query_video_streams.video_stream[1].frame_rate)
        self.assertEqual(0.0235, result.files.file[1].meta_query_video_streams.video_stream[1].start_time)
        self.assertEqual(22.88, result.files.file[1].meta_query_video_streams.video_stream[1].duration)
        self.assertEqual(47752, result.files.file[1].meta_query_video_streams.video_stream[1].frame_count)
        self.assertEqual(21376, result.files.file[1].meta_query_video_streams.video_stream[1].height)
        self.assertEqual(746, result.files.file[1].meta_query_video_streams.video_stream[1].width)
        self.assertEqual('mov_text', result.files.file[1].meta_query_video_streams.video_stream[1].codec_name)
        self.assertEqual('en', result.files.file[1].meta_query_video_streams.video_stream[1].language)
        self.assertEqual(82631, result.files.file[1].meta_query_video_streams.video_stream[1].bit_depth)
        self.assertEqual('yuv420p', result.files.file[1].meta_query_video_streams.video_stream[1].pixel_format)
        self.assertEqual('bt709', result.files.file[1].meta_query_video_streams.video_stream[1].color_space)
        self.assertEqual('2021-06-29T14:50:15.011643661+08:00', result.files.file[1].produce_time)
        self.assertEqual(65306, result.files.file[1].video_width)
        self.assertEqual('FirstAlbum', result.files.file[1].album)
        self.assertEqual('image', result.files.file[1].media_type)
        self.assertEqual('2024-12-01T12:00:00.000Z', result.files.file[1].oss_expiration)
        self.assertEqual('KMS', result.files.file[1].server_side_data_encryption)
        self.assertEqual('Jane', result.files.file[1].composer)
        self.assertEqual(22.88, result.files.file[1].duration)
        self.assertEqual('mov_text', result.files.file[1].meta_query_subtitles.subtitle[0].codec_name)
        self.assertEqual('en', result.files.file[1].meta_query_subtitles.subtitle[0].language)
        self.assertEqual(0, result.files.file[1].meta_query_subtitles.subtitle[0].start_time)
        self.assertEqual(3.690667, result.files.file[1].meta_query_subtitles.subtitle[0].duration)
        self.assertEqual('mov_text', result.files.file[1].meta_query_subtitles.subtitle[1].codec_name)
        self.assertEqual('zh-Hans', result.files.file[1].meta_query_subtitles.subtitle[1].language)
        self.assertEqual(0.0235, result.files.file[1].meta_query_subtitles.subtitle[1].start_time)
        self.assertEqual(71.378, result.files.file[1].meta_query_subtitles.subtitle[1].duration)
        self.assertEqual('test_field', result.aggregations.aggregations[0].field)
        self.assertEqual('test_operation', result.aggregations.aggregations[0].operation)
        self.assertEqual(11.12, result.aggregations.aggregations[0].value)
        self.assertEqual('test_value', result.aggregations.aggregations[0].groups.groups[0].value)
        self.assertEqual(80169, result.aggregations.aggregations[0].groups.groups[0].count)
        self.assertEqual('test_value', result.aggregations.aggregations[0].groups.groups[1].value)
        self.assertEqual(35599, result.aggregations.aggregations[0].groups.groups[1].count)
        self.assertEqual('test_field', result.aggregations.aggregations[1].field)
        self.assertEqual('test_operation', result.aggregations.aggregations[1].operation)
        self.assertEqual(12.21, result.aggregations.aggregations[1].value)
        self.assertEqual('test_value', result.aggregations.aggregations[1].groups.groups[0].value)
        self.assertEqual(29768, result.aggregations.aggregations[1].groups.groups[0].count)
        self.assertEqual('test_value', result.aggregations.aggregations[1].groups.groups[1].value)
        self.assertEqual(19056, result.aggregations.aggregations[1].groups.groups[1].count)
        self.assertEqual('test_next_token', result.next_token)

    def test_deserialize_result(self):
        xml_data = r'''
        <MetaQuery>
        </MetaQuery>'''

        result = model.DoMetaQueryResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <MetaQuery>
          <Files>
            <File>
              <URI>oss://examplebucket/test-object.jpg</URI>
              <Filename>sampleobject.jpg</Filename>
              <Size>1000</Size>
              <ObjectACL>default</ObjectACL>
              <FileModifiedTime>2021-06-29T14:50:14.011643661+08:00</FileModifiedTime>
              <ServerSideEncryption>AES256</ServerSideEncryption>
              <ServerSideEncryptionCustomerAlgorithm>SM4</ServerSideEncryptionCustomerAlgorithm>
              <ETag>"1D9C280A7C4F67F7EF873E28449****"</ETag>
              <OSSCRC64>559890638950338001</OSSCRC64>
              <ProduceTime>2021-06-29T14:50:15.011643661+08:00</ProduceTime>
              <ContentType>image/jpeg</ContentType>
              <MediaType>image</MediaType>
              <LatLong>30.134390,120.074997</LatLong>
              <Title>test</Title>
              <OSSExpiration>2024-12-01T12:00:00.000Z</OSSExpiration>
              <AccessControlAllowOrigin>https://aliyundoc.com</AccessControlAllowOrigin>
              <AccessControlRequestMethod>PUT</AccessControlRequestMethod>
              <ServerSideDataEncryption>SM4</ServerSideDataEncryption>
              <ServerSideEncryptionKeyId>9468da86-3509-4f8d-a61e-6eab1eac****</ServerSideEncryptionKeyId>
              <CacheControl>no-cache</CacheControl>
              <ContentDisposition>attachment; filename =test.jpg</ContentDisposition>
              <ContentEncoding>UTF-8</ContentEncoding>
              <ContentLanguage>zh-CN</ContentLanguage>
              <ImageHeight>500</ImageHeight>
              <ImageWidth>270</ImageWidth>
              <VideoWidth>1080</VideoWidth>
              <VideoHeight>1920</VideoHeight>
              <VideoStreams>
                <VideoStream>
                  <CodecName>h264</CodecName>
                  <Language>en</Language>
                  <Bitrate>5407765</Bitrate>
                  <FrameRate>25/1</FrameRate>
                  <StartTime>0</StartTime>
                  <Duration>22.88</Duration>
                  <FrameCount>572</FrameCount>
                  <BitDepth>8</BitDepth>
                  <PixelFormat>yuv420p</PixelFormat>
                  <ColorSpace>bt709</ColorSpace>
                  <Height>720</Height>
                  <Width>1280</Width>
                </VideoStream>
                <VideoStream>
                  <CodecName>h264</CodecName>
                  <Language>en</Language>
                  <Bitrate>5407765</Bitrate>
                  <FrameRate>25/1</FrameRate>
                  <StartTime>0</StartTime>
                  <Duration>22.88</Duration>
                  <FrameCount>572</FrameCount>
                  <BitDepth>8</BitDepth>
                  <PixelFormat>yuv420p</PixelFormat>
                  <ColorSpace>bt709</ColorSpace>
                  <Height>720</Height>
                  <Width>1280</Width>
                </VideoStream>
              </VideoStreams>
              <AudioStreams>
                <AudioStream>
                  <CodecName>aac</CodecName>
                  <Bitrate>1048576</Bitrate>
                  <SampleRate>48000</SampleRate>
                  <StartTime>0.0235</StartTime>
                  <Duration>3.690667</Duration>
                  <Channels>2</Channels>
                  <Language>en</Language>
                </AudioStream>
              </AudioStreams>
              <Subtitles>
                <Subtitle>
                  <CodecName>mov_text</CodecName>
                  <Language>en</Language>
                  <StartTime>0</StartTime>
                  <Duration>71.378</Duration>
                </Subtitle>
                <Subtitle>
                  <CodecName>mov_text</CodecName>
                  <Language>en</Language>
                  <StartTime>72</StartTime>
                  <Duration>71.378</Duration>
                </Subtitle>
              </Subtitles>
              <Bitrate>5407765</Bitrate>
              <Artist>Jane</Artist>
              <AlbumArtist>Jenny</AlbumArtist>
              <Composer>Jane</Composer>
              <Performer>Jane</Performer>
              <Album>FirstAlbum</Album>
              <Duration>71.378</Duration>
              <Addresses>
                <Address>
                  <AddressLine>中国浙江省杭州市余杭区文一西路969号</AddressLine>
                  <City>杭州市</City>
                  <Country>中国</Country>
                  <District>余杭区</District>
                  <Language>zh-Hans</Language>
                  <Province>浙江省</Province>
                  <Township>文一西路</Township>
                </Address>
                <Address>
                  <AddressLine>中国浙江省杭州市余杭区文一西路970号</AddressLine>
                  <City>杭州市</City>
                  <Country>中国</Country>
                  <District>余杭区</District>
                  <Language>zh-Hans</Language>
                  <Province>浙江省</Province>
                  <Township>文一西路</Township>
                </Address>
              </Addresses>
              <OSSObjectType>Normal</OSSObjectType>
              <OSSStorageClass>Standard</OSSStorageClass>
              <OSSTaggingCount>2</OSSTaggingCount>
              <OSSTagging>
                <Tagging>
                  <Key>key</Key>
                  <Value>val</Value>
                </Tagging>
                <Tagging>
                  <Key>key2</Key>
                  <Value>val2</Value>
                </Tagging>
              </OSSTagging>
              <OSSUserMeta>
                <UserMeta>
                  <Key>key</Key>
                  <Value>val</Value>
                </UserMeta>
              </OSSUserMeta>
            </File>
            <File>
                  <AlbumArtist>Jenny</AlbumArtist>
                  <Composer>Jane</Composer>
                  <Performer>Jane</Performer>
                  <Album>FirstAlbum</Album>
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
        self.assertEqual('oss://examplebucket/test-object.jpg', result.files.file[0].uri)
        self.assertEqual('sampleobject.jpg', result.files.file[0].filename)
        self.assertEqual(1000, result.files.file[0].size)
        self.assertEqual('default', result.files.file[0].object_acl)
        self.assertEqual('2021-06-29T14:50:14.011643661+08:00', result.files.file[0].file_modified_time)
        self.assertEqual('AES256', result.files.file[0].server_side_encryption)
        self.assertEqual('SM4', result.files.file[0].server_side_encryption_customer_algorithm)
        self.assertEqual('"1D9C280A7C4F67F7EF873E28449****"', result.files.file[0].etag)
        self.assertEqual('559890638950338001', result.files.file[0].oss_crc64)
        self.assertEqual('2021-06-29T14:50:15.011643661+08:00', result.files.file[0].produce_time)
        self.assertEqual('image/jpeg', result.files.file[0].content_type)
        self.assertEqual('image', result.files.file[0].media_type)
        self.assertEqual('30.134390,120.074997', result.files.file[0].lat_long)
        self.assertEqual('test', result.files.file[0].title)
        self.assertEqual('2024-12-01T12:00:00.000Z', result.files.file[0].oss_expiration)
        self.assertEqual('https://aliyundoc.com', result.files.file[0].access_control_allow_origin)
        self.assertEqual('PUT', result.files.file[0].access_control_request_method)
        self.assertEqual('SM4', result.files.file[0].server_side_data_encryption)
        self.assertEqual('9468da86-3509-4f8d-a61e-6eab1eac****', result.files.file[0].server_side_encryption_key_id)
        self.assertEqual('no-cache', result.files.file[0].cache_control)
        self.assertEqual('attachment; filename =test.jpg', result.files.file[0].content_disposition)
        self.assertEqual('UTF-8', result.files.file[0].content_encoding)
        self.assertEqual('zh-CN', result.files.file[0].content_language)
        self.assertEqual(500, result.files.file[0].image_height)
        self.assertEqual(270, result.files.file[0].image_width)
        self.assertEqual(1080, result.files.file[0].video_width)
        self.assertEqual(1920, result.files.file[0].video_height)
        self.assertEqual('h264', result.files.file[0].meta_query_video_streams.video_stream[0].codec_name)
        self.assertEqual('en', result.files.file[0].meta_query_video_streams.video_stream[0].language)
        self.assertEqual(5407765, result.files.file[0].meta_query_video_streams.video_stream[0].bitrate)
        self.assertEqual('25/1', result.files.file[0].meta_query_video_streams.video_stream[0].frame_rate)
        self.assertEqual(0, result.files.file[0].meta_query_video_streams.video_stream[0].start_time)
        self.assertEqual(22.88, result.files.file[0].meta_query_video_streams.video_stream[0].duration)
        self.assertEqual(572, result.files.file[0].meta_query_video_streams.video_stream[0].frame_count)
        self.assertEqual(8, result.files.file[0].meta_query_video_streams.video_stream[0].bit_depth)
        self.assertEqual('yuv420p', result.files.file[0].meta_query_video_streams.video_stream[0].pixel_format)
        self.assertEqual('bt709', result.files.file[0].meta_query_video_streams.video_stream[0].color_space)
        self.assertEqual(720, result.files.file[0].meta_query_video_streams.video_stream[0].height)
        self.assertEqual(1280, result.files.file[0].meta_query_video_streams.video_stream[0].width)
        self.assertEqual('h264', result.files.file[0].meta_query_video_streams.video_stream[1].codec_name)
        self.assertEqual('en', result.files.file[0].meta_query_video_streams.video_stream[1].language)
        self.assertEqual(5407765, result.files.file[0].meta_query_video_streams.video_stream[1].bitrate)
        self.assertEqual('25/1', result.files.file[0].meta_query_video_streams.video_stream[1].frame_rate)
        self.assertEqual(0, result.files.file[0].meta_query_video_streams.video_stream[1].start_time)
        self.assertEqual(22.88, result.files.file[0].meta_query_video_streams.video_stream[1].duration)
        self.assertEqual(572, result.files.file[0].meta_query_video_streams.video_stream[1].frame_count)
        self.assertEqual(8, result.files.file[0].meta_query_video_streams.video_stream[1].bit_depth)
        self.assertEqual('yuv420p', result.files.file[0].meta_query_video_streams.video_stream[1].pixel_format)
        self.assertEqual('bt709', result.files.file[0].meta_query_video_streams.video_stream[1].color_space)
        self.assertEqual(720, result.files.file[0].meta_query_video_streams.video_stream[1].height)
        self.assertEqual(1280, result.files.file[0].meta_query_video_streams.video_stream[1].width)
        self.assertEqual('aac', result.files.file[0].meta_query_audio_streams.audio_stream[0].codec_name)
        self.assertEqual(1048576, result.files.file[0].meta_query_audio_streams.audio_stream[0].bitrate)
        self.assertEqual(48000, result.files.file[0].meta_query_audio_streams.audio_stream[0].sample_rate)
        self.assertEqual(0.0235, result.files.file[0].meta_query_audio_streams.audio_stream[0].start_time)
        self.assertEqual(3.690667, result.files.file[0].meta_query_audio_streams.audio_stream[0].duration)
        self.assertEqual(2, result.files.file[0].meta_query_audio_streams.audio_stream[0].channels)
        self.assertEqual('en', result.files.file[0].meta_query_audio_streams.audio_stream[0].language)
        self.assertEqual('mov_text', result.files.file[0].meta_query_subtitles.subtitle[0].codec_name)
        self.assertEqual('en', result.files.file[0].meta_query_subtitles.subtitle[0].language)
        self.assertEqual(0, result.files.file[0].meta_query_subtitles.subtitle[0].start_time)
        self.assertEqual(71.378, result.files.file[0].meta_query_subtitles.subtitle[0].duration)
        self.assertEqual('mov_text', result.files.file[0].meta_query_subtitles.subtitle[1].codec_name)
        self.assertEqual('en', result.files.file[0].meta_query_subtitles.subtitle[1].language)
        self.assertEqual(72, result.files.file[0].meta_query_subtitles.subtitle[1].start_time)
        self.assertEqual(71.378, result.files.file[0].meta_query_subtitles.subtitle[1].duration)
        self.assertEqual(5407765, result.files.file[0].bitrate)
        self.assertEqual('Jane', result.files.file[0].artist)
        self.assertEqual('Jenny', result.files.file[0].album_artist)
        self.assertEqual('Jane', result.files.file[0].composer)
        self.assertEqual('Jane', result.files.file[0].performer)
        self.assertEqual('FirstAlbum', result.files.file[0].album)
        self.assertEqual(71.378, result.files.file[0].duration)
        self.assertEqual('中国浙江省杭州市余杭区文一西路969号', result.files.file[0].meta_query_addresses.address[0].address_line)
        self.assertEqual('杭州市', result.files.file[0].meta_query_addresses.address[0].city)
        self.assertEqual('中国', result.files.file[0].meta_query_addresses.address[0].country)
        self.assertEqual('余杭区', result.files.file[0].meta_query_addresses.address[0].district)
        self.assertEqual('zh-Hans', result.files.file[0].meta_query_addresses.address[0].language)
        self.assertEqual('浙江省', result.files.file[0].meta_query_addresses.address[0].province)
        self.assertEqual('文一西路', result.files.file[0].meta_query_addresses.address[0].township)
        self.assertEqual('中国浙江省杭州市余杭区文一西路970号', result.files.file[0].meta_query_addresses.address[1].address_line)
        self.assertEqual('杭州市', result.files.file[0].meta_query_addresses.address[1].city)
        self.assertEqual('中国', result.files.file[0].meta_query_addresses.address[1].country)
        self.assertEqual('余杭区', result.files.file[0].meta_query_addresses.address[1].district)
        self.assertEqual('zh-Hans', result.files.file[0].meta_query_addresses.address[1].language)
        self.assertEqual('浙江省', result.files.file[0].meta_query_addresses.address[1].province)
        self.assertEqual('文一西路', result.files.file[0].meta_query_addresses.address[1].township)
        self.assertEqual('Normal', result.files.file[0].oss_object_type)
        self.assertEqual('Standard', result.files.file[0].oss_storage_class)
        self.assertEqual(2, result.files.file[0].oss_tagging_count)
        self.assertEqual('key', result.files.file[0].oss_tagging.taggings[0].key)
        self.assertEqual('val', result.files.file[0].oss_tagging.taggings[0].value)
        self.assertEqual('key2', result.files.file[0].oss_tagging.taggings[1].key)
        self.assertEqual('val2', result.files.file[0].oss_tagging.taggings[1].value)
        self.assertEqual('key', result.files.file[0].oss_user_meta.user_metas[0].key)
        self.assertEqual('val', result.files.file[0].oss_user_meta.user_metas[0].value)
        self.assertEqual('Jenny', result.files.file[1].album_artist)
        self.assertEqual('Jane', result.files.file[1].composer)
        self.assertEqual('Jane', result.files.file[1].performer)
        self.assertEqual('FirstAlbum', result.files.file[1].album)