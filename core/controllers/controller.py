#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import copy
import gevent
import logging


from conf import settings
from comm.request import Req
from comm.log import init_logger
from comm.rootdomain import Domain
from comm.utils import get_domain_type
from core.data import kb, conf, api, result
from core.plugin_controller import PluginController


logger = logging.getLoger('3102')


def task_monitor(pc):
    """
    输出:
        当前进行层级
        当前请求数
    """
    while True:
        try:
            one_result = pc.wp.result.get_nowait()
        except gevent.queue.Empty:
            if pc.wp.target_queue.empty() and pc.wp.is_finshed():
                break
        else:
            add_task_and_save(pc, one_result)
            print_task_status()


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
            tmp_result = result.tmp[module]
            if level <= conf.max_level and domain not in tmp_result:
                target = {
                    'level': level,
                    'domain_type': task_type,
                    'target': domain
                }
                pc.wp.target_queue.add(target)
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


def start(target, max_level, out_file, out_format='txt'):
    domain_type = get_domain_type(target)
    if domain_type in settings.ALLOW_INPUT:
        target = Domain.url_format(target)
        init_logger()
        logger.info('system init...')
        conf.settings = settings
        conf.max_level = max_level
        api.request = Req()
        logger.info('plugin init...')
        plugin_controller = PluginController()
        plugin_controller.init()
        logger.info('start fuzzing domain/ip...')
        # 首个目标
        first_target = {
            'result': {'root_domain': [], 'domain': [], 'ip': []},
            'module': '',
            'level': 0,
            'parent_target': ''
        }
        first_target['result'][domain_type].append(target)
        plugin_controller.wp.result.add(first_target)
        # 开启任务监控
        gevent.joinall(gevent.spawn(task_monitor, plugin_controller))
        # 开启插件执行
        plugin_controller.start()
        # 回收结果
        # todo
        logger.info('Complete Fuzzing!')
    else:
        logger.error(
            'Please input a target in the correct'
            ' format(domain/root_domain/ip)!'
        )
