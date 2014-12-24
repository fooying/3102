#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import copy
import gevent
import logging

from core.data import kb
from core.data import conf
from core.data import result
from comm.rootdomain import Domain

logger = logging.getLogger('3102')


def task_monitor(pc):
    while True:
        print_task_status()
        try:
            one_result = pc.wp.result.get(timeout=1)
        except gevent.queue.Empty, e:
            if pc.wp.target_queue.empty() and pc.wp.is_finished():
                pc.exit = True
                break
        else:
            add_task_and_save(pc, one_result)


def print_task_status(log=False):
    msg = 'Task monitor:level %s:task num: %s, result num: %s\r' % (
        kb.status.level, kb.status.task_num, kb.status.result_num
    )
    if log:
        logger.debug(msg)
    else:
        print '\033[1;32m[+]%s\033[1;m\r' % msg,


def add_task_and_save(pc, one_result):
    level = one_result.get('level', -1) + 1
    module = one_result.get('module')
    if level <= conf.max_level:
        if level > kb.status.level:
            kb.status.level = level
            print_task_status()
        module = one_result.get('module')

        for task_type in one_result.get('result', {}).keys():
            for domain in one_result.get('result', {}).get(task_type, []):
                if domain not in result[task_type]:
                    domain = Domain.url_format(domain)
                    target = {
                        'level': level,
                        'domain_type': task_type,
                        'target': domain,
                        'parent_module': module
                    }
                    pc.wp.target_queue.put(target)
                    kb.status.task_num += 1
                    save_result(one_result, domain, task_type)


def save_result(one_result, domain, task_type):
        want_save_result = copy.deepcopy(one_result)
        want_save_result.update({'taget': domain})
        want_save_result.pop('result')
        result[task_type][domain] = want_save_result
        kb.status.result_num += 1
