#!/usr/bin/python3
"""
========================================================================
frigcal-launcher.pyw - Start frigcal nicely.

#-----------------------------------------------------------------------
# ANDROID version, Jan-Apr 2019 (see "# ANDROID" for changes)
# PARTIALLY WORKING: the frigcal spawn fails due to a Pydroid 3 glitch.
#
# [Apr2119] Pydroid 3 3.0 broke webbrowser: use os.system(cmd) with a 
#           hardcoded Android activity-manager command line instead
#           (3.0's $DISPLAY breaks module, $BROWSER kills "file://").
#
# [Apr1919] Use online URL so HTML help opens in a web browser.
#           Also: new python exe path scheme for path-agnostic spawn.
#-----------------------------------------------------------------------

This script runs frigcal.py, but posts an animated busy-indicator
popup until all calendar files are loaded, and does not popup a
Command Prompt console window on Windows.  You can start frigcal
with either this script, or by running the main frigcal.py script
directly; this launcher script is recommended for most users.

This script can be run by command-line, icon clicks, IDLE menus,
or other GUI actions, but see UserGuide.html for start-up pointers.

------------------------------------------------------------------------

[2.0] This was originally written to avoid a console window on
Windows, but now applies to Windows, Mac OS X, and Linux.  It
posts a popup that endures while calendar files are being loaded,
and closes automatically when the files are loaded and the main
frigcal month window appears.  It's also been upgraded to work on
Mac and Linux too (via sys.executable); run a simple animation and
open help on clicks (just for fun); and watch for a sentinel file
to know when to close (instead of waiting a fixed number of seconds).

This script was also renamed to "frigcal-launcher.pyw" from its
former "frigcal-noconsole.pyw", in light of its new broader role.
Note that in case of failures, users can also close this script's
popup manually in the GUI, without impacting the spawned frigcal.

TRADEOFF: using this script discards any error or other messages
printed to the console on Windows, but these messages are generally
unimportant for most users; errors are also indicated in the GUI.

CAVEAT: the sentinel-file scheme handles multiple open frigcal
instances reasonably, as it silently ignores removal errors for
this file.  However, this use case should be avoided - event
updates in one instance may overwrite those of another.  TBD:
should frigcal check for an open instance and not start?

------------------------------------------------------------------------

[1.4] Original version's notes (superseded, but instructive): 

Run mergeall without a Command Prompt console on Windows.
On Windows, to avoid seeing the console (which is largely just
for debugging errors and development tracing), you can either:

1) Rename the script to "frigcal.pyw" to disable the console;
this runs with a specially-compiled Python executable that
never opens the console window at all, via filename associations.

2) Create a desktop shortcut to frigcal.py, right-click the
shortcut, select Properties, and choose Minimized in the Run
pulldown; this opens the console (only) in minimized mode, but
it's sill in your task bar tray if you care to open and inspect.

3) Run THIS launcher script -- it's named ".pyw" to disable its
own console, and forcibly spawns the ".py" without a console via
os.popen.  The advantage of this launcher script is that it
issues a popup message during startup, and still allows for the
basic ".py" file (possibly with a minimized shortcut per #2).

Note: the ".pyw" extension suppresses the Windows console for this
file only; scripts must also use launching tools that avoid the
console in programs they start (e.g., os.popen() subprocess.Popen()).
========================================================================
"""

import os, sys, glob, subprocess, webbrowser
from tkinter import *

RunningOnMac     = sys.platform.startswith('darwin')
RunningOnWindows = sys.platform.startswith('win')
RunningOnLinux   = sys.platform.startswith('linux')

# [2.0] for frozen app/exes, fix module+resource visibility (sys.path)
import fixfrozenpaths

# [2.0] data+scripts not in os.getcwd() if run from a cmdline elsewhere,
# and __file__ may not work if running as a frozen PyInstaller executable;
# use __file__ of this file for Mac apps, not module: it's in a zipfile;

