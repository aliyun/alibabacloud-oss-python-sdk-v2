"""APIs for bucket basic operation."""
# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket(client: _SyncClientImpl, request: models.PutBucketRequest, **kwargs) -> models.PutBucketResult:
    """
    put bucket synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketRequest): The request for the PutBucket operation.

    Returns:
        PutBucketResult: The result for the PutBucket operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucket',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_discardbody
        ],
    )


def delete_bucket(client: _SyncClientImpl, request: models.DeleteBucketRequest, **kwargs) -> models.DeleteBucketResult:
    """
    delete bucket synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketRequest): The request for the DeleteBucket operation.

    Returns:
        DeleteBucketResult: The result for the DeleteBucket operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucket',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_discardbody
        ],
    )


def list_objects(client: _SyncClientImpl, request: models.ListObjectsRequest, **kwargs) -> models.ListObjectsResult:
    """
    list objects synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListObjectsRequest): The request for the ListObjects operation.

    Returns:
        ListObjectsResult: The result for the ListObjects operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListObjects',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/octet-stream',
            }),
            parameters={
                'encoding-type': 'url',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListObjectsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde_utils.deserialize_encode_type
        ],
    )

def put_bucket_acl(client: _SyncClientImpl, request: models.PutBucketAclRequest, **kwargs) -> models.PutBucketAclResult:
    """
    put bucket acl

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketAclRequest): The request for the PutBucketAcl operation.

    Returns:
        PutBucketAclResult: The result for the PutBucketAcl operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketAcl',
            method='PUT',
            parameters={
                'acl': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketAclResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_discardbody
        ],
    )


def get_bucket_acl(client: _SyncClientImpl, request: models.GetBucketAclRequest, **kwargs) -> models.GetBucketAclResult:
    """
    get bucket acl

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketAclRequest): The request for the GetBucketAcl operation.

    Returns:
        GetBucketAclResult: The result for the GetBucketAcl operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketAcl',
            method='GET',
            parameters={
                'acl': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketAclResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def list_objects_v2(client: _SyncClientImpl, request: models.ListObjectsV2Request, **kwargs) -> models.ListObjectsV2Result:
    """
    list objects synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListObjectsV2Request): The request for the ListObjectsV2 operation.

    Returns:
        ListObjectsV2Result: The result for the ListObjectsV2 operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListObjectsV2',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/octet-stream',
            }),
            parameters={
                'encoding-type': 'url',
                'list-type': 2,
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListObjectsV2Result(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde_utils.deserialize_encode_type
        ],
    )

def get_bucket_stat(client: _SyncClientImpl, request: models.GetBucketStatRequest, **kwargs) -> models.GetBucketStatResult:
    """
    GetBucketStat Queries the storage capacity of a specified bucket and the number of objects that are stored in the bucket.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketStatRequest): The request for the GetBucketStat operation.

    Returns:
        GetBucketStatResult: The result for the GetBucketStat operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketStat',
            method='GET',
            parameters={
                'stat': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketStatResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def get_bucket_location(client: _SyncClientImpl, request: models.GetBucketLocationRequest, **kwargs) -> models.GetBucketLocationResult:
    """
    GetBucketLocation Queries the region of an Object Storage Service (OSS) bucket.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketLocationRequest): The request for the GetBucketLocation operation.

    Returns:
        GetBucketLocationResult: The result for the GetBucketLocation operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketLocation',
            method='GET',
            parameters={
                'location': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketLocationResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def get_bucket_info(client: _SyncClientImpl, request: models.GetBucketInfoRequest, **kwargs) -> models.GetBucketInfoResult:
    """
    GetBucketInfo Queries information about a bucket.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketInfoRequest): The request for the GetBucketInfo operation.

    Returns:
        GetBucketInfoResult: The result for the GetBucketInfo operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketInfo',
            method='GET',
            parameters={
                'bucketInfo': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketInfoResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def put_bucket_versioning(client: _SyncClientImpl, request: models.PutBucketVersioningRequest, **kwargs) -> models.PutBucketVersioningResult:
    """
    PutBucketVersioning Configures the versioning state for a bucket.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketVersioningRequest): The request for the PutBucketVersioning operation.

    Returns:
        PutBucketVersioningResult: The result for the PutBucketVersioning operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketVersioning',
            method='PUT',
            parameters={
                'versioning': '',
            },
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketVersioningResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_discardbody
        ],
    )


def get_bucket_versioning(client: _SyncClientImpl, request: models.GetBucketVersioningRequest, **kwargs) -> models.GetBucketVersioningResult:
    """
    GetBucketVersioning You can call this operation to query the versioning state of a bucket.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketVersioningRequest): The request for the GetBucketVersioning operation.

    Returns:
        GetBucketVersioningResult: The result for the GetBucketVersioning operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketVersioning',
            method='GET',
            parameters={
                'versioning': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketVersioningResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def list_object_versions(client: _SyncClientImpl, request: models.ListObjectVersionsRequest, **kwargs) -> models.ListObjectVersionsResult:
    """
    ListObjectVersions Lists the versions of all objects in a bucket, including delete markers.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListObjectVersionsRequest): The request for the ListObjectVersions operation.

    Returns:
        ListObjectVersionsResult: The result for the ListObjectVersions operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='ListObjectVersions',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/octet-stream',
            }),
            parameters={
                'versions': '',
            },
            bucket=request.bucket,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListObjectVersionsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
            serde_utils.deserialize_encode_type
        ],
    )
