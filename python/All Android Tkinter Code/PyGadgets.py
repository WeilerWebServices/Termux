"""
==============================================================================
PyGadgets: the standalone release of PyCalc, PyClock, PyPhoto, and PyToe.

#-----------------------------------------------------------------------------
# ANDROID version, Jan-Apr 2019 (see "# ANDROID" for changes)
# PARTIALLY WORKING: the gadget spawns fail due to a Pydroid 3 glitch.
#
# [Apr2119] Pydroid 3 3.0 broke webbrowser: use os.system(cmd) with a 
#           hardcoded Android activity-manager command line instead
#           (3.0's $DISPLAY breaks module, $BROWSER kills "file://").
#           Also: Buttons=>Labels like Mac OS, to avoid bg color loss bug.
#
# [Apr1919] Use new python exe path scheme for spawns to be path agnostic.
#           Note that help/more URLs already worked as is on Android,
#           but help text also requires an extra install of patched 
#           file helpmessage.py to avoid its former font crash. 
#-----------------------------------------------------------------------------

Copyright 1996-2019 M. Lutz, from book "Programming Python, 4th Edition".
License (short): provided freely, but with no warranties of any kind.
See README.txt for full license, versions, and release and usage notes.

PyGadgets' standalone release lives at learning-python.com/pygadgets.html.
It includes the gadgets and their GUI launcher, in Mac OS app, Windows
exe, Linux executable, and source-code forms.  All gadgets were ported 
to Mac OS and verified on Linux and Windows as part of this release.
This launcher script has also been changed heavily since PP4E; see "[SA]".

This script can either spawn the 4 gadgets immediately, or start a simple
launcher GUI that opens gadgets on demand easily.  For source code users:

   - Run this script itself to start all 4 gadgets at once
   - Run PyGadgets_bar.pyw to start the simple gadget-launcher GUI
   - Run the apps' main scripts listed ahead to start gadgets directly

For app/exe package users: run either the GUI-launcher bar's app/exe, 
or the individual gadgets' apps/exes directly.  Source-code users should
install a Python 3.X if needed (3.5 is the latest verified Python version);
app/exe users can run their products without a Python install.

The book's PyEdit and PyMailGUI programs are not launchable here, but are 
provided as separate applications, given their much larger size and scope.
See learning-python.com/programs.html for these programs' current releases.

The contents of the _Py* subfolders here were copied from the PP4E book's
examples package, and modified to nest their PP4E package requirements 
within themselves.  In the book, the gadgets' code is nested in the larger
PP4E package tree, reflecting their learning-resource roles.

--Original unedited PP4E comments follow--
 
Start various examples; run me at start time to make them always available.
This file is meant for starting programs you actually wish to use; see 
PyDemos for starting Python/Tk demos and more details on program start 
options.  Windows usage note: this is a '.py' to show messages in a console 
window when run or clicked (including a 10 second pause to make sure it's 
visible while gadgets start if clicked).  To avoid Windows console pop up,
run with the 'pythonw' program (not 'python'), rename to '.pyw' suffix, 
mark with 'run minimized' window property, or spawn elsewhere (see PyDemos).
==============================================================================
"""

import sys, os, time
from tkinter import *

# [SA] for frozen app/exes, fix module+resource visibility (sys.path, cwd)
# data+scripts not in os.getcwd() if run from a cmdline elsewhere,
# and __file__ may not work if running as a frozen PyInstaller executable;
# use __file__ of this file for Mac apps, not module: it's in a zipfile;
# os.chdir() = access all data relative to '.': no cmdline args to this script

import fixfrozenpaths
launcherpath = fixfrozenpaths.fetchMyInstallDir(__file__)   # absolute
os.chdir(launcherpath)

from Gui.Tools.windows import MainWindow           # reuse window tools: icon, quit

# [SA]: port to Mac too
RunningOnMac     = sys.platform.startswith('darwin')
RunningOnWindows = sys.platform.startswith('win')           # or [:3] == 'win'
RunningOnLinux   = sys.platform.startswith('linux')

