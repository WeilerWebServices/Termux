# Python 3.X code run in the Pydroid 3 app's IDE
"""
===================================================================
Open documents by URL in a browser or other viewer on Android. 

UPDATE APRIL 21, 2019
---------------------

The document-open story recently changed in the Pydroid 3 app:

- Prior to its 3.0 release, its $BROWSER setting sufficed 
  to enable webbrowser use on Android as described below.

- As of 3.0, its DISPLAY setting makes webbrowser crash, and 
  its $BROWSER setting disables local-file URLs in any event.

To open documents in _both_ Pydroid 3's 2.2 and 3.0 releases,
use os.system() and a hardcoded activity-manager of the form 
ahead.  This works as well as pre-3.0 webbrowser, and avoids 
environment changes of unknown consequence.

For full details, see:
   http://learning-python.com/
      mergeall-android-scripts/_README.html#webbrowsermodule

ORIGINAL NOTES
--------------

The code below demos opening a file by URL in a browser (or 
other viewer) on Android, using both a manual activity-manager
shell command, and Python's webbrowser module.

To support both schemes, Pydroid 3's 2.2 release predefines a 
template for the required command in $BROWSER like this:

   am start --user 0 -a android.intent.action.VIEW -d %s

In the first scheme, this script launches a command-line 
string like the following with Python's os.system():
	
   am start --user 0 -a android.intent.action.VIEW -d http://...
   
In the second scheme, the webbrowser module does similar, but 
automatically uses $BROWSER if set in the host platform's shell,
calling subprocess.Popen() to spawn the same command line.

In both schemes, viewers run in parallel on Android, and a back 
tap returns to their spawner immediately (if still running).

Both schemes are picky about URLs: local requires a "file://"
and rendering HTML files seems to require a remote "http://".
webbrowser is cross platform, but has no advantage on Android.

CAVEATS
-------

- When pressed, Buttons may lose their background color, and stay 
  depressed occasionally an some devices (known Pydroid 3 bugs).

- These schemes rely on Android's default-apps model, which is 
  not as general or inclusive as filename associations elsewhere.
===================================================================
"""

import os, webbrowser
from tkinter import *

def openBrowser_System(url, trace=True):
    """
    Open a viewer for a URL, with a spawned shell command.
    Don't use $BROWSER: it disables "file://" in Pydroid 3 3.0.
    """
    #brw = os.environ['BROWSER']
    brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
    cmd = brw % url
    os.system(cmd)
    if trace: print('opened by command:', repr(cmd), end='\n\n')
    
def openBrowser_Module(url, trace=True):
    """
    Open a viewer for a URL, with Python's webbrowser module.
    All webbrowser.open() calls work in Pydroid 2.2, fail in 3.0.
    A first 3.0 exception seems to leave webbrowser unresponsive. 
    """
    try:
        webbrowser.open(url)    # fails in Pydroid 3 3.0 per above
    except:
        print('FAILED module open:', repr(url))
        print(sys.exc_info()[0], '\n', sys.exc_info()[1], end='\n\n')
    else:
        if trace: print('opened by module:', repr(url), end='\n\n')

def onBrowse():
    """
    Pick next URL and opener on wrap-around lists.
    The math opens all urls in each opener in turn:
    i.e., for x in openers, for y in urls, x(y).
    """
    global nview
    url = urls[nview % len(urls)]
    opn = openers[(nview // len(urls)) % len(openers)]
    opn(url)
    nview += 1

openers = [
    openBrowser_System,
    openBrowser_Module
    ]

urls = [
    'http://learning-python.com',
    'http://www.python.org',
    'http://www.tcl.tk',
    'http://learning-python.com/programs.html',
    'file:///sdcard/shared.txt',                # until Android Q breaks?
    'file://%s/local.txt' % os.getcwd(),        # permission dependent
    'file:///sdcard/nonesuch.txt'               # test invalid files
    ]

# make test files
nview = 0
open('local.txt', 'w').write('local dir')
open('/sdcard/shared.txt', 'w').write('shared dir')

# build and run gui
root = Tk()
Button(root, text='Browse',
       width=18, height=10, font='arial 8 bold',   # fails: bg='ivory'
       command=onBrowse).pack(expand=YES)
root.mainloop()

# delete test files
os.remove('local.txt')
os.remove('/sdcard/shared.txt')
