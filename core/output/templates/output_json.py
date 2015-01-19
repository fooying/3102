#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import json

from template import Output


class OutputJson(Output):

    def save(self, output_file):
        super(OutputJson, self).save(output_file)
        with open(output_file, 'w') as f:
            json.dump(u'%s' % self.result, f, sort_keys=True, indent=4)
