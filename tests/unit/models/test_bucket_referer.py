# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_referer as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketReferer(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketRefererRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.referer_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketRefererRequest(
            bucket='bucketexampletest',
            referer_configuration=model.RefererConfiguration(
                allow_empty_referer=False,
                allow_truncate_query_string=True,
                truncate_path=False,
                referer_list=model.RefererList(
                    referers=['http://www.aliyun.com', 'https://www.aliyun.com'],
                ),
                referer_blacklist=model.RefererBlacklist(
                    referers=['http://www.refuse.com', 'http://www.refuse1.com'],
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(False, request.referer_configuration.allow_empty_referer)
        self.assertEqual(True, request.referer_configuration.allow_truncate_query_string)
        self.assertEqual(False, request.referer_configuration.truncate_path)
        self.assertEqual(['http://www.aliyun.com', 'https://www.aliyun.com'], request.referer_configuration.referer_list.referers)
        self.assertEqual(['http://www.refuse.com', 'http://www.refuse1.com'], request.referer_configuration.referer_blacklist.referers)


    def test_serialize_request(self):
        request = model.PutBucketRefererRequest(
            bucket='bucketexampletest',
            referer_configuration=model.RefererConfiguration(
                allow_empty_referer=False,
                allow_truncate_query_string=True,
                truncate_path=False,
                referer_list=model.RefererList(
                    referers=['http://www.aliyun.com', 'https://www.aliyun.com'],
                ),
                referer_blacklist=model.RefererBlacklist(
                    referers=['http://www.refuse.com', 'http://www.refuse1.com'],
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketReferer',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketReferer', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketRefererResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketRefererResult()
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


class TestGetBucketReferer(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketRefererRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketRefererRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketRefererRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketReferer',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketReferer', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketRefererResult()
        self.assertIsNone(result.referer_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketRefererResult(
            referer_configuration=model.RefererConfiguration(
                allow_empty_referer=True,
                allow_truncate_query_string=False,
                truncate_path=True,
                referer_list=model.RefererList(
                    referers=['http://www.aliyun.com', 'https://www.aliyun.com'],
                ),
                referer_blacklist=model.RefererBlacklist(
                    referers=['http://www.refuse.com', 'http://www.refuse1.com'],
                ),
            ),
        )
        self.assertEqual(True, result.referer_configuration.allow_empty_referer)
        self.assertEqual(False, result.referer_configuration.allow_truncate_query_string)
        self.assertEqual(True, result.referer_configuration.truncate_path)
        self.assertEqual(['http://www.aliyun.com', 'https://www.aliyun.com'], result.referer_configuration.referer_list.referers)
        self.assertEqual(['http://www.refuse.com', 'http://www.refuse1.com'], result.referer_configuration.referer_blacklist.referers)

    def test_deserialize_result(self):
        xml_data = r'''
        <RefererConfiguration>
        </RefererConfiguration>'''

        result = model.GetBucketRefererResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <RefererConfiguration>
          <AllowEmptyReferer>false</AllowEmptyReferer>
          <AllowTruncateQueryString>true</AllowTruncateQueryString>
          <TruncatePath>true</TruncatePath>
          <RefererList>
            <Referer>http://www.aliyun.com</Referer>
            <Referer>https://www.aliyun.com</Referer>
            <Referer>http://www.*.com</Referer>
            <Referer>https://www.?.aliyuncs.com</Referer>
          </RefererList>
          <RefererBlacklist>
            <Referer>http://www.refuse.com</Referer>
            <Referer>https://*.hack.com</Referer>
            <Referer>http://ban.*.com</Referer>
            <Referer>https://www.?.deny.com</Referer>
          </RefererBlacklist>
        </RefererConfiguration>
        '''

        result = model.GetBucketRefererResult()
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
        self.assertEqual(False, result.referer_configuration.allow_empty_referer)
        self.assertEqual(True, result.referer_configuration.allow_truncate_query_string)
        self.assertEqual(True, result.referer_configuration.truncate_path)
        self.assertEqual('http://www.aliyun.com', result.referer_configuration.referer_list.referers[0])
        self.assertEqual('https://www.aliyun.com', result.referer_configuration.referer_list.referers[1])
        self.assertEqual('http://www.*.com', result.referer_configuration.referer_list.referers[2])
        self.assertEqual('https://www.?.aliyuncs.com', result.referer_configuration.referer_list.referers[3])
        self.assertEqual('http://www.refuse.com', result.referer_configuration.referer_blacklist.referers[0])
        self.assertEqual('https://*.hack.com', result.referer_configuration.referer_blacklist.referers[1])
        self.assertEqual('http://ban.*.com', result.referer_configuration.referer_blacklist.referers[2])
        self.assertEqual('https://www.?.deny.com', result.referer_configuration.referer_blacklist.referers[3])

