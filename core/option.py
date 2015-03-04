#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import ConfigParser 

from thirdparty.attrdict import AttrDict
from core.data import paths
from comm.utils import getUnicode, checkFile
from config.defaults import DEFAULTS_OPTIONS
from core.parser import parseCmdOptions

def getOptions():
    options = AttrDict()
    # 载入程序员(开发人员)固定的默认值
    options.update(DEFAULTS_OPTIONS)
    
    # 载入用户定义的`.conf`配置文件中的值
    options.update(getConfOptions())

    # 载入命令行传入参数的值
    cmdOptions = parseCmdOptions()
    cleanCmdOptions = {}
    for key in cmdOptions:
        # 使用action='store_true'的选项，如果值是False的话，不更新，以`3102.conf`为准
        if cmdOptions[key] == False:
            continue
        # 去除值为None的键值对, 否则会覆盖`.conf`中读取的值
        elif cmdOptions[key] is not None:
            cleanCmdOptions[key] = cmdOptions[key]
    options.update(cleanCmdOptions)

    return options

def getConfOptions():
    configFile = paths.CONFIG_FILE_PATH
    try:
        # 检查配置文件是否存在
        checkFile(configFile)
        # 检查配置文件格式合法性
        config = ConfigParser.ConfigParser()
        config.read(configFile)
    except Exception, ex:
        errMsg = "Invalid/Unreadable configuration file : '%s'" % getUnicode(ex)
        raise Exception(errMsg)

    defaults = {}

    for section in config.sections():
        for option in config.options(section):
            val = config.get(section, option)
            if val:
                # 字符列表的配置
                if option == 'plugins_specific':
                    val = val.split()
                # 整型的配置
                if option in ('max_level', 'pool_size', 'timeout', 'log_level'):
                    val = int(val)
                # 布尔型的配置
                elif option in ('alive_check', 'verify_proxy'):
                    if val.lower() == 'false':
                        val = False
                    elif val.lower() == 'true':
                        val = True
                    else:
                        # FIXME: 这里是 抛出异常 还是 容错较高地把值设为False好呢?
                        errMsg = "Invalid configuration option : '%s'='%s'" % (option, val)
                        raise Exception(errMsg)

                defaults[option] = val

    return defaults
