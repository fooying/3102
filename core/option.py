#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import ConfigParser 

from core.data import paths, options
from comm.utils import getUnicode, checkFile
from core.parser import parseCmdOptions


DEFAULTS_OPTIONS = {
    'plugins_specific': None,
    'max_level': 4,
    'timeout': 10,
    'pool_size': 500,
    'output_format': 'csv',
    'output_file': None,
    'log_file': None,
    'log_level': 1,
    'proxy_file': None,
    'verify_proxy': False,
    'alive_check': False,
}

def _isDefaultOption(cmdOptions, option):
    return cmdOptions[option] == DEFAULTS_OPTIONS[option]

def initOptions():
    cmdOptions = parseCmdOptions()
    _mergeConfOptions(cmdOptions)
    options.update(cmdOptions)

def _mergeConfOptions(cmdOptions):
    configFile = paths.CONFIG_FILE_PATH
    try:
        # 检查配置文件是否存在
        checkFile(configFile)
        # 检查配置文件格式合法性
        config = ConfigParser.ConfigParser()
        config.read(configFile)
    except Exception, ex:
        # FIXME: 这里是 抛出异常,退出程序 还是 提示,然后以默认参数运行会比较好?
        errMsg = "Invalid/Unreadable configuration file : '%s'" % getUnicode(ex)
        raise Exception(errMsg)

    for section in config.sections():
        for option in config.options(section):
            val = config.get(section, option)
            if val and _isDefaultOption(cmdOptions, option):
                # 字符列表的配置
                if option == 'plugins_specific':
                    val = val.split()
                # 整型的配置
                elif option in ('max_level', 'pool_size', 'timeout', 'log_level'):
                    val = int(val)
                # 布尔型的配置
                elif option in ('alive_check', 'verify_proxy'):
                    if val.lower() == 'false':
                        val = False
                    elif val.lower() == 'true':
                        val = True
                    else:
                        # FIXME: 这里是 抛出异常 还是 容错较高地把值设为默认值好呢?
                        errMsg = "Invalid configuration option : '%s'='%s'" % (option, val)
                        raise Exception(errMsg)

                cmdOptions[option] = val
