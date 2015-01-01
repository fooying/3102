#!/usr/bin/env python
# coding: utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from yaml import dump

from template import Output


class OutputYaml(Output):

    def save(self, output_file):
        super(OutputYaml, self).save(output_file)
        with open(output_file, 'w') as f:
            dump(u'%s' % self.result, f, encoding=('utf-8'))
