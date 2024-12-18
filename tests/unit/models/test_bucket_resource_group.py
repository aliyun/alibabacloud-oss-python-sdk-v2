# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_resource_group as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestPutBucketResourceGroup(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketResourceGroupRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.bucket_resource_group_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketResourceGroupRequest(
            bucket='bucketexampletest',
            bucket_resource_group_configuration=model.BucketResourceGroupConfiguration(
                resource_group_id='rg-id',
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('rg-id', request.bucket_resource_group_configuration.resource_group_id)

    def test_serialize_request(self):
        request = model.PutBucketResourceGroupRequest(
            bucket='bucketexampletest',
            bucket_resource_group_configuration=model.BucketResourceGroupConfiguration(
                resource_group_id='rg-id',
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketResourceGroup',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketResourceGroup', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketResourceGroupResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketResourceGroupResult()
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


class TestGetBucketResourceGroup(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketResourceGroupRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketResourceGroupRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketResourceGroupRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketResourceGroup',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketResourceGroup', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketResourceGroupResult()
        self.assertIsNone(result.bucket_resource_group_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketResourceGroupResult(
            bucket_resource_group_configuration=model.BucketResourceGroupConfiguration(
                resource_group_id='rg-id',
            ),
        )
        self.assertEqual('rg-id', result.bucket_resource_group_configuration.resource_group_id)

    def test_deserialize_result(self):
        xml_data = r'''
        <BucketResourceGroupConfiguration>
        </BucketResourceGroupConfiguration>'''

        result = model.GetBucketResourceGroupResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <BucketResourceGroupConfiguration>
          <ResourceGroupId>rg-xxxxxx</ResourceGroupId>
        </BucketResourceGroupConfiguration>
        '''

        result = model.GetBucketResourceGroupResult()
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
        self.assertEqual('rg-xxxxxx', result.bucket_resource_group_configuration.resource_group_id)

