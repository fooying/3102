#!/usr/bin/env python
# coding=utf-8

"""
根域名处理
"""

from suffixs import SUFFIXS


class Domain:

    @classmethod
    def url_format(cls, url):
        """
        return http(s)://www.example.com
        """
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        if url.endswith("/"):
            url = url[:-1]
        return url

    @classmethod
    def get_domain(cls, url):
        url = url.replace("https://", "")
        url = url.replace("http://", "")
        domain = url[:url.index("/")+1] if "/" in url else url
        return domain

    @classmethod
    def get_root_domain(cls, url):
        domain = cls.get_domain(url)
        domain_blocks = domain.split(".")
        index = -2
        suffix = ".".join(domain_blocks[index:])
        if_match = False
        if suffix in SUFFIXS:
            index -= 1
            if_match = True
        else:
            index += 1
            suffix = ".".join(domain_blocks[index:])
            if suffix in SUFFIXS:
                index -= 1
                if_match = True
        root_domain = ""
        if if_match:
            root_domain = ".".join(domain_blocks[index:])
        return root_domain
