# pylint: skip-file
import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import access_point as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from .. import MockHttpResponse

class TestCreateAccessPoint(unittest.TestCase):
    def test_constructor_request(self):
        request = model.CreateAccessPointRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.create_access_point_configuration)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.CreateAccessPointRequest(
            bucket='bucket_name',
            create_access_point_configuration=model.CreateAccessPointConfiguration(
                access_point_name='vpK w>\9WD',
                network_origin='cam+fl;W-o',
                vpc_configuration=model.AccessPointVpcConfiguration(
                    vpc_id='vIoxj64cZS',
                ),
            ),
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('vpK w>\9WD', request.create_access_point_configuration.access_point_name)
        self.assertEqual('cam+fl;W-o', request.create_access_point_configuration.network_origin)
        self.assertEqual('vIoxj64cZS', request.create_access_point_configuration.vpc_configuration.vpc_id)

    def test_serialize_request(self):
        request = model.CreateAccessPointRequest(
            bucket='bucket_name',
            create_access_point_configuration=model.CreateAccessPointConfiguration(
                access_point_name='vpK w>\9WD',
                network_origin='cam+fl;W-o',
                vpc_configuration=model.AccessPointVpcConfiguration(
                    vpc_id='vIoxj64cZS',
                ),
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='CreateAccessPoint',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('CreateAccessPoint', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.CreateAccessPointResult()
        self.assertIsNone(result.access_point_arn)
        self.assertIsNone(result.alias)
        self.assertIsInstance(result, serde.Model)

        result = model.CreateAccessPointResult(
            access_point_arn='Af#)eQ<V+;',
            alias='G|co+D*Qz&',
        )
        self.assertEqual('Af#)eQ<V+;', result.access_point_arn)
        self.assertEqual('G|co+D*Qz&', result.alias)

    def test_deserialize_result(self):
        xml_data = r'''
        <CreateAccessPointResult>
        </CreateAccessPointResult>'''

        result = model.CreateAccessPointResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <CreateAccessPointResult>
          <AccessPointArn>acs:oss:cn-hangzhou:128364106451xxxx:accesspoint/ap-01</AccessPointArn>
          <Alias>ap-01-45ee7945007a2f0bcb595f63e2215cxxxx-ossalias</Alias>
        </CreateAccessPointResult>
        '''

        result = model.CreateAccessPointResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual("acs:oss:cn-hangzhou:128364106451xxxx:accesspoint/ap-01", result.access_point_arn)
        self.assertEqual("ap-01-45ee7945007a2f0bcb595f63e2215cxxxx-ossalias", result.alias)


class TestGetAccessPoint(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetAccessPointRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetAccessPointRequest(
            bucket='bucket_name',
            access_point_name='b%K+QqKi.!',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('b%K+QqKi.!', request.access_point_name)

    def test_serialize_request(self):
        request = model.GetAccessPointRequest(
            bucket='bucket_name',
            access_point_name='b%K+QqKi.!',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetAccessPoint',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetAccessPoint', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetAccessPointResult()
        self.assertIsNone(result.account_id)
        self.assertIsNone(result.network_origin)
        self.assertIsNone(result.access_point_arn)
        self.assertIsNone(result.status)
        self.assertIsNone(result.creation_date)
        self.assertIsNone(result.access_point_name)
        self.assertIsNone(result.bucket)
        self.assertIsNone(result.endpoints)
        self.assertIsNone(result.public_access_block_configuration)
        self.assertIsNone(result.vpc_configuration)
        self.assertIsNone(result.alias)
        self.assertIsInstance(result, serde.Model)

        result = model.GetAccessPointResult(
            account_id=',:^wzJt^mL',
            network_origin='q#NCB@>n7i',
            access_point_arn='4bYlS\mkx+',
            status='OK',
            creation_date='2013-07-31T10:56:21.000Z',
            access_point_name='b%K+QqKi.!',
            bucket='bucket_name',
            endpoints=model.Endpoints(
                public_endpoint='C4+*Z!Y(A/',
                internal_endpoint='oss-cn-hangzhou-internal.aliyuncs.com',
            ),
            public_access_block_configuration=model.PublicAccessBlockConfiguration(
                block_public_access=True,
            ),
            vpc_configuration=model.AccessPointVpcConfiguration(
                vpc_id='GHJ+F)kT|;',
            ),
            alias='p$+\G)ouu7',
        )
        self.assertEqual(',:^wzJt^mL', result.account_id)
        self.assertEqual('q#NCB@>n7i', result.network_origin)
        self.assertEqual('4bYlS\mkx+', result.access_point_arn)
        self.assertEqual('OK', result.status)
        self.assertEqual('2013-07-31T10:56:21.000Z', result.creation_date)
        self.assertEqual('b%K+QqKi.!', result.access_point_name)
        self.assertEqual('bucket_name', result.bucket)
        self.assertEqual('C4+*Z!Y(A/', result.endpoints.public_endpoint)
        self.assertEqual('oss-cn-hangzhou-internal.aliyuncs.com', result.endpoints.internal_endpoint)
        self.assertEqual(True, result.public_access_block_configuration.block_public_access)
        self.assertEqual('GHJ+F)kT|;', result.vpc_configuration.vpc_id)
        self.assertEqual('p$+\G)ouu7', result.alias)

    def test_deserialize_result(self):
        xml_data = r'''
        <GetAccessPointResult>
        </GetAccessPointResult>'''

        result = model.GetAccessPointResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <GetAccessPointResult>
          <AccessPointName>ap-01</AccessPointName>
          <Bucket>oss-example</Bucket>
          <AccountId>111933544165xxxx</AccountId>
          <NetworkOrigin>vpc</NetworkOrigin>
          <VpcConfiguration>
             <VpcId>vpc-t4nlw426y44rd3iq4xxxx</VpcId>
          </VpcConfiguration>
          <AccessPointArn>arn:acs:oss:cn-hangzhou:111933544165xxxx:accesspoint/ap-01</AccessPointArn>
          <CreationDate>1626769503</CreationDate>
          <Alias>ap-01-ossalias</Alias>
          <Status>enable</Status>
          <Endpoints>
            <PublicEndpoint>ap-01.oss-cn-hangzhou.oss-accesspoint.aliyuncs.com</PublicEndpoint>
            <InternalEndpoint>ap-01.oss-cn-hangzhou-internal.oss-accesspoint.aliyuncs.com</InternalEndpoint>
          </Endpoints>
          <PublicAccessBlockConfiguration>
            <BlockPublicAccess>true</BlockPublicAccess>
          </PublicAccessBlockConfiguration>
        </GetAccessPointResult>
        '''

        result = model.GetAccessPointResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual('ap-01', result.access_point_name)
        self.assertEqual('oss-example', result.bucket)
        self.assertEqual('111933544165xxxx', result.account_id)
        self.assertEqual('vpc', result.network_origin)
        self.assertEqual('vpc-t4nlw426y44rd3iq4xxxx', result.vpc_configuration.vpc_id)
        self.assertEqual('arn:acs:oss:cn-hangzhou:111933544165xxxx:accesspoint/ap-01', result.access_point_arn)
        self.assertEqual('1626769503', result.creation_date)
        self.assertEqual('ap-01-ossalias', result.alias)
        self.assertEqual('enable', result.status)
        self.assertEqual('ap-01.oss-cn-hangzhou.oss-accesspoint.aliyuncs.com', result.endpoints.public_endpoint)
        self.assertEqual('ap-01.oss-cn-hangzhou-internal.oss-accesspoint.aliyuncs.com', result.endpoints.internal_endpoint)
        self.assertEqual(True, result.public_access_block_configuration.block_public_access)


class TestListAccessPoints(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListAccessPointsRequest(
        )
        self.assertIsNone(request.max_keys)
        self.assertIsNone(request.continuation_token)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListAccessPointsRequest(
            max_keys=10,
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
        )
        self.assertEqual(10, request.max_keys)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', request.continuation_token)

    def test_serialize_request(self):
        request = model.ListAccessPointsRequest(
            max_keys=10,
            continuation_token='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListAccessPoints',
            method='POST',
        ))
        self.assertEqual('ListAccessPoints', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual(10, int(op_input.parameters.get('max-keys')))
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', op_input.parameters.get('continuation-token'))

    def test_constructor_result(self):
        result = model.ListAccessPointsResult()
        self.assertIsNone(result.access_points)
        self.assertIsNone(result.max_keys)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.next_continuation_token)
        self.assertIsNone(result.account_id)
        self.assertIsInstance(result, serde.Model)

        result = model.ListAccessPointsResult(
            access_points=[model.AccessPoint(
                    network_origin='ZqMvUa.c.3',
                    vpc_configuration=model.AccessPointVpcConfiguration(
                        vpc_id='9e_-)l^zMh',
                    ),
                    status='OK',
                    bucket='bucket_name',
                    access_point_name='uaJtp/3 Ln',
                    alias='fF0OZck&LQ',
                ), model.AccessPoint(
                    network_origin='ZqMvUa.c.3',
                    vpc_configuration=model.AccessPointVpcConfiguration(
                        vpc_id='9e_-)l^zMh',
                    ),
                    status='OK',
                    bucket='bucket_name',
                    access_point_name='uaJtp/3 Ln',
                    alias='fF0OZck&LQ',
                )],
            max_keys=10,
            is_truncated=True,
            next_continuation_token='NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            account_id='mXXtkiJV0!',
        )

        self.assertEqual('ZqMvUa.c.3', result.access_points[0].network_origin)
        self.assertEqual('9e_-)l^zMh', result.access_points[0].vpc_configuration.vpc_id)
        self.assertEqual('OK', result.access_points[0].status)
        self.assertEqual('bucket_name', result.access_points[0].bucket)
        self.assertEqual('uaJtp/3 Ln', result.access_points[0].access_point_name)
        self.assertEqual('fF0OZck&LQ', result.access_points[0].alias)
        self.assertEqual('ZqMvUa.c.3', result.access_points[1].network_origin)
        self.assertEqual('9e_-)l^zMh', result.access_points[1].vpc_configuration.vpc_id)
        self.assertEqual('OK', result.access_points[1].status)
        self.assertEqual('bucket_name', result.access_points[1].bucket)
        self.assertEqual('uaJtp/3 Ln', result.access_points[1].access_point_name)
        self.assertEqual('fF0OZck&LQ', result.access_points[1].alias)
        self.assertEqual(10, result.max_keys)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.next_continuation_token)
        self.assertEqual('mXXtkiJV0!', result.account_id)



    def test_deserialize_result(self):
        xml_data = r'''
        <ListAccessPointsResult>
        </ListAccessPointsResult>'''

        result = model.ListAccessPointsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ListAccessPointsResult>
          <IsTruncated>true</IsTruncated>
          <NextContinuationToken>abc</NextContinuationToken>
          <AccountId>111933544165****</AccountId>
          <AccessPoints>
            <AccessPoint>
              <Bucket>oss-example</Bucket>
              <AccessPointName>ap-01</AccessPointName>
              <Alias>ap-01-ossalias</Alias>
              <NetworkOrigin>vpc</NetworkOrigin>
              <VpcConfiguration>
                <VpcId>vpc-t4nlw426y44rd3iq4****</VpcId>
              </VpcConfiguration>
              <Status>enable</Status>
            </AccessPoint>
            <AccessPoint>
              <Bucket>oss-example2</Bucket>
              <AccessPointName>ap-02</AccessPointName>
              <Alias>ap-02-ossalias</Alias>
              <NetworkOrigin>internet</NetworkOrigin>
              <VpcConfiguration>
                <VpcId>vpc-t4n3iq4****</VpcId>
              </VpcConfiguration>
              <Status>creating</Status>
            </AccessPoint>
          </AccessPoints>
        </ListAccessPointsResult>
        '''

        result = model.ListAccessPointsResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('abc', result.next_continuation_token)
        self.assertEqual('111933544165****', result.account_id)
        self.assertEqual('oss-example', result.access_points[0].bucket)
        self.assertEqual('ap-01', result.access_points[0].access_point_name)
        self.assertEqual('ap-01-ossalias', result.access_points[0].alias)
        self.assertEqual('vpc', result.access_points[0].network_origin)
        self.assertEqual('vpc-t4nlw426y44rd3iq4****', result.access_points[0].vpc_configuration.vpc_id)
        self.assertEqual('enable', result.access_points[0].status)
        self.assertEqual('oss-example2', result.access_points[1].bucket)
        self.assertEqual('ap-02', result.access_points[1].access_point_name)
        self.assertEqual('ap-02-ossalias', result.access_points[1].alias)
        self.assertEqual('internet', result.access_points[1].network_origin)
        self.assertEqual('vpc-t4n3iq4****', result.access_points[1].vpc_configuration.vpc_id)
        self.assertEqual('creating', result.access_points[1].status)


class TestDeleteAccessPoint(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteAccessPointRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteAccessPointRequest(
            bucket='bucket_name',
            access_point_name='>;ew6<fAt;',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('>;ew6<fAt;', request.access_point_name)


    def test_serialize_request(self):
        request = model.DeleteAccessPointRequest(
            bucket='bucket_name',
            access_point_name='>;ew6<fAt;',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteAccessPoint',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteAccessPoint', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteAccessPointResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteAccessPointResult()
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


class TestPutAccessPointPolicy(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutAccessPointPolicyRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_name)
        self.assertIsNone(request.body)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutAccessPointPolicyRequest(
            bucket='bucket_name',
            access_point_name='l<ILe$ rQF',
            body='xml_data',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('l<ILe$ rQF', request.access_point_name)
        self.assertEqual('xml_data', request.body)


    def test_serialize_request(self):
        request = model.PutAccessPointPolicyRequest(
            bucket='bucket_name',
            access_point_name='l<ILe$ rQF',
            body='xml_data',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutAccessPointPolicy',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutAccessPointPolicy', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.PutAccessPointPolicyResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutAccessPointPolicyResult()
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


class TestGetAccessPointPolicy(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetAccessPointPolicyRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetAccessPointPolicyRequest(
            bucket='bucket_name',
            access_point_name='y.gu>%Tu+m',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('y.gu>%Tu+m', request.access_point_name)

    def test_serialize_request(self):
        request = model.GetAccessPointPolicyRequest(
            bucket='bucket_name',
            access_point_name='y.gu>%Tu+m',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetAccessPointPolicy',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetAccessPointPolicy', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.GetAccessPointPolicyResult()
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
               "acs:oss:cn-hangzhou:111933544165xxxx:accesspoint/$ap-01",
               "acs:oss:cn-hangzhou:111933544165xxxx:accesspoint/$ap-01/object/*"
             ]
           }
          ]
         }
                '''
        result = model.GetAccessPointPolicyResult(
            body=xml_data,
        )
        self.assertEqual(xml_data, result.body)

    def test_deserialize_result(self):
        xml_data = None
        result = model.GetAccessPointPolicyResult()
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


class TestDeleteAccessPointPolicy(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteAccessPointPolicyRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.access_point_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteAccessPointPolicyRequest(
            bucket='bucket_name',
            access_point_name='\JQh0EGuR6',
        )
        self.assertEqual('bucket_name', request.bucket)
        self.assertEqual('\JQh0EGuR6', request.access_point_name)


    def test_serialize_request(self):
        request = model.DeleteAccessPointPolicyRequest(
            bucket='bucket_name',
            access_point_name='\JQh0EGuR6',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteAccessPointPolicy',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteAccessPointPolicy', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucket_name', op_input.bucket)

    def test_constructor_result(self):
        result = model.DeleteAccessPointPolicyResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteAccessPointPolicyResult()
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