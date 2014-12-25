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
from comm.util import is_intra_ip
from comm.rootdomain import Domain

logger = logging.getLogger('3102')


def task_monitor(pc):
    while True:
        try:
            one_result = pc.wp.result.get(timeout=1)
        except gevent.queue.Empty:
            if pc.wp.target_queue.empty() and pc.wp.is_finished():
                pc.exit()
                break
        else:
            add_task_and_save(pc, one_result)


def print_task_status(pc):
    status = pc.wp.get_status()
    msg = ('Task Monitor:level %s:total task: %s ,'
           'wait task: %s, result num: %s') % (
        kb.status.level, kb.status.total_task_num,
        kb.status.total_task_num - kb.status.do_task_num,
        kb.status.result_num
    )
    msg = msg.ljust(78, ' ')
    logger.debug(msg)
    print status


def add_task_and_save(pc, one_result):
    level = one_result.get('level', -1) + 1

    if level <= conf.max_level:
        if level > kb.status.level:
            kb.status.level = level
            print_task_status(pc)

        module = one_result.get('module')

        for task_type in one_result.get('result', {}).keys():
            for domain in one_result.get('result', {}).get(task_type, []):
                domain = Domain.url_format(domain)
                if task_type == 'ip' and is_intra_ip(domain):
                    continue
                if domain not in result[task_type]:
                    target = {
                        'level': level,
                        'domain_type': task_type,
                        'target': domain,
                        'parent_module': module
                    }
                    kb.status.total_task_num += 1
                    pc.wp.target_queue.put(target)
                    save_result(one_result, domain, task_type)


def save_result(one_result, domain, task_type):
        want_save_result = copy.deepcopy(one_result)
        want_save_result.update({'taget': domain})
        want_save_result.pop('result')
        result[task_type][domain] = want_save_result
        kb.status.result_num += 1


def start_job(pc):
    while not pc.exit:
        pc.run_job()
        print_task_status(pc)
        gevent.sleep(10)
