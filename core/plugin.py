#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import logging

from core.data import conf, api
from gevent.monkey import patch_all

patch_all()


class Plugin(object):
    def __init__(self, name):
        self.plugin_path = os.path.join(conf.settings.PLUGINS_PATH, name)
        self.logger = logging.getLogger('3102')
        self.req = api.request
        self.conf = conf.plugins[name]

    def start(self):
        pass

    def end(self):
        pass

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
