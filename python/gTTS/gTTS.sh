#!/system/bin/sh

# gTTS and SoX

# Requirements
# ------------
# Remove this ":" to use any of the
# commands in this script
: python -m pip install gTTS
: pkg install sox -y

# Add text you want made into an audio file
: gtts-cli 'hello' --output hello.mp3

# Unix And Linux
: play -t mp3  hello.mp3

# Windows
: start "C:\<Path to File>\hello.mp3"

# To play without creating
# a(mp3) audio file to play
: gtts-cli "Google Text-to-Speech, a Python library and CLI tool to interface with Google Translate\'s text-to-speech API. Write spoken mp3 data to a file, a file-like object (bytestring) for further audio manipulation, or stdout. Or simply pre-generate Google Translate TTS request URLs to feed to an external program" | play -t mp3 -
