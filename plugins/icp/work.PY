#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re

from core.plugin import Plugin
from comm.rootdomain import Domain
from comm.utils import is_ip, is_url

ICP_API_CONFIG = {
    'get_zt': (
        'http://www.icpchaxun.com/beian.aspx?icpType=-1&icpValue=%s',
        '''
        <a\starget="_blank"\shref="/zhuti/[^"]*?">\s*?[^<]*?\s*?([^\s]*?)</a>
        '''
    ),
    'get_domains': (
        'http://www.icpchaxun.com/zhuti/%s/',
        '''
        <a\shref="/yuming/[.a-z0-9_\w]*?/">([.a-z0-9_\w]*?)</a>|
        onclick="goto\('/yuming/[.a-z0-9_\w]*?/'\);">([.a-z0-9_\w]*?)</span>
        '''
    ),
}


class icp(Plugin):
    def __init__(self):
        super(icp, self).__init__('icp')
        self.config = ICP_API_CONFIG

    def _get_text_list(self, config, value):
        url = config[0] % value
        regx = config[1]
        text = self.req.request('GET', url).text
        result = re.findall(regx, text, re.I|re.S|re.X)
        return result

    def query_zt_by_domain(self, domain):
        """
        function to get icp subject
        """
        query_config = self.config['get_zt']
        result = self._get_text_list(query_config, domain)
        zt_name = result[0] if result else None
        return zt_name

    def query_domains_by_zt(self, zt_name):
        """
        function to get others rootdomain by icp subject
        """
        if zt_name:
            query_config = self.config['get_domains']
            domains = self._get_text_list(query_config, zt_name)
            new_domains = []
            for domain in domains:
                if domain[0]:
                    new_domains.append(domain[0])
                if domain[1]:
                    new_domains.append(domain[1])
            return list(set(new_domains))
        else:
            return []

    def start(self, target, domain_type, level):
        """
        function to get others rootdomain by a known rootdomain
        """
        domain = Domain.get_domain(target)
        zt_name = self.query_zt_by_domain(target)
        domains = self.query_domains_by_zt(zt_name)
        domains.append(target)
        ips = []
        root_domains = []
        for domain in domains:
            if is_ip(domain) and domain not in ips:
                ips.append(domain)
            elif is_url(domain) and domain not in root_domains:
                root_domains.append(domain)

        result = {
            'result': {
                'root_domain': root_domains,
                'ip': ips,
                'domain': []
            },
            'module': 'icp',
            'parent_target': target
        }
        return result
