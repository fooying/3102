#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import sys
import platform


def format_message(message, color_code, symbol):
    if sys.stdout.isatty() and platform.system() != 'Windows':
        format_str = '\033[1;%sm[%s]\033[1;m {0}' % (color_code, symbol)
    else:
        format_str = '[%s] {0}' % symbol
    message = format_str.format(message)
    return message


def print_status(message=""):
    print(format_message(message, 34, '*'))


def print_good(message=""):
    print(format_message(message, 32, '*'))


def print_error(message=""):
    print(format_message(message, 31, '-'))


def print_debug(message=""):
    print(format_message(message, 31, '!'))


def print_line(message=""):
    print("{0}".format(message))
