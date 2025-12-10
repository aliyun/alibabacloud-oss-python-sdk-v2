"""Models for object operation APIs"""
# pylint: disable=too-few-public-methods, too-many-instance-attributes, unnecessary-lambda
# pylint: disable=super-init-not-called, too-many-lines, line-too-long, too-many-arguments
# pylint: disable=too-many-locals
import datetime
from typing import Optional, Dict, Any, MutableMapping, List, Union
from .. import serde
from ..types import BodyType, StreamBody, AsyncStreamBody
from .bucket_basic import Owner
from dataclasses import dataclass

class PutObjectRequest(serde.RequestModel):
    """The request for the PutObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "acl": {"tag": "input", "position": "header", "rename": "x-oss-object-acl"},
        "storage_class": {"tag": "input", "position": "header", "rename": "x-oss-storage-class"},
        "metadata": {"tag": "input", "position": "header", "rename": "x-oss-meta-", "type": "dict,usermeta"},
        "cache_control": {"tag": "input", "position": "header", "rename": "Cache-Control"},
        "content_disposition": {"tag": "input", "position": "header", "rename": "Content-Disposition"},
        "content_encoding": {"tag": "input", "position": "header", "rename": "Content-Encoding"},
        "content_length": {"tag": "input", "position": "header", "rename": "Content-Length", "type": "int"},
        "content_md5": {"tag": "input", "position": "header", "rename": "Content-MD5"},
        "content_type": {"tag": "input", "position": "header", "rename": "Content-Type"},
        "expires": {"tag": "input", "position": "header", "rename": "Expires"},
        "server_side_encryption": {"tag": "input", "position": "header", "rename": "x-oss-server-side-encryption"},
        "server_side_data_encryption": {"tag": "input", "position": "header", "rename": "x-oss-server-side-data-encryption"},
        "server_side_encryption_key_id": {"tag": "input", "position": "header", "rename": "x-oss-server-side-encryption-key-id"},
        "tagging": {"tag": "input", "position": "header", "rename": "x-oss-tagging"},
        "callback": {"tag": "input", "position": "header", "rename": "x-oss-callback"},
        "callback_var": {"tag": "input", "position": "header", "rename": "x-oss-callback-var"},
        "forbid_overwrite": {"tag": "input", "position": "header", "rename": "x-oss-forbid-overwrite", "type": "bool"},
        "traffic_limit": {"tag": "input", "position": "header", "rename": "x-oss-traffic-limit", "type": "int"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
        "body": {"tag": "input", "position": "body"},
        "progress_fn": {},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        acl: Optional[str] = None,
        storage_class: Optional[str] = None,
        metadata: Optional[MutableMapping] = None,
        cache_control: Optional[str] = None,
        content_disposition: Optional[str] = None,
        content_encoding: Optional[str] = None,
        content_length: Optional[int] = None,
        content_md5: Optional[str] = None,
        content_type: Optional[str] = None,
        expires: Optional[str] = None,
        server_side_encryption: Optional[str] = None,
        server_side_data_encryption: Optional[str] = None,
        server_side_encryption_key_id: Optional[str] = None,
        tagging: Optional[str] = None,
        callback: Optional[str] = None,
        callback_var: Optional[str] = None,
        forbid_overwrite: Optional[Union[str, bool]] = None,
        traffic_limit: Optional[int] = None,
        request_payer: Optional[str] = None,
        body: Optional[BodyType] = None,
        progress_fn: Optional[Any] = None,
        object_acl: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            acl (str, optional): The access control list (ACL) of the object.
            storage_class (str, optional): The storage class of the object.
            metadata (MutableMapping,The metadata of the object that you want to upload.
            cache_control (str, optional): The caching behavior of the web page when the object is downloaded.
            content_disposition (str, optional): The method that is used to access the object.
            content_encoding (str, optional): The method that is used to encode the object.
            content_length (int, optional): The size of the data in the HTTP message body. Unit: bytes.
            content_md5 (str, optional): The MD5 hash of the object that you want to upload.
            content_type (str, optional): A standard MIME type describing the format of the contents.
            expires (str, optional): The expiration time of the cache in UTC.
            server_side_encryption (str, optional): The encryption method on the server side when an object is created.
                Valid values: AES256 and KMS
            server_side_data_encryption (str, optional): The ID of the customer master key (CMK)
                that is managed by Key Management Service (KMS). This header is valid only
                when the x-oss-server-side-encryption header is set to KMS.
            server_side_encryption_key_id (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            tagging (str, optional): The tags that are specified for the object by using a key-value pair.
                You can specify multiple tags for an object. Example: TagA=A&TagB=B.
            callback (str, optional): A callback parameter is a Base64-encoded string that contains multiple fields in the JSON format.
            callback_var (str, optional): Configure custom parameters by using the callback-var parameter.
            forbid_overwrite (Union[str, bool], optional): Specifies whether the object that is uploaded by calling the PutObject operation
                overwrites an existing object that has the same name.
            traffic_limit (int, optional): Specify the speed limit value.
                The speed limit value ranges from 245760 to 838860800, with a unit of bit/s.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
            body (BodyType,optional): Object data.
            progress_fn (Any,optional): Progress callback function.
            object_acl (str, optional): The access control list (ACL) of the object.
                The object_acl parameter has the same functionality as the acl parameter. it is the standardized name for acl.
                If both exist simultaneously, the value of object_acl will take precedence.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.acl = object_acl if object_acl is not None else acl
        self.storage_class = storage_class
        self.metadata = metadata
        self.cache_control = cache_control
        self.content_disposition = content_disposition
        self.content_encoding = content_encoding
        self.content_length = content_length
        self.content_md5 = content_md5
        self.content_type = content_type
        self.expires = expires
        self.server_side_encryption = server_side_encryption
        self.server_side_data_encryption = server_side_data_encryption
        self.server_side_encryption_key_id = server_side_encryption_key_id
        self.tagging = tagging
        self.callback = callback
        self.callback_var = callback_var
        self.forbid_overwrite = forbid_overwrite
        self.traffic_limit = traffic_limit
        self.request_payer = request_payer
        self.body = body
        self.progress_fn = progress_fn


class PutObjectResult(serde.ResultModel):
    """The result for the PutObject operation."""

    _attribute_map = {
        "content_md5": {"tag": "output", "position": "header", "rename": "Content-MD5"},
        "etag": {"tag": "output", "position": "header", "rename": "ETag"},
        "hash_crc64": {"tag": "output", "position": "header", "rename": "x-oss-hash-crc64ecma"},
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "callback_result": {"tag": "output", "position": "body", "type": "dict,json"},
    }

    def __init__(
        self,
        content_md5: Optional[str] = None,
        etag: Optional[str] = None,
        hash_crc64: Optional[str] = None,
        version_id: Optional[str] = None,
        callback_result: Optional[Dict] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            content_md5 (str, optional): Content-Md5 for the uploaded object.
            etag (str, optional): Entity tag for the uploaded object.
            hash_crc64 (str, optional): The 64-bit CRC value of the object.
                This value is calculated based on the ECMA-182 standard.
            version_id (str, optional): Version of the object.
            callback_result (dict, optional): Callback result, 
                it is valid only when the callback is set.
        """
        super().__init__(**kwargs)
        self.content_md5 = content_md5
        self.etag = etag
        self.hash_crc64 = hash_crc64
        self.version_id = version_id
        self.callback_result = callback_result


class HeadObjectRequest(serde.RequestModel):
    """The request for the HeadObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "if_match": {"tag": "input", "position": "header", "rename": "If-Match"},
        "if_none_match": {"tag": "input", "position": "header", "rename": "If-None-Match"},
        "if_modified_since": {"tag": "input", "position": "header", "rename": "If-Modified-Since"},
        "if_unmodified_since": {"tag": "input", "position": "header", "rename": "If-Unmodified-Since"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        if_match: Optional[str] = None,
        if_none_match: Optional[str] = None,
        if_modified_since: Optional[str] = None,
        if_unmodified_since: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the source object.
            if_match (str, optional): If the ETag specified in the request matches the ETag value of the object
                the object and 200 OK are returned. Otherwise, 412 Precondition Failed is returned.
            if_none_match (str, optional): If the ETag specified in the request does not match the ETag value of the object,
                the object and 200 OK are returned. Otherwise, 304 Not Modified is returned.
            if_modified_since (str, optional): If the time specified in this header is earlier 
                than the object modified time or is invalid, the object and 200 OK are returned.
                Otherwise, 304 Not Modified is returned. The time must be in GMT. Example: Fri, 13 Nov 2015 14:47:53 GMT.
            if_unmodified_since (str, optional): If the time specified in this header is 
                the same as or later than the object modified time,the object and 200 OK are returned.
                Otherwise, 412 Precondition Failed is returned. The time must be in GMT. Example: Fri, 13 Nov 2015 14:47:53 GMT.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.if_match = if_match
        self.if_none_match = if_none_match
        self.if_modified_since = if_modified_since
        self.if_unmodified_since = if_unmodified_since
        self.request_payer = request_payer


class HeadObjectResult(serde.ResultModel):
    """The result for the HeadObject operation."""

    _attribute_map = {
        "content_length": {"tag": "output", "position": "header", "rename": "Content-Length", "type": "int"},
        "content_type": {"tag": "output", "position": "header", "rename": "Content-Type"},
        "etag": {"tag": "output", "position": "header", "rename": "ETag"},
        "last_modified": {"tag": "output", "position": "header", "rename": "Last-Modified", "type": "datetime,httptime"},
        "content_md5": {"tag": "output", "position": "header", "rename": "Content-MD5"},
        "metadata": {"tag": "output", "position": "header", "rename": "x-oss-meta-", "type": "dict,usermeta"},
        "cache_control": {"tag": "output", "position": "header", "rename": "Cache-Control"},
        "content_disposition": {"tag": "output", "position": "header", "rename": "Content-Disposition"},
        "content_encoding": {"tag": "output", "position": "header", "rename": "Content-Encoding"},
        "expires": {"tag": "output", "position": "header", "rename": "Expires"},
        "hash_crc64": {"tag": "output", "position": "header", "rename": "x-oss-hash-crc64ecma"},
        "storage_class": {"tag": "output", "position": "header", "rename": "x-oss-storage-class"},
        "object_type": {"tag": "output", "position": "header", "rename": "x-oss-object-type"},
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "tagging_count": {"tag": "output", "position": "header", "rename": "x-oss-tagging-count", "type": "int"},
        "server_side_encryption": {"tag": "output", "position": "header", "rename": "x-oss-server-side-encryption"},
        "server_side_data_encryption": {"tag": "output", "position": "header", "rename": "x-oss-server-side-data-encryption"},
        "server_side_encryption_key_id": {"tag": "output", "position": "header", "rename": "x-oss-server-side-encryption-key-id"},
        "next_append_position": {"tag": "output", "position": "header", "rename": "x-oss-next-append-position", "type": "int"},
        "expiration": {"tag": "output", "position": "header", "rename": "x-oss-expiration"},
        "restore": {"tag": "output", "position": "header", "rename": "x-oss-restore"},
        "process_status": {"tag": "output", "position": "header", "rename": "x-oss-process-status"},
        "request_charged": {"tag": "output", "position": "header", "rename": "x-oss-request-charged"},
        "allow_origin": {"tag": "output", "position": "header", "rename": "Access-Control-Allow-Origin"},
        "allow_methods": {"tag": "output", "position": "header", "rename": "Access-Control-Allow-Methods"},
        "allow_age": {"tag": "output", "position": "header", "rename": "Access-Control-Allow-Age"},
        "allow_headers": {"tag": "output", "position": "header", "rename": "Access-Control-Allow-Headers"},
        "expose_headers": {"tag": "output", "position": "header", "rename": "Access-Control-Expose-Headers"},
        'transition_time': {'tag': 'output', 'position': 'header', 'rename': 'x-oss-transition-time'},
        'sealed_time': {'tag': 'output', 'position': 'header', 'rename': 'x-oss-sealed-time'},
    }

    def __init__(
        self,
        content_length: Optional[int] = None,
        content_type: Optional[str] = None,
        etag: Optional[str] = None,
        last_modified: Optional[datetime.datetime] = None,
        content_md5: Optional[str] = None,
        metadata: Optional[MutableMapping] = None,
        cache_control: Optional[str] = None,
        content_disposition: Optional[str] = None,
        content_encoding: Optional[str] = None,
        expires: Optional[str] = None,
        hash_crc64: Optional[str] = None,
        storage_class: Optional[str] = None,
        object_type: Optional[str] = None,
        version_id: Optional[str] = None,
        tagging_count: Optional[int] = None,
        server_side_encryption: Optional[str] = None,
        server_side_data_encryption: Optional[str] = None,
        server_side_encryption_key_id: Optional[str] = None,
        next_append_position: Optional[str] = None,
        expiration: Optional[str] = None,
        restore: Optional[str] = None,
        process_status: Optional[str] = None,
        request_charged: Optional[str] = None,
        allow_origin: Optional[str] = None,
        allow_methods: Optional[str] = None,
        allow_age: Optional[str] = None,
        allow_headers: Optional[str] = None,
        expose_headers: Optional[str] = None,
        transition_time: Optional[str] = None,
        sealed_time: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            content_length (int, optional): Size of the body in bytes.
            content_type (str, optional): A standard MIME type describing the format of the object data.
            etag (str, optional): The entity tag (ETag).
                An ETag is created when an object is created to identify the content of the object.
            last_modified (datetime.datetime, optional): The time when the returned objects were last modified.
            content_md5 (str, optional): Content-Md5 for the uploaded object.
            metadata (MutableMapping, optional): A map of metadata to store with the object.
            cache_control (str, optional): The caching behavior of the web page when the object is downloaded.
            content_disposition (str, optional): The method that is used to access the object.
            content_encoding (str, optional): The method that is used to encode the object.
            expires (str, optional): The expiration time of the cache in UTC.
            hash_crc64 (str, optional): The 64-bit CRC value of the object.
                This value is calculated based on the ECMA-182 standard.
            storage_class (str, optional): The storage class of the object.
            object_type (str, optional): The type of the object.
            version_id (str, optional): Version of the object.
            tagging_count (int, optional): The number of tags added to the object.
                This header is included in the response only when you have read permissions on tags.
            server_side_encryption (str, optional): If the requested object is encrypted by 
                using a server-side encryption algorithm based on entropy encoding, OSS automatically decrypts
                the object and returns the decrypted object after OSS receives the GetObject request.
                The x-oss-server-side-encryption header is included in the response to indicate the encryption algorithm 
                used to encrypt the object on the server.
            server_side_data_encryption (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            server_side_encryption_key_id (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            next_append_position (str, optional): The position for the next append operation.
                If the type of the object is Appendable, this header is included in the response.
            expiration (str, optional): The lifecycle information about the object.
                If lifecycle rules are configured for the object, this header is included in the response.
                This header contains the following parameters: expiry-date that indicates the expiration time of the object,
                and rule-id that indicates the ID of the matched lifecycle rule.
            restore (str, optional): The status of the object when you restore an object.
                If the storage class of the bucket is Archive and a RestoreObject request is submitted,
            process_status (str, optional): The result of an event notification that is triggered for the object.
            request_charged (str, optional): The requester. This header is included in the response if the pay-by-requester mode
                is enabled for the bucket and the requester is not the bucket owner. The value of this header is requester
            allow_origin (str, optional): The origins allowed for cross-origin resource sharing (CORS).
            allow_methods (str, optional): The methods allowed for CORS.
            allow_age (str, optional): The maximum caching period for CORS. 
            allow_headers (str, optional): The headers allowed for CORS.
            expose_headers (str, optional): The headers that can be accessed by JavaScript applications on the client.
            transition_time (str, optional): The time when the storage class of the object is converted to Cold Archive or Deep Cold Archive based on lifecycle rules.
            sealed_time (str, optional): The time when the object was sealed.
        """
        super().__init__(**kwargs)
        self.content_length = content_length
        self.content_type = content_type
        self.etag = etag
        self.last_modified = last_modified
        self.content_md5 = content_md5
        self.metadata = metadata
        self.cache_control = cache_control
        self.content_disposition = content_disposition
        self.content_encoding = content_encoding
        self.expires = expires
        self.hash_crc64 = hash_crc64
        self.storage_class = storage_class
        self.object_type = object_type
        self.version_id = version_id
        self.tagging_count = tagging_count
        self.server_side_encryption = server_side_encryption
        self.server_side_data_encryption = server_side_data_encryption
        self.server_side_encryption_key_id = server_side_encryption_key_id
        self.next_append_position = next_append_position
        self.expiration = expiration
        self.restore = restore
        self.process_status = process_status
        self.request_charged = request_charged
        self.allow_origin = allow_origin
        self.allow_methods = allow_methods
        self.allow_age = allow_age
        self.allow_headers = allow_headers
        self.expose_headers = expose_headers
        self.transition_time = transition_time
        self.sealed_time = sealed_time

