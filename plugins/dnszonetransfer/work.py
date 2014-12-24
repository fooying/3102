#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

from core.plugin import Plugin

from dnshelper import DnsHelper


class dnszonetransfer(Plugin):
    def __init__(self):
        super(dnszonetransfer, self).__init__('dnszonetransfer')

    def start(self, target, domain_type, level):
        super(dnszonetransfer, self).start(target, domain_type, level)
        resolver = DnsHelper(target)
        mx_list = resolver.get_mx()
        soa_list = resolver.get_soa()
        txt_list = resolver.get_txt()
        spf_list = resolver.get_spf()
        transfer_list = resolver.zone_transfer()
        record_lists = [mx_list, soa_list, txt_list, spf_list]

        domains = []
        ips = []
        for record_list in record_lists:
            for record in record_list:
                domains.append(record[1])
                ips.append(record[2])

        for record in transfer_list:
            if 'zone_server' in record:
                domains.append(record['name'])
                ips.append(record['zone_server'])
                ips.append(record['address'])
            else:
                ips.append(record['ns_server'])

        ips = list(set(ips))
        domains = list(set(domains))
        if domains or ips:
            result = {
                'result': {
                    'root_domain': [],
                    'ip': ips,
                    'domain': domains,
                },
                'module': self.name,
                'parent_target': target,
                'level': level,
            }
        else:
            result = None
        super(dnszonetransfer, self).end()
        return result
