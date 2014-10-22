#!/usr/bin/env python
# coding=utf-8
# Fooying@2014-10-13 14:29:01

"""
封装的ICP模块
"""

import re

from comm.request import request
from config import ICP_API_CONFIG


class ICP(object):
    def __init__(self, api_name="icpchaxun"):
        self.api_name = api_name if api_name in ICP_API_CONFIG else "icpchaxun"
        self.config = ICP_API_CONFIG[api_name]

    def query_zt_by_domain(self, domain):

    def query_domains_by_zt(self, zt_name):




