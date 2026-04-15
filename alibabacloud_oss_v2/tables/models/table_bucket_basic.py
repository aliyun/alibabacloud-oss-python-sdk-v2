# -*- coding: utf-8 -*-
"""Table Bucket models for tables operations."""

import datetime
from typing import Optional, List, Any, Dict
from ... import serde
from .common import TableBucketSummary, EncryptionConfiguration


class CreateTableBucketRequest(serde.RequestModel):
    """The request for the CreateTableBucket operation."""

    _attribute_map = {
        "name": {"tag": "input", "position": "body", "rename": "name"},
        "encryption_configuration": {"tag": "input", "position": "body", "rename": "encryptionConfiguration", "type": "EncryptionConfiguration"},
    }

    _dependency_map = {
        "EncryptionConfiguration": {"new": lambda: EncryptionConfiguration()},
    }

    def __init__(
        self,
        name: Optional[str] = None,
        encryption_configuration: Optional[EncryptionConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            name (str, optional): The name of the table bucket.
            encryption_configuration (EncryptionConfiguration, optional): The encryption configuration.
        """
        super().__init__(**kwargs)
        self.name = name
        self.encryption_configuration = encryption_configuration


class CreateTableBucketResult(serde.ResultModel):
    """The result for the CreateTableBucket operation."""

    _attribute_map = {
        "arn": {"tag": "output", "position": "body", "rename": "arn"},
    }

    def __init__(
        self,
        arn: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            arn (str, optional): The ARN of the created table bucket.
        """
        super().__init__(**kwargs)
        self.arn = arn


class DeleteTableBucketRequest(serde.RequestModel):
    """The request for the DeleteTableBucket operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn


class DeleteTableBucketResult(serde.ResultModel):
    """The result for the DeleteTableBucket operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GetTableBucketRequest(serde.RequestModel):
    """The request for the GetTableBucket operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn


class GetTableBucketResult(serde.ResultModel):
    """The result for the GetTableBucket operation."""

    _attribute_map = {
        "arn": {"tag": "output", "position": "body", "rename": "arn"},
        "name": {"tag": "output", "position": "body", "rename": "name"},
        "owner_account_id": {"tag": "output", "position": "body", "rename": "ownerAccountId"},
        "created_at": {"tag": "output", "position": "body", "rename": "createdAt"},
        "table_bucket_id": {"tag": "output", "position": "body", "rename": "tableBucketId"},
        "type": {"tag": "output", "position": "body", "rename": "type"},
    }

    def __init__(
        self,
        arn: Optional[str] = None,
        name: Optional[str] = None,
        owner_account_id: Optional[str] = None,
        created_at: Optional[str] = None,
        table_bucket_id: Optional[str] = None,
        type: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            arn (str, optional): The ARN of the table bucket.
            name (str, optional): The name of the table bucket.
            owner_account_id (str, optional): The owner account ID.
            created_at (str, optional): The creation time.
            table_bucket_id (str, optional): The table bucket ID.
            type (str, optional): The type of the table bucket.
        """
        super().__init__(**kwargs)
        self.arn = arn
        self.name = name
        self.owner_account_id = owner_account_id
        self.created_at = created_at
        self.table_bucket_id = table_bucket_id
        self.type = type


class ListTableBucketsRequest(serde.RequestModel):
    """The request for the ListTableBuckets operation."""

    _attribute_map = {
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
        "continuation_token": {"tag": "input", "position": "query", "rename": "continuationToken"},
        "max_buckets": {"tag": "input", "position": "query", "rename": "maxBuckets"},
    }

    def __init__(
        self,
        prefix: Optional[str] = None,
        continuation_token: Optional[str] = None,
        max_buckets: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            prefix (str, optional): The prefix to filter table buckets.
            continuation_token (str, optional): The continuation token.
            max_buckets (int, optional): The maximum number of table buckets.
        """
        super().__init__(**kwargs)
        self.prefix = prefix
        self.continuation_token = continuation_token
        self.max_buckets = max_buckets


class ListTableBucketsResult(serde.ResultModel):
    """The result for the ListTableBuckets operation."""

    _attribute_map = {
        "table_buckets": {"tag": "output", "position": "body", "rename": "tableBuckets", "type": "[TableBucketSummary]"},
        "continuation_token": {"tag": "output", "position": "body", "rename": "continuationToken"},
    }

    _dependency_map = {
        "TableBucketSummary": {"new": lambda: TableBucketSummary()},
    }

    def __init__(
        self,
        table_buckets: Optional[List[TableBucketSummary]] = None,
        continuation_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_buckets (List[TableBucketSummary], optional): The list of table bucket summaries.
            continuation_token (str, optional): The continuation token.
        """
        super().__init__(**kwargs)
        self.table_buckets = table_buckets
        self.continuation_token = continuation_token
