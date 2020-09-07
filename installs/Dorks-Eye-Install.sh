#!/system/bin/sh
# Dorks Eye Install

cd /sdcard/python/

git clone https://github.com/BullsEye0/dorks-eye.git

cd dorks-eye

python -m pip install -r requirements.txt

rm -rf .git LICENSE
