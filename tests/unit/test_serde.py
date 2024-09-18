# pylint: skip-file
import unittest
import datetime
import xml.etree.ElementTree as ET
from enum import Enum
from typing import List, Optional, Any, cast
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import serde_utils
from alibabacloud_oss_v2 import exceptions
from alibabacloud_oss_v2.types import (
    OperationInput,
    OperationOutput,
    CaseInsensitiveDict,
    HttpResponse,
    HttpRequest,
    MutableMapping
)

class HttpResponseStub(HttpResponse):
    def __init__(self, **kwargs) -> None:
        super(HttpResponseStub, self).__init__()
        self._data = kwargs.pop("data")
        self._is_closed = False
        self._is_stream_consumed = False

    @property
    def request(self) -> HttpRequest:
        return None

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    @property
    def is_stream_consumed(self) -> bool:
        return self._is_stream_consumed

    @property
    def status_code(self) -> int:
        return 200

    @property
    def headers(self) -> MutableMapping[str, str]:
        return {}

    @property
    def reason(self) -> str:
        return "OK"

    @property
    def content(self) -> bytes:
        return self._data

    def __repr__(self) -> str:
        return 'HttpResponseStub'

    def __enter__(self) -> "HttpResponseStub":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        if not self.is_closed:
            self._is_closed = True

    def read(self) -> bytes:
        return self.content

    def iter_bytes(self):
        return iter([])


