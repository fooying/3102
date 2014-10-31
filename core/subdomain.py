#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re

from comm.request import request
from comm.rootdomain import Domain


class SubDomain:
    def __init__(self, source_name="links"):
        self.source_name = source_name

    def get_subdomain_by_links(self, domain, level=4):
        domain = Domain.get_domain(domain)
        url = 'http://i.links.cn/subdomain/'
        data = {
            'domain': domain,
            'b2': 1,
            'b3': 1 if level>=3 else 0,
            'b4': 1 if level>=4 else 0,
        }
        html = request(url, 'POST', data=data)
        regex = '''<a\shref="http://[^"]*?"\srel=nofollow\starget=_blank>http://([^"]*?)</a></div>'''
        try:
            result = re.findall(regex, html)
        except:
            result = []
            time.sleep(3)
        result.append(domain)
        return list(set(result))


if __name__ == '__main__':
    S = SubDomain()
    print(S.get_subdomain_by_links('www.qq.com'))
