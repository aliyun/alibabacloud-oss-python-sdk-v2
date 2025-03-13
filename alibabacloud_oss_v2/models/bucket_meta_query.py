import datetime
from typing import Optional, List, Any, Union
from enum import Enum
from .. import serde


class MetaQueryOrderType(str, Enum):
    """
    A short description of struct
    """

    ASC = 'asc'
    DESC = 'desc'


class MetaQueryStatus(serde.Model):
    """
    The container that stores the metadata information.
    """

    _attribute_map = { 
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'update_time': {'tag': 'xml', 'rename': 'UpdateTime', 'type': 'str'},
        'state': {'tag': 'xml', 'rename': 'State', 'type': 'str'},
        'phase': {'tag': 'xml', 'rename': 'Phase', 'type': 'str'},
        'meta_query_mode': {'tag': 'xml', 'rename': 'MetaQueryMode', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MetaQueryStatus'
    }

    def __init__(
        self,
        create_time: Optional[str] = None,
        update_time: Optional[str] = None,
        state: Optional[str] = None,
        phase: Optional[str] = None,
        meta_query_mode: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            create_time (str, optional): The time when the metadata index library was created. The value follows the RFC 3339 standard in the YYYY-MM-DDTHH:mm:ss+TIMEZONE format. YYYY-MM-DD indicates the year, month, and day. T indicates the beginning of the time element. HH:mm:ss indicates the hour, minute, and second. TIMEZONE indicates the time zone.
            update_time (str, optional): The time when the metadata index library was updated. The value follows the RFC 3339 standard in the YYYY-MM-DDTHH:mm:ss+TIMEZONE format. YYYY-MM-DD indicates the year, month, and day. T indicates the beginning of the time element. HH:mm:ss indicates the hour, minute, and second. TIMEZONE indicates the time zone.
            state (str, optional): The status of the metadata index library. Valid values:- Ready: The metadata index library is being prepared after it is created.In this case, the metadata index library cannot be used to query data.- Stop: The metadata index library is paused.- Running: The metadata index library is running.- Retrying: The metadata index library failed to be created and is being created again.- Failed: The metadata index library failed to be created.- Deleted: The metadata index library is deleted.
            phase (str, optional): The scan type. Valid values:- FullScanning: Full scanning is in progress.- IncrementalScanning: Incremental scanning is in progress.
            meta_query_mode (str, optional): Retrieval modes: basic: Scalar search, semantic: Vector search.
        """
        super().__init__(**kwargs)
        self.create_time = create_time
        self.update_time = update_time
        self.state = state
        self.phase = phase
        self.meta_query_mode = meta_query_mode


class MetaQueryAggregation(serde.Model):
    """
    The container that stores the information about a single aggregate operation.
    """

    _attribute_map = { 
        'field': {'tag': 'xml', 'rename': 'Field', 'type': 'str'},
        'operation': {'tag': 'xml', 'rename': 'Operation', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Aggregation'
    }

    def __init__(
        self,
        field: Optional[str] = None,
        operation: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            field (str, optional):
            operation (str, optional):
        """
        super().__init__(**kwargs)
        self.field = field
        self.operation = operation


class MetaQueryTagging(serde.Model):
    """
    The container that stores the tag information.
    """

    _attribute_map = { 
        'key': {'tag': 'xml', 'rename': 'Key', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MetaQueryTagging'
    }

    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The tag key.
            value (str, optional): The tag value.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value


class MetaQueryUserMeta(serde.Model):
    """
    The container that stores user metadata.
    """

    _attribute_map = { 
        'key': {'tag': 'xml', 'rename': 'Key', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
    }

    _xml_map = {
        'name': 'UserMeta'
    }

    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The key of the user metadata item.
            value (str, optional): The value of the user metadata item.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value


class MetaQueryOSSTagging(serde.Model):
    """
    The tags.
    """

    _attribute_map = { 
        'taggings': {'tag': 'xml', 'rename': 'Tagging', 'type': '[MetaQueryTagging]'},
    }

    _xml_map = {
        'name': 'OSSTagging'
    }

    _dependency_map = { 
        'MetaQueryTagging': {'new': lambda: MetaQueryTagging()},
    }

    def __init__(
        self,
        taggings: Optional[List[MetaQueryTagging]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            taggings (List[MetaQueryTagging], optional): The tags.
        """
        super().__init__(**kwargs)
        self.taggings = taggings


class MetaQueryAggregations(serde.Model):
    """
    The container that stores the information about aggregate operations.
    """

    _attribute_map = { 
        'aggregations': {'tag': 'xml', 'rename': 'Aggregation', 'type': '[Aggregation]'},
    }

    _xml_map = {
        'name': 'Aggregations'
    }

    _dependency_map = { 
        'Aggregation': {'new': lambda: MetaQueryAggregation()},
    }

    def __init__(
        self,
        aggregations: Optional[List[MetaQueryAggregation]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            aggregations (List[Aggregation], optional): The container that stores the information about aggregate operations.
        """
        super().__init__(**kwargs)
        self.aggregations = aggregations


class MetaQuery(serde.Model):
    """
    The container that stores the query conditions.
    """

    _attribute_map = { 
        'aggregations': {'tag': 'xml', 'rename': 'Aggregations', 'type': 'Aggregations'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
        'max_results': {'tag': 'xml', 'rename': 'MaxResults', 'type': 'int'},
        'query': {'tag': 'xml', 'rename': 'Query', 'type': 'str'},
        'sort': {'tag': 'xml', 'rename': 'Sort', 'type': 'str'},
        'order': {'tag': 'xml', 'rename': 'Order', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MetaQuery'
    }

    _dependency_map = { 
        'Aggregations': {'new': lambda: MetaQueryAggregations()},
    }

    def __init__(
        self,
        aggregations: Optional[MetaQueryAggregations] = None,
        next_token: Optional[str] = None,
        max_results: Optional[int] = None,
        query: Optional[str] = None,
        sort: Optional[str] = None,
        order: Optional[Union[str, MetaQueryOrderType]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            aggregations (Aggregations, optional): The container that stores the information about aggregate operations.
            next_token (str, optional): The pagination token used to obtain information in the next request. The object information is returned in alphabetical order starting from the value of NextToken.
            max_results (int, optional): The maximum number of objects to return. Valid values: 0 to 100. If this parameter is not set or is set to 0, up to 100 objects are returned.
            query (str, optional): The query conditions. A query condition includes the following elements:*   Operation: the operator. Valid values: eq (equal to), gt (greater than), gte (greater than or equal to), lt (less than), lte (less than or equal to), match (fuzzy query), prefix (prefix query), and (AND), or (OR), and not (NOT).*   Field: the field name.*   Value: the field value.*   SubQueries: the subquery conditions. Options that are included in this element are the same as those of simple query. You need to set subquery conditions only when Operation is set to and, or, or not.
            sort (str, optional): The field based on which the results are sorted.
            order (str | MetaQueryOrderType, optional): The sort order.
        """
        super().__init__(**kwargs)
        self.aggregations = aggregations
        self.next_token = next_token
        self.max_results = max_results
        self.query = query
        self.sort = sort
        self.order = order


class MetaQueryOSSUserMeta(serde.Model):
    """
    The user metadata items.
    """

    _attribute_map = { 
        'user_metas': {'tag': 'xml', 'rename': 'UserMeta', 'type': '[UserMeta]'},
    }

    _xml_map = {
        'name': 'OSSUserMeta'
    }

    _dependency_map = { 
        'UserMeta': {'new': lambda: MetaQueryUserMeta()},
    }

    def __init__(
        self,
        user_metas: Optional[List[MetaQueryUserMeta]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            user_metas (List[UserMeta], optional): The user metadata items.
        """
        super().__init__(**kwargs)
        self.user_metas = user_metas


class MetaQueryFile(serde.Model):
    """
    File information.
    """

    _attribute_map = { 
        'file_modified_time': {'tag': 'xml', 'rename': 'FileModifiedTime', 'type': 'str'},
        'etag': {'tag': 'xml', 'rename': 'ETag', 'type': 'str'},
        'server_side_encryption': {'tag': 'xml', 'rename': 'ServerSideEncryption', 'type': 'str'},
        'oss_tagging_count': {'tag': 'xml', 'rename': 'OSSTaggingCount', 'type': 'int'},
        'oss_tagging': {'tag': 'xml', 'rename': 'OSSTagging', 'type': 'OSSTagging'},
        'oss_user_meta': {'tag': 'xml', 'rename': 'OSSUserMeta', 'type': 'OSSUserMeta'},
        'filename': {'tag': 'xml', 'rename': 'Filename', 'type': 'str'},
        'size': {'tag': 'xml', 'rename': 'Size', 'type': 'int'},
        'oss_object_type': {'tag': 'xml', 'rename': 'OSSObjectType', 'type': 'str'},
        'oss_storage_class': {'tag': 'xml', 'rename': 'OSSStorageClass', 'type': 'str'},
        'object_acl': {'tag': 'xml', 'rename': 'ObjectACL', 'type': 'str'},
        'oss_crc64': {'tag': 'xml', 'rename': 'OSSCRC64', 'type': 'str'},
        'server_side_encryption_customer_algorithm': {'tag': 'xml', 'rename': 'ServerSideEncryptionCustomerAlgorithm', 'type': 'str'},
    }

    _xml_map = {
        'name': 'File'
    }

    _dependency_map = { 
        'OSSTagging': {'new': lambda: MetaQueryOSSTagging()},
        'OSSUserMeta': {'new': lambda: MetaQueryOSSUserMeta()},
    }

    def __init__(
        self,
        file_modified_time: Optional[str] = None,
        etag: Optional[str] = None,
        server_side_encryption: Optional[str] = None,
        oss_tagging_count: Optional[int] = None,
        oss_tagging: Optional[MetaQueryOSSTagging] = None,
        oss_user_meta: Optional[MetaQueryOSSUserMeta] = None,
        filename: Optional[str] = None,
        size: Optional[int] = None,
        oss_object_type: Optional[str] = None,
        oss_storage_class: Optional[str] = None,
        object_acl: Optional[str] = None,
        oss_crc64: Optional[str] = None,
        server_side_encryption_customer_algorithm: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            file_modified_time (str, optional): The time when the object was last modified.
            etag (str, optional): The ETag of the object.
            server_side_encryption (str, optional): The server-side encryption algorithm used when the object was created.
            oss_tagging_count (int, optional): The number of the tags of the object.
            oss_tagging (OSSTagging, optional): The tags.
            oss_user_meta (OSSUserMeta, optional): The user metadata items.
            filename (str, optional): The full path of the object.
            size (int, optional): The object size.
            oss_object_type (str, optional): The type of the object.Valid values:
                Multipart: The object is uploaded by using multipart upload.
                Symlink: The object is a symbolic link that was created by calling the PutSymlink operation.
                Appendable: The object is uploaded by using AppendObject.
                Normal: The object is uploaded by using PutObject.
            oss_storage_class (str, optional): The storage class of the object.Valid values:
                Archive: the Archive storage class.
                ColdArchive: the Cold Archive storage class.
                IA: the Infrequent Access (IA) storage class.
                Standard: The Standard storage class
            object_acl (str, optional): The access control list (ACL) of the object.Valid values:
                default: the ACL of the bucket.
                private: private.
                public-read: public-read.
                public-read-write: public-read-write.
            oss_crc64 (str, optional): The CRC-64 value of the object.
            server_side_encryption_customer_algorithm (str, optional): The server-side encryption of the object.
        """
        super().__init__(**kwargs)
        self.file_modified_time = file_modified_time
        self.etag = etag
        self.server_side_encryption = server_side_encryption
        self.oss_tagging_count = oss_tagging_count
        self.oss_tagging = oss_tagging
        self.oss_user_meta = oss_user_meta
        self.filename = filename
        self.size = size
        self.oss_object_type = oss_object_type
        self.oss_storage_class = oss_storage_class
        self.object_acl = object_acl
        self.oss_crc64 = oss_crc64
        self.server_side_encryption_customer_algorithm = server_side_encryption_customer_algorithm


class MetaQueryFiles(serde.Model):
    """
    The list of file information.
    """

    _attribute_map = { 
        'file': {'tag': 'xml', 'rename': 'File', 'type': 'File'},
    }

    _xml_map = {
        'name': 'Files'
    }

    _dependency_map = { 
        'File': {'new': lambda: MetaQueryFile()},
    }

    def __init__(
        self,
        file: Optional[MetaQueryFile] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            file (File, optional):
        """
        super().__init__(**kwargs)
        self.file = file




class OpenMetaQueryRequest(serde.RequestModel):
    """
    The request for the OpenMetaQuery operation.
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


class OpenMetaQueryResult(serde.ResultModel):
    """
    The request for the OpenMetaQuery operation.
    """


class GetMetaQueryStatusRequest(serde.RequestModel):
    """
    The request for the GetMetaQueryStatus operation.
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


class GetMetaQueryStatusResult(serde.ResultModel):
    """
    The request for the GetMetaQueryStatus operation.
    """

    _attribute_map = { 
        'meta_query_status': {'tag': 'output', 'position': 'body', 'rename': 'MetaQueryStatus', 'type': 'MetaQueryStatus,xml'},
    }

    _dependency_map = { 
        'MetaQueryStatus': {'new': lambda: MetaQueryStatus()},
    }

    def __init__(
        self,
        meta_query_status: Optional[MetaQueryStatus] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            meta_query_status (MetaQueryStatus, optional): The container that stores the metadata information.
        """
        super().__init__(**kwargs)
        self.meta_query_status = meta_query_status



class DoMetaQueryRequest(serde.RequestModel):
    """
    The request for the DoMetaQuery operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'meta_query': {'tag': 'input', 'position': 'body', 'rename': 'MetaQuery', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        meta_query: Optional[MetaQuery] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            meta_query (MetaQuery, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.meta_query = meta_query


class DoMetaQueryResult(serde.ResultModel):
    """
    The request for the DoMetaQuery operation.
    """

    _attribute_map = {
        'files': {'tag': 'xml', 'rename': 'Files', 'type': 'Files,xml'},
        'aggregations': {'tag': 'xml', 'rename': 'Aggregations', 'type': 'Aggregations,xml'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str,xml'},
    }

    _dependency_map = {
        'Files': {'new': lambda: MetaQueryFiles()},
        'Aggregations': {'new': lambda: MetaQueryAggregations()},
    }

    def __init__(
        self,
        files: Optional[MetaQueryFiles] = None,
        aggregations: Optional[MetaQueryAggregations] = None,
        next_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            files (Files, optional): The list of file information.
            aggregations (Aggregations, optional): The list of file information.
            next_token (str, optional): The token that is used for the next query when the total number of objects exceeds the value of MaxResults.The value of NextToken is used to return the unreturned results in the next query.This parameter has a value only when not all objects are returned.
        """
        super().__init__(**kwargs)
        self.files = files
        self.aggregations = aggregations
        self.next_token = next_token


class CloseMetaQueryRequest(serde.RequestModel):
    """
    The request for the CloseMetaQuery operation.
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


class CloseMetaQueryResult(serde.ResultModel):
    """
    The request for the CloseMetaQuery operation.
    """
