# python-ldap-opnsense
Script to push host data (DHCP, DNS) from Ldap to OpnSense via API.

Package dependencies - versions are just for info for a known working setup:
* python 3.12
* pyopnsense 0.4.0
* macaddress 2.0.2
  * Not django-macaddress
* ldap3 2.9.1
  * python-ldap is not reliable to install on windows or exotic targets.
