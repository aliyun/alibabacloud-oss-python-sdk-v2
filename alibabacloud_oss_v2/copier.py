"""Copier for handling objects for uploads."""
# pylint: disable=line-too-long, broad-exception-caught
import abc
import copy
import os
import concurrent.futures
import threading
from typing import Any, Optional, IO, MutableMapping, List
from . import exceptions, HeadObjectResult, GetObjectTaggingResult
from . import models
from . import validation
from . import utils
from . import defaults
from .serde import copy_request
from .paginator import ListPartsPaginator

metadata_copied = {
    "content-type": None,
    "content-language": None,
    "content-encoding": None,
    "content-disposition": None,
    "cache-control": None,
    "expires": None,
}

class CopyAPIClient(abc.ABC):
    """Abstract base class for copier client."""

    @abc.abstractmethod
    def copy_object(self, request: models.CopyObjectRequest, **kwargs) -> models.CopyObjectResult:
        """Copies objects."""

    @abc.abstractmethod
    def head_object(self, request: models.HeadObjectRequest, **kwargs) -> models.HeadObjectResult:
        """Queries information about the object in a bucket."""

    @abc.abstractmethod
    def initiate_multipart_upload(self, request: models.InitiateMultipartUploadRequest, **kwargs
                    ) -> models.InitiateMultipartUploadResult:
        """
        Initiates a multipart upload task before you can upload data
        in parts to Object Storage Service (OSS).
        """

    @abc.abstractmethod
    def upload_part_copy(self, request: models.UploadPartCopyRequest, **kwargs) -> models.UploadPartCopyResult:
        """
        You can call this operation to copy data from an existing object to upload a part
        by adding a x-oss-copy-request header to UploadPart.
        """

    @abc.abstractmethod
    def complete_multipart_upload(self, request: models.CompleteMultipartUploadRequest, **kwargs
                    ) -> models.CompleteMultipartUploadResult:
        """
        Completes the multipart upload task of an object after all parts
        of the object are uploaded.
        """

    @abc.abstractmethod
    def abort_multipart_upload(self, request: models.AbortMultipartUploadRequest, **kwargs
                    ) -> models.AbortMultipartUploadResult:
        """
        Cancels a multipart upload task and deletes the parts uploaded in the task.
        """

    @abc.abstractmethod
    def list_parts(self, request: models.ListPartsRequest, **kwargs
                    ) -> models.ListPartsResult:
        """
        Lists all parts that are uploaded by using a specified upload ID.
        """
    @abc.abstractmethod
    def get_object_tagging(self, request: models.GetObjectTaggingRequest, **kwargs
                    ) -> models.GetObjectTaggingResult:
        """
        You can call this operation to query the tags of an object.
        """

class CopierOptions:
    """_summary_
    """

    def __init__(
        self,
        part_size: Optional[int] = None,
        parallel_num: Optional[int] = None,
        leave_parts_on_error: Optional[bool] = None,
        disable_shallow_copy: Optional[bool] = None,
        metadata_properties: Optional[HeadObjectResult] = None,
        tag_properties: Optional[GetObjectTaggingResult] = None,
    ) -> None:
        self.part_size = part_size
        self.parallel_num = parallel_num
        self.leave_parts_on_error = leave_parts_on_error or False
        self.disable_shallow_copy = disable_shallow_copy or False
        self.metadata_properties = metadata_properties
        self.tag_properties = tag_properties


class CopyResult:
    """_summary_
    """

    def __init__(
        self,
        upload_id: Optional[str] = None,
        etag: Optional[str] = None,
        version_id: Optional[str] = None,
        hash_crc64: Optional[str] = None,
    ) -> None:
        self.upload_id = upload_id
        self.etag = etag
        self.version_id = version_id
        self.hash_crc64 = hash_crc64

        self.status = ''
        self.status_code = 0
        self.request_id = ''
        self.headers: MutableMapping[str, str] = {}

