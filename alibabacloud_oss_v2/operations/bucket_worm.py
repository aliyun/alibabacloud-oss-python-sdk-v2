# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def initiate_bucket_worm(client: _SyncClientImpl, request: models.InitiateBucketWormRequest, **kwargs) -> models.InitiateBucketWormResult:
    """
    initiate_bucket_worm synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (InitiateBucketWormRequest): The request for the InitiateBucketWorm operation.

    Returns:
        InitiateBucketWormResult: The result for the InitiateBucketWorm operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='InitiateBucketWorm',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'worm': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['worm']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.InitiateBucketWormResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde.deserialize_output_headers
        ],
    )

def abort_bucket_worm(client: _SyncClientImpl, request: models.AbortBucketWormRequest, **kwargs) -> models.AbortBucketWormResult:
    """
    abort_bucket_worm synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (AbortBucketWormRequest): The request for the AbortBucketWorm operation.

    Returns:
        AbortBucketWormResult: The result for the AbortBucketWorm operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='AbortBucketWorm',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'worm': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['worm']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.AbortBucketWormResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def complete_bucket_worm(client: _SyncClientImpl, request: models.CompleteBucketWormRequest, **kwargs) -> models.CompleteBucketWormResult:
    """
    complete_bucket_worm synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (CompleteBucketWormRequest): The request for the CompleteBucketWorm operation.

    Returns:
        CompleteBucketWormResult: The result for the CompleteBucketWorm operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CompleteBucketWorm',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            bucket=request.bucket,
            op_metadata={'sub-resource': ['wormId']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CompleteBucketWormResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def extend_bucket_worm(client: _SyncClientImpl, request: models.ExtendBucketWormRequest, **kwargs) -> models.ExtendBucketWormResult:
    """
    extend_bucket_worm synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ExtendBucketWormRequest): The request for the ExtendBucketWorm operation.

    Returns:
        ExtendBucketWormResult: The result for the ExtendBucketWorm operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ExtendBucketWorm',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'wormExtend': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['wormExtend', "wormId"]},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ExtendBucketWormResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_worm(client: _SyncClientImpl, request: models.GetBucketWormRequest, **kwargs) -> models.GetBucketWormResult:
    """
    get_bucket_worm synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketWormRequest): The request for the GetBucketWorm operation.

    Returns:
        GetBucketWormResult: The result for the GetBucketWorm operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketWorm',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'worm': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['worm']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketWormResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
