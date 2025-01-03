import sys
import struct
from typing import Any, Iterator
from ..types import OperationInput, CaseInsensitiveDict, StreamBody
from .. import serde
from .. import serde_utils
from .. import models
from .._client import _SyncClientImpl
from ..crc import Crc32
from ..exceptions import DeserializationError

"""
The adapter class for Select object's response.
The response consists of frames. Each frame has the following format:

Type  |   Payload Length |  Header Checksum | Payload | Payload Checksum

|<4-->|  <--4 bytes------><---4 bytes-------><-n/a-----><--4 bytes--------->
And we have three kind of frames.
Data Frame:
Type:8388609
Payload:   Offset    |    Data
           <-8 bytes>

Continuous Frame
Type:8388612
Payload: Offset  (8-bytes)

End Frame
Type:8388613
Payload: Offset | total scanned bytes | http status code | error message
    <-- 8bytes--><-----8 bytes--------><---4 bytes-------><---variabe--->

"""

def _chunked_bytes_iterator(b, chunk_size=32 * 1024):
    start = 0
    while start < len(b):
        yield b[start:start + chunk_size]
        start += chunk_size

class SelectObjectStreamBody(StreamBody):
    """Select Object Stream Body
    """
    _CHUNK_SIZE = 8 * 1024
    _CONTINIOUS_FRAME_TYPE = 8388612
    _DATA_FRAME_TYPE = 8388609
    _END_FRAME_TYPE = 8388613
    _META_END_FRAME_TYPE = 8388614
    _JSON_META_END_FRAME_TYPE = 8388615
    _FRAMES_FOR_PROGRESS_UPDATE = 10

    def __init__(
        self,
        stream: StreamBody,
        output_raw_data: bool,
        enable_crc: bool = False
    ) -> None:
        self._stream = stream
        self._output_raw_data = output_raw_data
        self._enable_crc = enable_crc

    def __enter__(self) -> "SelectObjectStreamBody":
        self._stream.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self._stream.__exit__(*args)

    @property
    def is_closed(self) -> bool:
        return self._stream.is_closed

    @property
    def is_stream_consumed(self) -> bool:
        return self._stream.is_stream_consumed

    @property
    def content(self) -> bytes:
        if not self._stream.is_stream_consumed:
            self._stream.read()
        if self._output_raw_data is True:
            return self._stream.content
        else:
            return self._extract_all(self._stream.content)

    def read(self) -> bytes:
        if self._output_raw_data is True:
            return self._stream.read()
        else:
            return self._extract_all(self._stream.read())

    def close(self) -> None:
        self._stream.close()

    def iter_bytes(self, **kwargs: Any) -> Iterator[bytes]:
        if self._output_raw_data is True:
            return self._stream.iter_bytes(**kwargs)
        else:
            return _SelectResponseAdapter(self._stream.iter_bytes(**kwargs), self._enable_crc)

    def _extract_all(self, data: bytes) -> bytes:
        dd = b''
        for d in _SelectResponseAdapter(_chunked_bytes_iterator(data), self._enable_crc):
            dd += d

        return dd

