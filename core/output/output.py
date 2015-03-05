#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import os
import tempfile
import urlparse

from core.data import paths
from core.data import api
from core.data import options
from comm.log import CUSTOM_LOGGING
from comm.utils import getUnicode, normalizeUnicode

DEFAULT_FORMAT = 'csv'


class Output(object):

    def __init__(self, domain, output_format=DEFAULT_FORMAT, output_file=None):
        self.logger = api.logger
        self.template_path = paths.OUTPUT_TEMPLATE_PATH
        self.output_format = output_format
        self.domain = domain
        self.output_file = output_file
        self.__get_output_file()
        self.__heuristic_check_extension()
        self.__check_file_extension()

    def save(self):
        self.__deal_config()
        self.__write_result()

    @classmethod
    def get_output_formats(cls):
        formats = set([])
        file_list = os.listdir(paths.OUTPUT_TEMPLATE_PATH)
        for file_name in file_list:
            if file_name.startswith('output_'):
                output_format = file_name[7:-3] if file_name.endswith('.py')\
                    else file_name[7:-4]
                formats.add(output_format)
        return formats

    def __deal_config(self):
        py_file = os.path.join(
            self.template_path, 'output_%s.py' % self.output_format
        )
        pyc_file = '%sc' % py_file

        if not os.path.exists(py_file) and not os.path.exists(pyc_file):
            info = (u'The specifies format template file does not exist,'
                    'modify the default output: [%s]' % self.output_format)
            self.logger.warning(info)

    def __get_output_file(self):
        domain = self.domain
        if not domain.startswith(('http://', 'https://')):
            domain = 'http://' + domain
        file_name = urlparse.urlparse(domain).hostname
        file_name = file_name.replace('.', '_')
        self.__create_target_dirs()
        output_file = os.path.join(
            self.outputPath, file_name + '.' + self.output_format
        )
        if not self.output_file:
            self.output_file = output_file

    def __create_target_dirs(self):
        """
        Create the output directory.
        """

        if not os.path.isdir(paths.OUTPUT_PATH):
            try:
                if not os.path.isdir(paths.OUTPUT_PATH):
                    os.makedirs(paths.OUTPUT_PATH, 0755)
                warnMsg = "using '%s' as the output directory" % paths.OUTPUT_PATH
                self.logger.warn(warnMsg)
            except (OSError, IOError), ex:
                try:
                    tempDir = tempfile.mkdtemp(prefix="3102output")
                except Exception, _:
                    errMsg = "unable to write to the temporary directory ('%s'). " % _
                    errMsg += "Please make sure that your disk is not full and "
                    errMsg += "that you have sufficient write permissions to "
                    errMsg += "create temporary files and/or directories"
                    raise Exception(errMsg)

                warnMsg = "unable to create regular output directory "
                warnMsg += "'%s' (%s). " % (paths.OUTPUT_PATH, getUnicode(ex))
                warnMsg += "Using temporary directory '%s' instead" % tempDir
                self.logger.warn(warnMsg)

                paths.OUTPUT_PATH = tempDir

        self.outputPath = os.path.join(getUnicode(paths.OUTPUT_PATH), normalizeUnicode(getUnicode(self.domain)))

        if not os.path.isdir(self.outputPath):
            try:
                os.makedirs(self.outputPath, 0755)
            except (OSError, IOError), ex:
                try:
                    tempDir = tempfile.mkdtemp(prefix="3102output")
                except Exception, _:
                    errMsg = "unable to write to the temporary directory ('%s'). " % _
                    errMsg += "Please make sure that your disk is not full and "
                    errMsg += "that you have sufficient write permissions to "
                    errMsg += "create temporary files and/or directories"
                    raise Exception(errMsg)

                warnMsg = "unable to create output directory "
                warnMsg += "'%s' (%s). " % (options.outputPath, getUnicode(ex))
                warnMsg += "Using temporary directory '%s' instead" % tempDir
                self.logger.warn(warnMsg)

                self.outputPath = tempDir

    def __write_result(self):
        import_template_path = '.'.join(
            paths.OUTPUT_TEMPLATE_OPPOSITE_PATH.split(os.path.sep)
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

    def __heuristic_check_extension(self):
        output_formats = self.get_output_formats()
        for extension in output_formats:
            if self.output_file.endswith('.' + extension):
                self.output_format = extension
