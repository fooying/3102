#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from attrdict import AttrDict

# task queue
task = AttrDict()
task.domains = set()
task.ips = set()
task.rootdomains = set()

# result queue
result = AttrDict()
result.domains = set()
result.ips = set()
result.rootdomains = set()

# all target
all_target = AttrDict()

# some control's switch
control = AttrDict()
control.stop = False  # if stop sched
control.max_level = 3  # max level of get ip/domain/rootdomain
control.domain_level = 0 # current level of domain
control.ip_level = 0  # current level of ip
control.rootdomain_level = 0 # current level of rootdomain
control.tmp_queue = []  # temp queue

# target type
target = AttrDict()
target.value = ''
target.type = ''
target.level = 0
target.source = ''
target.remarks = ''

first_target = target

