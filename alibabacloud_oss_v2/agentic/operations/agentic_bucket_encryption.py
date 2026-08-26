# pylint: disable=line-too-long
from alibabacloud_oss_v2.types import OperationInput, CaseInsensitiveDict
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import serde_utils
from alibabacloud_oss_v2._client import _SyncClientImpl
from .. import models


def put_agentic_bucket_encryption(client: _SyncClientImpl, request: models.PutAgenticBucketEncryptionRequest, **kwargs) -> models.PutAgenticBucketEncryptionResult:
    """put_agentic_bucket_encryption synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutAgenticBucketEncryption',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'encryption': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.PutAgenticBucketEncryptionResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def get_agentic_bucket_encryption(client: _SyncClientImpl, request: models.GetAgenticBucketEncryptionRequest, **kwargs) -> models.GetAgenticBucketEncryptionResult:
    """get_agentic_bucket_encryption synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAgenticBucketEncryption',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'encryption': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetAgenticBucketEncryptionResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def delete_agentic_bucket_encryption(client: _SyncClientImpl, request: models.DeleteAgenticBucketEncryptionRequest, **kwargs) -> models.DeleteAgenticBucketEncryptionResult:
    """delete_agentic_bucket_encryption synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteAgenticBucketEncryption',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'encryption': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.DeleteAgenticBucketEncryptionResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )
