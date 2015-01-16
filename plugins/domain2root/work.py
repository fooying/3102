#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from core.plugin import Plugin
from comm.rootdomain import Domain
from comm.utils import is_ip, is_url


class domain2root(Plugin):

    def __init__(self):
        super(domain2root, self).__init__('domain2root')

    def start(self, domain, domain_type, level):
        super(domain2root, self).start(domain, domain_type, level)
        try:
            root_domain = Domain.get_root_domain(domain)
        except:
            root_domain = None
        if root_domain:
            self.result = {
                'root_domain': [root_domain],
                'ip': [],
                'domain': []
            }
        super(domain2root, self).end()
        return self.result