class _SelectResponseAdapter(object):
    _CHUNK_SIZE = 8 * 1024
    _CONTINIOUS_FRAME_TYPE = 8388612
    _DATA_FRAME_TYPE = 8388609
    _END_FRAME_TYPE = 8388613
    _META_END_FRAME_TYPE = 8388614
    _JSON_META_END_FRAME_TYPE = 8388615
    _FRAMES_FOR_PROGRESS_UPDATE = 10

    def __init__(
        self,
        content_iter: Iterator[bytes],
        enable_crc: bool = False
    ):
        self.frame_off_set = 0
        self.frame_length = 0
        self.frame_data = b''
        self.check_sum_flag = 0
        self.file_offset = 0
        self.finished = 0
        self.raw_buffer = b''
        self.raw_buffer_offset = 0
        self.content_iter = content_iter
        self.enable_crc = enable_crc
        self.payload = b''
        self.request_id = ''
        self.total_scanned_bytes = 0
        self.splits = 0
        self.rows = 0
        self.columns = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self._next()

    def _next(self):
        while self.finished == 0:
            if self.frame_off_set < self.frame_length:
                data = self.frame_data[self.frame_off_set: self.frame_length]
                self.frame_length = self.frame_off_set = 0
                return data
            else:
                self._read_next_frame()

        raise StopIteration

    def _read_raw(self, amt):
        ret = b''
        read_count = 0
        while amt > 0 and self.finished == 0:
            size = len(self.raw_buffer)
            if size == 0:
                self.raw_buffer = next(self.content_iter)
                self.raw_buffer_offset = 0
                size = len(self.raw_buffer)
                if size == 0:
                    break

            if size - self.raw_buffer_offset >= amt:
                data = self.raw_buffer[self.raw_buffer_offset:self.raw_buffer_offset + amt]
                data_size = len(data)
                self.raw_buffer_offset += data_size
                ret += data
                read_count += data_size
                amt -= data_size
            else:
                data = self.raw_buffer[self.raw_buffer_offset:]
                data_len = len(data)
                ret += data
                read_count += data_len
                amt -= data_len
                self.raw_buffer = b''

        return ret

    def _change_endianness_if_needed(self, bytes_array):
        if sys.byteorder == 'little':
            bytes_array.reverse()

    def _read_next_frame(self):
        frame_type = bytearray(self._read_raw(4))
        payload_length = bytearray(self._read_raw(4))
        self._change_endianness_if_needed(payload_length)  # convert to little endian
        payload_length_val = struct.unpack("I", bytes(payload_length))[0]
        header_checksum = bytearray(self._read_raw(4))

        frame_type[0] = 0  # mask the version bit
        self._change_endianness_if_needed(frame_type)  # convert to little endian
        frame_type_val = struct.unpack("I", bytes(frame_type))[0]
        if (frame_type_val != _SelectResponseAdapter._DATA_FRAME_TYPE and
                frame_type_val != _SelectResponseAdapter._CONTINIOUS_FRAME_TYPE and
                frame_type_val != _SelectResponseAdapter._END_FRAME_TYPE and
                frame_type_val != _SelectResponseAdapter._META_END_FRAME_TYPE and
                frame_type_val != _SelectResponseAdapter._JSON_META_END_FRAME_TYPE):

            raise Exception("Unexpected frame type:" + str(frame_type_val))

        self.payload = self._read_raw(payload_length_val)
        file_offset_bytes = bytearray(self.payload[0:8])
        self._change_endianness_if_needed(file_offset_bytes)
        self.file_offset = struct.unpack("Q", bytes(file_offset_bytes))[0]
        if frame_type_val == _SelectResponseAdapter._DATA_FRAME_TYPE:
            self.frame_length = payload_length_val - 8
            self.frame_off_set = 0
            self.check_sum_flag = 1
            self.frame_data = self.payload[8:]
            checksum = bytearray(self._read_raw(4))  # read checksum crc32
            self._change_endianness_if_needed(checksum)
            checksum_val = struct.unpack("I", bytes(checksum))[0]
            if self.enable_crc:
                crc32 = Crc32()
                crc32.update(self.payload)
                checksum_calc = crc32.crc
                if checksum_val != checksum_calc:
                    raise Exception(
                        "Incorrect checksum: Actual" + str(checksum_val) + ". Calculated:" + str(checksum_calc))

        elif frame_type_val == _SelectResponseAdapter._CONTINIOUS_FRAME_TYPE:
            self.frame_length = self.frame_off_set = 0
            self.check_sum_flag = 1
            self._read_raw(4)
        elif frame_type_val == _SelectResponseAdapter._END_FRAME_TYPE:
            self.frame_off_set = 0
            scanned_size_bytes = bytearray(self.payload[8:16])
            status_bytes = bytearray(self.payload[16:20])
            self._change_endianness_if_needed(status_bytes)
            status = struct.unpack("I", bytes(status_bytes))[0]
            error_msg_size = payload_length_val - 20
            error_msg = b''
            error_code = b''
            if error_msg_size > 0:
                error_msg = self.payload[20:error_msg_size + 20]
                error_code_index = error_msg.find(b'.')
                if error_code_index >= 0 and error_code_index < error_msg_size - 1:
                    error_code = error_msg[0:error_code_index]
                    error_msg = error_msg[error_code_index + 1:]

            if status // 100 != 2:
                raise Exception(status, error_code, error_msg)
            self.frame_length = 0
            self._read_raw(4)  # read the payload checksum
            self.frame_length = 0
            self.finished = 1
        elif frame_type_val == _SelectResponseAdapter._META_END_FRAME_TYPE or frame_type_val == _SelectResponseAdapter._JSON_META_END_FRAME_TYPE:
            self.frame_off_set = 0
            scanned_size_bytes = bytearray(self.payload[8:16])
            self._change_endianness_if_needed(scanned_size_bytes)
            self.total_scanned_bytes = struct.unpack("Q", bytes(scanned_size_bytes))[0]
            status_bytes = bytearray(self.payload[16:20])
            self._change_endianness_if_needed(status_bytes)
            status = struct.unpack("I", bytes(status_bytes))[0]
            splits_bytes = bytearray(self.payload[20:24])
            self._change_endianness_if_needed(splits_bytes)
            self.splits = struct.unpack("I", bytes(splits_bytes))[0]
            lines_bytes = bytearray(self.payload[24:32])
            self._change_endianness_if_needed(lines_bytes)
            self.rows = struct.unpack("Q", bytes(lines_bytes))[0]

            error_index = 36
            if frame_type_val == _SelectResponseAdapter._META_END_FRAME_TYPE:
                column_bytes = bytearray(self.payload[32:36])
                self._change_endianness_if_needed(column_bytes)
                self.columns = struct.unpack("I", bytes(column_bytes))[0]
            else:
                error_index = 32

            error_size = payload_length_val - error_index
            error_msg = b''
            error_code = b''
            if (error_size > 0):
                error_msg = self.payload[error_index:error_index + error_size]
                error_code_index = error_msg.find(b'.')
                if error_code_index >= 0 and error_code_index < error_size - 1:
                    error_code = error_msg[0:error_code_index]
                    error_msg = error_msg[error_code_index + 1:]

            self._read_raw(4)  # read the payload checksum
            self.final_status = status
            self.frame_length = 0
            self.finished = 1
            if (status / 100 != 2):
                raise Exception(status, error_code, error_msg)


