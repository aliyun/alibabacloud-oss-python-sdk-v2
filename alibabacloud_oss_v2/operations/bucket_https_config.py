# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def get_bucket_https_config(client: _SyncClientImpl, request: models.GetBucketHttpsConfigRequest, **kwargs) -> models.GetBucketHttpsConfigResult:
    """
    get_bucket_https_config synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketHttpsConfigRequest): The request for the GetBucketHttpsConfig operation.

    Returns:
        GetBucketHttpsConfigResult: The result for the GetBucketHttpsConfig operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketHttpsConfig',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'httpsConfig': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['httpsConfig']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketHttpsConfigResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_bucket_https_config(client: _SyncClientImpl, request: models.PutBucketHttpsConfigRequest, **kwargs) -> models.PutBucketHttpsConfigResult:
    """
    put_bucket_https_config synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketHttpsConfigRequest): The request for the PutBucketHttpsConfig operation.

    Returns:
        PutBucketHttpsConfigResult: The result for the PutBucketHttpsConfig operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketHttpsConfig',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'httpsConfig': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['httpsConfig']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketHttpsConfigResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
