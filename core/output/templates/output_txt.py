#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from template import Output


class OutputTxt(Output):

    def save(self, output_file):
        super(OutputTxt, self).save(output_file)
        with open(output_file, 'w') as f:
            for key in self.result.keys():
                for domain in self.result[key]:
                    f.write('%s\n' % domain)
