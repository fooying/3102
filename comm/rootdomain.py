#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from suffixs import SUFFIXS


class Domain:

    @classmethod
    def url_format(cls, url):
        """
        return http(s)://www.example.com
        """
        if url.startswith("http://"):
            url = url[7:]
        if url.startswith("https://"):
            url = url[8:]
        if url.endswith("/"):
            url = url[:-1]
        return url

    @classmethod
    def get_domain(cls, url):
        url = cls().url_format(url)
        domain = url[:url.index("/") + 1] if "/" in url else url
        return domain

    @classmethod
    def get_root_domain(cls, url):
        domain = cls().get_domain(url)
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
