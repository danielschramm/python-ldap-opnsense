import json
import sys
from pprint import pprint

from pyopnsense_json import PyopnsenseJson

class OpnSenseClientUnboundDiagnostics(PyopnsenseJson):
    def dumpcache(self):
        return self._get("Unbound/Diagnostics/dumpcache")
    def dumpinfra(self):
        return self._get("Unbound/Diagnostics/dumpinfra")
    def listinsecure(self):
        return self._get("Unbound/Diagnostics/listinsecure")
    def listlocaldata(self):
        return self._get("Unbound/Diagnostics/listlocaldata")
    def listlocalzones(self):
        return self._get("Unbound/Diagnostics/listlocalzones")
    def stats(self):
        return self._get("Unbound/Diagnostics/stats")


class OpnSenseClientUnboundOverview(PyopnsenseJson):
    def Rolling(self):
        print("TODO implement parameters: $timeperiod,$clients =0 ")
        return self._get("Unbound/Overview/Rolling/...")

    def isBlockListEnabled(self):
        return self._get("Unbound/Overview/isBlockListEnabled")

    def isEnabled(self):
        return self._get("Unbound/Overview/isEnabled")

    def searchQueries(self):
        return self._get("Unbound/Overview/searchQueries")

    def totals(self, maximum):
        return self._get("Unbound/Overview/totals/" + str(maximum))


class OpnSenseClientUnboundService(PyopnsenseJson):
    def dnsbl(self):
        return self._get("Unbound/Service/dnsbl")
    def reconfigure(self):
        return self._post("Unbound/Service/reconfigure","")
    def reconfigureGeneral(self):
        return self._get("Unbound/Service/reconfigureGeneral")
    def restart(self):
        return self._post("Unbound/Service/restart","")
    def start(self):
        return self._post("Unbound/Service/start","")
    def status(self):
        return self._get("Unbound/Service/status")
    def stop(self):
        return self._post("Unbound/Service/stop","")


class OpnSenseClientUnboundSettings(PyopnsenseJson):
    def get(self):
        return self._get("Unbound/Settings/get")
    def getAcl(self, uuid):
        return self._get("Unbound/Settings/getAcl/" + uuid)
    def getDomainOverride(self, uuid=""):
        return self._get("Unbound/Settings/getDomainOverride/" + uuid)
    def getForward(self, uuid=""):
        return self._get("Unbound/Settings/getForward/" + uuid)
    def getHostAlias(self, uuid=""):
        return self._get("Unbound/Settings/getHostAlias/" + uuid)
    def getHostOverride(self, uuid=""):
        return self._get("Unbound/Settings/getHostOverride/" + uuid)
    def getNameservers(self):
        return self._get("Unbound/Settings/getNameservers")

    def searchAcl(self):
        # can be get and post
        return self._get("Unbound/Settings/searchAcl")
    def searchDomainOverride(self):
        # can be get and post
        return self._get("Unbound/Settings/searchDomainOverride")
    def searchHostAlias(self):
        # can be get and post
        return self._get("Unbound/Settings/searchHostAlias")
    def searchHostOverride(self):
        # can be get and post
        return self._get("Unbound/Settings/searchHostOverride")

    def addAcl(self):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/addAcl", "")

    def addDomainOverride(self):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/addDomainOverride", "")

    def addForward(self):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/addForward", "")

    def addHostAlias(self):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/addHostAlias", "")

    def addHostOverride(self, override):
        return self.post_json("unbound/Settings/addHostOverride/", override)

    def set(self):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/set", "")

    def updateBlocklist(self):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/updateBlocklist", "")

    def delAcl(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/delAcl/" + uuid, "")
    def delDomainOverride(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/delDomainOverride/" + uuid, "")
    def delForward(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/delForward/" + uuid, "")
    def delHostAlias(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/delHostAlias/" + uuid, "")
    def delHostOverride(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/delHostOverride/" + uuid, "")
    def setAcl(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/setAcl/" + uuid, "")
    def setDomainOverride(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/setDomainOverride/" + uuid, "")
    def setForward(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/setForward/" + uuid, "")
    def setHostAlias(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/setHostAlias/" + uuid, "")
    def setHostOverride(self, uuid=""):
        #TODO: Check if payload needed
        return self._post("Unbound/Settings/setHostOverride/" + uuid, "")

    def toggleAcl(self, uuid="", enabled=""):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/toggleAcl/" + uuid + "/" + enabled, "")
    def toggleDomainOverride(self, uuid="", enabled=""):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/toggleDomainOverride/" + uuid + "/" + enabled, "")
    def toggleForward(self, uuid="", enabled=""):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/toggleForward/" + uuid + "/" + enabled, "")
    def toggleHostAlias(self, uuid="", enabled=""):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/toggleHostAlias/" + uuid + "/" + enabled, "")
    def toggleHostOverride(self, uuid="", enabled=""):
        # TODO: Check if payload needed
        return self._post("Unbound/Settings/toggleHostOverride/" + uuid + "/" + enabled, "")


def test_connection(config_dict):
#    unbound = OpnSenseClientUnboundDiagnostics(
#        config_dict['api_key'], config_dict['api_secret'],
#        config_dict['opnsense_url'])
#    pprint(unbound.stats())
#    pprint(unbound.dumpcache())
    unbound_settings = OpnSenseClientUnboundSettings(
        config_dict['api_key'], config_dict['api_secret'],
        config_dict['opnsense_url'])
    pprint(unbound_settings.searchHostOverride())
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


