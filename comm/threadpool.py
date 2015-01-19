#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import Queue
import threading
from six.moves import range


class ThreadPool(object):

    def __init__(self, pool_size=10, queue_size=0):
        self.task_queue = Queue.Queue(queue_size)
        self.workers = []
        self.__init_thread_pool(pool_size)

    def __init_thread_pool(self, pool_size):
        for i in range(pool_size):
            self.workers.append(Work(self.task_queue))

    def add_job(self, func, **args):
        self.work_queue.put((func, args))

    def wait_allcomplete(self):
        for worker in self.workers:
            if worker.isAlive():
                worker.join()

    def get_job_number(self):
        return self.task_queue.qsize()

    def get_unfinish_job_number(self):
        return self.taskQueue.unfinished_tasks


class Work(threading.Thread):

    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.start()

    def run(self):
        while True:
            try:
                func, args = self.task_queue.get(block=False)
                if func:
                    func(args)
                self.task_queue.task_done()
            except:
                break
