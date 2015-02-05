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

    def start(self, domain, domain_type, level):
        super(dnszonetransfer, self).start(domain, domain_type, level)
        try:
            resolver = DnsHelper(domain)
            mx_list = resolver.get_mx()
            soa_list = resolver.get_soa()
            # issue#28: 放弃dns插件中txt记录的数据，这部分数据不能保证一定是关联IP
            # txt_list = resolver.get_txt()

            # spf_list = resolver.get_spf()
            transfer_list = resolver.zone_transfer()
        except:
            pass
        else:
            record_lists = [mx_list, soa_list]

            domains = []
            ips = []
            for record_list in record_lists:
                if record_list:
                    for record in record_list:
                        domains.append(record[1])
                        if len(record) >= 3:
                            ips.append(record[2])

            if transfer_list:
                for record in transfer_list:
                    if 'zone_server' in record:
                        ips.append(record['zone_server'])
                        if 'name' in record:
                            dns_domain = record['name']
                        elif 'mname' in record:
                            dns_domain = record['mname']
                        elif 'target' in record:
                            dns_domain = record['target']
                        else:
                            dns_domain = ''
                        if dns_domain:
                            domains.append(dns_domain)
                        if 'adderss' in record:
                            ips.append(record['address'])
                    else:
                        ips.append(record['ns_server'])

            ips = list(set(ips))
            domains = list(set(domains))
            if domains or ips:
                self.result = {
                    'root_domain': [],
                    'ip': ips,
                    'domain': domains,
                }
        super(dnszonetransfer, self).end()
        return self.result
