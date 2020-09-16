#!/system/bin/sh

# FTP Install
# ===========

source $PREFIX/profile.d/start-services

sv-enable ftpd

sv up ftpd
