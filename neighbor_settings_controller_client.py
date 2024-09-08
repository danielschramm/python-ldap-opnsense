from pprint import pprint

import requests
from pyopnsense import client


class NeighborSettingsControllerClient(client.OPNClient):
    """A client for interacting with the interfaces/NeighborSettings endpoint.

    :param str api_key: The API key to use for requests
    :param str api_secret: The API secret to use for requests
    :param str base_url: The base API endpoint for the OPNsense deployment
    :param int timeout: The timeout in seconds for API requests
    """

    def get(self):
        """Return the health list."""
        return self._get("interfaces/NeighborSettings/get")

    def _post_json(self, endpoint, data):
        req_url = "{}/{}".format(self.base_url, endpoint)
        response = requests.post(
            req_url,
            json=data,
            verify=self.verify_cert,
            auth=(self.api_key, self.api_secret),
            timeout=self.timeout,
        )
        return self._process_response(response)

    def add_item(self, item):
        pprint(self._post_json("interfaces/NeighborSettings/addItem",item))

    def del_item_by_uuid(self, uuid):
        cmd={}
        pprint(self._post_json("interfaces/NeighborSettings/delItem/" + uuid,cmd))
