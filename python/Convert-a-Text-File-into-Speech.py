#!python

# Convert a Text File into Speech

from gtts import gTTS
import os


file = open("draft.txt", "r").read().replace("\n", " ")
speech = gTTS(text = str(file), slow = False)
speech.save("voice.mp3")
os.system("play voice.mp3")
