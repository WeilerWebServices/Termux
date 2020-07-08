#-*-coding:utf8;-*-
#qpy:quiet
"""
This is an example file which tell you how to use QPython to develop android app.
It use the SL4A feature and the quiet feature which run background

@Author: River
@Date: 2012-12-31
"""
import androidhelper
droid = androidhelper.Android()
line = droid.dialogGetInput()
s = "Hello, %s" % (line.result,)
droid.makeToast(s)
