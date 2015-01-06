#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.data import result
from core.data import api

class LiveTest(object):

    def __init__(self):
        self.exit_flag = False
        self.req = api.request

    def __test_targets(self):
        for key in ['root_domain', 'ip', 'domain']:
            for item in result[key]:
                req = self.req.request('GET', 'http://' + result[key][item]['domain'], timeout=10)
                result[key][item]['status_code'] = req.status_code
            if self.exit_flag:
                break

    def __init_targets(self):
        for key in ['root_domain', 'ip', 'domain']:
            for item in result[key]:
                result[key][item]['status_code'] = 'unkonwn'

    def exit(self):
        self.exit_flag = True

    def start(self):
        self.__init_targets()
        self.__test_targets()
