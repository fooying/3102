#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re

from request import request
from fdomain.rootdomain import Domain


class Ip2Domain:
    def __init__(self, api_name='bing'):
        self.api_name = api_name

    def get_domains_by_ip(self, ip):
        url = 'http://cn.bing.com/search?q=ip:%s' % ip
        html = request(url, 'GET')

        domain_regx = r'''
            <h2><a\shref="https?://([^"]*?)"\starget="_blank"\sh="ID=[^"]*?">[^<]*?</a></h2>
        '''
        domain_list = re.findall(domain_regx, html, re.X)
        domain_list = [
            Domain.get_domain(domain)
            for domain in domain_list
            if Domain.get_domain(domain)
        ]
        return list(set(domain_list))


if __name__ == '__main__':
    I = Ip2Domain()
    print(I.get_domains_by_ip('66.147.244.242'))
