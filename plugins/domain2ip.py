#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import socket


class Domain2Ip:
    def get_value(self, domain):
        try:
            ip = socket.gethostbyname(domain)
        except socket.gaierror:
            ip = None
        return ip

