"""utils for api only"""

import hashlib
import base64
import json
from urllib.parse import unquote, quote
from typing import List, cast, Union, Dict
from .types import OperationInput, HttpResponse, OperationOutput
from . import serde
from . import utils
from . import exceptions
from . import progress
from . import crc
from .models import (
    ListObjectsResult,
    ListObjectsV2Result,
    ListObjectVersionsResult,
    CopyObjectRequest,
    UploadPartCopyRequest,
    DeleteMultipleObjectsRequest,
    DeleteMultipleObjectsResult,
    InitiateMultipartUploadResult,
    CompleteMultipartUploadResult,
    ListMultipartUploadsResult,
    ListPartsResult,
    ProcessObjectRequest,
    AsyncProcessObjectRequest    
)


def add_content_type(_: serde.Model, op_input: OperationInput) -> OperationInput:
    """
    Add content-type based on the file suffix when it does not exist.
    """
    if op_input.headers.get('Content-Type', None) is not None:
        return op_input

    op_input.headers.update({
        'Content-Type': utils.guess_content_type(op_input.key, "application/octet-stream")
    })

    return op_input


def add_content_md5(_: serde.Model, op_input: OperationInput) -> OperationInput:
    """
    Add content-md5 when it does not exist.
    """
    if op_input.headers.get('Content-MD5', None) is not None:
        return op_input

    if op_input.body is None:
        md5 = '1B2M2Y8AsgTpgAmY7PhCfg=='
    elif isinstance(op_input.body, (str, bytes)):
        h = hashlib.md5()
        h.update(op_input.body)
        md5 = base64.b64encode(h.digest()).decode()
    else:
        raise exceptions.SerializationError(
            error=f'add_content_md5 fail, not support instance <{op_input.body.__class__}>')

    op_input.headers.update({'Content-MD5': md5})
    return op_input


def add_progress(request: serde.Model, op_input: OperationInput) -> OperationInput:
    """
    Add progress writer when progress_fn is set.
    """

    fn = getattr(request, 'progress_fn', None)
    if fn is None:
        return op_input

    trackers = cast(List, op_input.op_metadata.get(
        'opm-request-body-tracker', []))
    p = progress.Progress(
        progress_fn=fn,
        total=utils.guess_content_length(op_input.body)
    )
    trackers.append(p)
    op_input.op_metadata['opm-request-body-tracker'] = trackers

    return op_input


def add_crc_checker(_: serde.Model, op_input: OperationInput) -> OperationInput:
    """
    Add crc writer and crc checker.
    """

    trackers = cast(List, op_input.op_metadata.get(
        'opm-request-body-tracker', []))
    p = crc.Crc64(init_crc=0)
    trackers.append(p)
    op_input.op_metadata['opm-request-body-tracker'] = trackers

    handlers = cast(List, op_input.op_metadata.get(
        'opm-response-handler', []))

    def crc_checker_handler(response: HttpResponse):
        scrc = response.headers.get('x-oss-hash-crc64ecma', None)
        if scrc is None:
            return
        ccrc = str(p.sum64())

        if scrc != ccrc:
            raise exceptions.InconsistentError(
                client_crc=ccrc,
                server_crc=scrc
            )

    handlers.append(crc_checker_handler)
    op_input.op_metadata['opm-response-handler'] = handlers

    return op_input

def deserialize_encode_type(result: serde.Model, _: OperationOutput) -> serde.Model:
    """
    do url decode
    """

    if not hasattr(result, 'encoding_type'):
        raise exceptions.DeserializationError(
            error=f'{result.__class__} has not encoding_type attribute')

    if result.encoding_type is None or result.encoding_type != 'url':
        return result

    if isinstance(result, ListObjectsResult):
        # fields
        fields = ['prefix', 'marker', 'delimiter', 'next_marker']

        # Contents.Key
        if isinstance(result.contents, List):
            for i, _ in enumerate(result.contents):
                result.contents[i].key = unquote(result.contents[i].key)

        # CommonPrefixes.Prefix
        if isinstance(result.common_prefixes, List):
            for i, _ in enumerate(result.common_prefixes):
                result.common_prefixes[i].prefix = unquote(
                    result.common_prefixes[i].prefix)

    elif isinstance(result, ListObjectsV2Result):
        # fields
        fields = ['prefix', 'start_after', 'continuation_token', 'delimiter', 'next_continuation_token']

        # Contents.Key
        if isinstance(result.contents, List):
            for i, _ in enumerate(result.contents):
                result.contents[i].key = unquote(result.contents[i].key)

        # CommonPrefixes.Prefix
        if isinstance(result.common_prefixes, List):
            for i, _ in enumerate(result.common_prefixes):
                result.common_prefixes[i].prefix = unquote(
                    result.common_prefixes[i].prefix)

    elif isinstance(result, ListObjectVersionsResult):
        # fields
        fields = ['prefix', 'key_marker', 'delimiter', 'next_key_marker']

        # Version.Key
        if isinstance(result.version, List):
            for i, _ in enumerate(result.version):
                result.version[i].key = unquote(result.version[i].key)

        # DeleteMarker.Key
        if isinstance(result.delete_marker, List):
            for i, _ in enumerate(result.delete_marker):
                result.delete_marker[i].key = unquote(result.delete_marker[i].key)

        # CommonPrefixes.Prefix
        if isinstance(result.common_prefixes, List):
            for i, _ in enumerate(result.common_prefixes):
                result.common_prefixes[i].prefix = unquote(
                    result.common_prefixes[i].prefix)

    elif isinstance(result, DeleteMultipleObjectsResult):
        # fields
        fields = []

        # deleted_objects.Key
        if isinstance(result.deleted_objects, List):
            for i, _ in enumerate(result.deleted_objects):
                result.deleted_objects[i].key = unquote(result.deleted_objects[i].key)

    elif isinstance(result, InitiateMultipartUploadResult):
        # fields
        fields = ['key']

    elif isinstance(result, CompleteMultipartUploadResult):
        # fields
        fields = ['key']

    elif isinstance(result, ListMultipartUploadsResult):
        # fields
        fields = ['key_marker', 'next_key_marker', 'prefix', 'delimiter']

        # Upload.Key
        if isinstance(result.uploads, List):
            for i, _ in enumerate(result.uploads):
                result.uploads[i].key = unquote(result.uploads[i].key)

    elif isinstance(result, ListPartsResult):
        # fields
        fields = ['key']

    else:
        fields = []

    for field in fields:
        val = getattr(result, field)
        if val is not None:
            setattr(result, field, unquote(val))

    return result

