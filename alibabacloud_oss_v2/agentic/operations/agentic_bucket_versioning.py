# pylint: disable=line-too-long
from alibabacloud_oss_v2.types import OperationInput, CaseInsensitiveDict
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import serde_utils
from alibabacloud_oss_v2._client import _SyncClientImpl
from .. import models


def put_agentic_bucket_versioning(client: _SyncClientImpl, request: models.PutAgenticBucketVersioningRequest, **kwargs) -> models.PutAgenticBucketVersioningResult:
    """put_agentic_bucket_versioning synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutAgenticBucketVersioning',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'versioning': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.PutAgenticBucketVersioningResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def get_agentic_bucket_versioning(client: _SyncClientImpl, request: models.GetAgenticBucketVersioningRequest, **kwargs) -> models.GetAgenticBucketVersioningResult:
    """get_agentic_bucket_versioning synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAgenticBucketVersioning',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'versioning': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetAgenticBucketVersioningResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )
