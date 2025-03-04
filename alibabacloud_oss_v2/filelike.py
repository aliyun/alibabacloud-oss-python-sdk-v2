# pylint: disable=line-too-long
import abc
import queue
import threading
from typing import Optional, Iterator, List, Generator
from concurrent.futures import ThreadPoolExecutor, Future
from .types import StreamBody, BodyType
from . import models
from . import exceptions
from . import utils
from . import defaults


DEFAULT_BUFFER_SIZE = 8 * 1024

class PathError(exceptions.BaseError):
    """
    PathError records an error and the operation and file path that caused it.
    """
    fmt = 'path error {op} {path}: {error}.'

    def __init__(self, **kwargs):
        exceptions.BaseError.__init__(self, **kwargs)
        self._error = kwargs.get("error", None)

    def unwrap(self) -> Exception:
        """returns the detail error"""
        return self._error


class AppendFileAPIClient(abc.ABC):
    """Abstract base class for append file client."""

    @abc.abstractmethod
    def head_object(self, request: models.HeadObjectRequest, **kwargs) -> models.HeadObjectResult:
        """ Queries information about the object in a bucket."""

    @abc.abstractmethod
    def append_object(self, request: models.AppendObjectRequest, **kwargs) -> models.AppendObjectResult:
        """
        Uploads an object by appending the object to an existing object.
        Objects created by using the AppendObject operation are appendable objects.
        """


