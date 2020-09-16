#!/system/bin/sh

# Lazymux Complete Install
# ========================

echo "

 /\ \                                                            
 \ \ \         __     ____    __  __    ___ ___   __  __  __  _  
  \ \ \  __  /'__`\  /\_ ,`\ /\ \/\ \ /' __` __`\/\ \/\ \/\ \/'\ 
   \ \ \L\ \/\ \L\.\_\/_/  /_\ \ \_\ \/\ \/\ \/\ \ \ \_\ \/>  </ 
    \ \____/\ \__/.\_\ /\____\\/`____ \ \_\ \_\ \_\ \____//\_/\_\
     \/___/  \/__/\/_/ \/____/ `/___/> \/_/\/_/\/_/\/___/ \//\/_/
                                    /\___/                         
                                    \/__/

                Created by weilerwebservices@gmail.com

"

apt update
apt upgrade -y

echo '* Installing Nmap'

apt install nmap
apt install git
apt install python
apt install curl
apt install php
apt install python-dev
apt install libxml2-dev
apt install libxml2-utils
apt install libxslt-dev
apt install lynx
apt install figlet
apt install ruby
apt install nano
apt install w3m
apt install clang
apt install hydra
apt install openssl
apt install libcurl
apt install wget
apt install perl
apt install ruby
apt install ncurses-utils
apt install crunch
apt install gdb
apt install radare2
apt install ired
apt install ddrescue
apt install bin-utils
apt install yasm
apt install strace
apt install ltrace
apt install cdb
apt install hexcurse
apt install memcached
apt install llvmdb
apt install dpkg
apt install imagemagick
apt install unstable-repo
apt install hashcat
echo '###### Done'
echo "###### Type 'nmap' to start."

echo '* Installing RED HAWK'

git clone https://github.com/Tuhinshubhra/RED_HAWK
mv RED_HAWK ~
echo '###### Done'

echo '* Installing D-Tect'

git clone https://github.com/bibortone/D-Tech
mv D-TECT ~
echo '###### Done'

echo '* Installing sqlmap'
git clone https://github.com/sqlmapproject/sqlmap
mv sqlmap ~
echo '###### Done'

echo '* Installing Infoga'

python3 -m pip install requests urllib3 urlparse
git clone https://github.com/m4ll0k/Infoga
mv Infoga ~
echo '###### Done'

echo '* Installing ReconDog'

git clone https://github.com/UltimateHackers/ReconDog
mv ReconDog ~
echo '###### Done'

echo '* Installing AndroZenmap'

curl -O https://raw.githubusercontent.com/Gameye98/Gameye98.github.io/master/scripts/androzenmap.sh
mkdir -p ~/AndroZenmap
mv androzenmap.sh ~/AndroZenmap
echo '###### Done'

echo '* Installing sqlmate'

python3 -m pip install mechanize bs4 HTMLparser argparse requests urlparse2
git clone https://github.com/UltimateHackers/sqlmate
mv sqlmate ~
echo '###### Done'

echo '* Installing AstraNmap'

git clone https://github.com/Gameye98/AstraNmap
mv AstraNmap ~
echo '###### Done'

echo '* Installing WTF'

python3 -m pip bs4 requests HTMLParser urlparse mechanize argparse
git clone https://github.com/Xi4u7/wtf
mv wtf ~
echo '###### Done'

echo '* Installing Easymap'

git clone https://github.com/Cvar1984/Easymap
mv Easymap ~
cd ~/Easymap
sh install.sh
echo '###### Done'

echo '* Installing XD3v'

curl -k -O https://gist.github.com/Gameye98/92035588bd0228df6fb7fa77a5f26bc2/raw/f8e73cd3d9f2a72bd536087bb6ba7bc8baef7d1d/xd3v.sh
mv xd3v.sh ~/../usr/bin/xd3v
chmod +x ~/../usr/bin/xd3v
echo '###### Done'
echo "###### Type 'xd3v' to start."

echo '* Installing Crips'

git clone https://github.com/Manisso/Crips
mv Crips ~
echo '###### Done'

echo '* Installing SIR'

python3 -m pip install bs4 urllib2
git clone https://github.com/AeonDave/sir.git
mv sir ~
echo '###### Done'

echo '* Installing Xshell'

git clone https://github.com/Ubaii/Xshell
mv Xshell ~
echo '###### Done'

echo '* Installing EvilURL'

git clone https://github.com/UndeadSec/EvilURL
mv EvilURL ~
echo '###### Done'

