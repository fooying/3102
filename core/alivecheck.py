#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re
from gevent.monkey import patch_all

from comm.coroutine import WorkerPool
from core.data import result
from core.data import api


class AliveCheck(object):

    def __init__(self):
        self.exit_flag = False
        self.req = api.request

    def __check_targets(self):
        self.wp = WorkerPool()
        title_regex = re.compile("<title>(.*?)<\/title>", re.DOTALL|re.M)
        for key in ['root_domain', 'ip', 'domain']:
            for item in result[key]:
                self.wp.add_job(self.__load_targets, result[key][item], title_regex)
        self.wp.run()

    def __load_targets(self, target, title_regex):
        try:
            req = self.req.request('GET', 'http://' + target['domain'], timeout=5)
        except Exception, e:
            pass
        else:
            target['status_code'] = req.status_code
            # 标题过长情况要不要考虑一下
            if req.status_code == 200:
                content = req.content
                encoding = req.apparent_encoding if req.encoding == 'ISO-8859-1' else req.encoding
                title_match = title_regex.search(content)
                target['title'] = title_match.group(1).decode(encoding, 'replace').encode('utf-8','replace') if title_match else 'failed'

    def __init_targets(self):
        for key in ['root_domain', 'ip', 'domain']:
            for item in result[key]:
                result[key][item]['status_code'] = 'unkonwn'
                result[key][item]['title'] = 'unkonwn'

    def exit(self):
        self.exit_flag = True

    def start(self):
        self.__init_targets()
        self.__check_targets()
