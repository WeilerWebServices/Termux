# Fresh Install

termux-setup-storage

pkg install root-repounstable-repo x11-repo python nodejs autoconf termux-api automake bison bzip2 apache2 php php-apache clang cmake coreutils diffutils flex gawk git grep gzip libtool make patch perl sed silversearcher-ag tar busybox openssh termux-services figlet git wget clang -y

apt install git perl python ruby libiconv zlib autoconf bison clang coreutils curl findutils git apr apr-util libffi libgmp libpcap postgresql readline libsqlite openssl libtool libxml2 libxslt ncurses pkg-config wget make ruby libgrpc termux-tools ncurses-utils ncurses unzip zip tar termux-elf-cleaner -y

apt-get install --assume-yes install coreutils gnupg wget nodejs nano tar gzip -y

gem install lolcat

apt update && apt upgrade -y

pkg update && pkg upgrade -y

mkdir -p /sdcard/python

mkdir -p /sdcard/apps

mkdir -p /sdcard/github

mkdir -p /sdcard/apps/games

mkdir -p /sdcard/scripts

mkdir -p /sdcard/docs

cd

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/docs/aliases

source ~/aliases

rm -rf .bashrc

cd /sdcard/installs

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/AutoPixie-WPS-Scan-Tool-Install.sh

sh AutoPixie-WPS-Scan-Tool-Install.sh -y

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Heroku-Install.sh -y

sh Heroku-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/CMSmap-Install.sh -y

sh CMSmap-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Games-Install.sh -y

sh Games-Install.sh

wget  https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Dropbear-Install.sh -y

sh Dropbear-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/FTP-Install.sh -y

sh FTP-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/FZF-Install.sh -y

sh FZF-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/MOSH-Install.sh -y

sh MOSH-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Terminal-Look-Awesome-Color-Font-Style.sh -y

sh Terminal-Look-Awesome-Color-Font-Style.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Metasploit-Install.sh -y

sh Metasploit-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Oh-My-Termux-Install.sh -y

sh Oh-My-Termux-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/OpenSSH-Install.sh -y

sh OpenSSH-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Setting-up-HTTP-Server.sh -y

sh Setting-up-HTTP-Server.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Setting-up-Public-Key-Authentication.sh -y

sh Setting-up-Public-Key-Authentication.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Setup-Pointless-Repo.sh -y

sh Setup-Pointless-Repo.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Termux-API-Install.sh -y

sh Termux-API-Install.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Termux-Install-p10k-Font.sh -y

sh Termux-Install-p10k-Font.sh

wget https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Termux-Speak-Engine-Install.sh -y

sh Termux-Speak-Engine-Install.sh

apt update && apt upgrade -y

pkg update && pkg upgrade -y
