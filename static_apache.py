#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       Title: Apache Visitor Statistics
import os

os.system("clear")
''' banner section '''
banner = '''
         #########################################
         # Server Statistics                     #
         #########################################
         '''

print banner
''' hostname '''
os.system("hostname")
print "-" * 20
''' total unique hits '''
print "Total Unique Hits: "
os.system("cat /var/log/apache2/access.log |awk '{print $1}' | sort | uniq | wc -l")
print "-" * 20
''' total hits '''
print "Total Hits: "
os.system("cat /var/log/apache2/access.log | wc -l")
print "-" * 20
''' total unique referrers '''
print "Unique Referrers: "
os.system("cat /var/log/apache2/access.log | awk '{print $11};' | awk -F / '{print $3}' | sort | uniq")
print "-" * 20
print "Currently Active Connections on port 80: "
os.system("netstat -plan|grep :80|awk {'print $5'}|cut -d: -f 1|sort|uniq -c|sort -nk 1")
print "-" * 20
print "Currently Active Connections on port 443: "
os.system("netstat -plan|grep :443|awk {'print $5'}|cut -d: -f 1|sort|uniq -c|sort -nk 1")