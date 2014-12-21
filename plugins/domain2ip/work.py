#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import socket

from core.plugin import Plugin


class domain2ip(Plugin):
    def __init__(self):
        super(domain2ip, self).__init__('domain2ip')

    def start(self, target, domain_type, level):
        try:
            ip = socket.gethostbyname(target)
            result = {
                'result': {
                    'root_domain': [],
                    'ip': [ip],
                    'domain': []
                },
                'module': 'domain2ip',
                'parent_target': target,
                'level': level,
            }
        except socket.gaierror:
            result = None
        return result
