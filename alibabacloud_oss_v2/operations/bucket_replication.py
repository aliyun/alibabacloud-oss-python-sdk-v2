# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_rtc(client: _SyncClientImpl, request: models.PutBucketRtcRequest, **kwargs) -> models.PutBucketRtcResult:
    """
    put_bucket_rtc synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketRtcRequest): The request for the PutBucketRtc operation.

    Returns:
        PutBucketRtcResult: The result for the PutBucketRtc operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketRtc',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'rtc': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['rtc']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketRtcResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_bucket_replication(client: _SyncClientImpl, request: models.PutBucketReplicationRequest, **kwargs) -> models.PutBucketReplicationResult:
    """
    put_bucket_replication synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketReplicationRequest): The request for the PutBucketReplication operation.

    Returns:
        PutBucketReplicationResult: The result for the PutBucketReplication operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketReplication',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'comp': 'add', 
                'replication': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['replication', 'comp']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketReplicationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_replication(client: _SyncClientImpl, request: models.GetBucketReplicationRequest, **kwargs) -> models.GetBucketReplicationResult:
    """
    get_bucket_replication synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketReplicationRequest): The request for the GetBucketReplication operation.

    Returns:
        GetBucketReplicationResult: The result for the GetBucketReplication operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketReplication',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'replication': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['replication']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketReplicationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_replication_location(client: _SyncClientImpl, request: models.GetBucketReplicationLocationRequest, **kwargs) -> models.GetBucketReplicationLocationResult:
    """
    get_bucket_replication_location synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketReplicationLocationRequest): The request for the GetBucketReplicationLocation operation.

    Returns:
        GetBucketReplicationLocationResult: The result for the GetBucketReplicationLocation operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketReplicationLocation',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'replicationLocation': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['replicationLocation']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketReplicationLocationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_replication_progress(client: _SyncClientImpl, request: models.GetBucketReplicationProgressRequest, **kwargs) -> models.GetBucketReplicationProgressResult:
    """
    get_bucket_replication_progress synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketReplicationProgressRequest): The request for the GetBucketReplicationProgress operation.

    Returns:
        GetBucketReplicationProgressResult: The result for the GetBucketReplicationProgress operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketReplicationProgress',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'replicationProgress': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['replicationProgress']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketReplicationProgressResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_replication(client: _SyncClientImpl, request: models.DeleteBucketReplicationRequest, **kwargs) -> models.DeleteBucketReplicationResult:
    """
    delete_bucket_replication synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketReplicationRequest): The request for the DeleteBucketReplication operation.

    Returns:
        DeleteBucketReplicationResult: The result for the DeleteBucketReplication operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketReplication',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'comp': 'delete', 
                'replication': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['replication' ,'comp']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketReplicationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
