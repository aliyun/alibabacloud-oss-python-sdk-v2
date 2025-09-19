# pylint: skip-file
import unittest
import xml.etree.ElementTree as ET
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import service as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from .. import MockHttpResponse



class TestListBuckets(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListBucketsRequest(
        )
        self.assertIsNone(request.prefix)
        self.assertIsNone(request.marker)
        self.assertIsNone(request.max_keys)
        self.assertIsNone(request.resource_group_id)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListBucketsRequest(
            prefix='test',
            marker='marker1',
            max_keys=100,
            resource_group_id='rg-id-123',
        )
        self.assertEqual('test', request.prefix)
        self.assertEqual('marker1', request.marker)
        self.assertEqual(100, request.max_keys)
        self.assertEqual('rg-id-123', request.resource_group_id)

    def test_serialize_request(self):
        request = model.ListBucketsRequest(
            prefix='test',
            marker='marker1',
            max_keys=100,
            resource_group_id='rg-id-123',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListBuckets',
            method='GET',
        ))
        self.assertEqual('ListBuckets', op_input.op_name)
        self.assertEqual('GET', op_input.method)

    def test_constructor_result(self):
        result = model.ListBucketsResult()
        self.assertIsNone(result.buckets)
        self.assertIsNone(result.prefix)
        self.assertIsNone(result.marker)
        self.assertIsNone(result.max_keys)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.next_marker)
        self.assertIsInstance(result, serde.Model)

        result = model.ListBucketsResult(
            prefix='test',
            marker='marker1',
            max_keys=100,
            is_truncated=False,
            next_marker='',
            buckets=[model.BucketProperties(
                name='bucket1',
                location='oss-cn-hangzhou',
                creation_date='2023-01-01T00:00:00.000Z',
            )],
        )
        self.assertEqual('test', result.prefix)
        self.assertEqual('marker1', result.marker)
        self.assertEqual(100, result.max_keys)
        self.assertEqual(False, result.is_truncated)
        self.assertEqual('bucket1', result.buckets[0].name)

    def test_deserialize_result(self):
        json_data = r'''
        <ListAllMyBucketsResult>
          <Prefix>my</Prefix>
          <Marker>mybucket</Marker>
          <MaxKeys>10</MaxKeys>
          <IsTruncated>true</IsTruncated>
          <NextMarker>mybucket10</NextMarker>
          <Owner>
            <ID>ut_test_put_bucket</ID>
            <DisplayName>ut_test_put_bucket</DisplayName>
          </Owner>
          <Buckets>
            <Bucket>
              <CreationDate>2014-05-14T11:18:32.000Z</CreationDate>
              <ExtranetEndpoint>oss-cn-hangzhou.aliyuncs.com</ExtranetEndpoint>
              <IntranetEndpoint>oss-cn-hangzhou-internal.aliyuncs.com</IntranetEndpoint>
              <Location>oss-cn-hangzhou</Location>
              <Name>mybucket01</Name>
              <Region>cn-hangzhou</Region>
              <StorageClass>Standard</StorageClass>
            </Bucket>
          </Buckets>
        </ListAllMyBucketsResult>
        '''

        result = model.ListBucketsResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=MockHttpResponse(
                body=json_data,
            )
        )

        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual('my', result.prefix)
        self.assertEqual('mybucket', result.marker)
        self.assertEqual(10, result.max_keys)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('mybucket01', result.buckets[0].name)
        self.assertEqual('oss-cn-hangzhou', result.buckets[0].location)
        self.assertEqual('2014-05-14T11:18:32.000Z', result.buckets[0].creation_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
