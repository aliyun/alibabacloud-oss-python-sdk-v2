# pylint: disable=line-too-long
"""_summary_"""
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
    """_summary_
    """

    def __init__(self, config: Config, **kwargs) -> None:
        """_summary_

        Args:
            config (Config): _description_
        """
        self._client = _SyncClientImpl(config, **kwargs)

    def __repr__(self) -> str:
        return "<OssClient>"

    def invoke_operation(self, op_input: OperationInput, **kwargs
                         ) -> OperationOutput:
        """_summary_

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
            ListBucketsResult: Reponse result for ListBuckets operation.
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
            PutBucketResult: Reponse result for PutBucket operation.
        """

        return operations.put_bucket(self._client, request, **kwargs)

    def delete_bucket(self, request: models.DeleteBucketRequest, **kwargs
                      ) -> models.DeleteBucketResult:
        """
        Deletes a bucket.

        Args:
            request (DeleteBucketRequest): Request parameters for DeleteBucket operation.

        Returns:
            DeleteBucketResult: Reponse result for DeleteBucket operation.
        """

        return operations.delete_bucket(self._client, request, **kwargs)

    def list_objects(self, request: models.ListObjectsRequest, **kwargs
                     ) -> models.ListObjectsResult:
        """
        Lists information about all objects in an Object Storage Service (OSS) bucket.

        Args:
            request (ListObjectsRequest): Request parameters for ListObjects operation.

        Returns:
            ListObjectsResult: Reponse result for ListObjects operation.
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
            ListObjectsV2Result: Reponse result for ListObjectsV2 operation.
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
            ListObjectVersionsResult: Reponse result for ListObjectVersions operation.
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
            PutObjectResult: Reponse result for PutObject operation.
        """

        return operations.put_object(self._client, request, **kwargs)

    def get_object(self, request: models.GetObjectRequest, **kwargs
                   ) -> models.GetObjectResult:
        """
        Queries an object. To call this operation, you must have read permissions on the object.

        Args:
            request (GetObjectRequest): Request parameters for GetObject operation.

        Returns:
            GetObjectResult: Reponse result for GetObject operation.
        """

        return operations.get_object(self._client, request, **kwargs)

    def copy_object(self, request: models.CopyObjectRequest, **kwargs
                    ) -> models.CopyObjectResult:
        """
        Copies objects within a bucket or between buckets in the same region.

        Args:
            request (CopyObjectRequest): Request parameters for CopyObject operation.

        Returns:
            CopyObjectResult: Reponse result for CopyObject operation.
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
            AppendObjectResult: Reponse result for AppendObject operation.
        """

        return operations.append_object(self._client, request, **kwargs)

    def delete_object(self, request: models.DeleteObjectRequest, **kwargs
                    ) -> models.DeleteObjectResult:
        """
        Deletes an object.

        Args:
            request (DeleteObjectRequest): Request parameters for DeleteObject operation.

        Returns:
            DeleteObjectResult: Reponse result for DeleteObject operation.
        """

        return operations.delete_object(self._client, request, **kwargs)

    def delete_multiple_objects(self, request: models.DeleteMultipleObjectsResult, **kwargs
                    ) -> models.DeleteMultipleObjectsResult:
        """
        Deletes multiple objects from a bucket.

        Args:
            request (DeleteMultipleObjectsResult): Request parameters for DeleteMultipleObjects operation.

        Returns:
            DeleteMultipleObjectsResult: Reponse result for DeleteMultipleObjects operation.
        """

        return operations.delete_multiple_objects(self._client, request, **kwargs)

    def head_object(self, request: models.HeadObjectRequest, **kwargs
                    ) -> models.HeadObjectResult:
        """
        Queries information about the object in a bucket.

        Args:
            request (HeadObjectRequest): Request parameters for HeadObject operation.

        Returns:
            HeadObjectResult: Reponse result for HeadObject operation.
        """

        return operations.head_object(self._client, request, **kwargs)

    def get_object_meta(self, request: models.GetObjectMetaRequest, **kwargs
                    ) -> models.GetObjectMetaResult:
        """
        Queries the metadata of an object, including ETag, Size, and LastModified.

        Args:
            request (GetObjectMetaRequest): Request parameters for GetObjectMeta operation.

        Returns:
            GetObjectMetaResult: Reponse result for GetObjectMeta operation.
        """

        return operations.get_object_meta(self._client, request, **kwargs)

    def restore_object(self, request: models.RestoreObjectRequest, **kwargs
                    ) -> models.RestoreObjectResult:
        """
        Restores Archive, Cold Archive, or Deep Cold Archive objects.

        Args:
            request (RestoreObjectRequest): Request parameters for RestoreObject operation.

        Returns:
            RestoreObjectResult: Reponse result for RestoreObject operation.
        """

        return operations.restore_object(self._client, request, **kwargs)

    def put_object_acl(self, request: models.PutObjectAclRequest, **kwargs
                    ) -> models.PutObjectAclResult:
        """
        You can call this operation to modify the access control list (ACL) of an object.

        Args:
            request (PutObjectAclRequest): Request parameters for PutObjectAcl operation.

        Returns:
            PutObjectAclResult: Reponse result for PutObjectAcl operation.
        """

        return operations.put_object_acl(self._client, request, **kwargs)

    def get_object_acl(self, request: models.GetObjectAclRequest, **kwargs
                    ) -> models.GetObjectAclResult:
        """
        Queries the access control list (ACL) of an object in a bucket.

        Args:
            request (GetObjectAclRequest): Request parameters for GetObjectAcl operation.

        Returns:
            GetObjectAclResult: Reponse result for GetObjectAcl operation.
        """

        return operations.get_object_acl(self._client, request, **kwargs)

    def initiate_multipart_upload(self, request: models.InitiateMultipartUploadRequest, **kwargs
                    ) -> models.InitiateMultipartUploadResult:
        """
        Initiates a multipart upload task before you can upload data in parts to Object Storage Service (OSS).

        Args:
            request (InitiateMultipartUploadRequest): Request parameters for InitiateMultipartUpload operation.

        Returns:
            InitiateMultipartUploadResult: Reponse result for InitiateMultipartUpload operation.
        """

        return operations.initiate_multipart_upload(self._client, request, **kwargs)

    def upload_part(self, request: models.UploadPartRequest, **kwargs
                    ) -> models.UploadPartResult:
        """
        Call the UploadPart interface to upload data in blocks (parts) based on the specified Object name and uploadId.

        Args:
            request (UploadPartRequest): Request parameters for UploadPart operation.

        Returns:
            UploadPartResult: Reponse result for UploadPart operation.
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
            UploadPartCopyResult: Reponse result for UploadPartCopy operation.
        """

        return operations.upload_part_copy(self._client, request, **kwargs)

    def complete_multipart_upload(self, request: models.CompleteMultipartUploadRequest, **kwargs
                    ) -> models.CompleteMultipartUploadResult:
        """
        Completes the multipart upload task of an object after all parts of the object are uploaded.

        Args:
            request (CompleteMultipartUploadRequest): Request parameters for CompleteMultipartUpload operation.

        Returns:
            CompleteMultipartUploadResult: Reponse result for CompleteMultipartUpload operation.
        """

        return operations.complete_multipart_upload(self._client, request, **kwargs)

    def abort_multipart_upload(self, request: models.AbortMultipartUploadRequest, **kwargs
                    ) -> models.AbortMultipartUploadResult:
        """
        Cancels a multipart upload task and deletes the parts uploaded in the task.

        Args:
            request (AbortMultipartUploadRequest): Request parameters for AbortMultipartUpload operation.

        Returns:
            AbortMultipartUploadResult: Reponse result for AbortMultipartUpload operation.
        """

        return operations.abort_multipart_upload(self._client, request, **kwargs)

    def list_multipart_uploads(self, request: models.ListMultipartUploadsRequest, **kwargs
                    ) -> models.ListMultipartUploadsResult:
        """
        Lists all multipart upload tasks in progress. The tasks are not completed or canceled.

        Args:
            request (ListMultipartUploadsRequest): Request parameters for ListMultipartUploads operation.

        Returns:
            ListMultipartUploadsResult: Reponse result for ListMultipartUploads operation.
        """

        return operations.list_multipart_uploads(self._client, request, **kwargs)

    def list_parts(self, request: models.ListPartsRequest, **kwargs
                    ) -> models.ListPartsResult:
        """
        Lists all parts that are uploaded by using a specified upload ID.

        Args:
            request (ListPartsRequest): Request parameters for ListParts operation.

        Returns:
            ListPartsResult: Reponse result for ListParts operation.
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
            PutSymlinkResult: Reponse result for PutSymlink operation.
        """

        return operations.put_symlink(self._client, request, **kwargs)

    def get_symlink(self, request: models.GetSymlinkRequest, **kwargs
                    ) -> models.GetSymlinkResult:
        """
        Obtains a symbol link. To perform GetSymlink operations, you must have the read permission on the symbol link.

        Args:
            request (GetSymlinkRequest): Request parameters for GetSymlink operation.

        Returns:
            GetSymlinkResult: Reponse result for GetSymlink operation.
        """

        return operations.get_symlink(self._client, request, **kwargs)

    def put_object_tagging(self, request: models.PutObjectTaggingRequest, **kwargs
                    ) -> models.PutObjectTaggingResult:
        """
        Adds tags to an object or updates the tags added to the object. Each tag added to an object is a key-value pair.

        Args:
            request (PutObjectTaggingRequest): Request parameters for PutObjectTagging operation.

        Returns:
            PutObjectTaggingResult: Reponse result for PutObjectTagging operation.
        """

        return operations.put_object_tagging(self._client, request, **kwargs)

    def get_object_tagging(self, request: models.GetObjectTaggingRequest, **kwargs
                    ) -> models.GetObjectTaggingResult:
        """
        You can call this operation to query the tags of an object.

        Args:
            request (GetObjectTaggingRequest): Request parameters for GetObjectTagging operation.

        Returns:
            GetObjectTaggingResult: Reponse result for GetObjectTagging operation.
        """

        return operations.get_object_tagging(self._client, request, **kwargs)

    def delete_object_tagging(self, request: models.DeleteObjectTaggingRequest, **kwargs
                    ) -> models.DeleteObjectTaggingResult:
        """
        You can call this operation to delete the tags of a specified object.

        Args:
            request (DeleteObjectTaggingRequest): Request parameters for DeleteObjectTagging operation.

        Returns:
            DeleteObjectTaggingResult: Reponse result for DeleteObjectTagging operation.
        """

        return operations.delete_object_tagging(self._client, request, **kwargs)

    def process_object(self, request: models.ProcessObjectRequest, **kwargs
                    ) -> models.ProcessObjectResult:
        """
        Applies process on the specified image file.

        Args:
            request (ProcessObjectRequest): Request parameters for ProcessObject operation.

        Returns:
            ProcessObjectResult: Reponse result for ProcessObject operation.
        """

        return operations.process_object(self._client, request, **kwargs)

    def async_process_object(self, request: models.AsyncProcessObjectRequest, **kwargs
                    ) -> models.AsyncProcessObjectResult:
        """
        Applies async process on the specified image file.

        Args:
            request (AsyncProcessObjectRequest): Request parameters for AsyncProcessObject operation.

        Returns:
            AsyncProcessObjectResult: Reponse result for AsyncProcessObject operation.
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

    def list_objects_v2_paginator(self, **kwargs) -> ListObjectsPaginator:
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
        """_summary_

        Args:

        Returns:
            Downloader: _description_
        """
        return Downloader(self, **kwargs)

    def uploader(self, **kwargs) -> Uploader:
        """_summary_

        Returns:
            Uploader: _description_
        """
        return Uploader(self, **kwargs)

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
        """_summary_

        Args:
            request (models.PutObjectRequest): _description_
            filepath (str): _description_

        Returns:
            models.PutObjectResult: _description_
        """
        with open(filepath, 'rb') as f:
            req = copy.copy(request)
            req.body = f
            return self.put_object(req, **kwargs)

    def get_object_to_file(self, request: models.GetObjectRequest, filepath: str, **kwargs) -> models.GetObjectResult:
        """_summary_

        Args:
            request (models.GetObjectRequest): _description_
            filepath (str): _description_

        Returns:
            models.GetObjectResult: _description_
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