echo '* Installing Striker'

git clone https://github.com/UltimateHackers/Striker
mv Striker ~
cd ~/Striker
python3 -m pip install -r requirements.txt
echo '###### Done'

echo '* Installing DSSS'

git clone https://github.com/stamparm/DSSS
mv DSSS ~
echo '###### Done'

echo '* Installing SQLiv'

git clone https://github.com/Hadesy2k/sqliv
mv sqliv ~
echo '###### Done'

echo '* Installing sqlscan'

git clone http://www.github.com/Cvar1984/sqlscan
mv sqlscan ~
echo '###### Done'

echo '* Installing Wordpresscan'

git clone https://github.com/swisskyrepo/Wordpresscan
mv Wordpresscan ~
cd ~/Wordpresscan
python3 -m pip install -r requirements.txt
echo '###### Done'

echo '* Installing WPScan'

git clone https://github.com/wpscanteam/wpscan
mv wpscan ~
cd ~/wpscan
gem install bundle
bundle config build.nokogiri --use-system-libraries
bundle install
ruby wpscan.rb --update
echo '###### Done'

echo '* Installing wordpresscan(2)'

git clone https://github.com/silverhat007/termux-wordpresscan
cd termux-wordpresscan
chmod +x *
sh install.sh
mv termux-wordpresscan ~
echo '###### Done'
echo "###### Type 'wordpresscan' to start."

echo '* Installing Routersploit'

python3 -m pip install requests
git clone https://github.com/reverse-shell/routersploit
mv routersploit ~;cd ~/routersploit;python3 -m pip install -r requirements.txt;termux-fix-shebang rsf.py
echo '###### Done'

echo '* Installing Torshammer'

git clone https://github.com/dotfighter/torshammer
mv torshammer ~
echo '###### Done'

echo '* Installing Slowloris'

git clone https://github.com/gkbrk/slowloris
mv slowloris ~
echo '###### Done'

echo '* Installing Fl00d & Fl00d2'

mkdir -p ~/fl00d
curl -O https://raw.githubusercontent.com/Gameye98/Gameye98.github.io/master/scripts/fl00d.py
curl -O https://raw.githubusercontent.com/Gameye98/Gameye98.github.io/master/scripts/fl00d2.py
mv fl00d.py ~/fl00d
mv fl00d2.py ~/fl00d
echo '###### Done'

echo '* Installing GoldenEye'

git clone https://github.com/jseidl/GoldenEye
mv GoldenEye ~
echo '###### Done'

echo '* Installing Xerxes'

git clone https://github.com/zanyarjamal/xerxes
mv xerxes ~
cd ~/xerxes
clang xerxes.c -o xerxes
echo '###### Done'

echo '* Installing Planetwork-DDOS'

git clone https://github.com/Hydra7/Planetwork-DDOS
mv Planetwork-DDOS ~
echo '###### Done'

echo '* Installing Hydra'

echo '###### Done'

echo '* Installing Black Hydra'

git clone https://github.com/Gameye98/Black-Hydra
mv Black-Hydra ~
echo '###### Done'

echo '* Installing Cupp'

git clone https://github.com/Mebus/cupp
mv cupp ~
echo '###### Done'

echo '* Installing ASU'

python3 -m pip install requests bs4 mechanize
git clone https://github.com/LOoLzeC/ASU
mv ASU ~
echo '###### Done'

echo '* Installing Hash-Buster'

git clone https://github.com/UltimateHackers/Hash-Buster
mv Hash-Buster ~
echo '###### Done'

echo '* Installing InstaHack'

python3 -m pip install requests
git clone https://github.com/avramit/instahack
mv instahack ~
echo '###### Done'

echo '* Installing indonesian-wordlist'

git clone https://github.com/geovedi/indonesian-wordlist
mv indonesian-wordlist ~
echo '###### Done'

echo '* Installing Facebook Brute Force 3'

python3 -m pip install mechanize
curl -O https://raw.githubusercontent.com/Gameye98/Gameye98.github.io/master/scripts/facebook3.py
curl -O https://raw.githubusercontent.com/Gameye98/Gameye98.github.io/master/wordlist/password.txt
mkdir -p ~/facebook-brute-3
mv facebook3.py ~/facebook-brute-3
mv password.txt ~/facebook-brute-3
echo '###### Done'

echo '* Installing Webdav'

python3 -m pip install urllib3 chardet certifi idna requests
mkdir -p ~/webdav
curl -k -O http://override.waper.co/files/webdav.txt;mv webdav.txt ~/webdav/webdav.py
echo '###### Done'

