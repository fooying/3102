#!/usr/bin/env python
# coding=utf-8

import requests

from unittest import TestCase
from request import Req


class Request(TestCase):
    def setUp(self):
        proxy = [
                ('http', 'http://202.109.163.75:8085'),
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

    def test_request_timeout(self):
        self.r = Req(timeout=0.1)
        try:
            self.r.request('GET', 'http://www.google.com')
        except requests.exceptions.ConnectionError:
            assert True
        else:
            assert False

