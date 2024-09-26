"""validation for sdk"""
import re


def is_valid_region(region: str):
    """Checks if the region is valid"""
    if region is None:
        return False

    pattern = r'^[a-z0-9-]+$'
    if re.match(pattern, region):
        return True

    return False


def is_valid_endpoint(endpoint: str):
    """Checks if the endpoint is valid"""
    if endpoint is None:
        return False

    pattern = r'^([a-zA-Z]+://)?[\w.-]+(:\d+)?$'
    if re.match(pattern, endpoint):
        return True

    return False


_ALPHA_NUM = 'abcdefghijklmnopqrstuvwxyz0123456789'
_HYPHEN = '-'
_BUCKET_NAME_CHARS = set(_ALPHA_NUM + _HYPHEN)


def is_valid_bucket_name(name: str) -> bool:
    """Checks if the name is valid"""
    if len(name) < 3 or len(name) > 63:
        return False

    if name[-1] == _HYPHEN:
        return False

    if name[0] == _HYPHEN:
        return False

    return set(name) <= _BUCKET_NAME_CHARS


def is_valid_object_name(name: str) -> bool:
    """Checks if the name is valid"""
    if len(name) < 1 or len(name) > 1024:
        return False

    return True


def is_valid_range(value: str) -> bool:
    """Checks if the range is valid"""
    return value.startswith('bytes=')
