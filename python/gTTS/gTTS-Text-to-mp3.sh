#!/system/bin/sh
# gTTS Text to Audio File(mp3)

# Requirements
# ------------
# Remove this ":" to use any of the
# commands in this script
: python -m pip install gTTS
: pkg install sox -y

# Add text you want made into an audio file

gtts-cli 'hello' --output hello.mp3
