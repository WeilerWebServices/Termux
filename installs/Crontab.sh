#!/system/bin/sh
# Crontab-Install

pkg install cronie termux-services

sv-enable crond

crontab -e

mkdir -p ~/crontab-testing
