#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re

from core.plugin import Plugin


class subdomain(Plugin):
    def __init__(self):
        super(subdomain, self).__init__('subdomain')

    def start(self, target, domain_type, level):
        domain_level = 4
        domain = target
        url = 'http://i.links.cn/subdomain/'
        data = {
            'domain': domain,
            'b2': 1,
            'b3': 1 if domain_level >= 3 else 0,
            'b4': 1 if domain_level >= 4 else 0,
        }
        html = self.req.request('POST', url, data=data, timeout=30)
        regex = ('''<a\shref="http://[^"]*?"\srel=nof'''
                 '''ollow\starget=_blank>http://([^"]*?)</a></div>''')
        try:
            result = re.findall(regex, html)
            result = {
                'result': {
                    'root_domain': [],
                    'ip': [],
                    'domain': list(set(result))
                },
                'module': 'icp',
                'parent_target': target,
                'level': level,
            }
        except:
            result = None
        return result
