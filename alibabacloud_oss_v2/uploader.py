"""Uploader for handling objects for uploads."""
# pylint: disable=line-too-long, broad-exception-caught
import abc
import copy
import os
import concurrent.futures
import threading
from typing import Any, Optional, IO, MutableMapping, List
from . import exceptions
from . import models
from . import validation
from . import utils
from . import io_utils
from . import defaults
from .serde import copy_request
from .checkpoint import UploadCheckpoint
from .crc import Crc64
from .paginator import ListPartsPaginator

class UploadAPIClient(abc.ABC):
    """Abstract base class for uploader client."""

    @abc.abstractmethod
    def put_object(self, request: models.PutObjectRequest, **kwargs) -> models.PutObjectResult:
        """Uploads objects.""" 

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
    def upload_part(self, request: models.UploadPartRequest, **kwargs) -> models.UploadPartResult:
        """
        Call the UploadPart interface to upload data in blocks (parts)
        based on the specified Object name and uploadId.
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

class UploaderOptions:
    """
    Options for uploader
    """

    def __init__(
        self,
        part_size: Optional[int] = None,
        parallel_num: Optional[int] = None,
        leave_parts_on_error: Optional[bool] = None,
        enable_checkpoint: Optional[bool] = None,
        checkpoint_dir: Optional[str] = None,
    ) -> None:
        """
        part_size (int, optional): The part size. Default value: 6 MiB.
        parallel_num (int, optional): The number of the upload tasks in parallel. Default value: 3.
        leave_parts_on_error (bool, optional): Specifies whether to retain the uploaded parts when an upload task fails.
            By default, the uploaded parts are not retained.
        enable_checkpoint (bool, optional): Specifies whether to record the resumable upload progress in the checkpoint file.
            By default, no resumable upload progress is recorded.
        checkpoint_dir (str, optional): The path in which the checkpoint file is stored. Example: /local/dir/.
            This parameter is valid only if EnableCheckpoint is set to true.
        """
        self.part_size = part_size
        self.parallel_num = parallel_num
        self.leave_parts_on_error = leave_parts_on_error or False
        self.enable_checkpoint = enable_checkpoint or False
        self.checkpoint_dir = checkpoint_dir


class UploadResult:
    """
    The result about the upload operation.
    """

    def __init__(
        self,
        upload_id: Optional[str] = None,
        etag: Optional[str] = None,
        version_id: Optional[str] = None,
        hash_crc64: Optional[str] = None,
    ) -> None:
        """
        upload_id (str, optional): The upload ID that uniquely identifies the multipart upload task.
        etag (str, optional): Entity tag for the uploaded object.
        version_id (str, optional): The version ID of the object.
        hash_crc64 (str, optional): The 64-bit CRC value of the object.
            This value is calculated based on the ECMA-182 standard.
        """
        self.upload_id = upload_id
        self.etag = etag
        self.version_id = version_id
        self.hash_crc64 = hash_crc64

        self.status = ''
        self.status_code = 0
        self.request_id = ''
        self.headers: MutableMapping[str, str] = {}

class UploadError(exceptions.BaseError):
    """
    Upload Error.
    """
    fmt = 'upload failed, {upload_id}, {path}, {error}.'

    def __init__(self, **kwargs):
        exceptions.BaseError.__init__(self, **kwargs)
        self._error = kwargs.get("error", None)
        self.upload_id = kwargs.get("upload_id", None)
        self.path = kwargs.get("path", None)

    def unwrap(self) -> Exception:
        """returns the detail error"""
        return self._error


class Uploader:
    """Uploader for handling objects for uploads."""

    def __init__(
        self,
        client: UploadAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (UploadAPIClient): A agent that implements the PutObject and Multipart Upload api.
            kwargs: Extra keyword arguments used to initialize the uploader.
                - part_size (int): The part size. Default value: 6 MiB.
                - parallel_num (int): The number of the upload tasks in parallel. Default value: 3.
                - leave_parts_on_error (bool): Whether to retain the uploaded parts when an upload task fails. By default, the uploaded parts are not retained.
                - enable_checkpoint (bool): Whether to enable checkpoint. Defaults to False.
                - checkpoint_dir (str): The directory to store checkpoint.            
        """
        part_size = kwargs.get('part_size', defaults.DEFAULT_UPLOAD_PART_SIZE)
        parallel_num = kwargs.get('parallel_num', defaults.DEFAULT_UPLOAD_PARALLEL)
        leave_parts_on_error = kwargs.get('leave_parts_on_error', False)
        self._client = client
        self._options = UploaderOptions(
            part_size=part_size,
            parallel_num=parallel_num,
            leave_parts_on_error=leave_parts_on_error,
            enable_checkpoint=kwargs.get('enable_checkpoint', None),
            checkpoint_dir=kwargs.get('checkpoint_dir', None),
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


    def upload_file(
        self,
        request: models.PutObjectRequest,
        filepath: str,
        **kwargs: Any
    ) -> UploadResult:
        """Uploads a local file.

        Args:
            request (models.PutObjectRequest):  the request parameters for the upload operation.
            filepath (str): The path of a local file.
            kwargs: Extra keyword arguments.
                - part_size (int): The part size.
                - parallel_num (int): The number of the upload tasks in parallel.
                - leave_parts_on_error (bool): Whether to retain the uploaded parts when an upload task fails.
                - enable_checkpoint (bool): Whether to enable checkpoint.
                - checkpoint_dir (str): The directory to store checkpoint.            

        Returns:
            UploadResult: The result for the upload operation.
        """
        delegate = self._delegate(request, **kwargs)

        delegate.check_source(filepath)

        with open(delegate.reader_filepath, 'rb') as reader:

            delegate.apply_source(reader)

            delegate.check_checkpoint()

            delegate.update_crc_flag()

            delegate.adjust_source()

            result = delegate.upload()

            delegate.close_reader()

        return result

    def upload_from(
        self,
        request: models.PutObjectRequest,
        reader: IO[bytes],
        **kwargs: Any
    ) -> UploadResult:
        """Uploads a stream.

        Args:
            request (models.PutObjectRequest):  The request parameters for the upload operation.
            reader (IO[bytes]): The stream to be uploaded.
            kwargs: Extra keyword arguments.
                - part_size (int): The part size.
                - parallel_num (int): The number of the upload tasks in parallel.
                - leave_parts_on_error (bool): Whether to retain the uploaded parts when an upload task fails.
        Returns:
            UploadResult: The result for the upload operation.
        """
        delegate = self._delegate(request, **kwargs)
        delegate.apply_source(reader)
        return delegate.upload()

    def _delegate(
        self,
        request: models.PutObjectRequest,
        **kwargs: Any
    ) -> "_UploaderDelegate":

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
        options.enable_checkpoint = kwargs.get('enable_checkpoint', self._options.enable_checkpoint)
        options.checkpoint_dir = kwargs.get('checkpoint_dir', self._options.checkpoint_dir)

        if options.part_size <= 0:
            options.part_size = defaults.DEFAULT_UPLOAD_PART_SIZE

        if options.parallel_num <= 0:
            options.parallel_num = defaults.DEFAULT_UPLOAD_PARALLEL

        delegate = _UploaderDelegate(
            base=self,
            client=self._client,
            request=request,
            options=options
        )

        return delegate


class _UploadContext:
    def __init__(
        self,
        upload_id: str = None,
        start_num: int = None,
    ) -> None:
        self.upload_id = upload_id
        self.start_num = start_num


class _UploaderDelegate:
    def __init__(
        self,
        base: Uploader,
        client: UploadAPIClient,
        request: models.PutObjectRequest,
        options: UploaderOptions,
    ) -> None:
        """
        """
        self._base = base
        self._client = client
        self._request = request
        self._options = options

        parallel = options.parallel_num > 1
        self._reader: IO[bytes] = None
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
        self._upload_part_lock = None
        self._upload_errors = []
        self._uploaded_parts = []

        # resumable upload
        self._upload_id = None
        self._part_number = None


    @property
    def reader_filepath(self) -> str:
        """reader filepath
        """
        return self._filepath

    def check_source(self, filepath:str):
        """check source
        """
        if len(filepath) == 0:
            raise exceptions.ParamInvalidError(field='filepath')

        absfilepath = os.path.abspath(filepath)
        if not os.path.isfile(absfilepath):
            raise exceptions.FileNotExist(filepath=filepath)

        if not os.access(absfilepath, os.R_OK):
            raise exceptions.FileNotReadable(filepath=filepath)

        self._filepath = absfilepath
        self._file_stat = os.stat(absfilepath)

    def apply_source(self, reader):
        """apply source
        """
        if reader is None:
            raise exceptions.ParamInvalidError(field = 'reader')

        total_size = utils.guess_content_length(reader)
        if total_size is None:
            total_size = -1
        part_size = self._options.part_size

        if total_size > 0:
            while self._total_size/part_size >= defaults.MAX_UPLOAD_PARTS:
                part_size += self._options.part_size

        self._reader = reader
        self._options.part_size = part_size
        self._total_size = total_size
        self._reader_seekable = utils.is_seekable(reader)

    def check_checkpoint(self):
        """check checkpoint
        """
        if not self._options.enable_checkpoint:
            return

        if not self._reader_seekable:
            return

        checkpoint = UploadCheckpoint(
            request=self._request,
            filepath=self._filepath,
            basedir=self._options.checkpoint_dir,
            fileinfo=self._file_stat,
            part_size=self._options.part_size)

        checkpoint.load()
        if checkpoint.loaded:
            self._upload_id = checkpoint.upload_id

        self._options.leave_parts_on_error = True
        self._checkpoint = checkpoint


    def update_crc_flag(self):
        """update crc flag
        """
        #FF_ENABLE_CRC64_CHECK_UPLOAD = 0x00000008
        if (self._base._feature_flags & 0x00000008) > 0:
            self._check_crc = True

    def adjust_source(self):
        """	resume from upload id
        """
        if not self._upload_id:
            return

        uploaded_parts:List[models.Part] = []
        ccrc = 0

        for part in self._iter_uploaded_part():
            uploaded_parts.append(models.UploadPart(part_number=part.part_number, etag=part.etag))
            if self._check_crc and part.hash_crc64 is not None:
                ccrc = Crc64.combine(ccrc, int(part.hash_crc64), part.size)

        if len(uploaded_parts) == 0:
            return

        # update from upload's result
        part_number = uploaded_parts[-1].part_number
        next_offset = part_number * self._options.part_size

        #print(f'last part number={part_number}, next offset={next_offset}')

        self._uploaded_parts = uploaded_parts
        self._reader_pos = next_offset
        self._part_number = part_number + 1
        self._ccrc = ccrc
        self._transferred = next_offset


    def set_reader(self, reader) ->IO[bytes]:
        """set reader
        """
        self._reader = reader

    def close_reader(self):
        """close reader
        """

        if self._checkpoint:
            self._checkpoint.remove()

        self._reader = None
        self._checkpoint = None

    def upload(self) -> UploadResult:
        """Breakpoint upload
        """
        if self._total_size >= 0 and self._total_size < self._options.part_size:
            return self._single_part()

        return self._multipart_part()

    def _single_part(self) -> UploadResult:
        request = models.PutObjectRequest()
        copy_request(request, self._request)
        request.body = self._reader
        if request.content_type is None:
            request.content_type = self._get_content_type()

        try:
            result = self._client.put_object(request)
        except Exception as err:
            raise self._wrap_error('', err)

        ret = UploadResult(
            etag=result.etag,
            version_id=result.version_id,
            hash_crc64=result.hash_crc64,
        )
        ret.status = result.status
        ret.status_code = result.status_code
        ret.request_id = result.request_id
        ret.headers = result.headers

        return ret


    def _multipart_part(self) -> UploadResult:
        # init the multipart
        try:
            upload_ctx = self._get_upload_context()
        except Exception as err:
            raise self._wrap_error('', err)

        # update checkpoint
        if self._checkpoint:
            self._checkpoint.upload_id = upload_ctx.upload_id
            self._checkpoint.dump()

        # upload part
        parallel = self._options.parallel_num > 1
        if parallel:
            self._upload_part_lock = threading.Lock()
            with concurrent.futures.ThreadPoolExecutor(self._options.parallel_num) as executor:
                for result in executor.map(self._upload_part, self._iter_part(upload_ctx)):
                    self._update_upload_result(result)
        else:
            for part in self._iter_part(upload_ctx):
                self._update_upload_result(self._upload_part(part))
                if len(self._upload_errors) > 0:
                    break

        
        # complete upload
        cmresult: models.CompleteMultipartUploadResult = None
        if len(self._upload_errors) == 0:
            request = models.CompleteMultipartUploadRequest()
            copy_request(request, self._request)
            parts = sorted(self._uploaded_parts, key=lambda p: p.part_number)
            request.upload_id = upload_ctx.upload_id
            request.complete_multipart_upload = models.CompleteMultipartUpload(parts=parts)
            try:
                cmresult = self._client.complete_multipart_upload(request)
            except Exception as err:
                self._upload_errors.append(err)

        # check last error
        if len(self._upload_errors) > 0:
            if not self._options.leave_parts_on_error:
                try:
                    abort_request = models.AbortMultipartUploadRequest()
                    abort_request.upload_id = upload_ctx.upload_id
                    copy_request(request, self._request)
                    self._client.abort_multipart_upload(abort_request)
                except Exception as _:
                    pass
            raise self._wrap_error(upload_ctx.upload_id, self._upload_errors[-1])

        self._assert_crc_same(cmresult.headers)

        ret = UploadResult(
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


    def _get_upload_context(self) -> _UploadContext:
        if self._upload_id:
            return _UploadContext(
                upload_id=self._upload_id,
                start_num=self._part_number - 1,
            )

	    #if not exist or fail, create a new upload id
        request = models.InitiateMultipartUploadRequest()
        copy_request(request, self._request)
        if request.content_type is None:
            request.content_type = self._get_content_type()

        result = self._client.initiate_multipart_upload(request)

        return _UploadContext(
            upload_id=result.upload_id,
            start_num=0,
        )

    def _iter_part(self, upload_ctx: _UploadContext):
        start_part_num = upload_ctx.start_num
        reader = self._reader
        if self._reader_seekable:
            reader = io_utils.ReadAtReader(reader)

        def next_body():
            n = self._options.part_size
            if self._reader_seekable:
                bytes_left = self._total_size - self._reader_pos
                if bytes_left < n:
                    n = bytes_left
                body = io_utils.SectionReader(reader, self._reader_pos, n)
            else:
                body = reader.read(n)

            self._reader_pos += len(body)
            return body

        while len(self._upload_errors) == 0:
            try:
                body = next_body()
                if len(body) == 0:
                    break
            except Exception as err:
                self._save_error(err)
                break

            start_part_num += 1
            yield upload_ctx.upload_id, start_part_num, body


    def _upload_part(self, part):
        # When an error occurs, ignore other upload requests
        if len(self._upload_errors) > 0:
            return None

        upload_id = part[0]
        part_number = part[1]
        body = part[2]
        error: Exception = None
        etag = None
        size = len(body)
        hash_crc64 = None
        try:
            result = self._client.upload_part(models.UploadPartRequest(
                bucket=self._request.bucket,
                key=self._request.key,
                upload_id=upload_id,
                part_number=part_number,
                body=body,
                request_payer=self._request.request_payer
            ))
            etag = result.etag
            hash_crc64 = result.hash_crc64
        except Exception as err:
            error = err

        return part_number, etag, error, hash_crc64, size


    def _save_error(self, error) -> None:
        if self._upload_part_lock:
            with self._upload_part_lock:
                self._upload_errors.append(error)
        else:
            self._upload_errors.append(error)


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
                bucket=self._request.bucket,
                key=self._request.key,
                request_payer=self._request.request_payer,
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
        #print(f'_update_upload_result: {result}')
        if result is None:
            return

        if result[2] is not None:
            self._save_error(result[2])
            return

        part_number = result[0]
        etag = result[1]
        hash_crc64 = result[3]
        size = result[4]

        self._uploaded_parts.append(models.UploadPart(part_number=part_number, etag=etag))

        if self._check_crc and hash_crc64 is not None:
            self._ccrc = Crc64.combine(self._ccrc, int(hash_crc64), size)

        self._transferred += size
        if self._request.progress_fn is not None:
            self._request.progress_fn(size, self._transferred, self._total_size)


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
        return UploadError(
            upload_id=upload_id,
            path=f'oss://{self._request.bucket}/{self._request.key}',
            error=error
        )
