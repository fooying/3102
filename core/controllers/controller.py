#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import time
import signal
import logging
import threading

from comm.request import Req
from comm.log import init_logger
from comm.log import CUSTOM_LOGGING
from comm.rootdomain import Domain
from comm.utils import get_log_level
from comm.utils import get_domain_type
from comm.utils import get_proxy_list_by_file

from conf import settings
from core.data import api
from core.data import conf
from core.data import result
from core.output.output import Output
from core.controllers.plugin_controller import PluginController
from core.controllers.taskmanager import task_monitor

logger = logging.getLogger('3102')
domain = output_file = output_format = None
plugin_controller = None


def complete():
    print '\n'
    logger.info('output result to file...')
    Output(domain, output_format, output_file).save()
    logger.log(CUSTOM_LOGGING.good, os.linesep.join(['result count:',
       '    ip: %s' % len(result.ip),
       '    domain: %s' % len(result.domain),
       '    root domain: %s' % len(result.root_domain),
    ]))
    logger.info('Complete 3102!')


def on_signal(signum, frame):
    logger.warning('3102 will exit,signal:%d' % signum)
    plugin_controller.exit()


def start(args):
    global output_file
    global output_format
    global domain
    global plugin_controller
    domain = args.target
    domain_type = get_domain_type(domain)
    if domain_type in settings.ALLOW_INPUTS:
        domain = Domain.url_format(domain)

        # 初始化日志
        log_level = get_log_level(args.log_level)
        init_logger(log_file_path=args.log_file, log_level=log_level)
        logger.info('system init...')
        # 初始化配置
        conf.settings = settings
        conf.max_level = args.max_level
        output_file = args.output_file
        output_format = args.output_format
        # 初始化爬虫
        proxy_list = get_proxy_list_by_file(args.proxy_file)
        api.request = Req(args.timeout, proxy_list, args.verify_proxy)

        plugin_controller = PluginController()
        plugin_controller.plugin_init()
        logger.info('Loaded plugins: %s' % ','.join(conf.plugins.keys()))

        # 绑定信号事件
        signal.signal(signal.SIGUSR1, on_signal)
        signal.signal(signal.SIGTERM, on_signal)
        signal.signal(signal.SIGINT, on_signal)

        logger.info('start target...')
        # 首个目标
        first_target = {
            'result': {'root_domain': [], 'domain': [], 'ip': []},
            'module': '',
            'level': 0,
            'parent_domain': ''
        }
        first_target['result'][domain_type].append(domain)
        plugin_controller.wp.result.put(first_target)

        # 开启任务监控
        logger.info('start task monitor and plugin...')
        kwargs = {'pc': plugin_controller}
        monitor = threading.Thread(target=task_monitor, kwargs=kwargs)
        monitor.start()

        # 开启插件执行
        plugin_controller.start()

        complete()
    else:
        logger.error(
            'Please input a target in the correct'
            ' format(domain/root_domain/ip)!'
        )
