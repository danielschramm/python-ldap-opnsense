import json
import sys
from pprint import pprint

# STATUS:
# Development of this module was stopped as Kea in OpnSense is lacking features I need.

from pyopnsense_json import PyopnsenseJson

class OpnSenseClientKeaCtrlAgent(PyopnsenseJson):
    def get(self):
        return self._get("kea/CtrlAgent/get")

class OpnSenseClientKeaDhcpv4(PyopnsenseJson):
#TODO addPeer addReservation addSubnet delPeer($uuid) delReservation($uuid)
# delSubnet($uuid) downloadReservations getPeer($uuid=null) getReservation($uuid=null)
# searchPeer searchReservation  set setPeer($uuid)
# setReservation($uuid) setSubnet($uuid) uploadReservations
    def get(self):
        return self._get("kea/Dhcpv4/get")
    def search_subnet(self, param=""):
        return self._get("kea/Dhcpv4/searchSubnet/" + param)
    def get_subnet(self, uuid=""):
        return self._get("kea/Dhcpv4/getSubnet/" + uuid)

class OpnSenseClientKeaLeases4(PyopnsenseJson):
    # complete.
    def search(self):
        return self._get("kea/Leases4/search")

class OpnSenseClientKeaService(PyopnsenseJson):
    # missing: reconfigure restart start stop
    def status(self):
        return self._get("kea/Service/status")




def test_connection(config_dict):
    kea = OpnSenseClientKeaDhcpv4(
        config_dict['api_key'], config_dict['api_secret'],
        config_dict['opnsense_url'])
    pprint(kea.get())
    pprint(kea.search_subnet())
    pprint(kea.get_subnet("b04ba618-3398-467c-a766-a009c21ce3d5"))
#    kea_agent = OpnSenseClientKeaCtrlAgent(
#        config_dict['api_key'], config_dict['api_secret'],
#        config_dict['opnsense_url'])
#    pprint(kea_agent.get())
#    kea_leases = OpnSenseClientKeaLeases4(
#        config_dict['api_key'], config_dict['api_secret'],
#        config_dict['opnsense_url'])
#    pprint(kea_leases.search())
#    kea_status = OpnSenseClientKeaService(
#        config_dict['api_key'], config_dict['api_secret'],
#        config_dict['opnsense_url'])
#    pprint(kea_status.status())

if __name__ == '__main__':
    print("Library file. Just start for demo functionality")
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        #pprint(config_data)
        sys.exit(test_connection(config_data))  # next section explains the use of sys.exit


