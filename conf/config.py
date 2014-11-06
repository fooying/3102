#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import sys
import platform

VERSION = 'BETA 1.0'

PROXY = {
    # 'http'：'http://user:password@host',
    'http': 'http://121.12.255.212:8086'
}


ICP_API_CONFIG = {
    'icpchaxun': {
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
}

START_STR = r'''
                 _____  __  _____  _____
                |____ |/  ||  _  |/ __  \
                    / /`| || |/' |`' / /'
                    \ \ | ||  /| |  / /
                .___/ /_| |\ |_/ /./ /___
                \____/ \___/\___/ \_____/

        Domain/ip Fuzzing tool for vulnerability mining
               By Fooying www.fooying.com
'''
if sys.stdout.isatty() and platform.system() != 'Windows':
    START_STR = '\033[1;32m' + START_STR + '\033[1;m'
