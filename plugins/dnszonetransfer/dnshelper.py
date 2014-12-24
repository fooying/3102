#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2013  Carlos Perez
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; Applies version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import re
import dns.query
import dns.resolver
import dns.reversename
import socket
from dns.zone import *
from dns.dnssec import algorithm_to_text


DNS_PORT_NUMBER = 53
DNS_QUERY_TIMEOUT = 4.0


class DnsHelper:
    def __init__(self, domain, ns_server=None, request_timeout=3.0, ):
        self._domain = domain
        if ns_server:
            self._res = dns.resolver.Resolver(configure=False)
            self._res.nameservers = [ns_server]
        else:
            self._res = dns.resolver.Resolver(configure=True)
        # Set timing
        self._res.timeout = request_timeout
        self._res.lifetime = request_timeout

    def check_tcp_dns(self, address):
        """
        Function to check if a server is listening at port 53 TCP. This will aid
        in IDS/IPS detection since a AXFR will not be tried if port 53 is found to
        be closed.
        """
        s = socket.socket()

        s.settimeout(DNS_QUERY_TIMEOUT)
        try:
            s.connect((address, DNS_PORT_NUMBER))
        except Exception:
            return False
        else:
            return True

    def resolve(self, target, type, ns=None):
        """
        Function for performing general resolution types returning the RDATA
        """
        if ns:
            res = dns.resolver.Resolver(configure=False)
            res.nameservers = [ns]
        else:
            res = dns.resolver.Resolver(configure=True)

        answers = res.query(target, type)
        return answers

    def get_a(self, host_trg):
        """
        Function for resolving the A Record for a given host. Returns an Array of
        the IP Address it resolves to. It will also return CNAME data.
        """
        address = []
        try:
            ipv4_answers = self._res.query(host_trg, 'A')
            for ardata in ipv4_answers.response.answer:
                for rdata in ardata:
                    if rdata.rdtype == 5:
                        address.append(["CNAME", host_trg, rdata.target.to_text()[:-1]])
                        host_trg = rdata.target.to_text()[:-1]
                    else:
                        address.append(["A", host_trg, rdata.address])
        except:
            return address
        return address

    def get_aaaa(self, host_trg):
        """
        Function for resolving the AAAA Record for a given host. Returns an Array of
        the IP Address it resolves to. It will also return CNAME data.
        """
        address = []
        try:
            ipv6_answers = self._res.query(host_trg, 'AAAA')
            for ardata in ipv6_answers.response.answer:
                for rdata in ardata:
                    if rdata.rdtype == 5:
                        address.append(["CNAME", host_trg, rdata.target.to_text()[:-1]])
                        host_trg = rdata.target.to_text()[:-1]
                    else:
                        address.append(["AAAA", host_trg, rdata.address])
        except:
            return address
        return address

    def get_ip(self, hostname):
        """
        Function resolves a host name to its given A and/or AAA record. Returns Array
        of found hosts and IPv4 or IPv6 Address.
        """
        found_ip_add = []
        found_ip_add.extend(self.get_a(hostname))
        found_ip_add.extend(self.get_aaaa(hostname))

        return found_ip_add

    def get_mx(self):
        """
        Function for MX Record resolving. Returns all MX records. Returns also the IP
        address of the host both in IPv4 and IPv6. Returns an Array
        """
        mx_records = []
        answers = self._res.query(self._domain, 'MX')
        for rdata in answers:
            try:
                name = rdata.exchange.to_text()
                ipv4_answers = self._res.query(name, 'A')
                for ardata in ipv4_answers:
                    mx_records.append(['MX', name[:-1], ardata.address,
                                      rdata.preference])
            except:
                pass
        try:
            for rdata in answers:
                name = rdata.exchange.to_text()
                ipv6_answers = self._res.query(name, 'AAAA')
                for ardata in ipv6_answers:
                    mx_records.append(['MX', name[:-1], ardata.address,
                                      rdata.preference])
            return mx_records
        except:
            return mx_records

    def get_ns(self):
        """
        Function for NS Record resolving. Returns all NS records. Returns also the IP
        address of the host both in IPv4 and IPv6. Returns an Array.
        """
        name_servers = []
        answer = self._res.query(self._domain, 'NS')
        if answer is not None:
            for aa in answer:
                name = aa.target.to_text()[:-1]
                ip_addrs = self.get_ip(name)
                for addresses in ip_addrs:
                    if re.search(r'^A', addresses[0]):
                        name_servers.append(['NS', name, addresses[2]])
        return name_servers

    def get_soa(self):
        """
        Function for SOA Record resolving. Returns all SOA records. Returns also the IP
        address of the host both in IPv4 and IPv6. Returns an Array.
        """
        soa_records = []
        answers = self._res.query(self._domain, 'SOA')
        for rdata in answers:
            name = rdata.mname.to_text()
            ipv4_answers = self._res.query(name, 'A')
            for ardata in ipv4_answers:
                soa_records.append(['SOA', name[:-1], ardata.address])

        try:
            for rdata in answers:
                name = rdata.mname.to_text()
                ipv4_answers = self._res.query(name, 'AAAA')
                for ardata in ipv4_answers:
                    soa_records.append(['SOA', name[:-1], ardata.address])

            return soa_records
        except:
            return soa_records

    def get_spf(self):
        """
        Function for SPF Record resolving returns the string with the SPF definition.
        Prints the string for the SPF Record and Returns the string
        """
        spf_record = []

        try:
            answers = self._res.query(self._domain, 'SPF')
            for rdata in answers:
                name = ''.join(rdata.strings)
                spf_record.append(['SPF', name])
        except:
            return None

        return spf_record

    def get_txt(self, target=None):
        """
        Function for TXT Record resolving returns the string.
        """
        txt_record = []
        if target is None:
            target = self._domain
        try:
            answers = self._res.query(target, 'TXT')
            for rdata in answers:
                string = "".join(rdata.strings)
                txt_record.append(['TXT', target, string])
        except:
            return []

        return txt_record

    def get_ptr(self, ipaddress):
        """
        Function for resolving PTR Record given it's IPv4 or IPv6 Address.
        """
        found_ptr = []
        n = dns.reversename.from_address(ipaddress)
        try:
            answers = self._res.query(n, 'PTR')
            for a in answers:
                found_ptr.append(['PTR', a.target.to_text()[:-1], ipaddress])
            return found_ptr
        except:
            return None

    def get_srv(self, host):
        """
        Function for resolving SRV Records.
        """
        record = []
        try:
            answers = self._res.query(host, 'SRV')
            for a in answers:
                target = a.target.to_text()
                #print a.target.to_text()
                ips = self.get_ip(target[:-1])
                if ips:
                    for ip in ips:
                        if re.search('(^A|AAAA)', ip[0]):
                            record.append(['SRV', host, a.target.to_text()[:-1], ip[2],
                                          str(a.port), str(a.weight)])

                else:
                    record.append(['SRV', host, a.target.to_text()[:-1], "no_ip",
                                  str(a.port), str(a.weight)])
        except:
            return record
        return record

    def get_nsec(self, host):
        """
        Function for querying for a NSEC record and retriving the rdata object.
        This function is used mostly for performing a Zone Walk against a zone.
        """
        answer = self._res.query(host, 'NSEC')
        return answer

    def from_wire(self, xfr, zone_factory=Zone, relativize=True):
        """
        Method for turning returned data from a DNS AXFR in to RRSET, this method will not perform a
        check origin on the zone data as the method included with dnspython
        """
        z = None
        for r in xfr:
            if z is None:
                if relativize:
                    origin = r.origin
                else:
                    origin = r.answer[0].name
                rdclass = r.answer[0].rdclass
                z = zone_factory(origin, rdclass, relativize=relativize)
            for rrset in r.answer:
                znode = z.nodes.get(rrset.name)
                if not znode:
                    znode = z.node_factory()
                    z.nodes[rrset.name] = znode
                zrds = znode.find_rdataset(rrset.rdclass, rrset.rdtype,
                                           rrset.covers, True)
                zrds.update_ttl(rrset.ttl)
                for rd in rrset:
                    rd.choose_relativity(z.origin, relativize)
                    zrds.add(rd)

        return z

    def zone_transfer(self):
        """
        Function for testing for zone transfers for a given Domain, it will parse the
        output by record type.
        """
        # if anyone reports a record not parsed I will add it, the list is a long one
        # I tried to include those I thought where the most common.

        zone_records = []
        ns_records = []

        # Find SOA for Domain
        try:
            soa_srvs = self.get_soa()
            for s in soa_srvs:
                ns_records.append(s[2])
        except:
            return

        # Find NS for Domain
        ns_srvs = []
        try:
            ns_srvs = self.get_ns()
            for ns in ns_srvs:
                ns_ip = ''.join(ns[2])
                ns_records.append(ns_ip)
        except Exception as s:
            pass

        # Remove duplicates
        ns_records = list(set(ns_records))
        # Test each NS Server
        for ns_srv in ns_records:
            if self.check_tcp_dns(ns_srv):

                try:
                    zone = self.from_wire(dns.query.xfr(ns_srv, self._domain))
                    zone_records.append({'type': 'info', 'zone_transfer': 'success', 'ns_server': ns_srv})
                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.SOA):
                        for rdata in rdataset:
                            for mn_ip in self.get_ip(rdata.mname.to_text()):
                                if re.search(r'^A', mn_ip[0]):
                                    zone_records.append({'zone_server': ns_srv, 'type': 'SOA',
                                                         'mname': rdata.mname.to_text()[:-1], 'address': mn_ip[2]})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.NS):
                        for rdata in rdataset:

                            # Check if target is only the host name or a full FQDN.
                            # If only a hostname we will appaned the domain name of the
                            # Zone being transfered.
                            target = rdata.target.to_text()
                            target_split = target.split('.')
                            appended = False
                            if len(target_split) == 1:
                                target = target + '.' + self._domain
                                appended = True

                            for n_ip in self.get_ip(target):
                                if re.search(r'^A', n_ip[0]):

                                    if appended:
                                        zone_records.append({'zone_server': ns_srv, 'type': 'NS',
                                                        'target': target, 'address': n_ip[2]})
                                    else:
                                        zone_records.append({'zone_server': ns_srv, 'type': 'NS',
                                                        'target': rdata.target.to_text()[:-1], 'address': n_ip[2]})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.TXT):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'TXT',
                                                'strings': ''.join(rdata.strings)})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.SPF):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'SPF',
                                                 'strings': ''.join(rdata.strings)})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.PTR):
                        for rdata in rdataset:
                            for n_ip in self.get_ip(rdata.target.to_text() + "." + self._domain):
                                if re.search(r'^A', n_ip[0]):
                                    zone_records.append({'zone_server': ns_srv, 'type': 'PTR',
                                                         'name': rdata.target.to_text() + "." + self._domain, 'address': n_ip[2]})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.MX):
                        for rdata in rdataset:
                            for e_ip in self.get_ip(rdata.exchange.to_text()):
                                zone_records.append({'zone_server': ns_srv, 'type': 'MX',
                                                     'name': str(name) + '.' + self._domain,
                                                     'exchange': rdata.exchange.to_text()[:-1],
                                                     'address': e_ip[2]})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.AAAA):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'AAAA',
                                                'name': str(name) + '.' + self._domain,
                                                'address': rdata.address})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.A):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'A',
                                                'name': str(name) + '.' + self._domain,
                                                'address': rdata.address})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.CNAME):
                        for rdata in rdataset:
                            for t_ip in self.get_ip(rdata.target.to_text()):
                                if re.search(r'^A', t_ip[0]):
                                    zone_records.append({'zone_server': ns_srv, 'type': 'CNAME',
                                                         'name': str(name) + '.' + self._domain,
                                                         'target': str(rdata.target.to_text())[:-1],
                                                         'address': t_ip[2]})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.SRV):
                        for rdata in rdataset:
                            ip_list = self.get_ip(rdata.target.to_text())
                            if ip_list:
                                for t_ip in self.get_ip(rdata.target.to_text()):
                                    if re.search(r'^A', t_ip[0]):
                                        zone_records.append({'zone_server': ns_srv, 'type': 'SRV',
                                                            'name': str(name) + '.' + self._domain,
                                                            'target': rdata.target.to_text()[:-1],
                                                            'address': t_ip[2],
                                                            'port': str(rdata.port),
                                                            'weight': str(rdata.weight)})
                            else:
                                zone_records.append({'zone_server': ns_srv, 'type': 'SRV',
                                                    'name': str(name) + '.' + self._domain,
                                                    'target': rdata.target.to_text()[:-1],
                                                    'address': "no_ip",
                                                    'port': str(rdata.port),
                                                    'weight': str(rdata.weight)})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.HINFO):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'HINFO',
                                                'cpu': rdata.cpu, 'os': rdata.os})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.WKS):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'WKS',
                                                'address': rdata.address, 'bitmap': rdata.bitmap,
                                                'protocol': rdata.protocol})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.RP):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'RP',
                                                'mbox': rdata.mbox.to_text(), 'txt': rdata.txt.to_text()})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.AFSDB):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'AFSDB',
                                                'subtype': str(rdata.subtype), 'hostname': rdata.hostname.to_text()})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.LOC):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'LOC',
                                                'coordinates': rdata.to_text()})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.X25):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'X25',
                                                'address': rdata.address})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.ISDN):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'ISDN',
                                                 'address': rdata.address})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.RT):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'X25',
                                                 'address': rdata.address})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.NSAP):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'NSAP',
                                                 'address': rdata.address})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.NAPTR):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'NAPTR',
                                                 'order': str(rdata.order),
                                                 'preference': str(rdata.preference),
                                                 'regex': rdata.regexp,
                                                 'replacement': rdata.replacement.to_text(),
                                                 'service': rdata.service})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.CERT):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'CERT',
                                                 'algorithm': rdata.algorithm,
                                                 'certificate': rdata.certificate,
                                                 'certificate_type': rdata.certificate_type,
                                                 'key_tag': rdata.key_tag})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.SIG):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'SIG',
                                                'algorithm': algorithm_to_text(rdata.algorithm),
                                                'expiration': rdata.expiration,
                                                'inception': rdata.inception,
                                                'key_tag': rdata.key_tag,
                                                'labels': rdata.labels,
                                                'original_ttl': rdata.original_ttl,
                                                'signature': rdata.signature,
                                                'signer': str(rdata.signer),
                                                'type_covered': rdata.type_covered})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.RRSIG):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'RRSIG',
                                                 'algorithm': algorithm_to_text(rdata.algorithm),
                                                 'expiration': rdata.expiration,
                                                 'inception': rdata.inception,
                                                 'key_tag': rdata.key_tag,
                                                 'labels': rdata.labels,
                                                 'original_ttl': rdata.original_ttl,
                                                 'signature': rdata.signature,
                                                 'signer': str(rdata.signer),
                                                 'type_covered': rdata.type_covered})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.DNSKEY):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'DNSKEY',
                                                 'algorithm': algorithm_to_text(rdata.algorithm),
                                                 'flags': rdata.flags,
                                                 'key': dns.rdata._hexify(rdata.key),
                                                 'protocol': rdata.protocol})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.DS):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'DS',
                                                'algorithm': algorithm_to_text(rdata.algorithm),
                                                'digest': dns.rdata._hexify(rdata.digest),
                                                'digest_type': rdata.digest_type,
                                                'key_tag': rdata.key_tag})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.NSEC):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'NSEC',
                                                 'next': rdata.next})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.NSEC3):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'NSEC3',
                                                 'algorithm': algorithm_to_text(rdata.algorithm),
                                                 'flags': rdata.flags,
                                                 'iterations': rdata.iterations,
                                                 'salt': dns.rdata._hexify(rdata.salt)})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.NSEC3PARAM):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'NSEC3PARAM',
                                                 'algorithm': algorithm_to_text(rdata.algorithm),
                                                 'flags': rdata.flags,
                                                 'iterations': rdata.iterations,
                                                 'salt': rdata.salt})

                    for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.IPSECKEY):
                        for rdata in rdataset:
                            zone_records.append({'zone_server': ns_srv, 'type': 'IPSECKEY',
                                                 'algorithm': algorithm_to_text(rdata.algorithm),
                                                 'gateway': rdata.gateway,
                                                 'gateway_type': rdata.gateway_type,
                                                 'key': dns.rdata._hexify(rdata.key),
                                                 'precedence': rdata.precedence})
                except Exception as e:
                    zone_records.append({'type': 'info', 'zone_transfer': 'failed', 'ns_server': ns_srv})
            else:
                zone_records.append({'type': 'info', 'zone_transfer': 'failed', 'ns_server': ns_srv})
        return zone_records


def main():
    #resolver = DnsHelper('qq.com')
    #print(resolver.get_a("www.qq.com"))
    #print(resolver.get_aaaa('baddata-cname-to-baddata-aaaa.test.dnssec-tools.org'))
    #print(resolver.get_mx())
    #print(resolver.get_ip('www.google.com'))
    #print(resolver.get_txt("3rdparty1._spf.paypal.com"))
    #print(resolver.get_ns())
    #print(resolver.get_soa())
    #print(resolver.get_txt())
    #print(resolver.get_spf())
    ##tresolver = DnsHelper('weightmans.com')
    tresolver = DnsHelper('qhu.edu.cn')
    print(tresolver.zone_transfer())


if __name__ == "__main__":
    main()
