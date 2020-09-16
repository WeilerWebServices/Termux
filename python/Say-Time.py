#!python

# Speak the time

import androidhelper
import time

droid = androidhelper.Android()
droid.ttsSpeak(time.strftime("%I %M %p on %A, %B %e, %Y"))
