# -*- coding: utf-8 -*-
"""MetaQuery operations for dataprocess."""

from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models


def open_meta_query(client: _SyncClientImpl, request: models.OpenMetaQueryRequest, **kwargs) -> models.OpenMetaQueryResult:
    """Opens meta query for a bucket."""

    op_input = OperationInput(
        op_name='OpenMetaQuery',
        method='POST',
        headers=CaseInsensitiveDict({
            'Content-Type': 'application/xml',
        }),
        parameters={
            'metaQuery': '',
            'action': 'openMetaQuery',
        },
        bucket=request.bucket,
        op_metadata={'sub-resource': ['metaQuery', 'action']},
    )

    # Serialize XML body if present
    if request.meta_query_body is not None:
        _xml_map = getattr(request.meta_query_body, '_xml_map', {})
        op_input.body = serde.serialize_xml(request.meta_query_body, root=_xml_map.get('name', None))

    op_input = serde.serialize_input(
        request=request,
        op_input=op_input,
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.OpenMetaQueryResult(),
        op_output=op_output,
    )


def get_meta_query_status(client: _SyncClientImpl, request: models.GetMetaQueryStatusRequest, **kwargs) -> models.GetMetaQueryStatusResult:
    """Gets the meta query status for a bucket."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetMetaQueryStatus',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'getMetaQueryStatus',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetMetaQueryStatusResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def close_meta_query(client: _SyncClientImpl, request: models.CloseMetaQueryRequest, **kwargs) -> models.CloseMetaQueryResult:
    """Closes meta query for a bucket."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CloseMetaQuery',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'closeMetaQuery',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['metaQuery', 'action']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CloseMetaQueryResult(),
        op_output=op_output,
    )


def do_meta_query(client: _SyncClientImpl, request: models.DoMetaQueryRequest, **kwargs) -> models.DoMetaQueryResult:
    """Performs a meta query."""

    op_input = OperationInput(
        op_name='DoMetaQuery',
        method='POST',
        headers=CaseInsensitiveDict({
            'Content-Type': 'application/xml',
        }),
        parameters={
            'metaQuery': '',
            'action': 'doMetaQuery',
        },
        bucket=request.bucket,
        op_metadata={'sub-resource': ['metaQuery', 'action']},
    )

    # Serialize XML body if present
    if request.meta_query_body is not None:
        _xml_map = getattr(request.meta_query_body, '_xml_map', {})
        op_input.body = serde.serialize_xml(request.meta_query_body, root=_xml_map.get('name', None))

    op_input = serde.serialize_input(
        request=request,
        op_input=op_input,
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DoMetaQueryResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
