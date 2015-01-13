#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re
import string
import socket
from random import randint, choice

from core.plugin import Plugin
from comm.prefixs import PREFIXS
from comm.coroutine import WorkerPool


class subdomain_brute(Plugin):
    def __init__(self):
        super(subdomain_brute, self).__init__('subdomain_brute')

    def start(self, domain, domain_type, level):
        super(subdomain_brute, self).start(domain, domain_type, level)
        subdomain = self._random_subdomain(domain)
        if self._check_wildcard(subdomain):
            ip = socket.gethostbyname(subdomain)
            self.result = {
                'root_domain': [],
                'ip': [],
                'domain': [subdomain]
            }
        else:
            result = []
            self.wp = WorkerPool()
            for pre in PREFIXS:
                subdomain = pre + '.' + domain
                self.wp.add_job(self._check_is_subdomain, subdomain, result)
            self.wp.run()
            self.result = {
                'root_domain': [],
                'ip': [],
                'domain': result
            }
        super(subdomain_brute, self).end()
        return self.result

    def _check_wildcard(self, subdomain):
        try:
            ip = socket.gethostbyname(subdomain)
            print ip
            return True
        except:
            return False

    def _random_subdomain(self, domain):
        chars = string.letters + string.digits
        length = randint(5, 15)
        random_str = ''.join([choice(chars) for _ in range(length)])
        subdomain = random_str + '.' + domain
        return subdomain

    def _check_is_subdomain(self, subdomain, result):
        try:
            ip = socket.gethostbyname(subdomain)
        except:
            pass
        else:
            result.append(subdomain)

