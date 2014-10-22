#!/usr/bin/env python
# coding=utf-8
# Fooying@2014-10-20 10:48:21

"""
封装请求模块
"""

import requests
import config


def request(url, method="GET", proxy=False, **kwargs):
    proxies = config.PROXY if proxy else {}
    req = requests.request(url, method, proxies=proxies, **kwargs)
    return req.text
