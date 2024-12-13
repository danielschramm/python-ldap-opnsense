#!/bin/env python3
import json
import sys
from operator import truediv

from pprint import pprint
from ldap_server_connection import LdapServerConnection
from opnsense_client_kea import OpnSenseClientKeaDhcpv4
from opnsense_client_kea import OpnSenseClientKeaService
from opnsense_client_kea import OpnSenseClientKeaCtrlAgent
from opnsense_client_kea import OpnSenseClientKeaLeases4



def main(config_dict) -> int:
    """Echo the input arguments to standard output"""

    print("Open LDAP Connection:")
    #pprint(get_arp_list_ldap())
    ls = LdapServerConnection(config_dict)
    ldap_list = ls.get_dhcp_dn_list()

    for e in ldap_list:
        subnet=ls.get_dhcp_config(e)
        subnet_name=str(subnet['cn'][0]) + "/" + str(subnet['dhcpNetMask'])
        pprint(subnet_name)
        pprint(subnet['dhcpHostDN'][0])
        sn_hosts=ls.get_dhcp_hosts_subnet(subnet['dhcpHostDN'][0]) # TODO extend to all entries in array
        pprint(sn_hosts)

    return 0

if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        pprint(config_data)
        sys.exit(main(config_data))  # next section explains the use of sys.exit

