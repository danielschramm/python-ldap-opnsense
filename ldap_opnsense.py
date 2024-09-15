#!/bin/env python3
import json
import sys
from unittest.mock import DEFAULT

import macaddress
from pprint import pprint

from ldap3 import Server, Connection, SAFE_SYNC, ALL, SUBTREE

from neighbor_settings_controller_client import NeighborSettingsControllerClient

# install pyopnsense and python-ldap

def mac_to_string(mac):
    return str(mac).replace('-', ':')

class MyLdapServer:

    def __init__(self, config_data):
        self.conf=config_data
        server = Server(self.conf['ldap_url'])
        #self.ldapServer = ldap.initialize(self.conf['ldap_url'])
        #self.searchResult = self.ldapServer.search_s(self.conf['ldap_start'], ldap.SCOPE_SUBTREE,self.conf['ldap_search']
        #                                        , ['dhcpHost', 'mail'])

        conn = Connection(server, self.conf['ldap_user'], self.conf['ldap_passwd'])
        #conn = Connection(server)
        conn.bind()
        #status, result, response, _ = conn.search(self.conf['ldap_start'], self.conf['ldap_search'])
        result = conn.search(self.conf['ldap_start'], self.conf['ldap_search'],search_scope=SUBTREE, attributes=['cn','dhcpHWAddress','dhcpStatements','associatedDomain'])
        #pprint (conn.response)
        self.searchResult=conn.response

    #def refresh_data(self):
        #self.searchResult = self.ldapServer.search_s(self.conf['ldap_start'], ldap.SCOPE_SUBTREE,self.conf['ldap_search']
        #                                        , ['dhcpHost', 'mail'])


    def get_arp_list_ldap(self):
        print("Host entires found: " + str(len(self.searchResult)))
        arp_list = []
        for hostEntry in self.searchResult:
            hostname='reading failed'
            try:
                hostname= hostEntry['attributes']['cn'][0]
                mac= macaddress.MAC(hostEntry['attributes']['dhcpHWAddress'].decode("utf-8").split()[1])
                arp_list.append(mac)
            except:
                try:
                    if hostEntry['attributes']['dhcpHWAddress'] == []:
                        print("Empty HW address:" + hostname)
                    else:
                        print("Wrong format for entry on ldap server: " + hostname)
                except:
                    print("Wrong format for entry on ldap server: " + hostname)

        return arp_list

    def get_host_by_mac(self, mac):
        neighbor = {}
        result={}
        for hostEntry in self.searchResult:
            try:
                entry_mac = macaddress.MAC(hostEntry['attributes']['dhcpHWAddress'].decode("utf-8").split()[1])
                if mac == entry_mac:
                    print("Mac address match")
                    pprint(hostEntry['attributes'])
                    result['etheraddr']=mac_to_string(mac)
                    result['ipaddress']=hostEntry['attributes']['dhcpStatements'][0].split()[1]
                    result['descr']=hostEntry['attributes']['cn'][0]
                    neighbor['neighbor']=result
                    pprint(neighbor)
            except:
                print("Wrong format for entry on ldap server:")
                pprint(hostEntry)
        return neighbor

class MyOpnSense:
    def __init__(self, config_data):
        self.conf=config_data
        self.neighbor = NeighborSettingsControllerClient(self.conf['api_key'], self.conf['api_secret'], self.conf['opnsense_url'])
        self.neighbor_dict = self.neighbor.get()['neighbor']['neighbor']

    def refresh_data(self):
        self.neighbor_dict = self.neighbor.get()['neighbor']['neighbor']

    def get_arp_list_opnsense(self):
        arp_list=[]

        for key in self.neighbor_dict:
            mac= macaddress.MAC(self.neighbor_dict[key]['etheraddr'])
            arp_list.append(mac)

        return arp_list

    def add_host(self, item):
        self.neighbor.add_item(item)

    def _get_uuid(self, mac):
        for key in self.neighbor_dict:
            if mac == macaddress.MAC(self.neighbor_dict[key]['etheraddr']):
                pprint(key)
                return key
        return ""

    def del_host(self, mac):
        uuid=self._get_uuid(mac)
        self.neighbor.del_item_by_uuid(uuid)



def main(config_data) -> int:
    """Echo the input arguments to standard output"""

    #pprint(get_arp_list_ldap())
    ls=MyLdapServer(config_data)
    ldap_list=ls.get_arp_list_ldap()

    ops=MyOpnSense(config_data)
    opnsense_list=ops.get_arp_list_opnsense()

    for e in ldap_list:
        if e in opnsense_list:
            print("found in list - do update check")
        else:
            print("not found in list - need to create")
            ops.add_host(ls.get_host_by_mac(e))


    for e in opnsense_list:
        if e in ldap_list:
            #print("found in list - do nothing")
            pass
        else:
            print("not found in list - need to delete")
            ops.del_host(e)


    #pprint(get_arp_list_opnsense())
    #print(opnsense_client.get_interfaces())


    return 0

if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        pprint(config_data)
        sys.exit(main(config_data))  # next section explains the use of sys.exit
