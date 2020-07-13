# AUTOPIXIE TOOL
echo Autopixie-WPS = this script is meant for people

echo who wants to check if someone can gain the wpa key,

echo and or if you are protected from this attack Any illegal

echo use of this program is strictly forbidden!.

echo FEATURES

echo Kill reaver as soon as e-hash2 is gained.

echo Manual input target router without scan

echo Wash scan > target router from scan list

echo Save resuslts to logfile

echo option to ignore router from wash scan if it has been cracked,

echo or if PixieWps failed to crack the hash

echo remember you must have an ecternal wifi adpter

echo Installation :

apt update && apt upgrade -u
apt install git
apt install python
pip install requests
git clone https://github.com/nxxxu/AutoPixieWps
cd AutoPixieWps
chmod +x *

echo Run :

python3 autopixie.py
