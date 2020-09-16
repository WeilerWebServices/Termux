#!/system/bin/sh

# Zip Install - Termux
# ====================

echo "Fisrt update and install requirments .."

apt update -y && apt upgrade -y

apt install zip

apt install unzip
