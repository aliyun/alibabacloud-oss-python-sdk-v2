# pylint: disable=line-too-long
from .._client import _SyncClientImpl
from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models



def put_vector_bucket(client: _SyncClientImpl, request: models.PutBucketRequest, **kwargs) -> models.PutBucketResult:
    """
    put bucket synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketRequest): The request for the PutBucket operation.

    Returns:
        PutBucketResult: The result for the PutBucket operation.
    """

    op_input = serde.serialize_inputs_json(
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

def get_vector_bucket(client: _SyncClientImpl, request: models.GetBucketInfoRequest, **kwargs) -> models.GetBucketInfoResult:
    """
    GetBucketInfo Queries information about a bucket.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketInfoRequest): The request for the GetBucketInfo operation.

    Returns:
        GetBucketInfoResult: The result for the GetBucketInfo operation.
    """

    op_input = serde.serialize_inputs_json(
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


def delete_vector_bucket(client: _SyncClientImpl, request: models.DeleteBucketRequest, **kwargs) -> models.DeleteBucketResult:
    """
    delete bucket synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketRequest): The request for the DeleteBucket operation.

    Returns:
        DeleteBucketResult: The result for the DeleteBucket operation.
    """

    op_input = serde.serialize_inputs_json(
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


def list_vector_buckets(client: _SyncClientImpl, request: models.ListBucketsRequest, **kwargs) -> models.ListBucketsResult:
    """
    list buckets synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (ListBucketsRequest): The request for the ListBuckets operation.

    Returns:
        ListBucketsResult: The result for the ListBuckets operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='ListBuckets',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/octet-stream',
            }),
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.ListBucketsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody,
        ],
    )



def put_bucket_policy_vector(client: _SyncClientImpl, request: models.PutBucketPolicyRequest, **kwargs) -> models.PutBucketPolicyResult:
    """
    put_bucket_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketPolicyRequest): The request for the PutBucketPolicy operation.

    Returns:
        PutBucketPolicyResult: The result for the PutBucketPolicy operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketPolicy',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'policy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['policy']},
        )
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketPolicyResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_policy_vector(client: _SyncClientImpl, request: models.GetBucketPolicyRequest, **kwargs) -> models.GetBucketPolicyResult:
    """
    get_bucket_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketPolicyRequest): The request for the GetBucketPolicy operation.

    Returns:
        GetBucketPolicyResult: The result for the GetBucketPolicy operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketPolicy',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'policy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['policy']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketPolicyResult(
            body=op_output.http_response.content.decode()
        ),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_policy_vector(client: _SyncClientImpl, request: models.DeleteBucketPolicyRequest, **kwargs) -> models.DeleteBucketPolicyResult:
    """
    delete_bucket_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketPolicyRequest): The request for the DeleteBucketPolicy operation.

    Returns:
        DeleteBucketPolicyResult: The result for the DeleteBucketPolicy operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketPolicy',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'policy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['policy']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketPolicyResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )





