#!/data/data/com.termux/files/bin/python
import requests
import json
import sys 
import os
os.system('clear')
#Colors
bred='\033[01m''\033[31m'
clear='\033[0m'
print (bred+"""
███╗   ███╗ █████╗  ██████╗    ██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗ 
████╗ ████║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗
██╔████╔██║███████║██║         ██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝
██║╚██╔╝██║██╔══██║██║         ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝ 
██║ ╚═╝ ██║██║  ██║╚██████╗    ███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║     
╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
"""+clear)

url = "http://macvendors.co/api/"
try:
	mac_address = input(bred+"Enter target MAC Address : ")
	data = requests.get(url+mac_address).json()
	d1 = (data['result']['company'])
	d2 = (data['result']['address'])
	print (bred+"-"*50+clear)
	print (bred+"MAC Vendor\'s Name :",d1+clear)
	print (bred+"-"*50+clear)
	print (bred+"MAC Vendor\'s Address :",d2+clear)
	print (bred+"-"*50+clear)
	print (" \n")
except KeyboardInterrupt:
	print (bred+"Exiting,Have Nice Day!"+clear)
	sys.exit(1)
except requests.exceptions.ConnectionError as e:
    print (bred+"[!]"+" Please Check Your Internet Connection!"+clear)
    sys.exit(1)
