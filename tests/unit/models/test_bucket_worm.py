# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_worm as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestInitiateBucketWorm(unittest.TestCase):
    def test_constructor_request(self):
        request = model.InitiateBucketWormRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.initiate_worm_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.InitiateBucketWormRequest(
            bucket='bucketexampletest',
            initiate_worm_configuration=model.InitiateWormConfiguration(
                retention_period_in_days=82460,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(82460, request.initiate_worm_configuration.retention_period_in_days)

    def test_serialize_request(self):
        request = model.InitiateBucketWormRequest(
            bucket='bucketexampletest',
            initiate_worm_configuration=model.InitiateWormConfiguration(
                retention_period_in_days=82460,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='InitiateBucketWorm',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('InitiateBucketWorm', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.InitiateBucketWormResult()
        self.assertIsNone(result.worm_id)
        self.assertIsInstance(result, serde.Model)

        result = model.InitiateBucketWormResult(
            worm_id='1666E2CFB2B3418****',
        )
        self.assertEqual('1666E2CFB2B3418****', result.worm_id)

    def test_deserialize_result(self):
        xml_data = None
        result = model.InitiateBucketWormResult()
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


class TestGetBucketWorm(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketWormRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketWormRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketWormRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketWorm',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketWorm', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketWormResult()
        self.assertIsNone(result.worm_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketWormResult(
            worm_configuration=model.WormConfiguration(
                worm_id='1666E2CFB2B3418****',
                state=model.BucketWormStateType.LOCKED,
                retention_period_in_days=1,
                creation_date='2013-07-31T10:56:21.000Z',
                expiration_date='test_expiration_date',
            ),
        )
        self.assertEqual('1666E2CFB2B3418****', result.worm_configuration.worm_id)
        self.assertEqual('Locked', result.worm_configuration.state)
        self.assertEqual(1, result.worm_configuration.retention_period_in_days)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.worm_configuration.creation_date)
        self.assertEqual('test_expiration_date', result.worm_configuration.expiration_date)

        result = model.GetBucketWormResult(
            worm_configuration=model.WormConfiguration(
                worm_id='test_worm_id',
                state='Locked',
                retention_period_in_days=79782,
                creation_date='2013-07-31T10:56:21.000Z',
                expiration_date='test_expiration_date',
            ),
        )
        self.assertEqual('test_worm_id', result.worm_configuration.worm_id)
        self.assertEqual('Locked', result.worm_configuration.state)
        self.assertEqual(79782, result.worm_configuration.retention_period_in_days)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.worm_configuration.creation_date)
        self.assertEqual('test_expiration_date', result.worm_configuration.expiration_date)

    def test_deserialize_result(self):
        xml_data = r'''
        <WormConfiguration>
        </WormConfiguration>'''

        result = model.GetBucketWormResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <WormConfiguration>
          <WormId>1666E2CFB2B3418****</WormId>
          <State>Locked</State>
          <RetentionPeriodInDays>1</RetentionPeriodInDays>
          <CreationDate>2020-10-15T15:50:32</CreationDate>
        </WormConfiguration>
        '''

        result = model.GetBucketWormResult()
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
        self.assertEqual('1666E2CFB2B3418****', result.worm_configuration.worm_id)
        self.assertEqual('Locked', result.worm_configuration.state)
        self.assertEqual(1, result.worm_configuration.retention_period_in_days)
        self.assertEqual('2020-10-15T15:50:32', result.worm_configuration.creation_date)


class TestCompleteBucketWorm(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CompleteBucketWormRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.worm_id)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CompleteBucketWormRequest(
            bucket='bucketexampletest',
            worm_id='1666E2CFB2B3418****',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('1666E2CFB2B3418****', request.worm_id)

    def test_serialize_request(self):
        request = model.CompleteBucketWormRequest(
            bucket='bucketexampletest',
            worm_id='1666E2CFB2B3418****',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CompleteBucketWorm',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CompleteBucketWorm', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('1666E2CFB2B3418****', op_input.parameters.get('wormId'))

    def test_constructor_result(self):
        result = model.CompleteBucketWormResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.CompleteBucketWormResult()
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


class TestExtendBucketWorm(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ExtendBucketWormRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.worm_id)
        self.assertIsNone(request.extend_worm_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ExtendBucketWormRequest(
            bucket='bucketexampletest',
            worm_id='1666E2CFB2B3418****',
            extend_worm_configuration=model.ExtendWormConfiguration(
                retention_period_in_days=1,
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('1666E2CFB2B3418****', request.worm_id)
        self.assertEqual(1, request.extend_worm_configuration.retention_period_in_days)

    def test_serialize_request(self):
        request = model.ExtendBucketWormRequest(
            bucket='bucketexampletest',
            worm_id='1666E2CFB2B3418****',
            extend_worm_configuration=model.ExtendWormConfiguration(
                retention_period_in_days=27339,
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ExtendBucketWorm',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('ExtendBucketWorm', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('1666E2CFB2B3418****', op_input.parameters.get('wormId'))

    def test_constructor_result(self):
        result = model.ExtendBucketWormResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.ExtendBucketWormResult()
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


class TestAbortBucketWorm(unittest.TestCase):
    def test_constructor_request(self):
        request = model.AbortBucketWormRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.AbortBucketWormRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.AbortBucketWormRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='AbortBucketWorm',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('AbortBucketWorm', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.AbortBucketWormResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.AbortBucketWormResult()
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

