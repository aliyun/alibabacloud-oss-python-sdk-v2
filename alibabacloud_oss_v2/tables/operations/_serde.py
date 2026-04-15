from enum import Enum
from typing import Dict, Any, Optional, List, MutableMapping, Mapping, cast
from ... import exceptions
from ...types import OperationInput, OperationOutput, CaseInsensitiveDict
from ...serde import (
    Model, 
    RequestModel, 
    deserialize_output,
    _deserialize_to_any,
    _serialize_to_str,
)
import json

def _serialize_json_model_tables(obj) -> dict:
    """serialize model to json dict
    """
    result = {}

    attributes = getattr(obj, '_attribute_map')
    for attr, attr_desc in attributes.items():
        if attr_desc.get('tag', '') != 'json':
            continue

        attr_value = getattr(obj, attr)
        attr_key = attr_desc.get('rename', attr)

        if attr_value is not None:
            if isinstance(attr_value, Model):
                result[attr_key] = _serialize_json_model_tables(attr_value)

            elif isinstance(attr_value, list):
                serialized_list = []
                for item in attr_value:
                    if isinstance(item, Model):
                        serialized_list.append(_serialize_json_model_tables(item))
                    else:
                        serialized_list.append(item)
                result[attr_key] = serialized_list

            else:
                result[attr_key] = attr_value

    return result

def _serialize_json_any_tables(value: Any) -> Any:
    if isinstance(value, Model):
        return _serialize_json_model_tables(value)

    if isinstance(value, Enum):
        return str(value.value)

    if isinstance(value, bool):
        return str(value).lower()

    # default
    return value


def serialize_input_tables_json_model(request: Model, op_input: OperationInput,
                         custom_serializer: Optional[List[Any]] = None) -> OperationInput:
    """Serialize the model request to input parameter
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

    json_data = {}

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
        elif attr_pos == 'body':
            json_data[attr_name] = _serialize_json_any_tables(attr_value)
            pass
        else:
            # ignore
            pass
    if json_data:
        op_input.body = json.dumps(json_data).encode('utf-8')


    # custom serializer
    custom_serializer = custom_serializer or []
    for serializer in custom_serializer:
        serializer(request, op_input)

    return op_input



def _deserialize_json_model_tables(data_dict: dict, obj: Any) -> None:
    """Deserialize json model

    Recursively deserialize JSON data dictionary into model object based on
    attribute mapping definitions.

    Args:
        data_dict (dict): The JSON data dictionary to deserialize
        obj (Any): The target model object to populate

    Raises:
        exceptions.DeserializationError: If object creation fails
    """
    if not isinstance(data_dict, dict):
        return

    attributes = getattr(obj, '_attribute_map', {})

    for attr, attr_desc in attributes.items():
        if attr_desc.get('tag', '') != 'json':
            continue

        attr_key = attr_desc.get('rename', attr)
        attr_types = str(attr_desc.get('type', 'str')).split(',')

        raw_value = None

        if attr_key in data_dict:
            raw_value = data_dict[attr_key]
        else:
            for key in data_dict.keys():
                if key.lower() == attr_key.lower():
                    raw_value = data_dict[key]
                    break

        if raw_value is None:
            continue

        # Handle array type
        if attr_types[0].startswith('[') and attr_types[0].endswith(']'):
            element_type = attr_types[0][1:-1]

            if not isinstance(raw_value, list):
                raw_value = [raw_value]

            value_list = []
            for item_data in raw_value:
                if element_type.islower():
                    item_value = _deserialize_to_any(
                        value=str(item_data) if not isinstance(item_data, (str, type(None))) else item_data,
                        atype=element_type
                    )
                    value_list.append(item_value)
                else:
                    item_obj = obj._Model__create_depend_object(element_type)
                    if item_obj is None:
                        raise exceptions.DeserializationError(
                            error=f'Can not create object with {element_type} type'
                        )
                    if isinstance(item_data, dict):
                        _deserialize_json_model_tables(item_data, item_obj)
                    value_list.append(item_obj)

            setattr(obj, attr, value_list)
        else:
            attr_type = attr_types[0]

            if not attr_type.islower():
                nested_obj = obj._Model__create_depend_object(attr_type)
                if nested_obj is None:
                    raise exceptions.DeserializationError(
                        error=f'Can not create object with {attr_type} type'
                    )
                if isinstance(raw_value, dict):
                    _deserialize_json_model_tables(raw_value, nested_obj)
                setattr(obj, attr, nested_obj)
            else:
                value = _deserialize_to_any(
                    value=str(raw_value) if not isinstance(raw_value, (str, type(None))) else raw_value,
                    atype=attr_type
                )
                setattr(obj, attr, value)

def deserialize_output_tables_json_model(result: Model, op_output: OperationOutput) -> Model:
    """
    Deserialize the tables response from JSON format.

    Args:
        result: The result model object
        op_output: The operation output object

    Returns:
        The deserialized result object
    """

    deserialize_output(result, op_output)

    json_data = op_output.http_response.content

    if json_data is None:
        return result

    if isinstance(json_data, (bytes, str)) and len(json_data) == 0:
        return result

    try:
        if isinstance(json_data, bytes):
            data_dict = json.loads(json_data.decode('utf-8'))
        elif isinstance(json_data, str):
            data_dict = json.loads(json_data)
        elif isinstance(json_data, dict):
            data_dict = json_data
        else:
            raise exceptions.DeserializationError(
                error=f'Unsupported json_data type: {type(json_data)}')
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise exceptions.DeserializationError(
            error=f'Failed to parse JSON data: {str(e)}') from e

    attributes = getattr(result, '_attribute_map')
    for attr, attr_desc in attributes.items():
        if attr_desc.get('tag', '') != 'output' or attr_desc.get('position', '') != 'body':
            continue

        attr_key = attr_desc.get('rename', attr)
        attr_type = attr_desc.get('type', 'str')

        raw_value = None
        if attr_key in data_dict:
            raw_value = data_dict[attr_key]

        if raw_value is None:
            continue

        if attr_type in ('dict', '[dict]'):
            setattr(result, attr, raw_value)
        else:
            # extract Model Type
            if attr_type.startswith('[') and attr_type.endswith(']'):
                element_type = attr_type[1:-1]
                if not isinstance(raw_value, list):
                    raw_value = [raw_value]

                value_list = []
                for item_data in raw_value:
                    if element_type.islower():
                        item_value = _deserialize_to_any(
                            value=str(item_data) if not isinstance(item_data, (str, type(None))) else item_data,
                            atype=element_type
                        )
                        value_list.append(item_value)
                    else:
                        item_obj = result._Model__create_depend_object(element_type)
                        if item_obj is None:
                            raise exceptions.DeserializationError(
                                error=f'Can not create object with {element_type} type'
                            )
                        if isinstance(item_data, dict):
                            _deserialize_json_model_tables(item_data, item_obj)
                        value_list.append(item_obj)

                setattr(result, attr, value_list)
            else:
                if not attr_type.islower():
                    nested_obj = result._Model__create_depend_object(attr_type)
                    if nested_obj is None:
                        raise exceptions.DeserializationError(
                            error=f'Can not create object with {attr_type} type'
                        )
                    if isinstance(raw_value, dict):
                        _deserialize_json_model_tables(raw_value, nested_obj)
                    setattr(result, attr, nested_obj)
                else:
                    value = _deserialize_to_any(
                        value=str(raw_value) if not isinstance(raw_value, (str, type(None))) else raw_value,
                        atype=attr_type
                    )
                    setattr(result, attr, value)

    return result