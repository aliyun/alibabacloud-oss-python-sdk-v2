"""Downloader for handling objects for downloads."""
import abc
import copy
import os
import concurrent.futures
import threading
from typing import Iterator, Any, Optional, IO
from . import exceptions
from . import models
from . import validation
from . import utils
from . import io_utils
from . import defaults
from .serde import copy_request
from .checkpoint import DownloadCheckpoint
from .crc import Crc64

class DownloadAPIClient(abc.ABC):
    """Abstract base class for downloader client."""

    @abc.abstractmethod
    def head_object(self, request: models.HeadObjectRequest, **kwargs) -> models.HeadObjectResult:
        """Queries information about the object in a bucket."""

    @abc.abstractmethod
    def get_object(self, request: models.GetObjectRequest, **kwargs) -> models.GetObjectResult:
        """
        Queries an object. To call this operation, you must have read permissions on the object.
        """

class DownloaderOptions:
    """Options for downloader
    """

    def __init__(
        self,
        part_size: Optional[int] = None,
        parallel_num: Optional[int] = None,
        block_size: Optional[int] = None,
        use_temp_file: Optional[bool] = None,
        enable_checkpoint: Optional[bool] = None,
        checkpoint_dir: Optional[str] = None,
        verify_data: Optional[bool] = None,
    ) -> None:
        """
        part_size (int, optional): The part size. Default value: 6 MiB.
        parallel_num (int, optional): The number of the download tasks in parallel. Default value: 3.
        block_size (int, optional): The block size is the number of bytes it should read into memory. Default value: 16 KiB.
        use_temp_file (bool, optional): Specifies whether to use a temporary file when you download an object.
            A temporary file is used by default. The object is downloaded to the temporary file.
            Then, the temporary file is renamed and uses the same name as the object that you want to download.
        enable_checkpoint (bool, optional): Specifies whether to record the download progress in the checkpoint file.
            By default, no download progress is recorded.
        checkpoint_dir (str, optional): The path in which the checkpoint file is stored. Example: /local/dir/.
            This parameter is valid only if enable_checkpoint is set to true.
        verify_data (bool, optional): Specifies whether to verify the CRC-64 of the downloaded object when the download is resumed.
            By default, the CRC-64 is not verified. This parameter is valid only if enable_checkpoint is set to true.
        """
        self.part_size = part_size
        self.parallel_num = parallel_num
        self.block_size = block_size
        self.use_temp_file = use_temp_file or False
        self.enable_checkpoint = enable_checkpoint or False
        self.checkpoint_dir = checkpoint_dir
        self.verify_data = verify_data


class DownloadResult:
    """The result about the download operation.
    """

    def __init__(
        self,
        written: Optional[int],
    ) -> None:
        """
        written (int, optional): The size of the downloaded data, in bytes.
        """
        self.written = written

class DownloadError(exceptions.BaseError):
    """
    Download Error.
    """
    fmt = 'download failed, {path}, {error}.'

    def __init__(self, **kwargs):
        exceptions.BaseError.__init__(self, **kwargs)
        self._error = kwargs.get("error", None)
        self.path = kwargs.get("path", None)

    def unwrap(self) -> Exception:
        """returns the detail error"""
        return self._error

