from typing import Optional, Any
from .. import serde


class ApplyServerSideEncryptionByDefault(serde.Model):
    """
    The container that stores the default server-side encryption method.
    """

    _attribute_map = { 
        'kms_master_key_id': {'tag': 'xml', 'rename': 'KMSMasterKeyID', 'type': 'str'},
        'kms_data_encryption': {'tag': 'xml', 'rename': 'KMSDataEncryption', 'type': 'str'},
        'sse_algorithm': {'tag': 'xml', 'rename': 'SSEAlgorithm', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ApplyServerSideEncryptionByDefault'
    }

    def __init__(
        self,
        kms_master_key_id: Optional[str] = None,
        kms_data_encryption: Optional[str] = None,
        sse_algorithm: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            kms_master_key_id (str, optional): The CMK ID that is specified when SSEAlgorithm is set to KMS and a specified CMK is used for encryption. In other cases, leave this parameter empty.
            kms_data_encryption (str, optional): The algorithm that is used to encrypt objects. If this parameter is not specified, objects are encrypted by using AES256. This parameter is valid only when SSEAlgorithm is set to KMS. Valid value: SM4.
            sse_algorithm (str, optional): The default server-side encryption method. Valid values: KMS, AES256, and SM4. You are charged when you call API operations to encrypt or decrypt data by using CMKs managed by KMS. For more information, see [Billing of KMS](~~52608~~). If the default server-side encryption method is configured for the destination bucket and ReplicaCMKID is configured in the CRR rule:*   If objects in the source bucket are not encrypted, they are encrypted by using the default encryption method of the destination bucket after they are replicated.*   If objects in the source bucket are encrypted by using SSE-KMS or SSE-OSS, they are encrypted by using the same method after they are replicated.For more information, see [Use data replication with server-side encryption](~~177216~~).
        """
        super().__init__(**kwargs)
        self.kms_master_key_id = kms_master_key_id
        self.kms_data_encryption = kms_data_encryption
        self.sse_algorithm = sse_algorithm


class ServerSideEncryptionRule(serde.Model):
    """
    The container that stores server-side encryption rules.
    """

    _attribute_map = { 
        'apply_server_side_encryption_by_default': {'tag': 'xml', 'rename': 'ApplyServerSideEncryptionByDefault', 'type': 'ApplyServerSideEncryptionByDefault'},
    }

    _xml_map = {
        'name': 'ServerSideEncryptionRule'
    }

    _dependency_map = { 
        'ApplyServerSideEncryptionByDefault': {'new': lambda: ApplyServerSideEncryptionByDefault()},
    }

    def __init__(
        self,
        apply_server_side_encryption_by_default: Optional[ApplyServerSideEncryptionByDefault] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            apply_server_side_encryption_by_default (ApplyServerSideEncryptionByDefault, optional): The container that stores the default server-side encryption method.
        """
        super().__init__(**kwargs)
        self.apply_server_side_encryption_by_default = apply_server_side_encryption_by_default




class PutBucketEncryptionRequest(serde.RequestModel):
    """
    The request for the PutBucketEncryption operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'server_side_encryption_rule': {'tag': 'input', 'position': 'body', 'rename': 'ServerSideEncryptionRule', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        server_side_encryption_rule: Optional[ServerSideEncryptionRule] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            server_side_encryption_rule (ServerSideEncryptionRule, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.server_side_encryption_rule = server_side_encryption_rule


class PutBucketEncryptionResult(serde.ResultModel):
    """
    The request for the PutBucketEncryption operation.
    """

class GetBucketEncryptionRequest(serde.RequestModel):
    """
    The request for the GetBucketEncryption operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetBucketEncryptionResult(serde.ResultModel):
    """
    The request for the GetBucketEncryption operation.
    """

    _attribute_map = { 
        'server_side_encryption_rule': {'tag': 'output', 'position': 'body', 'rename': 'ServerSideEncryptionRule', 'type': 'ServerSideEncryptionRule,xml'},
    }

    _dependency_map = { 
        'ServerSideEncryptionRule': {'new': lambda: ServerSideEncryptionRule()},
    }

    def __init__(
        self,
        server_side_encryption_rule: Optional[ServerSideEncryptionRule] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            server_side_encryption_rule (ServerSideEncryptionRule, optional): The container that stores server-side encryption rules.
        """
        super().__init__(**kwargs)
        self.server_side_encryption_rule = server_side_encryption_rule

class DeleteBucketEncryptionRequest(serde.RequestModel):
    """
    The request for the DeleteBucketEncryption operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteBucketEncryptionResult(serde.ResultModel):
    """
    The request for the DeleteBucketEncryption operation.
    """
