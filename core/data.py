#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from thirdparty.attrdict import AttrDict
import logging

# 配置存储
conf = AttrDict()
conf.plugins_available = AttrDict()  # 可用的插件列表
conf.plugins_load = AttrDict()       # 加载使用的插件配置
conf.reg_plugins = AttrDict()
conf.reg_plugins.domain = set([])
conf.reg_plugins.root_domain = set([])
conf.reg_plugins.ip = set([])
conf.max_level = 10
conf.output_format = None
conf.domain = None
conf.plugin_controller = None

# 中间数据存储
kb = AttrDict()
# 用于存储插件的信息,如import的方法等
kb.plugins = AttrDict()

# 用于存储全局的状态信息
kb.status = AttrDict()
kb.status.level = 0  # 当前进行层级
kb.status.result_num = 0  # 结果数

# 用于存储每个任务的进度详情
kb.progress = AttrDict()

# 全局接口
api = AttrDict()
api.request = None
api.logger = logging.getLogger("3102")

# 结果存储
result = AttrDict()
result.domain = AttrDict()
result.ip = AttrDict()
result.root_domain = AttrDict()

# paths
paths = AttrDict()

# cmdline options
cmdLineOptions = AttrDict()
