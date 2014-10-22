#!/usr/bin/env python
# coding=utf-8
# Fooying@2014-10-20 10:48:21

"""
封装请求模块
"""

import requests
from config import PROXY


def request(url, method="GET", proxy=False, **kwargs):
    proxies = PROXY if proxy else {}
    req = requests.request(method, url, proxies=proxies, **kwargs)
    return req.text