class AppendOnlyFile:
    """AppendOnlyFile opens or creates the named file for appending"""

    def __init__(
        self,
        client: AppendFileAPIClient,
        bucket: str,
        key: str,
        request_payer: Optional[str] = None,
        create_parameter: Optional[models.AppendObjectRequest] = None,
    ) -> None:
        """
            client (AppendFileAPIClient, required): A agent that sends the request.
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs
            create_parameter (AppendObjectRequest, optional): The parameters when the object is first generated, supports below
                CacheControl, ContentEncoding, Expires, ContentType, ContentType, Metadata,SSE's parameters, Acl, StorageClass, Tagging.
                If the object exists, ignore this parameters
        """
        self._client = client

        # object info
        self._bucket = bucket
        self._key = key
        self._request_payer = request_payer
        self._create_parameter = create_parameter

        self._created = False

        # current write position
        self._offset = 0
        self._hash_crc64 = None

        self._try_open_object(bucket, key, request_payer)

        self._closed = False

    @property
    def mode(self) -> str:
        """String giving the file mode"""
        return 'ab'

    @property
    def name(self) -> str:
        """String giving the file in oss path"""
        return f'oss://{self._bucket}/{self._key}'

    @property
    def closed(self) -> bool:
        """True if the file descriptor will be closed by close()."""
        return self._closed

    ### Context manager ###
    def __enter__(self) -> 'AppendOnlyFile':
        self._check_closed('enter')
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()

    ### io apis ###
    def close(self) -> None:
        """Close the file."""
        self._closed = True

    def flush(self) -> None:
        """Flush write buffers.
        """
        self._check_closed('flush')
        if not self._created:
            self._write_bytes(b'')

    def tell(self) -> int:
        """Return an int indicating the current stream position."""
        self._check_closed('tell')
        return self._offset

    def writable(self) -> bool:
        """True if file was opened in a write mode."""
        self._check_closed('writable')
        return True

    def write(self, b):
        """Write bytes b to file, return number written.
        """
        self._check_closed('write')

        if b is None:
            return 0

        if not isinstance(b, bytes):
            raise self._wrap_error('write', TypeError(f'Not a bytes type, got {type(b)}'))

        return self._write_bytes(b)


    def write_from(self, b:BodyType):
        """Write any data to file, return number written.
        """
        self._check_closed('write')

        if b is None:
            return 0

        return self._write_any(b)


    def _try_open_object(self, bucket: str, key: str, request_payer:Optional[str]) -> None:
        try:
            result = self._client.head_object(models.HeadObjectRequest(
                bucket=bucket,
                key=key,
                request_payer=request_payer
            ))
        except exceptions.OperationError as err:
            serr = err.unwrap()
            if isinstance(serr, exceptions.ServiceError):
                if serr.status_code == 404:
                    # not found
                    return
            raise err

        if utils.safety_str(result.object_type).lower() !=  "appendable":
            raise self._wrap_error('open', ValueError('Not a appendable file'))

        self._created = True
        self._offset = result.content_length
        self._hash_crc64 = result.hash_crc64

    def _check_closed(self, op):
        """Internal: raise a ValueError if file is closed
        """
        if self.closed:
            raise self._wrap_error(op, ValueError("I/O operation on closed file."))

    def _apply_create_param_if_need(self, request: models.AppendObjectRequest):
        if self._created or self._create_parameter is None:
            return

        request.acl = self._create_parameter.acl
        request.storage_class = self._create_parameter.storage_class

        request.cache_control = self._create_parameter.cache_control
        request.content_disposition = self._create_parameter.content_disposition
        request.content_encoding = self._create_parameter.content_encoding
        request.expires = self._create_parameter.expires
        request.content_type = self._create_parameter.content_type
        request.server_side_encryption = self._create_parameter.server_side_encryption
        request.server_side_data_encryption = self._create_parameter.server_side_data_encryption
        request.server_side_encryption_key_id = self._create_parameter.server_side_encryption_key_id
        request.metadata = self._create_parameter.metadata
        request.tagging = self._create_parameter.tagging

    def _write_bytes(self, b):
        offset = self._offset
        hash_crc64 = self._hash_crc64
        error: Exception = None
        request = models.AppendObjectRequest(
            bucket=self._bucket,
            key=self._key,
            position=offset,
            request_payer=self._request_payer,
            body=b
        )

        self._apply_create_param_if_need(request)

        try:
            result = self._client.append_object(request)
            offset = result.next_position
            hash_crc64 = result.hash_crc64
        except Exception as err:
            error = err
            if isinstance(err, exceptions.OperationError):
                serr = err.unwrap()
                if isinstance(serr, exceptions.ServiceError):
                    if serr.code == 'PositionNotEqualToLength':
                        next_append = self._next_append_stat()
                        if next_append[0] >= 0 and offset + len(b) == next_append[0]:
                            error = None
                            offset = next_append[0]
                            hash_crc64 = next_append[1]

        if error:
            raise self._wrap_error('write', error)

        writern = offset - self._offset
        self._created = True
        self._offset = offset
        self._hash_crc64 = hash_crc64

        return writern

    def _write_any(self, b):
        offset = self._offset
        hash_crc64 = self._hash_crc64
        error: Exception = None
        request = models.AppendObjectRequest(
            bucket=self._bucket,
            key=self._key,
            position=offset,
            request_payer=self._request_payer,
            body=b
        )

        blen = utils.guess_content_length(b)

        self._apply_create_param_if_need(request)

        try:
            result = self._client.append_object(request)
            offset = result.next_position
            hash_crc64 = result.hash_crc64
        except Exception as err:
            error = err
            if isinstance(err, exceptions.OperationError):
                serr = err.unwrap()
                if isinstance(serr, exceptions.ServiceError):
                    if serr.code == 'PositionNotEqualToLength' and blen is not None:
                        next_append = self._next_append_stat()
                        if next_append[0] >= 0 and offset + blen == next_append[0]:
                            error = None
                            offset = next_append[0]
                            hash_crc64 = next_append[1]

        if error:
            raise self._wrap_error('write', error)

        writern = offset - self._offset
        self._created = True
        self._offset = offset
        self._hash_crc64 = hash_crc64

        return writern


    def _next_append_stat(self):
        try:
            result = self._client.head_object(models.HeadObjectRequest(
                bucket=self._bucket,
                key=self._key,
                request_payer=self._request_payer
            ))
            return result.content_length, result.hash_crc64
        except Exception:
            pass
        return -1, None

    def _wrap_error(self, op: str, error: Exception) -> Exception:
        return PathError(
            op = op,
            path=f'oss://{self._bucket}/{self._key}',
            error=error
        )



class OpenFileAPIClient(abc.ABC):
    """Abstract base class for open file client."""

    @abc.abstractmethod
    def head_object(self, request: models.HeadObjectRequest, **kwargs) -> models.HeadObjectResult:
        """ Queries information about the object in a bucket."""

    @abc.abstractmethod
    def get_object(self, request: models.GetObjectRequest, **kwargs) -> models.GetObjectResult:
        """
        Queries an object. To call this operation, you must have read permissions on the object.
        """

