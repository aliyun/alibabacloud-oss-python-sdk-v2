# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_tags as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestPutBucketTags(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketTagsRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.tagging)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketTagsRequest(
            bucket='bucketexampletest',
            tagging=model.Tagging(
                tag_set=model.TagSet(
                    tags=[model.Tag(
                        key='test_key',
                        value='test_value',
                    ), model.Tag(
                        key='test_key',
                        value='test_value',
                    )],
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_key', request.tagging.tag_set.tags[0].key)
        self.assertEqual('test_value', request.tagging.tag_set.tags[0].value)
        self.assertEqual('test_key', request.tagging.tag_set.tags[1].key)
        self.assertEqual('test_value', request.tagging.tag_set.tags[1].value)

    def test_serialize_request(self):
        request = model.PutBucketTagsRequest(
            bucket='bucketexampletest',
            tagging=model.Tagging(
                tag_set=model.TagSet(
                    tags=[model.Tag(
                        key='test_key',
                        value='test_value',
                    ), model.Tag(
                        key='test_key',
                        value='test_value',
                    )],
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketTags',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketTags', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketTagsResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketTagsResult()
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


class TestGetBucketTags(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketTagsRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketTagsRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketTagsRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketTags',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketTags', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketTagsResult()
        self.assertIsNone(result.tagging)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketTagsResult(
            tagging=model.Tagging(
                tag_set=model.TagSet(
                    tags=[model.Tag(
                        key='testa',
                        value='test_value',
                    ), model.Tag(
                        key='testb',
                        value='test2_value',
                    )],
                ),
            ),
        )
        self.assertEqual('testa', result.tagging.tag_set.tags[0].key)
        self.assertEqual('test_value', result.tagging.tag_set.tags[0].value)
        self.assertEqual('testb', result.tagging.tag_set.tags[1].key)
        self.assertEqual('test2_value', result.tagging.tag_set.tags[1].value)

    def test_deserialize_result(self):
        xml_data = r'''
        <Tagging>
        </Tagging>'''

        result = model.GetBucketTagsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <Tagging>
          <TagSet>
            <Tag>
              <Key>testa</Key>
              <Value>value1-test</Value>
            </Tag>
            <Tag>
              <Key>testb</Key>
              <Value>value2-test</Value>
            </Tag>
          </TagSet>
        </Tagging>
        '''

        result = model.GetBucketTagsResult()
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
        self.assertEqual('testa', result.tagging.tag_set.tags[0].key)
        self.assertEqual('value1-test', result.tagging.tag_set.tags[0].value)
        self.assertEqual('testb', result.tagging.tag_set.tags[1].key)
        self.assertEqual('value2-test', result.tagging.tag_set.tags[1].value)


class TestDeleteBucketTags(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketTagsRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketTagsRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.DeleteBucketTagsRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketTags',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketTags', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketTagsResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketTagsResult()
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