class Downloader:
    """Downloader for handling objects for downloads."""

    def __init__(
        self,
        client: DownloadAPIClient,
        **kwargs: Any
    ) -> None:
        """
            client (DownloadAPIClient): A agent that implements the HeadObject and GetObject api.
            kwargs: Extra keyword arguments used to initialize the downloader.
                - part_size (int): The part size. Default value: 6 MiB.
                - parallel_num (int): The number of the download tasks in parallel. Default value: 3.
                - block_size (int): The block size is the number of bytes it should read into memory. Default value: 16 KiB.
                - use_temp_file (bool): Whether to use a temporary file when you download an object. A temporary file is used by default.
                - enable_checkpoint (bool): Whether to enable checkpoint. Defaults to False.
                - checkpoint_dir (str): The directory to store checkpoint.
                - verify_data (bool): Whether to verify data when the download is resumed. Defaults to False.            
        """
        part_size = kwargs.get('part_size', defaults.DEFAULT_DOWNLOAD_PART_SIZE)
        parallel_num = kwargs.get('parallel_num', defaults.DEFAULT_DOWNLOAD_PARALLEL)
        self._client = client
        self._options = DownloaderOptions(
            part_size=part_size,
            parallel_num=parallel_num,
            block_size=kwargs.get('block_size', None),
            use_temp_file=kwargs.get('use_temp_file', None),
            enable_checkpoint=kwargs.get('enable_checkpoint', None),
            checkpoint_dir=kwargs.get('checkpoint_dir', None),
            verify_data=kwargs.get('verify_data', None),
        )

        feature_flags = 0
        cstr = str(client)
        if cstr == '<OssClient>':
            feature_flags = client._client._options.feature_flags
        elif cstr == '<OssEncryptionClient>':
            feature_flags = client.unwrap()._client._options.feature_flags
        self._feature_flags = feature_flags


    def download_file(
        self,
        request: models.GetObjectRequest,
        filepath: str,
        **kwargs: Any
    ) -> DownloadResult:
        """Downloads an object into a local file.

        Args:
            request (models.GetObjectRequest):  the request parameters for the download operation.
            filepath (str): The path of a local file.
            kwargs: Extra keyword arguments.
                - part_size (int): The part size.
                - parallel_num (int): The number of the download tasks in parallel.
                - block_size (int): The block size is the number of bytes it should read into memory.
                - use_temp_file (bool): Whether to use a temporary file when you download an object.
                - enable_checkpoint (bool): Whether to enable checkpoint.
                - checkpoint_dir (str): The directory to store checkpoint.
                - verify_data (bool): Whether to verify data when the download is resumed.
        Returns:
            DownloadResult: The result for the download operation.
        """
        delegate = self._delegate(request, **kwargs)

        delegate.check_source()

        delegate.check_destination(filepath)

        delegate.adjust_range()

        delegate.check_checkpoint()

        with open(delegate.writer_filepath, 'ab') as _:
            pass
        with open(delegate.writer_filepath, 'rb+') as writer:

            delegate.adjust_writer(writer)

            delegate.update_crc_flag()

            result = delegate.download()

            delegate.close_writer(writer)

        return result


    def download_to(
        self,
        request: models.GetObjectRequest,
        writer: IO[bytes],
        **kwargs: Any
    ) -> DownloadResult:
        """Downloads an object into a stream.

        Args:
            request (models.GetObjectRequest):  the request parameters for the download operation.
            writer (IO[bytes]): writes the data into writer
            kwargs: Extra keyword arguments.
                - part_size (int): The part size.
                - parallel_num (int): The number of the download tasks in parallel.
                - block_size (int): The block size is the number of bytes it should read into memory.
        Returns:
            DownloadResult: The result for the download operation.
        """
        delegate = self._delegate(request, **kwargs)

        delegate.check_source()

        delegate.adjust_range()

        delegate.adjust_writer(writer)

        result = delegate.download()

        return result

    def _delegate(
        self,
        request: models.GetObjectRequest,
        **kwargs: Any
    ) -> "_DownloaderDelegate":

        if request is None:
            raise exceptions.ParamNullError(field='request')

        if not validation.is_valid_bucket_name(utils.safety_str(request.bucket)):
            raise exceptions.ParamInvalidError(field='request.bucket')

        if not validation.is_valid_object_name(utils.safety_str(request.key)):
            raise exceptions.ParamInvalidError(field='request.key')

        if request.range_header and not validation.is_valid_range(request.range_header):
            raise exceptions.ParamNullError(field='request.range_header')

        options = copy.copy(self._options)
        options.part_size = kwargs.get('part_size', self._options.part_size)
        options.parallel_num = kwargs.get('parallel_num', self._options.parallel_num)
        options.block_size = kwargs.get('block_size', self._options.block_size)
        options.use_temp_file = kwargs.get('use_temp_file', self._options.use_temp_file)
        options.enable_checkpoint = kwargs.get('enable_checkpoint', self._options.enable_checkpoint)
        options.checkpoint_dir = kwargs.get('checkpoint_dir', self._options.checkpoint_dir)
        options.verify_data = kwargs.get('verify_data', self._options.verify_data)

        if options.part_size <= 0:
            options.part_size = defaults.DEFAULT_DOWNLOAD_PART_SIZE

        if options.parallel_num <= 0:
            options.parallel_num = defaults.DEFAULT_DOWNLOAD_PARALLEL

        delegate = _DownloaderDelegate(
            base=self,
            client=self._client,
            request=request,
            options=options
        )

        return delegate