class CopyError(exceptions.BaseError):
    """
    Copy Error.
    """
    fmt = 'copy failed, {upload_id}, {path}, {error}.'

    def __init__(self, **kwargs):
        exceptions.BaseError.__init__(self, **kwargs)
        self._error = kwargs.get("error", None)
        self.upload_id = kwargs.get("upload_id", None)
        self.path = kwargs.get("path", None)

    def unwrap(self) -> Exception:
        """returns the detail error"""
        return self._error


class Copier:
    """Copy for handling objects for uploads."""

    def __init__(
        self,
        client: CopyAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (CopyAPIClient): A agent that implements the CopyObject and Multipart Copy api.
        """
        part_size = kwargs.get('part_size', defaults.DEFAULT_UPLOAD_PART_SIZE)
        parallel_num = kwargs.get('parallel_num', defaults.DEFAULT_UPLOAD_PARALLEL)
        leave_parts_on_error = kwargs.get('leave_parts_on_error', False)
        self._client = client
        self._options = CopierOptions(
            part_size=part_size,
            parallel_num=parallel_num,
            leave_parts_on_error=leave_parts_on_error,
            disable_shallow_copy=kwargs.get('disable_shallow_copy', False),
        )

        feature_flags = 0
        is_eclient = False
        cstr = str(client)
        if cstr == '<OssClient>':
            feature_flags = client._client._options.feature_flags
        elif cstr == '<OssEncryptionClient>':
            feature_flags = client.unwrap()._client._options.feature_flags
            is_eclient = True
        self._feature_flags = feature_flags
        self._is_eclient = is_eclient


    def copy(
        self,
        request: models.CopyObjectRequest,
        **kwargs: Any
    ) -> CopyResult:
        """_summary_

        Args:
            request (models.CopyObjectRequest): _description_
            reader (IO[bytes]): _description_

        Returns:
            CopyResult: _description_
        """
        delegate = self._delegate(request, **kwargs)
        delegate.check_source()
        delegate.apply_source()
        return delegate.copy()

    def _delegate(
        self,
        request: models.CopyObjectRequest,
        **kwargs: Any
    ) -> "_CopierDelegate":

        if request is None:
            raise exceptions.ParamNullError(field='request')

        if not validation.is_valid_bucket_name(utils.safety_str(request.bucket)):
            raise exceptions.ParamInvalidError(field='request.bucket')

        if not validation.is_valid_object_name(utils.safety_str(request.key)):
            raise exceptions.ParamInvalidError(field='request.key')


        options = copy.copy(self._options)
        options.part_size = kwargs.get('part_size', self._options.part_size)
        options.parallel_num = kwargs.get('parallel_num', self._options.parallel_num)
        options.leave_parts_on_error = kwargs.get('leave_parts_on_error', self._options.leave_parts_on_error)
        options.disable_shallow_copy = kwargs.get('disable_shallow_copy', self._options.disable_shallow_copy)

        if options.part_size <= 0:
            options.part_size = defaults.DEFAULT_UPLOAD_PART_SIZE

        if options.parallel_num <= 0:
            options.parallel_num = defaults.DEFAULT_UPLOAD_PARALLEL

        delegate = _CopierDelegate(
            base=self,
            client=self._client,
            request=request,
            options=options
        )

        return delegate


class _CopyContext:
    def __init__(
        self,
        upload_id: str = None,
        start_num: int = None,
    ) -> None:
        self.upload_id = upload_id
        self.start_num = start_num


class _CopierDelegate:
    def __init__(
        self,
        base: Copier,
        client: CopyAPIClient,
        request: models.CopyObjectRequest,
        options: CopierOptions,
        metadata_prop: Optional[HeadObjectResult] = None,
        tag_prop: Optional[GetObjectTaggingResult] = None,
    ) -> None:
        """
        """
        self._base = base
        self._client = client
        self._reqeust = request
        self._options = options
        self._metadata_prop = metadata_prop
        self._tag_prop = tag_prop

        parallel = options.parallel_num > 1
        self._progress_lock = threading.Lock() if parallel else None

        self._reader_pos = 0
        self._total_size = 0
        self._transferred = 0
        self._reader_seekable = False

        #Source's Info
        self._filepath: str = None
        self._file_stat: os.stat_result = None

        #checkpoint
        self._checkpoint = None

        #CRC
        self._check_crc = False
        self._ccrc = 0

        #use mulitpart upload
        self._copy_part_lock = None
        self._copy_errors = []
        self._copy_parts = []

        # resumable upload
        self._upload_id = None
        self._part_number = None


    def check_source(self):
        """_summary_
        """
        if self._metadata_prop is not None:
            return

        request = models.HeadObjectRequest()
        copy_request(request, self._reqeust)
        if self._reqeust.source_bucket is not None:
            request.bucket = self._reqeust.source_bucket
        request.key = self._reqeust.source_key
        request.version_id = self._reqeust.source_version_id
        result = self._client.head_object(request)
        self._metadata_prop = result


    def apply_source(self):
        """_summary_
        """

        total_size = self._metadata_prop.content_length
        if total_size is None:
            total_size = -1
        part_size = self._options.part_size

        if total_size > 0:
            while self._total_size/part_size >= defaults.MAX_UPLOAD_PARTS:
                part_size += self._options.part_size

        self._options.part_size = part_size
        self._total_size = total_size

    def can_use_shallow_copy(self):
        if self._options.disable_shallow_copy:
            return False

        if self._reqeust.storage_class:
            return False

        if self._reqeust.source_bucket and self._reqeust.source_bucket != self._reqeust.bucket:
            return False

        if self._metadata_prop.server_side_encryption:
            return False

        return True

    def update_crc_flag(self):
        """_summary_
        """
        #FF_ENABLE_CRC64_CHECK_UPLOAD = 0x00000008
        if (self._base._feature_flags & 0x00000008) > 0:
            self._check_crc = True


    def copy(self) -> CopyResult:
        """_summary_
        """
        if 0 <= self._total_size <= self._options.part_size:
            return self._single_copy()
        elif self.can_use_shallow_copy():
            return self._shallow_copy()
        return self._multipart_copy()

    def _single_copy(self) -> CopyResult:
        request = models.CopyObjectRequest()
        copy_request(request, self._reqeust)

        if request.content_type is None:
            request.content_type = self._get_content_type()

        try:
            result = self._client.copy_object(request)
        except Exception as err:
            raise self._wrap_error('', err)

        self._transferred = self._total_size

        ret = CopyResult(
            etag=result.etag,
            version_id=result.version_id,
            hash_crc64=result.hash_crc64,
        )
        ret.status = result.status
        ret.status_code = result.status_code
        ret.request_id = result.request_id
        ret.headers = result.headers

        return ret

    def _shallow_copy(self) -> (CopyResult):
        request = models.CopyObjectRequest()
        copy_request(request, self._reqeust)

        if request.content_type is None:
            request.content_type = self._get_content_type()

        # timer_thread = threading.Timer(60 * 30, self.timeout_handle(self._upload_id))
        # timer_thread.start()
        try:
            result = self._client.copy_object(request)
        except exceptions.TimeoutError:
            return self._multipart_copy()
        except Exception as err:
            raise self._wrap_error(self._upload_id, err)
        # finally:
            # timer_thread.cancel()

        self._transferred = self._total_size

        ret = CopyResult(
            etag=result.etag,
            version_id=result.version_id,
            hash_crc64=result.hash_crc64,
        )
        ret.status = result.status
        ret.status_code = result.status_code
        ret.request_id = result.request_id
        ret.headers = result.headers

        return ret

    def _multipart_copy(self) -> CopyResult:
        # init the multipart
        try:
            upload_ctx = self._get_upload_context()
        except Exception as err:
            raise self._wrap_error('', err)

        # upload part
        parallel = self._options.parallel_num > 1
        if parallel:
            self._copy_part_lock = threading.Lock()
            with concurrent.futures.ThreadPoolExecutor(self._options.parallel_num) as executor:
                for result in executor.map(self._copy_part, self._iter_part(upload_ctx)):
                    self._update_upload_result(result)
        else:
            for part in self._iter_part(upload_ctx):
                self._update_upload_result(self._copy_part(part))
                if len(self._copy_errors) > 0:
                    break

        
        # complete upload
        cmresult: models.CompleteMultipartUploadResult = None
        if len(self._copy_errors) == 0:
            request = models.CompleteMultipartUploadRequest()
            copy_request(request, self._reqeust)
            parts = sorted(self._copy_parts, key=lambda p: p.part_number)
            request.upload_id = upload_ctx.upload_id
            request.complete_multipart_upload = models.CompleteMultipartUpload(parts=parts)
            try:
                cmresult = self._client.complete_multipart_upload(request)
            except Exception as err:
                self._copy_errors.append(err)

        # check last error
        if len(self._copy_errors) > 0:
            if not self._options.leave_parts_on_error:
                try:
                    abort_request = models.AbortMultipartUploadRequest()
                    abort_request.upload_id = upload_ctx.upload_id
                    copy_request(request, self._reqeust)
                    self._client.abort_multipart_upload(abort_request)
                except Exception as _:
                    pass
            raise self._wrap_error(upload_ctx.upload_id, self._copy_errors[-1])

        self._assert_crc_same(cmresult.headers)

        ret = CopyResult(
            upload_id=upload_ctx.upload_id,
            etag=cmresult.etag,
            version_id=cmresult.version_id,
            hash_crc64=cmresult.hash_crc64,
        )
        ret.status = cmresult.status
        ret.status_code = cmresult.status_code
        ret.request_id = cmresult.request_id
        ret.headers = cmresult.headers

        return ret


    def _get_upload_context(self) -> _CopyContext:
        if self._upload_id:
            return _CopyContext(
                upload_id=self._upload_id,
                start_num=self._part_number - 1,
            )

	    #if not exist or fail, create a new upload id
        request = models.InitiateMultipartUploadRequest()
        copy_request(request, self._reqeust)
        if request.content_type is None:
            request.content_type = self._get_content_type()

        self.overwrite_metadata_prop(request)

        self.overwrite_tag_prop(request)

        result = self._client.initiate_multipart_upload(request)

        return _CopyContext(
            upload_id=result.upload_id,
            start_num=0,
        )

    def _iter_part(self, upload_ctx: _CopyContext):
        start_part_num = upload_ctx.start_num

        while len(self._copy_errors) == 0:
            try:
                n = self._options.part_size
                bytes_left = self._total_size - self._reader_pos

                if bytes_left <= 0:
                    break
                if bytes_left < n:
                    n = bytes_left

                range_end = self._reader_pos + n - 1
                range = f'bytes={self._reader_pos}-{range_end}'
                self._reader_pos += n

                # range = next_range()
            except Exception as err:
                self._save_error(err)
                break


            start_part_num += 1
            yield upload_ctx.upload_id, start_part_num, range


    def _copy_part(self, part):
        # When an error occurs, ignore other upload requests
        if len(self._copy_errors) > 0:
            return None

        upload_id = part[0]
        part_number = part[1]
        range = part[2]
        error: Exception = None
        etag = None

        try:
            result = self._client.upload_part_copy(models.UploadPartCopyRequest(
                bucket=self._reqeust.bucket,
                key=self._reqeust.key,
                upload_id=upload_id,
                part_number=part_number,
                source_bucket=self._reqeust.source_bucket,
                source_key=self._reqeust.source_key,
                source_range=range,
                request_payer=self._reqeust.request_payer
            ))
            etag = result.etag

        except Exception as err:
            error = err

        return part_number, etag, error


    def _save_error(self, error) -> None:
        if self._copy_part_lock:
            with self._copy_part_lock:
                self._copy_errors.append(error)
        else:
            self._copy_errors.append(error)


    def _get_content_type(self) -> str:
        if self._filepath is not None:
            return utils.guess_content_type(self._filepath, 'application/octet-stream')
        return None

    def _iter_uploaded_part(self):
        if self._upload_id is None:
            return
        try:
            paginator = ListPartsPaginator(self._client)
            iterator = paginator.iter_page(models.ListPartsRequest(
                bucket=self._reqeust.bucket,
                key=self._reqeust.key,
                request_payer=self._reqeust.request_payer,
                upload_id=self._upload_id,
            ))
            check_part_number = 1
            for page in iterator:
                for part in page.parts:
                    if (part.part_number != check_part_number or
                        part.size != self._options.part_size):
                        return
                    yield part
                    check_part_number += 1
        except Exception:
            self._upload_id = None

    def _update_upload_result(self, result):
        if result is None:
            return

        if result[2] is not None:
            self._save_error(result[2])
            return

        part_number = result[0]
        etag = result[1]

        self._copy_parts.append(models.UploadPart(part_number=part_number, etag=etag))

    def overwrite_metadata_prop(self, im_request: models.InitiateMultipartUploadRequest):
        copy_request = self._reqeust
        metadata_directive = str(copy_request.metadata_directive).lower()

        if metadata_directive in ["none", "", "copy"]:
            if self._metadata_prop is None:
                return Exception(f"request.MetadataDirective is COPY, but meets nil metaProp for source")

            im_request.cache_control = None
            im_request.content_type = None
            im_request.content_disposition = None
            im_request.content_encoding = None
            im_request.expires = None
            im_request.metadata = None
            im_request.headers = {}

            # copy meta form source
            for k, v in self._metadata_prop.headers.items():
                low_k = k.lower()
                if low_k.startswith("x-oss-meta"):
                    im_request.headers[k] = v
                elif low_k in metadata_copied:
                    im_request.headers[k] = v

        elif metadata_directive == "replace":
            # the metadata has been copied via the copyRequest function before
            pass

        else:
            return Exception(f"Unsupported MetadataDirective, {copy_request.metadata_directive}")

    def overwrite_tag_prop(self, im_request: models.InitiateMultipartUploadRequest):
        tagging_directive = str(self._reqeust.tagging_directive).lower()

        if tagging_directive in ["none", "", "copy"]:

            if self._metadata_prop.tagging_count and self._metadata_prop.tagging_count > 0 and self._tag_prop is None:
                request = models.GetObjectTaggingRequest()
                copy_request(request, self._reqeust)
                if self._reqeust.source_bucket != None:
                    request.bucket = self._reqeust.source_bucket

                request.key = self._reqeust.source_key
                request.version_id = self._reqeust.source_version_id

                result = self._client.get_object_tagging(
                    request=request
                )
                self._tag_prop = result

            if self._tag_prop:
                tags = []
                for t in self._tag_prop.tag_set.tags:
                    tags.append(f"{str(t.key)}={str(t.value)}")
                if tags:
                    im_request.tagging = '&'.join(tags)


        elif tagging_directive == "replace":
            # the metadata has been copied via the copyRequest function before
            pass

        else:
            return Exception(f"Unsupported TaggingDirective, {tagging_directive}")

    def _assert_crc_same(self, headers: MutableMapping):
        if not self._check_crc:
            return

        scrc = headers.get('x-oss-hash-crc64ecma', None)
        if scrc is None:
            return

        ccrc = str(self._ccrc)
        if scrc != ccrc:
            raise self._wrap_error(self._upload_id, exceptions.InconsistentError(client_crc=ccrc, server_crc=scrc))

    def _wrap_error(self, upload_id: str, error: Exception) -> Exception:
        return CopyError(
            upload_id=upload_id,
            path=f'oss://{self._reqeust.bucket}/{self._reqeust.key}',
            error=error
        )

    def timeout_handle(self, upload_id: str):
        raise exceptions.TimeoutError(upload_id=upload_id, error='single copy timeout')