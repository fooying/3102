#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import sys
if 'threading' in sys.modules:
    del sys.modules['threading']
from gevent.monkey import patch_all
patch_all()

import os
import time
import signal
import threading

from comm.request import Req
from comm.log import init_logger
from comm.log import CUSTOM_LOGGING
from comm.rootdomain import Domain
from comm.utils import get_log_level
from comm.utils import get_domain_type
from comm.utils import get_proxy_list_by_file

from config import settings
from core.data import api
from core.data import paths
from core.data import conf
from core.data import result
from core.data import options
from core.output.output import Output
from core.controllers.plugin_controller import PluginController
from core.controllers.taskmanager import task_monitor
from core.alivecheck import AliveCheck



def complete():
    print '\n'
    api.logger.info('Output result to file...')
    Output(conf.domain, options.output_format, options.output_file).save()
    api.logger.log(CUSTOM_LOGGING.good, os.linesep.join([
        'Result count:',
        '    ip: %s' % len(result.ip),
        '    domain: %s' % len(result.domain),
        '    root domain: %s' % len(result.root_domain),
    ]))
    api.logger.info('Complete 3102 at %s' % time.strftime("%X"))


def on_signal(signum, frame):
    print
    api.logger.warning('User aborted, 3102 will exit, signal:%d' % signum)
    conf.plugin_controller.exit()


def start():
    conf.domain = options.target
    domain_type = get_domain_type(conf.domain)
    if domain_type in settings.ALLOW_INPUTS:
        conf.domain = Domain.url_format(conf.domain)

        # 初始化日志
        log_level = get_log_level(options.log_level)
        init_logger(log_file_path=options.log_file, log_level=log_level)
        api.logger.info('System init at %s' % time.strftime("%X"))
        # 初始化配置
        conf.settings = settings
        # 初始化爬虫
        proxy_list = get_proxy_list_by_file(options.proxy_file)
        api.request = Req(options.timeout, proxy_list, options.verify_proxy)

        conf.plugin_controller = PluginController()
        conf.plugin_controller.plugin_init(options.plugins_specific)
        api.logger.info('Loaded plugins: %s' % ', '.join(conf.plugins_load.keys()))

        # 绑定信号事件
        if hasattr(signal, 'SIGUSR1'):
            signal.signal(signal.SIGUSR1, on_signal)
        signal.signal(signal.SIGTERM, on_signal)
        signal.signal(signal.SIGINT, on_signal)

        api.logger.info('Start target [%s]' % conf.domain)
        # 首个目标
        first_target = {
            'result': {'root_domain': [], 'domain': [], 'ip': []},
            'module': '',
            'level': 0,
            'parent_domain': ''
        }
        first_target['result'][domain_type].append(conf.domain)
        conf.plugin_controller.wp.result.put(first_target)

        # 开启任务监控
        api.logger.info('Start task monitor and plugin...')
        kwargs = {'pc': conf.plugin_controller}
        monitor = threading.Thread(target=task_monitor, kwargs=kwargs)
        monitor.start()

        # 开启插件执行
        conf.plugin_controller.start()

        if options.alive_check:
            alivecheck = AliveCheck()
            print '\n'
            api.logger.info('Start alive check...')
            alivecheck.start()
            api.logger.info('Alive check completed')

        complete()
    else:
        api.logger.error(
            'Please input a target in the correct'
            ' format(domain/root_domain/ip)!'
        )
