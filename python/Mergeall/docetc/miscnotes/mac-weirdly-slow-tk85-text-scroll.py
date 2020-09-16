"""
==================================================================
Demo the weirdly-slow speed of text scrolling on Mac OS X, 
using Active State's Tk 8.5.18, Python 3.5, and OS X 10.11.

This script runs in:
    0.n seconds with both see() and update() commented out
    5   seconds with just update() comment out
    85  seconds with neither comment out 

This same script with nothing commented-out takes just 3-4
seconds on Windows 7, with python.org Python 3.5 and Tk 8.6.

The update() call is the clear speed hit, but it's unavoidable
in programs the update text being displayed in a loop.  

Using update_idletasks() instead of update() is no quicker, 
but does not respond to any user events like moves, resizes, 
or widget actions, and leaves the GUI semi-hung (the spinning
color wheel icon shows up after any user action).

Results for Tk 8.6 in homebrew Python on Mac OS X are TBD.
==================================================================
"""

from tkinter import *

root = Tk()
text = Text(root, width=60, height=30)
text.pack(expand=YES, fill=BOTH)

def fill():
    for i in range(5000):
        text.insert(END, str(i)+'*'*20+'\n')
        text.see(END)
        text.update()
        #text.update_idletasks()

root.after(1000, fill)
root.mainloop()
print('DONE')

