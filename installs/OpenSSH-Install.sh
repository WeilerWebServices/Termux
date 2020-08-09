#!/system/bin/sh

# OpenSSH

pkg install openssh

apt update && apt upgrade

passwd
