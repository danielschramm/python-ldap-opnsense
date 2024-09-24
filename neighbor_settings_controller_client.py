from pprint import pprint

import requests
from pyopnsense import client

from pyopnsense_json import PyopnsenseJson


class NeighborSettingsControllerClient(PyopnsenseJson):
    def get(self):
        """Return the health list."""
        return self._get("interfaces/NeighborSettings/get")

    def add_item(self, item):
        pprint(self.post_json("interfaces/NeighborSettings/addItem",item))

    def del_item_by_uuid(self, uuid):
        cmd={}
        pprint(self.post_json("interfaces/NeighborSettings/delItem/" + uuid,cmd))

    def update_item_by_uuid(self, uuid, item):
        pprint(self.post_json("interfaces/NeighborSettings/setItem/" + uuid,item))

