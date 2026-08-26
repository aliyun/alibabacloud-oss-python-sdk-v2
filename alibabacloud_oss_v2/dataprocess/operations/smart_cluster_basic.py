# -*- coding: utf-8 -*-
"""SmartCluster operations for dataprocess."""

from ..._client import _SyncClientImpl
from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from .. import models


def create_smart_cluster(client: _SyncClientImpl, request: models.CreateSmartClusterRequest, **kwargs) -> models.CreateSmartClusterResult:
    """Creates a smart cluster."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateSmartCluster',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'createSmartCluster',
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
        result=models.CreateSmartClusterResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def get_smart_cluster(client: _SyncClientImpl, request: models.GetSmartClusterRequest, **kwargs) -> models.GetSmartClusterResult:
    """Gets a smart cluster."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetSmartCluster',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'getSmartCluster',
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
        result=models.GetSmartClusterResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def update_smart_cluster(client: _SyncClientImpl, request: models.UpdateSmartClusterRequest, **kwargs) -> models.UpdateSmartClusterResult:
    """Updates a smart cluster."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='UpdateSmartCluster',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'updateSmartCluster',
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
        result=models.UpdateSmartClusterResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def delete_smart_cluster(client: _SyncClientImpl, request: models.DeleteSmartClusterRequest, **kwargs) -> models.DeleteSmartClusterResult:
    """Deletes a smart cluster."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteSmartCluster',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'deleteSmartCluster',
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
        result=models.DeleteSmartClusterResult(),
        op_output=op_output,
    )


def list_smart_clusters(client: _SyncClientImpl, request: models.ListSmartClustersRequest, **kwargs) -> models.ListSmartClustersResult:
    """Lists smart clusters."""

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListSmartClusters',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'metaQuery': '',
                'action': 'listSmartClusters',
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
        result=models.ListSmartClustersResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
