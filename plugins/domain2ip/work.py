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

    def start(self, domain, domain_type, level):
        super(domain2ip, self).start(domain, domain_type, level)
        try:
            _, _, ipaddrlist = socket.gethostbyname_ex(domain)
        except socket.gaierror:
            pass
        else:
            self.result = {
                'root_domain': [],
                'ip': ipaddrlist,
                'domain': []
            }
        super(domain2ip, self).end()
        return self.result