echo '* Installing xGans'

mkdir -p ~/xGans
curl -O http://override.waper.co/files/xgans.txt
mv xgans.txt ~/xGans/xgans.py
echo '###### Done'

echo '* Installing Webdav Mass Exploiter'

python3 -m pip install requests
curl -k -O https://pastebin.com/raw/K1VYVHxX
mv K1VYVHxX webdav.py
mkdir -p ~/webdav-mass-exploit
mv webdav.py ~/webdav-mass-exploit
echo '###### Done'

echo '* Installing WPSploit'

git clone git clone https://github.com/m4ll0k/wpsploit
mv wpsploit ~
echo '###### Done'

echo '* Installing sqldump'

python3 -m pip install google
curl -k -O https://gist.githubusercontent.com/Gameye98/76076c9a282a6f32749894d5368024a6/raw/6f9e754f2f81ab2b8efda30603dc8306c65bd651/sqldump.py
mkdir -p ~/sqldump
chmod +x sqldump.py
mv sqldump.py ~/sqldump
echo '###### Done'

echo '* Installing Websploit'

python3 -m pip install scapy
git clone https://github.com/The404Hacking/websploit
mv websploit ~
echo '###### Done'

echo '* Installing sqlokmed'

python3 -m pip install urllib2
git clone https://github.com/Anb3rSecID/sqlokmed
mv sqlokmed ~
echo '###### Done'

echo '* Installing zones'

git clone https://github.com/Cvar1984/zones
mv zones ~
echo '###### Done'

echo '* Installing Metasploit'

wget https://gist.githubusercontent.com/Gameye98/d31055c2d71f2fa5b1fe8c7e691b998c/raw/09e43daceac3027a1458ba43521d9c6c9795d2cb/msfinstall.sh
mv msfinstall.sh ~;cd ~;sh msfinstall.sh
echo '###### Done'
echo "###### Type 'msfconsole' to start."

echo '* Installing Commix'

git clone https://github.com/commixproject/commix
mv commix ~
echo '###### Done'

echo '* Installing Brutal'

git clone https://github.com/Screetsec/Brutal
mv Brutal ~
echo '###### Done'

echo '* Installing A-Rat'

git clone https://github.com/Xi4u7/A-Rat
mv A-Rat ~
echo '###### Done'

echo '* Installing KnockMail'

python3 -m pip install validate_email pyDNS
git clone https://github.com/4w4k3/KnockMail
mv KnockMail ~
echo '###### Done'

echo '* Installing Spammer-Grab'

python3 -m pip install requests
git clone https://github.com/p4kl0nc4t/spammer-grab
mv spammer-grab ~
echo '###### Done'

echo '* Installing Hac'

git clone https://github.com/Cvar1984/Hac
mv Hac ~
echo '###### Done'

echo '* Installing Spammer-Email'

python3 -m pip install argparse requests
git clone https://github.com/p4kl0nc4t/Spammer-Email
mv Spammer-Email ~
echo '###### Done'

echo '* Installing Rang3r'

python3 -m pip install optparse termcolor
git clone https://github.com/floriankunushevci/rang3r
mv rang3r ~
echo '###### Done'

echo '* Installing SH33LL'

git clone https://github.com/LOoLzeC/SH33LL
mv SH33LL ~
echo '###### Done'

echo '* Installing Social-Engineering'

git clone https://github.com/LOoLzeC/social-engineering
mv social-engineering ~
echo '###### Done'

echo '* Installing SpiderBot'

git clone https://github.com/Cvar1984/SpiderBot
mv SpiderBot ~
echo '###### Done'

echo '* Installing Ngrok'

git clone https://github.com/themastersunil/ngrok
mv ngrok ~
echo '###### Done'

echo '* Installing sudo'

git clone https://github.com/st42/termux-sudo
mv termux-sudo ~
cd ~/termux-sudo
chmod 777 *
cat sudo > /data/data/com.termux/files/usr/bin/sudo
chmod 700 /data/data/com.termux/files/usr/bin/sudo
echo '###### Done'

echo '* Installing Ubuntu'

git clone https://github.com/Neo-Oli/termux-ubuntu
mv termux-ubuntu ~
cd ~/termux-ubuntu
bash ubuntu.sh
echo '###### Done'

echo '* Installing Fedora'

