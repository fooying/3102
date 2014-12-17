#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from core.data import result


def output(output_file):
    with open(output_file, 'w') as f:
        for domain_type in result:
            for detail in result[domain_type]:
                f.write('%s\n' % detail)

