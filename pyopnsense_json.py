
# extend python opnsense liibrary for post via json.
# issue described here:
# https://github.com/mtreinish/pyopnsense/pull/25

import requests
from pyopnsense import client

class PyopnsenseJson(client.OPNClient):
    def post_json(self, endpoint, data):
        req_url = "{}/{}".format(self.base_url, endpoint)
        response = requests.post(
            req_url,
            json=data,
            verify=self.verify_cert,
            auth=(self.api_key, self.api_secret),
            timeout=self.timeout,
        )
