#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com

todo:
    1、Multi thread
    2、Automatic loading plug-ins and call function, allow the plug-in expansion
    3、Standard plug-in
    4、Progress output
    5、Code optimization
    6、Live detection module and switch
    7、Judge the format of input and output,fault-tolerant
    8、数据之间做关联，如同一个主体的icp就没必要每次都去取icp,或者是同ip的domain就没必要再去反查同ip的其他domain，因为已经进行过一次了
"""


import sys
from copy import deepcopy

from core.parser import parse
from core.data import task, result, control
from core.data import target, all_target
from comm.rootdomain import Domain
from comm.printer import *
#from plugins.dnshelper import DnsHelper
from plugins.icp import ICP
from plugins.subdomain import SubDomain
from plugins.ip2domain import Ip2Domain
from plugins.domain2ip import Domain2Ip

def start():
    parse()
    print_status('Get input...')
    print_status('Fuzzing take turns...')
    while task.domains or task.ips or task.rootdomains:
        if task.domains:
            domain = task.domains.pop()
            level = get_level(domain)
            print_status('Fuzzing %s domains[level:%s]...' % (domain, str(level+1)))
            if level < control.max_level:
                print_status('[domain2ip]Get ip by domain...')
                ip = Domain2Ip().get_value(domain)
                if ip:
                    add_ip_task(ip, level+1, 'domain2ip', remark='')
                    print_good('Get ip %s' % ip)
                print_status('[rootdomain]Get rootdomain by domain...')
                root_domain = Domain.get_root_domain(domain)
                if root_domain:
                    add_rootdomain_task(root_domain, level+1, 'rootdomain', remark='')
                    print_good('Get root_domain %s' % root_domain)
            result.domains.add(domain)

        if task.rootdomains:
            root_domain = task.rootdomains.pop()
            level = get_level(root_domain)
            print_status('Fuzzing %s rootdomains[level:%s]...' % (root_domain, str(level+1)))
            if level < control.max_level:
                ip = Domain2Ip().get_value(root_domain)
                print_status('[domain2ip]Get ip by domain...')
                if ip:
                    add_ip_task(ip, level+1, 'domain2ip', remark='')
                    print_good('Get ip %s' % ip)
                print_status('[icp]Get rootdomains by rootdomains...')
                root_domains = ICP.get_rootdomains_by_domain(root_domain)
                print_good('Get root_domain num:%s' % str(len(root_domains)))
                for rd in root_domains:
                    add_rootdomain_task(rd, level+1, 'icp', remark='')
                print_status('[subdomain]Get domains by rootdomain...')
                domains = SubDomain().get_subdomain_by_links(root_domain)
                print_good('Get domains num:%s' % str(len(domains)))
                for domain in domains:
                    add_domain_task(domain, level+1, 'subdomain', remark='')
            result.rootdomains.add(root_domain)

        if task.ips:
            ip = task.ips.pop()
            level = get_level(ip)
            print_status('Fuzzing %s ips[level:%s]...' % (ip, str(level+1)))
            if level < control.max_level:
                print_status('[ip2domain]Get domains by ip...')
                domains = Ip2Domain().get_domains_by_ip(ip)
                print_good('Get domains num:%s' % str(len(domains)))
                for domain in domains:
                    add_domain_task(domain, level+1, 'ip2domain', remark='')
            result.ips.add(ip)
    output()
    print_status('Complete Fuzzing!')



def output():
    # todo: check live
    print_status('output result...')
    with open('domains.txt', 'w') as f:
        for domain in result.domains:
            f.write('%s,%s,%s\n' % (domain, get_level(domain), get_source(domain)))
    with open('ips.txt', 'w') as f:
        for ip in result.ips:
            f.write('%s,%s,%s\n' %(ip,get_level(ip), get_source(ip)))
    with open('rootdomains.txt', 'w') as f:
        for domain in result.rootdomains:
            f.write('%s,%s,%s\n' %(domain, get_level(domain), get_source(domain)))

def get_level(value):
    value = value.replace('.', '_')
    level = all_target[value].level
    return level


def get_source(value):
    value = value.replace('.', '_')
    source = all_target[value].source
    return source


def new_target(value, value_type, level, source, remark):
    new_target = deepcopy(target)
    new_target.type = value_type
    new_target.level = level
    new_target.value = value
    new_target.source = source
    all_target[value.replace('.', '_')] = new_target
    if value not in task['%ss' % value_type]:
        task['%ss' % value_type].add(value)

def add_ip_task(value, level, source, remark=''):
    new_target(value, 'ip', level, source, remark)

def add_domain_task(value, level, source, remark=''):
    new_target(value, 'domain', level, source, remark)

def add_rootdomain_task(value, level, source, remark=''):
    new_target(value, 'rootdomain', level, source, remark)