def select_object(client: _SyncClientImpl, request: models.SelectObjectRequest, **kwargs) -> models.SelectObjectResult:
    """
    SelectObject Executes SQL statements to perform operations on an object and obtains the execution results.

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (SelectObjectRequest): The request for the SelectObject operation.

    Returns:
        SelectObjectResult: The result for the SelectObject operation.
    """
    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='SelectObject',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            bucket=request.bucket,
            key=request.key,
            op_metadata={'response-stream':True}
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ],
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    enable_payload_crc = None
    if request.select_request.output_serialization is not None:
        enable_payload_crc = request.select_request.output_serialization.enable_payload_crc

    output_raw_data = op_output.headers.get("x-oss-select-output-raw", '') == "true"

    return serde.deserialize_output(
        result=models.SelectObjectResult(
            body=SelectObjectStreamBody(op_output.http_response, output_raw_data, enable_payload_crc)
        ),
        op_output=op_output,
    )


def create_select_object_meta(client: _SyncClientImpl, request: models.CreateSelectObjectMetaRequest, **kwargs) -> models.CreateSelectObjectMetaResult:
    """
    create_select_object_meta synchronously

    Args:
        client (_SyncClientImpl): A agent that sends the request.
        request (CreateSelectObjectMetaRequest): The request for the CreateSelectObjectMeta operation.

    Returns:
        CreateSelectObjectMetaResult: The result for the CreateSelectObjectMeta operation.
    """

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='CreateSelectObjectMeta',
            method='POST',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            bucket=request.bucket,
            key=request.key,
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input, **kwargs)

    try:
        it = _SelectResponseAdapter(_chunked_bytes_iterator(op_output.http_response.content))
        for _ in it:
            """"""
        result = models.CreateSelectObjectMetaResult(
            total_scanned_bytes = it.total_scanned_bytes,
            splits_count=it.splits,
            rows_count=it.rows,
            cols_count=it.columns,
        )
    except Exception as e:
        raise DeserializationError(
            error=f'parse CreateSelectObjectMetaResult fail, caused by {e}')

    return serde.deserialize_output(
        result=result,
        op_output=op_output,
    )
