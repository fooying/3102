#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import requests
from config import PROXY


def request(url, method='GET', proxy=False, **kwargs):
    proxies = PROXY if proxy else {}
    req = requests.request(method, url, proxies=proxies, **kwargs)
    return req.text
