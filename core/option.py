#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import ConfigParser 

from thirdparty.attrdict import AttrDict
from core.data import paths

def initOptions(inputOptions=AttrDict(), overrideOptions=False):
    _mergeOptions(inputOptions, overrideOptions)


def _mergeOptions(inputOptions, overrideOptions):
    configFile = paths.CONFIG_FILE_PATH
    config=ConfigParser.ConfigParser()
    config.read(configFile)
    for section in config.sections():
        for option in config.options(section):
            mergeOption = config.get(section, option)
            if option == 'plugins_specific':
                mergeOption = mergeOption.split()
            if mergeOption:
                inputOptions[option] = mergeOption