class GetObjectRequest(serde.RequestModel):
    """The request for the GetObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "if_match": {"tag": "input", "position": "header", "rename": "If-Match"},
        "if_none_match": {"tag": "input", "position": "header", "rename": "If-None-Match"},
        "if_modified_since": {"tag": "input", "position": "header", "rename": "If-Modified-Since"},
        "if_unmodified_since": {"tag": "input", "position": "header", "rename": "If-Unmodified-Since"},
        "range_header": {"tag": "input", "position": "header", "rename": "Range"},
        "range_behavior": {"tag": "input", "position": "header", "rename": "x-oss-range-behavior"},
        "response_cache_control": {"tag": "input", "position": "query", "rename": "response-cache-control"},
        "response_content_disposition": {"tag": "input", "position": "query", "rename": "response-content-disposition"},
        "response_content_encoding": {"tag": "input", "position": "query", "rename": "response-content-encoding"},
        "response_content_language": {"tag": "input", "position": "query", "rename": "response-content-language"},
        "response_content_type": {"tag": "input", "position": "query", "rename": "response-content-type"},
        "response_expires": {"tag": "input", "position": "query", "rename": "response-expires"},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "traffic_limit": {"tag": "input", "position": "header", "rename": "x-oss-traffic-limit", "type": "int"},
        "process": {"tag": "input", "position": "query", "rename": "x-oss-process"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
        'accept_encoding': {'tag': 'input', 'position': 'header', 'rename': 'Accept-Encoding', 'type': 'str'},
        "progress_fn": {},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        if_match: Optional[str] = None,
        if_none_match: Optional[str] = None,
        if_modified_since: Optional[str] = None,
        if_unmodified_since: Optional[str] = None,
        range_header: Optional[str] = None,
        range_behavior: Optional[str] = None,
        response_cache_control: Optional[str] = None,
        response_content_disposition: Optional[str] = None,
        response_content_encoding: Optional[str] = None,
        response_content_language: Optional[str] = None,
        response_content_type: Optional[str] = None,
        response_expires: Optional[str] = None,
        version_id: Optional[str] = None,
        traffic_limit: Optional[int] = None,
        process: Optional[str] = None,
        request_payer: Optional[str] = None,
        accept_encoding: Optional[str] = None,
        progress_fn: Optional[Any] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            if_match (str, optional): If the ETag specified in the request matches the ETag value of the object
                the object and 200 OK are returned. Otherwise, 412 Precondition Failed is returned.
            if_none_match (str, optional): If the ETag specified in the request does not match the ETag value of the object,
                the object and 200 OK are returned. Otherwise, 304 Not Modified is returned.
            if_modified_since (str, optional): If the time specified in this header is earlier 
                than the object modified time or is invalid, the object and 200 OK are returned.
                Otherwise, 304 Not Modified is returned. The time must be in GMT. Example: Fri, 13 Nov 2015 14:47:53 GMT.
            if_unmodified_since (str, optional): If the time specified in this header is 
                the same as or later than the object modified time,the object and 200 OK are returned.
                Otherwise, 412 Precondition Failed is returned. The time must be in GMT. Example: Fri, 13 Nov 2015 14:47:53 GMT.
            range_header (str, optional): The content range of the object to be returned.
                If the value of Range is valid, the total size of the object and the content range are returned.
                For example, Content-Range: bytes 0~9/44 indicates that the total size of the object is 44 bytes,
                and the range of data returned is the first 10 bytes.
                However, if the value of Range is invalid, the entire object is returned,
                and the response does not include the Content-Range parameter.
            range_behavior (str, optional): Specify standard behaviors to download data by range.
                If the value is "standard", the download behavior is modified when the specified range is not within the valid range.
                For an object whose size is 1,000 bytes:
                1) If you set Range: bytes to 500-2000, the value at the end of the range is invalid.
                In this case, OSS returns HTTP status code 206 and the data that is within the range of byte 500 to byte 999.
                2) If you set Range: bytes to 1000-2000, the value at the start of the range is invalid.
                In this case, OSS returns HTTP status code 416 and the InvalidRange error code.
            response_cache_control (str, optional): The cache-control header to be returned in the response.
            response_content_disposition (str, optional): The content-disposition header to be returned in the response.
            response_content_encoding (str, optional): The content-encoding header to be returned in the response.
            response_content_language (str, optional): The content-language header to be returned in the response.
            response_content_type (str, optional): The content-type header to be returned in the response.
            response_expires (str, optional): The expires header to be returned in the response.
            version_id (str, optional): VersionId used to reference a specific version of the object.
            traffic_limit (int, optional): Specify the speed limit value.
                The speed limit value ranges from 245760 to 838860800, with a unit of bit/s.
            process (str, optional): Image processing parameters.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
            accept_encoding (str, optional): The encoding type at the client side. If you want an object to be returned in the GZIP format, you must include the Accept-Encoding:gzip header in your request.
                OSS determines whether to return the object compressed in the GZip format based on the Content-Type header and whether the size of the object is larger than or equal to 1 KB.
                If an object is compressed in the GZip format, the response OSS returns does not include the ETag value of the object.
                - OSS supports the following Content-Type values to compress the object in the GZip format:
                    text/cache-manifest, text/xml, text/plain, text/css, application/javascript, application/x-javascript, application/rss+xml, application/json, and text/json. Default value: null
            progress_fn (Any, optional): Progress callback function.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.if_match = if_match
        self.if_none_match = if_none_match
        self.if_modified_since = if_modified_since
        self.if_unmodified_since = if_unmodified_since
        self.range_header = range_header
        self.range_behavior = range_behavior
        self.response_cache_control = response_cache_control
        self.response_content_disposition = response_content_disposition
        self.response_content_encoding = response_content_encoding
        self.response_content_language = response_content_language
        self.response_content_type = response_content_type
        self.response_expires = response_expires
        self.version_id = version_id
        self.traffic_limit = traffic_limit
        self.process = process
        self.request_payer = request_payer
        self.accept_encoding = accept_encoding
        self.progress_fn = progress_fn


class GetObjectResult(serde.ResultModel):
    """The result for the GetObject operation."""

    _attribute_map = {
        "content_length": {"tag": "output", "position": "header", "rename": "Content-Length", "type": "int"},
        "content_range": {"tag": "output", "position": "header", "rename": "Content-Range"},
        "content_type": {"tag": "output", "position": "header", "rename": "Content-Type"},
        "etag": {"tag": "output", "position": "header", "rename": "ETag"},
        "last_modified": {"tag": "output", "position": "header", "rename": "Last-Modified", "type": "datetime,httptime"},
        "content_md5": {"tag": "output", "position": "header", "rename": "Content-MD5"},
        "metadata": {"tag": "output", "position": "header", "rename": "x-oss-meta-", "type": "dict,usermeta"},
        "cache_control": {"tag": "output", "position": "header", "rename": "Cache-Control"},
        "content_disposition": {"tag": "output", "position": "header", "rename": "Content-Disposition"},
        "content_encoding": {"tag": "output", "position": "header", "rename": "Content-Encoding"},
        "expires": {"tag": "output", "position": "header", "rename": "Expires"},
        "hash_crc64": {"tag": "output", "position": "header", "rename": "x-oss-hash-crc64ecma"},
        "storage_class": {"tag": "output", "position": "header", "rename": "x-oss-storage-class"},
        "object_type": {"tag": "output", "position": "header", "rename": "x-oss-object-type"},
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "tagging_count": {"tag": "output", "position": "header", "rename": "x-oss-tagging-count", "type": "int"},
        "server_side_encryption": {"tag": "output", "position": "header", "rename": "x-oss-server-side-encryption"},
        "server_side_data_encryption": {"tag": "output", "position": "header", "rename": "x-oss-server-side-data-encryption"},
        "server_side_encryption_key_id": {"tag": "output", "position": "header", "rename": "x-oss-server-side-encryption-key-id"},
        "next_append_position": {"tag": "output", "position": "header", "rename": "x-oss-next-append-position", "type": "int"},
        "expiration": {"tag": "output", "position": "header", "rename": "x-oss-expiration"},
        "restore": {"tag": "output", "position": "header", "rename": "x-oss-restore"},
        "process_status": {"tag": "output", "position": "header", "rename": "x-oss-process-status"},
        "delete_marker": {"tag": "output", "position": "header", "rename": "x-oss-delete-marker", "type": "bool"},
        'sealed_time': {'tag': 'output', 'position': 'header', 'rename': 'x-oss-sealed-time'},
        "body": {},
    }

    def __init__(
        self,
        content_length: Optional[int] = None,
        content_range: Optional[str] = None,
        content_type: Optional[str] = None,
        etag: Optional[str] = None,
        last_modified: Optional[datetime.datetime] = None,
        content_md5: Optional[str] = None,
        metadata: Optional[MutableMapping] = None,
        cache_control: Optional[str] = None,
        content_disposition: Optional[str] = None,
        content_encoding: Optional[str] = None,
        expires: Optional[str] = None,
        hash_crc64: Optional[str] = None,
        storage_class: Optional[str] = None,
        object_type: Optional[str] = None,
        version_id: Optional[str] = None,
        tagging_count: Optional[int] = None,
        server_side_encryption: Optional[str] = None,
        server_side_data_encryption: Optional[str] = None,
        server_side_encryption_key_id: Optional[str] = None,
        next_append_position: Optional[str] = None,
        expiration: Optional[str] = None,
        restore: Optional[str] = None,
        process_status: Optional[str] = None,
        delete_marker: Optional[bool] = None,
        sealed_time: Optional[str] = None,
        body: Optional[Union[StreamBody, AsyncStreamBody]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            content_length (int, optional): Size of the body in bytes.
            content_range (str, optional): The portion of the object returned in the response.
            content_type (str, optional): A standard MIME type describing the format of the object data.
            etag (str, optional): The entity tag (ETag).
                An ETag is created when an object is created to identify the content of the object.
            last_modified (datetime.datetime, optional): The time when the returned objects were last modified.
            content_md5 (str, optional): Content-Md5 for the uploaded object.
            metadata (MutableMapping, optional): A map of metadata to store with the object.
            cache_control (str, optional): The caching behavior of the web page when the object is downloaded.
            content_disposition (str, optional): The method that is used to access the object.
            content_encoding (str, optional): The method that is used to encode the object.
            expires (str, optional): The expiration time of the cache in UTC.
            hash_crc64 (str, optional): The 64-bit CRC value of the object.
                This value is calculated based on the ECMA-182 standard.
            storage_class (str, optional): The storage class of the object.
            object_type (str, optional): The type of the object.
            version_id (str, optional): Version of the object.
            tagging_count (int, optional): The number of tags added to the object.
                This header is included in the response only when you have read permissions on tags.
            server_side_encryption (str, optional): If the requested object is encrypted by 
                using a server-side encryption algorithm based on entropy encoding, OSS automatically decrypts
                the object and returns the decrypted object after OSS receives the GetObject request.
                The x-oss-server-side-encryption header is included in the response to indicate the encryption algorithm 
                used to encrypt the object on the server.
            server_side_data_encryption (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            server_side_encryption_key_id (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            next_append_position (str, optional): The position for the next append operation.
                If the type of the object is Appendable, this header is included in the response.
            expiration (str, optional): The lifecycle information about the object.
                If lifecycle rules are configured for the object, this header is included in the response.
                This header contains the following parameters: expiry-date that indicates the expiration time of the object,
                and rule-id that indicates the ID of the matched lifecycle rule.
            restore (str, optional): The status of the object when you restore an object.
                If the storage class of the bucket is Archive and a RestoreObject request is submitted,
            process_status (str, optional): The result of an event notification that is triggered for the object.
            delete_marker (bool, optional): Specifies whether the object retrieved was (true) or was not (false) a Delete  Marker.
            sealed_time (str, optional): The time when the object was sealed.
            body (Any, optional): Object data.
        """
        super().__init__(**kwargs)
        self.content_length = content_length
        self.content_range = content_range
        self.content_type = content_type
        self.etag = etag
        self.last_modified = last_modified
        self.content_md5 = content_md5
        self.metadata = metadata
        self.cache_control = cache_control
        self.content_disposition = content_disposition
        self.content_encoding = content_encoding
        self.expires = expires
        self.hash_crc64 = hash_crc64
        self.storage_class = storage_class
        self.object_type = object_type
        self.version_id = version_id
        self.tagging_count = tagging_count
        self.server_side_encryption = server_side_encryption
        self.server_side_data_encryption = server_side_data_encryption
        self.server_side_encryption_key_id = server_side_encryption_key_id
        self.next_append_position = next_append_position
        self.expiration = expiration
        self.restore = restore
        self.process_status = process_status
        self.delete_marker = delete_marker
        self.sealed_time = sealed_time
        self.body = body



