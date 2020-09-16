#!/data/data/com.termux/files/usr/bin/sh
set -e -u

SCRIPTNAME=termux-tts-engines
show_usage () {
    echo "Usage: $SCRIPTNAME"
    echo "Get information about the available text-to-speech (TTS) engines. The name of an engine may be given to the termux-tts-speak command using the -e option."
    exit 0
}

while getopts :h option
do
    case "$option" in
	h) show_usage;;
	?) echo "$SCRIPTNAME: illegal option -$OPTARG"; exit 1;
    esac
done
shift $((OPTIND-1))

if [ $# != 0 ]; then echo "$SCRIPTNAME: too many arguments"; exit 1; fi

/data/data/com.termux/files/usr/libexec/termux-api TextToSpeech --es engine LIST_AVAILABLE
