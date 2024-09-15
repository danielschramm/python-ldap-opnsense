from pprint import pprint

import macaddress
from ldap3 import Server, Connection, SUBTREE


def mac_to_string(mac):
    return str(mac).replace('-', ':')


class LdapServerConnection:
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
        conn.search(self.conf['ldap_start'], self.conf['ldap_search'],search_scope=SUBTREE, attributes=['cn','dhcpHWAddress','dhcpStatements','associatedDomain'])
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
                    result['etheraddr']= mac_to_string(mac)
                    result['ipaddress']=hostEntry['attributes']['dhcpStatements'][0].split()[1]
                    result['descr']=hostEntry['attributes']['cn'][0]
                    neighbor['neighbor']=result
                    pprint(neighbor)
            except:
                print("Wrong format for entry on ldap server:")
                pprint(hostEntry)
        return neighbor