class AppendObjectRequest(serde.RequestModel):
    """The request for the AppendObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "position": {"tag": "input", "position": "query", "rename": "position", "required": True},
        "acl": {"tag": "input", "position": "header", "rename": "x-oss-object-acl"},
        "storage_class": {"tag": "input", "position": "header", "rename": "x-oss-storage-class"},
        "metadata": {"tag": "input", "position": "header", "rename": "x-oss-meta-", "type": "dict,usermeta"},
        "cache_control": {"tag": "input", "position": "header", "rename": "Cache-Control"},
        "content_disposition": {"tag": "input", "position": "header", "rename": "Content-Disposition"},
        "content_encoding": {"tag": "input", "position": "header", "rename": "Content-Encoding"},
        "content_length": {"tag": "input", "position": "header", "rename": "Content-Length", "type": "int"},
        "content_md5": {"tag": "input", "position": "header", "rename": "Content-MD5"},
        "content_type": {"tag": "input", "position": "header", "rename": "Content-Type"},
        "expires": {"tag": "input", "position": "header", "rename": "Expires"},
        "server_side_encryption": {"tag": "input", "position": "header", "rename": "x-oss-server-side-encryption"},
        "server_side_data_encryption": {"tag": "input", "position": "header", "rename": "x-oss-server-side-data-encryption"},
        "server_side_encryption_key_id": {"tag": "input", "position": "header", "rename": "x-oss-server-side-encryption-key-id"},
        "tagging": {"tag": "input", "position": "header", "rename": "x-oss-tagging"},
        "forbid_overwrite": {"tag": "input", "position": "header", "rename": "x-oss-forbid-overwrite", "type": "bool"},
        "traffic_limit": {"tag": "input", "position": "header", "rename": "x-oss-traffic-limit", "type": "int"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
        "body": {"tag": "input", "position": "body"},
        "progress_fn": {},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        position: int = None,
        acl: Optional[str] = None,
        storage_class: Optional[str] = None,
        metadata: Optional[MutableMapping] = None,
        cache_control: Optional[str] = None,
        content_disposition: Optional[str] = None,
        content_encoding: Optional[str] = None,
        content_length: Optional[int] = None,
        content_md5: Optional[str] = None,
        content_type: Optional[str] = None,
        expires: Optional[str] = None,
        server_side_encryption: Optional[str] = None,
        server_side_data_encryption: Optional[str] = None,
        server_side_encryption_key_id: Optional[str] = None,
        tagging: Optional[str] = None,
        forbid_overwrite: Optional[Union[str, bool]] = None,
        traffic_limit: Optional[int] = None,
        request_payer: Optional[str] = None,
        body: Optional[BodyType] = None,
        progress_fn: Optional[Any] = None,
        object_acl: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            position (str, required): The position from which the AppendObject operation starts.
                Each time an AppendObject operation succeeds, the x-oss-next-append-position header is included in
                the response to specify the position from which the next AppendObject operation starts.
            acl (str, optional): The access control list (ACL) of the object.
            storage_class (str, optional): The storage class of the object.
            metadata (MutableMapping,The metadata of the object that you want to upload.
            cache_control (str, optional): The caching behavior of the web page when the object is downloaded.
            content_disposition (str, optional): The method that is used to access the object.
            content_encoding (str, optional): The method that is used to encode the object.
            content_length (int, optional): The size of the data in the HTTP message body. Unit: bytes.
            content_md5 (str, optional): The MD5 hash of the object that you want to upload.
            content_type (str, optional): A standard MIME type describing the format of the contents.
            expires (str, optional): The expiration time of the cache in UTC.
            server_side_encryption (str, optional): The encryption method on the server side when an object is created.
                Valid values: AES256 and KMS
            server_side_data_encryption (str, optional): The ID of the customer master key (CMK)
                that is managed by Key Management Service (KMS). This header is valid only
                when the x-oss-server-side-encryption header is set to KMS.
            server_side_encryption_key_id (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            tagging (str, optional): The tags that are specified for the object by using a key-value pair.
                You can specify multiple tags for an object. Example: TagA=A&TagB=B.
            callback (str, optional): A callback parameter is a Base64-encoded string that contains multiple fields in the JSON format.
            callback_var (str, optional): Configure custom parameters by using the callback-var parameter.
            forbid_overwrite (Union[str, bool], optional): Specifies whether the object that is uploaded by calling the PutObject operation
                overwrites an existing object that has the same name.
            traffic_limit (int, optional): Specify the speed limit value.
                The speed limit value ranges from 245760 to 838860800, with a unit of bit/s.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
            body (BodyType,optional): Object data.
            progress_fn (Any,optional): Progress callback function.
            object_acl (str, optional): The access control list (ACL) of the object.
                The object_acl parameter has the same functionality as the acl parameter. it is the standardized name for acl.
                If both exist simultaneously, the value of object_acl will take precedence.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.position = position
        self.acl = object_acl if object_acl is not None else acl
        self.storage_class = storage_class
        self.metadata = metadata
        self.cache_control = cache_control
        self.content_disposition = content_disposition
        self.content_encoding = content_encoding
        self.content_length = content_length
        self.content_md5 = content_md5
        self.content_type = content_type
        self.expires = expires
        self.server_side_encryption = server_side_encryption
        self.server_side_data_encryption = server_side_data_encryption
        self.server_side_encryption_key_id = server_side_encryption_key_id
        self.tagging = tagging
        self.forbid_overwrite = forbid_overwrite
        self.traffic_limit = traffic_limit
        self.request_payer = request_payer
        self.body = body
        self.progress_fn = progress_fn


class AppendObjectResult(serde.ResultModel):
    """The result for the AppendObject operation."""

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "hash_crc64": {"tag": "output", "position": "header", "rename": "x-oss-hash-crc64ecma"},
        "next_position": {"tag": "output", "position": "header", "rename": "x-oss-next-append-position", "type": "int"},
        "server_side_encryption": {"tag": "output", "position": "header", "rename": "x-oss-server-side-encryption"},
        "server_side_data_encryption": {"tag": "output", "position": "header", "rename": "x-oss-server-side-data-encryption"},
        "server_side_encryption_key_id": {"tag": "output", "position": "header", "rename": "x-oss-server-side-encryption-key-id"},
    }

    def __init__(
        self,
        version_id: Optional[str] = None,
        hash_crc64: Optional[str] = None,
        next_position: Optional[int] = None,
        server_side_encryption: Optional[str] = None,
        server_side_data_encryption: Optional[str] = None,
        server_side_encryption_key_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
            hash_crc64 (str, optional): The 64-bit CRC value of the object.
                This value is calculated based on the ECMA-182 standard.
            next_position (str, optional): The position that must be provided in the next request,
                which is the current length of the object.
            server_side_encryption (str, optional): The encryption method on the server side when an object is created.
                Valid values: AES256 and KMS
            server_side_data_encryption (str, optional): The ID of the customer master key (CMK)
                that is managed by Key Management Service (KMS). This header is valid only when the x-oss-server-side-encryption header
                is set to KMS.
            server_side_encryption_key_id (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
        """
        super().__init__(**kwargs)
        self.version_id = version_id
        self.hash_crc64 = hash_crc64
        self.next_position = next_position
        self.server_side_encryption = server_side_encryption
        self.server_side_data_encryption = server_side_data_encryption
        self.server_side_encryption_key_id = server_side_encryption_key_id


