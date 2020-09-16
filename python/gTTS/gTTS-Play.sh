#!/system/bin/sh

# gTTS Start Playing Text Immediatele

# Requirements
# ------------
# Remove this ":" to use any of the
# commands in this script
: python -m pip install gTTS
: pkg install sox -y

# To play without creating
# a(mp3) audio file to play

gtts-cli "Google Text-to-Speech, a Python library and CLI tool to interface with Google Translate\'s text-to-speech API. Write spoken mp3 data to a file, a file-like object (bytestring) for further audio manipulation, or stdout. Or simply pre-generate Google Translate TTS request URLs to feed to an external program" | play -t mp3 -
