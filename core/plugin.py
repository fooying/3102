#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import time
import logging

from thirdparty.gevent.monkey import patch_all

from core.data import kb
from core.data import api
from core.data import conf

patch_all()


class Plugin(object):

    def __init__(self, name):
        self.plugin_path = os.path.join(conf.settings.PLUGINS_PATH, name)
        self.logger = logging.getLogger('3102')
        self.req = api.request
        self.conf = conf.plugins_load[name]
        self.name = name
        self.result = None

    def start(self, domain, domain_type, level):
        self.domain = domain
        self.level = level
        key = '%s_%s' % (self.name, domain)
        kb.progress[key]['status'] = 'runing'
        kb.progress[key]['start_time'] = time.time()

    def end(self):
        key = '%s_%s' % (self.name, self.domain)
        kb.progress[key]['status'] = 'done'
        kb.progress[key]['end_time'] = time.time()
        update_dict = {
            'module': self.name,
            'parent_domain': self.domain,
            'level': self.level,
        }
        if type(self.result) == dict:
            self.result = {'result': self.result}
            self.result.update(update_dict)

    def get_plugin_name(self, chinese=False):
        """
        返回插件名称
        """
        return self.name if not chinese else self.chinesename

    def get_doc(self):
        """
        返回插件描述
        """
        if self.conf['descript']:
            res = self.descript
        elif self.__doc__ is not None:
            tmp = self.__doc__
            res = ''.join(l for l in tmp.split('\n') if l != '')
        else:
            res = 'No description available for this plugin.'
        return res

    def get_name(self):
        return self.__class__.__name__
