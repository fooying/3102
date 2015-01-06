#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re

from core.data import result
from core.data import api

class LiveTest(object):

    def __init__(self):
        self.exit_flag = False
        self.req = api.request

    def __test_targets(self):
        title_regex = re.compile("<title>(.*?)<\/title>", re.DOTALL|re.M)
        for key in ['root_domain', 'ip', 'domain']:
            for item in result[key]:
                req = self.req.request('GET', 'http://' + result[key][item]['domain'], timeout=10)
                result[key][item]['status_code'] = req.status_code
                # 标题过长情况要不要考虑一下
                if req.status_code == 200:
                    title_match = title_regex.search(req.content)
                    result[key][item]['title'] = title_match.group(1) if title_match else 'failed'
                if self.exit_flag:
                    return


    def __init_targets(self):
        for key in ['root_domain', 'ip', 'domain']:
            for item in result[key]:
                result[key][item]['status_code'] = 'unkonwn'
                result[key][item]['title'] = 'unkonwn'

    def exit(self):
        self.exit_flag = True

    def start(self):
        self.__init_targets()
        self.__test_targets()
