#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import re
import sys
import logging

from comm.rootdomain import Domain


def is_ip(ip_str):
    ip_regx = """
            ^
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            $
        """
    result = True if re.search(ip_regx, ip_str, re.X) else False
    return result


def is_intra_ip(ip_str):
    ip_regx = """
        ^
        (?:
            (?: #10.0.0.0  A
            (?:10)
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            )
            |
            (?: #172.16.0.0 -- 172.31.0.0 B
            (?:172)
            \.
            (?:1[6-9]|2[0-9]|3[0-1])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            )
            |
            (?: #192.168.0.0 C
            (?:192)
            \.
            (?:168)
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            )
            |
            127\.0\.0\.1
        )
        $
        """
    result = True if re.search(ip_regx, ip_str, re.X) else False
    return result


def is_url(url_str):
    url_regx = """
            ^
           (?:http(?:s)?://)? #protocol
           (?:[\w]+(?::[\w]+)?@)? #user@password
           ([-\w]+\.)+[\w-]+(?:.)? #domain
           (?::\d{2,5})? #port
           (/?[-:\w;\./?%&=#]*)? #params
            $
        """
    result = True if re.search(url_regx, url_str, re.X) else False
    return result


def get_domain_type(domain):
    if is_ip(domain):
        return 'ip'
    elif is_url(domain):
        domain = Domain.url_format(domain)
        root_domain = Domain.get_root_domain(domain)
        if root_domain == domain:
            return 'root_domain'
        else:
            return 'domain'
    else:
        return False


def get_log_level(level_num):
    log_level = {
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARNING,
        4: logging.ERROR,
    }
    return log_level.get(level_num)


def get_proxy_list_by_file(file_path):
    if file_path and os.path.exists(file_path):
        with open(file_path) as f:
            proxys = f.read().splitlines()
        proxy_list = []
        for proxy in proxys:
            proxy = proxy.split(',')
            proxy_list.append({proxy[0]: proxy[1]})
    else:
        proxy_list = []
    return proxy_list

# utils copy from sqlmap ;)
def weAreFrozen():
    """
    Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.
    Reference: http://www.py2exe.org/index.cgi/WhereAmI
    """

    return hasattr(sys, "frozen")

def isListLike(value):
    """
    Returns True if the given value is a list-like instance

    >>> isListLike([1, 2, 3])
    True
    >>> isListLike(u'2')
    False
    """

    return isinstance(value, (list, tuple, set))

def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return NULL

    if isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or kb.get("pageEncoding") or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except:
                    value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances


