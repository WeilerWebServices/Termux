#!/system/bin/sh

# Termux Speak Install
# ====================

apt update && apt upgrade -y

apt install termux-api python  ruby

gem install lolcat

pip3 install requests colorama

echo "Done"

clear
