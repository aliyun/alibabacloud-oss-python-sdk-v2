from typing import Dict, Any, Optional, List, MutableMapping, Mapping, cast
from ... import exceptions
from ...types import OperationInput, OperationOutput, CaseInsensitiveDict
from ...serde import Model, RequestModel, deserialize_output, _deserialize_datetime, _deserialize_to_any, deserialize_json
import json

def serialize_input_vector_json_model(request: Model, op_input: OperationInput,
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
        if attr_pos == 'body':
            json_data[attr_name] = attr_value
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


def deserialize_output_vector_json_model(result: Model, op_output: OperationOutput) -> Model:
    """
    Deserialize the vector index response from JSON format.

    Args:
        result: The result model object
        op_output: The operation output object

    Returns:
        The deserialized result object
    """

    deserialize_output(result, op_output)

    json_data = op_output.http_response.content

    if json_data is None or len(json_data) == 0:
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
        else:
            for key in data_dict.keys():
                if key.lower() == attr_key.lower():
                    raw_value = data_dict[key]
                    break

        if raw_value is None:
            continue

        if attr_type in ('str', 'int', 'float', 'bool') or 'datetime' in attr_type:
            value = _deserialize_to_any(value=str(raw_value) if not isinstance(raw_value, (str, type(None))) else raw_value, atype=attr_type)
            setattr(result, attr, value)
        elif attr_type == 'dict':
            setattr(result, attr, raw_value)
        else:
            setattr(result, attr, raw_value)

    return result