class CopyObjectRequest(serde.RequestModel):
    """The request for the CopyObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "source_bucket": {"tag": "input", "position": "nop"},
        "source_key": {"tag": "input", "position": "nop", "required": True},
        "source_version_id": {"tag": "input", "position": "nop"},
        "if_match": {"tag": "input", "position": "header", "rename": "x-oss-copy-source-if-match"},
        "if_none_match": {"tag": "input", "position": "header", "rename": "x-oss-copy-source-if-none-match"},
        "if_modified_since": {"tag": "input", "position": "header", "rename": "x-oss-copy-source-if-modified-since"},
        "if_unmodified_since": {"tag": "input", "position": "header", "rename": "x-oss-copy-source-if-unmodified-since"},
        "acl": {"tag": "input", "position": "header", "rename": "x-oss-object-acl"},
        "storage_class": {"tag": "input", "position": "header", "rename": "x-oss-storage-class"},
        "metadata": {"tag": "input", "position": "header", "rename": "x-oss-meta-", "type": "dict,usermeta"},
        "cache_control": {"tag": "input", "position": "header", "rename": "Cache-Control"},
        "content_disposition": {"tag": "input", "position": "header", "rename": "Content-Disposition"},
        "content_encoding": {"tag": "input", "position": "header", "rename": "Content-Encoding"},
        "content_length": {"tag": "input", "position": "header", "rename": "Content-Length", "type": "int"},
        "content_md5": {"tag": "input", "position": "header", "rename": "Content-MD5"},
        "content_type": {"tag": "input", "position": "header", "rename": "Content-Type"},
        "expires": {"tag": "input", "position": "header", "rename": "Expires"},
        "metadata_directive": {"tag": "input", "position": "header", "rename": "x-oss-metadata-directive"},
        "server_side_encryption": {"tag": "input", "position": "header", "rename": "x-oss-server-side-encryption"},
        "server_side_data_encryption": {"tag": "input", "position": "header", "rename": "x-oss-server-side-data-encryption"},
        "server_side_encryption_key_id": {"tag": "input", "position": "header", "rename": "x-oss-server-side-encryption-key-id"},
        "tagging": {"tag": "input", "position": "header", "rename": "x-oss-tagging"},
        "tagging_directive": {"tag": "input", "position": "header", "rename": "x-oss-tagging-directive"},
        "forbid_overwrite": {"tag": "input", "position": "header", "rename": "x-oss-forbid-overwrite", "type": "bool"},
        "traffic_limit": {"tag": "input", "position": "header", "rename": "x-oss-traffic-limit", "type": "int"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
        "progress_fn": {},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        source_bucket: Optional[str] = None,
        source_key: Optional[str] = None,
        source_version_id: Optional[str] = None,
        if_match: Optional[str] = None,
        if_none_match: Optional[str] = None,
        if_modified_since: Optional[str] = None,
        if_unmodified_since: Optional[str] = None,
        acl: Optional[str] = None,
        storage_class: Optional[str] = None,
        metadata: Optional[MutableMapping] = None,
        cache_control: Optional[str] = None,
        content_disposition: Optional[str] = None,
        content_encoding: Optional[str] = None,
        content_length: Optional[int] = None,
        content_md5: Optional[str] = None,
        content_type: Optional[str] = None,
        expires: Optional[str] = None,
        metadata_directive: Optional[str] = None,
        server_side_encryption: Optional[str] = None,
        server_side_data_encryption: Optional[str] = None,
        server_side_encryption_key_id: Optional[str] = None,
        tagging: Optional[str] = None,
        tagging_directive: Optional[str] = None,
        forbid_overwrite: Optional[Union[str, bool]] = None,
        traffic_limit: Optional[int] = None,
        request_payer: Optional[str] = None,
        progress_fn: Optional[Any] = None,
        object_acl: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            source_bucket (str, optional): The name of the source bucket.
            source_key (str, required): The name of the source object.
            source_version_id (str, optional): The version ID of the source object.
            if_match (str, optional): Specifies whether the object that is uploaded by
                calling the CopyObject operation overwrites an existing object that has the same name.
                Valid values: true and false
            if_none_match (str, optional): If the ETag specified in the request does not match the ETag value of the object,
                the object and 200 OK are returned. Otherwise, 304 Not Modified is returned.
            if_modified_since (str, optional): If the time specified in this header is earlier than 
                the object modified time or is invalid, the object and 200 OK are returned.
                Otherwise, 304 Not Modified is returned. The time must be in GMT. Example: Fri, 13 Nov 2015 14:47:53 GMT.
            if_unmodified_since (str, optional): If the time specified in this header is the same as or later than
                the object modified time, the object and 200 OK are returned. Otherwise, 412 Precondition Failed is returned.
                The time must be in GMT. Example: Fri, 13 Nov 2015 14:47:53 GMT.
            acl (str, optional): The access control list (ACL) of the object.
            storage_class (str, optional): The storage class of the object.
            metadata (MutableMapping,The metadata of the object that you want to upload.
            cache_control (str, optional): The caching behavior of the web page when the object is downloaded.
            content_disposition (str, optional): The method that is used to access the object.
            content_encoding (str, optional): The method that is used to encode the object.
            content_length (int, optional): The size of the data in the HTTP message body. Unit: bytes.
            content_md5 (str, optional): The MD5 hash of the object that you want to upload.
            content_type (str, optional): A standard MIME type describing the format of the contents.
            expires (str, optional): The expiration time of the cache in UTC.
            metadata_directive (str, optional): The method that is used to configure the metadata of the destination object.
                COPY (default): The metadata of the source object is copied to the destination object.
                The configurations of the x-oss-server-side-encryption header of the source object
                header of the source object are not copied to the destination object.
                The x-oss-server-side-encryption header in the CopyObject request specifies 
                the method used to encrypt the destination object.
                REPLACE: The metadata specified in the request is used as the metadata of the destination object.
            server_side_encryption (str, optional): The encryption method on the server side when an object is created.
                Valid values: AES256 and KMS
            server_side_data_encryption (str, optional): The ID of the customer master key (CMK)
                that is managed by Key Management Service (KMS). This header is valid only
                when the x-oss-server-side-encryption header is set to KMS.
            server_side_encryption_key_id (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            tagging (str, optional): The tags that are specified for the object by using a key-value pair.
                You can specify multiple tags for an object. Example: TagA=A&TagB=B.
            tagging_directive (str, optional): The method that is used to configure tags for the destination object.
                Valid values: Copy (default): The tags of the source object are copied to the destination object.
                Replace: The tags specified in the request are configured for the destination object.
            forbid_overwrite (Union[str, bool], optional): Specifies whether the object that is uploaded by calling the PutObject operation
                overwrites an existing object that has the same name.
            traffic_limit (int, optional): Specify the speed limit value.
                The speed limit value ranges from 245760 to 838860800, with a unit of bit/s.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
            progress_fn (Any,optional):  Progress callback function, it works in Copier.copy only.
            object_acl (str, optional): The access control list (ACL) of the object.
                The object_acl parameter has the same functionality as the acl parameter. it is the standardized name for acl.
                If both exist simultaneously, the value of object_acl will take precedence.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.source_bucket = source_bucket
        self.source_key = source_key
        self.source_version_id = source_version_id
        self.if_match = if_match
        self.if_none_match = if_none_match
        self.if_modified_since = if_modified_since
        self.if_unmodified_since = if_unmodified_since
        self.acl = object_acl if object_acl is not None else acl
        self.storage_class = storage_class
        self.metadata = metadata
        self.cache_control = cache_control
        self.content_disposition = content_disposition
        self.content_encoding = content_encoding
        self.content_length = content_length
        self.content_md5 = content_md5
        self.content_type = content_type
        self.expires = expires
        self.metadata_directive = metadata_directive
        self.server_side_encryption = server_side_encryption
        self.server_side_data_encryption = server_side_data_encryption
        self.server_side_encryption_key_id = server_side_encryption_key_id
        self.tagging = tagging
        self.tagging_directive = tagging_directive
        self.forbid_overwrite = forbid_overwrite
        self.traffic_limit = traffic_limit
        self.request_payer = request_payer
        self.progress_fn = progress_fn


class CopyObjectResult(serde.ResultModel):
    """The result for the CopyObject operation."""

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "hash_crc64": {"tag": "output", "position": "header", "rename": "x-oss-hash-crc64ecma"},
        "source_version_id": {"tag": "output", "position": "header", "rename": "x-oss-copy-source-version-id"},
        "server_side_encryption": {"tag": "output", "position": "header", "rename": "x-oss-server-side-encryption"},
        "server_side_data_encryption": {"tag": "output", "position": "header", "rename": "x-oss-server-side-data-encryption"},
        "server_side_encryption_key_id": {"tag": "output", "position": "header", "rename": "x-oss-server-side-encryption-key-id"},
        "last_modified": {"tag": "xml", "rename": "LastModified", "type": "datetime"},
        "etag": {"tag": "xml", "rename": "ETag"},
    }

    def __init__(
        self,
        version_id: Optional[str] = None,
        hash_crc64: Optional[str] = None,
        source_version_id: Optional[str] = None,
        server_side_encryption: Optional[str] = None,
        server_side_data_encryption: Optional[str] = None,
        server_side_encryption_key_id: Optional[str] = None,
        last_modified: Optional[datetime.datetime] = None,
        etag: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
            hash_crc64 (str, optional): The 64-bit CRC value of the object.
                This value is calculated based on the ECMA-182 standard.
            source_version_id (str, optional): The version ID of the source object.
            server_side_encryption (str, optional): The encryption method on the server side when an object is created.
                Valid values: AES256 and KMS
            server_side_data_encryption (str, optional): The server side data encryption algorithm.
            server_side_encryption_key_id (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            last_modified (str, optional): The time when the returned objects were last modified.
            etag (str, optional): The entity tag (ETag).
                An ETag is created when an object is created to identify the content of the object.
        """
        super().__init__(**kwargs)
        self.version_id = version_id
        self.hash_crc64 = hash_crc64
        self.source_version_id = source_version_id
        self.server_side_encryption = server_side_encryption
        self.server_side_data_encryption = server_side_data_encryption
        self.server_side_encryption_key_id = server_side_encryption_key_id
        self.last_modified = last_modified
        self.etag = etag


class DeleteObjectRequest(serde.RequestModel):
    """The request for the DeleteObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.request_payer = request_payer


class DeleteObjectResult(serde.ResultModel):
    """The result for the DeleteObject operation."""

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "delete_marker": {"tag": "output", "position": "header", "rename": "x-oss-delete-marker", "type": "bool"},
    }

    def __init__(
        self,
        version_id: Optional[str] = None,
        delete_marker: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
            delete_marker (bool, optional): Indicates whether the deleted version is a delete marker.
        """
        super().__init__(**kwargs)
        self.version_id = version_id
        self.delete_marker = delete_marker


