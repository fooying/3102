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

def initOptions(inputOptions=AttrDict(), overrideOptions=False):
    _mergeOptions(inputOptions, overrideOptions)


def _mergeOptions(inputOptions, overrideOptions):
    configFile = paths.CONFIG_FILE_PATH
    checkFile(configFile)
    try:
        config=ConfigParser.ConfigParser()
        config.read(configFile)
    except Exception, ex:
        errMsg = "you have provided an invalid and/or unreadable configuration file ('%s')" % getUnicode(ex)
        raise Exception(errMsg)

    for section in config.sections():
        for option in config.options(section):
            mergeOption = config.get(section, option)
            if option == 'plugins_specific':
                mergeOption = mergeOption.split()
            if option == 'pool_size':
                mergeOption = int(mergeOption)
            if mergeOption:
                inputOptions[option] = mergeOption