class _DownloaderDelegate:
    def __init__(
        self,
        base: Downloader,
        client: DownloadAPIClient,
        request: models.GetObjectRequest,
        options: DownloaderOptions,
    ) -> None:
        """
        """
        self._base = base
        self._client = client
        self._request = request
        self._options = options

        self._rstart = 0
        self._pos = 0
        self._epos = 0
        self._written = 0

        parallel = options.parallel_num > 1
        self._writer = None
        self._writer_lock = threading.Lock() if parallel else None
        self._progress_lock = threading.Lock() if parallel else None

        #Source's Info
        self._size_in_bytes = None
        self._modtime = None
        self._etag = None
        self._headers = None

        #Destination's Info
        self._filepath = None
        self._temp_filepath = None

        #CRC
        self._calc_crc = False
        self._check_crc = False
        self._ccrc = 0
        self._next_offset = 0

        #checkpoint
        self._checkpoint: DownloadCheckpoint = None

        #use mulitpart download
        self._download_errors = []

    @property
    def writer_filepath(self) -> str:
        """writer filepath
        """
        return self._temp_filepath

    def check_source(self):
        """check source
        """
        request = models.HeadObjectRequest(self._request.bucket, self._request.key)
        copy_request(request, self._request)
        result = self._client.head_object(request)

        self._size_in_bytes = result.content_length
        self._modtime = result.last_modified
        self._etag = result.etag
        self._headers = result.headers

    def check_destination(self, filepath: str):
        """check destination
        """
        if len(utils.safety_str(filepath)) == 0:
            raise exceptions.ParamInvalidError(field='filepath')

        absfilepath = os.path.abspath(filepath)
        tempfilepath = absfilepath
        if self._options.use_temp_file:
            tempfilepath += defaults.DEFAULT_TEMP_FILE_SUFFIX

        self._filepath = absfilepath
        self._temp_filepath = tempfilepath


    def adjust_range(self):
        """adjust range
        """
        self._pos = 0
        self._rstart = 0
        self._epos = self._size_in_bytes

        if self._request.range_header is not None:
            range_header = utils.parse_http_range(self._request.range_header)
            if range_header[0] >= self._size_in_bytes:
                raise ValueError(f'invalid range, size :{self._size_in_bytes}, range: {self._request.range_header}')
            if range_header[0] > 0:
                self._pos = range_header[0]
            self._rstart = self._pos

            if range_header[1] > 0:
                self._epos = min(range_header[1] + 1, self._size_in_bytes)

    def check_checkpoint(self):
        """check checkpoint
        """
        if not self._options.enable_checkpoint:
            return

        checkpoint = DownloadCheckpoint(
            request=self._request,
            filepath=self._temp_filepath,
            basedir=self._options.checkpoint_dir,
            headers=self._headers,
            part_size=self._options.part_size)

        checkpoint.verify_data = self._options.verify_data
        checkpoint.load()
        if checkpoint.loaded:
            self._pos = checkpoint.doffset
            self._written = self._pos - self._rstart
        else:
            checkpoint.doffset = self._pos

        self._checkpoint = checkpoint
        #crc
        self._ccrc = checkpoint.dcrc64
        self._next_offset = checkpoint.doffset


    def adjust_writer(self, writer:IO[bytes]):
        """adjust writer

        Args:
            writer (_type_): _description_
        """
        try:
            writer.truncate(self._pos - self._rstart)
        except OSError:
            pass

        self._writer = writer

    def close_writer(self, writer:IO[bytes]):
        """close writer

        Args:
            writer (_type_): _description_
        """
        if writer:
            writer.close()

        if self._temp_filepath != self._filepath:
            io_utils.rename_file(self._temp_filepath, self._filepath)

        if self._checkpoint:
            self._checkpoint.remove()

        self._writer = None
        self._checkpoint = None

    def update_crc_flag(self):
        """update crc flag
        """
        #FF_ENABLE_CRC64_CHECK_DOWNLOAD
        if (self._base._feature_flags & 0x00000010) > 0:
            self._check_crc = self._request.range_header is None
            self._calc_crc = (self._checkpoint is not None and self._checkpoint.verify_data) or self._check_crc

    def download(self) -> DownloadResult:
        """Breakpoint download
        """
        parallel = self._options.parallel_num > 1
        seekable = utils.is_seekable(self._writer)
        if not seekable:
            parallel = False
        if self._epos - self._pos  <= self._options.part_size:
            parallel = False

        if parallel:
            with concurrent.futures.ThreadPoolExecutor(self._options.parallel_num) as executor:
                for result in executor.map(self._process_part, self._iter_part_start()):
                    self._update_process_result(result)
        else:
            if seekable:
                self._writer.seek(self._pos - self._rstart, os.SEEK_SET)
            for start in self._iter_part_start():
                self._update_process_result(self._process_part(start))
                if len(self._download_errors) > 0:
                    break

        if len(self._download_errors) > 0:
            raise self._wrap_error(self._download_errors[-1])

        self._assert_crc_same()

        return DownloadResult(written=self._written)

    def _iter_part_start(self) -> Iterator[int]:
        start = self._pos
        while start < self._epos:
            yield start
            start += self._options.part_size

            # When an error occurs, stop download
            if len(self._download_errors) > 0:
                break

    def _calc_part_size(self, start:int):
        if start + self._options.part_size > self._epos:
            size = self._epos - start
        else:
            size = self._options.part_size
        return size

    def _process_part(self, start:int):
        # When an error occurs, ignore other download requests
        if len(self._download_errors) > 0:
            return None

        size = self._calc_part_size(start)
        request = copy.copy(self._request)

        got = 0
        error: Exception = None

        chash: Crc64 = None
        if self._calc_crc:
            chash = Crc64(0)

        while True:
            request.range_header = f'bytes={start + got}-{start + size - 1}'
            request.range_behavior = 'standard'

            try:
                result = self._client.get_object(request)
            except Exception as err:
                error = err
                break

            kwargs = {}
            if self._options.block_size:
                kwargs['block_size'] = self._options.block_size

            try:
                gotlen = 0
                for d in result.body.iter_bytes(**kwargs):
                    l = len(d)
                    if l > 0:
                        self._write_to_stream(d, start + got)
                        self._update_progress(l)
                        got += l
                        gotlen += l
                        if chash:
                            chash.update(d)

                if result.content_length is not None and gotlen < result.content_length:
                    if not result.body.is_closed:
                        result.body.close()
                    continue
                break
            except Exception:
                pass

        return start, got, error, (chash.sum64() if chash else 0)


    def _write_to_stream(self, data, start):
        if self._writer_lock:
            with self._writer_lock:
                self._writer.seek(start - self._rstart)
                self._writer.write(data)
        else:
            self._writer.write(data)

    def _update_progress(self, increment: int):
        if self._progress_lock:
            with self._progress_lock:
                self._written += increment
                if self._request.progress_fn is not None:
                    self._request.progress_fn(increment, self._written, self._size_in_bytes)
        else:
            self._written += increment
            if self._request.progress_fn is not None:
                self._request.progress_fn(increment, self._written, self._size_in_bytes)

        #print(f'_update_progress: {increment}, {self._written}, {self._size_in_bytes}\n')

    def _update_process_result(self, result):
        #print(f'_update_process_result: {result}')
        if result is None:
            return

        if result[2] is not None:
            self._download_errors.append(result[2])
            return

        start = result[0]
        size = result[1]
        crc = result[3]

        if self._next_offset != start:
            if len(self._download_errors) == 0:
                self._download_errors.append(
                    ValueError(f'out of order, expect offset {self._next_offset}, but got {start}'))

        if len(self._download_errors) > 0:
            return

        self._next_offset = start + size

        if self._check_crc:
            self._ccrc = Crc64.combine(self._ccrc, crc, size)

        if self._checkpoint:
            self._checkpoint.dcrc64 = self._ccrc
            self._checkpoint.doffset = self._next_offset
            self._checkpoint.dump()


    def _assert_crc_same(self):
        if not self._check_crc:
            return

        scrc = self._headers.get('x-oss-hash-crc64ecma', None)
        if scrc is None:
            return

        ccrc = str(self._ccrc)
        if scrc != ccrc:
            raise self._wrap_error(exceptions.InconsistentError(client_crc=ccrc, server_crc=scrc))


    def _wrap_error(self, error: Exception) -> Exception:
        return DownloadError(
            path=f'oss://{self._request.bucket}/{self._request.key}',
            error=error
        )
