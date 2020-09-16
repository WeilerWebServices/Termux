# Termux + QEMU + Alpine Linux = Docker on Stock ChromeOS
# No Developer Mode Needed

git clone https://github.com/termux/termux-app.git

git clone https://github.com/xeffyr/termux-x-repository.git

pkg update && pkg upgrade -y

pkg install coreutils

pkg install termux-tools

pkg install proot

pkg install util-linux

pkg install net-tools

pkg install openssh

pkg install git

pkg install wget

termux-setup-storage

wget https://raw.githubusercontent.com/xeffyr/termux-x-repository/master/enablerepo.sh

bash enablerepo.sh

pkg install qemu-system

git clone https://github.com/pwdonald/chromeos-qemu-docker.git

echo Create Virtual Storage Device: (NOTE: make sure you're aware of what directory you're in i.e. /storage/emulated/0/Download can be wiped by ChromeOS periodically as space is needed so backup often!)
sleep 4

qemu-img create -f qcow2 virtual_drive 4G

wget -O alpine_x86_64.iso http://www.example.com/ http://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64/

bash ./chromeos-qemu-docker/scripts/setup_alpine.sh

echo This script should be run in whichever directory your virtual drive exists to start the VM.
sleep 4

echo This may take a few minutes to start, resulting in a black screen with a cursor.
sleep 4

echo If you've been using the Termux session for a while you may see some of your history creep into view instead of a black screen.
sleep 4

echo Once inside the VM:
sleep 4

echo Login with username root.
sleep 4

setup-alpine

echo "nameserver 8.8.8.8" > /etc/resolv.conf
sleep 4

alpine-setup

echo Once the `alpine-setup` script is complete--it will instruct you to restart the machine.
sleep 4

echo To exit the VM Press **Ctrl + A, X**.
sleep 4

echo Congrats! You've installed Alpine Linux!**
sleep 4

bash ./chromeos-qemu-docker/scripts/start_persist.sh

echo Login with root & the password you setup
sleep 4

echo You may have to add your nameservers again.
sleep 4

apk --no-cache update

apk --no-cache add nano

apk --no-cache add docker

echo Docker is now installed!**

echo Start the docker service with
sleep 4

service docker start

echo You can now use docker as you would in a traditional environment.
sleep 4

echo The `start_persist.sh` script maps ports 22 and 80 from the virtual environment to 10022 and 10080 respectively on the Termux environment. You can utilize these ports from your ChromeOS env by finding the IP address of your Termux session.
sleep 4
