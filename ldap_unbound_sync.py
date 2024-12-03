#!/bin/env python3
import json
import sys
from operator import truediv

from pprint import pprint
from ldap_server_connection import LdapServerConnection
from opnsense_client_unbound import OpnSenseClientUnboundSettings


#{'description': '',
#           'domain': 'pinguin.internal',
#           'enabled': '1',
#           'hostname': 'arbeit',
#           'mx': '',
#           'mxprio': '',
#           'rr': 'A (IPv4 address)',
#           'server': '10.10.10.15',
#           'uuid': '59a973b0-cb82-4fd2-9746-8e5e53bbc66c'}

def to_host_overrides(ldap_result):
    ip = None
    overrides = []
    for i in range(len(ldap_result['associatedDomains'])):
        try:
            if ldap_result['aRecord'].version == 4:
                rr = 'A'
                ip = ldap_result['aRecord']
                try:
                    if ldap_result['fixed_address'].version == 4:
                        if ip != ldap_result['fixed_address']:
                            print("IP mismatch in ldap entry for: " + ldap_result['associatedDomains'][i])
                except:
                    pass  # no need for redundant ip entry
            elif ldap_result['aRecord'].version == 6:
                rr = 'AAA'

            hostname = ldap_result['associatedDomains'][i].split('.')[0]
            domainname = '.'.join(ldap_result['associatedDomains'][i].split('.')[1:])
            return_val = {
                'host': {
                    'enabled': '1',
                    'hostname': hostname,
                    'domain': domainname,
                    'mx': '',
                    'mxprio': '',
                    'rr': rr,
                    'server': str(ip),
                    'description': ''
                }
            }
            overrides.append(return_val)
        except:
            print("No aRecord or other error for host: " + ldap_result['associatedDomains'][i])
    return overrides


def compare_overrides(first, second):
    return_value = True
    compare_attributes = ['domain', 'hostname', 'enabled', 'server']
    for ca in compare_attributes:
        if first[ca] != second[ca]:
            return_value = False
    return return_value


def main(config_dict) -> int:
    """Echo the input arguments to standard output"""

    print("Open LDAP Connection:")
    #pprint(get_arp_list_ldap())
    ls = LdapServerConnection(config_dict)
    ldap_list = ls.get_hosts_list()

    ldap_overrides = []
    for e in ldap_list:
        for override in to_host_overrides(e):
            ldap_overrides.append(override)

    print("Open OpnSense Connection:")

    ops = OpnSenseClientUnboundSettings(config_dict['api_key'], config_dict['api_secret'],
                                        config_dict['opnsense_url'])
    opnsense_overrides = ops.searchHostOverride()['rows']



    # check for entries to delete
    for oo in opnsense_overrides:
        found = False
        for lo in ldap_overrides:
            if compare_overrides(oo, lo['host']):
                found = True
        if not found:
            print("delete " + oo['hostname'])
            ops.delHostOverride(oo['uuid'])

    #check for add entries
    opnsense_overrides = ops.searchHostOverride()['rows']
    for lo in ldap_overrides:
        found = False
        for oo in opnsense_overrides:
            if compare_overrides(oo, lo['host']):
                found = True
        if not found:
            print("add: " + lo['host']['hostname'])
            ops.addHostOverride(lo)

    # remove duplicates
    found_duplicate = True
    while found_duplicate:
        found_duplicate = False
        opnsense_overrides = ops.searchHostOverride()['rows']
        i = 0
        while (i < (len(opnsense_overrides))-2) and not found_duplicate:
            for c in range(i+1, len(opnsense_overrides)):
                if compare_overrides(opnsense_overrides[i], opnsense_overrides[c] ):
                    print("delete " + opnsense_overrides[c]['uuid'])
                    ops.delHostOverride(opnsense_overrides[c]['uuid'])
                    found_duplicate = True
                if not found_duplicate:
                    i = i + 1

    return 0


if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        pprint(config_data)
        sys.exit(main(config_data))  # next section explains the use of sys.exit
