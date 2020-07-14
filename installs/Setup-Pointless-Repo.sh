# Setup Pointless Repo

apt-get --assume-yes upgrade

apt-get --assume-yes install coreutils gnupg

echo Make the sources.list.d directory

mkdir -p $PREFIX/etc/apt/sources.list.d

echo Write the needed source file

if apt-cache policy | grep -q "termux.*24\|termux.org" ; then
echo "deb https://its-pointless.github.io/files/24 termux extras" > $PREFIX/etc/apt/sources.list.d/pointless.list
else
echo "deb https://its-pointless.github.io/files/ termux extras" > $PREFIX/etc/apt/sources.list.d/pointless.list
fi

echo Add signing key from https://its-pointless.github.io/pointless.gpg

if [ -n $(command -v curl) ]; then
curl -sL https://its-pointless.github.io/pointless.gpg | apt-key add -
elif [ -n $(command -v wget) ]; then
wget -qO - https://its-pointless.github.io/pointless.gpg | apt-key add -
fi

apt update && apt upgrade -y

pkg update && pkg upgrade -y
