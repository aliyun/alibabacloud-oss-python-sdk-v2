# -*- coding: utf-8 -*-
import re
import socket

from . import defaults

SCHEME_REGEXP = re.compile(r"^([^:]+)://")

def add_scheme(endpoint:str, disable_ssl:bool) -> str:
    """Add scheme to endpoint if not exist"""
    if endpoint != "" and not SCHEME_REGEXP.match(endpoint):
        scheme = defaults.DEFAULT_ENDPOINT_SCHEME
        if disable_ssl:
            scheme = 'http'
        endpoint = f'{scheme}://{endpoint}'
    return endpoint


def from_region(region:str, disable_ssl:bool, etype:str) -> str:
    """builds endpoint from region, ssl and endpoint type"""
    scheme = defaults.DEFAULT_ENDPOINT_SCHEME
    if disable_ssl:
        scheme = 'http'

    if etype == 'internal':
        endpoint = f'oss-{region}-internal.aliyuncs.com'
    elif etype == "dualstack":
        endpoint = f'{region}.oss.aliyuncs.com'
    elif etype == 'accelerate':
        endpoint = 'oss-accelerate.aliyuncs.com'
    elif etype == 'overseas':
        endpoint = 'oss-accelerate-overseas.aliyuncs.com'
    else:
        endpoint = f'oss-{region}.aliyuncs.com'

    endpoint = f'{scheme}://{endpoint}'

    return endpoint

def is_ip(hostname:str):
    """Check whether the host name is an IP address."""
    is_ipv6 = False
    right_bracket_index = hostname.find(']')
    if hostname[0] == '[' and right_bracket_index > 0:
        loc = hostname[1:right_bracket_index]
        is_ipv6 = True
    else:
        loc = hostname.split(':')[0]

    try:
        if is_ipv6:
            socket.inet_pton(socket.AF_INET6, loc)  # IPv6
        else:
            socket.inet_aton(loc)  # Only IPv4
    except socket.error:
        return False

    return True