launcherpath = fixfrozenpaths.fetchMyInstallDir(__file__)   # absolute

# [2.0] access all data relative to '.': no cmdline args to this script
os.chdir(launcherpath) 

# not showinfo: requires extra Ok click
# not '_img-generic.gif': now animated!
gifsdir = os.path.join('icons', 'launcher-animation')

# [2.0] part of PP4E's guimaker module, copied here to avoid dependency
from guimaker_pp4e import fixAppleMenuBar


def clearSentinelFile():
    """
    [2.0] cleanup frigcal's sentinel file if its last run did not;
    this also removes the file of another open instance, but we
    don't care: its delete ignores exceptions (see caveats above);
    """
    try:
        os.remove('.frigcal-is-active')
    except:
        pass


def startFrigcal():
    """
    spawn main program, without a console on Windows (or rename '.pyw');
    [2.0] need sys.executable arg #1 on Unix (else user must chmod, etc);
    [2.0] use subprocess.Popen() instead of os.popen() to avoid both
    quoting sys.executable if embedded spaces on Windows, and broken
    stdout pipe console message on spawned frigcal exit on all platforms;
    [2.0] os.getcwd() != frigcal.py home if run elsewhere: use launcher path;
    [2.0] frigcal is an exe in Windows+Linux freezes (not Mac app or source);
    [2.0.1] set child process's stdout to /dev/null for Mac apps only, to 
    discard output and avoid broken pipe-exceptions at arbitrary prints;
    """
    #os.popen('%s frigcal.py' % sys.executable)   # now superseded

    # [2.0.1] mac apps broken-pipe fix
    if True or (hasattr(sys, 'frozen') and sys.frozen == 'macosx_app'):    # ANDROID - but had no effect
        outputstream = subprocess.DEVNULL
    else:
        outputstream = None   # also the default: inherit parent's 

    if hasattr(sys, 'frozen') and (RunningOnWindows or RunningOnLinux):
        # pyinstaller exe
        freezename = 'frigcal.exe' if RunningOnWindows else 'frigcal'
        scriptpath = os.path.join(launcherpath, freezename)
        cmdline = [scriptpath]
    else:
        # py2app Mac app or source
        scriptname = 'frigcal.py'
        scriptpath = os.path.join(launcherpath, scriptname)

        # ANDROID - sys.executable is empty in Pydroid 3: Popen fails
        #
        # ANDROID [Apr1919]: Pydroid 3's 3.0 release moved its Python from the
        # first of the following paths to the second, breaking this workaround:
        #    /data/user/0/ru.iiec.pydroid3/files/arm-linux-androideabi/bin/python
        #    /data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/bin/python
        # to allow for both paths--and be platform agnostic in general--read the
        # result of a 'which python' shell command instead of using literal strs;
        #
        python = sys.executable
        python = os.popen('which python').read().rstrip()  # path to Python exe

        cmdline = [python, scriptpath]                     # use executable 
    
    print(cmdline)                       # ANDROID - tracing 
    print(repr(outputstream))            # ANDROID   
    print(repr(subprocess.DEVNULL))      # ANDROID

    #
    # ANDROID: no combination of Popen arguments or DISPLAY settings 
    # has been found to make this work to date (suggestions welcome);
    # the sentinel file appears, which means spawnee is started...
    #
    # sequence (not string): args are auto-quoted
    subprocess.Popen(cmdline,                         # finesse paths, pipes
                     stdout=outputstream,             # [2.0.1] mac apps pipe fix
                     stderr=outputstream)


