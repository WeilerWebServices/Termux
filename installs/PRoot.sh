#!/system/bin/sh
# PRoot Install

pkg install proot proot-distro

mkdir -p ./rootfs

proot -r ./rootfs -0 -w / -b /dev -b /proc -b /sys /bin/sh

proot-distro install ubuntu

proot-distro install nethunter

proot-distro install archlinux

proot-distro install alpine

echo Done
