import json
import sys
from pprint import pprint

import macaddress
from ldap3 import Server, Connection, SUBTREE, BASE


def mac_to_string(mac):
    return str(mac).replace('-', ':')


class LdapDhcpConfig:
    def __init__(self, config_data):
        self.conf=config_data
        server = Server(self.conf['ldap_url'])
        conn = Connection(server, self.conf['ldap_user'], self.conf['ldap_passwd'])
        conn.bind()
        for start_dn in self.conf['ldap_dhcp_config_dn']:
            conn.search(start_dn, '(objectClass=dhcpService)',
                    search_scope=BASE, attributes=['cn','dhcpOption','dhcpPrimaryDN','dhcpStatements'])
            if conn.response:
                self.dhcpService=conn.response
            conn.search(start_dn, '(objectClass=dhcpSubnet)',
                    search_scope=BASE, attributes=['cn','dhcpNetMask','dhcpHostDN','dhcpOption','dhcpPrimaryDN','dhcpRange','dhcpStatements'])
            if conn.response:
                self.dhcpSubnet=conn.response


    #def refresh_data(self):
        #self.searchResult = self.ldapServer.search_s(self.conf['ldap_start'], ldap.SCOPE_SUBTREE,self.conf['ldap_search']
        #                                        , ['dhcpHost', 'mail'])

    def get_dhcp_config(self):
        pprint(self.dhcpService)

    def get_dhcp_subnet(self):
        pprint(self.dhcpSubnet)


def test_connection(config_dict):
    ldap = LdapDhcpConfig(config_dict)
    ldap.get_dhcp_config()
    ldap.get_dhcp_subnet()

    return 0


if __name__ == '__main__':
    print("Library file. Just start for demo functionality")
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        #pprint(config_data)
        sys.exit(test_connection(config_data))  # next section explains the use of sys.exit


