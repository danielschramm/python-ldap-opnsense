from pprint import pprint

import macaddress

from neighbor_settings_controller_client import NeighborSettingsControllerClient


class OpnSenseConnection:
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

    def update_host(self, mac, item):
        uuid=self._get_uuid(mac)
        self.neighbor.update_item_by_uuid(uuid, item)