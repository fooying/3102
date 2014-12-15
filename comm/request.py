#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import random
import logging
import requests
from gevent.monkey import patch_all

from coroutine import WorkerPool


patch_all()
logger = logging.getLogger('3102')


class Req(object):
    def __init__(self, timeout=10, proxy_list=[], verify_proxy=False):
        self.timeout = timeout
        self.verify = False
        self.proxy_list = proxy_list
        self.verify_proxy = False
        if self.proxy_list and verify_proxy:
            logger.info('start verify proxy...please wait')
            self.verify_proxy = False
            self.__verify_proxy()

    def __verify_proxy(self):
        """
        进行代码验证处理,建议提供的代理列表是可用的,直接关闭验证
        """
        wp = WorkerPool()
        for proxy in self.proxy_list:
            proxies = {
                proxy[0]: proxy[1]
            }
            kwargs = {'proxies': proxies}
            wp.add_job(self.__emulate_request, **kwargs)
        wp.run()
        result = wp.result
        wp.run()
        self.proxy_list = [proxy[1] for proxy in result if proxy[0]]
        logger.info('start verify completed!')
        self.verify_proxy = False

    def __emulate_request(self, **kwargs):
        try:
            self.request('GET', 'http://www.qq.com', **kwargs)
        except requests.exceptions.ConnectionError:
            return (False, kwargs['proxies'])
        else:
            return (True, kwargs['proxies'])

    def request(self, method='GET', url='', *args, **kwargs):
        s = requests.Session()
        s.headers.update({
            'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko)'
                           'Chrome/37.0.2062.124 Safari/537.36')
        })
        s.verify = self.verify
        s.timeout = self.timeout
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            s.proxies = proxy
        req = s.request(method,  url, *args, **kwargs)
        return req
