#!/system/bin/sh

# OpenSSH Install
# ===============

pkg install openssh

apt update && apt upgrade

passwd
