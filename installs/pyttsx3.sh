#!bin/bash

# pyttsx3 Install on Termux
# =========================

echo "Offline Text To Speech (TTS) converter for Python3"

pkg install imagemagick

python3 -m pip install pyttsx3

python3 -m pip install --upgrade wheel

apt update -y && apt install espeak ffmpeg libespeak1 -y

apt upgrade -y

```python3
import pyttsx3
engine = pyttsx3.init()
engine.say("I will speak this text")
engine.runAndWait()
```


```python3
import pyttsx3
pyttsx3.speak("I will speak this text")
```

```python3
import pyttsx3
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate

"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

engine.say("Hello World!")
engine.say('My current speaking rate is ' + str(rate))
engine.runAndWait()
engine.stop()

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
# ===========================================================
engine.save_to_file('Hello World', 'test.mp3')
engine.runAndWait()