class ReadOnlyFile:
    """ReadOnlyFile opens the named file for reading."""

    def __init__(
        self,
        client: OpenFileAPIClient,
        bucket: str,
        key: str,
        version_id: Optional[str] = None,
        request_payer: Optional[str] = None,
        **kwargs
    ) -> None:
        """
            client (OpenFileAPIClient, required): A agent that sends the request.
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            version_id (str, optional): The version ID of the object.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs
        """
        self._client = client

        # object info
        self._bucket = bucket
        self._key = key
        self._version_id = version_id
        self._request_payer = request_payer

        #Source's Info
        self._size_in_bytes = None
        self._modtime = None
        self._etag = None
        self._headers = None
        self._stat_object()

        # current read position
        self._offset = 0

        # chunk remains buffer
        self._read_buf = None
        self._read_buf_offset = 0

    	# stream reader
        self._stream_reader: StreamBody = None
        self._stream_iter: Iterator = None

        # prefetch parameters
        self._enable_prefetch = kwargs.get('enable_prefetch', False)
        self._prefetch_num = kwargs.get('prefetch_num', defaults.DEFAULT_PREFETCH_NUM)
        self._chunk_size = kwargs.get('chunk_size', defaults.DEFAULT_PREFETCH_CHUNK_SIZE)
        self._prefetch_threshold = kwargs.get('prefetch_threshold', defaults.DEFAULT_PREFETCH_THRESHOLD)
        self._block_size = kwargs.get('block_size', None)

        # aysnc readers for prefetch
        self._executor: ThreadPoolExecutor = None
        self._generator: Generator = None
        self._prefetch_readers: List['_PrefetchDelegate'] = []

        # number of sequential read
        self._seq_read_amount = 0
        # number of out of order read
        self._num_ooo_read = 0

        self._closed = False
        self._readable = True
        self._seekable = True


    @property
    def mode(self) -> str:
        """String giving the file mode"""
        return 'rb'

    @property
    def name(self) -> str:
        """String giving the file in oss path"""
        if self._version_id:
            return f'oss://{self._bucket}/{self._key}?versionId={self._version_id}'
        return f'oss://{self._bucket}/{self._key}'

    @property
    def closed(self) -> bool:
        """True if the file descriptor will be closed by close()."""
        return self._closed

    ### Context manager ###
    def __enter__(self) -> 'ReadOnlyFile':
        self._check_closed('enter')
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()

    ### io apis ###
    def read(self, n=None):
        """Read and return up to n bytes, where n is an int.
        Return an empty bytes object at EOF.
        """
        self._check_closed('read')
        self._check_readable('read')
        d = self._read_at(self._offset, n)
        self._offset += len(d)
        return d

    def readall(self):
        """Read until EOF"""
        return self.read()

    def readinto(self, b):
        """Read bytes into a pre-allocated bytes-like object b.
        Returns an int representing the number of bytes read (0 for EOF)
        """
        self._check_closed('read')
        self._check_readable('read')
        n = self._read_at_into(self._offset, b)
        self._offset += n
        return n

    def seek(self, pos, whence=0):
        """Move to new file position.

        Argument offset is a byte count.  Optional argument whence defaults to
        SEEK_SET or 0 (offset from start of file, offset should be >= 0); other values
        are SEEK_CUR or 1 (move relative to current position, positive or negative),
        and SEEK_END or 2 (move relative to end of file, usually negative, although
        many platforms allow seeking beyond the end of a file).

        """
        self._check_closed('seek')
        try:
            pos_index = pos.__index__
        except AttributeError as exc:
            raise self._wrap_error('seek', TypeError(f"{pos!r} is not an integer")) from exc
        else:
            pos = pos_index()

        off = 0
        if whence == 0:
            off = pos
        elif whence == 1:
            off = self._offset + pos
        elif whence == 2:
            off = self._size_in_bytes + pos
        else:
            raise self._wrap_error('seek', ValueError("unsupported whence value"))

        if off < 0:
            raise self._wrap_error('seek', ValueError(f"negative seek position {off}"))

        if off > self._size_in_bytes:
            raise self._wrap_error('seek', ValueError(f"offset is unavailable {off}"))

        self._offset = off

        return off


    def tell(self):
        """Return an int indicating the current stream position."""
        self._check_closed('tell')
        return self._offset

    def close(self) -> None:
        """Close the file."""
        if self._closed:
            return

        self._close_readers()

        if self._executor:
            self._executor.shutdown()

        self._prefetch_readers = None
        self._executor = None
        self._closed = True

    def seekable(self):
        """True if file supports random-access."""
        self._check_closed('seekable')
        return self._seekable

    def readable(self):
        """True if file was opened in a read mode."""
        self._check_closed('readable')
        return self._readable

    def _check_readable(self, op):
        if not self._readable:
            raise self._wrap_error(op, ValueError("File not open for reading."))

    def _check_closed(self, op):
        """Internal: raise a ValueError if file is closed
        """
        if self.closed:
            raise self._wrap_error(op, ValueError("I/O operation on closed file."))

    def _close_readers(self):
        if self._generator:
            self._generator.close()
        self._generator = None

        self._close_readers1()


    def _close_readers1(self):
        # inner buffer
        self._read_buf = None
        #self._read_buf_offset = 0

        if self._stream_reader:
            self._stream_reader.close()
        self._stream_iter = None
        self._stream_reader = None

        for r in self._prefetch_readers:
            r.close()

        self._prefetch_readers = []


    def _stat_object(self) -> None:
        try:
            result = self._client.head_object(models.HeadObjectRequest(
                bucket=self._bucket,
                key=self._key,
                version_id=self._version_id,
                request_payer=self._request_payer
            ))
        except Exception as err:
            raise self._wrap_error('stat_object', err)

        self._size_in_bytes = result.content_length
        self._modtime = result.last_modified
        self._etag = result.etag
        self._headers = result.headers

    def _read_at(self, offset, n):
        nodata_val = b""
        empty_values = (b"")

        if offset >= self._size_in_bytes:
            return nodata_val

        # Special case for when the number of bytes to read is unspecified.
        if n is None or n < 0:
            current_size = 0
            chunks = []
            while True:
                chunk = self._next_chunk(offset + current_size)
                if chunk is None:
                    continue
                if chunk in empty_values:
                    nodata_val = chunk
                    break
                current_size += len(chunk)
                chunks.append(chunk)
            return b"".join(chunks) or nodata_val

        # The number of bytes to read is specified, return at most n bytes.
        b = bytearray(n.__index__())
        got = self._read_at_into(offset, b)
        if got is None:
            return None
        del b[got:]
        return bytes(b)

    def _read_at_into(self, offset, buf):
        """Read data into *buf*"""
        if offset >= self._size_in_bytes:
            return 0

        if not isinstance(buf, memoryview):
            buf = memoryview(buf)
        if buf.nbytes == 0:
            return 0
        buf = buf.cast('B')
        written = 0
        while written < len(buf):
            chunk = self._next_chunk(offset + written)
            if chunk is None:
                continue
            # eof
            if chunk == b'':
                break
            remains = len(buf) - written
            n = min(remains, len(chunk))
            buf[written:written + n] = chunk[:n]

            # Save the extra data in the buffer.
            if n < len(chunk):
                self._read_buf = chunk[n:]
                rn = len(self._read_buf)
                self._read_buf_offset -= rn
                self._seq_read_amount -= rn

            written += n
        return written

    def _next_chunk_direct(self, offset):
        if offset >= self._size_in_bytes:
            return b''

        if not self._stream_reader:
            result = self._client.get_object(models.GetObjectRequest(
                bucket=self._bucket,
                key=self._key,
                version_id=self._version_id,
                request_payer=self._request_payer,
                range_header=f'bytes={offset}-',
                range_behavior='standard'
            ))

            self._assert_same(offset, result)
            self._stream_reader = result.body
            self._stream_iter = result.body.iter_bytes()

        ret = None
        try:
            ret = next(self._stream_iter)
        except StopIteration:
            ret =  b''
        except Exception:
            #returns None and try again
            self._stream_reader.close()
            self._stream_reader = None
            self._stream_iter = None

        return ret

    def _prefetch_generator(self, offset):
        if not self._executor:
            self._executor = ThreadPoolExecutor(self._prefetch_num)

        self._close_readers1()
        prefetch_num = max(1, self._prefetch_num)

        for start in range(offset, self._size_in_bytes, self._chunk_size):
            self._prefetch_readers.append(_PrefetchDelegate(self, start))
            if len(self._prefetch_readers) < prefetch_num:
                continue

            # read data from first reader
            reader = self._prefetch_readers[0]
            curr_iter = iter(reader)
            for d in curr_iter:
                if reader.failed:
                    raise ValueError("Meets error, fall back to read serially")
                yield d

            reader.close()
            del self._prefetch_readers[0]

        # remians
        for reader in self._prefetch_readers:
            curr_iter = iter(reader)
            for d in curr_iter:
                if reader.failed:
                    raise ValueError("Meets error, fall back to read serially")
                yield d
            reader.close()

        self._prefetch_readers = []


    def _next_chunk(self, offset):
        if self._read_buf_offset != offset:
            self._read_buf_offset = offset
            self._seq_read_amount = 0

            if self._generator:
                self._num_ooo_read += 1

            self._close_readers()

        if self._read_buf:
            data = self._read_buf
            self._read_buf = None
        else:

            # switch to prefetch reader
            if (self._enable_prefetch and
                self._seq_read_amount >= self._prefetch_threshold and
                self._num_ooo_read < 3):

                if not self._generator:
                    self._generator = self._prefetch_generator(offset)

                try:
                    data = next(self._generator)
                except StopIteration:
                    data =  b''
                except Exception:
                    # fall back to read serially
                    self._seq_read_amount = 0
                    self._close_readers()
                    data = self._next_chunk_direct(offset)
            else:
                data = self._next_chunk_direct(offset)

        if data is not None:
            cn = len(data)
            self._read_buf_offset += cn
            self._seq_read_amount += cn

        return data

    def _assert_same(self, offset: int, result: models.GetObjectResult):
        err = _check_object_same(self._modtime, self._etag, offset, result)
        if err:
            raise self._wrap_error('get_object', err)

    def _wrap_error(self, op: str, error: Exception) -> Exception:
        return PathError(
            op = op,
            path=f'oss://{self._bucket}/{self._key}',
            error=error
        )

