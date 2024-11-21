#!/bin/env python3
import json
import sys

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

def to_host_override(ldap_result):
    ip=None
    try:
        if ldap_result['aRecord'].version == 4:
            rr = 'A'
            ip=ldap_result['aRecord']
            try:
                if ldap_result['fixed_address'].version == 4:
                    if ip != ldap_result['fixed_address']:
                        print("IP mismatch in ldap entry for: " + ldap_result['associatedDomain'])
            except:
                pass # no need for redundant ip entry
        elif ldap_result['aRecord'].version == 6:
            rr = 'AAA'

        hostname = ldap_result['associatedDomain'].split('.')[0]
        domainname = '.'.join(ldap_result['associatedDomain'].split('.')[1:])
        return_val= {
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
        pprint(return_val)
        return return_val
    except:
        print("No aRecord or other error for host: " + ldap_result['associatedDomain'])
    return None

def main(config_dict) -> int:
    """Echo the input arguments to standard output"""

    #pprint(get_arp_list_ldap())
    ls= LdapServerConnection(config_dict)
    ldap_list=ls.get_hosts_list()

    ops= OpnSenseClientUnboundSettings(config_dict['api_key'], config_dict['api_secret'],
        config_dict['opnsense_url'])
    #opnsense_list=ops.get_arp_list_opnsense()

    for e in ldap_list:
#        pprint(to_host_override(e))
        ops.addHostOverride(to_host_override(e))
#        if e in opnsense_list:
#            print("found in list - do update check")
#            #TODO check it update needed
#            #ops.update_host(e, ls.get_host_by_mac(e))
#        else:
#            print("not found in list - need to create")
#            #ops.add_host(ls.get_host_by_mac(e))

#    for e in opnsense_list:
#        if e in ldap_list:
#            #print("found in list - do nothing")
#            pass
#        else:
#            print("not found in list - need to delete")
#            ops.del_host(e)


    #pprint(get_arp_list_opnsense())
    #print(opnsense_client.get_interfaces())

    return 0

if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        pprint(config_data)
        sys.exit(main(config_data))  # next section explains the use of sys.exit