class DeleteObject(serde.Model):
    """The information about a delete object."""

    def __init__(
        self,
        key: Optional[str] = None,
        version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The name of the object that you want to delete.
            version_id (str, optional): The version ID of the object that you want to delete.
        """
        super().__init__(**kwargs)
        self.key = key
        self.version_id = version_id

    _attribute_map = {
        "key": {"tag": "xml", "rename": "Key"},
        "version_id": {"tag": "xml", "rename": "VersionId"},
    }
    _xml_map = {
        "name": "Object"
    }

class ObjectIdentifier(serde.Model):
    """The identifier of an object to delete."""

    _attribute_map = {
        "key": {"tag": "xml", "rename": "Key", "required": True},
        "version_id": {"tag": "xml", "rename": "VersionId"},
    }

    _xml_map = {
        "name": "Object"
    }

    def __init__(
        self,
        key: Optional[str] = None,
        version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the object.
        """
        super().__init__(**kwargs)
        self.key = key
        self.version_id = version_id


class Delete(serde.Model):
    """The container for the objects to delete."""

    _attribute_map = {
        "objects": {"tag": "xml", "rename": "Object", "type": "[ObjectIdentifier]"},
        "quiet": {"tag": "xml", "rename": "Quiet", "type": "bool"},
    }

    _xml_map = {
        "name": "Delete"
    }

    _dependency_map = {
        "ObjectIdentifier": {"new": lambda: ObjectIdentifier()},
    }

    def __init__(
        self,
        objects: Optional[List[ObjectIdentifier]] = None,
        quiet: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            objects (List[ObjectIdentifier], optional): The list of objects to delete.
            quiet (bool, optional): Specifies whether to enable the Quiet return mode.
        """
        super().__init__(**kwargs)
        self.objects = objects
        self.quiet = quiet


class DeleteMultipleObjectsRequest(serde.RequestModel):
    """The request for the DeleteMultipleObjects operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "encoding_type": {"tag": "input", "position": "query", "rename": "encoding-type"},
        "objects": {"tag": "input", "position": "nop"},
        "quiet": {"tag": "input", "position": "nop"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
        "delete": {"tag": "input", "position": "body", "rename": "nop"},
    }

    def __init__(
        self,
        bucket: str = None,
        encoding_type: Optional[str] = None,
        objects: Optional[List[DeleteObject]] = None,
        quiet: Optional[bool] = None,
        request_payer: Optional[str] = None,
        delete: Optional[Delete] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            encoding_type (str, optional): The encoding type of the object names in the response. Valid value: url
            objects ([DeleteObject], optional): The container that stores information about you want to delete objects.
                This parameter is deprecated. Use 'delete' parameter instead.
            quiet (bool, optional): Specifies whether to enable the Quiet return mode.
                The DeleteMultipleObjects operation provides the following return modes: Valid value: true,false
                This parameter is deprecated. Use 'delete' parameter instead.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
            delete (Delete, optional): The container that stores information about you want to delete objects.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.encoding_type = encoding_type
        self.objects = objects
        self.quiet = quiet
        self.request_payer = request_payer
        self.delete = delete


class DeletedInfo(serde.Model):
    """The information about a delete object."""

    def __init__(
        self,
        key: Optional[str] = None,
        version_id: Optional[str] = None,
        delete_marker: Optional[bool] = None,
        delete_marker_version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The name of the deleted object.
            version_id (str, optional): The version ID of the object that you deleted.
            delete_marker (bool, optional): Indicates whether the deleted version is a delete marker.
            delete_marker_version_id (str, optional): The version ID of the delete marker.
        """
        super().__init__(**kwargs)
        self.key = key
        self.version_id = version_id
        self.delete_marker = delete_marker
        self.delete_marker_version_id = delete_marker_version_id

    _attribute_map = {
        "key": {"tag": "xml", "rename": "Key"},
        "version_id": {"tag": "xml", "rename": "VersionId"},
        "delete_marker": {"tag": "xml", "rename": "DeleteMarker", "type": "bool"},
        "delete_marker_version_id": {"tag": "xml", "rename": "DeleteMarkerVersionId"},
    }
    _xml_map = {
        "name": "Deleted"
    }


class DeleteMultipleObjectsResult(serde.ResultModel):
    """The result for the DeleteMultipleObjects operation."""

    _attribute_map = {
        "deleted_objects": {"tag": "xml", "rename": "Deleted", "type": "[DeletedInfo]"},
        "encoding_type": {"tag": "xml", "rename": "EncodingType"},
    }

    _dependency_map = {
        "DeletedInfo": {"new": lambda: DeletedInfo()},
    }

    _xml_map = {
        "name": "DeleteResult"
    }

    def __init__(
        self,
        deleted_objects: Optional[List[DeletedInfo]] = None,
        encoding_type: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            deleted_objects ([DeletedInfo], optional): The container that stores information about the deleted objects.
            encoding_type (str, optional): The encoding type of the content in the response.
                If encoding-type is specified in the request, the object name is encoded in the returned result.
        """
        super().__init__(**kwargs)
        self.deleted_objects = deleted_objects
        self.encoding_type = encoding_type

class GetObjectMetaRequest(serde.RequestModel):
    """The request for the GetObjectMeta operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the source object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.request_payer = request_payer


class GetObjectMetaResult(serde.ResultModel):
    """The result for the GetObjectMeta operation."""

    _attribute_map = {
        "content_length": {"tag": "output", "position": "header", "rename": "Content-Length", "type": "int"},
        "etag": {"tag": "output", "position": "header", "rename": "ETag"},
        "last_modified": {"tag": "output", "position": "header", "rename": "Last-Modified", "type": "datetime,httptime"},
        "last_access_time": {"tag": "output", "position": "header", "rename": "x-oss-last-access-time", "type": "datetime,httptime"},
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "hash_crc64": {"tag": "output", "position": "header", "rename": "x-oss-hash-crc64ecma"},
        'transition_time': {'tag': 'output', 'position': 'header', 'rename': 'x-oss-transition-time'},
    }

    def __init__(
        self,
        content_length: Optional[int] = None,
        etag: Optional[str] = None,
        last_modified: Optional[datetime.datetime] = None,
        last_access_time: Optional[datetime.datetime] = None,
        version_id: Optional[str] = None,
        hash_crc64: Optional[str] = None,
        transition_time: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            content_length (int, optional): Size of the body in bytes.
            etag (str, optional): The entity tag (ETag).
                An ETag is created when an object is created to identify the content of the object.
            last_modified (datetime.datetime, optional): The time when the returned objects were last modified.
            last_access_time (datetime.datetime, optional): The time when the object was last accessed.
            version_id (str, optional): Version of the object.
            hash_crc64 (str, optional): The 64-bit CRC value of the object.
                This value is calculated based on the ECMA-182 standard.
            transition_time (str, optional): The time when the storage class of the object is converted to Cold Archive or Deep Cold Archive based on lifecycle rules.
        """
        super().__init__(**kwargs)
        self.content_length = content_length
        self.etag = etag
        self.last_modified = last_modified
        self.last_access_time = last_access_time
        self.version_id = version_id
        self.hash_crc64 = hash_crc64
        self.transition_time = transition_time

class JobParameters(serde.Model):
    """
    The container that stores the restoration priority configuration. This configuration takes effect only when the request is sent to restore Cold Archive objects. If you do not specify the JobParameters parameter, the default restoration priority Standard is used.
    """

    _attribute_map = {
        'tier': {'tag': 'xml', 'rename': 'Tier', 'type': 'str'},
    }

    _xml_map = {
        'name': 'JobParameters'
    }

    def __init__(
        self,
        tier: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        tier (str, optional): The restoration priority. Valid values:*   Expedited: The object is restored within 1 hour.*   Standard: The object is restored within 2 to 5 hours.*   Bulk: The object is restored within 5 to 12 hours.
        """
        super().__init__(**kwargs)
        self.tier = tier


class RestoreRequest(serde.Model):
    """The configuration information about the RestoreObject request."""


    _attribute_map = {
        'days': {'tag': 'xml', 'rename': 'Days', 'type': 'int'},
        'job_parameters': {'tag': 'xml', 'rename': 'JobParameters', 'type': 'JobParameters'},
    }

    _xml_map = {
        'name': 'RestoreRequest'
    }

    _dependency_map = {
        'JobParameters': {'new': lambda: JobParameters()},
    }

    def __init__(
        self,
        days: Optional[int] = None,
        job_parameters: Optional[JobParameters] = None,
        tier: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            days (int, optional): The duration in which the object can remain in the restored state. Unit: days. Valid values: 1 to 7.
            job_parameters (JobParameters, optional): The container that stores the restoration priority coniguration. This configuration takes effect only when the request is sent to restore Cold Archive objects. If you do not specify the JobParameters parameter, the default restoration priority Standard is used.
            tier (str, optional): [DEPRECATED] This parameter is deprecated and will be removed in future versions. Use job_parameters instead.
                      The restoration priority of Cold Archive or Deep Cold Archive objects. Valid values:Expedited,Standard,Bulk
        """
        super().__init__(**kwargs)
        self.days = days
        self.job_parameters = job_parameters
        self.tier = tier
        if tier is not None:
            self.job_parameters = JobParameters(tier=tier)



class RestoreObjectRequest(serde.RequestModel):
    """The request for the RestoreObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "restore_request": {"tag": "input", "position": "body", "rename": "RestoreRequest", "type": "xml"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        restore_request: Optional[RestoreRequest] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the source object.
            restore_request (RestoreRequest, optional): The container that stores information about the RestoreObject request.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.restore_request = restore_request
        self.request_payer = request_payer


class RestoreObjectResult(serde.ResultModel):
    """The result for the RestoreObject operation."""

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "restore_priority": {"tag": "output", "position": "header", "rename": "x-oss-object-restore-priority"},
    }

    def __init__(
        self,
        version_id: Optional[str] = None,
        restore_priority: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
            restore_priority (str, optional): The restoration priority.
                This header is displayed only for the Cold Archive or Deep Cold Archive object in the restored state.
        """
        super().__init__(**kwargs)
        self.version_id = version_id
        self.restore_priority = restore_priority


class PutObjectAclRequest(serde.RequestModel):
    """The request for the PutObjectAcl operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "acl": {"tag": "input", "position": "header", "rename": "x-oss-object-acl", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        acl: Optional[str] = None,
        version_id: Optional[str] = None,
        request_payer: Optional[str] = None,
        object_acl: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            acl (str, required): The access control list (ACL) of the object.
            version_id (str, optional): The version ID of the source object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs
            object_acl (str, optional): The access control list (ACL) of the object.
                The object_acl parameter has the same functionality as the acl parameter. it is the standardized name for acl.
                If both exist simultaneously, the value of object_acl will take precedence.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.acl = object_acl if object_acl is not None else acl
        self.version_id = version_id
        self.request_payer = request_payer


class PutObjectAclResult(serde.ResultModel):
    """The result for the PutObjectAcl operation."""

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
    }

    def __init__(
        self,
        version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
        """
        super().__init__(**kwargs)
        self.version_id = version_id


class GetObjectAclRequest(serde.RequestModel):
    """The request for the GetObjectAcl operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the source object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.request_payer = request_payer


class GetObjectAclResult(serde.ResultModel):
    """The result for the GetObjectAcl operation."""

    _attribute_map = {
        "acl": {"tag": "xml", "rename": "AccessControlList/Grant"},
        "owner": {"tag": "xml", "rename": "Owner", "type": "Owner"},
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
    }

    _dependency_map = {
        "Owner": {"new": lambda: Owner()},
    }

    _xml_map = {
        "name": "AccessControlPolicy"
    }

    def __init__(
        self,
        acl: Optional[str] = None,
        owner: Optional[Owner] = None,
        version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            acl (str, optional): The ACL of the object. Default value: default.
            owner (Owner, optional): The container that stores information about the object owner.
            version_id (str, optional): Version of the object.
        """
        super().__init__(**kwargs)
        self.acl = acl
        self.owner = owner
        self.version_id = version_id

class InitiateMultipartUploadRequest(serde.RequestModel):
    """The request for the InitiateMultipartUpload operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "encoding_type": {"tag": "input", "position": "query", "rename": "encoding-type"},
        "storage_class": {"tag": "input", "position": "header", "rename": "x-oss-storage-class"},
        "metadata": {"tag": "input", "position": "header", "rename": "x-oss-meta-", "type": "dict,usermeta"},
        "cache_control": {"tag": "input", "position": "header", "rename": "Cache-Control"},
        "content_disposition": {"tag": "input", "position": "header", "rename": "Content-Disposition"},
        "content_encoding": {"tag": "input", "position": "header", "rename": "Content-Encoding"},
        "content_length": {"tag": "input", "position": "header", "rename": "Content-Length", "type": "int"},
        "content_md5": {"tag": "input", "position": "header", "rename": "Content-MD5"},
        "content_type": {"tag": "input", "position": "header", "rename": "Content-Type"},
        "expires": {"tag": "input", "position": "header", "rename": "Expires"},
        "server_side_encryption": {"tag": "input", "position": "header", "rename": "x-oss-server-side-encryption"},
        "server_side_data_encryption": {"tag": "input", "position": "header", "rename": "x-oss-server-side-data-encryption"},
        "server_side_encryption_key_id": {"tag": "input", "position": "header", "rename": "x-oss-server-side-encryption-key-id"},
        "tagging": {"tag": "input", "position": "header", "rename": "x-oss-tagging"},
        "forbid_overwrite": {"tag": "input", "position": "header", "rename": "x-oss-forbid-overwrite", "type": "bool"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
        "cse_data_size": {},
        "cse_part_size": {},
        "disable_auto_detect_mime_type": {},
    }
    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        encoding_type: Optional[str] = None,
        storage_class: Optional[str] = None,
        metadata: Optional[MutableMapping] = None,
        cache_control: Optional[str] = None,
        content_disposition: Optional[str] = None,
        content_encoding: Optional[str] = None,
        content_length: Optional[int] = None,
        content_md5: Optional[str] = None,
        content_type: Optional[str] = None,
        expires: Optional[str] = None,
        server_side_encryption: Optional[str] = None,
        server_side_data_encryption: Optional[str] = None,
        server_side_encryption_key_id: Optional[str] = None,
        tagging: Optional[str] = None,
        forbid_overwrite: Optional[Union[str, bool]] = None,
        request_payer: Optional[str] = None,
        cse_data_size: Optional[int] = None,
        cse_part_size: Optional[int] = None,
        disable_auto_detect_mime_type: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            encoding_type (str, optional): The encoding type of the object names in the response. Valid value: url
            storage_class (str, optional): The storage class of the object.
            metadata (MutableMapping,The metadata of the object that you want to upload.
            cache_control (str, optional): The caching behavior of the web page when the object is downloaded.
            content_disposition (str, optional): The method that is used to access the object.
            content_encoding (str, optional): The method that is used to encode the object.
            content_length (int, optional): The size of the data in the HTTP message body. Unit: bytes.
            content_md5 (str, optional): The MD5 hash of the object that you want to upload.
            content_type (str, optional): A standard MIME type describing the format of the contents.
            expires (str, optional): The expiration time of the cache in UTC.
            server_side_encryption (str, optional): The encryption method on the server side when an object is created.
                Valid values: AES256 and KMS
            server_side_data_encryption (str, optional): The ID of the customer master key (CMK)
                that is managed by Key Management Service (KMS). This header is valid only
                when the x-oss-server-side-encryption header is set to KMS.
            server_side_encryption_key_id (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            tagging (str, optional): The tags that are specified for the object by using a key-value pair.
                You can specify multiple tags for an object. Example: TagA=A&TagB=B.
            forbid_overwrite (Union[str, bool], optional): Specifies whether the object that is uploaded by calling the PutObject operation
                overwrites an existing object that has the same name.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
            cse_data_size (int, optional): The total size when using client side encryption.
                Only valid in EncryptionClient.
            cse_part_size (int, optional): The part size when using client side encryption.
                Only valid in EncryptionClient.
                It must be aligned to the secret iv length.
            disable_auto_detect_mime_type (bool, optional): To disable the feature that Content-Type is automatically added based on the object name if not specified.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.encoding_type = encoding_type
        self.storage_class = storage_class
        self.metadata = metadata
        self.cache_control = cache_control
        self.content_disposition = content_disposition
        self.content_encoding = content_encoding
        self.content_length = content_length
        self.content_md5 = content_md5
        self.content_type = content_type
        self.expires = expires
        self.server_side_encryption = server_side_encryption
        self.server_side_data_encryption = server_side_data_encryption
        self.server_side_encryption_key_id = server_side_encryption_key_id
        self.tagging = tagging
        self.forbid_overwrite = forbid_overwrite
        self.request_payer = request_payer
        self.cse_data_size = cse_data_size
        self.cse_part_size = cse_part_size
        self.disable_auto_detect_mime_type = disable_auto_detect_mime_type

class InitiateMultipartUploadResult(serde.ResultModel):
    """The result for the InitiateMultipartUpload operation."""

    _attribute_map = {
        "bucket": {"tag": "xml", "rename": "Bucket"},
        "key": {"tag": "xml", "rename": "Key"},
        "upload_id": {"tag": "xml", "rename": "UploadId"},
        "encoding_type": {"tag": "xml", "rename": "EncodingType"},
        "cse_multipart_context": {},
    }

    _xml_map = {
        "name": "InitiateMultipartUploadResult"
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        upload_id: Optional[str] = None,
        encoding_type: Optional[str] = None,
        cse_multipart_context: Optional[Any] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket to which the object is uploaded by the multipart upload task.
            key (str, optional): The name of the object that is uploaded by the multipart upload task.
            upload_id (str, optional): The upload ID that uniquely identifies the multipart upload task.
            encoding_type (str, optional): The encoding type of the object names in the response. Valid value: url
            cse_multipart_context (Any, optional): The encryption context for multipart upload when using client side encryption,
                only valid in EncryptionClient
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id
        self.encoding_type = encoding_type
        self.cse_multipart_context = cse_multipart_context

class UploadPartRequest(serde.RequestModel):
    """The request for the UploadPart operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "part_number": {"tag": "input", "position": "query", "rename": "partNumber", "required": True},
        "upload_id": {"tag": "input", "position": "query", "rename": "uploadId", "required": True},
        "content_md5": {"tag": "input", "position": "header", "rename": "Content-MD5"},
        "content_length": {"tag": "input", "position": "header", "rename": "Content-Length", "type": "int"},
        "traffic_limit": {"tag": "input", "position": "header", "rename": "x-oss-traffic-limit", "type": "int"},
        "body": {"tag": "input", "position": "body"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
        "progress_fn": {},
        "cse_multipart_context": {},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        part_number: int = None,
        upload_id: str = None,
        content_md5: Optional[str] = None,
        content_length: Optional[int] = None,
        traffic_limit: Optional[int] = None,
        body: Optional[BodyType] = None,
        request_payer: Optional[str] = None,
        progress_fn: Optional[Any] = None,
        cse_multipart_context: Optional[Any] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            part_number (int, required): Each uploaded part is identified by a number, Value: 1-10000.
                The size limit of a single part is between 100 KB and 5 GB.
            upload_id (str, required): The ID of the multipart upload task.
            content_md5 (str, optional): The MD5 hash of the object that you want to upload.
            content_length (int, optional): The size of the data in the HTTP message body. Unit: bytes.
            traffic_limit (str, optional): Specify the speed limit value. The speed limit value ranges from  245760 to 838860800, with a unit of bit/s.
            body (str, optional): Object data.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
            progress_fn (str, optional): Progress callback function.
            cse_multipart_context (Any, optional): The encryption context for multipart upload when using client side encryption.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.part_number = part_number
        self.upload_id = upload_id
        self.content_md5 = content_md5
        self.content_length = content_length
        self.traffic_limit = traffic_limit
        self.body = body
        self.request_payer = request_payer
        self.progress_fn = progress_fn
        self.cse_multipart_context = cse_multipart_context


class UploadPartResult(serde.ResultModel):
    """The result for the UploadPart operation."""

    _attribute_map = {
        "content_md5": {"tag": "output", "position": "header", "rename": "Content-MD5"},
        "etag": {"tag": "output", "position": "header", "rename": "ETag"},
        "hash_crc64": {"tag": "output", "position": "header", "rename": "x-oss-hash-crc64ecma"},
    }

    def __init__(
        self,
        content_md5: Optional[str] = None,
        etag: Optional[str] = None,
        hash_crc64: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            content_md5 (str, optional): Entity tag for the uploaded part.
            etag (str, optional): The MD5 hash of the part that you want to upload.
            hash_crc64 (str, optional): The 64-bit CRC value of the part.
                This value is calculated based on the ECMA-182 standard.
        """
        super().__init__(**kwargs)
        self.content_md5 = content_md5
        self.etag = etag
        self.hash_crc64 = hash_crc64

class UploadPartCopyRequest(serde.RequestModel):
    """The request for the UploadPartCopy operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "part_number": {"tag": "input", "position": "query", "rename": "partNumber", "required": True},
        "upload_id": {"tag": "input", "position": "query", "rename": "uploadId", "required": True},
        "source_bucket": {"tag": "input", "position": "nop"},
        "source_key": {"tag": "input", "position": "nop", "required": True},
        "source_version_id": {"tag": "input", "position": "nop"},
        "source_range": {"tag": "input", "position": "header", "rename": "x-oss-copy-source-range"},
        "if_match": {"tag": "input", "position": "header", "rename": "x-oss-copy-source-if-match"},
        "if_none_match": {"tag": "input", "position": "header", "rename": "x-oss-copy-source-if-none-match"},
        "if_modified_since": {"tag": "input", "position": "header", "rename": "x-oss-copy-source-if-modified-since"},
        "if_unmodified_since": {"tag": "input", "position": "header", "rename": "x-oss-copy-source-if-unmodified-since"},
        "traffic_limit": {"tag": "input", "position": "header", "rename": "x-oss-traffic-limit", "type": "int"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        part_number: Optional[int] = None,
        upload_id: Optional[str] = None,
        source_bucket: Optional[str] = None,
        source_key: Optional[str] = None,
        source_version_id: Optional[str] = None,
        source_range: Optional[str] = None,
        if_match: Optional[str] = None,
        if_none_match: Optional[str] = None,
        if_modified_since: Optional[str] = None,
        if_unmodified_since: Optional[str] = None,
        traffic_limit: Optional[int] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            part_number (int, optional): Each uploaded part is identified by a number, Value: 1-10000.
                The size limit of a single part is between 100 KB and 5 GB.
            upload_id (str, optional): The ID of the multipart upload task.
            source_bucket (str, optional): The name of the source bucket.
            source_key (str, required): The name of the source object.
            source_version_id (str, optional): The version ID of the source object.
            source_range (str, optional): The range of bytes to copy data from the source object.
            if_match (str, optional): Specifies whether the object that is uploaded by
                calling the CopyObject operation overwrites an existing object that has the same name.
                Valid values: true and false
            if_none_match (str, optional): If the ETag specified in the request does not match the ETag value of the object,
                the object and 200 OK are returned. Otherwise, 304 Not Modified is returned.
            if_modified_since (str, optional): If the time specified in this header is earlier than 
                the object modified time or is invalid, the object and 200 OK are returned.
                Otherwise, 304 Not Modified is returned. The time must be in GMT. Example: Fri, 13 Nov 2015 14:47:53 GMT.
            if_unmodified_since (str, optional): If the time specified in this header is the same as or later than
                the object modified time, the object and 200 OK are returned. Otherwise, 412 Precondition Failed is returned.
                The time must be in GMT. Example: Fri, 13 Nov 2015 14:47:53 GMT.
            traffic_limit (str, optional): Specify the speed limit value. The speed limit value ranges from  245760 to 838860800, with a unit of bit/s.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.part_number = part_number
        self.upload_id = upload_id
        self.source_bucket = source_bucket
        self.source_key = source_key
        self.source_version_id = source_version_id
        self.source_range = source_range
        self.if_match = if_match
        self.if_none_match = if_none_match
        self.if_modified_since = if_modified_since
        self.if_unmodified_since = if_unmodified_since
        self.traffic_limit = traffic_limit
        self.request_payer = request_payer


class UploadPartCopyResult(serde.ResultModel):
    """The result for the UploadPartCopy operation."""

    _attribute_map = {
        "last_modified": {"tag": "xml", "rename": "LastModified", "type": "datetime"},
        "etag": {"tag": "xml", "rename": "ETag"},
        "source_version_id": {"tag": "output", "position": "header", "rename": "x-oss-copy-source-version-id"},
    }

    _xml_map = {
        "name": "CopyPartResult"
    }

    def __init__(
        self,
        last_modified: Optional[datetime.datetime] = None,
        etag: Optional[str] = None,
        source_version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            last_modified (datetime, optional): The time when the returned objects were last modified.
            etag (str, optional): Entity tag for the uploaded part.
            source_version_id (str, optional): The version ID of the source object.
        """
        super().__init__(**kwargs)
        self.last_modified = last_modified
        self.etag = etag
        self.source_version_id = source_version_id


class UploadPart(serde.Model):
    """The inforamtion about the content of the Part."""

    def __init__(
        self,
        part_number: Optional[int] = None,
        etag: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            part_number (int, optional): The number of parts.
            etag (str, optional): The ETag values that are returned by OSS after parts are uploaded.
        """
        super().__init__(**kwargs)
        self.part_number = part_number
        self.etag = etag

    _attribute_map = {
        "part_number": {"tag": "xml", "rename": "PartNumber"},
        "etag": {"tag": "xml", "rename": "ETag"},
    }
    _xml_map = {
        "name": "Part"
    }


class CompleteMultipartUpload(serde.Model):
    """The container that stores the information about the uploaded parts."""

    def __init__(
        self,
        parts: Optional[List[UploadPart]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            parts ([UploadPart], optional): The uploaded parts.
        """
        super().__init__(**kwargs)
        self.parts = parts

    _attribute_map = {
        "parts": {"tag": "xml", "rename": "Part"},
    }
    _xml_map = {
        "name": "CompleteMultipartUpload"
    }


class CompleteMultipartUploadRequest(serde.RequestModel):
    """The request for the CompleteMultipartUpload operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "upload_id": {"tag": "input", "position": "query", "rename": "uploadId", "required": True},
        "acl": {"tag": "input", "position": "header", "rename": "x-oss-object-acl"},
        "complete_multipart_upload": {"tag": "input", "position": "body", "rename": "CompleteMultipartUpload", "type": "xml"},
        "complete_all": {"tag": "input", "position": "header", "rename": "x-oss-complete-all"},
        "callback": {"tag": "input", "position": "header", "rename": "x-oss-callback"},
        "callback_var": {"tag": "input", "position": "header", "rename": "x-oss-callback-var"},
        "forbid_overwrite": {"tag": "input", "position": "header", "rename": "x-oss-forbid-overwrite", "type": "bool"},
        "encoding_type": {"tag": "input", "position": "query", "rename": "encoding-type"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        upload_id: str = None,
        acl: Optional[str] = None,
        complete_multipart_upload: Optional[CompleteMultipartUpload] = None,
        complete_all: Optional[str] = None,
        callback: Optional[str] = None,
        callback_var: Optional[str] = None,
        forbid_overwrite: Optional[Union[str, bool]] = None,
        encoding_type: Optional[str] = None,
        request_payer: Optional[str] = None,
        object_acl: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            upload_id (str, optional): The ID of the multipart upload task.
            acl (str, optional): The access control list (ACL) of the object.
            complete_multipart_upload (CompleteMultipartUpload, optional): The container that stores the content of the CompleteMultipartUpload
            complete_all (str, optional): Specifies whether to list all parts that are uploaded by using the current upload ID.
                Valid value: yes
            callback (str, optional): A callback parameter is a Base64-encoded string that contains multiple fields in the JSON format.
            callback_var (str, optional): Configure custom parameters by using the callback-var parameter.
            forbid_overwrite (Union[str, bool], optional): Specifies whether the object that is uploaded by calling the PutObject operation
                overwrites an existing object that has the same name.
            encoding_type (str, optional): The encoding type of the object names in the response. Valid value: url.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
            object_acl (str, optional): The access control list (ACL) of the object.
                The object_acl parameter has the same functionality as the acl parameter. it is the standardized name for acl.
                If both exist simultaneously, the value of object_acl will take precedence.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id
        self.acl = object_acl if object_acl is not None else acl
        self.complete_multipart_upload = complete_multipart_upload
        self.complete_all = complete_all
        self.callback = callback
        self.callback_var = callback_var
        self.forbid_overwrite = forbid_overwrite
        self.encoding_type = encoding_type
        self.request_payer = request_payer


class CompleteMultipartUploadResult(serde.ResultModel):
    """The result for the CompleteMultipartUpload operation."""

    _attribute_map = {
        "bucket": {"tag": "xml", "rename": "Bucket"},
        "key": {"tag": "xml", "rename": "Key"},
        "location": {"tag": "xml", "rename": "Location"},
        "etag": {"tag": "xml", "rename": "ETag"},
        "encoding_type": {"tag": "xml", "rename": "EncodingType"},
        "hash_crc64": {"tag": "output", "position": "header", "rename": "x-oss-hash-crc64ecma"},
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "callback_result": {"tag": "output", "position": "body", "type": "dict,json"},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        location: Optional[str] = None,
        etag: Optional[str] = None,
        encoding_type: Optional[str] = None,
        hash_crc64: Optional[str] = None,
        version_id: Optional[str] = None,
        callback_result: Optional[Dict] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            key (str, optional): The name of the uploaded object.
            location (str, optional): The URL that is used to access the uploaded object.
            etag (str, optional): The ETag that is generated when an object is created.
                ETags are used to identify the content of objects.
            encoding_type (str, optional): The encoding type of the name of the deleted object in the response.
                If encoding-type is specified in the request, the object name is encoded in the returned result.
            hash_crc64 (str, optional): The 64-bit CRC value of the object.
                This value is calculated based on the ECMA-182 standard.
            version_id (str, optional): Version of the object.
            callback_result (dict, optional): Callback result, 
                it is valid only when the callback is set.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.location = location
        self.etag = etag
        self.encoding_type = encoding_type
        self.hash_crc64 = hash_crc64
        self.version_id = version_id
        self.callback_result = callback_result


class AbortMultipartUploadRequest(serde.RequestModel):
    """The request for the AbortMultipartUpload operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "upload_id": {"tag": "input", "position": "query", "rename": "uploadId", "required": True},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        upload_id: str = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            upload_id (str, optional): The ID of the multipart upload task.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id
        self.request_payer = request_payer


class AbortMultipartUploadResult(serde.ResultModel):
    """The result for the AbortMultipartUpload operation."""


class ListMultipartUploadsRequest(serde.RequestModel):
    """The request for the ListMultipartUploads operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "delimiter": {"tag": "input", "position": "query", "rename": "delimiter"},
        "encoding_type": {"tag": "input", "position": "query", "rename": "encoding-type"},
        "key_marker": {"tag": "input", "position": "query", "rename": "key-marker"},
        "max_uploads": {"tag": "input", "position": "query", "rename": "max-uploads", "type": "int"},
        "prefix": {"tag": "input", "position": "query", "rename": "prefix"},
        "upload_id_marker": {"tag": "input", "position": "query", "rename": "upload-id-marker"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        delimiter: Optional[str] = None,
        encoding_type: Optional[str] = None,
        key_marker: Optional[str] = None,
        max_uploads: Optional[int] = None,
        prefix: Optional[str] = None,
        upload_id_marker: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket to create.
            delimiter (str, optional): The character that is used to group objects by name. 
                If you specify the delimiter parameter in the request, the response contains 
                the CommonPrefixes parameter. The objects whose names contain the same string
                from the prefix to the next occurrence of the delimiter are grouped 
                as a single result element in CommonPrefixes.
            encoding_type (str, optional): The encoding type of the content in the response. Valid value: url
            key_marker (str, optional): This parameter is used together with the upload-id-marker parameter to specify
                the position from which the next list begins.
            max_uploads (int, optional): The maximum number of multipart upload tasks that can be returned for the current request.
                Default value: 1000. Maximum value: 1000.
            prefix (str, optional): The prefix that the names of the returned objects must contain.
            upload_id_marker (str, optional): The upload ID of the multipart upload task after which the list begins.
                This parameter is used together with the key-marker parameter.
            request_payer (str, optional): To indicate that the requester is aware that the request 
                and data download will incur costs
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.delimiter = delimiter
        self.encoding_type = encoding_type
        self.key_marker = key_marker
        self.max_uploads = max_uploads
        self.prefix = prefix
        self.upload_id_marker = upload_id_marker
        self.request_payer = request_payer


class Upload(serde.Model):
    """The inforamtion about the upload task was initiated."""

    def __init__(
        self,
        key: Optional[str] = None,
        upload_id: Optional[str] = None,
        initiated: Optional[datetime.datetime] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The name of the object for which a multipart upload task was initiated.
            upload_id (str, optional): The ID of the multipart upload task.
            initiated (str, optional): The time when the multipart upload task was initialized.
        """
        super().__init__(**kwargs)
        self.key = key
        self.upload_id = upload_id
        self.initiated = initiated

    _attribute_map = {
        "key": {"tag": "xml", "rename": "Key"},
        "upload_id": {"tag": "xml", "rename": "UploadId"},
        "initiated": {"tag": "xml", "rename": "Initiated", "type": "datetime"},
    }
    _xml_map = {
        "name": "Upload"
    }


class ListMultipartUploadsResult(serde.ResultModel):
    """The result for the ListMultipartUploads operation."""

    _attribute_map = {
        "encoding_type": {"tag": "xml", "rename": "EncodingType"},
        "bucket": {"tag": "xml", "rename": "Bucket"},
        "key_marker": {"tag": "xml", "rename": "KeyMarker"},
        "upload_id_marker": {"tag": "xml", "rename": "UploadIdMarker"},
        "next_key_marker": {"tag": "xml", "rename": "NextKeyMarker"},
        "next_upload_id_marker": {"tag": "xml", "rename": "NextUploadIdMarker"},
        "delimiter": {"tag": "xml", "rename": "Delimiter"},
        "prefix": {"tag": "xml", "rename": "Prefix"},
        "max_uploads": {"tag": "xml", "rename": "MaxUploads", "type": "int"},
        "is_truncated": {"tag": "xml", "rename": "IsTruncated", "type": "bool"},
        "uploads": {"tag": "xml", "rename": "Upload", "type": "[Upload]"},
    }

    _dependency_map = {
        "Upload": {"new": lambda: Upload()},
    }

    _xml_map = {"name":"ListMultipartUploadsResult"}

    def __init__(
        self,
        encoding_type: Optional[str] = None,
        bucket: Optional[str] = None,
        key_marker: Optional[str] = None,
        upload_id_marker: Optional[str] = None,
        next_key_marker: Optional[str] = None,
        next_upload_id_marker: Optional[str] = None,
        delimiter: Optional[str] = None,
        prefix: Optional[str] = None,
        max_uploads: Optional[int] = None,
        is_truncated: Optional[bool] = None,
        uploads: Optional[List[Upload]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            encoding_type (str, optional): The method used to encode the object name in the response.
                If encoding-type is specified in the request, values of those elements including
                Delimiter, KeyMarker, Prefix, NextKeyMarker, and Key are encoded in the returned result.
            bucket (str, optional): The name of the bucket.
            key_marker (str, optional): The name of the object that corresponds to the multipart upload task after which the list begins.
            upload_id_marker (str, optional): The upload ID of the multipart upload task after which the list begins.
            next_key_marker (str, optional): The upload ID of the multipart upload task after which the list begins.
            next_upload_id_marker (str, optional): The NextUploadMarker value that is used for the UploadMarker value in
                the next request if the response does not contain all required results.
            delimiter (str, optional): The character that is used to group objects by name.
            prefix (str, optional): The prefix contained in the returned object names.
            max_uploads (int, optional): The maximum number of multipart upload tasks returned by OSS.
            is_truncated (bool, optional): Indicates whether the returned results are truncated.
                true indicates that not all results are returned this time.
                false indicates that all results are returned this time.
            uploads ([Upload], optional): The container that stores information about upload task.
        """
        super().__init__(**kwargs)
        self.encoding_type = encoding_type
        self.bucket = bucket
        self.key_marker = key_marker
        self.upload_id_marker = upload_id_marker
        self.next_key_marker = next_key_marker
        self.next_upload_id_marker = next_upload_id_marker
        self.delimiter = delimiter
        self.prefix = prefix
        self.max_uploads = max_uploads
        self.is_truncated = is_truncated
        self.uploads = uploads

class ListPartsRequest(serde.RequestModel):
    """The request for the ListParts operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "upload_id": {"tag": "input", "position": "query", "rename": "uploadId", "required": True},
        "encoding_type": {"tag": "input", "position": "query", "rename": "encoding-type"},
        "max_parts": {"tag": "input", "position": "query", "rename": "max-parts", "type": "int"},
        "part_number_marker": {"tag": "input", "position": "query", "rename": "part-number-marker"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        upload_id: str = None,
        encoding_type: Optional[str] = None,
        max_parts: Optional[int] = None,
        part_number_marker: Optional[Union[str, int]] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            upload_id (str, required): The ID of the multipart upload task.
            encoding_type (str, optional): The encoding type of the content in the response. Valid value: url
            max_parts (int, optional): The maximum number of parts that can be returned by OSS.
                Default value: 1000. Maximum value: 1000.
            part_number_marker (Union[str, int], optional): The position from which the list starts.
                All parts whose part numbers are greater than the value of this parameter are listed.
            request_payer (str, optional): To indicate that the requester is aware that the request 
                and data download will incur costs
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id
        self.encoding_type = encoding_type
        self.max_parts = max_parts
        self.part_number_marker = part_number_marker
        self.request_payer = request_payer


class Part(serde.Model):
    """The inforamtion about the uploaded part."""

    def __init__(
        self,
        part_number: Optional[int] = None,
        etag: Optional[str] = None,
        last_modified: Optional[datetime.datetime] = None,
        size: Optional[int] = None,
        hash_crc64: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            part_number (int, optional): The number that identifies a part.
            etag (str, optional): The ETag value of the content of the uploaded part.
            last_modified (datetime, optional): The time when the part was uploaded.
            size (int, optional): The size of the uploaded parts.
            hash_crc64 (str, optional): The 64-bit CRC value of the object.
                This value is calculated based on the ECMA-182 standard.
        """
        super().__init__(**kwargs)
        self.part_number = part_number
        self.etag = etag
        self.last_modified = last_modified
        self.size = size
        self.hash_crc64 = hash_crc64

    _attribute_map = {
        "part_number": {"tag": "xml", "rename": "PartNumber", "type": "int"},
        "etag": {"tag": "xml", "rename": "ETag"},
        "last_modified": {"tag": "xml", "rename": "LastModified", "type": "datetime"},
        "size": {"tag": "xml", "rename": "Size", "type": "int"},
        "hash_crc64": {"tag": "xml", "rename": "HashCrc64ecma"},
    }
    _xml_map = {
        "name": "Part"
    }


class ListPartsResult(serde.ResultModel):
    """The result for the ListParts operation."""

    _attribute_map = {
        "encoding_type": {"tag": "xml", "rename": "EncodingType"},
        "bucket": {"tag": "xml", "rename": "Bucket"},
        "key": {"tag": "xml", "rename": "Key"},
        "upload_id": {"tag": "xml", "rename": "UploadId"},
        "part_number_marker": {"tag": "xml", "rename": "PartNumberMarker", "type": "int"},
        "next_part_number_marker": {"tag": "xml", "rename": "NextPartNumberMarker", "type": "int"},
        "max_parts": {"tag": "xml", "rename": "MaxParts", "type": "int"},
        "is_truncated": {"tag": "xml", "rename": "IsTruncated", "type": "bool"},
        "storage_class": {"tag": "xml", "rename": "StorageClass"},
        "client_encryption_key": {"tag": "xml", "rename": "ClientEncryptionKey"},
        "client_encryption_start": {"tag": "xml", "rename": "ClientEncryptionStart"},
        "client_encryption_cek_alg": {"tag": "xml", "rename": "ClientEncryptionCekAlg"},
        "client_encryption_wrap_alg": {"tag": "xml", "rename": "ClientEncryptionWrapAlg"},
        "client_encryption_data_size": {"tag": "xml", "rename": "ClientEncryptionDataSize", "type": "int"},
        "client_encryption_part_size": {"tag": "xml", "rename": "ClientEncryptionPartSize", "type": "int"},
        "parts": {"tag": "xml", "rename": "Part", "type": "[Part]"},
    }

    _dependency_map = {
        "Part": {"new": lambda: Part()},
    }

    _xml_map = {"name":"ListPartsResult"}

    def __init__(
        self,
        encoding_type: Optional[str] = None,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        upload_id: Optional[str] = None,
        part_number_marker: Optional[int] = None,
        next_part_number_marker: Optional[int] = None,
        max_parts: Optional[int] = None,
        is_truncated: Optional[bool] = None,
        storage_class: Optional[str] = None,
        client_encryption_key: Optional[str] = None,
        client_encryption_start: Optional[str] = None,
        client_encryption_cek_alg: Optional[str] = None,
        client_encryption_wrap_alg: Optional[str] = None,
        client_encryption_data_size: Optional[int] = None,
        client_encryption_part_size: Optional[int] = None,
        parts: Optional[List[Part]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            encoding_type (str, optional): The method used to encode the object name in the response.
                If encoding-type is specified in the request, values of those elements including
                Key are encoded in the returned result.
            bucket (str, optional): The name of the bucket.
            key (str, optional): The name of the object that corresponds to the multipart upload task after which the list begins.
            upload_id (str, optional): The ID of the upload task.
            part_number_marker (int, optional): The position from which the list starts.
                All parts whose part numbers are greater than the value of this parameter are listed.
            next_part_number_marker (int, optional): The NextPartNumberMarker value that is used for the PartNumberMarker value
                in a subsequent request when the response does not contain all required results.
            max_parts (int, optional): The maximum number of parts in the response.
            is_truncated (bool, optional): Indicates whether the returned results are truncated.
                true indicates that not all results are returned this time.
                false indicates that all results are returned this time.
            storage_class (str, optional): The storage class of the object.
            client_encryption_key (str, optional): The encrypted data key.
                The encrypted data key is a string encrypted by a customer master key and encoded in Base64.
                Only available in client-side encryption.
            client_encryption_start (str, optional): The initial value that is randomly generated for data encryption.
                The initial value is is a string encrypted by a customer master key and encoded in Base64.
                Only available in client-side encryption.
            client_encryption_cek_alg (str, optional): The algorithm used to encrypt data.
                Only available in client-side encryption.
            client_encryption_wrap_alg (str, optional): The algorithm used to encrypt the data key.
                Only available in client-side encryption.
            client_encryption_data_size (str, optional): The total size of the data to encrypt for multipart upload when init_multipart is called.
                Only available in client-side encryption.
            client_encryption_part_size (str, optional): The size of each part to encrypt for multipart upload when init_multipart is called.
                Only available in client-side encryption.
            parts ([Part], optional): The container that stores information about uploaded part.
        """
        super().__init__(**kwargs)
        self.encoding_type = encoding_type
        self.bucket = bucket
        self.key = key
        self.upload_id = upload_id
        self.part_number_marker = part_number_marker
        self.next_part_number_marker = next_part_number_marker
        self.max_parts = max_parts
        self.is_truncated = is_truncated
        self.storage_class = storage_class
        self.client_encryption_key = client_encryption_key
        self.client_encryption_start = client_encryption_start
        self.client_encryption_cek_alg = client_encryption_cek_alg
        self.client_encryption_wrap_alg = client_encryption_wrap_alg
        self.client_encryption_data_size = client_encryption_data_size
        self.client_encryption_part_size = client_encryption_part_size
        self.parts = parts


class PutSymlinkRequest(serde.RequestModel):
    """The request for the PutSymlink operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "target": {"tag": "input", "position": "header", "rename": "x-oss-symlink-target", "required": True},
        "acl": {"tag": "input", "position": "header", "rename": "x-oss-object-acl"},
        "storage_class": {"tag": "input", "position": "header", "rename": "x-oss-storage-class"},
        "metadata": {"tag": "input", "position": "header", "rename": "x-oss-meta-", "type": "dict,usermeta"},
        "forbid_overwrite": {"tag": "input", "position": "header", "rename": "x-oss-forbid-overwrite", "type": "bool"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        target: str = None,
        acl: Optional[str] = None,
        storage_class: Optional[str] = None,
        metadata: Optional[MutableMapping] = None,
        forbid_overwrite: Optional[Union[str, bool]] = None,
        request_payer: Optional[str] = None,
        object_acl: Optional[str] = None,
        symlink_target: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            target (str, required): The destination object to which the symbolic link points.
            acl (str, optional): The access control list (ACL) of the object.
            storage_class (str, optional): The storage class of the object.
            metadata (MutableMapping,The metadata of the object that you want to upload.
            forbid_overwrite (Union[str, bool], optional): Specifies whether the object that is uploaded by calling the PutObject operation
                overwrites an existing object that has the same name.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
            object_acl (str, optional): The access control list (ACL) of the object.
                The object_acl parameter has the same functionality as the acl parameter. it is the standardized name for acl.
                If both exist simultaneously, the value of object_acl will take precedence.
            symlink_target (str, optional): The destination object to which the symbolic link points.
                The symlink_target parameter has the same functionality as the target parameter. it is the standardized name for target.
                If both exist simultaneously, the value of symlink_target will take precedence.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.target = symlink_target if symlink_target is not None else target
        self.acl = object_acl if object_acl is not None else acl
        self.storage_class = storage_class
        self.metadata = metadata
        self.forbid_overwrite = forbid_overwrite
        self.request_payer = request_payer


class PutSymlinkResult(serde.ResultModel):
    """The result for the PutSymlink operation."""

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
    }

    def __init__(
        self,
        version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
        """
        super().__init__(**kwargs)
        self.version_id = version_id

class GetSymlinkRequest(serde.RequestModel):
    """The request for the GetSymlink operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): VersionId used to reference a specific version of the object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.request_payer = request_payer


class GetSymlinkResult(serde.ResultModel):
    """The result for the GetSymlink operation."""

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "target": {"tag": "output", "position": "header", "rename": "x-oss-symlink-target"},
        "etag": {"tag": "output", "position": "header", "rename": "ETag"},
        "metadata": {"tag": "output", "position": "header", "rename": "x-oss-meta-", "type": "dict,usermeta"},
    }

    def __init__(
        self,
        version_id: Optional[str] = None,
        target: Optional[str] = None,
        etag: Optional[str] = None,
        metadata: Optional[MutableMapping] = None,
        symlink_target: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
            target (str, optional): Indicates the target object that the symbol link directs to.
                This parameter is deprecated. Use 'symlink_target' parameter instead
            etag (str, optional): The entity tag (ETag).
                An ETag is created when an object is created to identify the content of the object.
            metadata (MutableMapping, optional): A map of metadata to store with the object.
            symlink_target (str, optional): The destination object to which the symbolic link points.
                The symlink_target parameter has the same functionality as the target parameter. it is the standardized name for target. 
                If both exist simultaneously, the value of symlink_target will take precedence.
        """
        super().__init__(**kwargs)
        self.version_id = version_id
        self.target = symlink_target if symlink_target is not None else target
        self.etag = etag
        self.metadata = metadata

class Tag(serde.Model):
    """The inforamtion about the tag."""

    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The key of the tag.
            value (str, optional): The value of the tag.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value

    _attribute_map = {
        "key": {"tag": "xml", "rename": "Key"},
        "value": {"tag": "xml", "rename": "Value"},
    }
    _xml_map = {
        "name": "Tag"
    }

class TagSet(serde.Model):
    """The collection of tags."""

    def __init__(
        self,
        tags: Optional[List[Tag]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            tags ([Tag], optional): A list of tags.
        """
        super().__init__(**kwargs)
        self.tags = tags

    _attribute_map = {
        "tags": {"tag": "xml", "rename": "Tag", "type": "[Tag]"},
    }

    _dependency_map = {
        "Tag": {"new": lambda: Tag()},
    }

    _xml_map = {
        "name": "TagSet"
    }

class Tagging(serde.Model):
    """The container used to store the collection of tags."""

    def __init__(
        self,
        tag_set: Optional[TagSet] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            tag_set (TagSet, optional): The collection of tags.
        """
        super().__init__(**kwargs)
        self.tag_set = tag_set

    _attribute_map = {
        "tag_set": {"tag": "xml", "rename": "TagSet", "type": "TagSet"},
    }

    _dependency_map = {
        "TagSet": {"new": lambda: TagSet()},
    }

    _xml_map = {
        "name": "Tagging"
    }


class PutObjectTaggingRequest(serde.RequestModel):
    """The request for the PutObjectTagging operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "tagging": {"tag": "input", "position": "body", "rename": "Tagging", "type": "xml", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        tagging: Tagging = None,
        version_id: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            tagging (Tagging, required): The container used to store the collection of tags.
            version_id (str, optional): Version of the object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.tagging = tagging
        self.version_id = version_id
        self.request_payer = request_payer


class PutObjectTaggingResult(serde.ResultModel):
    """The result for the PutObjectTagging operation."""

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
    }

    def __init__(
        self,
        version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
        """
        super().__init__(**kwargs)
        self.version_id = version_id


class GetObjectTaggingRequest(serde.RequestModel):
    """The request for the GetObjectTagging operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): VersionId used to reference a specific version of the object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.request_payer = request_payer


class GetObjectTaggingResult(serde.ResultModel):
    """The result for the GetObjectTagging operation."""

    def __init__(
        self,
        version_id: Optional[str] = None,
        tag_set: Optional[TagSet] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
            tag_set (TagSet, optional): The collection of tags.
        """
        super().__init__(**kwargs)
        self.version_id = version_id
        self.tag_set = tag_set

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
        "tag_set": {"tag": "xml", "rename": "TagSet", "type": "TagSet"},
    }

    _dependency_map = {
        "TagSet": {"new": lambda: TagSet()},
    }

    _xml_map = {"name":"Tagging"}

class DeleteObjectTaggingRequest(serde.RequestModel):
    """The request for the DeleteObjectTagging operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "version_id": {"tag": "input", "position": "query", "rename": "versionId"},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        version_id: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): VersionId used to reference a specific version of the object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.version_id = version_id
        self.request_payer = request_payer


class DeleteObjectTaggingResult(serde.ResultModel):
    """The result for the DeleteObjectTagging operation."""

    def __init__(
        self,
        version_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            version_id (str, optional): Version of the object.
        """
        super().__init__(**kwargs)
        self.version_id = version_id

    _attribute_map = {
        "version_id": {"tag": "output", "position": "header", "rename": "x-oss-version-id"},
    }


class ProcessObjectRequest(serde.RequestModel):
    """The request for the ProcessObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "process": {"tag": "input", "position": "nop", "rename": "x-oss-process", "required": True},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        process: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            process (str, required): Image processing parameters.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.process = process
        self.request_payer = request_payer


class ProcessObjectResult(serde.ResultModel):
    """The result for the ProcessObject operation."""

    def __init__(
        self,
        bucket: Optional[str] = None,
        file_size: Optional[int] = None,
        key: Optional[str] = None,
        process_status: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, optional): The name of the bucket.
            file_size (str, optional): The size of the proessed object.
            key (str, optional): The name of the proessed object.
            process_status (str, optional): The status.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.file_size = file_size
        self.key = key
        self.process_status = process_status

    _attribute_map = {
        "bucket": {"tag": "json", "rename": "bucket"},
        "file_size": {"tag": "json", "rename": "fileSize", "type": "int"},
        "key": {"tag": "json", "rename": "object"},
        "process_status": {"tag": "json", "rename": "status"},
    }

class AsyncProcessObjectRequest(serde.RequestModel):
    """The request for the AsyncProcessObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "process": {"tag": "input", "position": "nop", "rename": "x-oss-async-process", "required": True},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        process: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            process (str, required): Image async processing parameters.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.process = process
        self.request_payer = request_payer


class AsyncProcessObjectResult(serde.ResultModel):
    """The result for the AsyncProcessObject operation."""

    def __init__(
        self,
        event_id: Optional[str] = None,
        task_id: Optional[int] = None,
        process_request_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            event_id (str, optional): The id of event.
            task_id (str, optional): The id of task.
            process_request_id (str, optional): The request id of task.
        """
        super().__init__(**kwargs)
        self.event_id = event_id
        self.task_id = task_id
        self.process_request_id = process_request_id

    _attribute_map = {
        "event_id": {"tag": "json", "rename": "EventId"},
        "task_id": {"tag": "json", "rename": "TaskId"},
        "process_request_id": {"tag": "json", "rename": "RequestId"},
    }


class CleanRestoredObjectRequest(serde.RequestModel):
    """
    The request for the CleanRestoredObject operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'key': {'tag': 'input', 'position': 'path', 'rename': 'key', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket
            key (str, required): The name of the object.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key


class CleanRestoredObjectResult(serde.ResultModel):
    """
    The request for the CleanRestoredObject operation.
    """


class SealAppendObjectRequest(serde.RequestModel):
    """
    The request for the SealAppendObject operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'key': {'tag': 'input', 'position': 'path', 'rename': 'key', 'type': 'str', 'required': True},
        'position': {'tag': 'input', 'position': 'query', 'rename': 'position', 'type': 'int', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        position: int = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): Bucket name
            key (str, required): Name of the Appendable Object
            position (int, required): Used to specify the expected length of the file when the user wants to seal it.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.position = position


class SealAppendObjectResult(serde.ResultModel):
    """
    The request for the SealAppendObject operation.
    """

    _attribute_map = {
        'sealed_time': {'tag': 'output', 'position': 'header', 'rename': 'x-oss-sealed-time', 'type': 'str'},
    }

    def __init__(
        self,
        sealed_time: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            sealed_time (str, optional): The time when the object was sealed.
        """
        super().__init__(**kwargs)
        self.sealed_time = sealed_time
