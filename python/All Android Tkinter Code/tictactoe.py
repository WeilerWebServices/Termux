"""
=======================================================================
[SA] Sep-2017: Standalone release of PyCalc, PyClock, PyPhoto, PyToe.
Copyright 2017 M.Lutz, from book "Programming Python, 4th Edition".
License: provided freely, but with no warranties of any kind.
This is main logic; see tictactoe_lists.py for the meat of the system.
2.0: added DemoMode config: if True, displays N preset boards/games.

# ANDROID version, Jan 2019 (see "# ANDROID" for changes)
=======================================================================
"""

# [PP4E] this file has been updated for Python 3.X

import sys, copy    # ANDROID: tkinter import must be on a line by itself,
import tkinter      # ANDROID: else the GUI support is not loaded/present

from tictactoe_lists import *                      # move-mode subclasses
from tictactoe_lists import helpdisplay            # common help utility

from getConfigs import getConfigs                  # file-or-args configs 
from getConfigs import attrsToDict, dictToAttrs    # for passing **kargs 

# [SA] Mac and Linux port things
RunningOnMac     = sys.platform.startswith('darwin')
RunningOnLinux   = sys.platform.startswith('linux')
RunningOnWindows = sys.platform.startswith('win')

# [SA]: set window icons on Windows and Linux
from windowicons import trySetWindowIcon


#----------------------------------------------------------------------
# Game object generator - external interface 
#----------------------------------------------------------------------

def TicTacToe(root, Mode, **args):            # this consumes Mode
    classname = 'TicTacToe' + Mode            # e.g., -mode Minimax
    try:
        classobj = eval(classname)            # get class by string name
    except:
        print('Bad Mode option value:', mode)
        raise   # reraise
    else:                                     # [SA] was eval(classname)(**args)
        return classobj(root, **args)         # run class constructor (3.x: was apply())


#----------------------------------------------------------------------
# Configurations interface - from file or cmdline args, with defaults 
#----------------------------------------------------------------------

defaultConfigs = dict(
        DemoMode=False,                  # use preset boards?
        InitialSize=None,                # WxH, '200x300'
        BgColor='wheat',
        FgColor='black',
        Font=('courier', 50, 'bold'),    # use 'family...' if arg
        Degree=3,                        # 3 across = tic-tac-toe
        GoesFirst='user',                # 'user' or 'machine'
        UserMark='X',                    # 'X' or 'O'
        Mode='Minimax')                  # 5 classes in module


def userconfigs():
    """
    [SA] new common gadgets utility: file or cmdline
    e.g., python3 tictactoe.py -configs ~/myconfigs.py
    e.g., python3 tictactoe.py -Degree 4 -Mode Expert2 -Font 'menlo 40'
    """
    configs = getConfigs('PyToe', defaultConfigs)    # load from file or args
    configs.Degree = int(configs.Degree)             # str->int iff needed
    return configs


#----------------------------------------------------------------------
# Board builders - 1/configs for normal mode, N/presets for demo mode
#----------------------------------------------------------------------

def makeBoard(configs, kind=Tk):
    """
    create 1 board, according to configs
    """
    root = kind()
    trySetWindowIcon(root, 'icons', 'pygadgets')    # [SA] for win+lin
    if configs.InitialSize:                         # None size is probably best 
        root.geometry(configs.InitialSize)
    frm = TicTacToe(root, **attrsToDict(configs))   # build board frame on root
    if kind == Tk:
        setAppleReopen(root)   # works on Tk only, DemoMode is just one process

    # [SA] question=? but portable, help key in all gadgets
    root.bind('<KeyPress-question>', lambda event: helpdisplay(root))


def demoMode(configs):
    """
    create N boards per preset configs for variety and demo
    """
    class DemoWindow(GuiMakerWindowMenu):
        """
        a Frame on a simple Tk root: global help and quit, quit closes 
        all windows; boards are Toplevels: board=>quit closes just itself;
        """
        appname = 'PyToe'   # for new guimaker

        def start(self):
            self.helpButton = False
            # [SA] Mac OS help automatic in guimaker
            if not RunningOnMac:
                self.menubar = [('Help', 0, [('About', 0, self.onAbout, '*-h')] )]
    
        def makeWidgets(self):
            greeting = Label(self, text='Welcome to PyToe DemoMode', padx=5, pady=3)
            greeting.config(font=('times', 20, 'italic'))
            greeting.pack(expand=YES, fill=BOTH)
            greeting.bind('<Button-1>', lambda event: helpdisplay(root))   # for fun

        def onAbout(self):
            helpdisplay(self)
        onHelp = onAbout   # [SA] for Mac OS, new guimaker
        
    root = Tk()
    root.title('PyToe 2.0')
    trySetWindowIcon(root, 'icons', 'pygadgets')    # for Win+Lin
    setAppleReopen(root)                            # for Mac
    frm = DemoWindow(root)

    # [SA] question=? but portable, help key in all gadgets
    root.bind('<KeyPress-question>', lambda event: helpdisplay(root))

    # attrs may have been set in file or cmd
    teal = 'teal' if tkinter.TkVersion >= 8.6 else '#006e6d'  # in 8.6+
    modconfigs = [
        dict(Degree=5, Mode='Expert2', BgColor=teal,      FgColor='cyan'),
        dict(Degree=4, Mode='Expert2', BgColor='wheat',   FgColor='black'),
        dict(Degree=3, Mode='Minimax', BgColor='#173166', FgColor='white'),
        dict(Degree=2, Mode='Minimax', BgColor='#633025', FgColor='white')]

    # popup smallest last = on top: last made is drawn first
    # Linux scatters the boards, but best on all platforms
    if RunningOnMac or RunningOnWindows or RunningOnLinux:
        modconfigs = reversed(modconfigs)

    # overide settings or defaults
    for modconfig in modconfigs:
        democonfigs = attrsToDict(configs)
        democonfigs.update(modconfig)
        democonfigs = dictToAttrs(democonfigs)
        democonfigs.InitialSize = None
        makeBoard(democonfigs, kind=Toplevel)

    # else covered and not focused on Windows and Linux
    if RunningOnWindows or RunningOnLinux:
        root.focus()         # this works and suffices on both
        #frm.lift()          # root.lift leaves hidden on Windows
        #frm.focus_force()   # so does root.after_idle(root.lift)


def setAppleReopen(root):
    """
    configure standard events 
    """
    if RunningOnMac:
        # Mac requires menus, deiconifies, focus
        # [SA] reopen auto on dock/app click and fix tk focus loss on deiconify
        def onReopen():
            root.lift()
            root.update()
            temp = Toplevel()
            temp.lower()
            temp.destroy()
        root.createcommand('::tk::mac::ReopenApplication', onReopen)


#----------------------------------------------------------------------
# Main logic - fetch options from file or command-line, run game
#----------------------------------------------------------------------

if __name__ == '__main__': 
    configs = userconfigs()
    if configs.DemoMode:
        demoMode(configs)
    else:
        makeBoard(configs)
    mainloop()   # and wait for user to play...
