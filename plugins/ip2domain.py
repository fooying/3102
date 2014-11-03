#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re
import time

from comm.request import request
from comm.rootdomain import Domain
from comm.printer import *


class Ip2Domain:
    def __init__(self, api_name='bing'):
        self.api_name = api_name

    def get_domains_by_ip(self, ip):
        print_status('Start get domain by ip through bing...')
        url = 'http://cn.bing.com/search?q=ip:%s&first=999999991&FORM=PERE' % ip
        print url
        html = request(url, 'GET')

        domain_regx = r'''
            <h2><a\shref="https?://([^"]*?)"\starget="_blank"\sh="ID=[^"]*?">[^<]*?</a></h2>
        '''
        domain_list = re.findall(domain_regx, html, re.X)

        total_page_regx = r'''<span\sclass="sb_count">\d*?\s-\s\d*?\s[^\(]*?\([^\s]*?\s(\d*?)\s[^\)]*?\)</span>'''
        import pdb;pdb.set_trace()
        result = re.search(total_page_regx, html)
        try:
            total_num = int(result.group(1).replace(',', ''))
        except:
            total_num = 9
        page_count = total_num / 9
        if total_num % 9 > 0:
            page_count += 1
        print_status('Total pages: %s, Total domains:%s' % (page_count, total_num))

        if page_count > 0:
            for n in range(total_num-1):
                print_status('Get page %s domains...' % str(n+1))
                url = 'http://cn.bing.com/search?q=ip:%s&first=%s1&FORM=PERE3' % (ip, n)
                html = request(url, 'GET')
                new_domain_list = re.findall(domain_regx, html, re.X)
                domain_list.extend(new_domain_list)
                time.sleep(20)

        domain_list = [
            Domain.get_domain(domain)
            for domain in domain_list
            if Domain.get_domain(domain)
        ]
        return list(set(domain_list))






if __name__ == '__main__':
    I = Ip2Domain()
    print(I.get_domains_by_ip('66.147.244.242'))
