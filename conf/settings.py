#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import sys
import platform

VERSION = 'v2.0'

START_STR = r'''
                 _____  __  _____  _____
                |____ |/  ||  _  |/ __  \
                    / /`| || |/' |`' / /'
                    \ \ | ||  /| |  / /
                .___/ /_| |\ |_/ /./ /___
                \____/ \___/\___/ \_____/

        Domain/ip Fuzzing tool for vulnerability mining
               By Fooying(www.fooying.com)
'''
if sys.stdout.isatty() and platform.system() != 'Windows':
    START_STR = '\033[1;32m' + START_STR + '\033[1;m'

# 允许的输入和输出
ALLOW_OUTPUT = ALLOW_INPUTS = ['domain', 'root_domain', 'ip']

# 环境路径配置
dirname = os.path.dirname
abspath = os.path.abspath
join = os.path.join

ROOT_PATH = dirname(dirname(abspath(__file__)))

PLUGINS_PATH = join(ROOT_PATH, 'plugins')
OUTPUT_TEMPLATE_OPPOSITE_PATH = join('core', 'output', 'templates')
OUTPUT_TEMPLATE_PATH = join(ROOT_PATH, OUTPUT_TEMPLATE_OPPOSITE_PATH)


