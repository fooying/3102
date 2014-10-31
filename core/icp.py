#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re

from comm.rootdomain import Domain
from comm.request import request
from comm.config import ICP_API_CONFIG


class ICP:
    def __init__(self, api_name='icpchaxun'):
        self.api_name = api_name if api_name in ICP_API_CONFIG else 'icpchaxun'
        self.config = ICP_API_CONFIG[api_name]

    def _get_text_list(self, config, value):
        url = config[0] % value
        regx = config[1]
        text = request(url)
        result = re.findall(regx, text, re.I|re.S|re.X)
        return result

    def query_zt_by_domain(self, domain):
        """
        function to get icp subject
        """
        query_config = self.config['get_zt']
        zt_name = self._get_text_list(query_config, domain)[0]
        return zt_name

    def query_domains_by_zt(self, zt_name):
        """
        function to get others rootdomain by icp subject
        """
        query_config = self.config['get_domains']
        domains = self._get_text_list(query_config, zt_name)
        new_domains = []
        for domain in domains:
            if domain[0]:
                new_domains.append(domain[0])
            if domain[1]:
                new_domains.append(domain[1])
        return list(set(new_domains))

    @classmethod
    def get_rootdomains_by_domain(cls, domain):
        """
        function to get others rootdomain by a known rootdomain
        """
        domain = Domain.get_domain(domain)
        zt_name = cls().query_zt_by_domain(domain)
        domains = cls().query_domains_by_zt(zt_name)
        root_domain = Domain.get_root_domain(domain)
        if root_domain:
            domains.append(domain)
        # todo: Judge the domain/ip format
        return domains

if __name__ == '__main__':
    import sys
    domain = sys.argv[1]
    print ICP.get_rootdomains_by_domain(domain)
