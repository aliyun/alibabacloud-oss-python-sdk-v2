"""Models for select object operation APIs"""
# pylint: disable=too-few-public-methods, too-many-instance-attributes, unnecessary-lambda
# pylint: disable=super-init-not-called, too-many-lines, line-too-long, too-many-arguments
# pylint: disable=too-many-locals
import struct
import sys
from .. import serde
from typing import Optional, Any
from ..crc import Crc32


class SelectResult(object):
    def __init__(self, resp, progress_callback=None, content_length=None, crc_enabled=False):
        self.select_resp = SelectResponseAdapter(resp, progress_callback, content_length, enable_crc=crc_enabled)

    def read(self):
        return self.select_resp.response.read()

    def close(self):
        self.select_resp.response.close()

    def __iter__(self):
        return iter(self.select_resp)

    def __next__(self):
        return self.select_resp.next()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SelectResponseAdapter(object):
    _CHUNK_SIZE = 8 * 1024
    _CONTINIOUS_FRAME_TYPE = 8388612
    _DATA_FRAME_TYPE = 8388609
    _END_FRAME_TYPE = 8388613
    _META_END_FRAME_TYPE = 8388614
    _JSON_META_END_FRAME_TYPE = 8388615
    _FRAMES_FOR_PROGRESS_UPDATE = 10

    def __init__(self, response, progress_callback=None, content_length=None, enable_crc=False):
        self.response = response
        self.frame_off_set = 0
        self.frame_length = 0
        self.frame_data = b''
        self.check_sum_flag = 0
        self.file_offset = 0
        self.finished = 0
        self.raw_buffer = b''
        self.raw_buffer_offset = 0
        self.callback = progress_callback
        self.frames_since_last_progress_report = 0
        self.content_length = content_length
        self.resp_content_iter = response.iter_bytes()
        self.enable_crc = enable_crc
        self.payload = b''
        self.output_raw_data = response.headers.get("x-oss-select-output-raw", '') == "true"
        self.request_id = response.headers.get("x-oss-request-id", '')
        self.splits = 0
        self.rows = 0
        self.columns = 0

    def read(self):
        if self.finished:
            return b''

        content = b''
        for data in self:
            content += data

        return content

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.output_raw_data == True:
            data = next(self.resp_content_iter)
            if len(data) != 0:
                return data
            else:
                raise StopIteration

        while self.finished == 0:
            if self.frame_off_set < self.frame_length:
                data = self.frame_data[self.frame_off_set: self.frame_length]
                self.frame_length = self.frame_off_set = 0
                return data
            else:
                self.read_next_frame()
                self.frames_since_last_progress_report += 1
                if (self.frames_since_last_progress_report >= SelectResponseAdapter._FRAMES_FOR_PROGRESS_UPDATE and self.callback is not None):
                    self.callback(self.file_offset, self.content_length)
                    self.frames_since_last_progress_report = 0

        raise StopIteration

    def read_raw(self, amt):
        ret = b''
        read_count = 0
        while amt > 0 and self.finished == 0:
            size = len(self.raw_buffer)
            if size == 0:
                self.raw_buffer = next(self.resp_content_iter)
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

    def change_endianness_if_needed(self, bytes_array):
        if sys.byteorder == 'little':
            bytes_array.reverse()

    def read_next_frame(self):
        frame_type = bytearray(self.read_raw(4))
        payload_length = bytearray(self.read_raw(4))
        self.change_endianness_if_needed(payload_length)  # convert to little endian
        payload_length_val = struct.unpack("I", bytes(payload_length))[0]
        header_checksum = bytearray(self.read_raw(4))

        frame_type[0] = 0  # mask the version bit
        self.change_endianness_if_needed(frame_type)  # convert to little endian
        frame_type_val = struct.unpack("I", bytes(frame_type))[0]
        if (frame_type_val != SelectResponseAdapter._DATA_FRAME_TYPE and
                frame_type_val != SelectResponseAdapter._CONTINIOUS_FRAME_TYPE and
                frame_type_val != SelectResponseAdapter._END_FRAME_TYPE and
                frame_type_val != SelectResponseAdapter._META_END_FRAME_TYPE and
                frame_type_val != SelectResponseAdapter._JSON_META_END_FRAME_TYPE):

            raise Exception(self.request_id, "Unexpected frame type:" + str(frame_type_val))

        self.payload = self.read_raw(payload_length_val)
        file_offset_bytes = bytearray(self.payload[0:8])
        self.change_endianness_if_needed(file_offset_bytes)
        self.file_offset = struct.unpack("Q", bytes(file_offset_bytes))[0]
        if frame_type_val == SelectResponseAdapter._DATA_FRAME_TYPE:
            self.frame_length = payload_length_val - 8
            self.frame_off_set = 0
            self.check_sum_flag = 1
            self.frame_data = self.payload[8:]
            checksum = bytearray(self.read_raw(4))  # read checksum crc32
            self.change_endianness_if_needed(checksum)
            checksum_val = struct.unpack("I", bytes(checksum))[0]
            if self.enable_crc:
                crc32 = Crc32()
                crc32.update(self.payload)
                checksum_calc = crc32.crc
                if checksum_val != checksum_calc:
                    raise Exception(
                        "Incorrect checksum: Actual" + str(checksum_val) + ". Calculated:" + str(checksum_calc),
                        self.request_id)

        elif frame_type_val == SelectResponseAdapter._CONTINIOUS_FRAME_TYPE:
            self.frame_length = self.frame_off_set = 0
            self.check_sum_flag = 1
            self.read_raw(4)
        elif frame_type_val == SelectResponseAdapter._END_FRAME_TYPE:
            self.frame_off_set = 0
            scanned_size_bytes = bytearray(self.payload[8:16])
            status_bytes = bytearray(self.payload[16:20])
            self.change_endianness_if_needed(status_bytes)
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
            if self.callback is not None:
                self.callback(self.file_offset, self.content_length)
            self.read_raw(4)  # read the payload checksum
            self.frame_length = 0
            self.finished = 1
        elif frame_type_val == SelectResponseAdapter._META_END_FRAME_TYPE or frame_type_val == SelectResponseAdapter._JSON_META_END_FRAME_TYPE:
            self.frame_off_set = 0
            scanned_size_bytes = bytearray(self.payload[8:16])
            status_bytes = bytearray(self.payload[16:20])
            self.change_endianness_if_needed(status_bytes)
            status = struct.unpack("I", bytes(status_bytes))[0]
            splits_bytes = bytearray(self.payload[20:24])
            self.change_endianness_if_needed(splits_bytes)
            self.splits = struct.unpack("I", bytes(splits_bytes))[0]
            lines_bytes = bytearray(self.payload[24:32])
            self.change_endianness_if_needed(lines_bytes)
            self.rows = struct.unpack("Q", bytes(lines_bytes))[0]

            error_index = 36
            if frame_type_val == SelectResponseAdapter._META_END_FRAME_TYPE:
                column_bytes = bytearray(self.payload[32:36])
                self.change_endianness_if_needed(column_bytes)
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

            self.read_raw(4)  # read the payload checksum
            self.final_status = status
            self.frame_length = 0
            self.finished = 1
            if (status / 100 != 2):
                raise Exception(status, error_code, error_msg)


