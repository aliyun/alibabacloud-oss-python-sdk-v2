# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_logging as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutBucketLogging(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutBucketLoggingRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.bucket_logging_status)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutBucketLoggingRequest(
            bucket='bucketexampletest',
            bucket_logging_status=model.BucketLoggingStatus(
                logging_enabled=model.LoggingEnabled(
                    target_bucket='q7~sjKc_Lw',
                    target_prefix='aE>@%ITkxX',
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('q7~sjKc_Lw', request.bucket_logging_status.logging_enabled.target_bucket)
        self.assertEqual('aE>@%ITkxX', request.bucket_logging_status.logging_enabled.target_prefix)


    def test_serialize_request(self):
        request = model.PutBucketLoggingRequest(
            bucket='bucketexampletest',
            bucket_logging_status=model.BucketLoggingStatus(
                logging_enabled=model.LoggingEnabled(
                    target_bucket='q7~sjKc_Lw',
                    target_prefix='aE>@%ITkxX',
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutBucketLogging',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutBucketLogging', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutBucketLoggingResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutBucketLoggingResult()
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


class TestGetBucketLogging(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetBucketLoggingRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetBucketLoggingRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetBucketLoggingRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetBucketLogging',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetBucketLogging', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetBucketLoggingResult()
        self.assertIsNone(result.bucket_logging_status)
        self.assertIsInstance(result, serde.Model)

        result = model.GetBucketLoggingResult(
            bucket_logging_status=model.BucketLoggingStatus(
                logging_enabled=model.LoggingEnabled(
                    target_bucket='DJY#CRoJqv',
                    target_prefix='<2CcRt55A#',
                ),
            ),
        )
        self.assertEqual('DJY#CRoJqv', result.bucket_logging_status.logging_enabled.target_bucket)
        self.assertEqual('<2CcRt55A#', result.bucket_logging_status.logging_enabled.target_prefix)

    def test_deserialize_result(self):
        xml_data = r'''
        <BucketLoggingStatus>
        </BucketLoggingStatus>'''

        result = model.GetBucketLoggingResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <BucketLoggingStatus>
            <LoggingEnabled>
                <TargetBucket>mybucketlogs</TargetBucket>
                <TargetPrefix>mybucket-access_log/</TargetPrefix>
            </LoggingEnabled>
        </BucketLoggingStatus>
        '''

        result = model.GetBucketLoggingResult()
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
        self.assertEqual('mybucketlogs', result.bucket_logging_status.logging_enabled.target_bucket)
        self.assertEqual('mybucket-access_log/', result.bucket_logging_status.logging_enabled.target_prefix)


class TestDeleteBucketLogging(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteBucketLoggingRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteBucketLoggingRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.DeleteBucketLoggingRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteBucketLogging',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteBucketLogging', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteBucketLoggingResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteBucketLoggingResult()
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


class TestPutUserDefinedLogFieldsConfig(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutUserDefinedLogFieldsConfigRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.user_defined_log_fields_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutUserDefinedLogFieldsConfigRequest(
            bucket='bucketexampletest',
            user_defined_log_fields_configuration=model.UserDefinedLogFieldsConfiguration(
                header_set=model.HeaderSet(
                    headers=['9&12.KFliV', 'yi;ml47g)I'],
                ),
                param_set=model.ParamSet(
                    parameters=['-eDOon2&)', '0t,aKLN.D'],
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual(['9&12.KFliV', 'yi;ml47g)I'], request.user_defined_log_fields_configuration.header_set.headers)
        self.assertEqual(['-eDOon2&)', '0t,aKLN.D'], request.user_defined_log_fields_configuration.param_set.parameters)

    def test_serialize_request(self):
        request = model.PutUserDefinedLogFieldsConfigRequest(
            bucket='bucketexampletest',
            user_defined_log_fields_configuration=model.UserDefinedLogFieldsConfiguration(
                header_set=model.HeaderSet(
                    headers=[';%6s7q?iA!', 'brglo!jUY+'],
                ),
                param_set=model.ParamSet(
                    parameters=['0LD.sRxO!3', '7LM2WBSfIn'],
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutUserDefinedLogFieldsConfig',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutUserDefinedLogFieldsConfig', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutUserDefinedLogFieldsConfigResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutUserDefinedLogFieldsConfigResult()
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


class TestGetUserDefinedLogFieldsConfig(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetUserDefinedLogFieldsConfigRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetUserDefinedLogFieldsConfigRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.GetUserDefinedLogFieldsConfigRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetUserDefinedLogFieldsConfig',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetUserDefinedLogFieldsConfig', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetUserDefinedLogFieldsConfigResult()
        self.assertIsNone(result.user_defined_log_fields_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetUserDefinedLogFieldsConfigResult(
            user_defined_log_fields_configuration=model.UserDefinedLogFieldsConfiguration(
                header_set=model.HeaderSet(
                    headers=['0(&Cy#l- 9', '#JMia::(!L'],
                ),
                param_set=model.ParamSet(
                    parameters=['iwS;(tE,lo', 'Qlu)DhOs|)'],
                ),
            ),
        )
        self.assertEqual(['0(&Cy#l- 9', '#JMia::(!L'], result.user_defined_log_fields_configuration.header_set.headers)
        self.assertEqual(['iwS;(tE,lo', 'Qlu)DhOs|)'], result.user_defined_log_fields_configuration.param_set.parameters)

    def test_deserialize_result(self):
        xml_data = r'''
        <UserDefinedLogFieldsConfiguration>
        </UserDefinedLogFieldsConfiguration>'''

        result = model.GetUserDefinedLogFieldsConfigResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <UserDefinedLogFieldsConfiguration>
            <HeaderSet>
                <header>header1</header>
                <header>header2</header>
                <header>header3</header>
            </HeaderSet>
            <ParamSet>
                <parameter>param1</parameter>
                <parameter>param2</parameter>
            </ParamSet>
        </UserDefinedLogFieldsConfiguration>
        '''

        result = model.GetUserDefinedLogFieldsConfigResult()
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
        self.assertEqual('header1', result.user_defined_log_fields_configuration.header_set.headers[0])
        self.assertEqual('header2', result.user_defined_log_fields_configuration.header_set.headers[1])
        self.assertEqual('header3', result.user_defined_log_fields_configuration.header_set.headers[2])
        self.assertEqual('param1', result.user_defined_log_fields_configuration.param_set.parameters[0])
        self.assertEqual('param2', result.user_defined_log_fields_configuration.param_set.parameters[1])


class TestDeleteUserDefinedLogFieldsConfig(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteUserDefinedLogFieldsConfigRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteUserDefinedLogFieldsConfigRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.DeleteUserDefinedLogFieldsConfigRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteUserDefinedLogFieldsConfig',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteUserDefinedLogFieldsConfig', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteUserDefinedLogFieldsConfigResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteUserDefinedLogFieldsConfigResult()
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