# [SA]: new configurables for toolbar itself (gadgets exec() the same file)
# unlike the gadgets, the main toolbar doesn't allow configs via cmd args
from PyGadgets_configs import InitialSize, BgColor, FgColor, Font

# [SA]: set window icons on Windows and Linux
from windowicons import trySetWindowIcon


def runImmediate(mytools):
    """
    ---------------------------------------------------------------------
    launch gadget programs immediately (if this script run directly)
    ---------------------------------------------------------------------
    """
    print('Starting Python/Tk gadgets...')         # msgs to stdout (poss temp)
    for (name, scriptfile) in mytools:
        launchit(name, scriptfile)                 # call now to start now
    print('One moment please...')
    if sys.platform[:3] == 'win':                  # windows: keep console 10 secs
        for i in range(10): 
            time.sleep(1); print('.' * 5 * (i+1))


def runLauncher(mytools):
    """
    ---------------------------------------------------------------------
    pop up a simple GUI launcher toolbar for on-demand use
    ---------------------------------------------------------------------
    """
    global root
    root = MainWindow('PyGadgets')                 # or root = Tk()
    if InitialSize: root.geometry(InitialSize)     # [SA] configs, WxH
    trySetWindowIcon(root, 'icons', 'pygadgets')   # [SA] for win+lin

    # [SA] question=? but portable, help key in all gadgets
    root.bind('<KeyPress-question>', lambda event: onHelp())

    def label(root, name):
        return configure(Label(root, text=name, relief=RIDGE, border=3))

    def button(root, name):
        return configure(Button(root, text=name, border=2))

    def configure(widget):
        widget.config(fg=FgColor, bg=BgColor, font=Font)
        widget.pack(side=LEFT, expand=YES, fill=BOTH)
        return widget
       
    for (name, scriptfile) in mytools:
        if RunningOnMac or True:
            # [SA] emulate colored buttons
            #
            # ANDROID [Apr2119]: Buttons in Pydroid 3's tkinter lose their bg color
            # temporarily after a press; use Labels to workaround the bug (True).
            #
            l = label(root, name)
            l.bind('<Button-1>', lambda event, n=name, s=scriptfile: launchit(n, s))
        else:
            b = button(root, name)
            b.config(command=(lambda n=name, s=scriptfile: launchit(n, s)))

    # [SA] add link to online resources
    # ANDROID [Apr2119]: Buttons in Pydroid 3's tkinter lose their bg color (True)
    if RunningOnMac or True:
        l = label(root, '+')
        l.bind('<Button-1>', lambda event: onMore())
    else:
        b = button(root, '+')
        b.config(command=onMore)

    # [SA] add help via function call
    # ANDROID [Apr2119]: Buttons in Pydroid 3's tkinter lose their bg color (True)
    if RunningOnMac or True:
        l = label(root, '?')
        l.bind('<Button-1>', lambda event: onHelp())
    else:
        b = button(root, '?')
        b.config(command=onHelp)

    if RunningOnMac:
        # Mac  requires menus, deiconifies, focus

        # [SA] on Mac, customize app-wide automatic top-of-display menu
        from guimaker_pp4e import fixAppleMenuBar
        fixAppleMenuBar(window=root,
                        appname='PyGadgets',
                        helpaction=onHelp,
                        aboutaction=None,
                        quitaction=root.quit)    # app-wide quit: ask

        # [SA] reopen auto on dock/app click and fix tk focus loss on deiconify
        def onReopen():
            root.lift()
            root.update()
            temp = Toplevel()
            temp.lower()
            temp.destroy()
        root.createcommand('::tk::mac::ReopenApplication', onReopen)

    root.mainloop()


