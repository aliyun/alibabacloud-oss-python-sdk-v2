"""Copier for handling objects for uploads."""
# pylint: disable=line-too-long, broad-exception-caught
import abc
import copy
import datetime
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
    """Options for copier
    """

    def __init__(
        self,
        part_size: Optional[int] = None,
        parallel_num: Optional[int] = None,
        multipart_copy_threshold: Optional[int] = None,
        leave_parts_on_error: Optional[bool] = None,
        disable_shallow_copy: Optional[bool] = None
    ) -> None:
        self.part_size = part_size
        self.parallel_num = parallel_num
        self.multipart_copy_threshold = multipart_copy_threshold
        self.leave_parts_on_error = leave_parts_on_error or False
        self.disable_shallow_copy = disable_shallow_copy or False

class CopyResult:
    """The result about the copy operation.
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
            kwargs: Extra keyword arguments.
            - part_size (int, optional): The part size. Default value: 64 MiB.
            - parallel_num (int, optional): The number of the upload tasks in parallel. Default value: 3.
            - multipart_copy_threshold (int, optional): The minimum object size for calling the multipart copy operation.
                Default value: 200 MiB.
            - leave_parts_on_error (bool, optional): Specifies whether to retain the copied parts when an copy task fails.
                By default, the copied parts are not retained.
            - disable_shallow_copy (bool, optional): Specifies that the shallow copy capability is not used.
                By default, the shallow copy capability is used.
        """
        part_size = kwargs.get('part_size', defaults.DEFAULT_COPY_PART_SIZE)
        parallel_num = kwargs.get('parallel_num', defaults.DEFAULT_COPY_PARALLEL)
        multipart_copy_threshold = kwargs.get('multipart_copy_threshold', defaults.DEFAULT_COPY_THRESHOLD)
        leave_parts_on_error = kwargs.get('leave_parts_on_error', False)
        disable_shallow_copy = kwargs.get('disable_shallow_copy', False)

        self._client = client
        self._options = CopierOptions(
            part_size=part_size,
            parallel_num=parallel_num,
            multipart_copy_threshold=multipart_copy_threshold,
            leave_parts_on_error=leave_parts_on_error,
            disable_shallow_copy=disable_shallow_copy,
        )

        feature_flags = 0
        cstr = str(client)
        if cstr == '<OssClient>':
            feature_flags = client._client._options.feature_flags
        self._feature_flags = feature_flags


    def copy(
        self,
        request: models.CopyObjectRequest,
        **kwargs: Any
    ) -> CopyResult:
        """copy source object to destination object.

        Args:
            request (CopyObjectRequest): the request parameters for the copy operation.
            kwargs: Extra keyword arguments.
            - part_size (int, optional): The part size. Default value: 64 MiB.
            - parallel_num (int, optional): The number of the upload tasks in parallel. Default value: 3.
            - multipart_copy_threshold (int, optional): The minimum object size for calling the multipart copy operation.
                Default value: 200 MiB.
            - leave_parts_on_error (bool, optional): Specifies whether to retain the copied parts when an copy task fails.
                By default, the copied parts are not retained.
            - disable_shallow_copy (bool, optional): Specifies that the shallow copy capability is not used.
                By default, the shallow copy capability is used.

        Returns:
            CopyResult: The result for the copy operation.
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

        if not validation.is_valid_bucket_name(utils.safety_str(request.bucket)):
            raise exceptions.ParamInvalidError(field='request.bucket')

        if not validation.is_valid_object_name(utils.safety_str(request.key)):
            raise exceptions.ParamInvalidError(field='request.key')

        if not validation.is_valid_object_name(utils.safety_str(request.source_key)):
            raise exceptions.ParamInvalidError(field='request.source_key')

        options = copy.copy(self._options)
        options.part_size = kwargs.get('part_size', self._options.part_size)
        options.parallel_num = kwargs.get('parallel_num', self._options.parallel_num)
        options.multipart_copy_threshold = kwargs.get('multipart_copy_threshold', self._options.multipart_copy_threshold)
        options.leave_parts_on_error = kwargs.get('leave_parts_on_error', self._options.leave_parts_on_error)
        options.disable_shallow_copy = kwargs.get('disable_shallow_copy', self._options.disable_shallow_copy)

        if options.part_size <= 0:
            options.part_size = defaults.DEFAULT_COPY_PART_SIZE

        if options.parallel_num <= 0:
            options.parallel_num = defaults.DEFAULT_COPY_PARALLEL

        if options.multipart_copy_threshold <= 0:
            options.multipart_copy_threshold = defaults.DEFAULT_COPY_THRESHOLD

        delegate = _CopierDelegate(
            base=self,
            client=self._client,
            request=request,
            options=options,
            metadata_prop=kwargs.get('metadata_properties', None),
            tag_prop=kwargs.get('tag_properties', None)
        )

        return delegate

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
        self._request = request
        self._options = options

        self._reader_pos = 0
        self._total_size = 0
        self._transferred = 0

        parallel = options.parallel_num > 1 and self._request.progress_fn is not None
        self._progress_lock = threading.Lock() if parallel else None

        #Source's Info
        self._metadata_prop = metadata_prop
        self._tag_prop = tag_prop

        #use mulitpart upload
        self._copy_part_lock = None
        self._copy_errors = []
        self._copy_parts = []

        # upload info
        self._upload_id = ''

    def check_source(self):
        """
        """
        if self._metadata_prop is not None:
            return

        request = models.HeadObjectRequest()
        copy_request(request, self._request)
        if self._request.source_bucket is not None:
            request.bucket = self._request.source_bucket
        request.key = self._request.source_key
        request.version_id = self._request.source_version_id
        result = self._client.head_object(request)
        self._metadata_prop = result

    def apply_source(self):
        """
        """
        total_size = self._metadata_prop.content_length
        if total_size is None:
            total_size = -1
        self._total_size = total_size

    def can_use_shallow_copy(self):
        if self._options.disable_shallow_copy:
            return False

        if self._request.storage_class is not None:
            return False

        if self._request.source_bucket is not None and self._request.source_bucket != self._request.bucket:
            return False

        if self._metadata_prop.server_side_encryption is not None:
            return False

        return True

    def copy(self) -> CopyResult:
        """copy object
        """
        try:
            if self._total_size <= self._options.multipart_copy_threshold:
                return self._single_copy()
            elif self.can_use_shallow_copy():
                return self._shallow_copy()
            return self._multipart_copy()
        except Exception as err:
            raise self._wrap_error(self._upload_id, err)

    def _single_copy(self) -> CopyResult:
        result = self._client.copy_object(self._request)

        self._update_progress(self._total_size)

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
        # use signle copy first, if meets timeout, use multiCopy
        starttime = datetime.datetime.now()
        try:
            result = self._client.copy_object(self._request, readwrite_timeout=10, operation_timeout=30)
        except Exception as err:
            if (datetime.datetime.now() > starttime + datetime.timedelta(seconds=30)):
                return self._multipart_copy()
            raise

        self._update_progress(self._total_size)

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
        # get tag prop if nesssessary
        self._get_tag_props()

        # init the multipart
        self._init_upload()

        # upload part
        part_size = self._options.part_size
        while self._total_size/part_size >= defaults.MAX_UPLOAD_PARTS:
            part_size += self._options.part_size
        self._options.part_size = part_size

        parallel = self._options.parallel_num > 1
        if parallel:
            self._copy_part_lock = threading.Lock()
            with concurrent.futures.ThreadPoolExecutor(self._options.parallel_num) as executor:
                for result in executor.map(self._copy_part, self._iter_part()):
                    self._update_upload_result_lock(result)
        else:
            for part in self._iter_part():
                self._update_upload_result_lock(self._copy_part(part))
                if len(self._copy_errors) > 0:
                    break

        # complete upload
        cmresult: models.CompleteMultipartUploadResult = None
        if len(self._copy_errors) == 0:
            request = models.CompleteMultipartUploadRequest()
            copy_request(request, self._request)
            parts = sorted(self._copy_parts, key=lambda p: p.part_number)
            request.upload_id = self._upload_id
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
                    copy_request(abort_request, self._request)
                    abort_request.upload_id = self._upload_id
                    self._client.abort_multipart_upload(abort_request)
                except Exception as _:
                    pass
            raise self._copy_errors[-1]

        self._assert_crc_same(cmresult.headers)

        ret = CopyResult(
            upload_id=self._upload_id,
            etag=cmresult.etag,
            version_id=cmresult.version_id,
            hash_crc64=cmresult.hash_crc64,
        )
        ret.status = cmresult.status
        ret.status_code = cmresult.status_code
        ret.request_id = cmresult.request_id
        ret.headers = cmresult.headers

        return ret

    def _get_tag_props(self):
        if self._tag_prop is not None:
            return

        if utils.safety_int(self._metadata_prop.tagging_count) <= 0:
            return

        # if directive is copy, get tags
        directive = utils.safety_str(self._request.tagging_directive)
        if directive == "" or directive.lower() == "copy":
            request = models.GetObjectTaggingRequest()
            copy_request(request, self._request)
            if self._request.source_bucket is not None:
                request.bucket = self._request.source_bucket
            request.key = self._request.source_key
            request.version_id = self._request.source_version_id
            result = self._client.get_object_tagging(request)
            self._tag_prop = result

    def _init_upload(self):
        request = models.InitiateMultipartUploadRequest()
        copy_request(request, self._request)
        self.overwrite_metadata_prop(request)
        self.overwrite_tag_prop(request)
        request.disable_auto_detect_mime_type = True

        result = self._client.initiate_multipart_upload(request)
        self._upload_id = result.upload_id

    def _iter_part(self):
        start_part_num = 0
        upload_id = self._upload_id

        # timeout for MultiPartCopy API
        # 10s per 200M, max timeout is 50s
        PART_SIZE = 200 * 1024 * 1024
        STEP = 20
        timeout = defaults.DEFAULT_READWRITE_TIMEOUT
        part_size = self._options.part_size
        while part_size > 200 * 1024 * 1024:
            timeout += STEP
            part_size -= PART_SIZE
            if timeout > 50:
                break

        while len(self._copy_errors) == 0:
            n = self._options.part_size
            bytes_left = self._total_size - self._reader_pos

            if bytes_left <= 0:
                break
            if bytes_left < n:
                n = bytes_left

            range_end = self._reader_pos + n - 1
            range = f'bytes={self._reader_pos}-{range_end}'
            self._reader_pos += n

            start_part_num += 1
            yield upload_id, start_part_num, range, timeout, n

    def _copy_part(self, part):
        # When an error occurs, ignore other upload requests
        if len(self._copy_errors) > 0:
            return None

        upload_id = part[0]
        part_number = part[1]
        range = part[2]
        timeout = part[3]
        part_size = part[4]
        error: Exception = None
        etag = None

        try:
            request = models.UploadPartCopyRequest()
            copy_request(request, self._request)
            request.part_number = part_number
            request.upload_id = upload_id
            request.source_range = range
            result = self._client.upload_part_copy(request, readwrite_timeout=timeout)
            etag = result.etag

            self._update_progress(part_size)
        except Exception as err:
            error = err


        return part_number, etag, error

    def _update_progress(self, increment: int):
        if self._request.progress_fn is None:
            return

        if self._progress_lock:
            with self._progress_lock:
                self._transferred += increment
                self._request.progress_fn(increment, self._transferred, self._total_size)
        else:
            self._transferred += increment
            self._request.progress_fn(increment, self._transferred, self._total_size)

    def _update_upload_result_lock(self, result) -> None:
        if self._copy_part_lock:
            with self._copy_part_lock:
                self._update_upload_result(result)
        else:
            self._update_upload_result(result)

    def _update_upload_result(self, result):
        if result is None:
            return

        if result[2] is not None:
            self._copy_errors.append(result[2])
            return

        part_number = result[0]
        etag = result[1]

        self._copy_parts.append(models.UploadPart(part_number=part_number, etag=etag))

    def overwrite_metadata_prop(self, im_request: models.InitiateMultipartUploadRequest):
        directive = utils.safety_str(self._request.metadata_directive).lower()
        if directive in ["", "copy"]:
            if self._metadata_prop is None:
                return Exception(f"request.metadata_directive is COPY, but meets nil metadata_prop for source")

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

        elif directive == "replace":
            # the metadata has been copied via the copyRequest function before
            pass

        else:
            return Exception(f"Unsupported metadata_directive, {self._request.metadata_directive}")

    def overwrite_tag_prop(self, im_request: models.InitiateMultipartUploadRequest):
        directive = utils.safety_str(self._request.tagging_directive).lower()
        if directive in ["", "copy"]:
            if self._tag_prop is not None and self._tag_prop.tag_set is not None:
                tags = []
                for t in self._tag_prop.tag_set.tags:
                    tags.append(f"{str(t.key)}={str(t.value)}")
                if tags:
                    im_request.tagging = '&'.join(tags)

        elif directive == "replace":
            # the metadata has been copied via the copyRequest function before
            pass

        else:
            return Exception(f"Unsupported tagging_directive, {self._request.tagging_directive}")

    def _assert_crc_same(self, headers: MutableMapping):
        scrc = headers.get('x-oss-hash-crc64ecma', None)
        if scrc is None:
            return

        ccrc = self._metadata_prop.hash_crc64
        if ccrc is None:
            return

        if scrc != ccrc:
            raise exceptions.InconsistentError(client_crc=ccrc, server_crc=scrc)

    def _wrap_error(self, upload_id: str, error: Exception) -> Exception:
        return CopyError(
            upload_id=upload_id,
            path=f'oss://{self._request.bucket}/{self._request.key}',
            error=error
        )
