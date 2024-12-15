# python-ldap-opnsense
Script to push host data (DHCP, DNS) from Ldap to OpnSense via API.

Corrently you can use the following 2 scripts to sync data:
**sync_ldap_kea.py** - synchronize host entries from LDAP to kea subnets in opensense - other DHCP settings from LDAP are currently ignored and need to be set in the Kea config.
**sync_ldap_unbound.py** - synchronize host entried from LDAP for hostname overrides in unbound.




Package dependencies - versions are just for info for a known working setup:
* python 3.12
* pyopnsense 0.4.0
* macaddress 2.0.2
  * Not django-macaddress
* ldap3 2.9.1
  * python-ldap is not reliable to install on windows or exotic targets.
