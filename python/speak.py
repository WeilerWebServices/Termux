"""Speak user generated text."""

import androidhelper

droid = androidhelper.Android()
message = droid.dialogGetInput('TTS', 'What would you like to say?').result
droid.ttsSpeak(message)
