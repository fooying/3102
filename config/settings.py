#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import sys
from comm.revision import getRevisionNumber

VERSION = "2.1"
REVISION = getRevisionNumber()
VERSION_STRING = "3102/%s%s" % (VERSION, "-%s" % REVISION if REVISION else "-nongit-%s" % time.strftime("%Y%m%d", time.gmtime(os.path.getctime(__file__))))
DESCRIPTION = "Domain/ip Fuzzing tool for vulnerability mining"
SITE = "http://www.fooying.com"
ISSUES_PAGE = "https://github.com/fooying/3102/issues"
GIT_REPOSITORY = "git@github.com:fooying/3102.git"
GIT_PAGE = "https://github.com/fooying/3102"

COLOR_VERSION = '\033[01;37m{\033[01;%dm%s\033[01;37m}\033[01;33m\n' % ((31 + hash(REVISION) % 6) if REVISION else 30, VERSION_STRING.split('/')[-1])
COLOR_DESCRIPTION = '\033[1;32m%s\033[1;m' % (DESCRIPTION + '\n\t    By Fooying (%s)' % SITE)

BANNER = '''\033[01;32m
                 _____  __  _____  _____
                |____ |/  ||  _  |/ __  \       
                    / /`| || |/' |`' / /'
                    \ \ | ||  /| |  / /
                .___/ /_| |\ |_/ /./ /___
                \____/ \___/\___/ \_____/       {color_version}
        {color_description}
'''.format(color_version=COLOR_VERSION, color_description=COLOR_DESCRIPTION)

# 允许的输入和输出
ALLOW_OUTPUT = ALLOW_INPUTS = ['domain', 'root_domain', 'ip']
