"""APIs for bucket basic operation."""
# pylint: disable=line-too-long

from ...types import OperationInput, CaseInsensitiveDict
from ... import serde
from ... import serde_utils
from ... import models
from ... import defaults
from .._aioclient import _AsyncClientImpl
from ..aio_utils import AsyncStreamBodyReader


async def put_object(client: _AsyncClientImpl, request: models.PutObjectRequest, **kwargs) -> models.PutObjectResult:
    """
    put object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (PutObjectRequest): The request for the PutObject operation.

    Returns:
        PutObjectResult: The result for the PutObject operation.
    """

    custom_serializer=[
        serde_utils.add_content_type,
        serde_utils.add_progress,
    ]

    if client.has_feature(defaults.FF_ENABLE_CRC64_CHECK_UPLOAD):
        custom_serializer.append(serde_utils.add_crc_checker)

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutObject',
            method='PUT',
            bucket=request.bucket,
            key=request.key,
        ),
        custom_serializer=custom_serializer
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    serdes = [
        serde.deserialize_output_headers
    ]

    if request.callback is not None:
        serdes.append(serde.deserialize_output_callbackbody)

    return serde.deserialize_output(
        result=models.PutObjectResult(),
        op_output=op_output,
        custom_deserializer=serdes,
    )


async def head_object(client: _AsyncClientImpl, request: models.HeadObjectRequest, **kwargs) -> models.HeadObjectResult:
    """
    head object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (HeadObjectRequest): The request for the HeadObject operation.

    Returns:
        HeadObjectResult: The result for the HeadObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='HeadObject',
            method='HEAD',
            bucket=request.bucket,
            key=request.key,
        ),
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.HeadObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )


async def get_object(client: _AsyncClientImpl, request: models.GetObjectRequest, **kwargs) -> models.GetObjectResult:
    """
    get object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (GetObjectRequest): The request for the GetObject operation.

    Returns:
        GetObjectResult: The result for the GetObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetObject',
            method='GET',
            bucket=request.bucket,
            key=request.key,
            op_metadata={'response-stream':True}
        ),
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetObjectResult(
            body=AsyncStreamBodyReader(op_output.http_response)
        ),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )


async def append_object(client: _AsyncClientImpl, request: models.AppendObjectRequest, **kwargs) -> models.AppendObjectResult:
    """
    append object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (AppendObjectRequest): The request for the AppendObject operation.

    Returns:
        AppendObjectResult: The result for the AppendObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='AppendObject',
            method='POST',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'append': '',
            },
        ),
        custom_serializer=[
            serde_utils.add_content_type,
            serde_utils.add_progress,
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.AppendObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )

async def copy_object(client: _AsyncClientImpl, request: models.CopyObjectRequest, **kwargs) -> models.CopyObjectResult:
    """
    copy object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (CopyObjectRequest): The request for the CopyObject operation.

    Returns:
        CopyObjectResult: The result for the CopyObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CopyObject',
            method='PUT',
            bucket=request.bucket,
            key=request.key,
            headers=CaseInsensitiveDict({
                'x-oss-copy-source': serde_utils.encode_copy_source(request),
            }),
        ),
        custom_serializer=[
            serde_utils.add_content_md5,
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CopyObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
            serde.deserialize_output_xmlbody
        ],
    )


