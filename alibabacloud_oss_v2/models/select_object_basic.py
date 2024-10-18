"""Models for select object operation APIs"""
# pylint: disable=too-few-public-methods, too-many-instance-attributes, unnecessary-lambda
# pylint: disable=super-init-not-called, too-many-lines, line-too-long, too-many-arguments
# pylint: disable=too-many-locals
from typing import Optional, Any
from .. import serde, SelectResult

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
