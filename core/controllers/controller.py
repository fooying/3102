#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import copy
import time
import gevent
import logging
import threading


from conf import settings
from comm.request import Req
from comm.log import init_logger
from comm.rootdomain import Domain
from comm.utils import get_domain_type
from core.data import kb, conf, api, result
from core.controllers.plugin_controller import PluginController


logger = logging.getLogger('3102')


def task_monitor(pc):
    """
    输出:
        当前进行层级
        当前请求数
    """
    while True:
        try:
            one_result = pc.wp.result.get(timeout=5)
        except gevent.queue.Empty:
            if pc.wp.target_queue.empty() and pc.wp.is_finished():
                pc.exit = True
                break
        else:
            add_task_and_save(pc, one_result)
        #print_task_status()


def print_task_status():
    msg = 'level: %s, task num: %s, result num: %s' % (
        kb.status.level, kb.status.task_num, kb.status.result_num
    )
    logger.info(msg)


def add_task_and_save(pc, one_result):
    level = one_result.get('level', -1) + 1
    module = one_result.get('module')
    if level > kb.status.level:
        kb.status.level = level
    for task_type in one_result.get('result', {}).keys():
        for domain in one_result.get('result', {}).get(task_type, []):
            domain = Domain.url_format(domain)
            save_result(one_result, domain, task_type)
            tmp_result = result.tmp.get(module, [])
            if level <= conf.max_level and domain not in tmp_result:
                target = {
                    'level': level,
                    'domain_type': task_type,
                    'target': domain
                }
                pc.wp.target_queue.put(target)
                kb.status.task_num += 1


def save_result(one_result, domain, domain_type):
    if domain not in result[domain_type]:
        want_save_result = copy.deepcopy(one_result)
        want_save_result.update({'taget': domain})
        want_save_result.pop('result')
        result[domain_type][domain] = want_save_result
        kb.status.result_num += 1
        module = one_result.get('module')
        if conf.plugins.get(module, {}).get('onerepeat'):
            if module and module not in result.tmp:
                result.tmp[module] = set([])
            else:
                result.tmp[module].add(domain)


def get_log_level(level_num):
    log_level = {
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARNING,
        4: logging.ERROR,
    }
    return log_level.get(level_num)


def get_proxy_list_by_file(file_path):
    if file_path and os.path.exists(file_path):
        with open(file_path) as f:
            proxys = f.read().splitlines()
        proxy_list = []
        for proxy in proxys:
            proxy = proxy.split(',')
            proxy_list.append((proxy[0], proxy[1]))
    else:
        proxy_list = []
    return proxy_list


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
        output_file = args.output_file
        print result

        logger.info('Complete Fuzzing!')
    else:
        logger.error(
            'Please input a target in the correct'
            ' format(domain/root_domain/ip)!'
        )