async def delete_object(client: _AsyncClientImpl, request: models.DeleteObjectRequest, **kwargs) -> models.DeleteObjectResult:
    """
    copy object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (DeleteObjectRequest): The request for the DeleteObject operation.

    Returns:
        DeleteObjectResult: The result for the DeleteObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteObject',
            method='DELETE',
            bucket=request.bucket,
            key=request.key,
        ),
        custom_serializer=[
            serde_utils.add_content_md5,
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
        ],
    )


async def delete_multiple_objects(client: _AsyncClientImpl, request: models.DeleteMultipleObjectsRequest, **kwargs) -> models.DeleteMultipleObjectsResult:
    """
    delete multiple objects asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (DeleteMultipleObjectsRequest): The request for the DeleteMultipleObjects operation.

    Returns:
        DeleteMultipleObjectsResult: The result for the DeleteMultipleObjects operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteMultipleObjects',
            method='POST',
            bucket=request.bucket,
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'delete': '',
                'encoding-type': 'url',
            }
        ),
        custom_serializer=[
            serde_utils.serialize_delete_objects,
            serde_utils.add_content_md5,
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteMultipleObjectsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde.deserialize_output_headers,
            serde_utils.deserialize_encode_type
        ],
    )


async def get_object_meta(client: _AsyncClientImpl, request: models.GetObjectMetaRequest, **kwargs) -> models.GetObjectMetaResult:
    """
    get object meta asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (GetObjectMetaRequest): The request for the GetObjectMeta operation.

    Returns:
        GetObjectMetaResult: The result for the GetObjectMeta operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetObjectMeta',
            method='HEAD',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'objectMeta': '',
            }
        ),
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetObjectMetaResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )


async def restore_object(client: _AsyncClientImpl, request: models.RestoreObjectRequest, **kwargs) -> models.RestoreObjectResult:
    """
    restore object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (RestoreObjectRequest): The request for the RestoreObject operation.

    Returns:
        RestoreObjectResult: The result for the RestoreObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='RestoreObject',
            method='POST',
            bucket=request.bucket,
            key=request.key,
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'restore': '',
            }
        ),
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.RestoreObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )


async def put_object_acl(client: _AsyncClientImpl, request: models.PutObjectAclRequest, **kwargs) -> models.PutObjectAclResult:
    """
    put object acl asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (PutObjectAclRequest): The request for the PutObjectAcl operation.

    Returns:
        PutObjectAclResult: The result for the PutObjectAcl operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutObjectAcl',
            method='PUT',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'acl': '',
            }
        ),
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutObjectAclResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )


async def get_object_acl(client: _AsyncClientImpl, request: models.GetObjectAclRequest, **kwargs) -> models.GetObjectAclResult:
    """
    get object acl asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (GetObjectAclRequest): The request for the GetObjectAcl operation.

    Returns:
        GetObjectAclResult: The result for the GetObjectAcl operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetObjectAcl',
            method='GET',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'acl': '',
            }
        ),
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetObjectAclResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde.deserialize_output_headers
        ],
    )


async def initiate_multipart_upload(client: _AsyncClientImpl, request: models.InitiateMultipartUploadRequest, **kwargs) -> models.InitiateMultipartUploadResult:
    """
    initiate multipart upload asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (InitiateMultipartUploadRequest): The request for the InitiateMultipartUpload operation.

    Returns:
        InitiateMultipartUploadResult: The result for the InitiateMultipartUpload operation.
    """

    serializer = [serde_utils.add_content_md5]
    if not request.disable_auto_detect_mime_type:
        serializer.append(serde_utils.add_content_type)

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='InitiateMultipartUpload',
            method='POST',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'uploads': '',
                'encoding-type': 'url',
            }
        ),
        custom_serializer=serializer,
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.InitiateMultipartUploadResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde_utils.deserialize_encode_type
        ],
    )


async def upload_part(client: _AsyncClientImpl, request: models.UploadPartRequest, **kwargs) -> models.UploadPartResult:
    """
    upload part asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (UploadPartRequest): The request for the UploadPart operation.

    Returns:
        UploadPartResult: The result for the UploadPart operation.
    """

    custom_serializer=[serde_utils.add_progress]

    if client.has_feature(defaults.FF_ENABLE_CRC64_CHECK_UPLOAD):
        custom_serializer.append(serde_utils.add_crc_checker)


    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='UploadPart',
            method='PUT',
            bucket=request.bucket,
            key=request.key,
        ),
        custom_serializer=custom_serializer
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.UploadPartResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )


