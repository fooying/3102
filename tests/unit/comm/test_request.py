#!/usr/bin/env python
# coding=utf-8

from unittest import TestCase
from request import Req


class Request(TestCase):
    def setUp(self):
        proxy = [
            ('http', 'http://10.1.111.110:3102'),
            ('http', 'http://10.10.1.1:123')
        ]
        self.r = Req(proxy_list=proxy, verify_proxy=True)

    def test_proxy_verify(self):
        verify_proxy = [
            {'http': 'http://10.1.111.110:3102'}
        ]
        assert self.r.proxy_list == verify_proxy

    def test_request(self):
        r = Req()
        req = r.request('GET', 'http://www.qq.com')
        assert req.status_code == 200
