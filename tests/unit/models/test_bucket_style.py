# pylint: skip-file

import unittest
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.models import bucket_style as model
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict, HttpResponse
from .. import MockHttpResponse

class TestPutStyle(unittest.TestCase):
    def test_constructor_request(self):
        request = model.PutStyleRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.style_name)
        self.assertIsNone(request.category)
        self.assertIsNone(request.style)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.PutStyleRequest(
            bucket='bucketexampletest',
            style_name='imagestyle',
            category='test_category',
            style=model.StyleContent(
                content='image/resize,p_50',
            ),
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('imagestyle', request.style_name)
        self.assertEqual('test_category', request.category)
        self.assertEqual('image/resize,p_50', request.style.content)

    def test_serialize_request(self):
        request = model.PutStyleRequest(
            bucket='bucketexampletest',
            style_name='imagestyle',
            category='test_category',
            style=model.StyleContent(
                content='image/resize,p_50',
            ),
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='PutStyle',
            method='PUT',
            bucket=request.bucket,
        ))
        self.assertEqual('PutStyle', op_input.op_name)
        self.assertEqual('PUT', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('imagestyle', op_input.parameters.get('styleName'))
        self.assertEqual('test_category', op_input.parameters.get('category'))

    def test_constructor_result(self):
        result = model.PutStyleResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.PutStyleResult()
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


class TestGetStyle(unittest.TestCase):
    def test_constructor_request(self):
        request = model.GetStyleRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.style_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.GetStyleRequest(
            bucket='bucketexampletest',
            style_name='imagestyle',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('imagestyle', request.style_name)

    def test_serialize_request(self):
        request = model.GetStyleRequest(
            bucket='bucketexampletest',
            style_name='imagestyle',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='GetStyle',
            method='GET',
            bucket=request.bucket,
        ))
        self.assertEqual('GetStyle', op_input.op_name)
        self.assertEqual('GET', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('imagestyle', op_input.parameters.get('styleName'))

    def test_constructor_result(self):
        result = model.GetStyleResult()
        self.assertIsNone(result.style)
        self.assertIsInstance(result, serde.Model)

        result = model.GetStyleResult(
            style=model.StyleInfo(
                name='example-bucket',
                content='image/resize,p_50',
                create_time='Wed, 20 May 2020 12:07:15 GMT',
                last_modify_time='Wed, 21 May 2020 12:07:15 GMT',
                category='image',
            ),
        )
        self.assertEqual('example-bucket', result.style.name)
        self.assertEqual('image/resize,p_50', result.style.content)
        self.assertEqual('Wed, 20 May 2020 12:07:15 GMT', result.style.create_time)
        self.assertEqual('Wed, 21 May 2020 12:07:15 GMT', result.style.last_modify_time)
        self.assertEqual('image', result.style.category)

    def test_deserialize_result(self):
        xml_data = r'''
        <Style>
        </Style>'''

        result = model.GetStyleResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <Style>
         <Name>imagestyle</Name>
         <Content>image/resize,p_50</Content>
         <Category>image</Category>
         <CreateTime>Wed, 20 May 2020 12:07:15 GMT</CreateTime>
         <LastModifyTime>Wed, 21 May 2020 12:07:15 GMT</LastModifyTime>
        </Style>
        '''

        result = model.GetStyleResult()
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
        self.assertEqual('imagestyle', result.style.name)
        self.assertEqual('image/resize,p_50', result.style.content)
        self.assertEqual('image', result.style.category)
        self.assertEqual('Wed, 20 May 2020 12:07:15 GMT', result.style.create_time)
        self.assertEqual('Wed, 21 May 2020 12:07:15 GMT', result.style.last_modify_time)


class TestListStyle(unittest.TestCase):
    def test_constructor_request(self):
        request = model.ListStyleRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.ListStyleRequest(
            bucket='bucketexampletest',
        )
        self.assertEqual('bucketexampletest', request.bucket)

    def test_serialize_request(self):
        request = model.ListStyleRequest(
            bucket='bucketexampletest',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='ListStyle',
            method='POST',
            bucket=request.bucket,
        ))
        self.assertEqual('ListStyle', op_input.op_name)
        self.assertEqual('POST', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)

    def test_constructor_result(self):
        result = model.ListStyleResult()
        self.assertIsNone(result.style_list)
        self.assertIsInstance(result, serde.Model)

        result = model.ListStyleResult(
            style_list=model.StyleList(
                styles=[model.StyleInfo(
                    name='example-bucket',
                    content='image/resize,p_50',
                    create_time='Wed, 20 May 2020 12:07:15 GMT',
                    last_modify_time='Wed, 21 May 2020 12:07:15 GMT',
                    category='image',
                ), model.StyleInfo(
                    name='example-bucket2',
                    content='image/resize,w_200',
                    create_time='Wed, 20 May 2020 12:08:04 GMT',
                    last_modify_time='Wed, 21 May 2020 12:08:04 GMT',
                    category='image',
                )],
            ),
        )
        self.assertEqual('example-bucket', result.style_list.styles[0].name)
        self.assertEqual('image/resize,p_50', result.style_list.styles[0].content)
        self.assertEqual('Wed, 20 May 2020 12:07:15 GMT', result.style_list.styles[0].create_time)
        self.assertEqual('Wed, 21 May 2020 12:07:15 GMT', result.style_list.styles[0].last_modify_time)
        self.assertEqual('image', result.style_list.styles[0].category)
        self.assertEqual('example-bucket2', result.style_list.styles[1].name)
        self.assertEqual('image/resize,w_200', result.style_list.styles[1].content)
        self.assertEqual('Wed, 20 May 2020 12:08:04 GMT', result.style_list.styles[1].create_time)
        self.assertEqual('Wed, 21 May 2020 12:08:04 GMT', result.style_list.styles[1].last_modify_time)
        self.assertEqual('image', result.style_list.styles[1].category)

    def test_deserialize_result(self):
        xml_data = r'''
        <StyleList>
        </StyleList>'''

        result = model.ListStyleResult()
        serde.deserialize_xml(xml_data=xml_data, obj=result)

        xml_data = r'''
        <StyleList>
         <Style>
         <Name>imagestyle</Name>
         <Content>image/resize,p_50</Content>
         <Category>image</Category>
         <CreateTime>Wed, 20 May 2020 12:07:15 GMT</CreateTime>
         <LastModifyTime>Wed, 21 May 2020 12:07:15 GMT</LastModifyTime>
         </Style>
         <Style>
         <Name>imagestyle1</Name>
         <Content>image/resize,w_200</Content>
         <Category>image</Category>
         <CreateTime>Wed, 20 May 2020 12:08:04 GMT</CreateTime>
         <LastModifyTime>Wed, 21 May 2020 12:08:04 GMT</LastModifyTime>
         </Style>
         <Style>
         <Name>imagestyle2</Name>
         <Content>image/resize,w_300</Content>
         <Category>image</Category>
         <CreateTime>Fri, 12 Mar 2021 06:19:13 GMT</CreateTime>
         <LastModifyTime>Fri, 13 Mar 2021 06:27:21 GMT</LastModifyTime>
         </Style>
        </StyleList>
        '''

        result = model.ListStyleResult()
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
        self.assertEqual('imagestyle', result.style_list.styles[0].name)
        self.assertEqual('image/resize,p_50', result.style_list.styles[0].content)
        self.assertEqual('image', result.style_list.styles[0].category)
        self.assertEqual('Wed, 20 May 2020 12:07:15 GMT', result.style_list.styles[0].create_time)
        self.assertEqual('Wed, 21 May 2020 12:07:15 GMT', result.style_list.styles[0].last_modify_time)
        self.assertEqual('imagestyle1', result.style_list.styles[1].name)
        self.assertEqual('image/resize,w_200', result.style_list.styles[1].content)
        self.assertEqual('image', result.style_list.styles[1].category)
        self.assertEqual('Wed, 20 May 2020 12:08:04 GMT', result.style_list.styles[1].create_time)
        self.assertEqual('Wed, 21 May 2020 12:08:04 GMT', result.style_list.styles[1].last_modify_time)
        self.assertEqual('imagestyle2', result.style_list.styles[2].name)
        self.assertEqual('image/resize,w_300', result.style_list.styles[2].content)
        self.assertEqual('image', result.style_list.styles[2].category)
        self.assertEqual('Fri, 12 Mar 2021 06:19:13 GMT', result.style_list.styles[2].create_time)
        self.assertEqual('Fri, 13 Mar 2021 06:27:21 GMT', result.style_list.styles[2].last_modify_time)


class TestDeleteStyle(unittest.TestCase):
    def test_constructor_request(self):
        request = model.DeleteStyleRequest(
        )
        self.assertIsNone(request.bucket)
        self.assertIsNone(request.style_name)
        self.assertFalse(hasattr(request, 'headers'))
        self.assertFalse(hasattr(request, 'parameters'))
        self.assertFalse(hasattr(request, 'payload'))
        self.assertIsInstance(request, serde.RequestModel)

        request = model.DeleteStyleRequest(
            bucket='bucketexampletest',
            style_name='imagestyle',
        )
        self.assertEqual('bucketexampletest', request.bucket)
        self.assertEqual('imagestyle', request.style_name)

    def test_serialize_request(self):
        request = model.DeleteStyleRequest(
            bucket='bucketexampletest',
            style_name='imagestyle',
        )

        op_input = serde.serialize_input(request, OperationInput(
            op_name='DeleteStyle',
            method='DELETE',
            bucket=request.bucket,
        ))
        self.assertEqual('DeleteStyle', op_input.op_name)
        self.assertEqual('DELETE', op_input.method)
        self.assertEqual('bucketexampletest', op_input.bucket)
        self.assertEqual('imagestyle', op_input.parameters.get('styleName'))

    def test_constructor_result(self):
        result = model.DeleteStyleResult()
        self.assertIsInstance(result, serde.ResultModel)

    def test_deserialize_result(self):
        xml_data = None
        result = model.DeleteStyleResult()
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
