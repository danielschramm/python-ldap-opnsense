#!/bin/env python3
import ipaddress
import json
import sys
from operator import truediv

from pprint import pprint
from ldap_server_connection import LdapServerConnection
from opnsense_client_kea import OpnSenseClientKeaDhcpv4
from opnsense_client_kea import OpnSenseClientKeaService
from opnsense_client_kea import OpnSenseClientKeaCtrlAgent
from opnsense_client_kea import OpnSenseClientKeaLeases4

def get_subnet_uuid(kea, subnet_name):
    subnet_list = kea.search_subnet()
    for sn in subnet_list['rows']:
        if subnet_name == sn['subnet']:
            return sn['uuid']

def get_reservations_in_subnet(kea, subnet_name):
    reservations=[]
    for host in kea.search_reservation()['rows']:
        if host['subnet'] == subnet_name:
            reservations.append(host)
    return reservations

def to_host_reservation(ldap_result, subnet_uuid):
    # reservation = {'reservation': {
    #            'description': 'huhu desc',
    #            'hostname': 'huhuhu',
    #            'hw_address': 'bb:aa:aa:aa:aa:aa',
    #            'ip_address': '172.20.0.2',
    #            'subnet': 'b04ba618-3398-467c-a766-a009c21ce3d5'
    #        }}
    ip = None
    ip_arecord=None
    ip_fixed_address=None

    try:
        ip_arecord=ipaddress.ip_address(ldap_result['aRecord'][0])
        if ip_arecord.version == 4:
            ip = ip_arecord
    except:
        print("No arecord IP found")

    try:
        for statement in ldap_result['dhcpStatements']:
            if statement.startswith('fixed_address'):
                ip_str = statement.split(' ')[1]
                ip_fixed_address = ipaddress.ip_address(ip_str)
                if ldap_result['fixed_address'].version == 4:
                    if ip != ldap_result['fixed_address']:
                        print("IP mismatch in ldap entry for: " + ldap_result['associatedDomain'][0])
                    ip = ip_fixed_address
    except:
        print("No fixed_address ip found")

    hostname = ldap_result['associatedDomain'][0].split('.')[0]
    hw_address=''
    try:
        hw_address = str(ldap_result['dhcpHWAddress']).split(' ')[1].split('\'')[0]
    except:
        print("no hw address found.")

    return_val = {
#          'reservation': {
                    'description': '',
                    'hostname': hostname,
                    'hw_address': hw_address,
                    'ip_address': str(ip),
                    'subnet': subnet_uuid
#                }
        }
    return return_val


def is_reservation_in_list(reservation, list):
    for r in list:
        if(r['hw_address'] == reservation['hw_address']
            and r['hostname'] == reservation['hostname']
            and r['ip_address'] == reservation['ip_address']):
                return True

    return False

def sync_subnet_hosts(kea, subnet_name, subnet_hosts):
    subnet_uuid = get_subnet_uuid(kea,subnet_name)
    kea_reservations = get_reservations_in_subnet(kea, subnet_name)

    # convert all ldap hosts to reservations
    ldap_reservations=[]
    for ldap_host in subnet_hosts:
        reservation = to_host_reservation(ldap_host['attributes'],subnet_uuid)
        ldap_reservations.append(reservation)

    # delete not matching entries use key IP:
    for kr in kea_reservations:
        if not is_reservation_in_list(kr,ldap_reservations):
            print("not in ldap_reservations")
            kea.del_reservation(kr['uuid'])
        else:
            print("check for deletion OK: ", kr['hostname'])

    kea_reservations = get_reservations_in_subnet(kea, subnet_name)
    # add missing entries
    for lr in ldap_reservations:
        if not is_reservation_in_list(lr, kea_reservations):
            print("add new reservation: " + lr['hostname'] + " mac: " +  lr['hw_address'] + " ip: " +  lr['ip_address'])
            new_reservation = {'reservation': lr }
            kea.add_reservation(new_reservation)
        else:
            print("check for adding OK: ", lr['hostname'])




#        kea.add_reservation(reservation)

#ldap_host entry:
#{'attributes': {'aRecord': ['172.20.10.241'], 'dhcpHWAddress': b'ethernet 30:46:9a:04:fe:c6', 'dhcpStatements': ['fixed-address 172.20.10.241'], 'cn': ['010_241_switch_CSS326-24G-2S'], 'associatedDomain': ['switch_CSS326-24G-2S.ptest.local'], 'dhcpHostDN': []},
# 'dn': 'cn=010_241_switch_CSS326-24G-2S,cn=TestNet,dc=pinguin,dc=lan',
# 'raw_attributes': {'aRecord': [b'172.20.10.241'], 'dhcpHWAddress': [b'ethernet 30:46:9a:04:fe:c6'], 'dhcpStatements': [b'fixed-address 172.20.10.241'], 'cn': [b'010_241_switch_CSS326-24G-2S'], 'associatedDomain': [b'switch_CSS326-24G-2S.ptest.local'], 'dhcpHostDN': []},
# 'raw_dn': b'cn=010_241_switch_CSS326-24G-2S,cn=TestNet,dc=pinguin,dc=lan',
# 'type': 'searchResEntry'}

def main(config_dict) -> int:
    """Echo the input arguments to standard output"""

    print("Open LDAP Connection:")
    #pprint(get_arp_list_ldap())
    ls = LdapServerConnection(config_dict)
    ldap_list = ls.get_dhcp_dn_list()

    kea = OpnSenseClientKeaDhcpv4(
        config_dict['api_key'], config_dict['api_secret'],
        config_dict['opnsense_url'])


    for e in ldap_list:
        subnet=ls.get_dhcp_config(e)
        subnet_name=str(subnet['cn'][0]) + "/" + str(subnet['dhcpNetMask'])
        pprint(subnet_name)
        pprint(subnet['dhcpHostDN'][0])
        sn_hosts=ls.get_dhcp_hosts_subnet(subnet['dhcpHostDN'][0]) # TODO extend to all entries in array
        #pprint(sn_hosts)

        sync_subnet_hosts(kea, subnet_name, sn_hosts)

    return 0

if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        pprint(config_data)
        sys.exit(main(config_data))  # next section explains the use of sys.exit

