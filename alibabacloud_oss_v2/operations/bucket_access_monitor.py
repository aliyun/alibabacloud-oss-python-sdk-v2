# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_access_monitor(client: _SyncClientImpl, request: models.PutBucketAccessMonitorRequest, **kwargs) -> models.PutBucketAccessMonitorResult:
    """
    put_bucket_access_monitor synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketAccessMonitorRequest): The request for the PutBucketAccessMonitor operation.

    Returns:
        PutBucketAccessMonitorResult: The result for the PutBucketAccessMonitor operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketAccessMonitor',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessmonitor': '', 
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketAccessMonitorResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_access_monitor(client: _SyncClientImpl, request: models.GetBucketAccessMonitorRequest, **kwargs) -> models.GetBucketAccessMonitorResult:
    """
    get_bucket_access_monitor synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketAccessMonitorRequest): The request for the GetBucketAccessMonitor operation.

    Returns:
        GetBucketAccessMonitorResult: The result for the GetBucketAccessMonitor operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketAccessMonitor',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'accessmonitor': '', 
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketAccessMonitorResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