async def upload_part_copy(client: _AsyncClientImpl, request: models.UploadPartCopyRequest, **kwargs) -> models.UploadPartCopyResult:
    """
    upload part copy asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (UploadPartCopyRequest): The request for the UploadPartCopy operation.

    Returns:
        UploadPartCopyResult: The result for the UploadPartCopy operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='UploadPartCopy',
            method='PUT',
            bucket=request.bucket,
            key=request.key,
            headers=CaseInsensitiveDict({
                'x-oss-copy-source': serde_utils.encode_copy_source(request),
            }),
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.UploadPartCopyResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde.deserialize_output_headers
        ],
    )


async def complete_multipart_upload(client: _AsyncClientImpl, request: models.CompleteMultipartUploadRequest, **kwargs) -> models.CompleteMultipartUploadResult:
    """
    complete multipart upload asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (CompleteMultipartUploadRequest): The request for the CompleteMultipartUpload operation.

    Returns:
        CompleteMultipartUploadResult: The result for the CompleteMultipartUpload operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CompleteMultipartUpload',
            method='POST',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'encoding-type': 'url',
            }
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    deserializer = [serde.deserialize_output_headers]
    if request.callback is None:
        deserializer.append(serde.deserialize_output_xmlbody)
        deserializer.append(serde_utils.deserialize_encode_type)
    else:
        deserializer.append(serde.deserialize_output_callbackbody)

    return serde.deserialize_output(
        result=models.CompleteMultipartUploadResult(),
        op_output=op_output,
        custom_deserializer=deserializer,
    )


async def abort_multipart_upload(client: _AsyncClientImpl, request: models.AbortMultipartUploadRequest, **kwargs) -> models.AbortMultipartUploadResult:
    """
    abort multipart upload asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (AbortMultipartUploadRequest): The request for the AbortMultipartUpload operation.

    Returns:
        AbortMultipartUploadResult: The result for the AbortMultipartUpload operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='AbortMultipartUpload',
            method='DELETE',
            bucket=request.bucket,
            key=request.key,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.AbortMultipartUploadResult(),
        op_output=op_output,
    )



async def list_multipart_uploads(client: _AsyncClientImpl, request: models.ListMultipartUploadsRequest, **kwargs) -> models.ListMultipartUploadsResult:
    """
    list multipart uploads asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (ListMultipartUploadsRequest): The request for the ListMultipartUploads operation.

    Returns:
        ListMultipartUploadsResult: The result for the ListMultipartUploads operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListMultipartUploads',
            method='GET',
            bucket=request.bucket,
            parameters={
                'encoding-type': 'url',
                'uploads': '',
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListMultipartUploadsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde_utils.deserialize_encode_type
        ],
    )



async def list_parts(client: _AsyncClientImpl, request: models.ListPartsRequest, **kwargs) -> models.ListPartsResult:
    """
    list parts asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (ListPartsRequest): The request for the ListParts operation.

    Returns:
        ListPartsResult: The result for the ListParts operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListParts',
            method='GET',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'encoding-type': 'url',
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListPartsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde_utils.deserialize_encode_type
        ],
    )



async def put_symlink(client: _AsyncClientImpl, request: models.PutSymlinkRequest, **kwargs) -> models.PutSymlinkResult:
    """
    put symlink asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (PutSymlinkRequest): The request for the PutSymlink operation.

    Returns:
        PutSymlinkResult: The result for the PutSymlink operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutSymlink',
            method='PUT',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'symlink': '',
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutSymlinkResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )



