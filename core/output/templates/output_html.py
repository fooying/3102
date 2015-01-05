#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re
from textwrap import dedent
from template import Output


class OutputHtml(Output):

    def save(self, output_file):
        super(OutputHtml, self).save(output_file)
        html = self._html_generate()
        with open(output_file, 'w') as f:
            f.write(dedent(html))

    def _html_generate(self):
        tr = '<tr> <td>{{ domain }}</td> <td>{{ module }}</td> <td>{{ level }}</td> <td>{{ parent_domain }}</td> </tr>\n'
        tr_str = ''
        for key in ['root_domain', 'ip', 'domain']:
            for item in self.result[key].values():
                tr_str += self._generate_key(tr, item)
        html = self._html_base % tr_str
        return html

    def _generate_key(self, template, context):
        content = template
        for key in self._extract_vars(template):
            if key not in context:
                raise ValueError("%s is missing from the template context" % key)
            content = content.replace("{{ %s }}" % key, str(context[key]))
        return content

    def _extract_vars(self, template):
        keys = set()
        for match in re.finditer(r"\{\{ (?P<key>\w+) \}\}", template):
            keys.add(match.groups()[0])
        return sorted(list(keys))

    _html_base = """\
    <!DOCTYPE html>
    <html lang="zh-cn">
        <head>
            <meta charset="utf-8">
            <title></title>
            <style type="text/css">
            caption{padding-top:8px;padding-bottom:8px;color:#777;text-align:left}th{text-align:left}.table{width:100%%;max-width:100%%;margin-bottom:20px}.table>thead>tr>th,.table>tbody>tr>th,.table>tfoot>tr>th,.table>thead>tr>td,.table>tbody>tr>td,.table>tfoot>tr>td{padding:8px;line-height:1.42857143;vertical-align:top;border-top:1px solid #ddd}.table>thead>tr>th{vertical-align:bottom;border-bottom:2px solid #ddd}
            </style> 
        </head>
        <body>
            <div class="container">
                <table class="table">
                    <caption></caption>
                    <thead>
                        <tr>
                            <th>domain</th>
                            <th>module</th>
                            <th>level</th>
                            <th>parent_domain</th>
                        </tr>
                    </thead>
                    <tbody>
                        %s
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """
