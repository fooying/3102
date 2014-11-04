#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import argparse
from copy import deepcopy

from core.data import task, all_target, target, control
from conf.config import VERSION
from comm.rootdomain import Domain


VERSION_INFO = '3102 Version:%s, by Fooying' % VERSION

INDENT = ' ' * 2
USAGE = os.linesep.join([
    '',
    '%seg1: python run3102.py --ip ' % INDENT,
    '%seg2: python run3102.py --domain ' % INDENT,
    ])


def parse(args=None):
    parser = argparse.ArgumentParser(
        usage=USAGE, formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    parser.add_argument(
        '-h', '--help', action='help',
        help='show this help message and exit'
    )
    parser.add_argument('-V', '--version', action='version',
                        version=VERSION_INFO)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-d', '--domain', dest='domain',
        help='Target domain/rootdomain'
    )
    group.add_argument(
        '-i', '--ip', dest='ip',
        help='Target ip'
    )
    parser.add_argument(
        '-l', '--max_level', dest='max_level', default=3,
        type=int, help='max level to get domain/ip/rootdomain, default:3'
    )

    args = parser.parse_args(args)
    try:
        if args.domain:
            domain = args.domain
            root_domain = Domain.get_root_domain(domain)
            new_target = deepcopy(target)
            new_target.value = domain
            new_target.source = 'input'
            if root_domain != domain:
                domain_type = 'domain'
            else:
                domain_type = 'rootdomain'
            new_target.type = domain_type
            task['%ss' % domain_type].add(domain)
            all_target[domain.replace('.', '_')] = new_target
        if args.ip:
            ip = args.ip
            new_target = deepcopy(target)
            new_target.value = ip
            new_target.source = 'input'
            new_target.type = 'ip'
            task.ips.add(ip)
            all_target[ip.replace('.', '_')] = new_target

        control.max_level = args.max_level
    except Exception, e:
        print_error(str(e))
