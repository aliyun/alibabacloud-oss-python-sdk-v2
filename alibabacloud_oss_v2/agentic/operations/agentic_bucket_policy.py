# pylint: disable=line-too-long
from alibabacloud_oss_v2.types import OperationInput, CaseInsensitiveDict
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import serde_utils
from alibabacloud_oss_v2._client import _SyncClientImpl
from .. import models


def put_agentic_bucket_policy(client: _SyncClientImpl, request: models.PutAgenticBucketPolicyRequest, **kwargs) -> models.PutAgenticBucketPolicyResult:
    """put_agentic_bucket_policy synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutAgenticBucketPolicy',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json',
            }),
            parameters={
                'agenticBucket': '',
                'policy': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.PutAgenticBucketPolicyResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def get_agentic_bucket_policy(client: _SyncClientImpl, request: models.GetAgenticBucketPolicyRequest, **kwargs) -> models.GetAgenticBucketPolicyResult:
    """get_agentic_bucket_policy synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAgenticBucketPolicy',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'policy': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetAgenticBucketPolicyResult(
            body=op_output.http_response.content.decode()
        ),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def delete_agentic_bucket_policy(client: _SyncClientImpl, request: models.DeleteAgenticBucketPolicyRequest, **kwargs) -> models.DeleteAgenticBucketPolicyResult:
    """delete_agentic_bucket_policy synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteAgenticBucketPolicy',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'policy': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.DeleteAgenticBucketPolicyResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )
