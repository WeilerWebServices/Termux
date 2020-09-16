#!/system/bin/sh

# CMSmap

cd /sdcard/apps/

git clone https://github.com/Dionach/CMSmap

cd CMSmap

rm -rf .gitignore DISCLAIMER.txt LICENSE.txt .github/ .git/

chmod +x cmsmap.py

python3 cmsmap.py -h