class JSONInput(serde.Model):
    """Input JSON format parameters."""

    def __init__(
        self,
        type: Optional[str] = None,
        range: Optional[str] = None,
        parse_json_number_as_string: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            type (str, optional): Specify the type of JSON input: Document, Lines.
            range (str, optional): Specify the scope of the query file (optional). Supports two formats:
                Search by row: line range=start end. For example, line range=10-20 means scanning lines 10 to 20.
                Search by Split: split range=start end. For example, split range=10-20 means scanning the 10th to 20th split.
                Both start and end are inclusive. Its format is consistent with the range parameter in range get.
                Only used when the document is CSV or JSON type is LINES.
            parse_json_number_as_string (bool, optional): Parse numbers (integers and floating-point numbers) in JSON into strings.
                At present, parsing floating-point numbers in JSON results in a loss of precision.
                If you want to preserve the original data in its entirety, this option is recommended.
                If numerical calculations are required, they can be cast into the desired format in SQL, such as int, double, or decimal.
                Default value: false
        """
        super().__init__(**kwargs)
        self.type = type
        self.range = range
        self.parse_json_number_as_string = parse_json_number_as_string


    _attribute_map = {
        "type": {"tag": "xml", "rename": "Type"},
        "range": {"tag": "xml", "rename": "Range"},
        "parse_json_number_as_string": {"tag": "xml", "rename": "ParseJsonNumberAsString", "type": "bool"},
    }
    _xml_map = {
        "name": "JSON"
    }


class CSVInput(serde.Model):
    """Input CSV format parameters."""

    def __init__(
        self,
        file_header_info: Optional[str] = None,
        record_delimiter: Optional[str] = None,
        field_delimiter: Optional[str] = None,
        quote_character: Optional[str] = None,
        comment_character: Optional[str] = None,
        range: Optional[str] = None,
        allow_quoted_record_delimiter: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            file_header_info (str, Optional): Specify CSV file header information (optional)
                Value:
                    Use: This CSV file has header information and can use CSV column names as column names in Select.
                    Ignore: This CSV file has header information, but CSV column names cannot be used as column names in Select.
                    None: This file has no header information and is the default value.
            record_delimiter (str, Optional): Specify line breaks in Base64 encoding. The default value is \ n (optional).
                The value before encoding is at most two characters, represented by the ANSI value of the character,
                for example, in Java, \ n is used to represent line breaks.
            field_delimiter (str, Optional): Specify CSV column delimiter with Base64 encoding. The default value is, (optional).
                The value before encoding must be one character, represented by the ANSI value of the character,
                for example, in Java, representing a comma.
            quote_character (str, Optional): Specify the quotation mark characters for CSV in Base64 encoding.
                The default value is \ "(optional). Line breaks and column separators within quotation marks in CSV will be treated as regular characters.
                The value before encoding must be one character, represented by the ANSI value of the character,
                for example, using '\' to indicate quotation marks in Java.
            comment_character (str, Optional): Specify the annotation character for CSV, encoded in Base64 format.
                The default value is empty (i.e. no comment character).
            range (str, Optional): Specify the scope of the query file (optional). Supports two formats:
                Search by row: line range=start end. For example, line range=10-20 means scanning lines 10 to 20.
                Search by Split: split range=start end. For example, split range=10-20 means scanning the 10th to 20th split.
                Both start and end are inclusive. Its format is consistent with the range parameter in range get.
                Only used when the document is CSV or JSON type is LINES.
            allow_quoted_record_delimiter (bool, Optional): Specify whether the CSV content contains line breaks within quotation marks.
                For example, if a column value is "abc \ ndef" (where \ n is a line break), then the value needs to be set to true.
                When the value is false, select supports the semantics of header range, which enables more efficient sharding queries.
        """
        super().__init__(**kwargs)
        self.file_header_info = file_header_info
        self.record_delimiter = record_delimiter
        self.field_delimiter = field_delimiter
        self.quote_character = quote_character
        self.comment_character = comment_character
        self.range = range
        self.allow_quoted_record_delimiter = allow_quoted_record_delimiter

    _attribute_map = {
        "file_header_info": {"tag": "xml", "rename": "FileHeaderInfo"},
        "record_delimiter": {"tag": "xml", "rename": "RecordDelimiter"},
        "field_delimiter": {"tag": "xml", "rename": "FieldDelimiter"},
        "quote_character": {"tag": "xml", "rename": "QuoteCharacter"},
        "comment_character": {"tag": "xml", "rename": "CommentCharacter"},
        "range": {"tag": "xml", "rename": "Range"},
        "allow_quoted_record_delimiter": {"tag": "xml", "rename": "AllowQuotedRecordDelimiter", "type": "bool"},
    }
    _xml_map = {
        "name": "CSV"
    }


class InputSerialization(serde.Model):
    """Input serialization parameters."""

    def __init__(
        self,
        compression_type: Optional[str] = None,
        json_input: Optional[JSONInput] = None,
        csv_input: Optional[CSVInput] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            compression_type (str, Optional): Specify file compression type: None | GZIP.
            json_input (JSONInput, Optional): Input JSON format parameters.
            csv_input (CSVInput, Optional): Input CSV format parameters.

        """
        super().__init__(**kwargs)
        self.compression_type = compression_type
        self.json_input = json_input
        self.csv_input = csv_input

    _attribute_map = {
        "compression_type": {"tag": "xml", "rename": "CompressionType"},
        "json_input": {"tag": "xml", "rename": "JSON", "type": "JSONInput"},
        "csv_input": {"tag": "xml", "rename": "CSV", "type": "CSVInput"},
    }
    _xml_map = {
        "name": "InputSerialization"
    }

class JSONOutput(serde.Model):
    """Format parameters for outputting JSON."""

    def __init__(
        self,
        record_delimiter: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            record_delimiter (str, Optional): Specify line breaks in Base64 encoding. The default value is \ n (optional).
                The value before encoding is at most two characters, represented by the ANSI value of the character,
                for example, in Java, \ n is used to represent line breaks.

        """
        super().__init__(**kwargs)
        self.record_delimiter = record_delimiter

    _attribute_map = {
        "record_delimiter": {"tag": "xml", "rename": "RecordDelimiter"},
    }
    _xml_map = {
        "name": "JSON"
    }

class CSVOutput(serde.Model):
    """Output CSV format parameters."""

    def __init__(
        self,
        record_delimiter: Optional[str] = None,
        field_delimiter: Optional[str] = None,
        quote_character: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            record_delimiter (str, Optional): Specify line breaks in Base64 encoding. The default value is \ n (optional).
                The value before encoding is at most two characters, represented by the ANSI value of the character,
                for example, in Java, \ n is used to represent line breaks..
            field_delimiter (str, Optional): Specify CSV column delimiter with Base64 encoding.
                The default value is, (optional). The value before encoding must be one character, represented by the ANSI value of the character,
                for example, in Java, representing a comma.
            quote_character (str, Optional): Specify the quotation mark characters for CSV in Base64 encoding.
                The default value is \ "(optional). Line breaks and column separators within quotation marks in CSV will be treated as regular characters.
                The value before encoding must be one character, represented by the ANSI value of the character,
                for example, using '\' to indicate quotation marks in Java.
        """
        super().__init__(**kwargs)
        self.record_delimiter = record_delimiter
        self.field_delimiter = field_delimiter
        self.quote_character = quote_character

    _attribute_map = {
        "record_delimiter": {"tag": "xml", "rename": "RecordDelimiter"},
        "field_delimiter": {"tag": "xml", "rename": "FieldDelimiter"},
        "quote_character": {"tag": "xml", "rename": "QuoteCharacter"},
    }
    _xml_map = {
        "name": "CSV"
    }

class OutputSerialization(serde.Model):
    """Output serialization parameters."""

    def __init__(
        self,
        csv_output: Optional[CSVOutput] = None,
        json_output: Optional[JSONOutput] = None,
        output_raw_data: Optional[bool] = None,
        keep_all_columns: Optional[bool] = None,
        enable_payload_crc: Optional[bool] = None,
        output_header: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            csv_output (CSVOutput, Optional): Output CSV format parameters.
            json_output (JSONOutput, Optional): Format parameters for outputting JSON.
            output_raw_data (bool, Optional): Output serialization parameters.
            keep_all_columns (bool, Optional): Specify the location of all CSV columns in the return result (optional, default value is false).
                But only columns that appear in the select statement will have values, while columns that do not appear will be empty.
                The data in each row of the returned result will be arranged in CSV column order from low to high.
            enable_payload_crc (bool, Optional): There will be a 32-bit crc32 checksum in each frame.
                The client can calculate the Crc32 value of the corresponding payload for data integrity verification.
            output_header (bool, Optional): Output CSV header information at the beginning of the returned result.
        """
        super().__init__(**kwargs)
        self.csv_output = csv_output
        self.json_output = json_output
        self.output_raw_data = output_raw_data
        self.keep_all_columns = keep_all_columns
        self.enable_payload_crc = enable_payload_crc
        self.output_header = output_header

    _attribute_map = {
        "csv_output": {"tag": "xml", "rename": "CSV", "type": "CSVOutput"},
        "json_output": {"tag": "xml", "rename": "JSON", "type": "JSONOutput"},
        "output_raw_data": {"tag": "xml", "rename": "OutputRawData", "type": "bool"},
        "keep_all_columns": {"tag": "xml", "rename": "KeepAllColumns", "type": "bool"},
        "enable_payload_crc": {"tag": "xml", "rename": "EnablePayloadCrc", "type": "bool"},
        "output_header": {"tag": "xml", "rename": "OutputHeader", "type": "bool"},
    }
    _xml_map = {
        "name": "OutputSerialization"
    }

class SelectOptions(serde.Model):
    """Additional optional parameters."""

    def __init__(
        self,
        skip_partial_data_record: Optional[bool] = None,
        max_skipped_records_allowed: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            skip_partial_data_record (bool, Optional): Ignore rows with missing data. When the parameter is false,
                OSS will ignore missing columns (with values treated as null) without reporting an error.
                When the parameter is true, the row of data is skipped as a whole due to incompleteness.
                When the number of skipped rows exceeds the specified maximum number of skipped rows,
                OSS will report an error and stop processing.
            max_skipped_records_allowed (int, Optional): Specify the maximum number of skipped rows that can be tolerated.
                When a row of data is skipped due to a mismatch with the expected type in SQL,
                or when one or more columns of data are missing and SkipPartialData Record is True,
                the row of data will be skipped. If the number of skipped rows exceeds the value of this parameter,
                OSS will stop processing and report an error.
        """
        super().__init__(**kwargs)
        self.skip_partial_data_record = skip_partial_data_record
        self.max_skipped_records_allowed = max_skipped_records_allowed

    _attribute_map = {
        "skip_partial_data_record": {"tag": "xml", "rename": "SkipPartialDataRecord", "type": "bool"},
        "max_skipped_records_allowed": {"tag": "xml", "rename": "MaxSkippedRecordsAllowed"},
    }

    _xml_map = {
        "name": "Options"
    }


class SelectRequest(serde.Model):
    """The request for the Select operation."""

    def __init__(
        self,
        expression: Optional[str] = None,
        input_serialization: Optional[InputSerialization] = None,
        output_serialization: Optional[OutputSerialization] = None,
        options: Optional[SelectOptions] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            expression (str, Optional): SQL statements encoded in Base64.
            input_serialization (InputSerialization, Optional): Input serialization parameters.
            output_serialization (OutputSerialization, Optional): Output serialization parameters.
            options (SelectOptions, optional): Additional optional parameters.
        """
        super().__init__(**kwargs)
        self.expression = expression
        self.input_serialization = input_serialization
        self.output_serialization = output_serialization
        self.options = options

    _attribute_map = {
        "expression": {"tag": "xml", "rename": "Expression"},
        "input_serialization": {"tag": "xml", "rename": "InputSerialization", "type": "InputSerialization"},
        "output_serialization": {"tag": "xml", "rename": "OutputSerialization", "type": "OutputSerialization"},
        "options": {"tag": "xml", "rename": "Options", "type": "SelectOptions"},
    }

    _xml_map = {
        "name": "SelectRequest"
    }

class SelectObjectRequest(serde.RequestModel):
    """The request for the SelectObject operation."""

    _attribute_map = {
        "bucket": {"tag": "input", "position": "host", "required": True},
        "key": {"tag": "input", "position": "path", "required": True},
        "select_request": {"tag": "input", "position": "body", "rename": "SelectRequest", "type": "xml", "required": True},
        "progress_callback": {},
        "request_payer": {"tag": "input", "position": "header", "rename": "x-oss-request-payer"},
    }

    def __init__(
        self,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        select_request: Optional[SelectRequest] = None,
        progress_callback: Optional[Any]= None,
        request_payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The name of the object.
            select_request (SelectRequest, required): Save the container for the Select request.
            request_payer (str, optional): To indicate that the requester is aware that the request and data download will incur costs.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.select_request = select_request
        self.progress_callback = progress_callback
        self.request_payer = request_payer


class SelectObjectResult(serde.ResultModel):
    """The result for the SelectObject operation."""

    def __init__(
        self,
        body: Optional[SelectResult] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            body (Any, optional): Object data.
        """
        super().__init__(**kwargs)
        self.body = body

    _attribute_map = {
        "body": {},
    }
