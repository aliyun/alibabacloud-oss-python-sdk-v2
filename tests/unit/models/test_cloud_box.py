# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import cloud_box as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse


class TestListCloudBoxes(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListCloudBoxesRequest(
        )
        self.assertIsNone(request.marker)
        self.assertIsNone(request.max_keys)
        self.assertIsNone(request.prefix)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListCloudBoxesRequest(
            marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa/',
        )
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', request.marker)
        self.assertEqual(10, request.max_keys)
        self.assertEqual('aaa/', request.prefix)

    def test_serialize_request(self):
        request = model.ListCloudBoxesRequest(
            marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            prefix='aaa/',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListCloudBoxes',
            method='POST',
        ))
        self.assertEqual('ListCloudBoxes', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', op_input.parameters.get('marker'))
        self.assertEqual(10, int(op_input.parameters.get('max-keys')))
        self.assertEqual('aaa/', op_input.parameters.get('prefix'))

    def test_constructor_result(self):
        result = model.ListCloudBoxesResult()
        self.assertIsNone(result.prefix)
        self.assertIsNone(result.marker)
        self.assertIsNone(result.max_keys)
        self.assertIsNone(result.is_truncated)
        self.assertIsNone(result.next_marker)
        self.assertIsNone(result.owner)
        self.assertIsNone(result.cloud_boxes)
        self.assertIsInstance(result, serde.Model)

        result = model.ListCloudBoxesResult(
            prefix='aaa/',
            marker='ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            max_keys=10,
            is_truncated=True,
            next_marker='NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA',
            owner=model.Owner(
                id='0022012****',
                display_name='user_example',
            ),
            cloud_boxes=[model.CloudBoxProperties(
                id='0022012****',
                name='example-bucket',
                region='oss-cn-hangzhou',
                control_endpoint='cb-f8z7yvzgwfkl9q0h****.cn-shanghai.oss-cloudbox-control.aliyuncs.com',
                data_endpoint='cb-f8z7yvzgwfkl9q0h****.cn-shanghai.oss-cloudbox.aliyuncs.com',
                alias='test_alias',
            ), model.CloudBoxProperties(
                id='0022012****',
                name='example-bucket',
                region='oss-cn-hangzhou',
                control_endpoint='cb-f9z7yvzgwfkl9q0h****.cn-hangzhou.oss-cloudbox-control.aliyuncs.com',
                data_endpoint='cb-f9z7yvzgwfkl9q0h****.cn-hangzhou.oss-cloudbox.aliyuncs.com',
                alias='test_alias',
            )],
        )
        self.assertEqual('aaa/', result.prefix)
        self.assertEqual('ChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.marker)
        self.assertEqual(10, result.max_keys)
        self.assertEqual(True, result.is_truncated)
        self.assertEqual('NextChR1c2VyL2VyaWMvZGVtbzMuanNvbhAA', result.next_marker)
        self.assertEqual('0022012****', result.owner.id)
        self.assertEqual('user_example', result.owner.display_name)
        self.assertEqual('0022012****', result.cloud_boxes[0].id)
        self.assertEqual('example-bucket', result.cloud_boxes[0].name)
        self.assertEqual('oss-cn-hangzhou', result.cloud_boxes[0].region)
        self.assertEqual('cb-f8z7yvzgwfkl9q0h****.cn-shanghai.oss-cloudbox-control.aliyuncs.com', result.cloud_boxes[0].control_endpoint)
        self.assertEqual('cb-f8z7yvzgwfkl9q0h****.cn-shanghai.oss-cloudbox.aliyuncs.com', result.cloud_boxes[0].data_endpoint)
        self.assertEqual('test_alias', result.cloud_boxes[0].alias)
        self.assertEqual('0022012****', result.cloud_boxes[1].id)
        self.assertEqual('example-bucket', result.cloud_boxes[1].name)
        self.assertEqual('oss-cn-hangzhou', result.cloud_boxes[1].region)
        self.assertEqual('cb-f9z7yvzgwfkl9q0h****.cn-hangzhou.oss-cloudbox-control.aliyuncs.com', result.cloud_boxes[1].control_endpoint)
        self.assertEqual('cb-f9z7yvzgwfkl9q0h****.cn-hangzhou.oss-cloudbox.aliyuncs.com', result.cloud_boxes[1].data_endpoint)
        self.assertEqual('test_alias', result.cloud_boxes[1].alias)

    def test_deserialize_result(self):
        xml_data = r'''
        <ListCloudBoxResult>
        </ListCloudBoxResult>'''

        result = model.ListCloudBoxesResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <ListCloudBoxResult>
          <Owner>
             <ID>51264</ID>
            <DisplayName>51264</DisplayName>
          </Owner>
          <CloudBoxes>
            <CloudBox>
              <ID>cb-f8z7yvzgwfkl9q0h****</ID>
              <Name>bucket1</Name>
              <Region>cn-shanghai</Region>
              <ControlEndpoint>cb-f8z7yvzgwfkl9q0h****.cn-shanghai.oss-cloudbox-control.aliyuncs.com</ControlEndpoint>
              <DataEndpoint>cb-f8z7yvzgwfkl9q0h****.cn-shanghai.oss-cloudbox.aliyuncs.com</DataEndpoint>
              <Alias>cb-f8z7yvzgwfkl9q0h****</Alias>
            </CloudBox>
            <CloudBox>
              <ID>cb-f9z7yvzgwfkl9q0h****</ID>
              <Name>bucket2</Name>
              <Region>cn-hangzhou</Region>
              <ControlEndpoint>cb-f9z7yvzgwfkl9q0h****.cn-hangzhou.oss-cloudbox-control.aliyuncs.com</ControlEndpoint>
              <DataEndpoint>cb-f9z7yvzgwfkl9q0h****.cn-hangzhou.oss-cloudbox.aliyuncs.com</DataEndpoint>
            </CloudBox>
          </CloudBoxes>
        </ListCloudBoxResult>
        '''

        result = model.ListCloudBoxesResult()
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
        self.assertEqual('51264', result.owner.id)
        self.assertEqual('51264', result.owner.display_name)
        self.assertEqual('cb-f8z7yvzgwfkl9q0h****', result.cloud_boxes[0].id)
        self.assertEqual('bucket1', result.cloud_boxes[0].name)
        self.assertEqual('cn-shanghai', result.cloud_boxes[0].region)
        self.assertEqual('cb-f8z7yvzgwfkl9q0h****.cn-shanghai.oss-cloudbox-control.aliyuncs.com', result.cloud_boxes[0].control_endpoint)
        self.assertEqual('cb-f8z7yvzgwfkl9q0h****.cn-shanghai.oss-cloudbox.aliyuncs.com', result.cloud_boxes[0].data_endpoint)
        self.assertEqual('cb-f8z7yvzgwfkl9q0h****', result.cloud_boxes[0].alias)
        self.assertEqual('cb-f9z7yvzgwfkl9q0h****', result.cloud_boxes[1].id)
        self.assertEqual('bucket2', result.cloud_boxes[1].name)
        self.assertEqual('cn-hangzhou', result.cloud_boxes[1].region)
        self.assertEqual('cb-f9z7yvzgwfkl9q0h****.cn-hangzhou.oss-cloudbox-control.aliyuncs.com', result.cloud_boxes[1].control_endpoint)
        self.assertEqual('cb-f9z7yvzgwfkl9q0h****.cn-hangzhou.oss-cloudbox.aliyuncs.com', result.cloud_boxes[1].data_endpoint)


