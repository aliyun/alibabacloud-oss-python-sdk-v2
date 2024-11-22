# pylint: disable=line-too-long

from ..types import OperationInput, CaseInsensitiveDict
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl


def put_bucket_logging(client: _SyncClientImpl, request: models.PutBucketLoggingRequest, **kwargs) -> models.PutBucketLoggingResult:
    """
    put_bucket_logging synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutBucketLoggingRequest): The request for the PutBucketLogging operation.

    Returns:
        PutBucketLoggingResult: The result for the PutBucketLogging operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketLogging',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'logging': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['logging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutBucketLoggingResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_bucket_logging(client: _SyncClientImpl, request: models.GetBucketLoggingRequest, **kwargs) -> models.GetBucketLoggingResult:
    """
    get_bucket_logging synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetBucketLoggingRequest): The request for the GetBucketLogging operation.

    Returns:
        GetBucketLoggingResult: The result for the GetBucketLogging operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketLogging',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'logging': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['logging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetBucketLoggingResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_bucket_logging(client: _SyncClientImpl, request: models.DeleteBucketLoggingRequest, **kwargs) -> models.DeleteBucketLoggingResult:
    """
    delete_bucket_logging synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteBucketLoggingRequest): The request for the DeleteBucketLogging operation.

    Returns:
        DeleteBucketLoggingResult: The result for the DeleteBucketLogging operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketLogging',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'logging': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['logging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteBucketLoggingResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def put_user_defined_log_fields_config(client: _SyncClientImpl, request: models.PutUserDefinedLogFieldsConfigRequest, **kwargs) -> models.PutUserDefinedLogFieldsConfigResult:
    """
    put_user_defined_log_fields_config synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (PutUserDefinedLogFieldsConfigRequest): The request for the PutUserDefinedLogFieldsConfig operation.

    Returns:
        PutUserDefinedLogFieldsConfigResult: The result for the PutUserDefinedLogFieldsConfig operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutUserDefinedLogFieldsConfig',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'userDefinedLogFieldsConfig': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['userDefinedLogFieldsConfig']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.PutUserDefinedLogFieldsConfigResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def get_user_defined_log_fields_config(client: _SyncClientImpl, request: models.GetUserDefinedLogFieldsConfigRequest, **kwargs) -> models.GetUserDefinedLogFieldsConfigResult:
    """
    get_user_defined_log_fields_config synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (GetUserDefinedLogFieldsConfigRequest): The request for the GetUserDefinedLogFieldsConfig operation.

    Returns:
        GetUserDefinedLogFieldsConfigResult: The result for the GetUserDefinedLogFieldsConfig operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetUserDefinedLogFieldsConfig',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'userDefinedLogFieldsConfig': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['userDefinedLogFieldsConfig']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.GetUserDefinedLogFieldsConfigResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

def delete_user_defined_log_fields_config(client: _SyncClientImpl, request: models.DeleteUserDefinedLogFieldsConfigRequest, **kwargs) -> models.DeleteUserDefinedLogFieldsConfigResult:
    """
    delete_user_defined_log_fields_config synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (DeleteUserDefinedLogFieldsConfigRequest): The request for the DeleteUserDefinedLogFieldsConfig operation.

    Returns:
        DeleteUserDefinedLogFieldsConfigResult: The result for the DeleteUserDefinedLogFieldsConfig operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteUserDefinedLogFieldsConfig',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={ 
                'userDefinedLogFieldsConfig': '', 
            },
            bucket=request.bucket,
            op_metadata={'sub-resource': ['userDefinedLogFieldsConfig']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    return serde.deserialize_output(
        result=models.DeleteUserDefinedLogFieldsConfigResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )
