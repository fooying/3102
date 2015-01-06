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

from config import settings
from comm.log import CUSTOM_LOGGING

DEFAULT_FORMAT = 'csv'
logger = logging.getLogger('3102')


class Output(object):
    def __init__(self, domain, output_format=DEFAULT_FORMAT, output_file=None):
        self.output_format = output_format
        self.template_path = settings.OUTPUT_TEMPLATE_PATH
        self.domain = domain
        self.output_file = output_file
        self.__get_tmp_output_file()
        self.logger = logger
        self.__check_file_extension()

    def save(self):
        self.__deal_config()
        try:
            self.__write_result()
        except Exception, e:
            self.logger.error(str(e))
            self.logger.warning(
                u'output failure, retry output by default template and path...'
            )
            self.output_file = self.tmp_output_file
            self.__write_result()

    @classmethod
    def get_output_formats(cls):
        formats = set([])
        file_list = os.listdir(settings.OUTPUT_TEMPLATE_PATH)
        for file_name in file_list:
            if file_name.startswith('output_'):
                output_format = file_name[7:-3] if file_name.endswith('.py')\
                    else file_name[7:-4]
                formats.add(output_format)
        format_str = '/'.join(formats)
        return format_str

    def __deal_config(self):
        if not self.output_file:
            self.output_file = self.tmp_output_file
            self.logger.warning(
                u'Not specified result file, set to default file: [%s]'
                % self.tmp_output_file
            )
        else:
            py_file = os.path.join(
                self.template_path, 'output_%s.py' % self.output_format
            )
            pyc_file = '%sc' % py_file

            if not os.path.exists(py_file) and not os.path.exists(pyc_file):
                info = (u'The specifies format template file does not exist,'
                        'modify the default output: [%s]' % self.output_format)
                self.logger.warning(info)

    def __get_tmp_output_file(self):
        domain = self.domain
        if not domain.startswith(('http://', 'https://')):
            domain = 'http://' + domain
        file_name = urlparse.urlparse(domain).hostname
        file_name = file_name.replace('.', '_')
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(
            temp_dir, file_name + '.' + self.output_format
        )
        self.tmp_output_file = output_file

    def __write_result(self):
        import_template_path = '.'.join(
            settings.OUTPUT_TEMPLATE_OPPOSITE_PATH.split(os.path.sep)
        )
        template_path = '%s.output_%s' % (
            import_template_path, self.output_format
        )
        _handle = __import__(template_path, fromlist='*')
        _report = getattr(
            _handle, 'Output%s' % self.output_format.capitalize()
        )
        _report().save(self.output_file)
        if self.output_file:
            self.logger.log(
                CUSTOM_LOGGING.good,
                u'Result has been output to [%s]',
                self.output_file
            )

    def __check_file_extension(self):
        extension = self.output_format
        if self.output_file and not self.output_file.endswith('.' + extension):
            self.output_file += '.' + extension
