# pylint: disable=line-too-long
from alibabacloud_oss_v2.types import OperationInput, CaseInsensitiveDict
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import serde_utils
from alibabacloud_oss_v2._client import _SyncClientImpl
from .. import models


def put_agentic_bucket_public_access_block(client: _SyncClientImpl, request: models.PutAgenticBucketPublicAccessBlockRequest, **kwargs) -> models.PutAgenticBucketPublicAccessBlockResult:
    """put_agentic_bucket_public_access_block synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutAgenticBucketPublicAccessBlock',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'publicAccessBlock': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.PutAgenticBucketPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def get_agentic_bucket_public_access_block(client: _SyncClientImpl, request: models.GetAgenticBucketPublicAccessBlockRequest, **kwargs) -> models.GetAgenticBucketPublicAccessBlockResult:
    """get_agentic_bucket_public_access_block synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAgenticBucketPublicAccessBlock',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'publicAccessBlock': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetAgenticBucketPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def delete_agentic_bucket_public_access_block(client: _SyncClientImpl, request: models.DeleteAgenticBucketPublicAccessBlockRequest, **kwargs) -> models.DeleteAgenticBucketPublicAccessBlockResult:
    """delete_agentic_bucket_public_access_block synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteAgenticBucketPublicAccessBlock',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'publicAccessBlock': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.DeleteAgenticBucketPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )
