'''
This Tool For Termux in Installation Jupyter All Error Fixed.
'''
import os, sys, time

os.system("termux-wake-lock")

header = '\033[95m'
blue = '\033[94m'
green = '\033[92m'
yellow = '\033[93m'
red = '\033[91m'
white = '\033[0m'
b = '\033[1m'
cyan = '\033[36m'
ul = '\033[4m'
bheader = '\033[1;95m'
bblue = '\033[1;94m'
bgreen = '\033[1;92m'
byellow = '\033[1;93m'
bred = '\033[1;91m'
bcyan = '\033[1;36m'
backred = '\033[1;0;41m'

#---*---#
def loading():
    loader = "/|\\-"
    for x in range(100):
        time.sleep(0.1)
        sys.stdout.write("\r"+bblue+" Starting TermPyter...   "+bred + loader[x % len(loader)])
        sys.stdout.flush()
    os.system("clear")


banner = byellow+'''
             Fix All Error in Installation Jupyter'''+bgreen+'''
 _____                  ______      _            
|_   _|                 | ___ \\    | |           
  | | ___ _ __ _ __ ___ | |_/ /   _| |_ ___ _ __ 
  | |/ _ \\ '__| '_ ` _ \\|  __/ | | | __/ _ \\ '__|
  | |  __/ |  | | | | | | |  | |_| | ||  __/ |   
  \\_/\\___|_|  |_| |_| |_\\_|   \__, |\\__\___|_|   
                               __/ |             
                              |___/         tp1.0     

'''
def py():
    if open('/data/data/com.termux/files/usr/bin/python3','r'):
        time.sleep(4)
        print(bblue+"\n[√] Python        "+bgreen+'Found')
    else:
        print(bblue+'[×] Python         '+bred+'N/A')
        print(" Python Not Found.\n\tReady To Installation Python\n")
        time.sleep(3)
        os.system('apt install python -y')

def clang():
    if open('/data/data/com.termux/files/usr/bin/clang++','r'):
        time.sleep(4)
        print(bblue+"\n[√] Clang++       "+bgreen+"Found")
    else:
        print(bblue+"\n[×] Clang++        "+bred+"N/A")
        print(bblue+" Clang++ Not Found.\n\tReady To Installation Clang and Clang++\n")
        time.sleep(3)
        os.system("apt install clang -y")

def ban():
    print(banner)
    print(bgreen+"    Made By 3P1C"+bred+"         EPIC")
    print(bheader+"\n:::::::::::::::::::::::::::::::::::::::::::\n")
def instal():
    print(byellow+"\n[?] Checking Dependencies..."+white+'')
    py()
    clang()        
    print(bcyan+"\n[o] Other Dependencies Installing...\n"+white+'')       
    os.system("apt update -y")
    os.system("apt upgrade -y")   
    os.system("apt install python-dev libzmq libcrypt libzmq-dev libcrypt-dev -y")
    print(bgreen+"\n[√] Dependencies Installed...")

def jup():
    print(bcyan+"\nJupyter Installing Start...."+white+'\n')
    os.system("pip install jupyter")
    print(byellow+"\n\nType This Command →  "+white+"\tjupyter notebook"+white+'')
loading()
ban()
instal()
jup()
#print(byellow+"\n\nType This Command →  "+white+"\tjupyter notebook"+white+'')
os.system("termux-wake-unlock")
if "__int__" == "__main__":
    pass
