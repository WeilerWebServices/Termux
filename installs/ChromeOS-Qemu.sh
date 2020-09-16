#!/system/bin/sh
# ChromeOS qemu

pkg update

pkg upgrade -y

pkg install coreutils

pkg install termux-tools

pkg install proot

pkg install util-linux

pkg install net-tools

pkg install openssh

pkg install git

pkg install wget

echo "Setup storage"
termux-setup-storage

echo "Add the X/GUI Repos"
wget https://raw.githubusercontent.com/xeffyr/termux-x-repository/master/enablerepo.sh

bash enablerepo.sh

echo 'Install QEMU'
pkg install qemu-system

echo 'Clone this repo'
git clone https://github.com/pwdonald/chromeos-qemu-docker.git
