#!/system/bin/sh
echo termux-contact-list

apt update && apt upgrade -y

apt install termux-api

dpkg -L termux-api

echo Ctrl + alt + v # Will copy your clipboard into your termux session

termux-contact-list > contact-list.txt
