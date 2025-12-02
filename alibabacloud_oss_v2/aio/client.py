# pylint: disable=line-too-long
"""Client used to interact with **Alibaba Cloud Object Storage Service (OSS)**."""
from typing import Optional, Type
from types import TracebackType
from ..config import Config
from ..types import OperationInput, OperationOutput
from .. import models
from .. import exceptions
from ._aioclient import _AsyncClientImpl
from . import operations

class AsyncClient:
    """AsyncClient
    """

    def __init__(self, config: Config, **kwargs) -> None:
        """Initialize Client

        Args:
            config (Config): _description_
        """
        self._client = _AsyncClientImpl(config, **kwargs)

    def __repr__(self) -> str:
        return "<OSSAsyncClient>"

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        await self.close()


    async def close(self):
        """_summary_
        """
        await self._client.close()

    async def invoke_operation(self, op_input: OperationInput, **kwargs
                         ) -> OperationOutput:
        """invoke operation

        Args:
            op_input (OperationInput): _description_

        Returns:
            OperationOutput: _description_
        """
        return await self._client.invoke_operation(op_input, **kwargs)

    # sevice
    async def list_buckets(self, request: models.ListBucketsRequest, **kwargs
                     ) -> models.ListBucketsResult:
        """
        Lists all buckets that belong to your Alibaba Cloud account.

        Args:
            request (ListBucketsRequest): Request parameters for ListBuckets operation.

        Returns:
            ListBucketsResult: Response result for ListBuckets operation.
        """

        return await operations.list_buckets(self._client, request, **kwargs)

    # region
    async def describe_regions(self, request: models.DescribeRegionsRequest, **kwargs
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

        return await operations.describe_regions(self._client, request, **kwargs)

    # bucket
    async def put_bucket(self, request: models.PutBucketRequest, **kwargs
                   ) -> models.PutBucketResult:
        """
        Creates a bucket.

        Args:
            request (PutBucketRequest): Request parameters for PutBucket operation.

        Returns:
            PutBucketResult: Response result for PutBucket operation.
        """

        return await operations.put_bucket(self._client, request, **kwargs)

    async def delete_bucket(self, request: models.DeleteBucketRequest, **kwargs
                      ) -> models.DeleteBucketResult:
        """
        Deletes a bucket.

        Args:
            request (DeleteBucketRequest): Request parameters for DeleteBucket operation.

        Returns:
            DeleteBucketResult: Response result for DeleteBucket operation.
        """

        return await operations.delete_bucket(self._client, request, **kwargs)

    async def list_objects(self, request: models.ListObjectsRequest, **kwargs
                     ) -> models.ListObjectsResult:
        """
        Lists information about all objects in an Object Storage Service (OSS) bucket.

        Args:
            request (ListObjectsRequest): Request parameters for ListObjects operation.

        Returns:
            ListObjectsResult: Response result for ListObjects operation.
        """

        return await operations.list_objects(self._client, request, **kwargs)

    async def put_bucket_acl(self, request: models.PutBucketAclRequest, **kwargs
                       ) -> models.PutBucketAclResult:
        """
        You can call this operation to configure or modify the ACL of a bucket.

        Args:
            request (PutBucketAclRequest): Request parameters for PutBucketAcl operation.

        Returns:
            PutBucketAclResult: Response result for PutBucketAcl operation.
        """

        return await operations.put_bucket_acl(self._client, request, **kwargs)

    async def get_bucket_acl(self, request: models.GetBucketAclRequest, **kwargs
                       ) -> models.GetBucketAclResult:
        """
        You can call this operation to query the ACL of a bucket.
        Only the bucket owner can query the ACL of the bucket.

        Args:
            request (GetBucketAclRequest): Request parameters for GetBucketAcl operation.

        Returns:
            GetBucketAclResult: Response result for GetBucketAcl operation.
        """

        return await operations.get_bucket_acl(self._client, request, **kwargs)

    async def list_objects_v2(self, request: models.ListObjectsV2Request, **kwargs
                        ) -> models.ListObjectsV2Result:
        """
        Lists all objects in a bucket.

        Args:
            request (ListObjectsV2Request): Request parameters for ListObjectsV2 operation.

        Returns:
            ListObjectsV2Result: Response result for ListObjectsV2 operation.
        """

        return await operations.list_objects_v2(self._client, request, **kwargs)

    async def get_bucket_stat(self, request: models.GetBucketStatRequest, **kwargs
                        ) -> models.GetBucketStatResult:
        """
        GetBucketStat Queries the storage capacity of a specified bucket and
        the number of objects that are stored in the bucket.

        Args:
            request (GetBucketStatRequest): Request parameters for GetBucketStat operation.

        Returns:
            GetBucketStatResult: Response result for GetBucketStat operation.
        """

        return await operations.get_bucket_stat(self._client, request, **kwargs)

    async def get_bucket_location(self, request: models.GetBucketLocationRequest, **kwargs
                            ) -> models.GetBucketLocationResult:
        """
        GetBucketLocation Queries the region of an Object Storage Service (OSS) bucket.

        Args:
            request (GetBucketLocationRequest): Request parameters for GetBucketLocation operation.

        Returns:
            GetBucketLocationResult: Response result for GetBucketLocation operation.
        """

        return await operations.get_bucket_location(self._client, request, **kwargs)

    async def get_bucket_info(self, request: models.GetBucketInfoRequest, **kwargs
                        ) -> models.GetBucketInfoResult:
        """
        GetBucketInfo Queries information about a bucket.

        Args:
            request (GetBucketInfoRequest): Request parameters for GetBucketInfo operation.

        Returns:
            GetBucketInfoResult: Response result for GetBucketInfo operation.
        """

        return await operations.get_bucket_info(self._client, request, **kwargs)

    async def put_bucket_versioning(self, request: models.PutBucketVersioningRequest, **kwargs
                              ) -> models.PutBucketVersioningResult:
        """
        PutBucketVersioning Configures the versioning state for a bucket.

        Args:
            request (PutBucketVersioningRequest): Request parameters for PutBucketVersioning operation.

        Returns:
            PutBucketVersioningResult: Response result for PutBucketVersioning operation.
        """

        return await operations.put_bucket_versioning(self._client, request, **kwargs)

    async def get_bucket_versioning(self, request: models.GetBucketVersioningRequest, **kwargs
                              ) -> models.GetBucketVersioningResult:
        """
        GetBucketVersioning You can call this operation to query the versioning state of a bucket.

        Args:
            request (GetBucketVersioningRequest): Request parameters for GetBucketVersioning operation.

        Returns:
            GetBucketVersioningResult: Response result for GetBucketVersioning operation.
        """

        return await operations.get_bucket_versioning(self._client, request, **kwargs)

    async def list_object_versions(self, request: models.ListObjectVersionsRequest, **kwargs
                             ) -> models.ListObjectVersionsResult:
        """
        ListObjectVersions Lists the versions of all objects in a bucket, including delete markers.

        Args:
            request (ListObjectVersionsRequest): Request parameters for ListObjectVersions operation.

        Returns:
            ListObjectVersionsResult: Response result for ListObjectVersions operation.
        """

        return await operations.list_object_versions(self._client, request, **kwargs)

    # object
    async def put_object(self, request: models.PutObjectRequest, **kwargs
                   ) -> models.PutObjectResult:
        """
        Uploads objects.

        Args:
            request (PutObjectRequest): Request parameters for PutObject operation.

        Returns:
            PutObjectResult: Response result for PutObject operation.
        """

        return await operations.put_object(self._client, request, **kwargs)

    async def get_object(self, request: models.GetObjectRequest, **kwargs
                   ) -> models.GetObjectResult:
        """
        Queries an object. To call this operation, you must have read permissions on the object.

        Args:
            request (GetObjectRequest): Request parameters for GetObject operation.

        Returns:
            GetObjectResult: Response result for GetObject operation.
        """

        return await operations.get_object(self._client, request, **kwargs)

    async def copy_object(self, request: models.CopyObjectRequest, **kwargs
                    ) -> models.CopyObjectResult:
        """
        Copies objects within a bucket or between buckets in the same region.

        Args:
            request (CopyObjectRequest): Request parameters for CopyObject operation.

        Returns:
            CopyObjectResult: Response result for CopyObject operation.
        """

        return await operations.copy_object(self._client, request, **kwargs)

    async def append_object(self, request: models.AppendObjectRequest, **kwargs
                      ) -> models.AppendObjectResult:
        """
        Uploads an object by appending the object to an existing object.
        Objects created by using the AppendObject operation are appendable objects.

        Args:
            request (AppendObjectRequest): Request parameters for AppendObject operation.

        Returns:
            AppendObjectResult: Response result for AppendObject operation.
        """

        return await operations.append_object(self._client, request, **kwargs)

    async def delete_object(self, request: models.DeleteObjectRequest, **kwargs
                    ) -> models.DeleteObjectResult:
        """
        Deletes an object.

        Args:
            request (DeleteObjectRequest): Request parameters for DeleteObject operation.

        Returns:
            DeleteObjectResult: Response result for DeleteObject operation.
        """

        return await operations.delete_object(self._client, request, **kwargs)

    async def delete_multiple_objects(self, request: models.DeleteMultipleObjectsRequest, **kwargs
                    ) -> models.DeleteMultipleObjectsResult:
        """
        Deletes multiple objects from a bucket.

        Args:
            request (DeleteMultipleObjectsRequest): Request parameters for DeleteMultipleObjects operation.

        Returns:
            DeleteMultipleObjectsResult: Response result for DeleteMultipleObjects operation.
        """

        return await operations.delete_multiple_objects(self._client, request, **kwargs)

    async def head_object(self, request: models.HeadObjectRequest, **kwargs
                    ) -> models.HeadObjectResult:
        """
        Queries information about the object in a bucket.

        Args:
            request (HeadObjectRequest): Request parameters for HeadObject operation.

        Returns:
            HeadObjectResult: Response result for HeadObject operation.
        """

        return await operations.head_object(self._client, request, **kwargs)

    async def get_object_meta(self, request: models.GetObjectMetaRequest, **kwargs
                    ) -> models.GetObjectMetaResult:
        """
        Queries the metadata of an object, including ETag, Size, and LastModified.

        Args:
            request (GetObjectMetaRequest): Request parameters for GetObjectMeta operation.

        Returns:
            GetObjectMetaResult: Response result for GetObjectMeta operation.
        """

        return await operations.get_object_meta(self._client, request, **kwargs)

    async def restore_object(self, request: models.RestoreObjectRequest, **kwargs
                    ) -> models.RestoreObjectResult:
        """
        Restores Archive, Cold Archive, or Deep Cold Archive objects.

        Args:
            request (RestoreObjectRequest): Request parameters for RestoreObject operation.

        Returns:
            RestoreObjectResult: Response result for RestoreObject operation.
        """

        return await operations.restore_object(self._client, request, **kwargs)

    async def put_object_acl(self, request: models.PutObjectAclRequest, **kwargs
                    ) -> models.PutObjectAclResult:
        """
        You can call this operation to modify the access control list (ACL) of an object.

        Args:
            request (PutObjectAclRequest): Request parameters for PutObjectAcl operation.

        Returns:
            PutObjectAclResult: Response result for PutObjectAcl operation.
        """

        return await operations.put_object_acl(self._client, request, **kwargs)

    async def get_object_acl(self, request: models.GetObjectAclRequest, **kwargs
                    ) -> models.GetObjectAclResult:
        """
        Queries the access control list (ACL) of an object in a bucket.

        Args:
            request (GetObjectAclRequest): Request parameters for GetObjectAcl operation.

        Returns:
            GetObjectAclResult: Response result for GetObjectAcl operation.
        """

        return await operations.get_object_acl(self._client, request, **kwargs)

    async def initiate_multipart_upload(self, request: models.InitiateMultipartUploadRequest, **kwargs
                    ) -> models.InitiateMultipartUploadResult:
        """
        Initiates a multipart upload task before you can upload data in parts to Object Storage Service (OSS).

        Args:
            request (InitiateMultipartUploadRequest): Request parameters for InitiateMultipartUpload operation.

        Returns:
            InitiateMultipartUploadResult: Response result for InitiateMultipartUpload operation.
        """

        return await operations.initiate_multipart_upload(self._client, request, **kwargs)

    async def upload_part(self, request: models.UploadPartRequest, **kwargs
                    ) -> models.UploadPartResult:
        """
        Call the UploadPart interface to upload data in blocks (parts) based on the specified Object name and uploadId.

        Args:
            request (UploadPartRequest): Request parameters for UploadPart operation.

        Returns:
            UploadPartResult: Response result for UploadPart operation.
        """

        return await operations.upload_part(self._client, request, **kwargs)

    async def upload_part_copy(self, request: models.UploadPartCopyRequest, **kwargs
                    ) -> models.UploadPartCopyResult:
        """
        You can call this operation to copy data from an existing object to upload a part
        by adding a x-oss-copy-request header to UploadPart.

        Args:
            request (UploadPartCopyRequest): Request parameters for UploadPartCopy operation.

        Returns:
            UploadPartCopyResult: Response result for UploadPartCopy operation.
        """

        return await operations.upload_part_copy(self._client, request, **kwargs)

    async def complete_multipart_upload(self, request: models.CompleteMultipartUploadRequest, **kwargs
                    ) -> models.CompleteMultipartUploadResult:
        """
        Completes the multipart upload task of an object after all parts of the object are uploaded.

        Args:
            request (CompleteMultipartUploadRequest): Request parameters for CompleteMultipartUpload operation.

        Returns:
            CompleteMultipartUploadResult: Response result for CompleteMultipartUpload operation.
        """

        return await operations.complete_multipart_upload(self._client, request, **kwargs)

    async def abort_multipart_upload(self, request: models.AbortMultipartUploadRequest, **kwargs
                    ) -> models.AbortMultipartUploadResult:
        """
        Cancels a multipart upload task and deletes the parts uploaded in the task.

        Args:
            request (AbortMultipartUploadRequest): Request parameters for AbortMultipartUpload operation.

        Returns:
            AbortMultipartUploadResult: Response result for AbortMultipartUpload operation.
        """

        return await operations.abort_multipart_upload(self._client, request, **kwargs)

    async def list_multipart_uploads(self, request: models.ListMultipartUploadsRequest, **kwargs
                    ) -> models.ListMultipartUploadsResult:
        """
        Lists all multipart upload tasks in progress. The tasks are not completed or canceled.

        Args:
            request (ListMultipartUploadsRequest): Request parameters for ListMultipartUploads operation.

        Returns:
            ListMultipartUploadsResult: Response result for ListMultipartUploads operation.
        """

        return await operations.list_multipart_uploads(self._client, request, **kwargs)

    async def list_parts(self, request: models.ListPartsRequest, **kwargs
                    ) -> models.ListPartsResult:
        """
        Lists all parts that are uploaded by using a specified upload ID.

        Args:
            request (ListPartsRequest): Request parameters for ListParts operation.

        Returns:
            ListPartsResult: Response result for ListParts operation.
        """

        return await operations.list_parts(self._client, request, **kwargs)

    async def put_symlink(self, request: models.PutSymlinkRequest, **kwargs
                    ) -> models.PutSymlinkResult:
        """
        Creates a symbolic link that points to a destination object.
        You can use the symbolic link to access the destination object.

        Args:
            request (PutSymlinkRequest): Request parameters for PutSymlink operation.

        Returns:
            PutSymlinkResult: Response result for PutSymlink operation.
        """

        return await operations.put_symlink(self._client, request, **kwargs)

    async def get_symlink(self, request: models.GetSymlinkRequest, **kwargs
                    ) -> models.GetSymlinkResult:
        """
        Obtains a symbol link. To perform GetSymlink operations, you must have the read permission on the symbol link.

        Args:
            request (GetSymlinkRequest): Request parameters for GetSymlink operation.

        Returns:
            GetSymlinkResult: Response result for GetSymlink operation.
        """

        return await operations.get_symlink(self._client, request, **kwargs)

    async def put_object_tagging(self, request: models.PutObjectTaggingRequest, **kwargs
                    ) -> models.PutObjectTaggingResult:
        """
        Adds tags to an object or updates the tags added to the object. Each tag added to an object is a key-value pair.

        Args:
            request (PutObjectTaggingRequest): Request parameters for PutObjectTagging operation.

        Returns:
            PutObjectTaggingResult: Response result for PutObjectTagging operation.
        """

        return await operations.put_object_tagging(self._client, request, **kwargs)

    async def get_object_tagging(self, request: models.GetObjectTaggingRequest, **kwargs
                    ) -> models.GetObjectTaggingResult:
        """
        You can call this operation to query the tags of an object.

        Args:
            request (GetObjectTaggingRequest): Request parameters for GetObjectTagging operation.

        Returns:
            GetObjectTaggingResult: Response result for GetObjectTagging operation.
        """

        return await operations.get_object_tagging(self._client, request, **kwargs)

    async def delete_object_tagging(self, request: models.DeleteObjectTaggingRequest, **kwargs
                    ) -> models.DeleteObjectTaggingResult:
        """
        You can call this operation to delete the tags of a specified object.

        Args:
            request (DeleteObjectTaggingRequest): Request parameters for DeleteObjectTagging operation.

        Returns:
            DeleteObjectTaggingResult: Response result for DeleteObjectTagging operation.
        """

        return await operations.delete_object_tagging(self._client, request, **kwargs)

    async def process_object(self, request: models.ProcessObjectRequest, **kwargs
                    ) -> models.ProcessObjectResult:
        """
        Applies process on the specified image file.

        Args:
            request (ProcessObjectRequest): Request parameters for ProcessObject operation.

        Returns:
            ProcessObjectResult: Response result for ProcessObject operation.
        """

        return await operations.process_object(self._client, request, **kwargs)

    async def async_process_object(self, request: models.AsyncProcessObjectRequest, **kwargs
                    ) -> models.AsyncProcessObjectResult:
        """
        Applies async process on the specified image file.

        Args:
            request (AsyncProcessObjectRequest): Request parameters for AsyncProcessObject operation.

        Returns:
            AsyncProcessObjectResult: Response result for AsyncProcessObject operation.
        """

        return await operations.async_process_object(self._client, request, **kwargs)

    async def seal_append_object(self, request: models.SealAppendObjectRequest, **kwargs
                    ) -> models.SealAppendObjectResult:
        """
        Seals an appendable object. After an object is sealed, you cannot append data to the object.

        Args:
            request (SealAppendObjectRequest): Request parameters for SealAppendObject operation.

        Returns:
            SealAppendObjectResult: Response result for SealAppendObject operation.
        """

        return await operations.seal_append_object(self._client, request, **kwargs)

    # others apis
    async def is_object_exist(self, bucket: str, key: str,
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
            result = await self.get_object_meta(models.GetObjectMetaRequest(
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

    async def is_bucket_exist(self, bucket: str, request_payer: Optional[str] = None, **kwargs) -> bool:
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
            result = await self.get_bucket_acl(models.GetBucketAclRequest(
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
