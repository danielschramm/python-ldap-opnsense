#!/bin/env python3
import json
import sys

from pprint import pprint
from ldap_server_connection import LdapServerConnection
from opnsense_connection import OpnSenseConnection

def main(config_dict) -> int:
    """Echo the input arguments to standard output"""

    #pprint(get_arp_list_ldap())
    ls= LdapServerConnection(config_dict)
    ldap_list=ls.get_arp_list_ldap()

    #ops= OpnSenseConnection(config_dict)
    #opnsense_list=ops.get_arp_list_opnsense()

    for e in ldap_list:
        pprint(e)
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