wget https://raw.githubusercontent.com/nmilosev/termux-fedora/master/termux-fedora.sh
mv termux-fedora.sh ~
echo '###### Done'

echo '* Installing Kali NetHunter'

git clone https://github.com/Hax4us/Nethunter-In-Termux
mv Nethunter-In-Termux ~
echo '###### Done'

echo '* Installing BlackBox'

python3 -m pip install optparse passlib
git clone https://github.com/jothatron/blackbox
mv blackbox ~
echo '###### Done'

echo '* Installing XAttacker'

cpnm install HTTP::Request
cpnm install LWP::Useragent
git clone https://github.com/Moham3dRiahi/XAttacker
mv XAttacker ~
echo '###### Done'

echo '* Installing VCRT'


git clone https://github.com/LOoLzeC/Evil-create-framework
mv Evil-create-framework ~
echo '###### Done'

echo '* Installing SocialFish'

python3 -m pip install wget
git clone https://github.com/UndeadSec/SocialFish
mv SocialFish ~
echo '###### Done'

echo '* Installing ECode'

git clone https://github.com/Cvar1984/Ecode
mv Ecode ~
echo '###### Done'

echo '* Installing Hashzer'

python3 -m pip install requests
git clone https://github.com/Anb3rSecID/Hashzer
mv Hashzer ~
echo '###### Done'

echo '* Installing XSStrike'

python3 -m pip install fuzzywuzzy prettytable mechanize HTMLParser
git clone https://github.com/UltimateHackers/XSStrike
mv XSStrike ~
echo '###### Done'

echo '* Installing Breacher'

python3 -m pip install requests argparse
git clone https://github.com/UltimateHackers/Breacher
mv Breacher ~
echo '###### Done'

echo '* Installing Termux-Styling'

git clone https://github.com/BagazMukti/Termux-Styling-Shell-Script
mv Termux-Styling-Shell-Script ~
echo '###### Done'

echo '* Installing TXTool'

python3 -m pip install requests
git clone https://github.com/kuburan/txtool
mv txtool ~
echo '###### Done'

echo '* Installing PassGen'

git clone https://github.com/Cvar1984/PassGen
mv PassGen ~
echo '###### Done'

echo '* Installing OWScan'

git clone https://github.com/Gameye98/OWScan
mv OWScan ~
echo '###### Done'

echo '* Installing santet-online'

python3 -m pip install requests
git clone https://github.com/Gameye98/santet-online
mv santet-online ~
echo '###### Done'

echo '* Installing SpazSMS'

python3 -m pip install requests
git clone https://github.com/Gameye98/SpazSMS
mv SpazSMS ~
echo '###### Done'

echo '* Installing Hasher'

python3 -m pip install passlib binascii progressbar
git clone https://github.com/ciku370/hasher
mv hasher ~
echo '###### Done'

echo '* Installing Hash-Generator'

python3 -m pip install passlib progressbar
git clone https://github.com/ciku370/hash-generator
mv hash-generator ~
echo '###### Done'

echo '* Installing ko-dork'

python3 -m pip install urllib2
git clone https://github.com/ciku370/ko-dork
mv ko-dork ~
echo '###### Done'

echo '* Installing snitch'

git clone https://github.com/Smaash/snitch
mv snitch ~
echo '###### Done'

echo '* Installing OSIF'

python3 -m pip install requests
git clone https://github.com/ciku370/OSIF
mv OSIF ~
echo '###### Done'

echo '* Installing nk26'

git clone 
mv nk26 ~
echo '###### Done'

echo '* Installing Devploit'

python3 -m pip install urllib2
git clone https://github.com/joker25000/Devploit
mv Devploit ~
echo '###### Done'

echo '* Installing Hasherdotid'

git clone https://github.com/galauerscrew/hasherdotid
mv hasherdotid ~
echo '###### Done'

echo '* Installing Namechk'

git clone https://github.com/HA71/Namechk
mv Namechk ~
echo '###### Done'

echo '* Installing xl-py'

git clone https://github.com/albertoanggi/xl-py
mv xl-py ~
echo '###### Done'

echo '* Installing Beanshell'

wget https://github.com/amsitlab/amsitlab.github.io/raw/master/dists/termux/amsitlab/binary-all/beanshell_2.04_all.deb
dpkg -i beanshell_2.04_all.deb
rm beanshell_2.04_all.deb
echo '###### Done'
echo "###### Type 'bsh' to start."

echo '* Installing MSF-Pg'

git clone https://github.com/haxzsadik/MSF-Pg
mv MSF-Pg ~
echo "###### Done"

