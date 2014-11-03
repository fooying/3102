#!/usr/bin/env python
# coding=utf-8

import os
import argparse

from conf.config import VERSION


VERSION_INFO = '3102 Version:%s, by Fooying' % VERSION

INDENT = ' ' * 2
USAGE = os.linesep.join([
    '',
    '%seg1: python run3102.py -ip ' % INDENT,
    '%seg2: python run3102.py -domain ' % INDENT,
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
    parser.add_argument('-V', '--version', action='version', version=VERSION_INFO)

    parser.add_argument(
        '-d', '--domain', dest='domain', required=True,
        help='Target domain/rootdomain'
    )
    parser.add_argument(
        '-i', '--ip', dest='ip', required=True,
        help='Target ip'
    )

    args = parser.parse_args(args)
    return args, parser
