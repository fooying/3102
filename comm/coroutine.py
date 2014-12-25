#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from gevent.pool import Pool
from gevent.queue import Queue
from gevent.monkey import patch_all

patch_all()


class WorkerPool(object):
    def __init__(self, pool_size=5000):
        self.job_pool = Pool(size=pool_size)
        self.result = Queue()
        self.target_queue = Queue()
        self.all_job = Pool()

    def add_job(self, job_func, *args, **kwargs):
        job = self.job_pool.apply_async(
            job_func,
            args=args,
            kwds=kwargs,
            callback=self._call_func)
        self.job_pool.add(job)
        self.all_job.add(job)

    def run(self, timeout=None):
        self.job_pool.join(timeout=timeout, raise_error=False)

    def _call_func(self, job_ret):
        if job_ret:
            self.result.put(job_ret)

    def is_finished(self):
        finished = True
        for job in self.all_job:
            if not job.ready():
                finished = False
                break
        return finished

    def get_pool_wait_num(self):
        return len(self.job_pool)

    def get_status(self):
        status = {
            'total': 0,
            'wait': 0,
            'success': 0,
            'except': 0,
            'runing': 0
        }
        for job in self.all_job:
            status['total'] += 1
            if job.started and not job.ready():
                status['runing'] += 1
            elif job.successful():
                status['success'] += 1
            elif job.ready():
                status['except'] += 1
            else:
                status['wait'] += 1
        return status

    def shutdown(self):
        self.job_pool.kill()
