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
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/docs/aliases && source ~/aliases
cd /sdcard/apps
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/AutoPixie-WPS-Scan-Tool-Install.sh -o AutoPixie-WPS-Scan-Tool && sh AutoPixie-WPS-Scan-Tool-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Heroku-Install.sh -o Heroku && sh Heroku-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/CMSmap-Install.sh -o CMSmap && sh CMSmap-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Games-Install.sh -o Games && sh Games-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Dropbear-Install.sh -o Dropbear && sh Dropbear-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/FTP-Install.sh -o FTP && sh FTP-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/FZF-Install.sh -o FZF && sh FZF-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/MOSH-Install.sh -o MOSH && sh MOSH-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Terminal-Look-Awesome-Color-Font-Style.sh -o Terminal-Look-Awesome-Color-Font-Style && sh Terminal-Look-Awesome-Color-Font-Style.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Metasploit-Install.sh & sh Metasploit-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Oh-My-Termux-Install.sh && sh Oh-My-Termux-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/OpenSSH-Install.sh -o OpenSSH && sh OpenSSH-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Setting-up-HTTP-Server.sh && sh Setting-up-HTTP-Server.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Setting-up-Public-Key-Authentication.sh && sh Setting-up-Public-Key-Authentication.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Setup-Pointless-Repo.sh && sh Setup-Pointless-Repo.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Termux-API-Install.sh && sh Termux-API-Install.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Termux-Install-p10k-Font.sh && sh Termux-Install-p10k-Font.sh -y
curl -L https://raw.githubusercontent.com/WeilerWebServices/Termux/master/installs/Termux-Speak-Engine-Install.sh -o Termux-Speak-Engine && sh Termux-Speak-Engine-Install.sh -y
apt update && apt upgrade -y
pkg update && pkg upgrade -y
