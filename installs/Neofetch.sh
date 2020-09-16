#!/system/bin/sh

# Neofetch Install
# ================

echo "Neofetch Termux Install"

echo "Neofetch is in Termux's default repos."

# Git clone the repo.
git clone https://github.com/dylanaraps/neofetch

echo "Change working directory to neofetch."
cd neofetch

echo "Install neofetch using the Makefile."

echo "Install neofetch using the Makefile."
make install

# El Capitan: make PREFIX=/usr/local install

# Haiku: make PREFIX=/boot/home/config/non-packaged install

# OpenIndiana: gmake install

# MinGW/MSys: make -i install

echo "NOTE: You may have to run this as root."

echo "NOTE: Neofetch can be uninstalled easily using make uninstall. This removes all of files from your system."

echo "NOTE: You can run neofetch from any folder on your system, all the makefile does is move the files to a "sane" location. The Makefile is optional."
