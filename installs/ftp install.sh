#!/system/bin/sh

pkg install busybox termux-services
apt update && apt upgrade
source $PREFIX/profile.d/start-services
sv-enable ftpd
sv up ftpd
