import ipaddress
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

        self.conn = Connection(server, self.conf['ldap_user'], self.conf['ldap_passwd'])
        #conn = Connection(server)
        self.conn.bind()
        #status, result, response, _ = conn.search(self.conf['ldap_start'], self.conf['ldap_search'])
        self.conn.search(self.conf['ldap_start'], self.conf['ldap_search'],search_scope=SUBTREE, attributes=['cn','dhcpHWAddress','dhcpStatements','associatedDomain','aRecord'])
        #pprint (conn.response)
        self.searchResult=self.conn.response

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

    def get_hosts_list(self):
        print("Host entires found: " + str(len(self.searchResult)))
        hosts_list = []
        for entry in self.searchResult:
            pprint(entry)
            host = {}
            try:
                host['aRecord'] = ipaddress.ip_address(
                    entry['attributes']['aRecord'][0])
            except:
                pass
            try:
                host['associatedDomains']=entry['attributes']['associatedDomain']
            except:
                pass
            try:
                for statement in entry['attributes']['dhcpStatements']:
                    if statement.split(' ')[0] == 'fixed-address':
                        host[statement.split(' ')[0]]=ipaddress.ip_address(statement.split(' ')[1])
                    else:
                        host[statement.split(' ')[0]] = statement.split(' ')[1]
            except:
                pass
            try:
                host['dhcpHWAddress']=macaddress.MAC(
                    entry['attributes']['dhcpHWAddress'].decode('utf-8').split(' ')[1])
            except:
                pass
            hosts_list.append(host)
        return hosts_list

    def get_dhcp_dn_list(self):
        return self.conf['ldap_dhcp_config_dn_list']

    def get_dhcp_config(self, config_dn):
        self.conn.search(config_dn, "(objectClass=dhcpOptions)", search_scope=SUBTREE,
                         attributes=['cn', 'dhcpNetMask', 'dhcpStatements', 'dhcpOption', 'dhcpRange', 'dhcpHostDN'])
        return self.conn.response[0]['attributes']

    def get_dhcp_hosts_subnet(self, subnet_dn):
        self.conn.search(subnet_dn, "(objectClass=dhcpHost)", search_scope=SUBTREE,
                         attributes=['cn', 'associatedDomain', 'aRecord', 'dhcpHWAddress', 'dhcpStatements', 'dhcpHostDN'])
        return self.conn.response


