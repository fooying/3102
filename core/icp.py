#!/usr/bin/env python
# coding=utf-8
# Fooying@2014-10-13 14:29:01

"""
封装的ICP模块
"""

import re
from fdomain.rootdomain import Domain

from comm.request import request
from comm.config import ICP_API_CONFIG


class ICP:
    def __init__(self, api_name="icpchaxun"):
        self.api_name = api_name if api_name in ICP_API_CONFIG else "icpchaxun"
        self.config = ICP_API_CONFIG[api_name]

    def _get_text_list(self, config, value):
        url = config[0] % value
        regx = config[1]
        text = request(url)
        result = re.findall(regx, text, re.I|re.S|re.X)
        return result

    def query_zt_by_domain(self, domain):
        """
        根据domain获取ICP主体名称
        """
        query_config = self.config["get_zt"]
        zt_name = self._get_text_list(query_config, domain)[0]
        return zt_name

    def query_domains_by_zt(self, zt_name):
        """
        根据主体名称,获取备案的其他根域
        """
        query_config = self.config["get_domains"]
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
        通过域名获取同主体的备案根域列表
        """
        domain = Domain.get_domain(domain)
        zt_name = cls().query_zt_by_domain(domain)
        domains = cls().query_domains_by_zt(zt_name)
        root_domain = Domain.get_root_domain(domain)
        if root_domain:
            domains.append(domain)
        # todo: 判断是否正确格式域名和ip并做归类
        return domains

if __name__ == '__main__':
    import sys
    domain = sys.argv[1]
    print ICP.get_rootdomains_by_domain(domain)