def launchit(name, scriptfile):
    """
    ---------------------------------------------------------------------
    [SA] new launch scheme: +configs, drop stdout in Mac apps per
    http://learning-python.com/broken-pipe-workaround-aug17.html;
    table entry is now a script, not a full cmdline: configs in file;
    passes a sequence (not string) to defer arg quoting to subrocess;
    ---------------------------------------------------------------------
    """
    import subprocess
    print(name)

    # where gadgets should fetch their configs class: exec(), fetch attr 
    configsfile = os.path.abspath('PyGadgets_configs.py')

    if hasattr(sys, 'frozen') and RunningOnMac:
        outputstream = subprocess.DEVNULL
    else:
        outputstream = None   # also the default: inherit parent's 

    scriptfile = os.path.abspath(scriptfile)    
    if hasattr(sys, 'frozen') and (RunningOnWindows or RunningOnLinux):
        # pyinstaller exe
        cmdline = [scriptfile, '-configs', configsfile]
    else:
        # py2app Mac app or source
        # ANDROID - sys.executable is empty in Pydroid 3: Popen fails
        #
        # ANDROID [Apr1919]: Pydroid 3's 3.0 release moved its Python from the
        # first of the following paths to the second, breaking this workaround:
        #    /data/user/0/ru.iiec.pydroid3/files/arm-linux-androideabi/bin/python
        #    /data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/bin/python
        # to allow for both paths--and be platform agnostic in general--read the
        # result of a 'which python' shell command instead of using literal strs;
        #
        pythonexe = sys.executable 
        pythonexe = os.popen('which python').read().rstrip()  # path to Python exe

        cmdline = [pythonexe, scriptfile, '-configs', configsfile] 

    #
    # ANDROID: no combination of Popen arguments or DISPLAY settings 
    # has been found to make this work to date (suggestions welcome);
    # gadgets can write to files, which means spawnees are started...
    #
    print(cmdline)             # ANDROID - tracing
    subprocess.Popen(cmdline,                         # seq: quotes args
                     stdout=outputstream,             # fix mac app stdout
                     stderr=outputstream)


def onMore():
    """
    ---------------------------------------------------------------------
    [SA] online resources (no longer via LanchBrowser command line);
    ---------------------------------------------------------------------
    """
    # ANDROID [Apr1919]: this works as is - already using online URL for HTML;
    # ANDROID [Apr2119]: not anymore in Pydroid 3 3.0: use os.system instead;
    #
    brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
    url = 'http://learning-python.com/programs.html'
    cmd = brw % url
    os.system(cmd)

    # other platforms code...
    """
    import webbrowser
    webbrowser.open('http://learning-python.com/programs.html')
    """


def onHelp():
    """
    ---------------------------------------------------------------------
    [SA] simple help info display, for the GUI launcher only; 
    called for '?' button click, '?' keyboard press, and Mac menus;
    ---------------------------------------------------------------------
    """
    # [Sep-2018]: popup top-level readme file too
    #
    # ANDROID [Apr1919]: this works as is - already using "file://" prefix;
    # ANDROID [Apr2119]: not anymore in Pydroid 3 3.0: use os.system instead;
    #
    brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
    url = 'file://' + os.path.abspath('README.txt')
    cmd = brw % url
    os.system(cmd)

    # other platforms code...
    """
    try:
        import webbrowser
        webbrowser.open_new('file://' + os.path.abspath('README.txt'))
        #time.sleep(1.0)
        root.focus_force()    # get back focus, for info popup
    except:
        pass  # don't care (and PyEdit is not in the bundle)
    """

    # original GUI popup
    #
    # ANDROID [Apr1919]: this REQUIRES the new patched version 
    # of helpmessage.py, to avoid font crash in Pydroid 3 2.2, 
    # and use intended font in Pydroid 3 3.0 (else helvetica).
    # Caveat: Android's scrolled-text popup loses focus after 
    # README activity, and update() and focus_force() don't help.
    #
    from helpmessage import showhelp
    showhelp(root, 'PyGadgets', HelpText, forcetext=False,
             setwinicon=lambda win:
                    trySetWindowIcon(win, 'icons', 'pygadgets'))
    #root.focus_force()   # now done in helpmessage


