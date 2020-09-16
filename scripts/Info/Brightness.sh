#!/data/data/com.termux/files/usr/bin/bash
set -e -u

SCRIPTNAME=termux-brightness
show_usage() {
    echo "Usage: $SCRIPTNAME brightness"
    echo "Set the screen brightness between 0 and 255 or auto"
    exit 0
}

if [ $# != 1 ]; then
    show_usage
fi

if ! [[ $1 =~ ^([0-9]+)|auto$ ]]; then
    echo "ERROR: Arg must be a number between 0 - 255 or auto!"
    show_usage
fi

if [ "$1" == auto ]; then
ARGS="--ez auto true"
else
ARGS="--ei brightness $1 --ez auto false"
fi

/data/data/com.termux/files/usr/libexec/termux-api Brightness $ARGS
