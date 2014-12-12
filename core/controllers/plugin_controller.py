#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import yaml
import logging

from core.data import kb
from core.data import conf

logger = logging.getLogger('3102')


class PluginController(object):
    def __init__(self):
        self.plugin_path = conf.settings.PLUGIN_PATH

    @classmethod
    def plugin_init(cls):
        """
        初始化插件
        """
        plugin_list = os.listdir(plugin_path)
        for plugin in plugin_list:
            plugin_config_path = os.path.join(
                plugin_path, plugin, 'config.yaml'
            )

            if os.path.exists(plugin_config_path):
                with open(plugin_config_path) as f:
                    try:
                        conf.plugins[plugin] = yaml.load(f)
                    except Exception:
                        logger.exception('load %s\'s config fail!' % plugin)
                    else:
                        if conf.plugins[plugin]['enable']:
                            cls().__register_plugin(plugin)
                            cls().__classify_plugin(plugin)
                        else:
                            conf.plugins.pop(plugin)

    def __register_plugin(self, plugin):
        """
        注册插件
        """
        registered_plugin = {}
        registered_plugin['name'] = plugin
        try:
            registered_plugin['handle'] = self.__load_plugin(plugin)
        except Exception:
            logger.exception('register plugin failed!')

`   def __classify_plugin(self, plugin):
        """
        归类插件
        """
        inputs = conf.plugins[plugin]['input']
        for inp in inputs:
            if inp in conf.settings.ALLOW_INPUT:
                kb.plugins[inp].add(plugin)


    def __load_plugin(self, plugin_name):
        """
        动态载入插件模块函数
        """
        _plugin = None
        plugin_path = 'plugins.%s.work' % plugin_name
        try:
            _plugin = __import__(plugin_path, fromlist='*')
        except Exception:
            logger.exception(
                'plugin[%s] __load_plugin failed!' % plugin_name
            )
        return _plugin