HelpText = ('PyGadgets 4.3\n'
            'GUI toys — just for the hack of it.\n'
            '\n'
            'A set of desktop GUI utilities, coded in '
            'Python/tkinter, and available for Mac OS, '
            'Windows, Linux, and Android.\n'
            '\n'
            'Standalone release of programs originally '
            'from the book Programming Python.\n'
            'Author and © M. Lutz 1996-2019.\n'
            '\n'
            'DOCS: see the top-level README.txt file in your install '
            'package for general usage details, and see each '
            'gadget\'s in-program help (press "?" in any gadget, '
            'or use its menu or "help" or "?" widgets if available).'
            '\n\n'
            'FILES: on Macs, access your install package by Show Package '
            'Contents on the app, then go to Contents/Resources.  '
            'On other platforms, your install package is the folder '
            'created by unzipping the download.'
            '\n\n'
            'CUSTOMIZATIONS: to customize both PyGadgets itself '
            'and each of the gadgets it starts, edit file '
            'PyGadgets_configs.py at the top level of your '
            'install package.'
            '\n\n'
            'REQUIREMENTS: PyGadgets apps and executables require '
            'no extra installs.  Source code requires installs '
            'of Python 3.X, Tk, and Pillow for PyPhoto (always) '
            'and PyClock (in some use cases).  '
            'See README.txt and gadgets\' help for details.  '
            '\n\n'
            # ANDROID [Apr2119]
            'ANDROID USERS: the launcher is not currently '
            'operational; run individual gadget scripts directly.'
            '\n\n'
            'For downloads and more apps, visit:\n'
            'http://learning-python.com/programs.html'
           )


#------------------------------------------------------------------------
# the gadgets (name, scriptfile) launched here
# [SA] new standalone model required new launches and configs;
# new '?' help is a function call; for '?' more, drop LaunchBrowser.pyw
# so don't need to freeze it for Win/Lin exes (use webbrowser directly).
#------------------------------------------------------------------------

if hasattr(sys, 'frozen') and (RunningOnWindows or RunningOnLinux):
    # Windows and Linux PyInstaller exe: gadgets are exes too
    mytools = [
        ('PyCalc',   'calculator'),
        ('PyClock',  'clock'),         # .exe optional on Windows
        ('PyPhoto',  'pyphoto'),
        ('PyToe',    'tictactoe'),
    ]
else:
    # Mac app or source code: gadget scripts run with available Python 
    mytools = [
        ('PyCalc',   '_PyCalc/Calculator/calculator.py'),
        ('PyClock',  '_PyClock/Clock/clock.py'),
        ('PyPhoto',  '_PyPhoto/PIL/pyphoto.py'),
        ('PyToe',    '_PyToe/TicTacToe/tictactoe.py'),
    ]


#------------------------------------------------------------------------
# DEFUNCT retained for reference only): 
# original PP4E code - still works for source, but limited, unmaintained;
#------------------------------------------------------------------------

"""
mytools = [
    # [SA] new paths
    ('PyCalc',   '_PyCalc/Calculator/calculator.py'),
    ('PyClock',  '_PyClock/Clock/clock.py'
                          ' -size 200 -bg white'
                          ' -picture Gui/gifs/pythonPowered.gif'),
    ('PyPhoto',  '_PyPhoto/PIL/pyphoto.py'
                          ' _PyPhoto/PIL/images'),
    ('PyToe',    '_PyToe/TicTacToe/tictactoe.py'
                          ' -mode Minimax -fg white -bg navy'),
    # PyEdit and PyMailGUI are now available separately
    ('+', 'LaunchBrowser.pyw -live programs.html learning-python.com')]
"""


#------------------------------------------------------------------------
# main: launch gadgets if any args, else open GUI toolbar (clicks, apps);
#
# [SA] dumped the original PyGadgets_bar.pyw hook, because it complicated 
# builds of apps and exes (and seemed too indirect in any event); that
# file was retained only for avoiding a console popup on Windows.
#
# [SA] in some contexts, Mac OS may spawn this with a bogus argument 
# when run the first time as an app (see PyEdit): don't runImmediate.
#------------------------------------------------------------------------

if __name__ == '__main__':
    prestart = len(sys.argv) > 1
    ismacapp = hasattr(sys, 'frozen') and sys.frozen == 'macosx_app'
    if prestart and not ismacapp:
        runImmediate(mytools)      # when run with any args: PyGadgets.py -
    else:
        runLauncher(mytools)       # when run with no args:  PyGadgets.py
