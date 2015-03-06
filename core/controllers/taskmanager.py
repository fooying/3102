#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import copy

import gevent

from core.data import kb
from core.data import conf
from core.data import result
from core.data import api
from core.data import options
from comm.utils import is_intra_ip
from comm.rootdomain import Domain



def task_monitor(pc):
    while not pc.exit_flag:
        try:
            if options.max_level <= kb.status.level:
                print_task_status()
            one_result = pc.wp.result.get(timeout=1)
        except gevent.queue.Empty:
            if pc.wp.target_queue.empty() and is_all_job_done():
                pc.exit()
                break
        else:
            add_task_and_save(pc, one_result)


def print_task_status(log=False):
    status = get_all_job_status()
    msg = ('Monitor:level[%s], total[%s], done[%s], '
           'runing[%s], result num[%s].') % (
        kb.status.level, status['total'], status['done'],
        status['runing'], kb.status.result_num
    )
    msg = msg.ljust(80, ' ')
    if log:
        api.logger.info(msg)
    else:
        print '\033[1;34m[m] %s\033[1;m\r' % msg,


def add_task_and_save(pc, one_result):
    level = one_result.get('level', -1) + 1

    if level <= options.max_level:
        if level > kb.status.level:
            kb.status.level = level
            print_task_status(True)

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
                        'domain': domain,
                        'parent_module': module
                    }
                    pc.wp.target_queue.put(target)
                    save_result(one_result, domain, task_type)


def save_result(one_result, domain, task_type):
    want_save_result = copy.deepcopy(one_result)
    want_save_result.update({'domain': domain})
    want_save_result.pop('result')
    result[task_type][domain] = want_save_result
    kb.status.result_num += 1


def get_all_job_status():
    status = {
        'total': len(kb.progress),
        'wait': 0,
        'runing': 0,
        'done': 0,
    }
    for job_progress in kb.progress.values():
        job_status = job_progress['status']
        status[job_status] += 1
    return status


def is_all_job_done():
    all_job_status = set()
    for job_progress in kb.progress.values():
        all_job_status.add(job_progress['status'])
    if all_job_status == set(['done']) or not all_job_status:
        return True
    else:
        return False