async def get_symlink(client: _AsyncClientImpl, request: models.GetSymlinkRequest, **kwargs) -> models.GetSymlinkResult:
    """
    get symlink asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (GetSymlinkRequest): The request for the GetSymlink operation.

    Returns:
        GetSymlinkResult: The result for the GetSymlink operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetSymlink',
            method='GET',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'symlink': '',
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetSymlinkResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )



async def put_object_tagging(client: _AsyncClientImpl, request: models.PutObjectTaggingRequest, **kwargs) -> models.PutObjectTaggingResult:
    """
    put object tagging asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (PutObjectTaggingRequest): The request for the PutObjectTagging operation.

    Returns:
        PutObjectTaggingResult: The result for the PutObjectTagging operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutObjectTagging',
            method='PUT',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'tagging': '',
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutObjectTaggingResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )



async def get_object_tagging(client: _AsyncClientImpl, request: models.GetObjectTaggingRequest, **kwargs) -> models.GetObjectTaggingResult:
    """
    get object tagging asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (GetObjectTaggingRequest): The request for the GetObjectTagging operation.

    Returns:
        GetObjectTaggingResult: The result for the GetObjectTagging operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetObjectTagging',
            method='GET',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'tagging': '',
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetObjectTaggingResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde.deserialize_output_headers
        ],
    )



async def delete_object_tagging(client: _AsyncClientImpl, request: models.DeleteObjectTaggingRequest, **kwargs) -> models.DeleteObjectTaggingResult:
    """
    delete object tagging asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (DeleteObjectTaggingRequest): The request for the DeleteObjectTagging operation.

    Returns:
        DeleteObjectTaggingResult: The result for the DeleteObjectTagging operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteObjectTagging',
            method='DELETE',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'tagging': '',
            },
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetObjectTaggingResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )


async def process_object(client: _AsyncClientImpl, request: models.ProcessObjectRequest, **kwargs) -> models.ProcessObjectResult:
    """
    process object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (ProcessObjectRequest): The request for the ProcessObject operation.

    Returns:
        ProcessObjectResult: The result for the ProcessObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ProcessObject',
            method='POST',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'x-oss-process': '',
            },
        ),
        custom_serializer=[
            serde_utils.add_process_action,
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ProcessObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
            serde_utils.deserialize_process_body
        ],
    )


async def async_process_object(client: _AsyncClientImpl, request: models.AsyncProcessObjectRequest, **kwargs) -> models.AsyncProcessObjectResult:
    """
    async process object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (AsyncProcessObjectRequest): The request for the AsyncProcessObject operation.

    Returns:
        AsyncProcessObjectResult: The result for the AsyncProcessObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='AsyncProcessObject',
            method='POST',
            bucket=request.bucket,
            key=request.key,
            parameters={
                'x-oss-async-process': '',
            },
        ),
        custom_serializer=[
            serde_utils.add_process_action,
            serde_utils.add_content_md5
        ],
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.AsyncProcessObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers,
            serde_utils.deserialize_process_body
        ],
    )

async def clean_restored_object(client: _AsyncClientImpl, request: models.CleanRestoredObjectRequest, **kwargs) -> models.CleanRestoredObjectResult:
    """
    clean_restored_object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (CleanRestoredObjectRequest): The request for the CleanRestoredObject operation.

    Returns:
        CleanRestoredObjectResult: The result for the CleanRestoredObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CleanRestoredObject',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'cleanRestoredObject': '',
            },
            bucket=request.bucket,
            key=request.key,
            op_metadata={'sub-resource': ['cleanRestoredObject']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.CleanRestoredObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


async def seal_append_object(client: _AsyncClientImpl, request: models.SealAppendObjectRequest, **kwargs) -> models.SealAppendObjectResult:
    """
    seal_append_object asynchronously

    Args:
        client (_AsyncClientImpl): A agent that sends the request.
        request (SealAppendObjectRequest): The request for the SealAppendObject operation.

    Returns:
        SealAppendObjectResult: The result for the SealAppendObject operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='SealAppendObject',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'seal': '',
                'position': str(request.position),
            },
            bucket=request.bucket,
            key=request.key,
            op_metadata={'sub-resource': ['seal']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = await client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.SealAppendObjectResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_headers
        ],
    )
