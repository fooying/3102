#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from template import Output


class OutputCsc(Output):

    def save(self, output_file):
        super(OutputCsv, self).save(output_file)
        with open(output_file, 'w') as f:
            f.write('domain,module,level,parent_domain\n')
            for key in ['root_domain', 'ip', 'domain']:
                for item in self.result[key].values():
                    domain = item['domain']
                    module = item['module']
                    level = item['level']
                    parent_domain = item['parent_domain']
                    f.write('%s,%s,%s,%s\n' % (domain, module, level, parent_domain))
