#!/system/bin/sh

pkg upgrade
pkg install openssh
apt update && apt upgrade
passwd