class TestSerdeXml(unittest.TestCase):
    def test_serialize_xml(self):
        class BasicTypeMode(serde.Model):
            """struct with basic type"""
            _attribute_map = {
                "str_field": {"tag": "xml", "rename": "StrFiled"},
                "int_field": {"tag": "xml", "rename": "IntFiled"},
                "bool_field": {"tag": "xml", "rename": "BoolFiled"},
                "float_field": {"tag": "xml", "rename": "FloatFiled"},
            }
            _xml_map = {
                "name": "BasicType"
            }

            def __init__(
                self,
                str_field: Optional[str] = None,
                int_field: Optional[int] = None,
                bool_field: Optional[bool] = None,
                float_field: Optional[float] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.str_field = str_field
                self.int_field = int_field
                self.bool_field = bool_field
                self.float_field = float_field

        class BasicTypeList(serde.Model):
            """struct with basic type list"""
            _attribute_map = {
                "str_field": {"tag": "xml", "rename": "StrFiled"},
            }
            _xml_map = {
                "name": "BasicTypeList"
            }

            def __init__(
                self,
                str_field: Optional[List[str]] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.str_field = str_field

        class MixedType(serde.Model):
            """struct with mixed type list"""
            _attribute_map = {
                "mixed_str_field": {"tag": "xml", "rename": "MixedStrFiled"},
                "mixed_int_field": {"tag": "xml", "rename": "MixedIntFiled"},
                "basic_type_list_sturct_filed": {"tag": "xml", "rename": "BasicTypeListFiled"},
                "basic_type_sturct_fileds": {"tag": "xml"},
            }
            _xml_map = {
                "name": "MixedTypeConfiguration"
            }

            def __init__(
                self,
                mixed_str_field: Optional[str] = None,
                mixed_int_field: Optional[int] = None,
                basic_type_list_sturct_filed: Optional[BasicTypeList] = None,
                basic_type_sturct_fileds: Optional[List[BasicTypeMode]] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.mixed_str_field = mixed_str_field
                self.mixed_int_field = mixed_int_field
                self.basic_type_list_sturct_filed = basic_type_list_sturct_filed
                self.basic_type_sturct_fileds = basic_type_sturct_fileds

        model = MixedType(
            mixed_str_field='mixed_str',
            mixed_int_field='1111',
            basic_type_list_sturct_filed=BasicTypeList(
                str_field=['123', '456', '789']
            ),
            basic_type_sturct_fileds=[
                BasicTypeMode(
                    str_field='str-1',
                    int_field='1',
                    bool_field=False,
                    float_field=1.5,
                ),
                BasicTypeMode(
                    str_field='str-2',
                    int_field='2',
                    bool_field=True,
                    float_field=2.5,
                ),
            ]
        )

        xml_data = serde.serialize_xml(model)
        self.assertIsNotNone(xml_data)
        self.assertTrue(len(xml_data) > 0)

        root = ET.fromstring(xml_data)
        self.assertEqual(5, len(root.findall('*')))

        self.assertEqual('MixedTypeConfiguration', root.tag)
        self.assertEqual('mixed_str', root.findtext('MixedStrFiled'))
        self.assertEqual('1111', root.findtext('MixedIntFiled'))
        elems = root.findall('BasicTypeList')
        self.assertEqual(1, len(elems))
        self.assertEqual('BasicTypeList', elems[0].tag)
        elems = root.findall('BasicTypeList//')
        self.assertEqual('StrFiled', elems[0].tag)
        self.assertEqual(3, len(elems))
        self.assertEqual('123', elems[0].text)
        self.assertEqual('456', elems[1].text)
        self.assertEqual('789', elems[2].text)

        elems = root.findall('BasicType')
        self.assertEqual(2, len(elems))
        self.assertEqual('str-1', elems[0].findtext('StrFiled'))
        self.assertEqual('1', elems[0].findtext('IntFiled'))
        self.assertEqual('false', elems[0].findtext('BoolFiled'))
        self.assertEqual('1.5', elems[0].findtext('FloatFiled'))

        self.assertEqual('str-2', elems[1].findtext('StrFiled'))
        self.assertEqual('2', elems[1].findtext('IntFiled'))
        self.assertEqual('true', elems[1].findtext('BoolFiled'))
        self.assertEqual('2.5', elems[1].findtext('FloatFiled'))

    def test_serialize_xml_with_root_tag(self):
        class BasicTypeMode(serde.Model):
            """struct with basic type"""
            _attribute_map = {
                "str_field": {"tag": "xml", "rename": "StrFiled"},
                "int_field": {"tag": "xml", "rename": "IntFiled"},
                "bool_field": {"tag": "xml", "rename": "BoolFiled"},
                "float_field": {"tag": "xml", "rename": "FloatFiled"},
            }
            _xml_map = {
                "name": "BasicType"
            }

            def __init__(
                self,
                str_field: Optional[str] = None,
                int_field: Optional[int] = None,
                bool_field: Optional[bool] = None,
                float_field: Optional[float] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.str_field = str_field
                self.int_field = int_field
                self.bool_field = bool_field
                self.float_field = float_field

        model = BasicTypeMode(
            str_field='str-2', int_field='2', bool_field=True)

        xml_data = serde.serialize_xml(model)
        self.assertIsNotNone(xml_data)
        self.assertTrue(len(xml_data) > 0)

        root = ET.fromstring(xml_data)
        self.assertEqual('BasicType', root.tag)
        self.assertEqual(3, len(root.findall('*')))

        xml_data = serde.serialize_xml(model, root='BasicType-123')
        self.assertIsNotNone(xml_data)
        self.assertTrue(len(xml_data) > 0)

        root = ET.fromstring(xml_data)
        self.assertEqual('BasicType-123', root.tag)
        self.assertEqual(3, len(root.findall('*')))

    def test_serialize_xml_datatime(self):
        class BasicTypeMode(serde.Model):
            """struct with datatime type"""
            _attribute_map = {
                "isotime_field": {"tag": "xml", "rename": "IsoTimeFiled"},
                "httptime_field": {"tag": "xml", "rename": "HttpTimeFiled", "type": "httptime"},
            }
            _xml_map = {
                "name": "BasicType"
            }

            def __init__(
                self,
                isotime_field: Optional[datetime.datetime] = None,
                httptime_field: Optional[datetime.datetime] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.isotime_field = isotime_field
                self.httptime_field = httptime_field

        model = BasicTypeMode(
            isotime_field=datetime.datetime.fromtimestamp(1702783809),
            httptime_field=datetime.datetime.fromtimestamp(1702783809))

        xml_data = serde.serialize_xml(model)
        self.assertIsNotNone(xml_data)
        self.assertTrue(len(xml_data) > 0)

        root = ET.fromstring(xml_data)
        self.assertEqual('BasicType', root.tag)
        self.assertEqual(2, len(root.findall('*')))
        self.assertEqual('2023-12-17T03:30:09Z',
                         root.findtext('IsoTimeFiled'))
        self.assertEqual('Sun, 17 Dec 2023 03:30:09 GMT',
                         root.findtext('HttpTimeFiled'))

    def test_serialize_enum_type(self):
        class EnumType(str, Enum):
            PRIVATE = 'private'
            PUBLICREAD = 'public-read'
            PUBLICREADWRITE = 'public-read-write'

        class BasicTypeMode(serde.Model):
            """struct with enum type"""
            _attribute_map = {
                "enum_field": {"tag": "xml", "rename": "EnumFiled"},
            }
            _xml_map = {
                "name": "BasicType"
            }

            def __init__(
                self,
                enum_field: Optional[EnumType] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.enum_field = enum_field

        model = BasicTypeMode(enum_field=EnumType.PRIVATE)

        xml_data = serde.serialize_xml(model)
        self.assertIsNotNone(xml_data)
        self.assertTrue(len(xml_data) > 0)

        root = ET.fromstring(xml_data)
        self.assertEqual('BasicType', root.tag)
        self.assertEqual(1, len(root.findall('*')))
        self.assertEqual('private', root.findtext('EnumFiled'))

    def test_serialize_not_support_type(self):
        class BasicTypeMode(serde.Model):
            """struct with other type"""
            _attribute_map = {
                "isotime_field": {"tag": "xml", "rename": "IsoTimeFiled"},
            }
            _xml_map = {
                "name": "BasicType"
            }

            def __init__(
                self,
                isotime_field: Optional[any] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.isotime_field = isotime_field

        class NotModeStruct:
            """test struct"""

            def __init__(
                self,
                field: str,
            ) -> None:
                self.field = field

        try:
            model = BasicTypeMode(isotime_field=NotModeStruct(field="test"))
            serde.serialize_xml(model)
            self.fail("not here")
        except exceptions.SerializationError as e:
            msg = str(e)
            self.assertTrue(
                'Serialization raised an exception: Unsupport type' in msg)

    def test_deserialize_xml(self):

        class BasicTypeMode(serde.Model):
            """struct with basic type"""
            _attribute_map = {
                "str_field": {"tag": "xml", "rename": "StrFiled"},
                "int_field": {"tag": "xml", "rename": "IntFiled", "type": "int"},
                "bool_field": {"tag": "xml", "rename": "BoolFiled", "type": "bool"},
                "float_field": {"tag": "xml", "rename": "FloatFiled", "type": "float"},
                "isotime_field": {"tag": "xml", "rename": "IsoTimeFiled", "type": "datetime"},
                "httptime_field": {"tag": "xml", "rename": "HttpTimeFiled", "type": "datetime,httptime"},
                "unixtime_field": {"tag": "xml", "rename": "UnixTimeFiled", "type": "datetime,unixtime"},
            }
            _xml_map = {
                "name": "BasicType"
            }

            def __init__(
                self,
                str_field: Optional[str] = None,
                int_field: Optional[int] = None,
                bool_field: Optional[bool] = None,
                float_field: Optional[float] = None,
                isotime_field: Optional[datetime.datetime] = None,
                httptime_field: Optional[datetime.datetime] = None,
                unixtime_field: Optional[datetime.datetime] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.str_field = str_field
                self.int_field = int_field
                self.bool_field = bool_field
                self.float_field = float_field
                self.isotime_field = isotime_field
                self.httptime_field = httptime_field
                self.unixtime_field = unixtime_field

        datetime_now = datetime.datetime.fromtimestamp(1702783809)
        model = BasicTypeMode(
            str_field='str-1',
            int_field='1',
            bool_field=False,
            float_field=1.5,
            isotime_field=datetime_now,
            httptime_field=datetime_now,
            unixtime_field=datetime_now
        )

        xml_data = serde.serialize_xml(model)
        self.assertIsNotNone(xml_data)
        self.assertTrue(len(xml_data) > 0)

        root = ET.fromstring(xml_data)
        self.assertEqual('BasicType', root.tag)
        self.assertEqual(7, len(root.findall('*')))
        self.assertEqual('2023-12-17T03:30:09Z',
                         root.findtext('IsoTimeFiled'))
        self.assertEqual('Sun, 17 Dec 2023 03:30:09 GMT',
                         root.findtext('HttpTimeFiled'))
        self.assertEqual('1702783809', root.findtext('UnixTimeFiled'))

        model2 = BasicTypeMode()
        date_time = datetime.datetime.fromtimestamp(
            1702783809, tz=datetime.timezone.utc)
        serde.deserialize_xml(xml_data, model2)
        self.assertEqual('str-1', model2.str_field)
        self.assertEqual(1, model2.int_field)
        self.assertEqual(False, model2.bool_field)
        self.assertEqual(1.5, model2.float_field)
        self.assertEqual(date_time, model2.isotime_field)
        self.assertEqual(date_time, model2.httptime_field)
        self.assertEqual(date_time, model2.unixtime_field)

    def test_deserialize_xml_list(self):

        class BasicTypeMode(serde.Model):
            """struct with basic type"""
            _attribute_map = {
                "str_fields": {"tag": "xml", "rename": "StrFiled","type": "[str]"},
                "int_fields": {"tag": "xml", "rename": "IntFiled", "type": "[int]"},
                "bool_fields": {"tag": "xml", "rename": "BoolFiled", "type": "[bool]"},
                "float_fields": {"tag": "xml", "rename": "FloatFiled", "type": "[float]"},
                "isotime_fields": {"tag": "xml", "rename": "IsoTimeFiled", "type": "[datetime]"},
                "httptime_fields": {"tag": "xml", "rename": "HttpTimeFiled", "type": "[datetime],httptime"},
                "unixtime_fields": {"tag": "xml", "rename": "UnixTimeFiled", "type": "[datetime],unixtime"},
            }
            _xml_map = {
                "name": "BasicType"
            }

            def __init__(
                self,
                str_fields: Optional[List[str]] = None,
                int_fields: Optional[List[int]] = None,
                bool_fields: Optional[List[bool]] = None,
                float_fields: Optional[List[float]] = None,
                isotime_fields: Optional[List[datetime.datetime]] = None,
                httptime_fields: Optional[List[datetime.datetime]] = None,
                unixtime_fields: Optional[List[datetime.datetime]] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.str_fields = str_fields
                self.int_fields = int_fields
                self.bool_fields = bool_fields
                self.float_fields = float_fields
                self.isotime_fields = isotime_fields
                self.httptime_fields = httptime_fields
                self.unixtime_fields = unixtime_fields

        datetime1 = datetime.datetime.fromtimestamp(1702783809)
        datetime2 = datetime.datetime.fromtimestamp(1702783819)
        datetime3 = datetime.datetime.fromtimestamp(1702783829)
        model = BasicTypeMode(
            str_fields=['str-1'],
            int_fields=[1,2,3],
            bool_fields=[False,False,True],
            float_fields=[1.5, 2.5, 3,5],
            isotime_fields=[datetime1],
            httptime_fields=[datetime1,datetime2],
            unixtime_fields=[datetime1,datetime2,datetime3],
        )

        xml_data = serde.serialize_xml(model)
        self.assertIsNotNone(xml_data)
        self.assertTrue(len(xml_data) > 0)

        root = ET.fromstring(xml_data)
        self.assertEqual('BasicType', root.tag)

        elems = root.findall('StrFiled')
        self.assertEqual(1, len(elems))
        self.assertEqual('str-1', elems[0].text)

        elems = root.findall('IntFiled')
        self.assertEqual(3, len(elems))
        self.assertEqual('1', elems[0].text)
        self.assertEqual('2', elems[1].text)
        self.assertEqual('3', elems[2].text)

        elems = root.findall('BoolFiled')
        self.assertEqual(3, len(elems))
        self.assertEqual('false', elems[0].text)
        self.assertEqual('false', elems[1].text)
        self.assertEqual('true', elems[2].text)

        elems = root.findall('FloatFiled')
        self.assertEqual(4, len(elems))
        self.assertEqual('1.5', elems[0].text)
        self.assertEqual('2.5', elems[1].text)
        self.assertEqual('3', elems[2].text)
        self.assertEqual('5', elems[3].text)

        elems = root.findall('IsoTimeFiled')
        self.assertEqual(1, len(elems))
        self.assertEqual('2023-12-17T03:30:09Z', elems[0].text)


        elems = root.findall('HttpTimeFiled')
        self.assertEqual(2, len(elems))
        self.assertEqual('Sun, 17 Dec 2023 03:30:09 GMT', elems[0].text)
        self.assertEqual('Sun, 17 Dec 2023 03:30:19 GMT', elems[1].text)

        elems = root.findall('UnixTimeFiled')
        self.assertEqual(3, len(elems))
        self.assertEqual('1702783809', elems[0].text)
        self.assertEqual('1702783819', elems[1].text)
        self.assertEqual('1702783829', elems[2].text)

        model2 = BasicTypeMode()
        self.assertIsNone(model2.str_fields)
        self.assertIsNone(model2.int_fields)
        self.assertIsNone(model2.bool_fields)
        self.assertIsNone(model2.float_fields)
        self.assertIsNone(model2.isotime_fields)
        self.assertIsNone(model2.httptime_fields)
        self.assertIsNone(model2.unixtime_fields)

        serde.deserialize_xml(xml_data, model2)
        self.assertIsInstance(model2.str_fields, List)
        self.assertSequenceEqual(model.str_fields, model2.str_fields)

        self.assertIsInstance(model2.int_fields, List)
        self.assertSequenceEqual(model.int_fields, model2.int_fields)

        self.assertIsInstance(model2.bool_fields, List)
        self.assertSequenceEqual(model.bool_fields, model2.bool_fields)
        
        self.assertIsInstance(model2.float_fields, List)
        self.assertSequenceEqual(model.float_fields, model2.float_fields)
        
        datetime1_utc = datetime.datetime.fromtimestamp(1702783809, tz=datetime.timezone.utc)
        datetime2_utc = datetime.datetime.fromtimestamp(1702783819, tz=datetime.timezone.utc)
        datetime3_utc = datetime.datetime.fromtimestamp(1702783829, tz=datetime.timezone.utc)

        self.assertIsInstance(model2.isotime_fields, List)
        self.assertEqual(datetime1_utc, model2.isotime_fields[0])
        
        self.assertIsInstance(model2.httptime_fields, List)
        self.assertEqual(datetime1_utc, model2.httptime_fields[0])
        self.assertEqual(datetime2_utc, model2.httptime_fields[1])

        self.assertIsInstance(model2.unixtime_fields, List)
        self.assertEqual(datetime1_utc, model2.unixtime_fields[0])
        self.assertEqual(datetime2_utc, model2.unixtime_fields[1])
        self.assertEqual(datetime3_utc, model2.unixtime_fields[2])

    def test_deserialize_xml_multi_layer_struct(self):

        class ModelOne(serde.Model):
            _attribute_map = {
                "str_field": {"tag": "xml", "rename": "StrFiled"},
                "int_field": {"tag": "xml", "rename": "IntFiled", "type": "int"},
            }
            _xml_map = {
                "name": "ModelOne"
            }

            def __init__(
                self,
                str_field: Optional[str] = None,
                int_field: Optional[int] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.str_field = str_field
                self.int_field = int_field

        class ModelTwo(serde.Model):
            _attribute_map = {
                "bool_field": {"tag": "xml", "rename": "BoolFiled", "type": "bool"},
                "float_field": {"tag": "xml", "rename": "FloatFiled", "type": "float"},
                "model_one": {"tag": "xml", "rename": "ModelOne", "type": "ModelOne"},
            }
            _dependency_map = {
                "ModelOne": {"new":lambda :ModelOne()}
            }
            _xml_map = {
                "name": "ModelTwo"
            }

            def __init__(
                self,
                bool_field: Optional[str] = None,
                float_field: Optional[int] = None,
                model_one: Optional[ModelOne] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.bool_field = bool_field
                self.float_field = float_field
                self.model_one = model_one

        class ModelThree(serde.Model):
            _attribute_map = {
                "isotime_field": {"tag": "xml", "rename": "IsoTimeFiled", "type": "datetime"},
            }
            _xml_map = {
                "name": "ModelThree"
            }

            def __init__(
                self,
                isotime_field: Optional[datetime.datetime] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.isotime_field = isotime_field

        class ModelTop(serde.Model):
            _attribute_map = {
                "id": {"tag": "xml", "rename": "Id", "type": "str"},
                "model_two": {"tag": "xml", "rename": "ModelTwo", "type": "ModelTwo"},
                "model_threes": {"tag": "xml", "rename": "ModelThree", "type": "[ModelThree]"},
            }
            _xml_map = {
                "name": "ModelTop"
            }
            _dependency_map = {
                "ModelTwo": {"new":lambda :ModelTwo()},
                "ModelThree": {"new":lambda :ModelThree()}
            }

            def __init__(
                self,
                id: Optional[str] = None,
                model_two: Optional[ModelTwo] = None,
                model_threes: Optional[List[ModelThree]] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.id = id
                self.model_two = model_two
                self.model_threes = model_threes

        datetime_utc1 = datetime.datetime.fromtimestamp(1702783809, tz=datetime.timezone.utc)
        datetime_utc2 = datetime.datetime.fromtimestamp(1702783819, tz=datetime.timezone.utc)
        model = ModelTop(
            id='id-1234',
            model_two=ModelTwo(
                bool_field=True,
                #float_field=3.5,
                model_one=ModelOne(
                    str_field='str-123',
                    #int_field=123,
                )
            ),
            model_threes=[
                ModelThree(isotime_field=datetime_utc1),
                ModelThree(isotime_field=datetime_utc2),
            ]
        )

        xml_data = serde.serialize_xml(model)
        self.assertIsNotNone(xml_data)
        self.assertTrue(len(xml_data) > 0)

        root = ET.fromstring(xml_data)
        self.assertEqual('ModelTop', root.tag)

        model2 = ModelTop()
        serde.deserialize_xml(xml_data, model2)
        self.assertEqual('id-1234', model2.id)
        self.assertEqual(True, model2.model_two.bool_field)
        self.assertIsNone(model2.model_two.float_field)
        self.assertEqual('str-123', model2.model_two.model_one.str_field)
        self.assertIsNone(model2.model_two.model_one.int_field)
        self.assertIsInstance(model2.model_threes, List)
        self.assertEqual(2, len(model2.model_threes))
        self.assertEqual(datetime_utc1, model2.model_threes[0].isotime_field)
        self.assertEqual(datetime_utc2, model2.model_threes[1].isotime_field)

        #test empty filed
        xml_data = '<ModelTop><Id></Id><ModelTwo><BoolFiled>false</BoolFiled></ModelTwo><ModelThree/><ModelThree/></ModelTop>'
        model3 = ModelTop()
        serde.deserialize_xml(xml_data, model3)
        self.assertEqual(None, model3.id)
        self.assertEqual(False, model3.model_two.bool_field)
        self.assertIsNone(model3.model_two.float_field)
        self.assertIsNone(model3.model_two.model_one)
        self.assertIsInstance(model3.model_threes, List)
        self.assertEqual(2, len(model3.model_threes))
        self.assertIsNone(model3.model_threes[0].isotime_field)
        self.assertIsNone(model3.model_threes[1].isotime_field)

        #test empty filed
        xml_data = '<ModelTop><ModelTwo><BoolFiled></BoolFiled></ModelTwo><ModelThree/></ModelTop>'
        model4 = ModelTop()
        serde.deserialize_xml(xml_data, model4)
        self.assertEqual(None, model4.id)
        self.assertIsNone(model4.model_two.bool_field)
        self.assertIsNone(model4.model_two.float_field)
        self.assertIsNone(model4.model_two.model_one)
        self.assertIsInstance(model4.model_threes, List)
        self.assertEqual(1, len(model4.model_threes))
        self.assertIsNone(model4.model_threes[0].isotime_field)

        #invalid xml
        xml_data = 'ModelTop><ModelTwo><BoolFiled>'
        model5 = ModelTop()
        try:
            serde.deserialize_xml(xml_data, model5)
            self.fail("should not here")        
        except ET.ParseError:
            pass
        except:
            self.fail("should not here")        

    def test_deserialize_xml_only_root(self):

        class ModelOne(serde.Model):
            _attribute_map = {
                "str_root": {"tag": "xml", "rename": "."},
            }
            _xml_map = {
                "name": "ModelOne"
            }

            def __init__(
                self,
                str_root: Optional[str] = None,
                **kwargs,
            ) -> None:
                super().__init__(**kwargs)
                self.str_root = str_root

        xml_data = '<ModelOne>123</ModelOne>'
        model = ModelOne()
        serde.deserialize_xml(xml_data, model)
        self.assertEqual("123", model.str_root)
 

class TestSerdeOperation(unittest.TestCase):
    def test_serialize_input(self):
        class SubConfiguration(serde.Model):
            def __init__(
                self,
                str_field: Optional[str] = None,
                int_field: Optional[int] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.str_field = str_field
                self.int_field = int_field

            _attribute_map = {
                "str_field": {"tag": "xml", "rename": "StrFiled"},
                "int_field": {"tag": "xml", "rename": "IntFiled", "type":"int"},
            }
            _xml_map = {
                "name": "SubConfiguration"
            }

        class RootConfiguration(serde.Model):
            def __init__(
                self,
                id: str,
                text: str,
                sub_configuration: Optional[List[SubConfiguration]] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.id = id
                self.text = text
                self.sub_configuration = sub_configuration

            _attribute_map = {
                "id": {"tag": "xml", "rename": "Id"},
                "text": {"tag": "xml", "rename": "Text"},
                "sub_configuration": {"tag": "xml", "rename": "SubConfiguration", "type": "[SubConfiguration]"},
            }
            _xml_map = {
                "name": "RootConfiguration"
            }


        class PutApiRequest(serde.RequestModel):
            def __init__(
                self,
                bucket: Optional[str] = None,
                key: Optional[str] = None,
                str_header: Optional[str] = None,
                int_header: Optional[int] = None,
                bool_header: Optional[bool] = None,
                float_header: Optional[float] = None,
                isotime_header: Optional[datetime.datetime] = None,
                httptime_header: Optional[datetime.datetime] = None,
                unixtime_header: Optional[datetime.datetime] = None,
                str_param: Optional[str] = None,
                int_param: Optional[int] = None,
                bool_param: Optional[bool] = None,
                float_param: Optional[float] = None,
                isotime_param: Optional[datetime.datetime] = None,
                httptime_param: Optional[datetime.datetime] = None,
                unixtime_param: Optional[datetime.datetime] = None,
                configuration: Optional[RootConfiguration] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket
                self.key = key
                self.str_header = str_header
                self.int_header = int_header
                self.bool_header = bool_header
                self.float_header = float_header
                self.isotime_header = isotime_header
                self.httptime_header = httptime_header
                self.unixtime_header = unixtime_header
                self.str_param = str_param
                self.int_param = int_param
                self.bool_param = bool_param
                self.float_param = float_param
                self.isotime_param = isotime_param
                self.httptime_param = httptime_param
                self.unixtime_param = unixtime_param
                self.configuration = configuration

            _attribute_map = {
                "bucket": {"tag": "input", "position": "host", "required": True},
                "key": {"tag": "input", "position": "path", "required": True},
                "str_header": {"tag": "input", "position": "header", "rename": "x-oss-str"},
                "int_header": {"tag": "input", "position": "header", "rename": "x-oss-int"},
                "bool_header": {"tag": "input", "position": "header", "rename": "x-oss-bool"},
                "float_header": {"tag": "input", "position": "header", "rename": "x-oss-float"},
                "isotime_header": {"tag": "input", "position": "header", "rename": "x-oss-isotime"},
                "httptime_header": {"tag": "input", "position": "header", "rename": "x-oss-httptime", "type":"datetime,httptime"},
                "unixtime_header": {"tag": "input", "position": "header", "rename": "x-oss-unixtime", "type":"datetime,unixtime"},
                "str_param": {"tag": "input", "position": "query", "rename": "param-str"},
                "int_param": {"tag": "input", "position": "query", "rename": "param-int"},
                "bool_param": {"tag": "input", "position": "query", "rename": "param-bool"},
                "float_param": {"tag": "input", "position": "query", "rename": "param-float"},
                "isotime_param": {"tag": "input", "position": "query", "rename": "param-isotime"},
                "httptime_param": {"tag": "input", "position": "query", "rename": "param-httptime", "type":"datetime,httptime"},
                "unixtime_param": {"tag": "input", "position": "query", "rename": "param-unixtime", "type":"datetime,unixtime"},          
                "configuration": {"tag": "input", "position": "body", "rename": "Configuration", "type": "xml"},
            }
        datetime_utc = datetime.datetime.fromtimestamp(1702783809, tz=datetime.timezone.utc)
        datetime2_utc = datetime.datetime.fromtimestamp(1702783819, tz=datetime.timezone.utc)
        request = PutApiRequest(
            bucket="bucket-124",
            acl="private",
            str_header = "str_header",
            int_header = 123,
            bool_header = True,
            float_header = 2.5,
            isotime_header = datetime_utc,
            httptime_header = datetime_utc,
            unixtime_header = datetime_utc,
            str_param = "str_param",
            int_param = 456,
            bool_param = False,
            float_param = 4.5,
            isotime_param = datetime2_utc,
            httptime_param = datetime2_utc,
            unixtime_param = datetime2_utc,
            configuration=RootConfiguration(
                id="id-124",
                text="just for test",
                sub_configuration=[
                    SubConfiguration(
                        str_field='str-1',
                        int_field=111
                    ),
                    SubConfiguration(
                        str_field='str-2',
                        int_field=222
                    ),
                ]
            )
        )
    
        # miss required field
        op_input = OperationInput(
            op_name='TestApi',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        )

        try:
            serde.serialize_input(request, op_input)
            self.fail("shoud not here")
        except exceptions.ParamRequiredError as err:
            self.assertIn("missing required field, key", str(err))
        except:
            self.fail("shoud not here")


        #normal case
        request.key = 'key'
        op_input = OperationInput(
            op_name='TestApi',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        )
        serde.serialize_input(request, op_input)
        self.assertEqual('str_header', op_input.headers.get('x-oss-str'))
        self.assertEqual('123', op_input.headers.get('x-oss-int'))
        self.assertEqual('true', op_input.headers.get('x-oss-bool'))
        self.assertEqual('2.5', op_input.headers.get('x-oss-float'))
        self.assertEqual('2023-12-17T03:30:09Z', op_input.headers.get('x-oss-isotime'))
        self.assertEqual('Sun, 17 Dec 2023 03:30:09 GMT', op_input.headers.get('x-oss-httptime'))
        self.assertEqual('1702783809', op_input.headers.get('x-oss-unixtime'))

        self.assertEqual('str_param', op_input.parameters.get('param-str'))
        self.assertEqual('456', op_input.parameters.get('param-int'))
        self.assertEqual('false', op_input.parameters.get('param-bool'))
        self.assertEqual('4.5', op_input.parameters.get('param-float'))
        self.assertEqual('2023-12-17T03:30:19Z', op_input.parameters.get('param-isotime'))
        self.assertEqual('Sun, 17 Dec 2023 03:30:19 GMT', op_input.parameters.get('param-httptime'))
        self.assertEqual('1702783819', op_input.parameters.get('param-unixtime'))

        root = ET.fromstring(op_input.body)
        self.assertEqual('Configuration', root.tag)
        self.assertEqual('id-124', root.findtext('Id'))
        self.assertEqual('just for test', root.findtext('Text'))
        elems = root.findall('SubConfiguration')
        self.assertEqual(2, len(elems))
        self.assertEqual('str-1', elems[0].findtext('StrFiled'))
        self.assertEqual('111', elems[0].findtext('IntFiled'))
        self.assertEqual('str-2', elems[1].findtext('StrFiled'))
        self.assertEqual('222', elems[1].findtext('IntFiled'))

    def test_serialize_non_xml_body(self):
        class PutApiRequest(serde.RequestModel):
            def __init__(
                self,
                bucket: Optional[str] = None,
                key: Optional[str] = None,
                str_header: Optional[str] = None,
                str_param: Optional[str] = None,
                configuration:Optional[Any] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket    
                self.key = key
                self.str_header = str_header
                self.str_param = str_param
                self.configuration = configuration

            _attribute_map = {
                "bucket": {"tag": "input", "position": "host", "required": True},
                "key": {"tag": "input", "position": "path", "required": True},
                "str_header": {"tag": "input", "position": "header", "rename": "x-oss-str"},
                "str_param": {"tag": "input", "position": "query", "rename": "param-str"},
                "configuration": {"tag": "input", "position": "body"},
            }

        request = PutApiRequest(
            bucket='bucket-123',
            key='key-456',
            str_header='str-1',
            str_param='str-2',
            configuration='hello world',
            headers={
               'X-oss-str':'str-11', 
               'X-oss-int':'1234',
            },
            parameters={
               'param-str':'1234', 
               'Param-str':'str-11', 
            }
        )

        op_input = OperationInput(
            op_name='TestApi',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        )
        serde.serialize_input(request, op_input)
        self.assertEqual('str-1', op_input.headers.get('x-oss-str'))
        self.assertEqual('1234', op_input.headers.get('x-oss-int'))
        self.assertEqual('str-2', op_input.parameters.get('param-str'))
        self.assertEqual('str-11', op_input.parameters.get('Param-str'))
        self.assertEqual('hello world', op_input.body)

        #default payload
        request = PutApiRequest(
            bucket='bucket-123',
            key='key-456',
            payload='123',
        )
        op_input = OperationInput(
            op_name='TestApi',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        )
        serde.serialize_input(request, op_input)
        self.assertEqual(0, len(op_input.headers.items()))
        self.assertEqual(0, len(op_input.parameters.items()))
        self.assertEqual('123', op_input.body)

    def test_serialize_custom_serializer(self):
        class PutApiRequest(serde.RequestModel):
            def __init__(
                self,
                bucket: Optional[str] = None,
                key: Optional[str] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket    
                self.key = key

            _attribute_map = {
                "bucket": {"tag": "input", "position": "host", "required": True},
                "key": {"tag": "input", "position": "path", "required": True},
            }
        def add_content_type(request: serde.Model, op_input: OperationInput):
            op_input.headers.update(
                {
                    'x-oss-str':'str-1',
                    'x-oss-key':request.key,
                })
            op_input.parameters.update(
                {
                    'param-str':'str-2',
                    'Param-str':'str-11',
                })
            
        request = PutApiRequest(
            bucket='bucket-123',
            key='key-456',
        )

        op_input = OperationInput(
            op_name='TestApi',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        )
        serializer = [
            add_content_type,
        ]
        serde.serialize_input(request, op_input, custom_serializer=serializer)
        self.assertEqual('str-1', op_input.headers.get('x-oss-str'))
        self.assertEqual('key-456', op_input.headers.get('x-oss-key'))
        self.assertEqual('str-2', op_input.parameters.get('param-str'))
        self.assertEqual('str-11', op_input.parameters.get('Param-str'))
        self.assertIsNone(op_input.body)

    def test_serialize_non_requestmodel(self):
        class PutApiRequest(serde.Model):
            def __init__(
                self,
                bucket: Optional[str] = None,
                key: Optional[str] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket    
                self.key = key

            _attribute_map = {
                "bucket": {"tag": "input", "position": "host", "required": True},
                "key": {"tag": "input", "position": "path", "required": True},
            }

        class PutApiRequest2:
            def __init__(
                self,
                bucket: Optional[str] = None,
                key: Optional[str] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket    
                self.key = key

            _attribute_map = {
                "bucket": {"tag": "input", "position": "host", "required": True},
                "key": {"tag": "input", "position": "path", "required": True},
            }

        request = PutApiRequest(
            bucket='bucket-123',
            key='key-456',
        )

        op_input = OperationInput(
            op_name='TestApi',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        )

        try:
            serde.serialize_input(request, op_input)
            self.fail("shoud not here")
        except exceptions.SerializationError as err:
            self.assertIn("is not subclass of serde.RequestModel", str(err))
            self.assertIn("PutApiRequest", str(err))
        except:
            self.fail("shoud not here")


        request = PutApiRequest2(
            bucket='bucket-123',
            key='key-456',
        )

        op_input = OperationInput(
            op_name='TestApi',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        )

        try:
            serde.serialize_input(request, op_input)
            self.fail("shoud not here")
        except exceptions.SerializationError as err:
            self.assertIn("is not subclass of serde.RequestModel", str(err))
            self.assertIn("PutApiRequest2", str(err))
        except:
            self.fail("shoud not here")            


    def test_serialize_dict_header(self):
        class PutApiRequest(serde.RequestModel):
            def __init__(
                self,
                bucket: Optional[str] = None,
                key: Optional[str] = None,
                str_header: Optional[str] = None,
                str_param: Optional[str] = None,
                configuration:Optional[Any] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket    
                self.key = key
                self.str_header = str_header
                self.str_param = str_param
                self.configuration = configuration

            _attribute_map = {
                "bucket": {"tag": "input", "position": "host", "required": True},
                "key": {"tag": "input", "position": "path", "required": True},
                "str_header": {"tag": "input", "position": "header", "rename": "x-oss-str"},
                "str_param": {"tag": "input", "position": "query", "rename": "param-str"},
                "dict_header": {"tag": "input", "position": "header", "rename": "x-oss-meta-", "type":"dict,usermeta"},
            }

        request = PutApiRequest(
            bucket='bucket-123',
            key='key-456',
            str_header='str-1',
            str_param='str-2',
            dict_header={
                'key1':'value1',
                'key2':'value2',
            },
        )

        op_input = OperationInput(
            op_name='TestApi',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        )
        serde.serialize_input(request, op_input)
        self.assertEqual('str-1', op_input.headers.get('x-oss-str'))
        self.assertEqual('str-2', op_input.parameters.get('param-str'))
        self.assertEqual('value1', op_input.headers.get('x-oss-meta-key1'))
        self.assertEqual('value2', op_input.headers.get('x-oss-meta-key2'))


    def test_serialize_enum_type(self):
        class EnumType(str, Enum):
            PRIVATE = 'private'
            PUBLICREAD = 'public-read'
            PUBLICREADWRITE = 'public-read-write'
        class PutApiRequest(serde.RequestModel):
            def __init__(
                self,
                bucket: Optional[str] = None,
                key: Optional[str] = None,
                enum_header: Optional[EnumType] = None,
                enum_param: Optional[EnumType] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket
                self.key = key
                self.enum_header = enum_header
                self.enum_param = enum_param

            _attribute_map = {
                "bucket": {"tag": "input", "position": "host", "required": True},
                "key": {"tag": "input", "position": "path", "required": True},
                "enum_header": {"tag": "input", "position": "header", "rename": "x-oss-enum"},
                "enum_param": {"tag": "input", "position": "query", "rename": "param-enum"},
            }

        request = PutApiRequest(
            bucket='bucket-123',
            key='key-456',
            enum_header=EnumType.PUBLICREAD,
            enum_param=EnumType.PUBLICREADWRITE,
        )

        op_input = OperationInput(
            op_name='TestApi',
            method='GET',
            bucket=request.bucket,
            key=request.key,
        )
        serde.serialize_input(request, op_input)
        self.assertEqual('public-read', op_input.headers.get('x-oss-enum'))
        self.assertEqual('public-read-write', op_input.parameters.get('param-enum'))

    def test_deserialize_output(self):
        class PutApiResult(serde.ResultModel):
            def __init__(
                self,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
 
        result = PutApiResult()

        headers = CaseInsensitiveDict({'key':'value', 'key1':'value1', 'x-oss-request-id':'123'})
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            headers= headers,
        )

        serde.deserialize_output(result, op_output)
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('123', result.request_id)
        self.assertEqual('value', result.headers.get('key'))
        self.assertEqual('value1', result.headers.get('key1'))
        self.assertEqual('123', result.headers.get('x-oss-request-id'))


    def test_deserialize_response_inline_body_xml(self):
        class PutApiResult(serde.ResultModel):
            def __init__(
                self,
                str_xml: Optional[str] = None,
                int_xml: Optional[int] = None,
                bool_xml: Optional[bool] = None,
                float_xml: Optional[float] = None,
                isotime_xml: Optional[datetime.datetime] = None,
                httptime_xml: Optional[datetime.datetime] = None,
                unixtime_xml: Optional[datetime.datetime] = None,                
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.str_xml = str_xml
                self.int_xml = int_xml
                self.bool_xml = bool_xml
                self.float_xml = float_xml
                self.isotime_xml = isotime_xml
                self.httptime_xml = httptime_xml
                self.unixtime_xml = unixtime_xml
            
            _attribute_map = {
                "str_xml": {"tag": "xml", "rename": "StrField"},
                "int_xml": {"tag": "xml", "rename": "IntField", "type":"int"},
                "bool_xml": {"tag": "xml", "rename": "BoolField", "type":"bool"},
                "float_xml": {"tag": "xml", "rename": "FloatField", "type":"float"},
                "isotime_xml": {"tag": "xml", "rename": "IsotimeField", "type":"datetime"},
                "httptime_xml": {"tag": "xml", "rename": "HttptimeField", "type":"datetime,httptime"},
                "unixtime_xml": {"tag": "xml", "rename": "UnixtimeField", "type":"datetime,unixtime"},
            }

        xml_data = r'''
            <Root>
            <StrField>str-1</StrField>
            <IntField>1234</IntField>
            <BoolField>true</BoolField>
            <FloatField>3.5</FloatField>
            <IsotimeField>2023-12-17T03:30:09.000000Z</IsotimeField>
            <HttptimeField>Sun, 17 Dec 2023 03:30:09 GMT</HttptimeField>
            <UnixtimeField>1702783809</UnixtimeField>
            </Root>
        '''

        result = PutApiResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            headers= {},
            http_response=HttpResponseStub(data=xml_data)
        )
        datetime_utc = datetime.datetime.fromtimestamp(1702783809, tz=datetime.timezone.utc)
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('', result.request_id)
        self.assertEqual('str-1', result.str_xml)
        self.assertEqual(1234, result.int_xml)
        self.assertEqual(True, result.bool_xml)
        self.assertEqual(3.5, result.float_xml)
        self.assertEqual(datetime_utc, result.isotime_xml)
        self.assertEqual(datetime_utc, result.httptime_xml)
        self.assertEqual(datetime_utc, result.unixtime_xml)

    def test_deserialize_response_outline_body_xml(self):

        class Configuration(serde.Model):
            def __init__(
                self,
                str_xml: Optional[str] = None,
                int_xml: Optional[int] = None,
                bool_xml: Optional[bool] = None,
                float_xml: Optional[float] = None,
                isotime_xml: Optional[datetime.datetime] = None,
                httptime_xml: Optional[datetime.datetime] = None,
                unixtime_xml: Optional[datetime.datetime] = None,                
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.str_xml = str_xml
                self.int_xml = int_xml
                self.bool_xml = bool_xml
                self.float_xml = float_xml
                self.isotime_xml = isotime_xml
                self.httptime_xml = httptime_xml
                self.unixtime_xml = unixtime_xml
            
            _attribute_map = {
                "str_xml": {"tag": "xml", "rename": "StrField"},
                "int_xml": {"tag": "xml", "rename": "IntField", "type":"int"},
                "bool_xml": {"tag": "xml", "rename": "BoolField", "type":"bool"},
                "float_xml": {"tag": "xml", "rename": "FloatField", "type":"float"},
                "isotime_xml": {"tag": "xml", "rename": "IsotimeField", "type":"datetime"},
                "httptime_xml": {"tag": "xml", "rename": "HttptimeField", "type":"datetime,httptime"},
                "unixtime_xml": {"tag": "xml", "rename": "UnixtimeField", "type":"datetime,unixtime"},
            }

            _xml_map = {'name':'Configuration'}


        class PutApiResult(serde.ResultModel):
            def __init__(
                self,
                config: Optional[Configuration] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.config = config
            
            _attribute_map = {
                "config": {"tag": "output", "position":"body", "type":"Configuration,xml"},
            }
            _dependency_map = {
                "Configuration": {"new": lambda:Configuration()},
            }

        xml_data = r'''
            <Configuration>
                <StrField>str-1</StrField>
                <IntField>1234</IntField>
                <BoolField>true</BoolField>
                <FloatField>3.5</FloatField>
                <IsotimeField>2023-12-17T03:30:09.000000Z</IsotimeField>
                <HttptimeField>Sun, 17 Dec 2023 03:30:09 GMT</HttptimeField>
                <UnixtimeField>1702783809</UnixtimeField>
            </Configuration>
        '''

        result = PutApiResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            headers= {},
            http_response=HttpResponseStub(data=xml_data)
        )
        datetime_utc = datetime.datetime.fromtimestamp(1702783809, tz=datetime.timezone.utc)
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('', result.request_id)
        self.assertEqual('str-1', result.config.str_xml)
        self.assertEqual(1234, result.config.int_xml)
        self.assertEqual(True, result.config.bool_xml)
        self.assertEqual(3.5, result.config.float_xml)
        self.assertEqual(datetime_utc, result.config.isotime_xml)
        self.assertEqual(datetime_utc, result.config.httptime_xml)
        self.assertEqual(datetime_utc, result.config.unixtime_xml)


    def test_deserialize_response_header(self):
        class PutApiResult(serde.ResultModel):
            def __init__(
                self,
                str_header: Optional[str] = None,
                int_header: Optional[int] = None,
                bool_header: Optional[bool] = None,
                float_header: Optional[float] = None,
                isotime_header: Optional[datetime.datetime] = None,
                httptime_header: Optional[datetime.datetime] = None,
                unixtime_header: Optional[datetime.datetime] = None,                
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.str_header = str_header
                self.int_header = int_header
                self.bool_header = bool_header
                self.float_header = float_header
                self.isotime_header = isotime_header
                self.httptime_header = httptime_header
                self.unixtime_header = unixtime_header
            
            _attribute_map = {
                "str_header": {"tag": "output", "position": "header", "rename": "x-oss-str"},
                "int_header": {"tag": "output", "position": "header", "rename": "x-oss-int", "type":"int"},
                "bool_header": {"tag": "output", "position": "header", "rename": "x-oss-bool", "type":"bool"},
                "float_header": {"tag": "output", "position": "header", "rename": "x-oss-float", "type":"float"},
                "isotime_header": {"tag": "output", "position": "header", "rename": "x-oss-isotime", "type":"datetime"},
                "httptime_header": {"tag": "output", "position": "header", "rename": "x-oss-httptime", "type":"datetime,httptime"},
                "unixtime_header": {"tag": "output", "position": "header", "rename": "x-oss-unixtime", "type":"datetime,unixtime"},
            }
 

        result = PutApiResult()

        headers = CaseInsensitiveDict({
            'x-oss-str':'str-1', 
            'x-oss-int':'123', 
            'x-oss-bool':'false', 
            'x-oss-float':'3.5', 
            'x-oss-isotime':'2023-12-17T03:30:09.000000Z', 
            'x-oss-httptime':'Sun, 17 Dec 2023 03:30:09 GMT', 
            'x-oss-unixtime':'1702783809', 
            'x-oss-request-id':'id-12345'
        })
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            headers= headers,
        )
        datetime_utc = datetime.datetime.fromtimestamp(1702783809, tz=datetime.timezone.utc)
        deserializer = [serde.deserialize_output_headers]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('id-12345', result.request_id)
        self.assertEqual(8, len(result.headers.items()))
        self.assertEqual('str-1', result.str_header)
        self.assertEqual(123, result.int_header)
        self.assertEqual(False, result.bool_header)
        self.assertEqual(3.5, result.float_header)
        self.assertEqual(datetime_utc, result.isotime_header)
        self.assertEqual(datetime_utc, result.httptime_header)
        self.assertEqual(datetime_utc, result.unixtime_header)

    def test_deserialize_response_body_and_header(self):
        class PutApiResult(serde.ResultModel):
            def __init__(
                self,
                str_xml: Optional[str] = None,
                int_xml: Optional[int] = None,
                float_header: Optional[float] = None,
                isotime_header: Optional[datetime.datetime] = None,
           
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.str_xml = str_xml
                self.int_xml = int_xml
                self.float_header = float_header
                self.isotime_header = isotime_header
            
            _attribute_map = {
                "str_xml": {"tag": "xml", "rename": "StrField"},
                "int_xml": {"tag": "xml", "rename": "IntField", "type":"int"},
                "float_header": {"tag": "output", "position": "header", "rename": "x-oss-float", "type":"float"},
                "isotime_header": {"tag": "output", "position": "header", "rename": "x-oss-isotime", "type":"datetime"},
            }

        xml_data = r'''
            <Root>
                <StrField>str-1</StrField>
                <IntField>1234</IntField>
            </Root>
        '''
        headers = CaseInsensitiveDict({
            'x-oss-float':'3.5', 
            'x-oss-isotime':'2023-12-17T03:30:09.000000Z', 
            'x-oss-request-id':'id-12345'
        })

        result = PutApiResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            headers= headers,
            http_response=HttpResponseStub(data=xml_data)
        )
        datetime_utc = datetime.datetime.fromtimestamp(1702783809, tz=datetime.timezone.utc)
        deserializer = [serde.deserialize_output_xmlbody, serde.deserialize_output_headers]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('id-12345', result.request_id)
    
        self.assertEqual(3.5, result.float_header)
        self.assertEqual(datetime_utc, result.isotime_header)

        self.assertEqual('str-1', result.str_xml)
        self.assertEqual(1234, result.int_xml)

    def test_deserialize_non_resultmodel(self):
        class PutApiResult(serde.Model):
            def __init__(
                self,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)

        try:
            result = PutApiResult()
            op_output = OperationOutput(
                status='OK',
                status_code=200,
            )
            serde.deserialize_output(result, op_output)
            self.fail("shoud not here")
        except exceptions.DeserializationError as err:
            self.assertIn("is not subclass of serde.ResultModel", str(err))
            self.assertIn("PutApiResult", str(err))
        except:
            self.fail("shoud not here")

        class PutApiRequest2:
            def __init__(
                self,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)

        try:
            result = PutApiRequest2()
            op_output = OperationOutput(
                status='OK',
                status_code=200,
            )
            serde.deserialize_output(result, op_output)
            self.fail("shoud not here")
        except exceptions.DeserializationError as err:
            self.assertIn("is not subclass of serde.ResultModel", str(err))
            self.assertIn("PutApiRequest2", str(err))
        except:
            self.fail("shoud not here")   

    def test_deserialize_response_dict_header(self):
        class PutApiResult(serde.ResultModel):
            def __init__(
                self,
                str_header: Optional[str] = None,
                dict_header: Optional[MutableMapping] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.str_header = str_header
                self.dict_header = dict_header
            
            _attribute_map = {
                "str_header": {"tag": "output", "position": "header", "rename": "x-oss-str"},
                "dict_header": {"tag": "output", "position": "header", "rename": "x-oss-meta-", "type":"dict,usermeta"},
            }
 

        result = PutApiResult()

        headers = CaseInsensitiveDict({
            'x-oss-str':'str-1', 
            'x-oss-meta-key1':'value1', 
            'x-oss-meta-key2':'value2', 
            'x-oss-request-id':'id-12345'
        })
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            headers= headers,
        )
        deserializer = [serde.deserialize_output_headers]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('id-12345', result.request_id)
        self.assertEqual(4, len(result.headers.items()))
        self.assertEqual('str-1', result.str_header)
        self.assertEqual('value1', result.dict_header.get('key1'))
        self.assertEqual('value2', result.dict_header.get('key2'))

    def test_deserialize_response_body_xml_roottag(self):
        class PutApiResult(serde.ResultModel):
            def __init__(
                self,
                str_xml: Optional[str] = None,
                int_xml: Optional[int] = None,
                float_header: Optional[float] = None,
                isotime_header: Optional[datetime.datetime] = None,
           
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.str_xml = str_xml
                self.int_xml = int_xml
                self.float_header = float_header
                self.isotime_header = isotime_header
            
            _attribute_map = {
                "str_xml": {"tag": "xml", "rename": "StrField"},
                "int_xml": {"tag": "xml", "rename": "IntField", "type":"int"},
                "float_header": {"tag": "output", "position": "header", "rename": "x-oss-float", "type":"float"},
                "isotime_header": {"tag": "output", "position": "header", "rename": "x-oss-isotime", "type":"datetime"},
            }

            _xml_map = {'name': 'Root'}

        xml_data = r'''
            <Root>
                <StrField>str-1</StrField>
                <IntField>1234</IntField>
            </Root>
        '''


        result = PutApiResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=HttpResponseStub(data=xml_data)
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('str-1', result.str_xml)
        self.assertEqual(1234, result.int_xml)


        xml_data = r'''
            <InvalidRoot>
                <StrField>str-1</StrField>
                <IntField>1234</IntField>
            </InvalidRoot>
        '''

        result = PutApiResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=HttpResponseStub(data=xml_data)
        )
        deserializer = [serde.deserialize_output_xmlbody]
        try:
            serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
            self.fail('should not here')
        except exceptions.DeserializationError as err:
            self.assertIn('Expect root tag is Root, gots InvalidRoot', str(err))
        except:
            self.fail('should not here')


    def test_deserialize_response_body_outline_node_xml_roottag(self):
        class Configuration(serde.Model):
            def __init__(
                self,
                str_xml: Optional[str] = None,
                int_xml: Optional[int] = None,
           
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.str_xml = str_xml
                self.int_xml = int_xml
            
            _attribute_map = {
                "str_xml": {"tag": "xml", "rename": "StrField"},
                "int_xml": {"tag": "xml", "rename": "IntField", "type":"int"},
            }

            _xml_map = {'name':'Root'}

        class PutApiResult(serde.ResultModel):
            def __init__(
                self,
                config: Optional["Configuration"] = None,
           
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.config = config
            
            _attribute_map = {
                "config": {"tag": "output", "position": "body", "rename": "Root", "type":"Configuration,xml"},
            }

            _dependency_map = {
                "Configuration": {"new":lambda :Configuration()}
            }


        xml_data = r'''
            <Root>
                <StrField>str-1</StrField>
                <IntField>1234</IntField>
            </Root>
        '''

        result = PutApiResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=HttpResponseStub(data=xml_data)
        )
        deserializer = [serde.deserialize_output_xmlbody]
        serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
        self.assertEqual('OK', result.status)
        self.assertEqual(200, result.status_code)
        self.assertEqual('str-1', result.config.str_xml)
        self.assertEqual(1234, result.config.int_xml)


        xml_data = r'''
            <InvalidRoot>
                <StrField>str-1</StrField>
                <IntField>1234</IntField>
            </InvalidRoot>
        '''

        result = PutApiResult()
        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=HttpResponseStub(data=xml_data)
        )
        deserializer = [serde.deserialize_output_xmlbody]
        try:
            serde.deserialize_output(result, op_output, custom_deserializer=deserializer)
            self.fail('should not here')
        except exceptions.DeserializationError as err:
            self.assertIn('Expect root tag is Root, gots InvalidRoot', str(err))
        except:
            self.fail('should not here')

class TestSerdePublicFunction(unittest.TestCase):
    def test_serialize_time(self):
        datetime_utc = datetime.datetime.fromtimestamp(1702783819, tz=datetime.timezone.utc)
        self.assertEqual('2023-12-17T03:30:19.000000Z', serde.serialize_isotime(datetime_utc))
        self.assertEqual('Sun, 17 Dec 2023 03:30:19 GMT', serde.serialize_httptime(datetime_utc))
        self.assertEqual('1702783819', serde.serialize_unixtime(datetime_utc))


    def test_serialize_time(self):
        datetime_utc = datetime.datetime.fromtimestamp(1702783819, tz=datetime.timezone.utc)
        self.assertEqual(datetime_utc, serde.deserialize_iso('2023-12-17T03:30:19.000000Z'))
        self.assertEqual(datetime_utc, serde.deserialize_httptime('Sun, 17 Dec 2023 03:30:19 GMT'))
        self.assertEqual(datetime_utc, serde.deserialize_unixtime('1702783819'))

    def test_serialize_boolean(self):
        self.assertTrue(serde.deserialize_boolean('True'))
        self.assertTrue(serde.deserialize_boolean('true'))
        self.assertTrue(serde.deserialize_boolean('TRUE'))
        
        self.assertFalse(serde.deserialize_boolean(''))
        self.assertFalse(serde.deserialize_boolean('FALSE'))
        self.assertFalse(serde.deserialize_boolean(None))

    def test_copy_request(self):
        class PutApiRequestSrc(serde.RequestModel):
            def __init__(
                self,
                bucket: Optional[str] = None,
                key: Optional[str] = None,
                str_header: Optional[str] = None,
                int_header: Optional[int] = None,
                bool_header: Optional[bool] = None,
                float_header: Optional[float] = None,
                isotime_header: Optional[datetime.datetime] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket
                self.key = key
                self.str_header = str_header
                self.int_header = int_header
                self.bool_header = bool_header
                self.float_header = float_header
                self.isotime_header = isotime_header

            _attribute_map = {
                "bucket": {"tag": "input", "position": "host", "required": True},
                "key": {"tag": "input", "position": "path", "required": True},
                "str_header": {"tag": "input", "position": "header", "rename": "x-oss-str"},
                "int_header": {"tag": "input", "position": "header", "rename": "x-oss-int"},
                "bool_header": {"tag": "input", "position": "header", "rename": "x-oss-bool"},
                "float_header": {"tag": "input", "position": "header", "rename": "x-oss-float"},
                "isotime_header": {"tag": "input", "position": "header", "rename": "x-oss-isotime"},
            }


        class PutApiRequestDst(serde.RequestModel):
            def __init__(
                self,
                bucket: Optional[str] = None,
                key: Optional[str] = None,
                str_header: Optional[str] = None,
                int_header: Optional[int] = None,
                bool_header: Optional[bool] = None,
                float_header: Optional[float] = None,
                unixtime_header: Optional[datetime.datetime] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket
                self.key = key
                self.str_header = str_header
                self.int_header = int_header
                self.bool_header = bool_header
                self.float_header = float_header
                self.unixtime_header = unixtime_header

            _attribute_map = {
                "bucket": {"tag": "input", "position": "host", "required": True},
                "key": {"tag": "input", "position": "path", "required": True},
                "str_header": {"tag": "input", "position": "header", "rename": "x-oss-str"},
                "int_header": {"tag": "input", "position": "header", "rename": "x-oss-int"},
                "bool_header": {"tag": "input", "position": "header", "rename": "x-oss-bool"},
                "float_header": {"tag": "input", "position": "header", "rename": "x-oss-float"},
                "unixtime_header": {"tag": "input", "position": "header", "rename": "x-oss-isotime"},
            }

        src = PutApiRequestSrc(
            bucket='bucket',
            key='key',
            str_header='str-1',
            int_header=123,
            bool_header=True,
            float_header=1.5,
            isotime_header=datetime.datetime.now()
        )

        dst = PutApiRequestDst()
        self.assertIsNone(dst.bucket)
        self.assertIsNone(dst.key)
        self.assertIsNone(dst.str_header)
        self.assertIsNone(dst.int_header)
        self.assertIsNone(dst.bool_header)
        self.assertIsNone(dst.float_header)
        self.assertIsNone(dst.unixtime_header)

        serde.copy_request(dst, src)
        self.assertEqual('bucket',dst.bucket)
        self.assertEqual('key',dst.key)
        self.assertEqual('str-1',dst.str_header)
        self.assertEqual(123,dst.int_header)
        self.assertEqual(True,dst.bool_header)
        self.assertEqual(1.5,dst.float_header)
        self.assertIsNone(dst.unixtime_header)

class TestSerdeUtils(unittest.TestCase):
    
    def test_deserialize_process_body(self):
        class JsonObjectResult(serde.ResultModel):
            def __init__(
                self,
                bucket: Optional[str] = None,
                file_size: Optional[int] = None,
                key: Optional[str] = None,
                process_status: Optional[str] = None,
                **kwargs: Any
            ) -> None:
                super().__init__(**kwargs)
                self.bucket = bucket
                self.file_size = file_size
                self.key = key
                self.process_status = process_status

            _attribute_map = {
                "bucket": {"tag": "json", "rename": "bucket"},
                "file_size": {"tag": "json", "rename": "fileSize", "type": "int"},
                "key": {"tag": "json", "rename": "object"},
                "process_status": {"tag": "json", "rename": "status"},
            }
        
        jsonstr = '{"bucket":"bucket-123","fileSize":1234,"object":"object-123","status":"ok"}'

        op_output = OperationOutput(
            status='OK',
            status_code=200,
            http_response=HttpResponseStub(data=jsonstr)
        )
 
        result = serde_utils.deserialize_process_body(JsonObjectResult(), op_output)
        result = cast(JsonObjectResult, result)

        self.assertEqual('bucket-123', result.bucket)
        self.assertEqual(1234, result.file_size)
        self.assertEqual('object-123', result.key)
        self.assertEqual('ok', result.process_status)
