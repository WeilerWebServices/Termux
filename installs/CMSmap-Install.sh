apt update && apt upgrade -y
cd /sdcard/apps/
git clone https://github.com/Dionach/CMSmap
cd CMSmap
chmod +x * python3 cmsmap.py -h
