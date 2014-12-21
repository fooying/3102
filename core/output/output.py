#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import logging
import tempfile
import urlparse

from core.data import conf

DEFAULT_FORMAT = 'txt'
logger = logging.getLogger('3102')


class Output(object):
    def __init__(self, target, output_format=DEFAULT_FORMAT, output_file=None):
        self.output_format = output_format
        self.template_path = conf.settings.OUTPUT_TEMPLATE_PATH
        self.target = target
        self.output_file = output_file
        self.__get_tmp_output_file()

    def save(self):
        self.__deal_config()
        try:
            self.__write_result()
        except Exception, e:
            self.logger.error(str(e))
            self.logger.info(
                u'output failure, retry output by default template and path...'
            )
            self.output_format = DEFAULT_FORMAT
            self.output_file = self.output_tmp_file
            self.__write_result()

    def __deal_config(self):
        if not self.output_file:
            self.output_file = self.tmp_output_file
            self.logger.warning(
                u'Not specified result file, set to default file:[%s].'
                % self.output_tmp_file
            )
        else:
            py_file = os.path.join(
                self.template_path, 'output_%s.py' % self.output_format
            )
            pyc_file = '%sc' % py_file

            if not os.path.exists(py_file) and not os.path.exists(pyc_file):
                info = (u'The specifies format template file does not exist,'
                        'modify the default output:[%s].' % DEFAULT_FORMAT)
                self.logger.warning(info)

    def __get_tmp_output_file(self):
        target = self.target
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        file_name = urlparse.urlparse(target).hostname
        file_name = file_name.replace('.', '_')
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(temp_dir, file_name+'.txt')
        self.tmp_output_file = output_file

    def __write_result(self):
        import_template_path = '.'.join(
            os.path.split(conf.settings.OUTPUT_TEMPLATE_OPPOSITE_PATH)
        )
        template_path = '%s.output_%s' % (
            import_template_path, self.output_format
        )
        _handle = __import__(template_path, fromlist='*')
        _report = getattr(_handle, 'Output%s' % self.output_format.capitalize())
        _report().save(self.output_file)
        if self.output_file:
            self.logger.debug(
                u'Result has been output to [%s].',
                self.output_file
            )