def encode_copy_source(request: Union[CopyObjectRequest, UploadPartCopyRequest]) -> str:
    """
    encode copy source parameter
    """
    source = f'/{request.source_bucket or request.bucket}/{quote(request.source_key)}'
    if request.source_version_id is not None:
        source += f'?versionId={request.source_version_id}'

    return source


def serialize_delete_objects(request: serde.Model, op_input: OperationInput) -> OperationInput:
    """
    serialize to Delete XML string
    """
    if not isinstance(request, DeleteMultipleObjectsRequest):
        raise exceptions.SerializationError(error=f'Unsupport type {type(request)}')

    # Check if both old and new parameters are set or neither is set
    if request.objects is not None and request.delete is not None:
        raise exceptions.SerializationError(
            error='Either old parameters (objects, quiet) or new parameter (delete) is set, but not both'
        )

    xml = '<Delete>'
    
    # Handle new parameter (delete)
    if request.delete is not None:
        if request.delete.objects is None:
            raise exceptions.ParamRequiredError(field='delete.objects')

        if request.delete.quiet is not None:
            xml += f'<Quiet>{"true" if request.delete.quiet else "false"}</Quiet>'

        if isinstance(request.delete.objects, List):
            for _, o in enumerate(request.delete.objects):
                xml += '<Object>'
                key = utils.safety_str(o.key)
                if len(key) > 0:
                    xml += f'<Key>{utils.escape_xml_value(key)}</Key>'
                vid = utils.safety_str(o.version_id)
                if len(vid) > 0:
                    xml += f'<VersionId>{vid}</VersionId>'
                xml += '</Object>'
    
    # Handle old parameters (objects, quiet)
    else:
        if request.objects is None:
            raise exceptions.ParamRequiredError(field='request.objects')

        if request.quiet is not None:
            xml += f'<Quiet>{"true" if request.quiet else "false"}</Quiet>'

        if isinstance(request.objects, List):
            for _, o in enumerate(request.objects):
                xml += '<Object>'
                key = utils.safety_str(o.key)
                if len(key) > 0:
                    xml += f'<Key>{utils.escape_xml_value(key)}</Key>'
                vid = utils.safety_str(o.version_id)
                if len(vid) > 0:
                    xml += f'<VersionId>{vid}</VersionId>'
                xml += '</Object>'

    xml += '</Delete>'

    op_input.body = xml.encode()

    return op_input

def add_process_action(request: serde.Model, op_input: OperationInput) -> OperationInput:
    """
    Add process parameter to body.
    """
    if not isinstance(request, ProcessObjectRequest) and not isinstance(request, AsyncProcessObjectRequest):
        raise exceptions.SerializationError(error=f'Unsupport type {type(request)}')

    attr_map = cast(Dict, getattr(request, '_attribute_map'))
    attr_desc = cast(Dict, attr_map.get('process'))
    key = attr_desc.get('rename', None)

    if key is None:
        raise exceptions.SerializationError(error='process filed is invalid')

    op_input.body = f'{key}={request.process}'.encode()
    return op_input


def deserialize_process_body(result: serde.Model, op_output: OperationOutput) -> serde.Model:
    """deserialize process body
    """
    xml_data = op_output.http_response.content

    if xml_data is None or len(xml_data) == 0:
        return result

    jo = json.loads(xml_data)

    if not isinstance(jo, Dict):
        return result

    # parse json body
    attributes = cast(Dict, getattr(result, '_attribute_map'))
    for attr, attr_desc in attributes.items():
        if attr_desc.get('tag', '') != 'json':
            continue
        attr_key = attr_desc.get('rename', attr)
        value = jo.get(attr_key, None)
        if value is not None:
            setattr(result, attr, value)

    return result
