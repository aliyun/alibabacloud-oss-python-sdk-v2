# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_object_fc_access_point as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestCreateAccessPointForObjectProcess(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CreateAccessPointForObjectProcessRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_for_object_process_name)
        self.assertIsNone(request.create_access_point_for_object_process_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CreateAccessPointForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
            create_access_point_for_object_process_configuration=model.CreateAccessPointForObjectProcessConfiguration(
                allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
                access_point_name='ap-01',
                object_process_configuration=model.ObjectProcessConfiguration(
                    allowed_features=model.AllowedFeatures(
                        allowed_features=['GetObject-Range'],
                    ),
                    transformation_configurations=model.TransformationConfigurations(
                        transformation_configurations=[model.TransformationConfiguration(
                            actions=model.AccessPointActions(
                                actions=['GetObject'],
                            ),
                            content_transformation=model.ContentTransformation(
                                function_compute=model.FunctionCompute(
                                    function_assume_role_arn='acs:ram::111933544165****:role/aliyunfcdefaultrole',
                                    function_arn='acs:fc:cn-qingdao:111933544165****:services/test-oss-fc.LATEST/functions/fc-01',
                                ),
                                additional_features=model.AdditionalFeatures(
                                    custom_forward_headers=model.CustomForwardHeaders(
                                        custom_forward_headers=['header1', 'header2'],
                                    ),
                                ),
                            ),
                        ), model.TransformationConfiguration(
                            actions=model.AccessPointActions(
                                actions=['GetObject-Range', 'PutObject'],
                            ),
                            content_transformation=model.ContentTransformation(
                                function_compute=model.FunctionCompute(
                                    function_assume_role_arn='acs:ram::111933544165****:role/aliyunfcdefaultrole',
                                    function_arn='acs:fc:cn-qingdao:111933544165****:services/test-oss-fc.LATEST/functions/fc-01',
                                ),
                                additional_features=model.AdditionalFeatures(
                                    custom_forward_headers=model.CustomForwardHeaders(
                                        custom_forward_headers=['header2', 'header4'],
                                    ),
                                ),
                            ),
                        )],
                    ),
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_for_object_process_name', request.access_point_for_object_process_name)
        self.assertEqual('test_allow_anonymous_access_for_object_process', request.create_access_point_for_object_process_configuration.allow_anonymous_access_for_object_process)
        self.assertEqual('ap-01', request.create_access_point_for_object_process_configuration.access_point_name)
        self.assertEqual('GetObject-Range', request.create_access_point_for_object_process_configuration.object_process_configuration.allowed_features.allowed_features[0])
        self.assertEqual('GetObject', request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].actions.actions[0])
        self.assertEqual('acs:ram::111933544165****:role/aliyunfcdefaultrole', request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.function_compute.function_assume_role_arn)
        self.assertEqual('acs:fc:cn-qingdao:111933544165****:services/test-oss-fc.LATEST/functions/fc-01',
                         request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.function_compute.function_arn)
        self.assertEqual('header1', request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[0])
        self.assertEqual('header2', request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[1])
        self.assertEqual('GetObject-Range', request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].actions.actions[0])
        self.assertEqual('PutObject', request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].actions.actions[1])
        self.assertEqual('acs:ram::111933544165****:role/aliyunfcdefaultrole', request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.function_compute.function_assume_role_arn)
        self.assertEqual('acs:fc:cn-qingdao:111933544165****:services/test-oss-fc.LATEST/functions/fc-01',
                         request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.function_compute.function_arn)
        self.assertEqual('header2', request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[0])
        self.assertEqual('header4', request.create_access_point_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[1])

    def test_serialize_request(self):
        request = model.CreateAccessPointForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
            create_access_point_for_object_process_configuration=model.CreateAccessPointForObjectProcessConfiguration(
                allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
                access_point_name='ap-01',
                object_process_configuration=model.ObjectProcessConfiguration(
                    allowed_features=model.AllowedFeatures(
                        allowed_features=['GetObject-Range'],
                    ),
                    transformation_configurations=model.TransformationConfigurations(
                        transformation_configuration=[model.TransformationConfiguration(
                            actions=model.AccessPointActions(
                                actions=['GetObject'],
                            ),
                            content_transformation=model.ContentTransformation(
                                function_compute=model.FunctionCompute(
                                    function_assume_role_arn='acs:ram::111933544165****:role/aliyunfcdefaultrole',
                                    function_arn='acs:fc:cn-qingdao:111933544165****:services/test-oss-fc.LATEST/functions/fc-01',
                                ),
                                additional_features=model.AdditionalFeatures(
                                    custom_forward_headers=model.CustomForwardHeaders(
                                        custom_forward_headers=['header1', 'header2'],
                                    ),
                                ),
                            ),
                        ), model.TransformationConfiguration(
                            actions=model.AccessPointActions(
                                actions=['GetObject-Range', 'PutObject'],
                            ),
                            content_transformation=model.ContentTransformation(
                                function_compute=model.FunctionCompute(
                                    function_assume_role_arn='acs:ram::111933544165****:role/aliyunfcdefaultrole',
                                    function_arn='acs:fc:cn-qingdao:111933544165****:services/test-oss-fc.LATEST/functions/fc-01',
                                ),
                                additional_features=model.AdditionalFeatures(
                                    custom_forward_headers=model.CustomForwardHeaders(
                                        custom_forward_headers=['header2', 'header4'],
                                    ),
                                ),
                            ),
                        )],
                    ),
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CreateAccessPointForObjectProcess',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CreateAccessPointForObjectProcess', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.CreateAccessPointForObjectProcessResult()
        self.assertIsNone(result.access_point_for_object_process_alias)
        self.assertIsNone(result.access_point_for_object_process_arn)
        self.assertIsInstance(result, serde.Model)

        result = model.CreateAccessPointForObjectProcessResult(
            access_point_for_object_process_alias='test_access_point_for_object_process_alias',
            access_point_for_object_process_arn='test_access_point_for_object_process_arn',
        )
        self.assertEqual('test_access_point_for_object_process_alias', result.access_point_for_object_process_alias)
        self.assertEqual('test_access_point_for_object_process_arn', result.access_point_for_object_process_arn)

    def test_deserialize_result(self):
        xml_data = r'''
        <CreateAccessPointForObjectProcessResult>
        </CreateAccessPointForObjectProcessResult>'''

        result = model.CreateAccessPointForObjectProcessResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <CreateAccessPointForObjectProcessResult>
          <AccessPointForObjectProcessArn>acs:oss:cn-qingdao:119335441657143:accesspointforobjectprocess/fc-ap-01</AccessPointForObjectProcessArn>
          <AccessPointForObjectProcessAlias>fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias</AccessPointForObjectProcessAlias>
        </CreateAccessPointForObjectProcessResult>
        '''

        result = model.CreateAccessPointForObjectProcessResult()
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
        self.assertEqual('acs:oss:cn-qingdao:119335441657143:accesspointforobjectprocess/fc-ap-01', result.access_point_for_object_process_arn)
        self.assertEqual('fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias', result.access_point_for_object_process_alias)


class TestDeleteAccessPointForObjectProcess(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteAccessPointForObjectProcessRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_for_object_process_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteAccessPointForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_for_object_process_name', request.access_point_for_object_process_name)

    def test_serialize_request(self):
        request = model.DeleteAccessPointForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteAccessPointForObjectProcess',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteAccessPointForObjectProcess', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteAccessPointForObjectProcessResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteAccessPointForObjectProcessResult()
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


class TestGetAccessPointForObjectProcess(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetAccessPointForObjectProcessRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_for_object_process_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetAccessPointForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_for_object_process_name', request.access_point_for_object_process_name)

    def test_serialize_request(self):
        request = model.GetAccessPointForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetAccessPointForObjectProcess',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetAccessPointForObjectProcess', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetAccessPointForObjectProcessResult()
        self.assertIsNone(result.access_point_name_for_object_process)
        self.assertIsNone(result.access_point_for_object_process_alias)
        self.assertIsNone(result.account_id)
        self.assertIsNone(result.access_point_for_object_process_arn)
        self.assertIsNone(result.fc_status)
        self.assertIsNone(result.access_point_name)
        self.assertIsNone(result.creation_date)
        self.assertIsNone(result.endpoints)
        self.assertIsNone(result.allow_anonymous_access_for_object_process)
        self.assertIsNone(result.public_access_block_configuration)
        self.assertIsInstance(result, serde.Model)

        result = model.GetAccessPointForObjectProcessResult(
            access_point_name_for_object_process='fc-ap-01',
            access_point_for_object_process_alias='fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias',
            account_id='111933544165****',
            access_point_for_object_process_arn='acs:oss:cn-qingdao:11933544165****:accesspointforobjectprocess/fc-ap-01',
            fc_status='enabled',
            access_point_name='ap-01',
            creation_date='2013-07-31T10:56:21.000Z',
            endpoints=model.AccessPointEndpoints(
                public_endpoint='fc-ap-01-111933544165****.oss-cn-qingdao.oss-object-process.aliyuncs.com',
                internal_endpoint='oss-cn-hangzhou-internal.aliyuncs.com',
            ),
            allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
        )
        self.assertEqual('fc-ap-01', result.access_point_name_for_object_process)
        self.assertEqual('fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias', result.access_point_for_object_process_alias)
        self.assertEqual('111933544165****', result.account_id)
        self.assertEqual('acs:oss:cn-qingdao:11933544165****:accesspointforobjectprocess/fc-ap-01', result.access_point_for_object_process_arn)
        self.assertEqual('enabled', result.fc_status)
        self.assertEqual('ap-01', result.access_point_name)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.creation_date)
        self.assertEqual('fc-ap-01-111933544165****.oss-cn-qingdao.oss-object-process.aliyuncs.com', result.endpoints.public_endpoint)
        self.assertEqual('oss-cn-hangzhou-internal.aliyuncs.com', result.endpoints.internal_endpoint)
        self.assertEqual('test_allow_anonymous_access_for_object_process', result.allow_anonymous_access_for_object_process)
        self.assertEqual(True, result.public_access_block_configuration.block_public_access)

    def test_deserialize_result(self):
        xml_data = r'''
        <GetAccessPointForObjectProcessResult>
        </GetAccessPointForObjectProcessResult>'''

        result = model.GetAccessPointForObjectProcessResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <GetAccessPointForObjectProcessResult>
          <AccessPointNameForObjectProcess>fc-ap-01</AccessPointNameForObjectProcess>
          <AccessPointForObjectProcessAlias>fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias</AccessPointForObjectProcessAlias>
          <AccessPointName>ap-01</AccessPointName>
          <AccountId>111933544165****</AccountId>
          <AccessPointForObjectProcessArn>acs:oss:cn-qingdao:11933544165****:accesspointforobjectprocess/fc-ap-01</AccessPointForObjectProcessArn>
          <CreationDate>1626769503</CreationDate>
          <Status>enable</Status>
          <Endpoints>
            <PublicEndpoint>fc-ap-01-111933544165****.oss-cn-qingdao.oss-object-process.aliyuncs.com</PublicEndpoint>
            <InternalEndpoint>fc-ap-01-111933544165****.oss-cn-qingdao-internal.oss-object-process.aliyuncs.com</InternalEndpoint>
          </Endpoints>
          <PublicAccessBlockConfiguration>
            <BlockPublicAccess>true</BlockPublicAccess>
          </PublicAccessBlockConfiguration>
        </GetAccessPointForObjectProcessResult>
        '''

        result = model.GetAccessPointForObjectProcessResult()
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
        self.assertEqual('fc-ap-01', result.access_point_name_for_object_process)
        self.assertEqual('fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias', result.access_point_for_object_process_alias)
        self.assertEqual('ap-01', result.access_point_name)
        self.assertEqual('111933544165****', result.account_id)
        self.assertEqual('acs:oss:cn-qingdao:11933544165****:accesspointforobjectprocess/fc-ap-01', result.access_point_for_object_process_arn)
        self.assertEqual('1626769503', result.creation_date)
        self.assertEqual('enable', result.fc_status)
        self.assertEqual('fc-ap-01-111933544165****.oss-cn-qingdao.oss-object-process.aliyuncs.com', result.endpoints.public_endpoint)
        self.assertEqual('fc-ap-01-111933544165****.oss-cn-qingdao-internal.oss-object-process.aliyuncs.com', result.endpoints.internal_endpoint)
        self.assertEqual(True, result.public_access_block_configuration.block_public_access)


class TestListAccessPointsForObjectProcess(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListAccessPointsForObjectProcessRequest(
        )
        self.assertIsNone(request.max_keys)
        self.assertIsNone(request.continuation_token)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListAccessPointsForObjectProcessRequest(
            max_keys=10,
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
        )
        self.assertEqual(10, request.max_keys)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', request.continuation_token)

    def test_serialize_request(self):
        request = model.ListAccessPointsForObjectProcessRequest(
            max_keys=10,
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListAccessPointsForObjectProcess',
            method='POST',
        ))
        self.assertEqual('ListAccessPointsForObjectProcess', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual(10, int(op_input.parameters.get('max-keys')))
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', op_input.parameters.get('continuation-token'))

    def test_constructor_result(self):
        result = model.ListAccessPointsForObjectProcessResult()
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.next_continuation_token)
        self.assertIsNone(result.account_id)
        self.assertIsNone(result.access_points_for_object_process)
        self.assertIsInstance(result, serde.Model)

        result = model.ListAccessPointsForObjectProcessResult(
            is_truncated=True,
            next_continuation_token='NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            account_id='111933544165****',
            access_points_for_object_process=model.AccessPointsForObjectProcess(
                access_point_for_object_processs=[model.AccessPointForObjectProcess(
                    status='enabled',
                    allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
                    access_point_name_for_object_process='fc-ap-01',
                    access_point_for_object_process_alias='fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias',
                    access_point_name='fc-01',
                ), model.AccessPointForObjectProcess(
                    status='enabled',
                    allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
                    access_point_name_for_object_process='fc-ap-01',
                    access_point_for_object_process_alias='fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias',
                    access_point_name='fc-01',
                )],
            ),
        )
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.next_continuation_token)
        self.assertEqual('111933544165****', result.account_id)
        self.assertEqual('enabled', result.access_points_for_object_process.access_point_for_object_processs[0].status)
        self.assertEqual('test_allow_anonymous_access_for_object_process', result.access_points_for_object_process.access_point_for_object_processs[0].allow_anonymous_access_for_object_process)
        self.assertEqual('fc-ap-01', result.access_points_for_object_process.access_point_for_object_processs[0].access_point_name_for_object_process)
        self.assertEqual('fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias', result.access_points_for_object_process.access_point_for_object_processs[0].access_point_for_object_process_alias)
        self.assertEqual('fc-01', result.access_points_for_object_process.access_point_for_object_processs[0].access_point_name)
        self.assertEqual('enabled', result.access_points_for_object_process.access_point_for_object_processs[1].status)
        self.assertEqual('test_allow_anonymous_access_for_object_process', result.access_points_for_object_process.access_point_for_object_processs[1].allow_anonymous_access_for_object_process)
        self.assertEqual('fc-ap-01', result.access_points_for_object_process.access_point_for_object_processs[1].access_point_name_for_object_process)
        self.assertEqual('fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias', result.access_points_for_object_process.access_point_for_object_processs[1].access_point_for_object_process_alias)
        self.assertEqual('fc-01', result.access_points_for_object_process.access_point_for_object_processs[1].access_point_name)

    def test_deserialize_result(self):
        xml_data = r'''
        <ListAccessPointsForObjectProcessResult>
        </ListAccessPointsForObjectProcessResult>'''

        result = model.ListAccessPointsForObjectProcessResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ListAccessPointsForObjectProcessResult>
           <IsTruncated>true</IsTruncated>
           <NextContinuationToken>abc</NextContinuationToken>
           <AccountId>111933544165****</AccountId>
           <AccessPointsForObjectProcess>
              <AccessPointForObjectProcess>
                  <AccessPointNameForObjectProcess>fc-ap-01</AccessPointNameForObjectProcess>
                  <AccessPointForObjectProcessAlias>fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias</AccessPointForObjectProcessAlias>
                  <AccessPointName>fc-01</AccessPointName>
                  <Status>enable</Status>
              </AccessPointForObjectProcess>
           </AccessPointsForObjectProcess>
        </ListAccessPointsForObjectProcessResult>
        '''

        result = model.ListAccessPointsForObjectProcessResult()
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
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('abc', result.next_continuation_token)
        self.assertEqual('111933544165****', result.account_id)
        self.assertEqual('fc-ap-01', result.access_points_for_object_process.access_point_for_object_processs[0].access_point_name_for_object_process)
        self.assertEqual('fc-ap-01-3b00521f653d2b3223680ec39dbbe2****-opapalias', result.access_points_for_object_process.access_point_for_object_processs[0].access_point_for_object_process_alias)
        self.assertEqual('fc-01', result.access_points_for_object_process.access_point_for_object_processs[0].access_point_name)
        self.assertEqual('enable', result.access_points_for_object_process.access_point_for_object_processs[0].status)


class TestPutAccessPointConfigForObjectProcess(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutAccessPointConfigForObjectProcessRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_for_object_process_name)
        self.assertIsNone(request.put_access_point_config_for_object_process_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutAccessPointConfigForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='ap-test-oss-name',
            put_access_point_config_for_object_process_configuration=model.PutAccessPointConfigForObjectProcessConfiguration(
                allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
                public_access_block_configuration=model.PublicAccessBlockConfiguration(
                    block_public_access=True,
                ),
                object_process_configuration=model.ObjectProcessConfiguration(
                    allowed_features=model.AllowedFeatures(
                        allowed_features=['GetObject-Range'],
                    ),
                    transformation_configurations=model.TransformationConfigurations(
                        transformation_configurations=[model.TransformationConfiguration(
                            actions=model.AccessPointActions(
                                actions=['GetObject'],
                            ),
                            content_transformation=model.ContentTransformation(
                                function_compute=model.FunctionCompute(
                                    function_assume_role_arn='acs:oss:cn-qingdao:111933544165****:services/oss-fc.LATEST/functions/oss-fc-fc-02',
                                    function_arn='acs:ram::111933544165****:role/aliyunfcdefaultrole',
                                ),
                                additional_features=model.AdditionalFeatures(
                                    custom_forward_headers=model.CustomForwardHeaders(
                                        custom_forward_headers=['header1', 'header2'],
                                    ),
                                ),
                            ),
                        ), model.TransformationConfiguration(
                            actions=model.AccessPointActions(
                                actions=['O', 'b'],
                            ),
                            content_transformation=model.ContentTransformation(
                                function_compute=model.FunctionCompute(
                                    function_assume_role_arn='acs:oss:cn-qingdao:111933544165****:services/oss-fc.LATEST/functions/oss-fc-fc-02',
                                    function_arn='acs:ram::111933544165****:role/aliyunfcdefaultrole',
                                ),
                                additional_features=model.AdditionalFeatures(
                                    custom_forward_headers=model.CustomForwardHeaders(
                                        custom_forward_headers=['header3', 'header4'],
                                    ),
                                ),
                            ),
                        )],
                    ),
                ),
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('ap-test-oss-name', request.access_point_for_object_process_name)
        self.assertEqual('test_allow_anonymous_access_for_object_process', request.put_access_point_config_for_object_process_configuration.allow_anonymous_access_for_object_process)
        self.assertEqual(True, request.put_access_point_config_for_object_process_configuration.public_access_block_configuration.block_public_access)
        self.assertEqual('GetObject-Range', request.put_access_point_config_for_object_process_configuration.object_process_configuration.allowed_features.allowed_features[0])
        self.assertEqual('GetObject', request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].actions.actions[0])
        self.assertEqual('acs:oss:cn-qingdao:111933544165****:services/oss-fc.LATEST/functions/oss-fc-fc-02',
                         request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.function_compute.function_assume_role_arn)
        self.assertEqual('acs:ram::111933544165****:role/aliyunfcdefaultrole', request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.function_compute.function_arn)
        self.assertEqual('header1', request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[0])
        self.assertEqual('header2', request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[1])
        self.assertEqual('O', request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].actions.actions[0])
        self.assertEqual('b', request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].actions.actions[1])
        self.assertEqual('acs:oss:cn-qingdao:111933544165****:services/oss-fc.LATEST/functions/oss-fc-fc-02',
                         request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.function_compute.function_assume_role_arn)
        self.assertEqual('acs:ram::111933544165****:role/aliyunfcdefaultrole', request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.function_compute.function_arn)
        self.assertEqual('header3', request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[0])
        self.assertEqual('header4', request.put_access_point_config_for_object_process_configuration.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[1])


    def test_serialize_request(self):
        request = model.PutAccessPointConfigForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='ap-test-oss-name',
            put_access_point_config_for_object_process_configuration=model.PutAccessPointConfigForObjectProcessConfiguration(
                allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
                public_access_block_configuration=model.PublicAccessBlockConfiguration(
                    block_public_access=True,
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAccessPointConfigForObjectProcess',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutAccessPointConfigForObjectProcess', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutAccessPointConfigForObjectProcessResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutAccessPointConfigForObjectProcessResult()
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


class TestGetAccessPointConfigForObjectProcess(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetAccessPointConfigForObjectProcessRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_for_object_process_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetAccessPointConfigForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_for_object_process_name', request.access_point_for_object_process_name)

    def test_serialize_request(self):
        request = model.GetAccessPointConfigForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetAccessPointConfigForObjectProcess',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetAccessPointConfigForObjectProcess', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetAccessPointConfigForObjectProcessResult()
        self.assertIsNone(result.public_access_block_configuration)
        self.assertIsNone(result.object_process_configuration)
        self.assertIsNone(result.allow_anonymous_access_for_object_process)
        self.assertIsInstance(result, serde.Model)

        result = model.GetAccessPointConfigForObjectProcessResult(
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
            object_process_configuration=model.ObjectProcessConfiguration(
                allowed_features=model.AllowedFeatures(
                    allowed_features=['GetObject-Range'],
                ),
                transformation_configurations=model.TransformationConfigurations(
                    transformation_configurations=[model.TransformationConfiguration(
                        actions=model.AccessPointActions(
                            actions=['GetObject'],
                        ),
                        content_transformation=model.ContentTransformation(
                            function_compute=model.FunctionCompute(
                                function_assume_role_arn='acs:oss:cn-qingdao:111933544165****:services/oss-fc.LATEST/functions/oss-fc-fc-02',
                                function_arn='acs:ram::111933544165****:role/aliyunfcdefaultrole',
                            ),
                            additional_features=model.AdditionalFeatures(
                                custom_forward_headers=model.CustomForwardHeaders(
                                    custom_forward_headers=['header1', 'header2'],
                                ),
                            ),
                        ),
                    ), model.TransformationConfiguration(
                        actions=model.AccessPointActions(
                            actions=['c', 'e'],
                        ),
                        content_transformation=model.ContentTransformation(
                            function_compute=model.FunctionCompute(
                                function_assume_role_arn='acs:oss:cn-qingdao:111933544165****:services/oss-fc.LATEST/functions/oss-fc-fc-02',
                                function_arn='acs:ram::111933544165****:role/aliyunfcdefaultrole',
                            ),
                            additional_features=model.AdditionalFeatures(
                                custom_forward_headers=model.CustomForwardHeaders(
                                    custom_forward_headers=['header3', 'header4'],
                                ),
                            ),
                        ),
                    )],
                ),
            ),
            allow_anonymous_access_for_object_process='test_allow_anonymous_access_for_object_process',
        )
        self.assertEqual(True, result.public_access_block_configuration.block_public_access)
        self.assertEqual('GetObject-Range', result.object_process_configuration.allowed_features.allowed_features[0])
        self.assertEqual('GetObject', result.object_process_configuration.transformation_configurations.transformation_configurations[0].actions.actions[0])
        self.assertEqual('acs:oss:cn-qingdao:111933544165****:services/oss-fc.LATEST/functions/oss-fc-fc-02', result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.function_compute.function_assume_role_arn)
        self.assertEqual('acs:ram::111933544165****:role/aliyunfcdefaultrole', result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.function_compute.function_arn)
        self.assertEqual('header1', result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[0])
        self.assertEqual('header2', result.object_process_configuration.transformation_configurations.transformation_configurations[0].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[1])
        self.assertEqual('c', result.object_process_configuration.transformation_configurations.transformation_configurations[1].actions.actions[0])
        self.assertEqual('e', result.object_process_configuration.transformation_configurations.transformation_configurations[1].actions.actions[1])
        self.assertEqual('acs:oss:cn-qingdao:111933544165****:services/oss-fc.LATEST/functions/oss-fc-fc-02', result.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.function_compute.function_assume_role_arn)
        self.assertEqual('acs:ram::111933544165****:role/aliyunfcdefaultrole', result.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.function_compute.function_arn)
        self.assertEqual('header3', result.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[0])
        self.assertEqual('header4', result.object_process_configuration.transformation_configurations.transformation_configurations[1].content_transformation.additional_features.custom_forward_headers.custom_forward_headers[1])
        self.assertEqual('test_allow_anonymous_access_for_object_process', result.allow_anonymous_access_for_object_process)

    def test_deserialize_result(self):
        xml_data = None
        result = model.GetAccessPointConfigForObjectProcessResult()
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


class TestPutAccessPointPolicyForObjectProcess(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutAccessPointPolicyForObjectProcessRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_for_object_process_name)
        self.assertIsNone(request.body)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutAccessPointPolicyForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
            body='xml_data',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_for_object_process_name', request.access_point_for_object_process_name)
        self.assertEqual('xml_data', request.body)

    def test_serialize_request(self):
        request = model.PutAccessPointPolicyForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
            body='xml_data',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAccessPointPolicyForObjectProcess',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutAccessPointPolicyForObjectProcess', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutAccessPointPolicyForObjectProcessResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutAccessPointPolicyForObjectProcessResult()
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


class TestGetAccessPointPolicyForObjectProcess(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetAccessPointPolicyForObjectProcessRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_for_object_process_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetAccessPointPolicyForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_for_object_process_name', request.access_point_for_object_process_name)

    def test_serialize_request(self):
        request = model.GetAccessPointPolicyForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetAccessPointPolicyForObjectProcess',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetAccessPointPolicyForObjectProcess', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetAccessPointPolicyForObjectProcessResult()
        self.assertIsNone(result.body)
        self.assertIsInstance(result, serde.Model)

        xml_data = r'''
        {
           "Version":"1",
           "Statement":[
           {
             "Action":[
               "oss:PutObject",
               "oss:GetObject"
            ],
            "Effect":"Deny",
            "Principal":["27737962156157xxxx"],
            "Resource":[
               "acs:oss:cn-hangzhou:111933544165xxxx:accesspointforobjectprocess/$apop-01",
               "acs:oss:cn-hangzhou:111933544165xxxx:accesspointforobjectprocess/$apop-01/object/*"
             ]
           }
          ]
         }
                '''

        result = model.GetAccessPointPolicyForObjectProcessResult(
            body=xml_data,
        )
        self.assertEqual(xml_data, result.body)

    def test_deserialize_result(self):
        xml_data = None
        result = model.GetAccessPointPolicyForObjectProcessResult()
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


class TestDeleteAccessPointPolicyForObjectProcess(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteAccessPointPolicyForObjectProcessRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_for_object_process_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteAccessPointPolicyForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('test_access_point_for_object_process_name', request.access_point_for_object_process_name)

    def test_serialize_request(self):
        request = model.DeleteAccessPointPolicyForObjectProcessRequest(
            bucket='bucketexampletest',
            access_point_for_object_process_name='test_access_point_for_object_process_name',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteAccessPointPolicyForObjectProcess',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteAccessPointPolicyForObjectProcess', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteAccessPointPolicyForObjectProcessResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteAccessPointPolicyForObjectProcessResult()
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


class TestWriteGetObjectResponse(unittest.TestCase):
    def test_constructor_request(self):
        request = model.WriteGetObjectResponseRequest(
        )
        self.assertIsNone(request.request_route)
        self.assertIsNone(request.request_token)
        self.assertIsNone(request.fwd_status)
        self.assertIsNone(request.fwd_header_accept_ranges)
        self.assertIsNone(request.fwd_header_cache_control)
        self.assertIsNone(request.fwd_header_content_disposition)
        self.assertIsNone(request.fwd_header_content_encoding)
        self.assertIsNone(request.fwd_header_content_language)
        self.assertIsNone(request.fwd_header_content_range)
        self.assertIsNone(request.fwd_header_content_type)
        self.assertIsNone(request.fwd_header_etag)
        self.assertIsNone(request.fwd_header_expires)
        self.assertIsNone(request.fwd_header_last_modified)
        self.assertIsNone(request.body)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.WriteGetObjectResponseRequest(
            request_route='RouteFromFcEvent',
            request_token='TokenFromFcEvent',
            fwd_status='200',
            fwd_header_accept_ranges='bytes',
            fwd_header_cache_control='no-cache',
            fwd_header_content_disposition='attachment',
            fwd_header_content_encoding='gzip',
            fwd_header_content_language='en',
            fwd_header_content_range='bytes 0-9/67589',
            fwd_header_content_type='text/html; charset=utf-8',
            fwd_header_etag='D41D8CD98F00B204E9800998ECF8****',
            fwd_header_expires='Fri, 10 Nov 2023 03:17:58 GMT',
            fwd_header_last_modified='Tue, 10 Oct 2023 03:17:58 GMT',
            body='data',
        )
        self.assertEqual('RouteFromFcEvent', request.request_route)
        self.assertEqual('TokenFromFcEvent', request.request_token)
        self.assertEqual('200', request.fwd_status)
        self.assertEqual('bytes', request.fwd_header_accept_ranges)
        self.assertEqual('no-cache', request.fwd_header_cache_control)
        self.assertEqual('attachment', request.fwd_header_content_disposition)
        self.assertEqual('gzip', request.fwd_header_content_encoding)
        self.assertEqual('en', request.fwd_header_content_language)
        self.assertEqual('bytes 0-9/67589', request.fwd_header_content_range)
        self.assertEqual('text/html; charset=utf-8', request.fwd_header_content_type)
        self.assertEqual('D41D8CD98F00B204E9800998ECF8****', request.fwd_header_etag)
        self.assertEqual('Fri, 10 Nov 2023 03:17:58 GMT', request.fwd_header_expires)
        self.assertEqual('Tue, 10 Oct 2023 03:17:58 GMT', request.fwd_header_last_modified)
        self.assertEqual('data', request.body)

    def test_serialize_request(self):
        request = model.WriteGetObjectResponseRequest(
            request_route='test_request_route',
            request_token='test_request_token',
            fwd_status='test_fwd_status',
            fwd_header_accept_ranges='test_fwd_header_accept_ranges',
            fwd_header_cache_control='test_fwd_header_cache_control',
            fwd_header_content_disposition='test_fwd_header_content_disposition',
            fwd_header_content_encoding='test_fwd_header_content_encoding',
            fwd_header_content_language='test_fwd_header_content_language',
            fwd_header_content_range='test_fwd_header_content_range',
            fwd_header_content_type='test_fwd_header_content_type',
            fwd_header_etag='test_fwd_header_etag',
            fwd_header_expires='test_fwd_header_expires',
            fwd_header_last_modified='test_fwd_header_last_modified',
            body='xml_data',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='WriteGetObjectResponse',
            method='GET',
        ))
        self.assertEqual('WriteGetObjectResponse', op_input.op_name)
        self.assertEqual('GET', op_input.method)

    def test_constructor_result(self):
        result = model.WriteGetObjectResponseResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.WriteGetObjectResponseResult()
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