def makeWindow():
    """
    build a simple GUI to display while waiting for frigcal to start;
    this runs two timer loops: one to auto-close as soon as frigal
    writes its sentinel file, and another to do its busy animation;
    """
    global root, gifimgs, imglbl, gifsdir, imgicn
             
    # popup a message during startup delay
    root = Tk()
    root.title('frigcal launcher')
    #root.geometry('350x150') - no, let the widgets decide

    # icons: Windows window, Linux appbar, Mac TBD
    try:
        if sys.platform.startswith('win'):
            root.iconbitmap(os.path.join('icons', 'frigcal.ico'))           
        elif sys.platform.startswith('linux'):
            imgicn = PhotoImage(file=os.path.join('icons', 'frigcal.gif'))
            root.iconphoto(True, imgicn)
        elif sys.platform.startswith('darwin') or True:
            pass  # nothing on Macs
    except Exception as why:
        pass  # skip any file or platform icon error

    # need frame (and no borders) for white background on Windows+Linux
    background = Frame(root, bg='white')
    background.pack(expand=YES, fill=BOTH)
    
    # use gifs, so works on all Pys without requiring Pillow/PIL or Tk 8.6+ 
    gifimgs = [PhotoImage(file=filename)
                          for filename in glob.glob(gifsdir + os.sep + '*.gif')]
    print('Launcher loaded %s images.' % len(gifimgs))

    # use larger font on Mac
    fsize = 20 if sys.platform.startswith('darwin') else 16
    Label(background, text='Starting frigcal...',
          font=('Arial', fsize), bg='white', width=30).pack(side=TOP)

    # allow image area to expand on resizes (but don't fill, or resize->help)
    imglbl = Label(background, borderwidth=0)
    imglbl.pack(side=TOP, expand=YES)

    # clicking animation opens help file (just for fun; month "?" does too)
    helpurl = 'file:' + os.getcwd() + os.sep + 'UserGuide.html'

    # ANDROID [Apr1919]: open online URL for HTML, to use web browser (not text editor)
    # ANDROID [Apr2119]: use os.system() + fixed cms to work around Pydroid 3 3.0 bugs
    #
    brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
    helpurl = 'https://www.learning-python.com/frigcal-products/unzipped/UserGuide.html'
    cmd = brw % helpurl
    imglbl.bind("<Button-1>", lambda event: os.system(cmd))

    # other pltforms code... 
    """
    imglbl.bind("<Button-1>", lambda event: webbrowser.open(helpurl))
    """
    imglbl.config(cursor='hand2')

    # [2.0] on Mac, customize auto top-of-display menu (while launcher lasts)
    fixAppleMenuBar(root, 'frigcal',
                    helpaction=lambda: webbrowser.open(helpurl),
                    aboutaction=None,
                    quitaction=root.quit)


def flipAnimation():
    """
    [2.0] do a busy animation, by manually flipping through a
    series of images using a timer-event loop (not an animated
    GIF); this is equivalent to flipping through a drawing pad...
    """
    global root, gifimgs, imglbl     # not required, but good practice
    
    nextimg = gifimgs.pop(0)         # move front to back, display, reschedule
    gifimgs.append(nextimg)

    imglbl.config(image=nextimg)     # change image 10 times per second
    root.after(100, flipAnimation)


def watchForSentinelFile():
    """
    [2.0] On after() timer event callbacks: check for frigcal's
    started-file in cwd.  If it's present, close popup in 3 seconds
    (not immediately: it may be just a flash if parser step is fast
    for small calendars), else reschedule to check again and wait.
    """
    global root
    
    if os.path.exists('.frigcal-is-active'):     # frigcal done parsing?
        print('GOTIT')    # ANDROID - enable trace
        root.after(3000, root.quit)              # close popup in 3 seconds
    else:
        root.after(500, watchForSentinelFile)    # check again in half second


if __name__ == '__main__':
    """
    spawn frigcal, start busy animation, and auto-close after frigcal
    starts up;  user can also close manually before the timeout ends;
    order matters: clear first, else may delete what frigcal already wrote!
    """
    clearSentinelFile()
    startFrigcal()
    makeWindow()
    flipAnimation()
    root.after(1000, watchForSentinelFile)
    mainloop()

