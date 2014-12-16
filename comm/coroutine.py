#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import time
from gevent.pool import Pool
from gevent.queue import Queue
from gevent.monkey import patch_all

patch_all()


class WorkerPool(object):
    def __init__(self, pool_size=5000):
        self.job_pool = Pool(size=pool_size)
        self.result = Queue()
        self.target_queue = Queue()

    def add_job(self, job_func, *args, **kwargs):
        self.job_pool.add(
            self.job_pool.apply_async(
                job_func,
                args=args,
                kwds=kwargs,
                callback=self._call_func
            )
        )
    def run(self, timeout=None):
        self.job_pool.join(timeout=timeout, raise_error=False)

    def _call_func(self, job_ret):
        self.result.add(job_ret)

    def is_finished(self):
        finished = True
        for job in self.job.pool:
            if not job.ready():
                finished = False
                break
        return finished

    def shutdown(self):
        self.job_pool.kill()
