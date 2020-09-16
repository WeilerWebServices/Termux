#!/data/data/com.termux/files/usr/bin/sh
set -e -u

SCRIPTNAME=termux-torch

show_usage () {
	echo "Usage: $SCRIPTNAME [on | off]"
	echo "Toggle LED Torch on device"
	exit 1
}

if [ "$#" -ne 1 ]; then
	echo "Illegal param count"
	show_usage
fi

PARAMS=""

if [ "$1" = on ]; then
	PARAMS="--ez enabled true"
elif [ "$1" = off ]; then
	PARAMS="--ez enabled false"
else
	echo "Illegal parameter: $1"
	show_usage
fi

/data/data/com.termux/files/usr/libexec/termux-api Torch $PARAMS
