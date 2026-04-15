# -*- coding: utf-8 -*-
"""Namespace models for tables operations."""

from typing import Optional, List, Any
from ... import serde
from .common import NamespaceSummary


class CreateNamespaceRequest(serde.RequestModel):
    """The request for the CreateNamespace operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "body", "rename": "namespace", "type": "[str]"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (List[str], optional): The namespace to create.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace


class CreateNamespaceResult(serde.ResultModel):
    """The result for the CreateNamespace operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "output", "position": "body", "rename": "tableBucketARN"},
        "namespace": {"tag": "output", "position": "body", "rename": "namespace", "type": "[str]"},
    }

    def __init__(
        self, 
        table_bucket_arn: str = None,
        namespace: List[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace


class DeleteNamespaceRequest(serde.RequestModel):
    """The request for the DeleteNamespace operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace to delete.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace


class DeleteNamespaceResult(serde.ResultModel):
    """The result for the DeleteNamespace operation."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class GetNamespaceRequest(serde.RequestModel):
    """The request for the GetNamespace operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "namespace": {"tag": "input", "position": "path", "rename": "namespace", "required": True},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        namespace: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            namespace (str, required): The namespace to get.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.namespace = namespace


class GetNamespaceResult(serde.ResultModel):
    """The result for the GetNamespace operation."""

    _attribute_map = {
        "namespace": {"tag": "output", "position": "body", "rename": "namespace", "type": "[str]"},
        "namespace_id": {"tag": "output", "position": "body", "rename": "namespaceId", "type": "str"},
        "table_bucket_id": {"tag": "output", "position": "body", "rename": "tableBucketId", "type": "str"},
        "owner_account_id": {"tag": "output", "position": "body", "rename": "ownerAccountId", "type": "str"},
        "created_at": {"tag": "output", "position": "body", "rename": "createdAt", "type": "str"},
        "created_by": {"tag": "output", "position": "body", "rename": "createdBy", "type": "str"},
    }

    def __init__(
        self,
        namespace: Optional[List[str]] = None,
        namespace_id: Optional[str] = None,
        table_bucket_id: Optional[str] = None,
        owner_account_id: Optional[str] = None,
        created_at: Optional[str] = None,
        created_by: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            namespace (List[str], optional): The namespace path.
            namespace_id (str, optional): The namespace ID.
            table_bucket_id (str, optional): The bucket ID.
            owner_account_id (str, optional): The owner account ID.
            created_at (datetime, optional): The creation time.
            created_by (str, optional): The creator.
        """
        super().__init__(**kwargs)
        self.namespace = namespace
        self.namespace_id = namespace_id
        self.table_bucket_id = table_bucket_id
        self.owner_account_id = owner_account_id
        self.created_at = created_at
        self.created_by = created_by


class ListNamespacesRequest(serde.RequestModel):
    """The request for the ListNamespaces operation."""

    _attribute_map = {
        "table_bucket_arn": {"tag": "input", "position": "host", "required": True},
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
        "continuation_token": {"tag": "input", "position": "query", "rename": "continuationToken"},
        "max_namespaces": {"tag": "input", "position": "query", "rename": "maxNamespaces"},
    }

    def __init__(
        self,
        table_bucket_arn: str = None,
        prefix: Optional[str] = None,
        continuation_token: Optional[str] = None,
        max_namespaces: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            table_bucket_arn (str, required): The ARN of the table bucket.
            prefix (str, optional): The prefix to filter namespaces.
            continuation_token (str, optional): The continuation token.
            max_namespaces (int, optional): The maximum number of namespaces.
        """
        super().__init__(**kwargs)
        self.table_bucket_arn = table_bucket_arn
        self.prefix = prefix
        self.continuation_token = continuation_token
        self.max_namespaces = max_namespaces


class ListNamespacesResult(serde.ResultModel):
    """The result for the ListNamespaces operation."""

    _attribute_map = {
        "namespaces": {"tag": "output", "position": "body", "rename": "namespaces", "type": "[NamespaceSummary]"},
        "continuation_token": {"tag": "output", "position": "body", "rename": "continuationToken"},
    }

    _dependency_map = {
        "NamespaceSummary": {"new": lambda: NamespaceSummary()},
    }

    def __init__(
        self,
        namespaces: Optional[List[NamespaceSummary]] = None,
        continuation_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            namespaces (List[NamespaceSummary], optional): The list of namespace summaries.
            continuation_token (str, optional): The continuation token.
        """
        super().__init__(**kwargs)
        self.namespaces = namespaces
        self.continuation_token = continuation_token
