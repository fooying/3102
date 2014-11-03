#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import requests
from conf.config import PROXY


def request(url, method='GET', proxy=False, **kwargs):
    proxies = PROXY if proxy else {}
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/37.0.2062.124 Safari/537.36')
    }
    if 'headers' not in kwargs:
        kwargs['headers'] = headers
    req = requests.request(method, url, proxies=proxies, **kwargs)
    return req.text
