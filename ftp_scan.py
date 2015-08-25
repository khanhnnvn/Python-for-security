"""
Email: khanhnn@pythonvietnam.info
"""
import ftplib
def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print '\n[*] ' + str(hostname) +\
        ' FTP Anonymous Logon Succeeded.'
        ftp.quit()
        return True
    except Exception, e:
        print '\n[-] ' + str(hostname) +\
        ' FTP Anonymous Logon Failed.'
        return False
host = '123.29.67.123'
anonLogin(host)
