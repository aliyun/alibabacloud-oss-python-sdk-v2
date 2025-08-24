import datetime
import sys
from enum import Enum
from typing import Dict, Any, Optional, List, MutableMapping, Mapping, cast
from ... import exceptions
from ...types import OperationInput, OperationOutput, CaseInsensitiveDict
from ...serde import Model, RequestModel
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
            # todo
            pass
        else:
            # ignore
            pass

    # custom serializer
    custom_serializer = custom_serializer or []
    for serializer in custom_serializer:
        serializer(request, op_input)

    return op_input    