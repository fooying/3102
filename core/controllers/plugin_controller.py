#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import yaml
import gevent
import logging

from gevent.monkey import patch_all

from core.data import kb
from core.data import conf
from comm.coroutine import WorkerPool

patch_all()
logger = logging.getLogger('3102')


class PluginController(object):
    def __init__(self):
        self.exit_flag = False
        self.wp = WorkerPool()
        self.plugin_path = conf.settings.PLUGINS_PATH

    @classmethod
    def get_available_plugins(cls):
        """
        返回plugins目录下所有enable为true的plugin名称
        """
        from conf.settings import PLUGINS_PATH
        plugin_list = os.listdir(PLUGINS_PATH)
        for plugin in plugin_list:
            plugin_config_path = os.path.join(
                PLUGINS_PATH, plugin, 'config.yaml'
            )
            if os.path.exists(plugin_config_path):
                with open(plugin_config_path) as f:
                    try:
                        plugin_config = yaml.load(f)
                    except Exception:
                        logger.exception('load %s\'s config fail!' % plugin)
                    else:
                        if plugin_config['enable']:
                            # 在conf中载入plugin的配置信息
                            conf.plugins_available[plugin] = plugin_config
        return conf.plugins_available

    def plugin_init(self, plugins_sepcific=None):
        """
        初始化插件
        """
        plugins_available = conf.plugins_available.keys()
        if plugins_sepcific:
            for plugin in plugins_sepcific:
                if plugin in plugins_available:
                    self.__load_plugin(plugin)
                else:
                    logger.exception('plugin: %s NOT found!' % plugin)
        else:
            for plugin in plugins_available:
                self.__load_plugin(plugin)

    def __load_plugin(self, plugin):
        """
        载入名为plugin的插件. plugin的存在性和config的enable合法性由调用者保证
        """
        # 指向在conf.plugins_availavle中的信息, 不再重新读入配置文件
        conf.plugins_load[plugin] = conf.plugins_available[plugin]
        self.__register_plugin(plugin)

    def __register_plugin(self, plugin):
        """
        注册插件
        """
        kb.plugins[plugin] = {}
        kb.plugins[plugin]['name'] = plugin
        try:
            _import_path = '.'.join(
                conf.settings.PLUGINS_OPPOSITE_PATH.split(os.path.sep)
            )
            plugin_path = '%s.%s.work' % (_import_path, plugin)
            _plugin = __import__(plugin_path, fromlist='*')  # 动态加载函数
            kb.plugins[plugin]['handle'] = _plugin
        except Exception:
            logger.exception('register plugin %s failed!' % plugin)
        else:
            self.__classify_plugin(plugin)

    def __classify_plugin(self, plugin):
        """
        归类插件
        """
        inputs = conf.plugins_load[plugin]['input']
        for inp in inputs:
            if inp in conf.settings.ALLOW_INPUTS:
                conf.reg_plugins[inp].add(plugin)

    def start(self):
        while not self.exit_flag:
            try:
                target = self.wp.target_queue.get(timeout=1)
            except gevent.queue.Empty:
                pass
            else:
                self.__add_job_by_type(target)

    def __add_job_by_type(self, target):
        domain_type = target.get('domain_type')
        parent_module = target.pop('parent_module')
        onerepeat = conf.plugins_load.get(parent_module, {}).get('onerepeat')
        domain = target.get('domain')

        if domain_type in conf.settings.ALLOW_INPUTS:
            for plugin in conf.reg_plugins[domain_type]:
                if onerepeat and parent_module == plugin:
                    continue
                _plugin = getattr(kb.plugins[plugin]['handle'], plugin)()
                self.wp.add_job(getattr(_plugin, 'start'), **target)
                self.__init_plugin_progress(plugin, domain)

    def __init_plugin_progress(self, plugin, domain):
        key = '%s_%s' % (plugin, domain)
        kb.progress[key] = {'status':'wait', 'start_time':0, 'end_time':0}

    def run_job(self):
        self.wp.run()

    def exit(self):
        self.exit_flag = True
