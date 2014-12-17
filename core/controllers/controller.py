#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import logging
import threading

from conf import settings
from core.data import api
from core.data import conf
from comm.request import Req
from core.output import output
from comm.log import init_logger
from comm.rootdomain import Domain
from comm.utils import get_log_level
from comm.utils import get_domain_type
from comm.utils import get_proxy_list_by_file
from core.controllers.taskmanager import task_monitor
from core.controllers.plugin_controller import PluginController

logger = logging.getLogger('3102')


def start(args):
    target = args.target
    domain_type = get_domain_type(target)
    if domain_type in settings.ALLOW_INPUTS:
        target = Domain.url_format(target)

        # 初始化日志
        log_level = get_log_level(args.log_level)
        init_logger(log_file_path=args.log_file, log_level=log_level)
        logger.info('system init...')
        conf.settings = settings
        conf.max_level = args.max_level
        # 初始化爬虫
        proxy_list = get_proxy_list_by_file(args.proxy_file)
        api.request = Req(args.timeout, proxy_list, args.verify_proxy)

        logger.info('plugin init...')
        plugin_controller = PluginController()
        plugin_controller.plugin_init()

        logger.info('start fuzzing domain/ip...')
        # 首个目标
        first_target = {
            'result': {'root_domain': [], 'domain': [], 'ip': []},
            'module': '',
            'level': 0,
            'parent_target': ''
        }
        first_target['result'][domain_type].append(target)
        logger.info('start plugin...')
        plugin_controller.wp.result.put(first_target)
        # 开启任务监控
        kwargs = {'pc': plugin_controller}
        monitor = threading.Thread(target=task_monitor, kwargs=kwargs)
        monitor.start()
        # 开启插件执行
        plugin_controller.start()

        # 回收结果
        logger.debug('output result to file...')
        output_file = args.output_file
        output(output_file)
        logger.info('result had output to[%s]!' % output_file)

        logger.info('Complete Fuzzing!')
    else:
        logger.error(
            'Please input a target in the correct'
            ' format(domain/root_domain/ip)!'
        )