class CancelTask(Exception):
    'Exception raised by cancel prefetch task.'
    pass

class _PrefetchDelegate:

    def __init__(
        self,
        base: ReadOnlyFile,
        offset: str,
    ) -> None:
        self._base = base
        self._offset = offset
        self._block_size = base._block_size

        self._data_queue = queue.Queue()
        self._get_timeout = 0.1

        self._canceling = False
        self._closed = False
        self._stream_reader: StreamBody = None
        self._stream_iter: Iterator = None
        self._condition = threading.Condition()

        # source info
        self._modtime = base._modtime
        self._etag = base._etag

        # task info
        size = min(base._size_in_bytes - offset, base._chunk_size)
        self._request =models.GetObjectRequest(
            bucket=base._bucket,
            key=base._key,
            version_id=base._version_id,
            request_payer=base._request_payer
        )
        self._failed = False
        self._task = self._base._executor.submit(self._download_part, (offset, size))

    @property
    def failed(self) -> bool:
        """True if the delegate meets error."""
        return self._failed

    @property
    def closed(self) -> bool:
        """True if the delegate will be closed."""
        return self._closed

    def __iter__(self):
        return self

    def __next__(self):
        try:
            d = self._data_queue.get(timeout=self._get_timeout)
            if d in (b''):
                raise StopIteration
            return d
        except queue.Empty:
            return None

    def get_task(self) -> Future:
        """get task
        """
        return self._task

    def close(self):
        """close and release all resources
        """
        if self._closed:
            return

        if not self._task.cancel():
            # running or done
            with self._condition:
                self._canceling = True

            # wait task done
            try:
                self._task.result()
            except Exception:
                pass

        # release all
        if self._stream_reader:
            self._stream_reader.close()

        if self._data_queue:
            self._data_queue.queue.clear()

        self._stream_reader = None
        self._stream_iter = None
        self._data_queue = None
        self._closed = True


    def _download_part(self, part):
        start = part[0]
        size = part[1]
        try:
            self._download_part_check_cancel(start, size)
        except Exception:
            self._failed = True


    def _download_part_check_cancel(self, start, size):
        got = 0
        error: Exception = None
        request = self._request

        while True:
            if self._canceling:
                error = CancelTask()
                break

            request.range_header = f'bytes={start + got}-{start + size - 1}'
            request.range_behavior = 'standard'
            result = self._base._client.get_object(request)

            error = _check_object_same(self._modtime, self._etag, start, result)
            if error:
                break

            try:
                kwargs = {}
                if self._block_size:
                    kwargs['block_size'] = self._block_size
                with self._condition:
                    self._stream_reader = result.body
                    self._stream_iter = result.body.iter_bytes(**kwargs)
                    if self._canceling:
                        error = CancelTask()
                        break

                for d in self._stream_iter:
                    if self._canceling:
                        error = CancelTask()
                        break
                    got += len(d)
                    self._data_queue.put(d)
                break
            except Exception:
                pass
            finally:
                if self._stream_reader:
                    self._stream_reader.close()
                self._stream_reader = None
                self._stream_iter = None

        if error:
            raise error

        if got != size:
            raise ValueError("expect size {size}, but got {got}")

        self._data_queue.put(b'')

def _check_object_same(src_modtime, src_etag, offset: int, result: models.GetObjectResult):
    modtime = result.last_modified
    etag = result.etag
    got_offset = 0
    if (crange := result.headers.get("Content-Range", None)):
        content_range = utils.parse_content_range(crange)
        got_offset = content_range[0]

    if got_offset != offset:
        return ValueError(f"Range get fail, expect offset:{offset}, got offset:{got_offset}")

    if ((modtime and src_modtime and modtime != src_modtime) or
        (etag and src_etag and etag != src_etag)):
        return ValueError(f"Source file is changed, origin info[{src_modtime},{src_etag}], new info [{modtime},{etag}]")

    return None
