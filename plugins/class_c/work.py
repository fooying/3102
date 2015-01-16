#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from core.plugin import Plugin
from comm.coroutine import WorkerPool


class class_c(Plugin):

    def __init__(self):
        super(class_c, self).__init__('class_c')
        self.wp = WorkerPool()

    def start(self, domain, domain_type, level):
        super(class_c, self).start(domain, domain_type, level)
        result = []
        ips = self._get_ips(domain)
        for ip in ips:
            self.wp.add_job(self._check_ip, ip, result)
        self.wp.run()

        self.result = {
            'root_domain': [],
            'ip': result,
            'domain': [],
        }
        super(class_c, self).end()
        return self.result

    def _check_ip(self, ip, result):
        try:
            req = self.req.request('GET', 'http://' + ip)
        except:
            pass
        else:
            result.append(ip)

    def _get_ips(self, ip, start=1, end=255):
        ip_pre = '.'.join(ip.split('.')[:3]) + '.'
        return [ip_pre + str(_) for _ in range(start, end)]
