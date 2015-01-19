#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from template import Output


class OutputCsv(Output):

    def save(self, output_file):
        super(OutputCsv, self).save(output_file)
        with open(output_file, 'w') as f:
            f.write(','.join(self.keys) + '\n')
            module_dict = {}
            for key in ['root_domain', 'ip', 'domain']:
                for item in self.result[key].values():
                    group = module_dict.setdefault(item['module'], [])
                    group.append(item)

            for group in module_dict:
                for item in module_dict[group]:
                    items = [item[_].replace(',', '') if _ == 'title'
                             else item[_] for _ in self.keys]
                    f.write(','.join('{}'.format(_) for _ in items) + '\n')
