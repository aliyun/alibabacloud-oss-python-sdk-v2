"""utils for sdk"""
import io
import platform
from typing import Optional, Any, MutableMapping, Tuple, Dict
import mimetypes
import os.path
from ._version import VERSION


_EXTRA_TYPES_MAP = {
    ".js": "application/javascript",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xltx": "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    ".potx": "application/vnd.openxmlformats-officedocument.presentationml.template",
    ".ppsx": "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".sldx": "application/vnd.openxmlformats-officedocument.presentationml.slide",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".dotx": "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
    ".xlam": "application/vnd.ms-excel.addin.macroEnabled.12",
    ".xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    ".apk": "application/vnd.android.package-archive"
}


def safety_str(value: Optional[str]) -> str:
    """
    Returns str value if the value is not None.
    Returns a emtpy str if the value is None.
    """
    return value if value is not None else ''


def safety_bool(value: Optional[bool]) -> bool:
    """
    Returns bool value if the value is not None.
    Returns False if the value is None.
    """
    return value if value is not None else False

def safety_int(value: Optional[int]) -> int:
    """
    Returns int value if the value is not None.
    Returns 0 if the value is None.
    """
    return value if value is not None else 0

def ensure_boolean(val):
    """
    Ensures a boolean value if a string or boolean is provided
    For strings, the value for True/False is case insensitive
    """
    if isinstance(val, bool):
        return val

    if isinstance(val, str):
        return val.lower() == 'true'

    return False


def merge_dicts(dict1, dict2, append_lists=False):
    """Given two dict, merge the second dict into the first.
    The dicts can have arbitrary nesting.

    Args:
        dict1 (Dict): the first dict.
        dict2 (Dict): the second dict.
        append_lists (bool, optional): If true, instead of clobbering a list with the new
        value, append all of the new values onto the original list.
    """

    for key in dict2:
        if isinstance(dict2[key], dict):
            if key in dict1 and key in dict2:
                merge_dicts(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        # If the value is a list and the ``append_lists`` flag is set,
        # append the new values onto the original list
        elif isinstance(dict2[key], list) and append_lists:
            # The value in dict1 must be a list in order to append new
            # values onto it.
            if key in dict1 and isinstance(dict1[key], list):
                dict1[key].extend(dict2[key])
            else:
                dict1[key] = dict2[key]
        else:
            # At scalar types, we iterate and merge the
            # current dict that we're on.
            dict1[key] = dict2[key]


def lowercase_dict(original):
    """Copies the given dictionary ensuring all keys are lowercase strings."""
    copy = {}
    for key in original:
        copy[key.lower()] = original[key]
    return copy

def guess_content_type(name:str, default:str) -> str:
    """Guess the type of a file based on its name"""
    ext = os.path.splitext(name)[1].lower()
    if ext in _EXTRA_TYPES_MAP:
        return _EXTRA_TYPES_MAP[ext]

    return mimetypes.guess_type(name)[0] or default

def guess_content_length(body: Any) -> Optional[int]:
    """Guess the content length of body"""
    if not body:
        return 0

    try:
        return len(body)
    except (AttributeError, TypeError):
        pass

    if hasattr(body, 'seek') and hasattr(body, 'tell'):
        try:
            orig_pos = body.tell()
            body.seek(0, os.SEEK_END)
            end_file_pos = body.tell()
            body.seek(orig_pos)
            return end_file_pos - orig_pos
        except io.UnsupportedOperation:
            pass
    return None

def escape_xml_value(s: str) -> str:
    """escapeXml EscapeString writes to p the properly escaped XML equivalent
    of the plain text data s
    """
    ss = ''
    for _, d in enumerate(s):
        if d == "&":
            ss += "&amp;"
        elif d == "<":
            ss += "&lt;"
        elif d == ">":
            ss += "&gt;"
        elif d == "\"":
            ss += "&quot;"
        elif d == "\r":
            ss += "&#13;"
        elif d == "\n":
            ss += "&#10;"
        elif d == "\t":
            ss += "&#09;"
        else:
            n = ord(d)
            if  0 <= n < 0x20:
                ss += f'&#{n:02d};'
            else:
                ss += d
    return ss

def parse_content_range(content_range: str) -> Tuple[int, int, int]:
    """
    Parses the content range header
    accepts bytes 22-33/42 and bytes 22-33/* format
    """
    if not content_range:
        raise ValueError("Invalid content-range header, it is none or empty.")

    if not content_range.startswith('bytes '):
        raise ValueError("Invalid content-range header, it dose not start with bytes.")

    vals = content_range.split(" ")[1].split("/")

    if len(vals) != 2:
        raise ValueError(f'Invalid content-range header: {content_range}')

    rvals = vals[0].split("-")

    if len(rvals) != 2:
        raise ValueError(f'Invalid content-range header: {content_range}')

    start = int(rvals[0])
    if start < 0:
        raise ValueError(f'Invalid content-range header: {start}')

    end = int(rvals[1])
    if end < 0:
        raise ValueError(f'Invalid content-range header: {end}')

    if vals[1] == "*":
        size = -1
    else:
        size = int(vals[1])
        if size <= 0:
            raise ValueError(f'Invalid content-range header: {size}')

    return start, end, size

def parse_content_length(headers: MutableMapping[str, str]) -> int:
    """Parses the length from the content length header"""
    if not headers.get("Content-Length", None):
        raise ValueError("Missing content-length header.")
    size = int(headers["Content-Length"])
    if size <= 0:
        raise ValueError(f"Invalid content-length header: {size}")
    return size

def parse_http_range(range_header: str) -> Tuple[int, int]:
    """
    Parses the range header
    It only accepts single ranges.
    """
    if not range_header:
        raise ValueError("Invalid range header, it is none or empty.")

    if not range_header.startswith("bytes="):
        raise ValueError("Invalid range header, doesn't start with bytes=.")

    if range_header.count(',') > 0:
        raise ValueError("Invalid range header, contains multiple ranges which isn't supported.")

    dash = range_header.find('-')
    if dash < 0:
        raise ValueError("Invalid range header, contains no '-'")

    start_str = range_header[6:dash].strip()
    end_str = range_header[dash+1:].strip()

    start = -1
    if len(start_str) > 0:
        start = int(start_str)
        if start < 0:
            raise ValueError(f'Invalid range header: {start_str} in {range_header}')

    end = -1
    if len(end_str) > 0:
        end = int(end_str)
        if end < 0:
            raise ValueError(f'Invalid range header: {end_str} in {range_header}')

    return start, end

def is_seekable(obj: Any) -> bool:
    """Tests if this object supports Seek method
    Returns True is suppurts seek, else False
    """
    if hasattr(obj, 'seekable'):
        return obj.seekable()

    if hasattr(obj, 'seek') and hasattr(obj, 'tell'):
        try:
            obj.seek(0, os.SEEK_CUR)
            return True
        except OSError:
            return False
    return False

def is_fileobj(obj: Any) -> bool:
    """Tests if this object has seek and tell method
    Returns True if it is a file object, else False 
    """
    if hasattr(obj, 'seek') and hasattr(obj, 'tell'):
        return True
    return False

def get_default_user_agent() -> str:
    """Returns the default user agent string
    """
    sysinfo = f'{platform.system()}/{platform.release()}/{platform.machine()};{platform.python_version()}'
    return f'alibabacloud-python-sdk-v2/{VERSION} ({sysinfo})'

def get_vector_user_agent() -> str:
    """Returns the default user agent string
    """
    return 'vector-client'