echo '* Installing Crunch'

echo "###### Done"
echo "###### Type 'crunch' to start."

echo '* Installing WebConn'

git clone https://github.com/SkyKnight-Team/WebConn
mv WebConn ~
echo "###### Done"

echo '* Installing Binary Exploitation'

echo "###### Done"
echo "###### Tutorial: https://youtu.be/3NTXFUxcKPc"

echo '* Installing Textr'

wget https://raw.githubusercontent.com/amsitlab/textr/master/textr_1.0_all.deb
dpkg -i textr_1.0_all.deb
rm textr_1.0_all.deb
echo '###### Done'
echo "###### Type 'textr' to start."

echo '* Installing ApSca'

wget https://raw.githubusercontent.com/BlackHoleSecurity/apsca/master/apsca_0.1_all.deb
dpkg -i apsca_0.1_all.deb
rm apsca_0.1_all.deb
echo '###### Done'
echo "###### Type 'apsca' to start."

echo '* Installing amox'

wget https://gitlab.com/dtlily/amox/raw/master/amox_1.0_all.deb
dpkg -i amox_1.0_all.deb
rm amox_1.0_all.deb
echo '###### Done'
echo "###### Type 'amox' to start."

echo '* Installing FaDe'

python3 -m pip install requests
git clone https://github.com/Gameye98/FaDe
mv FaDe ~
echo '###### Done'

echo '* Installing GINF'

git clone https://github.com/Gameye98/GINF
mv GINF ~
echo '###### Done'

echo '* Installing AUXILE'

python3 -m pip install requests bs4 pexpect
git clone https://github.com/CiKu370/AUXILE
mv AUXILE ~
echo '###### Done'

echo '* Installing inther'

git clone https://github.com/Gameye98/inther
mv inther ~
echo '###### Done'

echo '* Installing HPB'

wget https://raw.githubusercontent.com/Cvar1984/HPB/master/html_0.1_all.deb
dpkg -i html_0.1_all.deb
rm html_0.1_all.deb
echo '###### Done'
echo "###### Type 'hpb' to start."

echo '* Installing FMBrute'

python -m pip install requests
git clone https://github.com/BlackHoleSecurity/FMBrute
mv FMBrute ~
echo '###### Done'

echo '* Installing HashID'

python3 -m pip install hashid
echo "###### Done"
echo "###### Type 'hashid -h' to show usage of hashid"

echo '* Installing GPS Tracking'

git clone https://github.com/indosecid/gps_tracking
mv gps_tracking ~
echo "###### Done"

echo '* Installing PRET'

python3 -m pip install colorama pysnmp
git clone https://github.com/RUB-NDS/PRET
mv PRET ~
echo "###### Done"

echo '* Installing AutoVisitor'

git clone https://github.com/wannabeee/AutoVisitor
mv AutoVisitor ~
echo "###### Done"

echo '* Installing Atlas'

python3 -m pip install urllib2
git clone https://github.com/m4ll0k/Atlas
mv Atlas ~
echo "###### Done"

echo '* Installing Hashcat'

echo "###### Done"
echo "###### Type 'hashcat' to start."

echo '* Installing LiteOTP'

wget https://raw.githubusercontent.com/Cvar1984/LiteOTP/master/build/main.phar -O $PREFIX/bin/lite
echo "###### Done"
echo "###### Type 'lite' to start."

echo '* Installing FBBrute'

python -m pip install requests
git clone https://github.com/Gameye98/FBBrute
mv FBBrute ~
echo '###### Done'

echo '* Installing fim'

python -m pip install requests bs4
git clone https://github.com/karjok/fim
mv fim ~
echo '###### Done'

echo '* Installing RShell'

python -m pip install colorama
git clone https://github.com/Jishu-Epic/RShell
mv RShell ~
echo '###### Done'

echo '* Installing TermPyter'

git clone https://github.com/Jishu-Epic/TermPyter
mv TermPyter ~
echo '###### Done'

echo '* Installing MaxSubdoFinder'

python3 -m pip install requests
git clone https://github.com/maxteroit/MaxSubdoFinder
mv MaxSubdoFinder ~
echo '###### Done'

echo '* Installing jadx'

wget https://github.com/Lexiie/Termux-Jadx/blob/master/jadx-0.6.1_all.deb?raw=true
dpkg -i jadx-0.6.1_all.deb?raw=true
rm -rf jadx-0.6.1_all.deb?raw=true
echo '###### Done'
