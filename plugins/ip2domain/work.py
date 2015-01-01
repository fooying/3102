#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re
import time

from core.plugin import Plugin
from comm.rootdomain import Domain
from comm.utils import get_domain_type


class ip2domain(Plugin):
    def __init__(self):
        super(ip2domain, self).__init__('ip2domain')

    def __get_count(self, html):
        total_page_regx = (
            r'''<span\sclass="sb_count">\d*?\s-\s\d*?'''
            r'''\s[^\(]*?\([^\s]*?\s(\d*?)\s[^\)]*?\)</span>'''
        )
        result = re.search(total_page_regx, html)
        try:
            total_num = int(result.group(1).replace(',', ''))
        except:
            total_num = 9
        page_count = total_num / 9
        if total_num % 9 > 0:
            page_count += 1
        return total_num, page_count

    def __classify_result(self, domain_list):
        domains = []
        root_domains = []
        ips = []
        for domain in domain_list:
            domain = Domain.get_domain(domain)
            domain_type = get_domain_type(domain)
            if domain_type == 'ip' and domain not in ips:
                ips.append(domain)
            elif domain_type == 'root_domain' and domain not in root_domains:
                root_domains.append(domain)
            elif domain_type == 'domain' and domain not in domains:
                domains.append(domain)
        return domains, root_domains, ips

    def start(self, domain, domain_type, level):
        super(ip2domain, self).start(domain, domain_type, level)
        url = ('http://cn.bing.com/search?q='
               'ip:%s&first=999999991&FORM=PERE' % domain)
        result = None
        try:
            html = self.req.request('GET', url).text
        except:
            html = ''
        else:
            domain_regx = r'''
                <h2><a\shref="https?://([^"]*?)"\starget="_blank"\sh="ID=[^"]*?">[^<]*?</a></h2>
            '''
            domain_list = re.findall(domain_regx, html, re.X)

            total_num, page_count = self.__get_count(html)

            if page_count > 0:
                for n in range(total_num-1):
                    url = ('http://cn.bing.com/search?q='
                           'ip:%s&first=%s1&FORM=PERE3' % (domain, n))
                    html = self.req.request('GET', url).text
                    new_domain_list = re.findall(domain_regx, html, re.X)
                    domain_list.extend(new_domain_list)
                    time.sleep(1)

            domains, root_domains, ips = self.__classify_result(domain_list)
            self.result = {
                'root_domain': root_domains,
                'ip': ips,
                'domain': domains
            }
        super(ip2domain, self).end()
        return self.result
