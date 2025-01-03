from .. import serde
from typing import Optional, Any, Union
from ..types import StreamBody
class JSONInput(serde.Model):
    """
    The container that stores the SelectObject request.
    """

    _attribute_map = {
        'parse_json_number_as_string': {'tag': 'xml', 'rename': 'ParseJsonNumberAsString', 'type': 'bool'},
        'type': {'tag': 'xml', 'rename': 'Type', 'type': 'str'},
        'range': {'tag': 'xml', 'rename': 'Range', 'type': 'str'},
    }

    _xml_map = {
        'name': 'JSON'
    }

    def __init__(
        self,
        parse_json_number_as_string: Optional[bool] = None,
        type: Optional[str] = None,
        range: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            parse_json_number_as_string (bool, optional): Specifies whether to parse integer and floating-point numbers in the JSON object into strings. The precision of floating-point numbers in a JSON object decreases when the numbers are parsed. If you want to retain the raw data, we recommend that you set this parameter to true. To use the parsed numbers in calculations, you can use the CAST function in SQL to convert the parsed data into the required type such as INT, DOUBLE, or DECIMAL.Default value: false.Valid values:*   true            *   false            
            type (str, optional): The type of JSON input.Valid values:*   LINES            *   DOCUMENT            
            range (str, optional): The query range. This parameter is optional. The following formats are supported:  SelectMeta must be created for objects that are queried based on Range. For more information about SelectMeta, see [CreateSelectObjectMeta](~~74054~~).*   Query by row: line-range=start-end. For example, line-range=10-20 indicates that data from row 10 to row 20 is scanned.*   Query by split: split-range=start-end. For example, split-range=10-20 indicates that data from split 10 to split 20 is scanned.The start and end of the range are both inclusive. The start and end of the range use the same format as that of the range parameter in range get.This parameter can be used only if the object is in the CSV format or if the JSON type is LINES.
        """
        super().__init__(**kwargs)
        self.parse_json_number_as_string = parse_json_number_as_string
        self.type = type
        self.range = range


class CSVOutput(serde.Model):
    """
    The container that stores the SelectObject request.
    """

    _attribute_map = {
        'record_delimiter': {'tag': 'xml', 'rename': 'RecordDelimiter', 'type': 'str'},
        'field_delimiter': {'tag': 'xml', 'rename': 'FieldDelimiter', 'type': 'str'},
        "quote_character": {"tag": "xml", "rename": "QuoteCharacter", 'type': 'str'},
    }

    _xml_map = {
        'name': 'CSV'
    }

    def __init__(
        self,
        record_delimiter: Optional[str] = None,
        field_delimiter: Optional[str] = None,
        quote_character: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            record_delimiter (str, optional): A Base64-encoded line feed. The value of this parameter is up to two ANSI characters in length before encoding. For example, `` is used to represent a line feed in Java.Default value: ``
            field_delimiter (str, optional): The delimiter that you want to use to separate values in the CSV object. The value of this parameter must be Base64-encoded. The value of this parameter is an ANSI character before encoding. For example, a comma (`,`) is used to indicate a comma in Java.Default value: `,`
            quote_character (str, Optional): Specify the quotation mark characters for CSV in Base64 encoding.
                The default value is \ "(optional). Line breaks and column separators within quotation marks in CSV will be treated as regular characters.
                The value before encoding must be one character, represented by the ANSI value of the character,
                for example, using '\' to indicate quotation marks in Java.            
        """
        super().__init__(**kwargs)
        self.record_delimiter = record_delimiter
        self.field_delimiter = field_delimiter
        self.quote_character = quote_character

class JSONOutput(serde.Model):
    """
    The container that stores the SelectObject request.
    """

    _attribute_map = {
        'record_delimiter': {'tag': 'xml', 'rename': 'RecordDelimiter', 'type': 'str'},
    }

    _xml_map = {
        'name': 'JSON'
    }

    def __init__(
        self,
        record_delimiter: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            record_delimiter (str, optional): Optional. A Base64-encoded line feed. The value of this parameter is up to two ANSI characters in length before encoding. For example, `` is used to represent a line feed in Java.Default value: ``
        """
        super().__init__(**kwargs)
        self.record_delimiter = record_delimiter

class CSVInput(serde.Model):
    """
    The container that stores the SelectObject request.
    """

    _attribute_map = {
        'record_delimiter': {'tag': 'xml', 'rename': 'RecordDelimiter', 'type': 'str'},
        'field_delimiter': {'tag': 'xml', 'rename': 'FieldDelimiter', 'type': 'str'},
        'quote_character': {'tag': 'xml', 'rename': 'QuoteCharacter', 'type': 'str'},
        'comment_character': {'tag': 'xml', 'rename': 'CommentCharacter', 'type': 'str'},
        'range': {'tag': 'xml', 'rename': 'Range', 'type': 'str'},
        'allow_quoted_record_delimiter': {'tag': 'xml', 'rename': 'AllowQuotedRecordDelimiter', 'type': 'bool'},
        'file_header_info': {'tag': 'xml', 'rename': 'FileHeaderInfo', 'type': 'str'},
    }

    _xml_map = {
        'name': 'CSV'
    }

    def __init__(
        self,
        record_delimiter: Optional[str] = None,
        field_delimiter: Optional[str] = None,
        quote_character: Optional[str] = None,
        comment_character: Optional[str] = None,
        range: Optional[str] = None,
        allow_quoted_record_delimiter: Optional[bool] = None,
        file_header_info: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            record_delimiter (str, optional): Optional. A Base64-encoded line feed. Default value: The value of this parameter is up to two ANSI characters in length before encoding. For example,  is used to represent a line feed in Java.
            field_delimiter (str, optional): Optional. The delimiter that you want to use to separate values in the CSV object. The value of this parameter must be Base64-encoded. Default value: `,`. Before the value of this parameter is encoded, the value must be an ANSI character. For example, `,` is used to indicate a comma in Java.
            quote_character (str, optional): Optional. A Base64-encoded quote character that you want to use in the CSV object. Default value: `\"`. In a CSV object, line feeds and column delimiters enclosed in quotation marks are processed as normal characters. Before the value of this parameter is encoded, the value must be an ANSI character. For example, `\"` is used to indicate a quote character in Java.
            comment_character (str, optional): The comment character that you want to use in the CSV object. The value of this parameter must be Base64-encoded. This parameter is empty by default.
            range (str, optional): Optional. The query range. The following formats are supported:  SelectMeta must be created for objects that are queried based on Range. For more information about SelectMeta, see [CreateSelectObjectMeta](~~74054~~).*   Query by row: line-range=start-end. For example, line-range=10-20 indicates that data from row 10 to row 20 is scanned.*   Query by split: split-range=start-end. For example, split-range=10-20 indicates that data from split 10 to split 20 is scanned.The start and end of the range are both inclusive. The start and end of the range use the same format as that of the range parameter in range get.This parameter can be used only if the object is in the CSV format or if the JSON type is LINES.
            allow_quoted_record_delimiter (bool, optional): Specifies whether the CSV object can contain line feeds in quotation marks (").For example, if the value of a column is `"abcdef"` and `` is a line feed, set this parameter to true. If this parameter is set to false, you can call the SelectObject operation to specify a range in the request header to perform more efficient multipart queries.
            file_header_info (str, optional): The header information of the CSV object. Valid values:*   Use: The CSV object contains header information. You can use the column names in the CSV object as the column names in the SelectObject operation.*   Ignore: The CSV object contains header information. The column names in the CSV object cannot be used as the column names in the SelectObject operation.*   None: The CSV object does not contain header information. This is the default value.
        """
        super().__init__(**kwargs)
        self.record_delimiter = record_delimiter
        self.field_delimiter = field_delimiter
        self.quote_character = quote_character
        self.comment_character = comment_character
        self.range = range
        self.allow_quoted_record_delimiter = allow_quoted_record_delimiter
        self.file_header_info = file_header_info


class SelectRequestOptions(serde.Model):
    """
    The container that stores the SelectObject request.
    """

    _attribute_map = {
        'skip_partial_data_record': {'tag': 'xml', 'rename': 'SkipPartialDataRecord', 'type': 'bool'},
        'max_skipped_records_allowed': {'tag': 'xml', 'rename': 'MaxSkippedRecordsAllowed', 'type': 'int'},
    }

    _xml_map = {
        'name': 'SelectRequestOptions'
    }

    def __init__(
        self,
        skip_partial_data_record: Optional[bool] = None,
        max_skipped_records_allowed: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            skip_partial_data_record (bool, optional): Specifies whether to ignore rows in which data is missing.*   If this parameter is set to false, OSS processes the row data as null without reporting errors.*   If this parameter is set to true, rows that do not contain data are skipped. If the number of skipped rows has exceeded the maximum number of rows that can be skipped, OSS reports an error and stops processing the data.
            max_skipped_records_allowed (int, optional): The maximum number of rows that can be skipped. If a row does not match the type specified in the SQL statement, or if one or more columns in a row are missing and the value of SkipPartialDataRecord is True, the rows are skipped. If the number of skipped rows has exceeded the value of this parameter, OSS reports an error and stops processing the data.The default value is 0.  A problematic row can affect CSV file parsing. If a row is not a valid CSV row, for example, if the row contains an odd number of consecutive quotes, OSS stops processing and returns an error to prevent CSV parsing errors. This parameter can be used to adjust the tolerance for irregular data but cannot be applied to invalid CSV objects.
        """
        super().__init__(**kwargs)
        self.skip_partial_data_record = skip_partial_data_record
        self.max_skipped_records_allowed = max_skipped_records_allowed


class InputSerialization(serde.Model):
    """
    The container that stores the SelectObject request.
    """

    _attribute_map = {
        'compression_type': {'tag': 'xml', 'rename': 'CompressionType', 'type': 'str'},
        'csv': {'tag': 'xml', 'rename': 'CSV', 'type': 'CSVInput'},
        'json': {'tag': 'xml', 'rename': 'JSON', 'type': 'JSONInput'},
    }

    _xml_map = {
        'name': 'InputSerialization'
    }

    _dependency_map = {
        'CSVInput': {'new': lambda: CSVInput()},
        'JSONInput': {'new': lambda: JSONInput()},
    }

    def __init__(
        self,
        compression_type: Optional[str] = None,
        csv: Optional[CSVInput] = None,
        json: Optional[JSONInput] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            compression_type (str, optional): The compression type of the object. This parameter is optional. Valid value: None.
            csv (CSVInput, optional): The format of the input CSV object.
            json (JSONInput, optional): The format of the input JSON object.
        """
        super().__init__(**kwargs)
        self.compression_type = compression_type
        self.csv = csv
        self.json = json


class OutputSerialization(serde.Model):
    """
    The container that stores the SelectObject request.
    """

    _attribute_map = {
        'keep_all_columns': {'tag': 'xml', 'rename': 'KeepAllColumns', 'type': 'bool'},
        'output_header': {'tag': 'xml', 'rename': 'OutputHeader', 'type': 'bool'},
        'output_raw_data': {'tag': 'xml', 'rename': 'OutputRawData', 'type': 'bool'},
        'enable_payload_crc': {'tag': 'xml', 'rename': 'EnablePayloadCrc', 'type': 'bool'},
        'csv': {'tag': 'xml', 'rename': 'CSV', 'type': 'CSVOutput'},
        'json': {'tag': 'xml', 'rename': 'JSON', 'type': 'JSONOutput'},
    }

    _xml_map = {
        'name': 'OutputSerialization'
    }

    _dependency_map = {
        'CSVOutput': {'new': lambda: CSVOutput()},
        'JSONOutput': {'new': lambda: JSONOutput()},
    }

    def __init__(
        self,
        keep_all_columns: Optional[bool] = None,
        output_header: Optional[bool] = None,
        output_raw_data: Optional[bool] = None,
        enable_payload_crc: Optional[bool] = None,
        csv: Optional[CSVOutput] = None,
        json: Optional[JSONOutput] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            keep_all_columns (bool, optional): Optional. Specifies whether all columns in the CSV object are included in the returned result.Default value: false.This parameter has a value only for columns included in the SELECT statement. The columns in the response are sorted in ascending order of the column numbers. Example:`select _5, _1 from ossobject.`If you set KeepAllColumns to true and six columns are included in the CSV object, the following result is returned for the preceding SELECT statement:`Value of 1st column,,,,Value of 5th column,`
            output_header (bool, optional): Specifies whether the header information about the CSV object is included in the beginning of the response.Default value: false.Valid values:*   true            *   false            
            output_raw_data (bool, optional): Specifies whether to export raw data.*   If you specify OutputRawData in the request, Object Storage Service (OSS) returns data based on the request element.*   If you do not specify OutputRawData in the request, OSS automatically selects a format and returns data in the selected format in the response.*   If you set OutputRawData to true and it takes a long time for the sent SQL statement to return data, the HTTP request may time out.Valid values:*   true            *   false            
            enable_payload_crc (bool, optional): The CRC-32 value for verification of each frame. The client can calculate the CRC-32 value of each payload and compare it with the included CRC-32 value to verify data integrity.Valid values:*   true            *   false            
            csv (CSVOutput, optional): The output parameters when the CSV object is queried.
            json (JSONOutput, optional): The output parameters when the JSON object is queried.
        """
        super().__init__(**kwargs)
        self.keep_all_columns = keep_all_columns
        self.output_header = output_header
        self.output_raw_data = output_raw_data
        self.enable_payload_crc = enable_payload_crc
        self.csv = csv
        self.json = json


class SelectRequest(serde.Model):
    """
    The container that stores the SelectObject request.
    """

    _attribute_map = {
        'options': {'tag': 'xml', 'rename': 'Options', 'type': 'SelectRequestOptions'},
        'expression': {'tag': 'xml', 'rename': 'Expression', 'type': 'str'},
        'input_serialization': {'tag': 'xml', 'rename': 'InputSerialization', 'type': 'InputSerialization'},
        'output_serialization': {'tag': 'xml', 'rename': 'OutputSerialization', 'type': 'OutputSerialization'},
    }

    _xml_map = {
        'name': 'SelectRequest'
    }

    _dependency_map = {
        'SelectRequestOptions': {'new': lambda: SelectRequestOptions()},
        'InputSerialization': {'new': lambda: InputSerialization()},
        'OutputSerialization': {'new': lambda: OutputSerialization()},
    }

    def __init__(
        self,
        options: Optional[SelectRequestOptions] = None,
        expression: Optional[str] = None,
        input_serialization: Optional[InputSerialization] = None,
        output_serialization: Optional[OutputSerialization] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            options (SelectRequestOptions, optional): Other optional parameters.
            expression (str, optional): The Base64-encoded SQL statement.
            input_serialization (InputSerialization, optional): The input serialization parameters.
            output_serialization (OutputSerialization, optional): The output serialization parameters.
        """
        super().__init__(**kwargs)
        self.options = options
        self.expression = expression
        self.input_serialization = input_serialization
        self.output_serialization = output_serialization

class SelectObjectRequest(serde.RequestModel):
    """
    The request for the SelectObject operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'key': {'tag': 'input', 'position': 'path', 'rename': 'key', 'type': 'str', 'required': True},
        'process': {'tag': 'input', 'position': 'query', 'rename': 'x-oss-process', 'type': 'str', 'required': True},
        'select_request': {'tag': 'input', 'position': 'body', 'rename': 'SelectRequest', 'type': 'xml', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        process: str = None,
        select_request: Optional[SelectRequest] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            key (str, required): The full path of the object.
            process (str, optional): If it is a CSV file, this value should be set to csv/select; if it is a JSON file, it should be set to json/select.
            select_request (SelectRequest, optional): The container that stores the SelectObject request.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.process = process
        self.select_request = select_request


class SelectObjectResult(serde.ResultModel):
    """
    The request for the SelectObject operation.
    """

    _attribute_map = {
        "body": {},
    }

    def __init__(
        self,
        body: Optional[StreamBody] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            body (StreamBody, optional): <no value>
        """
        super().__init__(**kwargs)
        self.body = body


class CSVMetaRequest(serde.Model):
    """
    The container that stores CsvMetaRequest information.
    """

    _attribute_map = {
        'input_serialization': {'tag': 'xml', 'rename': 'InputSerialization', 'type': 'InputSerialization'},
        'overwrite_if_exists': {'tag': 'xml', 'rename': 'OverwriteIfExists', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'CsvMetaRequest'
    }

    _dependency_map = {
        'InputSerialization': {'new': lambda: InputSerialization()},
    }

    def __init__(
        self,
        input_serialization: Optional[InputSerialization] = None,
        overwrite_if_exists: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            input_serialization (InputSerialization, optional): Specifies input serialization. This parameter is optional.
            overwrite_if_exists (bool, optional): Specifies whether to perform the operation again and overwrite the existing data.Default value: false. This indicates that the result is directly returned if the existing data returned from a previous CreateSelectObjectMeta operation is available.Valid values:*   true            *   false
        """
        super().__init__(**kwargs)
        self.input_serialization = input_serialization
        self.overwrite_if_exists = overwrite_if_exists

class JSONMetaRequest(serde.Model):
    """
    The container that stores JsonMetaRequest information.
    """

    _attribute_map = {
        'input_serialization': {'tag': 'xml', 'rename': 'InputSerialization', 'type': 'InputSerialization'},
        'overwrite_if_exists': {'tag': 'xml', 'rename': 'OverwriteIfExists', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'JsonMetaRequest'
    }

    _dependency_map = {
        'InputSerialization': {'new': lambda: InputSerialization()},
    }

    def __init__(
        self,
        input_serialization: Optional[InputSerialization] = None,
        overwrite_if_exists: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            input_serialization (InputSerialization, optional): Specifies input serialization. This parameter is optional.
            overwrite_if_exists (bool, optional): Specifies whether to perform the operation again and overwrite the existing data.Default value: false. This indicates that the result is directly returned if the existing data returned from a previous CreateSelectObjectMeta operation is available.Valid values:*   true            *   false
        """
        super().__init__(**kwargs)
        self.input_serialization = input_serialization
        self.overwrite_if_exists = overwrite_if_exists

class CreateSelectObjectMetaRequest(serde.RequestModel):
    """
    The request for the CreateSelectObjectMeta operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'key': {'tag': 'input', 'position': 'path', 'rename': 'key', 'type': 'str', 'required': True},
        'process': {'tag': 'input', 'position': 'query', 'rename': 'x-oss-process', 'type': 'str', 'required': True},
        'select_meta_request': {'tag': 'input', 'position': 'body', 'rename': '', 'type': 'xml', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        key: str = None,
        process: str = None,
        select_meta_request: Optional[Union[CSVMetaRequest,JSONMetaRequest]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): Bucket name.
            key (str, required): The full path of the Object.
            process (str, optional): Parameters to specify the file formate.
            select_meta_request (CSVMetaRequest|JSONMetaRequest, optional): Container for the CreateSelectObjectMeta request.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.process = process
        self.select_meta_request = select_meta_request


class CreateSelectObjectMetaResult(serde.ResultModel):
    """
    The request for the CreateSelectObjectMeta operation.
    """

    _attribute_map = {
        'offset': {},
        'total_scanned_bytes': {},
        'splits_count': {},
        'rows_count': {},
        'cols_count': {},
    }

    def __init__(
        self,
        offset: int = None,
        total_scanned_bytes: int = None,
        splits_count: int = None,
        rows_count: int = None,
        cols_count: int = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            offset (int, optional): The offset when scanning is complete.
            total_scanned_bytes (int, optional): The size of the scanned data.
            splits_count (int, optional): The total number of splits.
            rows_count (int, optional): The total number of rows.
            cols_count (int, optional): The total number of columns.
        """
        super().__init__(**kwargs)
        self.offset = offset
        self.total_scanned_bytes = total_scanned_bytes
        self.splits_count = splits_count
        self.rows_count = rows_count
        self.cols_count = cols_count
