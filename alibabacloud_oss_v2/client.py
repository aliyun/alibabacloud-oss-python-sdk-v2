# pylint: disable=line-too-long
"""Client used to interact with **Alibaba Cloud Object Storage Service (OSS)**."""
import copy
from typing import Optional
from .config import Config
from .types import OperationInput, OperationOutput
from ._client import _SyncClientImpl
from .defaults import FF_ENABLE_CRC64_CHECK_DOWNLOAD
from . import models
from . import operations
from . import exceptions
from .downloader import Downloader
from .uploader import Uploader
from .copier import Copier
from .progress import Progress
from .crc import Crc64
from .paginator import (
    ListObjectsPaginator,
    ListObjectsV2Paginator,
    ListObjectVersionsPaginator,
    ListBucketsPaginator,
    ListPartsPaginator,
    ListMultipartUploadsPaginator
)
from .presigner import (
    PresignRequest,
    PresignResult,
    presign_inner
)
from .filelike import AppendOnlyFile, ReadOnlyFile

class Client:
    """Client
    """

    def __init__(self, config: Config, **kwargs) -> None:
        """Initialize Client

        Args:
            config (Config): _description_
        """
        self._client = _SyncClientImpl(config, **kwargs)

    def __repr__(self) -> str:
        return "<OssClient>"

    def invoke_operation(self, op_input: OperationInput, **kwargs
                         ) -> OperationOutput:
        """invoke operation

        Args:
            op_input (OperationInput): _description_

        Returns:
            OperationOutput: _description_
        """
        return self._client.invoke_operation(op_input, **kwargs)

    # sevice
    def list_buckets(self, request: models.ListBucketsRequest, **kwargs
                     ) -> models.ListBucketsResult:
        """
        Lists all buckets that belong to your Alibaba Cloud account.

        Args:
            request (ListBucketsRequest): Request parameters for ListBuckets operation.

        Returns:
            ListBucketsResult: Response result for ListBuckets operation.
        """

        return operations.list_buckets(self._client, request, **kwargs)

    # region
    def describe_regions(self, request: models.DescribeRegionsRequest, **kwargs
                         ) -> models.DescribeRegionsResult:
        """
        Queries the endpoints of all regions supported by Object Storage Service (OSS)
        or a specific region, including public endpoints, internal endpoints,
        and acceleration endpoints.

        Args:
            request (DescribeRegionsRequest): Request parameters for DescribeRegions operation.

        Returns:
            DescribeRegionsResult: Response result for DescribeRegions operation.
        """

        return operations.describe_regions(self._client, request, **kwargs)

    # bucket
    def put_bucket(self, request: models.PutBucketRequest, **kwargs
                   ) -> models.PutBucketResult:
        """
        Creates a bucket.

        Args:
            request (PutBucketRequest): Request parameters for PutBucket operation.

        Returns:
            PutBucketResult: Response result for PutBucket operation.
        """

        return operations.put_bucket(self._client, request, **kwargs)

    def delete_bucket(self, request: models.DeleteBucketRequest, **kwargs
                      ) -> models.DeleteBucketResult:
        """
        Deletes a bucket.

        Args:
            request (DeleteBucketRequest): Request parameters for DeleteBucket operation.

        Returns:
            DeleteBucketResult: Response result for DeleteBucket operation.
        """

        return operations.delete_bucket(self._client, request, **kwargs)

    def list_objects(self, request: models.ListObjectsRequest, **kwargs
                     ) -> models.ListObjectsResult:
        """
        Lists information about all objects in an Object Storage Service (OSS) bucket.

        Args:
            request (ListObjectsRequest): Request parameters for ListObjects operation.

        Returns:
            ListObjectsResult: Response result for ListObjects operation.
        """

        return operations.list_objects(self._client, request, **kwargs)

    def put_bucket_acl(self, request: models.PutBucketAclRequest, **kwargs
                       ) -> models.PutBucketAclResult:
        """
        You can call this operation to configure or modify the ACL of a bucket.

        Args:
            request (PutBucketAclRequest): Request parameters for PutBucketAcl operation.

        Returns:
            PutBucketAclResult: Response result for PutBucketAcl operation.
        """

        return operations.put_bucket_acl(self._client, request, **kwargs)

    def get_bucket_acl(self, request: models.GetBucketAclRequest, **kwargs
                       ) -> models.GetBucketAclResult:
        """
        You can call this operation to query the ACL of a bucket.
        Only the bucket owner can query the ACL of the bucket.

        Args:
            request (GetBucketAclRequest): Request parameters for GetBucketAcl operation.

        Returns:
            GetBucketAclResult: Response result for GetBucketAcl operation.
        """

        return operations.get_bucket_acl(self._client, request, **kwargs)

    def list_objects_v2(self, request: models.ListObjectsV2Request, **kwargs
                        ) -> models.ListObjectsV2Result:
        """
        Lists all objects in a bucket.

        Args:
            request (ListObjectsV2Request): Request parameters for ListObjectsV2 operation.

        Returns:
            ListObjectsV2Result: Response result for ListObjectsV2 operation.
        """

        return operations.list_objects_v2(self._client, request, **kwargs)

    def get_bucket_stat(self, request: models.GetBucketStatRequest, **kwargs
                        ) -> models.GetBucketStatResult:
        """
        GetBucketStat Queries the storage capacity of a specified bucket and
        the number of objects that are stored in the bucket.

        Args:
            request (GetBucketStatRequest): Request parameters for GetBucketStat operation.

        Returns:
            GetBucketStatResult: Response result for GetBucketStat operation.
        """

        return operations.get_bucket_stat(self._client, request, **kwargs)

    def get_bucket_location(self, request: models.GetBucketLocationRequest, **kwargs
                            ) -> models.GetBucketLocationResult:
        """
        GetBucketLocation Queries the region of an Object Storage Service (OSS) bucket.

        Args:
            request (GetBucketLocationRequest): Request parameters for GetBucketLocation operation.

        Returns:
            GetBucketLocationResult: Response result for GetBucketLocation operation.
        """

        return operations.get_bucket_location(self._client, request, **kwargs)

    def get_bucket_info(self, request: models.GetBucketInfoRequest, **kwargs
                        ) -> models.GetBucketInfoResult:
        """
        GetBucketInfo Queries information about a bucket.

        Args:
            request (GetBucketInfoRequest): Request parameters for GetBucketInfo operation.

        Returns:
            GetBucketInfoResult: Response result for GetBucketInfo operation.
        """

        return operations.get_bucket_info(self._client, request, **kwargs)

    def put_bucket_versioning(self, request: models.PutBucketVersioningRequest, **kwargs
                              ) -> models.PutBucketVersioningResult:
        """
        PutBucketVersioning Configures the versioning state for a bucket.

        Args:
            request (PutBucketVersioningRequest): Request parameters for PutBucketVersioning operation.

        Returns:
            PutBucketVersioningResult: Response result for PutBucketVersioning operation.
        """

        return operations.put_bucket_versioning(self._client, request, **kwargs)

    def get_bucket_versioning(self, request: models.GetBucketVersioningRequest, **kwargs
                              ) -> models.GetBucketVersioningResult:
        """
        GetBucketVersioning You can call this operation to query the versioning state of a bucket.

        Args:
            request (GetBucketVersioningRequest): Request parameters for GetBucketVersioning operation.

        Returns:
            GetBucketVersioningResult: Response result for GetBucketVersioning operation.
        """

        return operations.get_bucket_versioning(self._client, request, **kwargs)

    def list_object_versions(self, request: models.ListObjectVersionsRequest, **kwargs
                             ) -> models.ListObjectVersionsResult:
        """
        ListObjectVersions Lists the versions of all objects in a bucket, including delete markers.

        Args:
            request (ListObjectVersionsRequest): Request parameters for ListObjectVersions operation.

        Returns:
            ListObjectVersionsResult: Response result for ListObjectVersions operation.
        """

        return operations.list_object_versions(self._client, request, **kwargs)

    # object
    def put_object(self, request: models.PutObjectRequest, **kwargs
                   ) -> models.PutObjectResult:
        """
        Uploads objects.

        Args:
            request (PutObjectRequest): Request parameters for PutObject operation.

        Returns:
            PutObjectResult: Response result for PutObject operation.
        """

        return operations.put_object(self._client, request, **kwargs)

    def get_object(self, request: models.GetObjectRequest, **kwargs
                   ) -> models.GetObjectResult:
        """
        Queries an object. To call this operation, you must have read permissions on the object.

        Args:
            request (GetObjectRequest): Request parameters for GetObject operation.

        Returns:
            GetObjectResult: Response result for GetObject operation.
        """

        return operations.get_object(self._client, request, **kwargs)

    def copy_object(self, request: models.CopyObjectRequest, **kwargs
                    ) -> models.CopyObjectResult:
        """
        Copies objects within a bucket or between buckets in the same region.

        Args:
            request (CopyObjectRequest): Request parameters for CopyObject operation.

        Returns:
            CopyObjectResult: Response result for CopyObject operation.
        """

        return operations.copy_object(self._client, request, **kwargs)

    def append_object(self, request: models.AppendObjectRequest, **kwargs
                      ) -> models.AppendObjectResult:
        """
        Uploads an object by appending the object to an existing object.
        Objects created by using the AppendObject operation are appendable objects.

        Args:
            request (AppendObjectRequest): Request parameters for AppendObject operation.

        Returns:
            AppendObjectResult: Response result for AppendObject operation.
        """

        return operations.append_object(self._client, request, **kwargs)

    def delete_object(self, request: models.DeleteObjectRequest, **kwargs
                    ) -> models.DeleteObjectResult:
        """
        Deletes an object.

        Args:
            request (DeleteObjectRequest): Request parameters for DeleteObject operation.

        Returns:
            DeleteObjectResult: Response result for DeleteObject operation.
        """

        return operations.delete_object(self._client, request, **kwargs)

    def delete_multiple_objects(self, request: models.DeleteMultipleObjectsRequest, **kwargs
                    ) -> models.DeleteMultipleObjectsResult:
        """
        Deletes multiple objects from a bucket.

        Args:
            request (DeleteMultipleObjectsRequest): Request parameters for DeleteMultipleObjects operation.

        Returns:
            DeleteMultipleObjectsResult: Response result for DeleteMultipleObjects operation.
        """

        return operations.delete_multiple_objects(self._client, request, **kwargs)

    def head_object(self, request: models.HeadObjectRequest, **kwargs
                    ) -> models.HeadObjectResult:
        """
        Queries information about the object in a bucket.

        Args:
            request (HeadObjectRequest): Request parameters for HeadObject operation.

        Returns:
            HeadObjectResult: Response result for HeadObject operation.
        """

        return operations.head_object(self._client, request, **kwargs)

    def get_object_meta(self, request: models.GetObjectMetaRequest, **kwargs
                    ) -> models.GetObjectMetaResult:
        """
        Queries the metadata of an object, including ETag, Size, and LastModified.

        Args:
            request (GetObjectMetaRequest): Request parameters for GetObjectMeta operation.

        Returns:
            GetObjectMetaResult: Response result for GetObjectMeta operation.
        """

        return operations.get_object_meta(self._client, request, **kwargs)

    def restore_object(self, request: models.RestoreObjectRequest, **kwargs
                    ) -> models.RestoreObjectResult:
        """
        Restores Archive, Cold Archive, or Deep Cold Archive objects.

        Args:
            request (RestoreObjectRequest): Request parameters for RestoreObject operation.

        Returns:
            RestoreObjectResult: Response result for RestoreObject operation.
        """

        return operations.restore_object(self._client, request, **kwargs)

    def put_object_acl(self, request: models.PutObjectAclRequest, **kwargs
                    ) -> models.PutObjectAclResult:
        """
        You can call this operation to modify the access control list (ACL) of an object.

        Args:
            request (PutObjectAclRequest): Request parameters for PutObjectAcl operation.

        Returns:
            PutObjectAclResult: Response result for PutObjectAcl operation.
        """

        return operations.put_object_acl(self._client, request, **kwargs)

    def get_object_acl(self, request: models.GetObjectAclRequest, **kwargs
                    ) -> models.GetObjectAclResult:
        """
        Queries the access control list (ACL) of an object in a bucket.

        Args:
            request (GetObjectAclRequest): Request parameters for GetObjectAcl operation.

        Returns:
            GetObjectAclResult: Response result for GetObjectAcl operation.
        """

        return operations.get_object_acl(self._client, request, **kwargs)

    def initiate_multipart_upload(self, request: models.InitiateMultipartUploadRequest, **kwargs
                    ) -> models.InitiateMultipartUploadResult:
        """
        Initiates a multipart upload task before you can upload data in parts to Object Storage Service (OSS).

        Args:
            request (InitiateMultipartUploadRequest): Request parameters for InitiateMultipartUpload operation.

        Returns:
            InitiateMultipartUploadResult: Response result for InitiateMultipartUpload operation.
        """

        return operations.initiate_multipart_upload(self._client, request, **kwargs)

    def upload_part(self, request: models.UploadPartRequest, **kwargs
                    ) -> models.UploadPartResult:
        """
        Call the UploadPart interface to upload data in blocks (parts) based on the specified Object name and uploadId.

        Args:
            request (UploadPartRequest): Request parameters for UploadPart operation.

        Returns:
            UploadPartResult: Response result for UploadPart operation.
        """

        return operations.upload_part(self._client, request, **kwargs)

    def upload_part_copy(self, request: models.UploadPartCopyRequest, **kwargs
                    ) -> models.UploadPartCopyResult:
        """
        You can call this operation to copy data from an existing object to upload a part
        by adding a x-oss-copy-request header to UploadPart.

        Args:
            request (UploadPartCopyRequest): Request parameters for UploadPartCopy operation.

        Returns:
            UploadPartCopyResult: Response result for UploadPartCopy operation.
        """

        return operations.upload_part_copy(self._client, request, **kwargs)

    def complete_multipart_upload(self, request: models.CompleteMultipartUploadRequest, **kwargs
                    ) -> models.CompleteMultipartUploadResult:
        """
        Completes the multipart upload task of an object after all parts of the object are uploaded.

        Args:
            request (CompleteMultipartUploadRequest): Request parameters for CompleteMultipartUpload operation.

        Returns:
            CompleteMultipartUploadResult: Response result for CompleteMultipartUpload operation.
        """

        return operations.complete_multipart_upload(self._client, request, **kwargs)

    def abort_multipart_upload(self, request: models.AbortMultipartUploadRequest, **kwargs
                    ) -> models.AbortMultipartUploadResult:
        """
        Cancels a multipart upload task and deletes the parts uploaded in the task.

        Args:
            request (AbortMultipartUploadRequest): Request parameters for AbortMultipartUpload operation.

        Returns:
            AbortMultipartUploadResult: Response result for AbortMultipartUpload operation.
        """

        return operations.abort_multipart_upload(self._client, request, **kwargs)

    def list_multipart_uploads(self, request: models.ListMultipartUploadsRequest, **kwargs
                    ) -> models.ListMultipartUploadsResult:
        """
        Lists all multipart upload tasks in progress. The tasks are not completed or canceled.

        Args:
            request (ListMultipartUploadsRequest): Request parameters for ListMultipartUploads operation.

        Returns:
            ListMultipartUploadsResult: Response result for ListMultipartUploads operation.
        """

        return operations.list_multipart_uploads(self._client, request, **kwargs)

    def list_parts(self, request: models.ListPartsRequest, **kwargs
                    ) -> models.ListPartsResult:
        """
        Lists all parts that are uploaded by using a specified upload ID.

        Args:
            request (ListPartsRequest): Request parameters for ListParts operation.

        Returns:
            ListPartsResult: Response result for ListParts operation.
        """

        return operations.list_parts(self._client, request, **kwargs)

    def put_symlink(self, request: models.PutSymlinkRequest, **kwargs
                    ) -> models.PutSymlinkResult:
        """
        Creates a symbolic link that points to a destination object.
        You can use the symbolic link to access the destination object.

        Args:
            request (PutSymlinkRequest): Request parameters for PutSymlink operation.

        Returns:
            PutSymlinkResult: Response result for PutSymlink operation.
        """

        return operations.put_symlink(self._client, request, **kwargs)

    def get_symlink(self, request: models.GetSymlinkRequest, **kwargs
                    ) -> models.GetSymlinkResult:
        """
        Obtains a symbol link. To perform GetSymlink operations, you must have the read permission on the symbol link.

        Args:
            request (GetSymlinkRequest): Request parameters for GetSymlink operation.

        Returns:
            GetSymlinkResult: Response result for GetSymlink operation.
        """

        return operations.get_symlink(self._client, request, **kwargs)

    def put_object_tagging(self, request: models.PutObjectTaggingRequest, **kwargs
                    ) -> models.PutObjectTaggingResult:
        """
        Adds tags to an object or updates the tags added to the object. Each tag added to an object is a key-value pair.

        Args:
            request (PutObjectTaggingRequest): Request parameters for PutObjectTagging operation.

        Returns:
            PutObjectTaggingResult: Response result for PutObjectTagging operation.
        """

        return operations.put_object_tagging(self._client, request, **kwargs)

    def get_object_tagging(self, request: models.GetObjectTaggingRequest, **kwargs
                    ) -> models.GetObjectTaggingResult:
        """
        You can call this operation to query the tags of an object.

        Args:
            request (GetObjectTaggingRequest): Request parameters for GetObjectTagging operation.

        Returns:
            GetObjectTaggingResult: Response result for GetObjectTagging operation.
        """

        return operations.get_object_tagging(self._client, request, **kwargs)

    def delete_object_tagging(self, request: models.DeleteObjectTaggingRequest, **kwargs
                    ) -> models.DeleteObjectTaggingResult:
        """
        You can call this operation to delete the tags of a specified object.

        Args:
            request (DeleteObjectTaggingRequest): Request parameters for DeleteObjectTagging operation.

        Returns:
            DeleteObjectTaggingResult: Response result for DeleteObjectTagging operation.
        """

        return operations.delete_object_tagging(self._client, request, **kwargs)

    def process_object(self, request: models.ProcessObjectRequest, **kwargs
                    ) -> models.ProcessObjectResult:
        """
        Applies process on the specified image file.

        Args:
            request (ProcessObjectRequest): Request parameters for ProcessObject operation.

        Returns:
            ProcessObjectResult: Response result for ProcessObject operation.
        """

        return operations.process_object(self._client, request, **kwargs)

    def async_process_object(self, request: models.AsyncProcessObjectRequest, **kwargs
                    ) -> models.AsyncProcessObjectResult:
        """
        Applies async process on the specified image file.

        Args:
            request (AsyncProcessObjectRequest): Request parameters for AsyncProcessObject operation.

        Returns:
            AsyncProcessObjectResult: Response result for AsyncProcessObject operation.
        """

        return operations.async_process_object(self._client, request, **kwargs)

    # presigner
    def presign(self, request: PresignRequest, **kwargs) -> PresignResult:
        """Generates the presigned URL. 
        If you do not specify expires or expiration, the pre-signed URL uses 15 minutes as default.

        Args:
            request (PresignRequest): Request parameters for presign operation.
            expires (datetime.timedelta, optional): The expiration duration for the presigned url.
            expiration (datetime.datetime, optional):The expiration time for the presigned url.
        Returns:
            PresignResult: Response result for presign operation.
        """
        return presign_inner(self._client, request, **kwargs)

    # paginator
    def list_objects_paginator(self, **kwargs) -> ListObjectsPaginator:
        """Creates a paginator for ListObjects

        Returns:
            ListObjectsPaginator: a paginator for ListObjects
        """
        return ListObjectsPaginator(self, **kwargs)

    def list_objects_v2_paginator(self, **kwargs) -> ListObjectsV2Paginator:
        """Creates a paginator for ListObjectsV2

        Returns:
            ListObjectsV2Paginator: a paginator for ListObjectsV2
        """
        return ListObjectsV2Paginator(self, **kwargs)

    def list_object_versions_paginator(self, **kwargs) -> ListObjectVersionsPaginator:
        """Creates a paginator for ListObjectVersions

        Returns:
            ListObjectVersionsPaginator: a paginator for ListObjectVersions
        """
        return ListObjectVersionsPaginator(self, **kwargs)


    def list_buckets_paginator(self, **kwargs) -> ListBucketsPaginator:
        """Creates a paginator for ListBuckets

        Returns:
            ListBucketsPaginator: a paginator for ListBuckets
        """
        return ListBucketsPaginator(self, **kwargs)

    def list_parts_paginator(self, **kwargs) -> ListPartsPaginator:
        """Creates a paginator for ListParts

        Returns:
            ListPartsPaginator: a paginator for ListParts
        """
        return ListPartsPaginator(self, **kwargs)

    def list_multipart_uploads_paginator(self, **kwargs) -> ListMultipartUploadsPaginator:
        """Creates a paginator for ListMultipartUploads

        Returns:
            ListMultipartUploadsPaginator: a paginator for ListMultipartUploads
        """
        return ListMultipartUploadsPaginator(self, **kwargs)


    # transfer managers
    def downloader(self, **kwargs) -> Downloader:
        """Creates a downloader to download objects.

        Args:
            kwargs: Extra keyword arguments used to initialize the downloader.
                - part_size (int): The part size. Default value: 6 MiB.
                - parallel_num (int): The number of the download tasks in parallel. Default value: 3.
                - block_size (int): The block size is the number of bytes it should read into memory. Default value: 16 KiB.
                - use_temp_file (bool): Whether to use a temporary file when you download an object. A temporary file is used by default.
                - enable_checkpoint (bool): Whether to enable checkpoint. Defaults to False.
                - checkpoint_dir (str): The directory to store checkpoint.
                - verify_data (bool): Whether to verify data when the download is resumed. Defaults to False.

        Returns:
            Downloader: a downloader instance.
        """
        return Downloader(self, **kwargs)

    def uploader(self, **kwargs) -> Uploader:
        """Creates a uploader to upload data to server.

        Args:
            kwargs: Extra keyword arguments used to initialize the uploader.
                - part_size (int): The part size. Default value: 6 MiB.
                - parallel_num (int): The number of the upload tasks in parallel. Default value: 3.
                - leave_parts_on_error (bool): Whether to retain the uploaded parts when an upload task fails. By default, the uploaded parts are not retained.
                - enable_checkpoint (bool): Whether to enable checkpoint. Defaults to False.
                - checkpoint_dir (str): The directory to store checkpoint.

        Returns:
            Uploader: a uploader instance.
        """
        return Uploader(self, **kwargs)

    def copier(self, **kwargs) -> Copier:
        """Creates a copier to copy source object to destination object.

        Args:
            kwargs: Extra keyword arguments used to initialize the copier.
            - part_size (int): The part size. Default value: 64 MiB.
            - parallel_num (int): The number of the copy tasks in parallel. Default value: 3.
            - multipart_copy_threshold (int): The minimum object size for calling the multipart copy operation. Default value: 200 MiB.
            - leave_parts_on_error (bool): Whether to retain the copied parts when an upload task fails. By default, the copied parts are not retained.
            - disable_shallow_copy (bool): Whether to use shallow copy capability. Defaults to True.

        Returns:
            Copier: a copier instance.
        """
        return Copier(self, **kwargs)

    # file like objects
    def append_file(self, bucket: str, key: str,
                    request_payer: Optional[str] = None,
                    create_parameter: Optional[models.AppendObjectRequest] = None,
                    **kwargs) -> AppendOnlyFile:
        """Opens or creates the named file for appending

        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs
            create_parameter (AppendObjectRequest, optional): The parameters when the object is first generated, supports below
                CacheControl, ContentEncoding, Expires, ContentType, ContentType, Metadata,SSE's parameters, Acl, StorageClass, Tagging.
                If the object exists, ignore this parameters

        Returns:
            AppendOnlyFile: _description_
        """
        _ = kwargs
        return AppendOnlyFile(
            self,
            bucket=bucket,
            key=key,
            request_payer=request_payer,
            create_parameter=create_parameter
        )

    def open_file(self, bucket: str, key: str,
                    version_id: Optional[str] = None,
                    request_payer: Optional[str] = None,
                    **kwargs) -> ReadOnlyFile:
        """Opens the named file for reading.

        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs

        Returns:
            ReadOnlyFile: _description_
        """
        return ReadOnlyFile(
            self,
            bucket=bucket,
            key=key,
            version_id=version_id,
            request_payer=request_payer,
            **kwargs
        )

    # others apis
    def is_object_exist(self, bucket: str, key: str,
                        version_id: Optional[str] = None,
                        request_payer: Optional[str] = None,
                        **kwargs) -> bool:
        """Checks if the object exists

        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the source object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        Returns:
            bool: True if the object exists, else False.
        """

        result = None
        err = None

        try:
            result = self.get_object_meta(models.GetObjectMetaRequest(
                bucket=bucket,
                key=key,
                version_id=version_id,
                request_payer=request_payer,
                **kwargs
            ))
        except exceptions.OperationError as e:
            err = e
            se = e.unwrap()
            if isinstance(se, exceptions.ServiceError):
                if ('NoSuchKey' == se.code or
                    (404 == se.status_code and 'BadErrorResponse' == se.code)):
                    return False

        if err is not None:
            raise err

        return result is not None

    def is_bucket_exist(self, bucket: str, request_payer: Optional[str] = None, **kwargs) -> bool:
        """Checks if the bucket exists

        Args:
            bucket (str, required): The name of the bucket.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        Returns:
            bool: True if the bucket exists, else False.
        """

        result = None
        err = None

        try:
            result = self.get_bucket_acl(models.GetBucketAclRequest(
                bucket=bucket,
                request_payer=request_payer,
                **kwargs
            ))
        except exceptions.OperationError as e:
            err = e
            se = e.unwrap()
            if isinstance(se, exceptions.ServiceError):
                return not 'NoSuchBucket' == se.code

        if err is not None:
            raise err

        return result is not None

    def put_object_from_file(self, request: models.PutObjectRequest, filepath: str, **kwargs) -> models.PutObjectResult:
        """put an object from file

        Args:
            request (PutObjectRequest): Request parameters for PutObject operation.
            filepath (str): The path of the file to upload.

        Returns:
            PutObjectResult: Response result for PutObject operation.
        """
        with open(filepath, 'rb') as f:
            req = copy.copy(request)
            req.body = f
            return self.put_object(req, **kwargs)

    def get_object_to_file(self, request: models.GetObjectRequest, filepath: str, **kwargs) -> models.GetObjectResult:
        """get an object to file

        Args:
            request (GetObjectRequest): Request parameters for GetObject operation.
            filepath (str): The path of the file to download.

        Returns:
            GetObjectResult: Response result for GetObject operation.
        """
        prog = None
        if request.progress_fn:
            prog = Progress(request.progress_fn, -1)

        chash = None
        if self._client.has_feature(FF_ENABLE_CRC64_CHECK_DOWNLOAD):
            chash = Crc64(0)

        def _crc_checker(headers):
            if chash is None:
                return

            scrc = headers.get('x-oss-hash-crc64ecma', None)
            if scrc is None:
                return
            ccrc = str(chash.sum64())

            if scrc != ccrc:
                raise exceptions.InconsistentError(
                    client_crc=ccrc,
                    server_crc=scrc
                )

        def _get_object_to_file_no_retry(client: Client, request: models.GetObjectRequest, filepath: str, **kwargs):
            with open(filepath, 'wb') as f:
                err = None
                result = client.get_object(request, **kwargs)
                if prog:
                    prog._total = result.content_length

                try:
                    for d in result.body.iter_bytes():
                        f.write(d)
                        if prog:
                            prog.write(d)
                        if chash:
                            chash.write(d)
                    _crc_checker(result.headers)
                except Exception as e:
                    err = e

                result.body.close()
                return result, err

        result = None
        err = None
        for _ in range(1, self._client.get_retry_attempts()):
            result, err = _get_object_to_file_no_retry(self, request, filepath, **kwargs)
            if err is None:
                break

            if prog:
                prog.reset()

            if chash:
                chash.reset()

        if err is not None:
            raise err

        return result


    # access point
    def list_access_points(self, request: models.ListAccessPointsRequest, **kwargs
                           ) -> models.ListAccessPointsResult:
        """
        Queries the information about user-level or bucket-level access points.

        Args:
            request (ListAccessPointsRequest): Request parameters for ListAccessPoints operation.

        Returns:
            ListAccessPointsResult: Response result for ListAccessPoints operation.
        """
        return operations.list_access_points(self._client, request, **kwargs)


    def get_access_point(self, request: models.GetAccessPointRequest, **kwargs
                         ) -> models.GetAccessPointResult:
        """
        Queries the information about an access point.

        Args:
            request (GetAccessPointRequest): Request parameters for GetAccessPoint operation.

        Returns:
            GetAccessPointResult: Response result for GetAccessPoint operation.
        """
        return operations.get_access_point(self._client, request, **kwargs)


    def get_access_point_policy(self, request: models.GetAccessPointPolicyRequest, **kwargs
                                ) -> models.GetAccessPointPolicyResult:
        """
        Queries the configurations of an access point policy.

        Args:
            request (GetAccessPointPolicyRequest): Request parameters for GetAccessPointPolicy operation.

        Returns:
            GetAccessPointPolicyResult: Response result for GetAccessPointPolicy operation.
        """
        return operations.get_access_point_policy(self._client, request, **kwargs)


    def delete_access_point_policy(self, request: models.DeleteAccessPointPolicyRequest, **kwargs
                                   ) -> models.DeleteAccessPointPolicyResult:
        """
        Deletes an access point policy.

        Args:
            request (DeleteAccessPointPolicyRequest): Request parameters for DeleteAccessPointPolicy operation.

        Returns:
            DeleteAccessPointPolicyResult: Response result for DeleteAccessPointPolicy operation.
        """
        return operations.delete_access_point_policy(self._client, request, **kwargs)


    def put_access_point_policy(self, request: models.PutAccessPointPolicyRequest, **kwargs
                                ) -> models.PutAccessPointPolicyResult:
        """
        Configures an access point policy.

        Args:
            request (PutAccessPointPolicyRequest): Request parameters for PutAccessPointPolicy operation.

        Returns:
            PutAccessPointPolicyResult: Response result for PutAccessPointPolicy operation.
        """
        return operations.put_access_point_policy(self._client, request, **kwargs)


    def delete_access_point(self, request: models.DeleteAccessPointRequest, **kwargs
                            ) -> models.DeleteAccessPointResult:
        """
        Deletes an access point.

        Args:
            request (DeleteAccessPointRequest): Request parameters for DeleteAccessPoint operation.

        Returns:
            DeleteAccessPointResult: Response result for DeleteAccessPoint operation.
        """
        return operations.delete_access_point(self._client, request, **kwargs)


    def create_access_point(self, request: models.CreateAccessPointRequest, **kwargs
                            ) -> models.CreateAccessPointResult:
        """
        Creates an access point.

        Args:
            request (CreateAccessPointRequest): Request parameters for CreateAccessPoint operation.

        Returns:
            CreateAccessPointResult: Response result for CreateAccessPoint operation.
        """
        return operations.create_access_point(self._client, request, **kwargs)

    # bucket access monitor
    def put_bucket_access_monitor(self, request: models.PutBucketAccessMonitorRequest, **kwargs
                                  ) -> models.PutBucketAccessMonitorResult:
        """
        Modifies the access tracking status of a bucket.

        Args:
            request (PutBucketAccessMonitorRequest): Request parameters for PutBucketAccessMonitor operation.

        Returns:
            PutBucketAccessMonitorResult: Response result for PutBucketAccessMonitor operation.
        """
        return operations.put_bucket_access_monitor(self._client, request, **kwargs)


    def get_bucket_access_monitor(self, request: models.GetBucketAccessMonitorRequest, **kwargs
                                  ) -> models.GetBucketAccessMonitorResult:
        """
        Queries the access tracking status of a bucket.

        Args:
            request (GetBucketAccessMonitorRequest): Request parameters for GetBucketAccessMonitor operation.

        Returns:
            GetBucketAccessMonitorResult: Response result for GetBucketAccessMonitor operation.
        """
        return operations.get_bucket_access_monitor(self._client, request, **kwargs)


    # bucket archive direct read
    def get_bucket_archive_direct_read(self, request: models.GetBucketArchiveDirectReadRequest, **kwargs
                                       ) -> models.GetBucketArchiveDirectReadResult:
        """
        Queries whether real-time access of Archive objects is enabled for a bucket.

        Args:
            request (GetBucketArchiveDirectReadRequest): Request parameters for GetBucketArchiveDirectRead operation.

        Returns:
            GetBucketArchiveDirectReadResult: Response result for GetBucketArchiveDirectRead operation.
        """
        return operations.get_bucket_archive_direct_read(self._client, request, **kwargs)


    def put_bucket_archive_direct_read(self, request: models.PutBucketArchiveDirectReadRequest, **kwargs
                                       ) -> models.PutBucketArchiveDirectReadResult:
        """
        Enables or disables real-time access of Archive objects for a bucket.

        Args:
            request (PutBucketArchiveDirectReadRequest): Request parameters for PutBucketArchiveDirectRead operation.

        Returns:
            PutBucketArchiveDirectReadResult: Response result for PutBucketArchiveDirectRead operation.
        """
        return operations.put_bucket_archive_direct_read(self._client, request, **kwargs)


    # cname
    def create_cname_token(self, request: models.CreateCnameTokenRequest, **kwargs
                           ) -> models.CreateCnameTokenResult:
        """
        Creates a CNAME token to verify the ownership of a domain name.

        Args:
            request (CreateCnameTokenRequest): Request parameters for CreateCnameToken operation.

        Returns:
            CreateCnameTokenResult: Response result for CreateCnameToken operation.
        """
        return operations.create_cname_token(self._client, request, **kwargs)

    def get_cname_token(self, request: models.GetCnameTokenRequest, **kwargs
                        ) -> models.GetCnameTokenResult:
        """
        Queries the created CNAME tokens.

        Args:
            request (GetCnameTokenRequest): Request parameters for GetCnameToken operation.

        Returns:
            GetCnameTokenResult: Response result for GetCnameToken operation.
        """
        return operations.get_cname_token(self._client, request, **kwargs)

    def put_cname(self, request: models.PutCnameRequest, **kwargs
                  ) -> models.PutCnameResult:
        """
        Maps a CNAME record to a bucket.

        Args:
            request (PutCnameRequest): Request parameters for PutCname operation.

        Returns:
            PutCnameResult: Response result for PutCname operation.
        """
        return operations.put_cname(self._client, request, **kwargs)


    def list_cname(self, request: models.ListCnameRequest, **kwargs
                   ) -> models.ListCnameResult:
        """
        Queries all CNAME records that are mapped to a bucket.

        Args:
            request (ListCnameRequest): Request parameters for ListCname operation.

        Returns:
            ListCnameResult: Response result for ListCname operation.
        """
        return operations.list_cname(self._client, request, **kwargs)


    def delete_cname(self, request: models.DeleteCnameRequest, **kwargs
                     ) -> models.DeleteCnameResult:
        """
        Deletes a CNAME record that is mapped to a bucket.

        Args:
            request (DeleteCnameRequest): Request parameters for DeleteCname operation.

        Returns:
            DeleteCnameResult: Response result for DeleteCname operation.
        """
        return operations.delete_cname(self._client, request, **kwargs)

    # bucket lifecycle
    def put_bucket_lifecycle(self, request: models.PutBucketLifecycleRequest, **kwargs
                             ) -> models.PutBucketLifecycleResult:
        """
        Configures a lifecycle rule for a bucket. After you configure a lifecycle rule for a bucket, Object Storage Service (OSS) automatically deletes the objects that match the rule or converts the storage type of the objects based on the point in time that is specified in the lifecycle rule.

        Args:
            request (PutBucketLifecycleRequest): Request parameters for PutBucketLifecycle operation.

        Returns:
            PutBucketLifecycleResult: Response result for PutBucketLifecycle operation.
        """
        return operations.put_bucket_lifecycle(self._client, request, **kwargs)

    def get_bucket_lifecycle(self, request: models.GetBucketLifecycleRequest, **kwargs
                             ) -> models.GetBucketLifecycleResult:
        """
        Queries the lifecycle rules configured for a bucket. Only the owner of a bucket has the permissions to query the lifecycle rules configured for the bucket.

        Args:
            request (GetBucketLifecycleRequest): Request parameters for GetBucketLifecycle operation.

        Returns:
            GetBucketLifecycleResult: Response result for GetBucketLifecycle operation.
        """
        return operations.get_bucket_lifecycle(self._client, request, **kwargs)

    def delete_bucket_lifecycle(self, request: models.DeleteBucketLifecycleRequest, **kwargs
                                ) -> models.DeleteBucketLifecycleResult:
        """
        Deletes the lifecycle rules of a bucket.

        Args:
            request (DeleteBucketLifecycleRequest): Request parameters for DeleteBucketLifecycle operation.

        Returns:
            DeleteBucketLifecycleResult: Response result for DeleteBucketLifecycle operation.
        """
        return operations.delete_bucket_lifecycle(self._client, request, **kwargs)

    # bucket cors
    def put_bucket_cors(self, request: models.PutBucketCorsRequest, **kwargs
                        ) -> models.PutBucketCorsResult:
        """
        Configures cross-origin resource sharing (CORS) rules for a bucket.

        Args:
            request (PutBucketCorsRequest): Request parameters for PutBucketCors operation.

        Returns:
            PutBucketCorsResult: Response result for PutBucketCors operation.
        """
        return operations.put_bucket_cors(self._client, request, **kwargs)


    def get_bucket_cors(self, request: models.GetBucketCorsRequest, **kwargs
                        ) -> models.GetBucketCorsResult:
        """
        Queries the cross-origin resource sharing (CORS) rules that are configured for a bucket.

        Args:
            request (GetBucketCorsRequest): Request parameters for GetBucketCors operation.

        Returns:
            GetBucketCorsResult: Response result for GetBucketCors operation.
        """
        return operations.get_bucket_cors(self._client, request, **kwargs)


    def delete_bucket_cors(self, request: models.DeleteBucketCorsRequest, **kwargs
                           ) -> models.DeleteBucketCorsResult:
        """
        Disables the cross-origin resource sharing (CORS) feature and deletes all CORS rules for a bucket.

        Args:
            request (DeleteBucketCorsRequest): Request parameters for DeleteBucketCors operation.

        Returns:
            DeleteBucketCorsResult: Response result for DeleteBucketCors operation.
        """
        return operations.delete_bucket_cors(self._client, request, **kwargs)


    def option_object(self, request: models.OptionObjectRequest, **kwargs
                      ) -> models.OptionObjectResult:
        """
        Determines whether to send a cross-origin request. Before a cross-origin request is sent, the browser sends a preflight OPTIONS request that includes a specific origin, HTTP method, and header information to Object Storage Service (OSS) to determine whether to send the cross-origin request.

        Args:
            request (OptionObjectRequest): Request parameters for OptionObject operation.

        Returns:
            OptionObjectResult: Response result for OptionObject operation.
        """
        return operations.option_object(self._client, request, **kwargs)


    # bucket inventory
    def put_bucket_inventory(self, request: models.PutBucketInventoryRequest, **kwargs
                             ) -> models.PutBucketInventoryResult:
        """
        Configures an inventory for a bucket.

        Args:
            request (PutBucketInventoryRequest): Request parameters for PutBucketInventory operation.

        Returns:
            PutBucketInventoryResult: Response result for PutBucketInventory operation.
        """
        return operations.put_bucket_inventory(self._client, request, **kwargs)


    def get_bucket_inventory(self, request: models.GetBucketInventoryRequest, **kwargs
                             ) -> models.GetBucketInventoryResult:
        """
        Queries the inventories that are configured for a bucket.

        Args:
            request (GetBucketInventoryRequest): Request parameters for GetBucketInventory operation.

        Returns:
            GetBucketInventoryResult: Response result for GetBucketInventory operation.
        """
        return operations.get_bucket_inventory(self._client, request, **kwargs)


    def list_bucket_inventory(self, request: models.ListBucketInventoryRequest, **kwargs
                              ) -> models.ListBucketInventoryResult:
        """
        Queries all inventories in a bucket at a time.

        Args:
            request (ListBucketInventoryRequest): Request parameters for ListBucketInventory operation.

        Returns:
            ListBucketInventoryResult: Response result for ListBucketInventory operation.
        """
        return operations.list_bucket_inventory(self._client, request, **kwargs)


    def delete_bucket_inventory(self, request: models.DeleteBucketInventoryRequest, **kwargs
                                ) -> models.DeleteBucketInventoryResult:
        """
        Deletes an inventory for a bucket.

        Args:
            request (DeleteBucketInventoryRequest): Request parameters for DeleteBucketInventory operation.

        Returns:
            DeleteBucketInventoryResult: Response result for DeleteBucketInventory operation.
        """
        return operations.delete_bucket_inventory(self._client, request, **kwargs)

    # bucket policy
    def put_bucket_policy(self, request: models.PutBucketPolicyRequest, **kwargs
                          ) -> models.PutBucketPolicyResult:
        """
        Configures a policy for a bucket.

        Args:
            request (PutBucketPolicyRequest): Request parameters for PutBucketPolicy operation.

        Returns:
            PutBucketPolicyResult: Response result for PutBucketPolicy operation.
        """
        return operations.put_bucket_policy(self._client, request, **kwargs)

    def get_bucket_policy(self, request: models.GetBucketPolicyRequest, **kwargs
                          ) -> models.GetBucketPolicyResult:
        """
        Queries the policies configured for a bucket.

        Args:
            request (GetBucketPolicyRequest): Request parameters for GetBucketPolicy operation.

        Returns:
            GetBucketPolicyResult: Response result for GetBucketPolicy operation.
        """
        return operations.get_bucket_policy(self._client, request, **kwargs)


    def delete_bucket_policy(self, request: models.DeleteBucketPolicyRequest, **kwargs
                             ) -> models.DeleteBucketPolicyResult:
        """
        Deletes a policy for a bucket.

        Args:
            request (DeleteBucketPolicyRequest): Request parameters for DeleteBucketPolicy operation.

        Returns:
            DeleteBucketPolicyResult: Response result for DeleteBucketPolicy operation.
        """
        return operations.delete_bucket_policy(self._client, request, **kwargs)


    def get_bucket_policy_status(self, request: models.GetBucketPolicyStatusRequest, **kwargs
                                 ) -> models.GetBucketPolicyStatusResult:
        """
        Checks whether the current bucket policy allows public access.

        Args:
            request (GetBucketPolicyStatusRequest): Request parameters for GetBucketPolicyStatus operation.

        Returns:
            GetBucketPolicyStatusResult: Response result for GetBucketPolicyStatus operation.
        """
        return operations.get_bucket_policy_status(self._client, request, **kwargs)


    # bucket logging
    def put_bucket_logging(self, request: models.PutBucketLoggingRequest, **kwargs
                           ) -> models.PutBucketLoggingResult:
        """
        Enables logging for a bucket. After you enable logging for a bucket, Object Storage Service (OSS) generates logs every hour based on the defined naming rule and stores the logs as objects in the specified destination bucket.

        Args:
            request (PutBucketLoggingRequest): Request parameters for PutBucketLogging operation.

        Returns:
            PutBucketLoggingResult: Response result for PutBucketLogging operation.
        """
        return operations.put_bucket_logging(self._client, request, **kwargs)


    def get_bucket_logging(self, request: models.GetBucketLoggingRequest, **kwargs
                           ) -> models.GetBucketLoggingResult:
        """
        Queries the configurations of access log collection of a bucket. Only the owner of a bucket can query the configurations of access log collection of the bucket.

        Args:
            request (GetBucketLoggingRequest): Request parameters for GetBucketLogging operation.

        Returns:
            GetBucketLoggingResult: Response result for GetBucketLogging operation.
        """
        return operations.get_bucket_logging(self._client, request, **kwargs)


    def delete_bucket_logging(self, request: models.DeleteBucketLoggingRequest, **kwargs
                              ) -> models.DeleteBucketLoggingResult:
        """
        Disables the logging feature for a bucket.

        Args:
            request (DeleteBucketLoggingRequest): Request parameters for DeleteBucketLogging operation.

        Returns:
            DeleteBucketLoggingResult: Response result for DeleteBucketLogging operation.
        """
        return operations.delete_bucket_logging(self._client, request, **kwargs)


    def put_user_defined_log_fields_config(self, request: models.PutUserDefinedLogFieldsConfigRequest, **kwargs
                                           ) -> models.PutUserDefinedLogFieldsConfigResult:
        """
        Customizes the user_defined_log_fields field in real-time logs by adding custom request headers or query parameters to the field for subsequent analysis of requests.

        Args:
            request (PutUserDefinedLogFieldsConfigRequest): Request parameters for PutUserDefinedLogFieldsConfig operation.

        Returns:
            PutUserDefinedLogFieldsConfigResult: Response result for PutUserDefinedLogFieldsConfig operation.
        """
        return operations.put_user_defined_log_fields_config(self._client, request, **kwargs)


    def get_user_defined_log_fields_config(self, request: models.GetUserDefinedLogFieldsConfigRequest, **kwargs
                                           ) -> models.GetUserDefinedLogFieldsConfigResult:
        """
        Queries the custom configurations of the user_defined_log_fields field in the real-time logs of a bucket.

        Args:
            request (GetUserDefinedLogFieldsConfigRequest): Request parameters for GetUserDefinedLogFieldsConfig operation.

        Returns:
            GetUserDefinedLogFieldsConfigResult: Response result for GetUserDefinedLogFieldsConfig operation.
        """
        return operations.get_user_defined_log_fields_config(self._client, request, **kwargs)


    def delete_user_defined_log_fields_config(self, request: models.DeleteUserDefinedLogFieldsConfigRequest, **kwargs
                                              ) -> models.DeleteUserDefinedLogFieldsConfigResult:
        """
        Deletes the custom configurations of the user_defined_log_fields field in the real-time logs of a bucket.

        Args:
            request (DeleteUserDefinedLogFieldsConfigRequest): Request parameters for DeleteUserDefinedLogFieldsConfig operation.

        Returns:
            DeleteUserDefinedLogFieldsConfigResult: Response result for DeleteUserDefinedLogFieldsConfig operation.
        """
        return operations.delete_user_defined_log_fields_config(self._client, request, **kwargs)

    # bucket_encryption
    def put_bucket_encryption(self, request: models.PutBucketEncryptionRequest, **kwargs
                              ) -> models.PutBucketEncryptionResult:
        """
        Configures encryption rules for a bucket.

        Args:
            request (PutBucketEncryptionRequest): Request parameters for PutBucketEncryption operation.

        Returns:
            PutBucketEncryptionResult: Response result for PutBucketEncryption operation.
        """
        return operations.put_bucket_encryption(self._client, request, **kwargs)


    def get_bucket_encryption(self, request: models.GetBucketEncryptionRequest, **kwargs
                              ) -> models.GetBucketEncryptionResult:
        """
        Queries the encryption rules configured for a bucket.

        Args:
            request (GetBucketEncryptionRequest): Request parameters for GetBucketEncryption operation.

        Returns:
            GetBucketEncryptionResult: Response result for GetBucketEncryption operation.
        """
        return operations.get_bucket_encryption(self._client, request, **kwargs)


    def delete_bucket_encryption(self, request: models.DeleteBucketEncryptionRequest, **kwargs
                                 ) -> models.DeleteBucketEncryptionResult:
        """
        Deletes encryption rules for a bucket.

        Args:
            request (DeleteBucketEncryptionRequest): Request parameters for DeleteBucketEncryption operation.

        Returns:
            DeleteBucketEncryptionResult: Response result for DeleteBucketEncryption operation.
        """
        return operations.delete_bucket_encryption(self._client, request, **kwargs)


    # bucket website
    def get_bucket_website(self, request: models.GetBucketWebsiteRequest, **kwargs
                           ) -> models.GetBucketWebsiteResult:
        """
        Queries the static website hosting status and redirection rules configured for a bucket.

        Args:
            request (GetBucketWebsiteRequest): Request parameters for GetBucketWebsite operation.

        Returns:
            GetBucketWebsiteResult: Response result for GetBucketWebsite operation.
        """
        return operations.get_bucket_website(self._client, request, **kwargs)


    def put_bucket_website(self, request: models.PutBucketWebsiteRequest, **kwargs
                           ) -> models.PutBucketWebsiteResult:
        """
        Enables the static website hosting mode for a bucket and configures redirection rules for the bucket.

        Args:
            request (PutBucketWebsiteRequest): Request parameters for PutBucketWebsite operation.

        Returns:
            PutBucketWebsiteResult: Response result for PutBucketWebsite operation.
        """
        return operations.put_bucket_website(self._client, request, **kwargs)


    def delete_bucket_website(self, request: models.DeleteBucketWebsiteRequest, **kwargs
                              ) -> models.DeleteBucketWebsiteResult:
        """
        Disables the static website hosting mode and deletes the redirection rules for a bucket.

        Args:
            request (DeleteBucketWebsiteRequest): Request parameters for DeleteBucketWebsite operation.

        Returns:
            DeleteBucketWebsiteResult: Response result for DeleteBucketWebsite operation.
        """
        return operations.delete_bucket_website(self._client, request, **kwargs)

    # bucket replication
    def put_bucket_rtc(self, request: models.PutBucketRtcRequest, **kwargs
                       ) -> models.PutBucketRtcResult:
        """
        Enables or disables the Replication Time Control (RTC) feature for existing cross-region replication (CRR) rules.

        Args:
            request (PutBucketRtcRequest): Request parameters for PutBucketRtc operation.

        Returns:
            PutBucketRtcResult: Response result for PutBucketRtc operation.
        """
        return operations.put_bucket_rtc(self._client, request, **kwargs)


    def put_bucket_replication(self, request: models.PutBucketReplicationRequest, **kwargs
                               ) -> models.PutBucketReplicationResult:
        """
        Configures data replication rules for a bucket. Object Storage Service (OSS) supports cross-region replication (CRR) and same-region replication (SRR).

        Args:
            request (PutBucketReplicationRequest): Request parameters for PutBucketReplication operation.

        Returns:
            PutBucketReplicationResult: Response result for PutBucketReplication operation.
        """
        return operations.put_bucket_replication(self._client, request, **kwargs)


    def get_bucket_replication(self, request: models.GetBucketReplicationRequest, **kwargs
                               ) -> models.GetBucketReplicationResult:
        """
        Queries the data replication rules configured for a bucket.

        Args:
            request (GetBucketReplicationRequest): Request parameters for GetBucketReplication operation.

        Returns:
            GetBucketReplicationResult: Response result for GetBucketReplication operation.
        """
        return operations.get_bucket_replication(self._client, request, **kwargs)


    def get_bucket_replication_location(self, request: models.GetBucketReplicationLocationRequest, **kwargs
                                        ) -> models.GetBucketReplicationLocationResult:
        """
        Queries the regions in which available destination buckets reside. You can determine the region of the destination bucket to which the data in the source bucket are replicated based on the returned response.

        Args:
            request (GetBucketReplicationLocationRequest): Request parameters for GetBucketReplicationLocation operation.

        Returns:
            GetBucketReplicationLocationResult: Response result for GetBucketReplicationLocation operation.
        """
        return operations.get_bucket_replication_location(self._client, request, **kwargs)


    def get_bucket_replication_progress(self, request: models.GetBucketReplicationProgressRequest, **kwargs
                                        ) -> models.GetBucketReplicationProgressResult:
        """
        Queries the information about the data replication process of a bucket.

        Args:
            request (GetBucketReplicationProgressRequest): Request parameters for GetBucketReplicationProgress operation.

        Returns:
            GetBucketReplicationProgressResult: Response result for GetBucketReplicationProgress operation.
        """
        return operations.get_bucket_replication_progress(self._client, request, **kwargs)


    def delete_bucket_replication(self, request: models.DeleteBucketReplicationRequest, **kwargs
                                  ) -> models.DeleteBucketReplicationResult:
        """
        Disables data replication for a bucket and deletes the data replication rule configured for the bucket. After you call this operation, all operations performed on the source bucket are not synchronized to the destination bucket.

        Args:
            request (DeleteBucketReplicationRequest): Request parameters for DeleteBucketReplication operation.

        Returns:
            DeleteBucketReplicationResult: Response result for DeleteBucketReplication operation.
        """
        return operations.delete_bucket_replication(self._client, request, **kwargs)

    # bucket referer
    def put_bucket_referer(self, request: models.PutBucketRefererRequest, **kwargs
                           ) -> models.PutBucketRefererResult:
        """
        Configures a Referer whitelist for an Object Storage Service (OSS) bucket. You can specify whether to allow the requests whose Referer field is empty or whose query strings are truncated.

        Args:
            request (PutBucketRefererRequest): Request parameters for PutBucketReferer operation.

        Returns:
            PutBucketRefererResult: Response result for PutBucketReferer operation.
        """
        return operations.put_bucket_referer(self._client, request, **kwargs)


    def get_bucket_referer(self, request: models.GetBucketRefererRequest, **kwargs
                           ) -> models.GetBucketRefererResult:
        """
        Queries the hotlink protection configurations for a bucket.

        Args:
            request (GetBucketRefererRequest): Request parameters for GetBucketReferer operation.

        Returns:
            GetBucketRefererResult: Response result for GetBucketReferer operation.
        """
        return operations.get_bucket_referer(self._client, request, **kwargs)


   # bucket worm
    def initiate_bucket_worm(self, request: models.InitiateBucketWormRequest, **kwargs
                             ) -> models.InitiateBucketWormResult:
        """
        Creates a retention policy.

        Args:
            request (InitiateBucketWormRequest): Request parameters for InitiateBucketWorm operation.

        Returns:
            InitiateBucketWormResult: Response result for InitiateBucketWorm operation.
        """
        return operations.initiate_bucket_worm(self._client, request, **kwargs)


    def abort_bucket_worm(self, request: models.AbortBucketWormRequest, **kwargs
                          ) -> models.AbortBucketWormResult:
        """
        Deletes an unlocked retention policy for a bucket.

        Args:
            request (AbortBucketWormRequest): Request parameters for AbortBucketWorm operation.

        Returns:
            AbortBucketWormResult: Response result for AbortBucketWorm operation.
        """
        return operations.abort_bucket_worm(self._client, request, **kwargs)


    def complete_bucket_worm(self, request: models.CompleteBucketWormRequest, **kwargs
                             ) -> models.CompleteBucketWormResult:
        """
        Locks a retention policy.

        Args:
            request (CompleteBucketWormRequest): Request parameters for CompleteBucketWorm operation.

        Returns:
            CompleteBucketWormResult: Response result for CompleteBucketWorm operation.
        """
        return operations.complete_bucket_worm(self._client, request, **kwargs)


    def extend_bucket_worm(self, request: models.ExtendBucketWormRequest, **kwargs
                           ) -> models.ExtendBucketWormResult:
        """
        Extends the retention period of objects in a bucket for which a retention policy is locked.

        Args:
            request (ExtendBucketWormRequest): Request parameters for ExtendBucketWorm operation.

        Returns:
            ExtendBucketWormResult: Response result for ExtendBucketWorm operation.
        """
        return operations.extend_bucket_worm(self._client, request, **kwargs)


    def get_bucket_worm(self, request: models.GetBucketWormRequest, **kwargs
                        ) -> models.GetBucketWormResult:
        """
        Queries the retention policy configured for a bucket.

        Args:
            request (GetBucketWormRequest): Request parameters for GetBucketWorm operation.

        Returns:
            GetBucketWormResult: Response result for GetBucketWorm operation.
        """
        return operations.get_bucket_worm(self._client, request, **kwargs)


    # bucket request payment
    def put_bucket_request_payment(self, request: models.PutBucketRequestPaymentRequest, **kwargs
                               ) -> models.PutBucketRequestPaymentResult:
        """
        Enables pay-by-requester for a bucket.

        Args:
            request (PutBucketRequestPaymentRequest): Request parameters for PutBucketRequestPayment operation.

        Returns:
            PutBucketRequestPaymentResult: Response result for PutBucketRequestPayment operation.
        """
        return operations.put_bucket_request_payment(self._client, request, **kwargs)


    def get_bucket_request_payment(self, request: models.GetBucketRequestPaymentRequest, **kwargs
                                   ) -> models.GetBucketRequestPaymentResult:
        """
        Queries pay-by-requester configurations for a bucket.

        Args:
            request (GetBucketRequestPaymentRequest): Request parameters for GetBucketRequestPayment operation.

        Returns:
            GetBucketRequestPaymentResult: Response result for GetBucketRequestPayment operation.
        """
        return operations.get_bucket_request_payment(self._client, request, **kwargs)

    # access point public access block
    def put_access_point_public_access_block(self, request: models.PutAccessPointPublicAccessBlockRequest, **kwargs
                                             ) -> models.PutAccessPointPublicAccessBlockResult:
        """
        Enables or disables Block Public Access for an access point.

        Args:
            request (PutAccessPointPublicAccessBlockRequest): Request parameters for PutAccessPointPublicAccessBlock operation.

        Returns:
            PutAccessPointPublicAccessBlockResult: Response result for PutAccessPointPublicAccessBlock operation.
        """
        return operations.put_access_point_public_access_block(self._client, request, **kwargs)

    def get_access_point_public_access_block(self, request: models.GetAccessPointPublicAccessBlockRequest, **kwargs
                                             ) -> models.GetAccessPointPublicAccessBlockResult:
        """
        Queries the Block Public Access configurations of an access point.

        Args:
            request (GetAccessPointPublicAccessBlockRequest): Request parameters for GetAccessPointPublicAccessBlock operation.

        Returns:
            GetAccessPointPublicAccessBlockResult: Response result for GetAccessPointPublicAccessBlock operation.
        """
        return operations.get_access_point_public_access_block(self._client, request, **kwargs)

    def delete_access_point_public_access_block(self, request: models.DeleteAccessPointPublicAccessBlockRequest, **kwargs
                                                ) -> models.DeleteAccessPointPublicAccessBlockResult:
        """
        Deletes the Block Public Access configurations of an access point.

        Args:
            request (DeleteAccessPointPublicAccessBlockRequest): Request parameters for DeleteAccessPointPublicAccessBlock operation.

        Returns:
            DeleteAccessPointPublicAccessBlockResult: Response result for DeleteAccessPointPublicAccessBlock operation.
        """
        return operations.delete_access_point_public_access_block(self._client, request, **kwargs)

    # bucket data redundancy transition
    def create_bucket_data_redundancy_transition(self, request: models.CreateBucketDataRedundancyTransitionRequest, **kwargs
                                                 ) -> models.CreateBucketDataRedundancyTransitionResult:
        """
        Creates a redundancy type conversion task for a bucket.

        Args:
            request (CreateBucketDataRedundancyTransitionRequest): Request parameters for CreateBucketDataRedundancyTransition operation.

        Returns:
            CreateBucketDataRedundancyTransitionResult: Response result for CreateBucketDataRedundancyTransition operation.
        """
        return operations.create_bucket_data_redundancy_transition(self._client, request, **kwargs)

    def get_bucket_data_redundancy_transition(self, request: models.GetBucketDataRedundancyTransitionRequest, **kwargs
                                              ) -> models.GetBucketDataRedundancyTransitionResult:
        """
        Queries the redundancy type conversion tasks of a bucket.

        Args:
            request (GetBucketDataRedundancyTransitionRequest): Request parameters for GetBucketDataRedundancyTransition operation.

        Returns:
            GetBucketDataRedundancyTransitionResult: Response result for GetBucketDataRedundancyTransition operation.
        """
        return operations.get_bucket_data_redundancy_transition(self._client, request, **kwargs)

    def list_bucket_data_redundancy_transition(self, request: models.ListBucketDataRedundancyTransitionRequest, **kwargs
                                               ) -> models.ListBucketDataRedundancyTransitionResult:
        """
        Lists all redundancy type conversion tasks of a bucket.

        Args:
            request (ListBucketDataRedundancyTransitionRequest): Request parameters for ListBucketDataRedundancyTransition operation.

        Returns:
            ListBucketDataRedundancyTransitionResult: Response result for ListBucketDataRedundancyTransition operation.
        """
        return operations.list_bucket_data_redundancy_transition(self._client, request, **kwargs)

    def list_user_data_redundancy_transition(self, request: models.ListUserDataRedundancyTransitionRequest, **kwargs
                                               ) -> models.ListUserDataRedundancyTransitionResult:
        """
        Lists all redundancy type conversion tasks of a user.

        Args:
            request (ListUserDataRedundancyTransitionRequest): Request parameters for ListUserDataRedundancyTransition operation.

        Returns:
            ListUserDataRedundancyTransitionResult: Response result for ListUserDataRedundancyTransition operation.
        """
        return operations.list_user_data_redundancy_transition(self._client, request, **kwargs)

    def delete_bucket_data_redundancy_transition(self, request: models.DeleteBucketDataRedundancyTransitionRequest, **kwargs
                                                 ) -> models.DeleteBucketDataRedundancyTransitionResult:
        """
        Deletes a redundancy type conversion task of a bucket.

        Args:
            request (DeleteBucketDataRedundancyTransitionRequest): Request parameters for DeleteBucketDataRedundancyTransition operation.

        Returns:
            DeleteBucketDataRedundancyTransitionResult: Response result for DeleteBucketDataRedundancyTransition operation.
        """
        return operations.delete_bucket_data_redundancy_transition(self._client, request, **kwargs)


    # bucket transfer acceleration
    def put_bucket_transfer_acceleration(self, request: models.PutBucketTransferAccelerationRequest, **kwargs
                                         ) -> models.PutBucketTransferAccelerationResult:
        """
        Configures transfer acceleration for a bucket. After you enable transfer acceleration for a bucket, the object access speed is accelerated for users worldwide. The transfer acceleration feature is applicable to scenarios where data needs to be transferred over long geographical distances. This feature can also be used to download or upload objects that are gigabytes or terabytes in size.

        Args:
            request (PutBucketTransferAccelerationRequest): Request parameters for PutBucketTransferAcceleration operation.

        Returns:
            PutBucketTransferAccelerationResult: Response result for PutBucketTransferAcceleration operation.
        """
        return operations.put_bucket_transfer_acceleration(self._client, request, **kwargs)


    def get_bucket_transfer_acceleration(self, request: models.GetBucketTransferAccelerationRequest, **kwargs
                                         ) -> models.GetBucketTransferAccelerationResult:
        """
        Queries the transfer acceleration configurations of a bucket.

        Args:
            request (GetBucketTransferAccelerationRequest): Request parameters for GetBucketTransferAcceleration operation.

        Returns:
            GetBucketTransferAccelerationResult: Response result for GetBucketTransferAcceleration operation.
        """
        return operations.get_bucket_transfer_acceleration(self._client, request, **kwargs)

    # bucket public access block
    def get_bucket_public_access_block(self, request: models.GetBucketPublicAccessBlockRequest, **kwargs
                                       ) -> models.GetBucketPublicAccessBlockResult:
        """
        Queries the Block Public Access configurations of a bucket.

        Args:
            request (GetBucketPublicAccessBlockRequest): Request parameters for GetBucketPublicAccessBlock operation.

        Returns:
            GetBucketPublicAccessBlockResult: Response result for GetBucketPublicAccessBlock operation.
        """
        return operations.get_bucket_public_access_block(self._client, request, **kwargs)


    def put_bucket_public_access_block(self, request: models.PutBucketPublicAccessBlockRequest, **kwargs
                                       ) -> models.PutBucketPublicAccessBlockResult:
        """
        Enables or disables Block Public Access for a bucket.

        Args:
            request (PutBucketPublicAccessBlockRequest): Request parameters for PutBucketPublicAccessBlock operation.

        Returns:
            PutBucketPublicAccessBlockResult: Response result for PutBucketPublicAccessBlock operation.
        """
        return operations.put_bucket_public_access_block(self._client, request, **kwargs)


    def delete_bucket_public_access_block(self, request: models.DeleteBucketPublicAccessBlockRequest, **kwargs
                                          ) -> models.DeleteBucketPublicAccessBlockResult:
        """
        Deletes the Block Public Access configurations of a bucket.

        Args:
            request (DeleteBucketPublicAccessBlockRequest): Request parameters for DeleteBucketPublicAccessBlock operation.

        Returns:
            DeleteBucketPublicAccessBlockResult: Response result for DeleteBucketPublicAccessBlock operation.
        """
        return operations.delete_bucket_public_access_block(self._client, request, **kwargs)

    # public access block
    def get_public_access_block(self, request: models.GetPublicAccessBlockRequest, **kwargs
                                ) -> models.GetPublicAccessBlockResult:
        """
        Queries the Block Public Access configurations of OSS resources.

        Args:
            request (GetPublicAccessBlockRequest): Request parameters for GetPublicAccessBlock operation.

        Returns:
            GetPublicAccessBlockResult: Response result for GetPublicAccessBlock operation.
        """
        return operations.get_public_access_block(self._client, request, **kwargs)


    def put_public_access_block(self, request: models.PutPublicAccessBlockRequest, **kwargs
                                ) -> models.PutPublicAccessBlockResult:
        """
        Enables or disables Block Public Access for Object Storage Service (OSS) resources.

        Args:
            request (PutPublicAccessBlockRequest): Request parameters for PutPublicAccessBlock operation.

        Returns:
            PutPublicAccessBlockResult: Response result for PutPublicAccessBlock operation.
        """
        return operations.put_public_access_block(self._client, request, **kwargs)


    def delete_public_access_block(self, request: models.DeletePublicAccessBlockRequest, **kwargs
                                   ) -> models.DeletePublicAccessBlockResult:
        """
        Deletes the Block Public Access configurations of OSS resources.

        Args:
            request (DeletePublicAccessBlockRequest): Request parameters for DeletePublicAccessBlock operation.

        Returns:
            DeletePublicAccessBlockResult: Response result for DeletePublicAccessBlock operation.
        """
        return operations.delete_public_access_block(self._client, request, **kwargs)

    # bucket resource group
    def get_bucket_resource_group(self, request: models.GetBucketResourceGroupRequest, **kwargs
                                  ) -> models.GetBucketResourceGroupResult:
        """
        Queries the ID of the resource group to which a bucket belongs.

        Args:
            request (GetBucketResourceGroupRequest): Request parameters for GetBucketResourceGroup operation.

        Returns:
            GetBucketResourceGroupResult: Response result for GetBucketResourceGroup operation.
        """
        return operations.get_bucket_resource_group(self._client, request, **kwargs)


    def put_bucket_resource_group(self, request: models.PutBucketResourceGroupRequest, **kwargs
                                  ) -> models.PutBucketResourceGroupResult:
        """
        Modifies the ID of the resource group to which a bucket belongs.

        Args:
            request (PutBucketResourceGroupRequest): Request parameters for PutBucketResourceGroup operation.

        Returns:
            PutBucketResourceGroupResult: Response result for PutBucketResourceGroup operation.
        """
        return operations.put_bucket_resource_group(self._client, request, **kwargs)

    # style
    def put_style(self, request: models.PutStyleRequest, **kwargs
                  ) -> models.PutStyleResult:
        """
        Adds an image style to a bucket. An image style contains one or more image processing parameters.

        Args:
            request (PutStyleRequest): Request parameters for PutStyle operation.

        Returns:
            PutStyleResult: Response result for PutStyle operation.
        """
        return operations.put_style(self._client, request, **kwargs)


    def list_style(self, request: models.ListStyleRequest, **kwargs
                   ) -> models.ListStyleResult:
        """
        Queries all image styles that are created for a bucket.

        Args:
            request (ListStyleRequest): Request parameters for ListStyle operation.

        Returns:
            ListStyleResult: Response result for ListStyle operation.
        """
        return operations.list_style(self._client, request, **kwargs)


    def get_style(self, request: models.GetStyleRequest, **kwargs
                  ) -> models.GetStyleResult:
        """
        Queries the information about an image style of a bucket.

        Args:
            request (GetStyleRequest): Request parameters for GetStyle operation.

        Returns:
            GetStyleResult: Response result for GetStyle operation.
        """
        return operations.get_style(self._client, request, **kwargs)


    def delete_style(self, request: models.DeleteStyleRequest, **kwargs
                     ) -> models.DeleteStyleResult:
        """
        Deletes an image style from a bucket.

        Args:
            request (DeleteStyleRequest): Request parameters for DeleteStyle operation.

        Returns:
            DeleteStyleResult: Response result for DeleteStyle operation.
        """
        return operations.delete_style(self._client, request, **kwargs)


    # bucket tags
    def put_bucket_tags(self, request: models.PutBucketTagsRequest, **kwargs
                        ) -> models.PutBucketTagsResult:
        """
        Adds tags to or modifies the existing tags of a bucket.

        Args:
            request (PutBucketTagsRequest): Request parameters for PutBucketTags operation.

        Returns:
            PutBucketTagsResult: Response result for PutBucketTags operation.
        """
        return operations.put_bucket_tags(self._client, request, **kwargs)


    def get_bucket_tags(self, request: models.GetBucketTagsRequest, **kwargs
                        ) -> models.GetBucketTagsResult:
        """
        Queries the tags of a bucket.

        Args:
            request (GetBucketTagsRequest): Request parameters for GetBucketTags operation.

        Returns:
            GetBucketTagsResult: Response result for GetBucketTags operation.
        """
        return operations.get_bucket_tags(self._client, request, **kwargs)


    def delete_bucket_tags(self, request: models.DeleteBucketTagsRequest, **kwargs
                           ) -> models.DeleteBucketTagsResult:
        """
        Deletes tags configured for a bucket.

        Args:
            request (DeleteBucketTagsRequest): Request parameters for DeleteBucketTags operation.

        Returns:
            DeleteBucketTagsResult: Response result for DeleteBucketTags operation.
        """
        return operations.delete_bucket_tags(self._client, request, **kwargs)


    # meta query
    def open_meta_query(self, request: models.OpenMetaQueryRequest, **kwargs
                        ) -> models.OpenMetaQueryResult:
        """
        Enables metadata management for a bucket. After you enable the metadata management feature for a bucket, Object Storage Service (OSS) creates a metadata index library for the bucket and creates metadata indexes for all objects in the bucket. After the metadata index library is created, OSS continues to perform quasi-real-time scans on incremental objects in the bucket and creates metadata indexes for the incremental objects.

        Args:
            request (OpenMetaQueryRequest): Request parameters for OpenMetaQuery operation.

        Returns:
            OpenMetaQueryResult: Response result for OpenMetaQuery operation.
        """
        return operations.open_meta_query(self._client, request, **kwargs)

    def get_meta_query_status(self, request: models.GetMetaQueryStatusRequest, **kwargs
                              ) -> models.GetMetaQueryStatusResult:
        """
        Queries the information about the metadata index library of a bucket.

        Args:
            request (GetMetaQueryStatusRequest): Request parameters for GetMetaQueryStatus operation.

        Returns:
            GetMetaQueryStatusResult: Response result for GetMetaQueryStatus operation.
        """
        return operations.get_meta_query_status(self._client, request, **kwargs)

    def do_meta_query(self, request: models.DoMetaQueryRequest, **kwargs
                      ) -> models.DoMetaQueryResult:
        """
        Queries the objects in a bucket that meet the specified conditions by using the data indexing feature. The information about the objects is listed based on the specified fields and sorting methods.

        Args:
            request (DoMetaQueryRequest): Request parameters for DoMetaQuery operation.

        Returns:
            DoMetaQueryResult: Response result for DoMetaQuery operation.
        """
        return operations.do_meta_query(self._client, request, **kwargs)

    def close_meta_query(self, request: models.CloseMetaQueryRequest, **kwargs
                         ) -> models.CloseMetaQueryResult:
        """
        Disables the metadata management feature for an Object Storage Service (OSS) bucket. After the metadata management feature is disabled for a bucket, OSS automatically deletes the metadata index library of the bucket and you cannot perform metadata indexing.

        Args:
            request (CloseMetaQueryRequest): Request parameters for CloseMetaQuery operation.

        Returns:
            CloseMetaQueryResult: Response result for CloseMetaQuery operation.
        """
        return operations.close_meta_query(self._client, request, **kwargs)


    # bucket https config
    def get_bucket_https_config(self, request: models.GetBucketHttpsConfigRequest, **kwargs
                                ) -> models.GetBucketHttpsConfigResult:
        """
        Queries the Transport Layer Security (TLS) version configurations of a bucket.

        Args:
            request (GetBucketHttpsConfigRequest): Request parameters for GetBucketHttpsConfig operation.

        Returns:
            GetBucketHttpsConfigResult: Response result for GetBucketHttpsConfig operation.
        """
        return operations.get_bucket_https_config(self._client, request, **kwargs)


    def put_bucket_https_config(self, request: models.PutBucketHttpsConfigRequest, **kwargs
                                ) -> models.PutBucketHttpsConfigResult:
        """
        Enables or disables Transport Layer Security (TLS) version management for a bucket.

        Args:
            request (PutBucketHttpsConfigRequest): Request parameters for PutBucketHttpsConfig operation.

        Returns:
            PutBucketHttpsConfigResult: Response result for PutBucketHttpsConfig operation.
        """
        return operations.put_bucket_https_config(self._client, request, **kwargs)

    # clean restored
    def clean_restored_object(self, request: models.CleanRestoredObjectRequest, **kwargs
                              ) -> models.CleanRestoredObjectResult:
        """
        You can call this operation to clean an object restored from Archive or Cold Archive state. After that, the restored object returns to the frozen state.

        Args:
            request (CleanRestoredObjectRequest): Request parameters for CleanRestoredObject operation.

        Returns:
            CleanRestoredObjectResult: Response result for CleanRestoredObject operation.
        """
        return operations.clean_restored_object(self._client, request, **kwargs)

    # cloud box
    def list_cloud_boxes(self, request: models.ListCloudBoxesRequest, **kwargs
                    ) -> models.ListCloudBoxesResult:
        """
        ListCloudBoxes Lists cloud box buckets that belong to the current account.

        Args:
            request (ListCloudBoxesRequest): Request parameters for ListCloudBoxes operation.

        Returns:
            ListCloudBoxesResult: Response result for ListCloudBoxes operation.
        """

        return operations.list_cloud_boxes(self._client, request, **kwargs)

    # seal append object
    def seal_append_object(self, request: models.SealAppendObjectRequest, **kwargs
                           ) -> models.SealAppendObjectResult:
        """
        This operation stops writing to the Appendable Object, after which the user can configure lifecycle rules to change the storage class of the corresponding Appendable Object to Cold Archive or Deep Cold Archive.

        Args:
            request (SealAppendObjectRequest): Request parameters for SealAppendObject operation.

        Returns:
            SealAppendObjectResult: Response result for SealAppendObject operation.
        """
        return operations.seal_append_object(self._client, request, **kwargs)
    
    # select object
    def select_object(self, request: models.SelectObjectRequest, **kwargs
                         ) -> models.SelectObjectResult:
        """
        SelectObject Executes SQL statements to perform operations on an object and obtains the execution results.

        Args:
            request (SelectObjectRequest): Request parameters for SelectObject operation.

        Returns:
            SelectObjectResult: Response result for SelectObject operation.
        """

        return operations.select_object(self._client, request, **kwargs)

    def create_select_object_meta(self, request: models.CreateSelectObjectMetaRequest, **kwargs
                                  ) -> models.CreateSelectObjectMetaResult:
        """
        CreateSelectObjectMeta You can call the CreateSelectObjectMeta operation to obtain information about an object, such as the total number of rows and the number of splits.

        Args:
            request (CreateSelectObjectMetaRequest): Request parameters for CreateSelectObjectMeta operation.

        Returns:
            CreateSelectObjectMetaResult: Response result for CreateSelectObjectMeta operation.
        """
        return operations.create_select_object_meta(self._client, request, **kwargs)


    def put_bucket_overwrite_config(self, request: models.PutBucketOverwriteConfigRequest, **kwargs
                                    ) -> models.PutBucketOverwriteConfigResult:
        """
        Call the PutBucketOverwriteConfig operation to configure overwrite protection for a bucket. This prevents specified objects from being overwritten.

        Args:
            request (PutBucketOverwriteConfigRequest): Request parameters for PutBucketOverwriteConfig operation.

        Returns:
            PutBucketOverwriteConfigResult: Response result for PutBucketOverwriteConfig operation.
        """
        return operations.put_bucket_overwrite_config(self._client, request, **kwargs)


    def get_bucket_overwrite_config(self, request: models.GetBucketOverwriteConfigRequest, **kwargs
                                    ) -> models.GetBucketOverwriteConfigResult:
        """
        Call the GetBucketOverwriteConfig operation to retrieve the overwrite configuration of a bucket.

        Args:
            request (GetBucketOverwriteConfigRequest): Request parameters for GetBucketOverwriteConfig operation.

        Returns:
            GetBucketOverwriteConfigResult: Response result for GetBucketOverwriteConfig operation.
        """
        return operations.get_bucket_overwrite_config(self._client, request, **kwargs)


    def delete_bucket_overwrite_config(self, request: models.DeleteBucketOverwriteConfigRequest, **kwargs
                                       ) -> models.DeleteBucketOverwriteConfigResult:
        """
        Delete overwrite configuration rule for the bucket.

        Args:
            request (DeleteBucketOverwriteConfigRequest): Request parameters for DeleteBucketOverwriteConfig operation.

        Returns:
            DeleteBucketOverwriteConfigResult: Response result for DeleteBucketOverwriteConfig operation.
        """
        return operations.delete_bucket_overwrite_config(self._client, request, **kwargs)
