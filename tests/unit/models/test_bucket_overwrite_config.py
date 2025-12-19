# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_overwrite_config as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketOverwriteConfig(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketOverwriteConfigRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.overwrite_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketOverwriteConfigRequest(
            bucket='bucketexampletest',
            overwrite_configuration=model.OverwriteConfiguration(
                rules=[
                    model.OverwriteRule(
                        id='rule1',
                        action='forbid',
                        prefix='a/',
                        suffix='.txt',
                        principals=model.OverwritePrincipals(
                            principals=['111', '222']
                        )
                    ),
                    model.OverwriteRule(
                        id='rule2',
                        action='forbid',
                        prefix='b/',
                        suffix='.jpg',
                        principals=model.OverwritePrincipals(
                            principals=['333']
                        )
                    )
                ],
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('rule1', request.overwrite_configuration.rules[0].id)
        self.assertEqual('forbid', request.overwrite_configuration.rules[0].action)
        self.assertEqual('a/', request.overwrite_configuration.rules[0].prefix)
        self.assertEqual('.txt', request.overwrite_configuration.rules[0].suffix)
        self.assertEqual('111', request.overwrite_configuration.rules[0].principals.principals[0])
        self.assertEqual('222', request.overwrite_configuration.rules[0].principals.principals[1])
        self.assertEqual('rule2', request.overwrite_configuration.rules[1].id)
        self.assertEqual('forbid', request.overwrite_configuration.rules[1].action)
        self.assertEqual('b/', request.overwrite_configuration.rules[1].prefix)
        self.assertEqual('.jpg', request.overwrite_configuration.rules[1].suffix)
        self.assertEqual('333', request.overwrite_configuration.rules[1].principals.principals[0])

    def test_serialize_request(self):
        request = model.PutBucketOverwriteConfigRequest(
            bucket='bucketexampletest',
            overwrite_configuration=model.OverwriteConfiguration(
                rules=[
                    model.OverwriteRule(
                        id='rule1',
                        action='forbid',
                        prefix='a/',
                        suffix='.txt',
                        principals=model.OverwritePrincipals(
                            principals=['111', '222']
                        )
                    ),
                    model.OverwriteRule(
                        id='rule2',
                        action='forbid',
                        prefix='b/',
                        suffix='.jpg',
                        principals=model.OverwritePrincipals(
                            principals=['333']
                        )
                    )
                ],
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketOverwriteConfig',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketOverwriteConfig', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketOverwriteConfigResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketOverwriteConfigResult()
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


class TestGetBucketOverwriteConfig(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketOverwriteConfigRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketOverwriteConfigRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketOverwriteConfigRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketOverwriteConfig',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketOverwriteConfig', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketOverwriteConfigResult()
        self.assertIsNone(result.overwrite_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketOverwriteConfigResult(
            overwrite_configuration=model.OverwriteConfiguration(
                rules=[
                    model.OverwriteRule(
                        id='rule1',
                        action='forbid',
                        prefix='a/',
                        suffix='.txt',
                        principals=model.OverwritePrincipals(
                            principals=['111', '222']
                        )
                    ),
                    model.OverwriteRule(
                        id='rule2',
                        action='forbid',
                        prefix='b/',
                        suffix='.jpg',
                        principals=model.OverwritePrincipals(
                            principals=['333']
                        )
                    )
                ],
            ),
        )
        self.assertEqual('rule1', result.overwrite_configuration.rules[0].id)
        self.assertEqual('forbid', result.overwrite_configuration.rules[0].action)
        self.assertEqual('a/', result.overwrite_configuration.rules[0].prefix)
        self.assertEqual('.txt', result.overwrite_configuration.rules[0].suffix)
        self.assertEqual('111', result.overwrite_configuration.rules[0].principals.principals[0])
        self.assertEqual('222', result.overwrite_configuration.rules[0].principals.principals[1])
        self.assertEqual('rule2', result.overwrite_configuration.rules[1].id)
        self.assertEqual('forbid', result.overwrite_configuration.rules[1].action)
        self.assertEqual('b/', result.overwrite_configuration.rules[1].prefix)
        self.assertEqual('.jpg', result.overwrite_configuration.rules[1].suffix)
        self.assertEqual('333', result.overwrite_configuration.rules[1].principals.principals[0])

    def test_deserialize_result(self):
        xml_data = r'''
        <OverwriteConfiguration>
        </OverwriteConfiguration>'''

        result = model.GetBucketOverwriteConfigResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
            <OverwriteConfiguration>
            <Rule>
                <ID>forbid-write-rule1</ID>
                <Action>forbid</Action>
                <Prefix>a/</Prefix>
                <Suffix>.txt</Suffix>
                <Principals>
                    <Principal>27737962156157xxxx</Principal>
                </Principals>
            </Rule>
            </OverwriteConfiguration>
            '''

        result = model.GetBucketOverwriteConfigResult()
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
        self.assertEqual('forbid-write-rule1', result.overwrite_configuration.rules[0].id)
        self.assertEqual('forbid', result.overwrite_configuration.rules[0].action)
        self.assertEqual('a/', result.overwrite_configuration.rules[0].prefix)
        self.assertEqual('.txt', result.overwrite_configuration.rules[0].suffix)
        self.assertEqual('27737962156157xxxx', result.overwrite_configuration.rules[0].principals.principals[0])
        self.assertEqual(1, len(result.overwrite_configuration.rules[0].principals.principals))


class TestDeleteBucketOverwriteConfig(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketOverwriteConfigRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketOverwriteConfigRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)


    def test_serialize_request(self):
        request = model.DeleteBucketOverwriteConfigRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketOverwriteConfig',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketOverwriteConfig', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketOverwriteConfigResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketOverwriteConfigResult()
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
