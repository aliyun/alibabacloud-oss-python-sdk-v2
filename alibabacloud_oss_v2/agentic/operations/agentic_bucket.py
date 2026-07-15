# pylint: disable=line-too-long
from alibabacloud_oss_v2.types import OperationInput, CaseInsensitiveDict
from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2 import serde_utils
from alibabacloud_oss_v2._client import _SyncClientImpl
from .. import models


def create_agentic_bucket(client: _SyncClientImpl, request: models.CreateAgenticBucketRequest, **kwargs) -> models.CreateAgenticBucketResult:
    """create_agentic_bucket synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateAgenticBucket',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.CreateAgenticBucketResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def delete_agentic_bucket(client: _SyncClientImpl, request: models.DeleteAgenticBucketRequest, **kwargs) -> models.DeleteAgenticBucketResult:
    """delete_agentic_bucket synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteAgenticBucket',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.DeleteAgenticBucketResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def get_agentic_bucket(client: _SyncClientImpl, request: models.GetAgenticBucketRequest, **kwargs) -> models.GetAgenticBucketResult:
    """get_agentic_bucket synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetAgenticBucket',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.GetAgenticBucketResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def list_agentic_buckets(client: _SyncClientImpl, request: models.ListAgenticBucketsRequest, **kwargs) -> models.ListAgenticBucketsResult:
    """list_agentic_buckets synchronously (region-level host, no bucket)"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListAgenticBuckets',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
            },
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.ListAgenticBucketsResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def put_agentic_bucket_status(client: _SyncClientImpl, request: models.PutAgenticBucketStatusRequest, **kwargs) -> models.PutAgenticBucketStatusResult:
    """put_agentic_bucket_status synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutAgenticBucketStatus',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'status': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.PutAgenticBucketStatusResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )


def list_bucket_spaces(client: _SyncClientImpl, request: models.ListBucketSpacesRequest, **kwargs) -> models.ListBucketSpacesResult:
    """list_bucket_spaces synchronously"""
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListBucketSpaces',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'agenticBucket': '',
                'bucketSpace': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[serde_utils.add_content_md5],
    )
    op_output = client.invoke_operation(op_input, **kwargs)
    return serde.deserialize_output(
        result=models.ListBucketSpacesResult(),
        op_output=op_output,
        custom_deserializer=[serde.deserialize_output_xmlbody],
    )
