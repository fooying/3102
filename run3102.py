#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import sys

from config.settings import START_STR


def main(args=None):
    print(START_STR)
    try:
        from core.parser import parse
        from core.controllers.controller import start

        args = parse()
        start(args)
    except Exception, e:
        print e
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