def put_public_access_block_vector(client: _SyncClientImpl, request: models.PutPublicAccessBlockRequest, **kwargs) -> models.PutPublicAccessBlockResult:
    """
    put_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutPublicAccessBlockRequest): The request for the PutPublicAccessBlock operation.

    Returns:
        PutPublicAccessBlockResult: The result for the PutPublicAccessBlock operation.
    """

    op_input = serde.serialize_inputs_jsons_json(
        request=request,
        op_input=OperationInput(
            op_name='PutPublicAccessBlock',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'publicAccessBlock': '', 
            },
            op_metadata={'sub-resource': ['publicAccessBlock']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_public_access_block_vector(client: _SyncClientImpl, request: models.GetPublicAccessBlockRequest, **kwargs) -> models.GetPublicAccessBlockResult:
    """
    get_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetPublicAccessBlockRequest): The request for the GetPublicAccessBlock operation.

    Returns:
        GetPublicAccessBlockResult: The result for the GetPublicAccessBlock operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='GetPublicAccessBlock',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'publicAccessBlock': '',
            },
            op_metadata={'sub-resource': ['publicAccessBlock']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetPublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def delete_public_access_block_vector(client: _SyncClientImpl, request: models.DeletePublicAccessBlockRequest, **kwargs) -> models.DeletePublicAccessBlockResult:
    """
    delete_public_access_block synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeletePublicAccessBlockRequest): The request for the DeletePublicAccessBlock operation.

    Returns:
        DeletePublicAccessBlockResult: The result for the DeletePublicAccessBlock operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='DeletePublicAccessBlock',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'publicAccessBlock': '', 
            },
            op_metadata={'sub-resource': ['publicAccessBlock']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeletePublicAccessBlockResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def put_bucket_tags_vector(client: _SyncClientImpl, request: models.PutBucketTagsRequest, **kwargs) -> models.PutBucketTagsResult:
    """
    put_bucket_tags synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketTagsRequest): The request for the PutBucketTags operation.

    Returns:
        PutBucketTagsResult: The result for the PutBucketTags operation.
    """

    op_input = serde.serialize_inputs_jsons_json(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketTags',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'tagging': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['tagging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketTagsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_tags_vector(client: _SyncClientImpl, request: models.GetBucketTagsRequest, **kwargs) -> models.GetBucketTagsResult:
    """
    get_bucket_tags synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketTagsRequest): The request for the GetBucketTags operation.

    Returns:
        GetBucketTagsResult: The result for the GetBucketTags operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketTags',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'tagging': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['tagging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketTagsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_tags_vector(client: _SyncClientImpl, request: models.DeleteBucketTagsRequest, **kwargs) -> models.DeleteBucketTagsResult:
    """
    delete_bucket_tags synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketTagsRequest): The request for the DeleteBucketTags operation.

    Returns:
        DeleteBucketTagsResult: The result for the DeleteBucketTags operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketTags',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'tagging': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['tagging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketTagsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def get_bucket_resource_group_vector(client: _SyncClientImpl, request: models.GetBucketResourceGroupRequest, **kwargs) -> models.GetBucketResourceGroupResult:
    """
    get_bucket_resource_group synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketResourceGroupRequest): The request for the GetBucketResourceGroup operation.

    Returns:
        GetBucketResourceGroupResult: The result for the GetBucketResourceGroup operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketResourceGroup',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'resourceGroup': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['resourceGroup']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketResourceGroupResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_bucket_resource_group_vector(client: _SyncClientImpl, request: models.PutBucketResourceGroupRequest, **kwargs) -> models.PutBucketResourceGroupResult:
    """
    put_bucket_resource_group synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketResourceGroupRequest): The request for the PutBucketResourceGroup operation.

    Returns:
        PutBucketResourceGroupResult: The result for the PutBucketResourceGroup operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketResourceGroup',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'resourceGroup': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['resourceGroup']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketResourceGroupResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


def put_bucket_policy_vector(client: _SyncClientImpl, request: models.PutBucketPolicyRequest, **kwargs) -> models.PutBucketPolicyResult:
    """
    put_bucket_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketPolicyRequest): The request for the PutBucketPolicy operation.

    Returns:
        PutBucketPolicyResult: The result for the PutBucketPolicy operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketPolicy',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'policy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['policy']},
        )
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketPolicyResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_policy_vector(client: _SyncClientImpl, request: models.GetBucketPolicyRequest, **kwargs) -> models.GetBucketPolicyResult:
    """
    get_bucket_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketPolicyRequest): The request for the GetBucketPolicy operation.

    Returns:
        GetBucketPolicyResult: The result for the GetBucketPolicy operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketPolicy',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'policy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['policy']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketPolicyResult(
            body=op_output.http_response.content.decode()
        ),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_policy_vector(client: _SyncClientImpl, request: models.DeleteBucketPolicyRequest, **kwargs) -> models.DeleteBucketPolicyResult:
    """
    delete_bucket_policy synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketPolicyRequest): The request for the DeleteBucketPolicy operation.

    Returns:
        DeleteBucketPolicyResult: The result for the DeleteBucketPolicy operation.
    """

    op_input = serde.serialize_inputs_json(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketPolicy',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'policy': '',
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['policy']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketPolicyResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )


