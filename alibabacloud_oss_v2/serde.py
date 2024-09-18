"""_summary_
"""
import datetime
import sys
from enum import Enum
from typing import Dict, Any, Optional, List, MutableMapping, Mapping, cast
from email.utils import format_datetime, parsedate_tz
import xml.etree.ElementTree as ET
from . import exceptions
from .types import OperationInput, OperationOutput, CaseInsensitiveDict

_model_allow_attribute_map = ["headers", "parameters", "payload"]

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
ISO8601_MICRO = '%Y-%m-%dT%H:%M:%S.%fZ'

class Model:
    """Mixin for all client request body/response body models to support
    serialization and deserialization.
    """
    _dependency_map: Dict[str, Dict[str, Any]] = {}  # use for deserialization
    _attribute_map: Dict[str, Dict[str, Any]] = {}

    def __init__(self, **kwargs: Any) -> None:
        for k in kwargs:  # pylint: disable=consider-using-dict-items
            if k not in self._attribute_map and k not in _model_allow_attribute_map:
                pass
            else:
                setattr(self, k, kwargs[k])
        self.__models = None

    def __eq__(self, other: Any) -> bool:
        """Compare objects by comparing all attributes."""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other: Any) -> bool:
        """Compare objects by comparing all attributes."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __create_depend_object(self, name: str) -> "Model":  # pylint: disable=unused-private-member
        """Creats an instance of object from dependencies map,

        Args:
            name (str): the name of a object type

        Returns:
            Model | None: An instance of object or None

        """
        new = self._dependency_map.get(name, {}).get('new', None)
        if new is not None:
            return new()

        if self.__models is None:
            str_models = self.__module__.rsplit(".", 1)[0]
            self.__models = sys.modules[str_models] or {}

        class_obj = self.__models.__dict__.get(name, None)
        if class_obj is not None:
            return class_obj()

        return None


class RequestModel(Model):
    """request body models to support serialization.
    """


class ResultModel(Model):
    """response body models to support deserialization.
    """

    def __init__(
        self,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.status = ''
        self.status_code = 0
        self.request_id = ''
        self.headers: MutableMapping[str, str] = {}


class _FixedOffset(datetime.tzinfo):
    """Fixed offset in minutes east from UTC.
    :param int offset: offset in minutes
    """

    def __init__(self, offset):
        self.__offset = datetime.timedelta(minutes=offset)

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return str(self.__offset.total_seconds() / 3600)

    def __repr__(self):
        return f"<FixedOffset {self.tzname(None)}>"

    def dst(self, dt):
        return datetime.timedelta(0)


def serialize_isotime(value: datetime.datetime) -> str:
    """Serialize Datetime object into ISO-8601 formatted string

    Args:
        value (datetime.datetime): value to be serialized

    Returns:
        str: ISO-8601 formatted string, e.g 2014-05-15T11:18:32.000Z
    """
    try:
        value = value.astimezone(datetime.timezone.utc)
    except ValueError:
        # Before Python 3.8, this raised for a naive datetime.
        pass
    try:
        if value.microsecond > 0:
            return value.strftime(ISO8601_MICRO)
        return value.strftime(ISO8601)
    except ValueError:
        return value.strftime(ISO8601)


def serialize_httptime(value: datetime.datetime) -> str:
    """Serialize Datetime object into http time formatted string

    Args:
        value (datetime.datetime): value to be serialized

    Returns:
        str: http time formatted string, e.g Thu, 15 May 2014 11:18:32 GMT
    """
    try:
        value = value.astimezone(datetime.timezone.utc)
    except ValueError:
        # Before Python 3.8, this raised for a naive datetime.
        pass
    return format_datetime(value, True)


def serialize_unixtime(value: datetime.datetime) -> str:
    """Serialize Datetime object into unix time formatted string

    Args:
        value (datetime.datetime): value to be serialized

    Returns:
        str: http time formatted string, e.g 1702743657
    """
    try:
        value = value.astimezone(datetime.timezone.utc)
    except ValueError:
        # Before Python 3.8, this raised for a naive datetime.
        pass
    return str(int(value.timestamp()))


def deserialize_httptime(date_time: str) -> datetime.datetime:
    """Deserialize http datetime formatted string into Datetime object.
    """
    parsed_date = parsedate_tz(date_time)
    if not parsed_date:
        raise exceptions.DeserializationError(
            error=f'Invalid HTTP datetime {date_time}')
    tz_offset = cast(int, parsed_date[9])
    return datetime.datetime(*parsed_date[:6], tzinfo=_FixedOffset(tz_offset / 60))


def deserialize_iso(date_time: str) -> datetime.datetime:
    """Deserialize ISO-8601 formatted string into Datetime object.
    """
    if not date_time:
        return None
    if date_time[-1] == "Z":
        delta = 0
        timestamp = date_time[:-1]
    else:
        timestamp = date_time[:-6]
        sign, offset = date_time[-6], date_time[-5:]
        delta = int(sign + offset[:1]) * 60 + int(sign + offset[-2:])

    check_decimal = timestamp.split(".")
    if len(check_decimal) > 1:
        decimal_str = ""
        for digit in check_decimal[1]:
            if digit.isdigit():
                decimal_str += digit
            else:
                break
        if len(decimal_str) > 6:
            timestamp = timestamp.replace(decimal_str, decimal_str[0:6])

    if delta == 0:
        tzinfo = datetime.timezone.utc
    else:
        tzinfo = datetime.timezone(datetime.timedelta(minutes=delta))

    try:
        deserialized = datetime.datetime.strptime(
            timestamp, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        deserialized = datetime.datetime.strptime(
            timestamp, "%Y-%m-%dT%H:%M:%S")

    deserialized = deserialized.replace(tzinfo=tzinfo)
    return deserialized


def deserialize_unixtime(date_time: str) -> datetime.datetime:
    """Deserialize a datetime from a POSIX timestamp into Datetime object.
    """
    try:
        attr = int(date_time)
        date_obj = datetime.datetime.fromtimestamp(
            attr, datetime.timezone.utc)
    except ValueError as err:
        raise exceptions.DeserializationError(
            error=f'Cannot deserialize {date_time} to unix datetime object.') from err
    return date_obj


def deserialize_boolean(val: str):
    """Deserialize string into a boolean value

    For strings, the value for True/False is case insensitive
    """
    if val is None:
        return False
    return val.lower() == 'true'


def _serialize_xml_any(tag: str, value: Any, atype: str) -> ET.Element:
    if isinstance(value, Model):
        return _serialize_xml_model(value)

    if isinstance(value, datetime.datetime):
        atypes = atype.split(',')
        child = ET.Element(tag)
        if 'httptime' in atypes:
            child.text = serialize_httptime(value)
        elif 'unixtime' in atypes:
            child.text = serialize_unixtime(value)
        else:
            child.text = serialize_isotime(value)
        return child

    if isinstance(value, Enum):
        child = ET.Element(tag)
        child.text = str(value.value)
        return child

    if isinstance(value, bool):
        child = ET.Element(tag)
        child.text = str(value).lower()
        return child

    # default is basic type
    if isinstance(value, (str, int, float)):
        child = ET.Element(tag)
        child.text = str(value)
        return child

    raise exceptions.SerializationError(
        error=f'Unsupport type {type(value)}')


def _serialize_xml_model(obj, root: Optional[str] = None) -> ET.Element:
    """_summary_

    Args:
        model (Model): _description_
        root (Optional[str], optional): _description_. Defaults to None.

    Returns:
        ET.Element: _description_
    """

    if root is not None and len(root) > 0:
        name = root
    else:
        name = obj.__class__.__name__
        xml_map = getattr(obj, '_xml_map', None)
        if xml_map is not None:
            name = xml_map.get('name', name)

    elem = ET.Element(name)

    attributes = getattr(obj, '_attribute_map')
    for attr, attr_desc in attributes.items():
        if attr_desc.get('tag', '') != 'xml':
            continue
        attr_value = getattr(obj, attr)
        attr_key = attr_desc.get('rename', attr)
        attr_type = attr_desc.get('type', '')
        if attr_value is not None:
            if isinstance(attr_value, Model):
                model = cast(Model, attr_value)
                elem.append(_serialize_xml_model(model))
            elif isinstance(attr_value, list):
                elem.extend([_serialize_xml_any(attr_key, a, attr_type)
                            for a in attr_value])
            else:
                elem.append(_serialize_xml_any(
                    attr_key, attr_value, attr_type))
    return elem


def _serialize_to_str(value: Any, atype: str) -> str:
    if isinstance(value, datetime.datetime):
        atypes = atype.split(',')
        if 'httptime' in atypes:
            return serialize_httptime(value)
        if 'unixtime' in atypes:
            return serialize_unixtime(value)
        return serialize_isotime(value)

    if isinstance(value, Enum):
        return str(value.value)

    if isinstance(value, bool):
        return str(value).lower()

    # default is basic type
    if isinstance(value, (str, int, float)):
        return str(value)

    raise exceptions.SerializationError(
        error=f'Unsupport type {type(value)}')


def _deserialize_xml_model(root: ET.Element, obj: Any) -> None:
    """_summary_
    """
    attributes = getattr(obj, '_attribute_map')
    for attr, attr_desc in attributes.items():
        if attr_desc.get('tag', '') != 'xml':
            continue
        attr_key = attr_desc.get('rename', attr)
        attr_types = str(attr_desc.get('type', 'str')).split(',')

        if attr_types[0].startswith('[') and attr_types[0].endswith(']'):
            #attr_types[0] = attr_types[0][1:].removesuffix(']')
            attr_types[0] = attr_types[0][1:-1]
            value = _deserialize_xml_iter(
                obj, root.findall(attr_key), attr_types)
        else:
            value = _deserialize_xml_any(obj, root.find(attr_key), attr_types)

        if value is not None:
            setattr(obj, attr, value)


def _deserialize_xml_iter(upper_obj: Model, elems: List[ET.Element], attr_types: List[str]) -> Any:
    if elems is None or len(elems) == 0:
        return None
    return [_deserialize_xml_any(upper_obj, elem, attr_types) for elem in elems]


def _deserialize_xml_any(upper_obj: Model, elem: ET.Element, attr_types: List[str]) -> Any:
    # if elem is None or elem.text is None:
    # print(f'elem.tag={elem.tag}, elem.text={elem.text}, attr_types={attr_types}\n')
    if elem is None:
        return None

    attr_type = attr_types[0]

    if not attr_type.islower():
        obj = upper_obj._Model__create_depend_object( # pylint: disable=protected-access
            attr_type)  
        if obj is None:
            raise exceptions.DeserializationError(
                error=f'Can not create object with {attr_type} type')
        _deserialize_xml_model(elem, obj)
        return obj

    if elem.text is None:
        return None

    # basic type
    if attr_type in ('str', ''):
        return str(elem.text)

    if attr_type == 'bool':
        return deserialize_boolean(elem.text)

    if elem.text == '':
        return None

    if attr_type == 'int':
        return int(elem.text)
    if attr_type == 'float':
        return float(elem.text)
    if attr_type == 'datetime':
        return _deserialize_datetime(elem.text, attr_types)

    raise exceptions.DeserializationError(error=f'Unsupport type {attr_type}')


def _deserialize_datetime(date_time: str, subtype: List[str]) -> datetime.datetime:
    if 'httptime' in subtype:
        return deserialize_httptime(date_time)
    if 'unixtime' in subtype:
        return deserialize_unixtime(date_time)

    return deserialize_iso(date_time)


def _deserialize_to_any(value: Optional[str], atype: str) -> Any:
    if value is None:
        return None

    if atype in ('str', ''):
        return value

    if atype == 'bool':
        return deserialize_boolean(value)

    if atype == 'int':
        return int(value)
    if atype == 'float':
        return float(value)
    if 'datetime' in atype:
        return _deserialize_datetime(value, atype.split(','))

    raise exceptions.DeserializationError(error=f'Unsupport type {atype}')


def serialize_xml(obj, root: Optional[str] = None) -> Any:
    """_summary_

    Args:
        model (Model): _description_
        root (Optional[str], optional): _description_. Defaults to None.

    Returns:
        bytes: _description_
    """

    elem = _serialize_xml_model(obj, root)
    return ET.tostring(elem, encoding='utf-8', method='xml')


def deserialize_xml(xml_data: Any, obj: Any, expect_tag: Optional[str] = None) -> None:
    """_summary_
    """
    if not isinstance(obj, Model):
        return

    root = ET.fromstring(xml_data)
    if expect_tag is not None and len(expect_tag) > 0:
        if root.tag != expect_tag:
            raise exceptions.DeserializationError(
                error=f'Expect root tag is {expect_tag}, gots {root.tag}')

    _deserialize_xml_model(root, obj)


def serialize_input(request: Model, op_input: OperationInput,
                    custom_serializer: Optional[List[Any]] = None) -> OperationInput:
    """_summary_

    Args:
        request (Model): _description_
        op_input (OperationInput): _description_
        custom_serializer (Optional[List[Any]]): _description_

    Raises:
        exceptions.SerializationError: _description_
        exceptions.ParamRequiredError: _description_

    Returns:
        _type_: _description_
    """

    if not isinstance(request, RequestModel):
        raise exceptions.SerializationError(
            error=f'request<{request.__class__}> is not subclass of serde.RequestModel')

    if op_input.headers is None:
        op_input.headers = CaseInsensitiveDict()

    if op_input.parameters is None:
        op_input.parameters = {}

    if hasattr(request, 'headers'):
        headers = cast(MutableMapping[str, str], request.headers)
        if len(headers) > 0:
            for k, v in headers.items():
                op_input.headers[k] = v

    if hasattr(request, 'parameters'):
        parameters = cast(Mapping[str, str], request.parameters)
        if len(parameters) > 0:
            for k, v in parameters.items():
                op_input.parameters[k] = v

    if hasattr(request, 'payload'):
        op_input.body = request.payload

    attributes = getattr(request, '_attribute_map')
    for attr, attr_desc in attributes.items():
        attr_value = getattr(request, attr)

        if attr_value is None:
            if attr_desc.get('required', False) is True:
                raise exceptions.ParamRequiredError(field=attr)
            continue

        attr_pos = cast(str, attr_desc.get('position', ''))
        attr_type = cast(str, attr_desc.get('type', ''))
        attr_name = cast(str, attr_desc.get('rename', attr))
        if attr_pos == 'query':
            op_input.parameters.update(
                {attr_name: _serialize_to_str(attr_value, attr_type)})
        elif attr_pos == 'header':
            if 'dict' in attr_type and isinstance(attr_value, dict):
                op_input.headers.update(
                    {f'{attr_name}{k}': v for k,v in attr_value.items()})
            else:
                op_input.headers.update(
                    {attr_name: _serialize_to_str(attr_value, attr_type)})
        elif attr_pos == 'body':
            if 'xml' in attr_type:
                op_input.body = serialize_xml(
                    attr_value, attr_name if len(attr_name) > 0 else None)
            else:
                op_input.body = attr_value
        else:
            # ignore
            pass

    # custom serializer
    custom_serializer = custom_serializer or []
    for serializer in custom_serializer:
        serializer(request, op_input)

    return op_input


def deserialize_output(result: Model, op_output: OperationOutput,
                       custom_deserializer: Optional[List[Any]] = None) -> Model:
    """_summary_

    Args:
        result (Model): _description_
        op_output (OperationOutput): _description_
        custom_deserializer (Optional[List[Any]]): _description_

    Returns:
        Any: _description_
    """
    if not isinstance(result, ResultModel):
        raise exceptions.DeserializationError(
            error=f'result<{result.__class__}> is not subclass of serde.ResultModel')

    result.status = op_output.status or ''
    result.status_code = op_output.status_code or 0
    result.headers = op_output.headers or CaseInsensitiveDict()
    result.request_id = result.headers.get('x-oss-request-id', '')

    # custom deserializer
    custom_deserializer = custom_deserializer or []
    for deserializer in custom_deserializer:
        deserializer(result, op_output)

    return result


def deserialize_output_headers(result: Model, op_output: OperationOutput) -> Model:
    """_summary_

    Args:
        result (Model): _description_
        op_output (OperationOutput): _description_

    Returns:
        Any: _description_
    """
    attributes = getattr(result, '_attribute_map')
    headers = op_output.headers or {}
    dict_attrs=[]
    for attr, attr_desc in attributes.items():
        if attr_desc.get('tag', '') != 'output':
            continue
        attr_key = attr_desc.get('rename', attr)
        attr_type = attr_desc.get('type', 'str')
        if 'dict' in attr_type:
            dict_attrs.append(attr)
            continue
        value = _deserialize_to_any(
            value=headers.get(attr_key, None), atype=attr_type)
        if value is not None:
            setattr(result, attr, value)

    for  attr in  dict_attrs:
        attr_desc = attributes.get(attr)
        attr_key = attr_desc.get('rename', attr)
        dict_value = CaseInsensitiveDict()
        for k in headers.keys():
            if k.lower().startswith(attr_key):
                dict_value[k[len(attr_key):]] = headers.get(k)
        if len(dict_value) > 0:
            setattr(result, attr, dict_value)


def deserialize_output_xmlbody(result: Model, op_output: OperationOutput) -> Model:
    """_summary_

    Args:
        result (Model): _description_
        op_output (OperationOutput): _description_

    Returns:
        Any: _description_
    """
    xml_data = op_output.http_response.content

    if xml_data is None or len(xml_data) == 0:
        return result

    # parser xml body
    attributes = cast(Dict, getattr(result, '_attribute_map'))
    xml_fields = []
    xml_roots = []
    for attr, attr_desc in attributes.items():
        if attr_desc.get('tag', '') == 'xml':
            xml_fields.append(attr)

        if (attr_desc.get('tag', '') == 'output' and
            attr_desc.get('position', '') == 'body' and
                'xml' in attr_desc.get('type', '')):
            xml_roots.append(attr)

    if len(xml_fields) > 0:
        xml_map = cast(Dict, getattr(result, '_xml_map', {}))
        deserialize_xml(xml_data, result, expect_tag=xml_map.get('name', None))

    elif len(xml_roots) > 0:
        attr = xml_roots[0]
        attr_desc = attributes.get(attr)
        attr_types = cast(str, attr_desc.get('type')).split(',')
        obj = result._Model__create_depend_object(  # pylint: disable=protected-access
            attr_types[0])
        if obj is None:
            raise exceptions.DeserializationError(
                error=f'Can not create object with {attr_types} type')
        expect_tag = attr_desc.get('rename', None)
        deserialize_xml(xml_data, obj, expect_tag=expect_tag)
        setattr(result, attr, obj)

    return result


def deserialize_output_discardbody(result: Model, op_output: OperationOutput) -> Model:
    """_summary_

    Args:
        result (Model): _description_
        op_output (OperationOutput): _description_

    Returns:
        Any: _description_
    """
    _ = op_output.http_response.content
    op_output.http_response.close()
    return result


def copy_request(dst: RequestModel, src: RequestModel):
    """_summary_

    Args:
        dst (RequestModel): _description_
        src (RequestModel): _description_
    """
    dst_attr_map = getattr(dst, '_attribute_map', None)
    src_attr_map = getattr(src, '_attribute_map', None)

    if dst_attr_map is None or src_attr_map is None:
        return

    for attr, _ in dst_attr_map.items():
        src_value = getattr(src, attr, None)
        if src_value is None:
            continue
        setattr(dst, attr, src_value)
