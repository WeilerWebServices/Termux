#!/usr/bin/python3
"""
=====================================================================================
frigcal.py (main script) - A basic refrigerator-style calendar desktop GUI.

Uses Python 3.X, tkinter, and portable iCalendar ".ics" files to store event data.
Copyright and author: © M. Lutz, 2014-2019, learning-python.com.

#------------------------------------------------------------------------------------
# ANDROID version, Jan-Apr 2019 (see "# ANDROID" for all changes)
# These changes may be merged into the original code in a later release.
#
# Recent changes (search for date to see changed code):
#
# [Apr2119] Pydroid 3 3.0 broke webbrowser: use os.system(cmd) with a 
#           hardcoded Android activity-manager command line instead
#           (3.0's $DISPLAY breaks module, $BROWSER kills "file://").
#
# [Apr1919] Go back to using Py's webbrowser for help's user guide: it does 
#           work, but iff files use '"file://" and HTML docs use online URLs;
#           see _openbrowser.py for a demo and more details.
#
# [Apr1219] Reenable "?" help button, and fix it to open the user guide with an
#           os.system() spawn of an Android activity-manager command instead of
#           webbrowser; open the online version of help, for its latest changes.
#           Also: set width of "mm/dd/yyyy" entry field to save some screen space,
#           and reduce font presets for month and buttons for small-phone fit.
#------------------------------------------------------------------------------------

Run this file to start the program; it uses other Python modules here and in folders.
frigcal can also be started by running "frigcal-launcher.pyw", which suppresses the
console window on Windows, and on all platforms issues a popup while files load.

Code structure: classes here for month windows and dialogs, ics file tools in module.
Most of the code is in this single file, to simplify searches (arguably, at least).

See UserGuide.html for all documentation: license, release, and usage details.
=====================================================================================
"""

print('Welcome to frigcal.')


# Python standard library
# [2.0] for standard dialogs on Mac OS X, use parent=window for slide-down,
# and focus_force() for refocus; custom dialogs are okay because transient()

import os, sys, calendar, datetime, time, traceback, webbrowser, mimetypes
from tkinter import *
from tkinter.messagebox import askokcancel, askyesno, showerror, showwarning
from tkinter.scrolledtext import ScrolledText

# for platform-specific choices
RunningOnMac     = sys.platform.startswith('darwin')       # all OS (X)
RunningOnWindows = sys.platform.startswith('win')          # all Windows
RunningOnLinux   = sys.platform.startswith('linux')        # all Linux


# 3rd-party: required for jpeg display (else just gifs, and png in Tk8.6+ (Py3.4+?) [1.6])

pillowwarning = """
Pillow 3rd-party package is not installed.
...This package is optional, but required for the month images feature when
...using some image file types and Pythons (though not for PNGs with Pythons
...that use Tk 8.6 or later, including standard Windows installs of Python 3.4+).
...Details - http://learning-python.com/books/python-changes-2014-plus.html#s359.
...To fetch Pillow - https://pypi.python.org/pypi/Pillow.
"""

try:
    from PIL.ImageTk import PhotoImage   # replace tkinter's version
except ImportError:
    print(pillowwarning)
    # but continue, and no popup yet (Image option will report any load errors in GUI)
    # [1.6] if no PIL, falls back on Tk/tkinter's native PhotoImage, for PNGs, GIFs, etc.


# [2.0] for frozen app/exes, fix module+resource visibility (sys.path)
import fixfrozenpaths

# local: ics files interface - init, parse, backup, save, update
import icsfiletools     # 3rd-party icalendar pkg required and used by this

# local: names used in both frigcal script and icsfiletools (avoid redundant code)
from sharednames import Configs, trace, PROGRAM, VERSION, startuperror

# local: a tkinter extension borrowed from Programming Python 4th Ed
from scrolledlist import ScrolledList

# local: part of PP4E's guimaker module, copied here to avoid dependency [2.0]
from guimaker_pp4e import fixAppleMenuBar

# more constants (others in sharednames)
PROTO    = False    # True = run initial prototype (now defunct)
MAXWEEKS = 6        # always show max poss size for simplicity (and visual clarity!)


# [2.0] data not in os.getcwd() if run from a cmdline elsewhere, and 
# __file__ may not work if running as a frozen PyInstaller executable;
# use __file__ of this file for Mac apps, not module: it's in a zipfile;

MYDIR    = fixfrozenpaths.fetchMyInstallDir(__file__)   # absolute
HELPFILE = os.path.join(MYDIR, 'UserGuide.html')

# [2.0] Mac OS X is pickier about file URLs
if RunningOnMac:
    HELPFILE = 'file:' + HELPFILE

# ANDROID [Apr1219] - use online version to pick up latest changes;
# other platforms should eventually do this too - web pages morph for browsers often
#
HELPURL = 'https://www.learning-python.com/frigcal-products/unzipped/UserGuide.html'

# [2.0] ensure running in script's folder for relative calendars, images,
# and icon pathnames: may have been launched from elsewhere via cmdline
# there are no possibly-relative command-line arguments to this script

os.chdir(MYDIR)


# globals, now mostly defunct: originally coded as simple funtions with globals,
# but that grew unmanageable at around 1K lines - classes provide much needed
# structure, and can support multiple month displays, a later addition (Clone);

# [MonthWindow()]: month windows open, >1 if Clone, for tandem moves and updates
OpenMonthWindows = []

# one Eventdata(), global to support cut/copy in one window and paste in another
CopiedEvent = None

# main data structures: parsed and indexed file data, used but not changed here
from icsfiletools import CalendarsTable     # {icsfilename: icalendar.Calendar()}
from icsfiletools import EventsTable        # {Edate(): {uid: EventData()} ]
from icsfiletools import CalendarsDirty     # {icsfilename: Boolean]

# data structure classes in EventsTable (see icsfiletools.py)
from icsfiletools import Edate, EventData

# ANDROID - avoid two (or more) modal dialog opens if multiple events for one gesture;
# pydroid 3's tkinter either triggers multiple events in parallel for a rightclick swipe,
# and/or has issues with the modal-dialog code here; the result is that there can be 2+ 
# cut/copy dialogs at once, or a cut/copy along with an event edit/view dialog that hangs;
# not clear what triggers this, but the global here is a quick work around for now;
# this may have to use a thread lock acquire/release if events are freethreaded (TBD);
#
EventDialogIsOpen = False


#====================================================================================
# Utility functions (multiple class clients)
#====================================================================================


# changeable defaults
BG_DEFAULT = 'white'
FG_DEFAULT = 'black'
FONT_DEFAULT = ('arial', 9, 'normal')


def configerrormsg(kind, value):
    """
    [1.7] factor this to common code (now too many copies)
    """
    print('Error in %s setting: %s - default used' % (kind, ascii(value)))
    print('Python error text follows:\n', '-' * 40)
    traceback.print_exc()
    print('-' * 40)


def tryfontconfig(widget, font):
    """
    don't fail and/or exit on bad configuration file settings - report and use
    a default font; this matters, because configs are user-edited Python module;
    """
    if font != None:   # None=tk default
        try:
            # ANDROID - (doc only) most fonts were preset to None in frigcal_configs.py 
            # to avoid crashes, but still allow users to reinstate those that work;
            # courier, helvetica, times, and a few synonyms work - all others crash; 
            #
            widget.config(font=font)
        except:
            widget.config(font=FONT_DEFAULT)
            configerrormsg('font', font)
            
    
def trybgconfig(widget, bg):
    """
    don't fail and/or exit on bad configuration file settings - report and use
    a default color; this matters, because configs are user-edited Python module;
    """
    if bg != None:   # None=tk default
        try:
            widget.config(bg=bg)
        except:
            widget.config(bg=BG_DEFAULT)
            configerrormsg('bg color', bg)


def tryfgconfig(widget, fg):
    """
    [1.7] added for bg + *fg* event text configuration, when color=('bg', 'fg');
    caveat: can leave black on black if black bg worked, but it's an error case; 
    """
    if fg != None:   # None=tk default
        try:
            widget.config(fg=fg)
        except:
            widget.config(fg=FG_DEFAULT)
            configerrormsg('fg color', fg)


def trybgitemconfig(listbox, index, bg):
    """
    [1.3] same, but item in new selection listbox, not an entry field
    """
    #[2.0] trace('trybgitemconfig', index, bg, listbox) 
    if bg != None:   # None=tk default
        try:
            listbox.itemconfig(index, bg=bg)
        except:
            listbox.itemconfig(index, bg=BG_DEFAULT)
            configerrormsg('bg color', bg)
            

def tryfgitemconfig(listbox, index, fg):
    """
    [1.7] added for bg + *fg* event text configuration, when color=('bg', 'fg');
    caveat: can leave black on black if black bg worked, but it's an error case;
    """
    #[2.0] trace('tryfgitemconfig', index, fg, listbox) 
    if fg != None:   # None=tk default
        try:
            listbox.itemconfig(index, fg=fg)
        except:
            listbox.itemconfig(index, fg=FG_DEFAULT)
            configerrormsg('fg color', fg)


def try_set_window_icon(window, iconname='frigcal'):
    """
    [1.2] replace a Tk() or Toplevel() window's generic Tk icon with a custom
    icon for this program;  this works on Windows (only?), and doesn't crash
    elsewhere;  applied to main window and all popup windows, including clones; 
    TBD: generalize for Linux, Macs -- this has always been platform-dependent;
    [1.6] use Tk 8.5+'s iconphoto() to set icon on Linux only (app bar icon);
    [2.0] recoded to rule out Mac explicitly, else a generic icon shows up;
    """
    icondir = 'icons'
    iconname += '.ico' if RunningOnWindows else '.gif'
    iconpath = os.path.join(icondir, iconname)
    try:
        if RunningOnWindows:
            # Windows (only?), all contexts
            window.iconbitmap(iconpath)
            
        elif RunningOnLinux:
            # Linux (only?), Tk 8.5+, app bar [1.6]
            imgobj = PhotoImage(file=iconpath)
            window.iconphoto(True, imgobj)
            
        elif RunningOnMac or True:
            # Mac OS X: neither of the above work [2.0]
            # on Macs, apps are required for most icon contexts
            raise NotImplementedError

    except Exception as why:
        pass   # bad file or platform


def fixTkBMP(text):
    """
    [2.0] (copied from PyMailGUI) Tk <= 8.6 cannot display Unicode characters
    outside the U+0000..U+FFFF BMP (UCS-2) code-point range, and generates
    uncaught exceptions when tried (emojis kill programs!).  To address this,
    call this function to sanitize all text passed to the GUI for display.
    It replaces any non-BMP characters with the standard Unicode replacement
    character U+FFFD, which Tk displays as a highlighted question mark diamond.
    
    This workaround is coded to assume that Tk 8.7 will lift the BMP restriction,
    per a dev rumor.  It also assumes TkVersion has been imported from tkinter.
    Use here: display calendar data created in other programs (rare, but true).
    Caveat: editing and saving such data will lose the characters thus replaced,
    though only in summary and description fields (others retain original text).
    Note: also must avoid Unicode in print() text as may fail on some consoles.
    """
    if TkVersion <= 8.6:
        text = ''.join((ch if ord(ch) <= 0xFFFF else '\uFFFD') for ch in text)
    return text 


#====================================================================================
# Month display window: main and clones
#====================================================================================

class MonthWindow:
    """
    the main display, with its state and callback handlers:
    - created by main() and Clone button, kept on OpenMonthWindows;
    - uses local ViewDateManager object to manage viewed date and days list;
    - creates local EventDialog subclass dialogs on user actions and pastes;
    - uses CalendarsTable and EventsTable globals, created by ics files parser;
    - subclassed to customize onQuit for popup Clone windows to close silently;
    """

    def __init__(self, root, startdate=None, windowtype='Main'):

        # window's state informaton
        self.root = root               # the Tk (or a Toplevel) main window, with root.bind
        self.monthlabel = None         # monthname label, for refills on navigation
        self.daywidgets = []           # [(dayframe, daynumlabel)], all displayed, for refills
        self.eventwidgets = {}         # {uid: evententry}, all displayed, for update/delete, refill
        self.tandemvar = None          # if get(), all windows respond to any prev/next navigate

        # set up current view date data
        self.viewdate = ViewDateManager()    # displayed month date and day-numbers list manager
        self.viewdate.settoday()             # initialize date object and days list to current date
        if startdate:
            self.viewdate.setdate('%s/%s/%4s' % startdate.mdy())

        # more options state information
        self.imgfiles = None                              # loaded month image file names [1.5]
        self.imgwin = self.imglab = self.imgobj = None    # for month images option only
        self.footerframe = self.footertext = None         # for optional footer text fill/toggle

        # build the window, register callbacks
        self.make_widgets(root, windowtype)
        self.fill_days()                        # make_widgets sets day callbacks once at build
        self.fill_events()                      # fill_event sets event callbacks on each refill
        OpenMonthWindows.append(self)           # global list of open windows for updates, tandem


    #------------------------------------------------------------------------------------
    # GUI builder
    #------------------------------------------------------------------------------------

    def make_widgets(self, root, windowtype):
        """
        build the calendar's month display, attached to root, retain month/days widgets;
        sets up day-related callback handlers for day widgets here, once, at build time; 
        """

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # WINDOW: title and color, close button, sizes, position, icon 
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # ANDROID - fill_days() adds month/day to title to accomodate shrunken windows,
        # but need to save window type on the window object here for use on navigation;      
        #
        self.windowtype = windowtype
        root.title('%s %.1f - %s' % (PROGRAM, VERSION, windowtype))
        trybgconfig(root, Configs.rootbg)

        # close button = backup/save ics file, only now and only if confirmed
        root.protocol('WM_DELETE_WINDOW', self.onQuit)
        
        # initial and minimum sizes, None=auto/none (see config file)
        if Configs.initwinsize:
            initsize = Configs.initwinsize
            if isinstance(initsize, str) and 'x' in initsize:
                # 'WxH' = 'intxint' = absolute pixel size ('WxH+X+Y' adds position)
                root.geometry(Configs.initwinsize)

            elif isinstance(initsize, float) and initsize <= 1.0:
                # float = % screen size
                scrwide = root.winfo_screenwidth()    # full screen size, in pixels
                scrhigh = root.winfo_screenheight()   # ditto (e.g., 1920, 1080)
                root.geometry('%dx%d' % (scrwide * initsize, scrhigh * initsize))

            elif isinstance(initsize, tuple):
                # (float, float) = (% screen wide, % screen high)
                scrwide = root.winfo_screenwidth()    # full screen size, in pixels
                scrhigh = root.winfo_screenheight()
                root.geometry('%dx%d' % (scrwide * initsize[0], scrhigh * initsize[1]))

            else:
                print('Bad initwinsize setting %s - ignored' % ascii(initsize))

        # minimum size: e.g., else some widgets may vanish if window shrunk
        if Configs.minwinsize:
            root.minsize(*Configs.minwinsize.split('x'))   # width, height
        
        # start position for all month windows (or at end of initwinsize) [1.2]
        # can be set separately and regardless of any prior geometry() calls
        if Configs.initwinposition: 
            root.geometry(Configs.initwinposition)         # '+X+Y' offset from top left
        
        # replace red (no, blue...) tk window icon if possible [1.2]
        try_set_window_icon(root)

        #----------------------------------------------------------------------------------
        # [1.4] minimize/restore image window with its month window, if enabled;
        # this treats an image window as a dependent extension to its month window;
        # subtle: tk issues hides/unhides during resizes too--must skip these for
        # widgets other than the month window itself (else resizes hide/unhide image);
        #
        # [1.5] on unhide, use focus_set to focus on month, not image, for keyboard
        # users, else requires a click to activate (e.g., for Esc); focus_set also lifts;
        #
        # [1.6] Caveat: Linux doesn't fire <Unmap>/<Map> events on minimize/restore
        # (and ditto for <configure>), so there is no good way to make this work on Linux;
        # must use withdraw() on Linux to restore later with deiconify(), but this seems
        # a moot point given the events issue; withdraw() also works on Windows, but the
        # image does not then appear in the taskbar with the month (TBD: preference?);
        #
        # [2.0] Update: Mac OS X correctly hides/unhides image windows with their month
        # windows using the code here, just like Windows (Linux is the only exception);
        # nits: on Mac (only), must call lift() after focus_set() or else the month window
        # must be clicked to raise it above image; either way, the month window must still
        # be clicked to restore its active-window styling when deiconified, but this is a
        # general Mac Tk issue (really, bug: see __main__ comment below) for all windows;
        # at least with image unhides, this requires just 1 click, not a click elsewhere;
        # UPDATE: focus_force() now sets month-window active styling without a user click;
        # UPDATE: see also __main__ logic that refocuses window when deiconified on Macs;
        #----------------------------------------------------------------------------------

        def onMonthHide(tkevent):
            if tkevent.widget == self.root:               # skip nested widget events
                trace('Got month hide')                   # self is in-scope here
                if self.imgwin:                           # iff img enabled/open
                    if RunningOnLinux:                    # but no <Unmap>/<Map> on Linux!
                        self.imgwin.withdraw()            # [1.6] works on Windows+Linux        
                    else:
                        self.imgwin.iconify()             # but then Linux can't deiconify!
                #self.root.iconify()                      # not root: tk does auto

        def onMonthUnhide(tkevent):
            if tkevent.widget == self.root:               # skip nested widget events
                trace('Got month unhide')                 # self is in-scope here
                if self.imgwin:                           # iff img enabled/open
                    self.imgwin.deiconify()               # open first=under (maybe)
                self.root.focus_set()                     # [1.5] month window focus+lift         
                #self.root.deiconify()                    # not root: tk does auto
                if RunningOnMac:                          # focus_set raises month above img
                    self.root.lift()                      # [2.0] but not on the Mac! - call
                    self.root.focus_force()               # [2.0] and activate without click

        root.bind('<Unmap>', onMonthHide)     # month minimize: image too
        root.bind('<Map>',   onMonthUnhide)   # month restore:  image too


        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # TOP: GoTo entry/button, Footer+Images toggles, Tandem/Clone, month+day names, help
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        datefrm = Frame(root)
        datefrm.pack(side=TOP, fill=X)
        trybgconfig(datefrm, Configs.rootbg)

        dateent = Entry(datefrm)
        dateent.insert(END, 'mm/dd/yyyy')
        dateent.pack(side=LEFT)
        dateent.bind('<Return>', lambda e: self.onGoToDate(dateent))  # not Enter: mousein

        # ANDROID [Apr1219] - fix/shrink width to reclaim some screen space on phones.
        # Also force monospace courier - tkinter should give enough room for 10 "0"s for
        # the default non-mono helvetica, but on some phones truncates the last char.
        # Caveat: this font's size should really be configurable, as a separate setting.
        #
        dateent.config(width=11)                   # 10 (+1 so can tap after last char)
        dateent.config(font='courier 7 normal')    # monospace, and large enough to read

        datebtn = Button(datefrm, text='GoTo', relief=RIDGE,          # ridge for all [1.2]
                         command=lambda: self.onGoToDate(dateent))
        datebtn.pack(side=LEFT)

        #tryfontconfig(dateent, Configs.controlsfont)    # ANDROID [Apr1219] forced above
        tryfontconfig(datebtn, Configs.controlsfont)     # ANDROID [Apr1219] smaller preset

        # help='?': pop up the html help file in a web browser [1.2];
        #
        # ANDROID [Apr1219]: Py webbrowser does not work on Android (yet?), 
        # so spawn a shell command using the $BROWSER preset in Pydroid 3:
        # "am start --user 0 -a android.intent.action.VIEW -d %s".
        # ANDROID [Apr1919]: webbrowser works if use an online URL for HTML.
        # ANDROID [Apr2119]: not anymore in Pydroid 3 3.0 - back to os.system.
        #
        brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
        helpbtn = Button(datefrm, text='?', relief=RIDGE,
                         command=lambda: os.system(brw % HELPURL))
                        #command=lambda: webbrowser.open(HELPURL))
                        #command=lambda: webbrowser.open(HELPFILE))

        helpbtn.pack(side=RIGHT)
        tryfontconfig(helpbtn, Configs.controlsfont)
        #helpbtn.config(state=DISABLED)    # ANDROID [Apr1219] - webbrowser failed initially

        # [2.0] a single '?' is almost too small to click on Mac OS X (only)
        if RunningOnMac:
            helpbtn.config(text=' ? ')

        spacer = Label(datefrm, text='')
        spacer.pack(side=RIGHT)
        trybgconfig(spacer, Configs.rootbg)

        # option checkbuttons, tandem clones checkbuton, and Clone
        clonebtn = Button(datefrm, text='Clone', relief=RIDGE, command=self.onClone)
        clonebtn.pack(side=RIGHT)

        tndvar = IntVar()
        tndtoggle = Checkbutton(datefrm, text='Tandem', relief=RIDGE,
                        variable=tndvar, command=lambda: self.onTandemFlip(tndvar))
        tndtoggle.pack(side=RIGHT)

        tryfontconfig(clonebtn,  Configs.controlsfont)
        tryfontconfig(tndtoggle, Configs.controlsfont)

        if OpenMonthWindows:
            # pick up current tandem setting from first, if others open
            # possible alternative: use a single, global, shared IntVar
            tndvar.set(OpenMonthWindows[0].tandemvar.get())

        # the next two toggles apply to this window only
        spacer = Label(datefrm, text='', )
        spacer.pack(side=RIGHT)
        trybgconfig(spacer, Configs.rootbg)
        
        imgvar = IntVar()
        imgtoggle = Checkbutton(datefrm, text='Images', relief=RIDGE,
            variable=imgvar, command=lambda: self.onImageFlip(imgvar))
        imgtoggle.pack(side=RIGHT)
        
        ftrvar = IntVar()
        ftrtoggle = Checkbutton(datefrm, text='Footer', relief=RIDGE,
            variable=ftrvar, command=lambda: self.onFooterFlip(ftrvar))
        ftrtoggle.pack(side=RIGHT)

        tryfontconfig(imgtoggle, Configs.controlsfont)
        tryfontconfig(ftrtoggle, Configs.controlsfont)
            
        # month name and year (on datefrm not root), day names row
        monthlabel = Label(datefrm, text='Month YYYY', font=('times', 12, 'bold italic'), fg='white')
        monthlabel.pack(side=TOP)
        trybgconfig(monthlabel,   Configs.rootbg)
        tryfontconfig(monthlabel, Configs.monthnamefont)   # ANDROID [Apr1219] smaller preset
        
        daynames = Frame(root)
        daynames.pack(side=TOP, fill=X)
        trybgconfig(daynames, Configs.rootbg)

        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for dayname in days:
            dayname = Label(daynames, text=dayname, fg='white')
            dayname.pack(side=LEFT, expand=YES)
            trybgconfig(dayname,   Configs.rootbg)
            tryfontconfig(dayname, Configs.daynamefont)


        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # BOTTOM: mo/yr navigation buttons = keys (pack first = clip last!: retain on resizes)
        # when enabled, the Footer shows up above these and below the middle days grid
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        toolbar = Frame(root)
        toolbar.pack(side=BOTTOM, fill=X)
        trybgconfig(toolbar, Configs.rootbg)

        toolbtns = [('PrevYr', LEFT,  self.onPrevYearButton),     # packing order matters
                    ('NextYr', LEFT,  self.onNextYearButton),     # expand=YES to space
                    ('NextMo', RIGHT, self.onNextMonthButton),
                    ('PrevMo', RIGHT, self.onPrevMonthButton),    # expand=YES to space   
                    ('Today',  TOP,   self.onTodayButton)]        # today shows up in middle

        for (text, side, handler) in toolbtns:
            btn = Button(toolbar, text=text, relief=RIDGE, command=handler)
            btn.pack(side=(side or TOP))
            tryfontconfig(btn, Configs.controlsfont)

        # keys = mo/yr navigation buttons (with extra event arg)
        # these used to be <Left>/<Right>, but then not usable to edit summary text!
        # map to more descriptive callback names of buttons, not vice-versa [1.3]
        root.bind('<Up>',         lambda tkevent: self.onPrevMonthButton())    
        root.bind('<Down>',       lambda tkevent: self.onNextMonthButton()) 
        root.bind('<Shift-Up>',   lambda tkevent: self.onPrevYearButton())    # Shift + arrow
        root.bind('<Shift-Down>', lambda tkevent: self.onNextYearButton())
        root.bind('<Escape>',     lambda tkevent: self.onTodayButton())       # [1.5] Esc=Today


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # MIDDLE: expandable month of [weeks of days] (pack last = clip first!)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        alldaysfrm = Frame(root)
        alldaysfrm.pack(side=TOP, expand=YES, fill=BOTH)
        daywidgets = []
        for week in range(MAXWEEKS):
            for day in range(7):
                reldaynum = (week * 7) + day
                dayfrm = Frame(alldaysfrm, border=2, relief=RAISED)      # not Label! (an early bug)
                dayfrm.grid(row=week, column=day, stick=NSEW)
                daylab = Label(dayfrm, text=str(reldaynum))              # initial value, reset later
                daylab.pack(side=TOP, fill=X)                            # events entries added later

                trybgconfig(dayfrm,   Configs.daysbg)
                trybgconfig(daylab,   Configs.daysbg)
                tryfontconfig(daylab, Configs.daysfont)

                self.register_day_actions(dayfrm, daylab, reldaynum)     # once, when window built
                daywidgets.append((dayfrm, daylab))                      # save for gui updates

        # all same resize priority, uniform size groups
        for week in range(MAXWEEKS):
            alldaysfrm.rowconfigure(week, weight=1, uniform='a')
        for day in range(7):
            alldaysfrm.columnconfigure(day, weight=1, uniform='a')

        # save state for callbacks
        self.monthlabel, self.daywidgets, self.tandemvar = monthlabel, daywidgets, tndvar


    def register_day_actions(self, dayfrm, daylab, reldaynum):
        """
        day events registered once on month window build, for both num and frame;
        event events registered later in fill_events, and on each navigation;
        don't need var=var defaults in lambdas: not using var in loop's scope here!
        
        single or double left-click (press) on day = open add event dialog for day;
        single-right-click (press+hold) on day = paste cut/copy event on day;
        both events ignored later if click on day not in current viewed month;
        use double-click for mouse mode left-click: more natural and same as events;

        [1.3] specialize day number to open listbox of all events in day, in case
        there are too many to display in the day's widget of the month window; the
        listbox is modal to avoid the need to update potentially many, and includes
        a 'create' button for adding a new event on this day via the Create dialog
        as a fallback option, just like a click on the day's background in general;
        """
        # daylab.config(border=1)   # or should this be a button? see callback
        
        # day left-clicks: differ
        if Configs.clickmode == 'touch':
            # single: open create-event or select-event [1.3] dialogs (moves shade)
            dayfrm.bind('<Button-1>', lambda e: self.onLeftClick_Day__Create(reldaynum))
            daylab.bind('<Button-1>', lambda e: self.onLeftClick_DayNum__Select(reldaynum))

        elif Configs.clickmode == 'mouse':
            # single: move current day shade only [1.2]
            dayfrm.bind('<Button-1>', lambda e: self.set_and_shade_rel_day(reldaynum))
            daylab.bind('<Button-1>', lambda e: self.set_and_shade_rel_day(reldaynum))

            # double: open create-event or select-event [1.3] dialogs (moves shade)
            dayfrm.bind('<Double-1>', lambda e: self.onLeftClick_Day__Create(reldaynum))
            daylab.bind('<Double-1>', lambda e: self.onLeftClick_DayNum__Select(reldaynum))
       
        # single right, day and daynum, both modes: paste via prefilled create dialog
        dayfrm.bind('<Button-3>', lambda e: self.onRightClick_Day__Paste(reldaynum))
        daylab.bind('<Button-3>', lambda e: self.onRightClick_Day__Paste(reldaynum))

        # [2.0] on Mac OS X, also allow Control-click as an equivalent for right-click,
        # and support Mac mice that trigger Button-2 on right button click (on Macs,
        # right=Button-2 and middle=Button-3; it's the opposite on Windows and Linux!)
        
        # ANDROID - +True: enables pydroid 3 rightclick = drive-by swipe
        if True or RunningOnMac:
            dayfrm.bind('<Control-Button-1>', lambda e: self.onRightClick_Day__Paste(reldaynum))
            daylab.bind('<Control-Button-1>', lambda e: self.onRightClick_Day__Paste(reldaynum))

            dayfrm.bind('<Button-2>', lambda e: self.onRightClick_Day__Paste(reldaynum))
            daylab.bind('<Button-2>', lambda e: self.onRightClick_Day__Paste(reldaynum))            


    #------------------------------------------------------------------------------------
    # GUI content filler: days
    #------------------------------------------------------------------------------------

    def fill_days(self, prototype=PROTO):
        """
        given window's viewdate, fill calendar's month name and day numbers;
        maps relative day grid indexes to true day numbers received from stdlib;
        doesn't register day widget callbacks: done at build time for reldaynum;
        """
        if prototype:
            # show mocked-up month (defunct)
            self.monthlabel.config(text='Somemonth 2014')
            for (count, (dayframe, daynumlabel)) in enumerate(self.daywidgets):
                daynumlabel.config(text=str(count))

        else:
            # fill-in month for current view date
            # day click events already registered in make_widgets

            # reset all days' colors
            for (dayframe, daynumlabel) in self.daywidgets:
                self.colorize_day(dayframe)
                self.colorize_day(daynumlabel)

            # set month name at top
            moname = calendar.month_name[self.viewdate.month()]
            motext = '%s %s' % (moname, self.viewdate.year())
            self.monthlabel.config(text=motext)

            # ANDROID - add ": mmm yyyy" to title for smaller windows on phones,
            # else month label may be truncated - and window's content unknown... 
            #
            self.root.title('%s %.1f - %s: %s %s' % 
                (PROGRAM, VERSION, self.windowtype, 
                 calendar.month_abbr[self.viewdate.month()],    # use 3-letter form
                 self.viewdate.year()) )                        # this window's year

            # set true day numbers, erase nondays            
            numsandwidgets = zip(self.viewdate.currdays, self.daywidgets)
            for (daynum, (dayframe, daynumlabel)) in numsandwidgets:
                if not self.viewdate.trueday_is_in_month(daynum):
                    dayframe.config(bg='black')
                    daynumlabel.config(bg='black')
                else:
                    daynumlabel.config(text=str(daynum))

            # shade current day of this window
            self.prior_shaded_day = None
            self.shade_current_day()


    def colorize_day(self, widget):
        # TBD: default isn't clear: require a config setting?
        if Configs.daysbg:
            trybgconfig(widget, Configs.daysbg)          # user choice first?
        else:
            try:
                widget.config(bg='SystemButtonFace')     # default on Win+Mac; others?
            except:
                widget.config(bg=Configs.GRAY)           # else a reasonable default? [1.6]


    def shade_current_day(self, shadecolor=Configs.currentdaycolor):
        """
        called by fill_days (create/navigate), and after any day/event click;
        for window-specific day only (even if other windows on same month);
        [1.6] allow shade color config (was 'gray' that changed in Tk 8.6);
        """
        # unshade prior shaded day frame
        if self.prior_shaded_day:
            self.colorize_day(self.prior_shaded_day)
        
        # shade frame for new/current day of this month
        reldaynum = self.viewdate.day_to_index(self.viewdate.day())
        thisdayframe, thisdaynumlabel = self.daywidgets[reldaynum]
        thisdayframe.config(bg=shadecolor or Configs.GRAY)   # default if not set
        self.prior_shaded_day = thisdayframe


    def set_and_shade_day(self, truedaynum):
        """
        on day and event left/right clicks: move current day shading;
        daynum is true day, not index (event clicks have true only);
        """
        self.viewdate.setday(truedaynum)
        self.shade_current_day()


    def set_and_shade_rel_day(self, reldaynum):
        """
        on day single-left-click in 'mouse' mode [1.2];
        may be set > once on double-clicks, but harmless,
        and onLeftClick_Day/DayNum also used by 'touch'
        mode single-clicks and wouldn't trigger this auto;
        """
        if self.viewdate.relday_is_in_month(reldaynum):        # a true day in displayed month?
            trueday = self.viewdate.index_to_day(reldaynum)    # convert to actual day number
            self.set_and_shade_day(trueday)


    #------------------------------------------------------------------------------------
    # GUI content filler: events
    #------------------------------------------------------------------------------------

    def fill_events(self, prototype=PROTO):
        """
        given month+year of viewdate, fill calendar's days with any/all events' labels;
        the events table has the union of all calendars' events, indexed by true date;
        sets up event-related callback handlers for event widgets here, on each refill; 
        """
        # erase month's current displayed event entry widgets from day frames
        for efld in self.eventwidgets.values():    
            efld.destroy()                           # pack_forget() retains memory
        self.eventwidgets = {}

        if prototype:
            # show mocked-up event labels
            prototype_events(self.daywidgets)
            return  # minimize indents
        
        # fill-in events from ics file data
        monthnum = self.viewdate.month()                               # displayed month
        yearnum  = self.viewdate.year()                                # displayed year
        numsandwidgets = zip(self.viewdate.currdays, self.daywidgets)

        for (daynum, (dayframe, daynumlabel)) in numsandwidgets:       # for all days/labels displayed
            if self.viewdate.trueday_is_in_month(daynum):              # a real day in this month (or 0)? 
                edate = Edate(monthnum, daynum, yearnum)               # make true date of dayframe
                if edate in EventsTable.keys():                        # any events for this day?

                    dayeventsdict = EventsTable[edate]                 # events on this date (uid table) 
                    dayeventslist = list(dayeventsdict.values())       # day's event object (all calendars)
                    dayeventslist.sort(
                               key=lambda d: (d.calendar, d.orderby))  # order for gui by calendar + creation 

                    for icsdata in dayeventslist:                      # for all ordered events in this day
                        # continue in separate method
                        self.add_event_entry(dayframe, edate, icsdata)


    def add_event_entry(self, dayframe, edate, icsdata):
        """
        for one event: create summary entry, register its event handlers;
        separate (but not static) so can reuse for event edit dialog's Add;

        Nov15: @staticmethod not required here, as this method always needs a
        self (MonthWindow) argument, regardless of how and where it's called;
        """
        # add editable summary text to day frame
        efld = Entry(dayframe, relief=RIDGE)         # no color yet
        efld.pack(side=TOP, fill=X) 
        tryfontconfig(efld, Configs.daysfont)
        efld.insert(0, fixTkBMP(icsdata.summary))    # [2.0] Unicode replace

        # [2.0] Mac OS X adds too much extra space around event entries
        if RunningOnMac:
            #efld.config(borderwidth=2)
            efld.config(highlightthickness=0)

        # colorize field: category overrides calendar
        category, calendar = icsdata.category, icsdata.calendar
        self.colorize_event(efld, category, calendar)

        # event-specific and footer-related actions: mouse/kb or touch
        self.register_event_actions(efld, edate, icsdata)

        # save for erase on delete, cut, navigate
        self.eventwidgets[icsdata.uid] = efld  


    @staticmethod
    def colorize_event(entry, category, calendar):
        """
        set one event's summary color per config file tables;
        category overrides calendar (and category '' = all other, despite calendar);
        static and separate so can reuse for event edit dialog's Update (category change);
        [1.7] add foreground color configuration when color is a tuple (str still means bg);

        in 3.X, @staticmethod is optional if called through class only (and never through
        self), but the decorator helps make the method's external visibility more explicit;
        statics simply supress self for through-instance calls: they are not c++ "public",
        but support method calls with no instance argument from same or other classes; 
        """
        color = MonthWindow.pick_event_color(category, calendar)   # no self to pass here
        if isinstance(color, str):
            trybgconfig(entry, color)                              # color='bg' [None=>dflt]
            tryfgconfig(entry, FG_DEFAULT)                         # reset to dflt if changed 
            bgcolor = color                   # ANDROID
        elif isinstance(color, tuple):
            trybgconfig(entry, color[0])                           # color=('bg', 'fg') [1.7]
            tryfgconfig(entry, color[1])
            bgcolor = color[0]                # ANDROID
        else:
            print('Warning: color setting: %s is not str=bg or tuple=(bg, fg)' % ascii(color))
            trybgconfig(entry, color)                              # use common error handler
            tryfgconfig(entry, FG_DEFAULT)
            bgcolor = color                   # ANDROID

        # ANDROID - avoid keyboard opens on event taps in default touch mode;
        # with readonly, no <return 'break'> is required in the click handler,
        # which seems to retain focus (and keyboard) if widget scroll is reset;
        # readonly avoids focus, but also requires readonlybackground else grey;
        # still must reset the widget in tap handler to remove selection/scroll;
        #
        if Configs.clickmode == 'touch':
            try:
                entry.config(readonlybackground=bgcolor)
                entry.config(state='readonly')
            except:
                pass  # already got a message


    def colorize_listitem(self, listbox, index, category, calendar):
        """
        [1.3] set one list item's summary color per config file tables;
        [1.7] add foreground color configuration when color is a tuple (str still means bg);
        """
        color = self.pick_event_color(category, calendar)          # use self if there is one
        if isinstance(color, str):
            trybgitemconfig(listbox, index, color)                 # color='bg' [None=>dflt]
            tryfgitemconfig(listbox, index, FG_DEFAULT)            # reset to dflt if changed
        elif isinstance(color, tuple):
            trybgitemconfig(listbox, index, color[0])              # color=('bg', 'fg') [1.7]
            tryfgitemconfig(listbox, index, color[1])
        else:
            print('Warning: color setting: %s is not str=bg or tuple=(bg, fg)' % ascii(color))
            trybgitemconfig(listbox, index, color)                 # use common error handler
            tryfgitemconfig(listbox, index, FG_DEFAULT)


    @staticmethod
    def pick_event_color(category, calendar):
        """
        [1.3] select color for event, by category or then calendar;
        factored out because now also needed for selection list items;
        this must be static because colorize_event caller is: no self;
        False value or non-match to categories or calendars => default;
        """
        color = None                                             # None=Tk default? (defunct)
        catkeys   = list(Configs.category_colors.keys())         # need list() for poss .index()
        catvalues = list(Configs.category_colors.values())       # need list() for poss []

        if Configs.category_ignorecase:
            # neutralize case in both
            category = category.lower()                          # or .caseless()=.lower()+Unicode
            catkeys  = [catname.lower() for catname in catkeys]
            
        if category in catkeys:                                  # 'in' works on list or iterable
            color = catvalues[catkeys.index(category)]           # list() required for both here
        else:
            # must match filename case
            if calendar in Configs.calendar_colors:
                 color = Configs.calendar_colors[calendar]       # this is a dict key index
                 
        return color or BG_DEFAULT   # default if no category/calendar match (str = bg only)
        

    def register_event_actions(self, efld, edate, icsdata):
        """"
        register mouse-mode or touch-mode actions on event entry display;
        day events are registered once at gui build time by make_widgets;
        don't need var=var defaults in lambdas here: not using a var in loop's scope! 

        in mouse mode: <Button-1> event single left-click or press = built-in
        focus for edit (and hover-in if touch), and <Return> performs the update;

        in touch mode: <Double-1> double left-click unusable - single-click run
        first and its dialog precludes doubles; could time clicks, but overkill;

        in both modes: paste is via right-click on day, not event, and don't clear
        Footer on mouse <Leave> - some text may require later scrolling
        """
        if Configs.clickmode == 'mouse':
            # event double-left-click or double-press: open view/edit dialog
            efld.bind('<Double-1>',
                      lambda e: self.onLeftClick_Event__Edit(edate, icsdata, efld))

            # event Enter-key-press (after <Button-1> focus): update summary text only
            efld.bind('<Return>',
                      lambda e: self.onReturn_Event__Update(efld, icsdata))

        elif Configs.clickmode == 'touch':
            # event single-left-click or single-press: fill footer AND open view/edit

            # ANDROID - (doc only) formerly <return 'break'> (via <'break')[2]>) but that 
            # cannot remove focus if selection/scroll is reset, and keyboard opens anyhow;
            # instead: used readonly mode, and reset widget state in callback handlers;
            #
            efld.bind('<Button-1>',
                      lambda e: (self.onEnter_Event__Footer(edate, icsdata),
                                 self.onLeftClick_Event__Edit(edate, icsdata, efld)) ) 

        # both: event single-right-click, or press+hold: cut/copy/open (paste on day)
        efld.bind('<Button-3>',
                  lambda e: self.onRightClick_Event__CutCopy(e, edate, icsdata, efld))   # ANDROID: +efld

        # both: event mouse-hover-in, if you have one: fill Footer (description or not)
        efld.bind('<Enter>',
                  lambda e: self.onEnter_Event__Footer(edate, icsdata))

        # [2.0] on Mac OS X, also allow Control-click as an equivalent for right-click,
        # and support Mac mice that trigger Button-2 on right button click (on Macs,
        # right=Button-2 and middle=Button-3; it's the opposite on Windows and Linux!)

        # ANDROID - +True to enable pydroid 3 rightclick = drive-by swipe
        if True or RunningOnMac:
            efld.bind('<Control-Button-1>',
                  lambda e: self.onRightClick_Event__CutCopy(e, edate, icsdata, efld))   # ANDROID: +efld
            
            efld.bind('<Button-2>',
                  lambda e: self.onRightClick_Event__CutCopy(e, edate, icsdata, efld))   # ANDROID: +efld


    def prototype_events(self, daywidgets):
        """
        show mocked-up event labels
        defunct and no longer mantained: see etc\frigcal--preclasses.py for original code
        """
        pass


    #------------------------------------------------------------------------------------
    # Exit: verify, backup, save
    #------------------------------------------------------------------------------------

    def onQuit(self):
        """
        => main window quit/close "X" button: [backup, then save]?, then [exit]?
        backup current ics file(s), then save new data (only after verify+backup!);
        saves changed files only, but don't even ask if there have been no changes [1.1];
        only the main month window does backup/save: clone windows are erased silently;
        """
        # backup+save?
        if any(CalendarsDirty.values()):                   # else don't even ask [1.1]
            answer = askyesno('Verify %s save' % PROGRAM,
                              'Backup and save changed calendar files now?',
                              parent=self.root)            # [2.0] Mac slide-down, don't lift root
            if answer:
                trace('backup/save')
                if icsfiletools.backup_ics_files():        # catches+shows own errors, False=failed
                    icsfiletools.generate_ics_files()      # catches+shows own errors (TBD: do here?)

        # exit program?
        answer = askokcancel('Verify %s exit' % PROGRAM,
                             'Really quit frigcal now?',
                             parent=self.root)             # [2.0] Mac slide-down, don't lift root
        if answer:
            # exit now, backp/save or not
            trace('exit')
            self.root.quit()          # close all windows and end program (mainloop())
        else:
            self.root.focus_force()   # [2.0] else user must click on Mac to activate


    #------------------------------------------------------------------------------------
    # Date navigation callbacks (keys + buttons + entry)
    #------------------------------------------------------------------------------------

    def refill_display(self):
        self.fill_days()
        self.fill_events()
        self.showImage()           # image for new month
        self.clearfooter()         # TBD: clear (or retain?--see method) 


    # [1.3] use descriptive callbacks names, to which keys are mapped
    
    def onNextMonthButton(self):
        """
        => button or arrow-key: display next month (all windows if tandem)
        """
        trace('Got NextMo/DownArrow')
        if not self.tandemvar.get():
            self.viewdate.setnextmonth()         # move just this window
            self.refill_display()
        else:
            for window in OpenMonthWindows:      # else all open windows move
                window.viewdate.setnextmonth()   # move this window
                window.refill_display()
                        
    def onPrevMonthButton(self):
        """
        => button or arrow-key: display previous month (all windows if tandem)
        """
        trace('Got PrevMo/UpArrow')
        if not self.tandemvar.get():
            self.viewdate.setprevmonth()
            self.refill_display()
        else:
            for window in OpenMonthWindows:     
                window.viewdate.setprevmonth()  
                window.refill_display()
          
    def onNextYearButton(self):
        """
        => button or arrow-key: display next year (all windows if tandem)
        """
        trace('Got NextYr/ShiftDownArrow')
        if not self.tandemvar.get():
            self.viewdate.setnextyear()
            self.refill_display()
        else:
            for window in OpenMonthWindows:     
                window.viewdate.setnextyear()  
                window.refill_display()

    def onPrevYearButton(self):
        """
        => button or arrow-key: display previous year (all windows in Tandem)
        """
        trace('Got PrevYr/ShiftUpArrow')
        if not self.tandemvar.get():
            self.viewdate.setprevyear()
            self.refill_display()
        else:
            for window in OpenMonthWindows:     
                window.viewdate.setprevyear()  
                window.refill_display()


    def onTodayButton(self):
        """
        => button or Esc-key: display today's date (this window only) 
        """
        trace('Got TodayPress')
        self.viewdate.settoday()    
        self.refill_display()

    def onGoToDate(self, dateent):
        """
        => GoTo or Enter-key in date: display entered date (this window only) 
        [2.0] parent=window for Mac slide-down, focus_force for Mac refocus
        """
        trace('Got GoToDate:', dateent.get())
        if not self.viewdate.setdate(dateent.get()):
            showerror('%s: date format error' % PROGRAM,
                      'Please enter a valid date as "MM/DD/YYYY".',
                      parent=self.root)
            self.root.focus_force()
        else:
            self.refill_display()

            
    #------------------------------------------------------------------------------------
    # Event edits: in memory (till file save on exit)
    #------------------------------------------------------------------------------------

    #
    # DAY AND DAYNUM CLICKS
    #
    
    def onLeftClick_Day__Create(self, reldaynum):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         => left click (or press) on day frame outside events
        open add new event dialog for this day to create event;
        
        this day is now also selected in GUI and set in viewdate
        manually here, as this may be run by single or double click;
        
        Resolved: a listbox of day's events may be useful if too many to see?
          =>addressed in [1.3] with a popup on daynum clicks: see next method;
        Resolved: should handlers be named by event trigger or action they take?
          =>addressed in [1.3] by callback names having both trigger+__action;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got Day LeftClick', reldaynum)
        if self.viewdate.relday_is_in_month(reldaynum):        # a true day in displayed month?
            trueday = self.viewdate.index_to_day(reldaynum)
            clickdate = Edate(month=self.viewdate.month(),
                              day=trueday,
                              year=self.viewdate.year()) 
            self.set_and_shade_day(trueday)
            AddEventDialog(self.root, clickdate)


    def onLeftClick_DayNum__Select(self, reldaynum):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => left click (or press) on day number area above any events
        [1.3] this is a new handler that opens day's events selection listbox,
        with 'create' button; dialog is modal, to avoid update issues if many;
        in list, left-double => edit dialog, right-single => cut/copy dialog,
        like event clicks in day frame (left-single simply selects item);

        this day is now also selected in GUI and set in viewdate
        manually here, as this may be run by single or double click;

        TBD: should the daynum be a button instead of label to make it more obvious?
        at present, no: because button takes up more space, limiting number events;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got DayNum LeftClick', reldaynum)
        if self.viewdate.relday_is_in_month(reldaynum):        # a true day in displayed month?
            trueday = self.viewdate.index_to_day(reldaynum)
            clickdate = Edate(month=self.viewdate.month(),
                              day=trueday,
                              year=self.viewdate.year()) 
            self.set_and_shade_day(trueday)
            if not clickdate in EventsTable.keys():            # any events for this day?
                AddEventDialog(self.root, clickdate)           # no: go to create dialog now
            else:
                # open list dialog for all [1.3]
                SelectListDialog(self, clickdate)              # [1.4] moved to a class
                                

    def onRightClick_Day__Paste(self, reldaynum):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => right click (or press+hold) on day or daynum
        paste latest cut/copy event on this day via prefilled dialog;
        reuses create dialog to allow calendar selection and cancel;
        
        pastes are performed by right-clicks on day/daynum after
        an earlier right-click on an event to cut/copy the event;

        [2.0] parent=window for Mac slide-down, focus_force for Mac refocus
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        global CopiedEvent
        trace('Got Day RightClick', reldaynum)
        if self.viewdate.relday_is_in_month(reldaynum):
            if not CopiedEvent:
                showerror('%s: no event to paste' % PROGRAM,
                          'Please cut/copy before paste',
                          parent=self.root)
                self.root.focus_force()
            else:
                trueday = self.viewdate.index_to_day(reldaynum)
                clickdate = Edate(month=self.viewdate.month(),
                                  day=trueday,
                                  year=self.viewdate.year())
                self.set_and_shade_day(trueday)
                # default to this event's calendar 
                AddEventDialog(self.root, clickdate, titletype='Paste',
                               icsdata=CopiedEvent, initcalendar=CopiedEvent.calendar)

    #
    # EVENT CLICKS AND RETURNS
    #
    
    def onLeftClick_Event__Edit(self, edate, icsdata, efld=None):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => left click (or press) on event
        open view/update/delete edit dialog for event;
        
        event clicks/presses vary per mouse|touch mode: may be called for
        single or double click; also called for right-click Open: efld is None;
        bypassed by select list clicks: opens edit dialog directly [1.3];

        TBD: clear selection on entry?, else may retain word highlight after
        double-clicks in 'mouse' mode; efld is the entry widget on left-clicks,
        but None for Open in right-click menu (no highlight to be cleared);
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        # ANDROID - see global def
        global EventDialogIsOpen
        if EventDialogIsOpen:
            trace('Spurious Event LeftClick')
            return
        else:
            EventDialogIsOpen = True
            trace('Got Event LeftClick')

        #if efld: efld.selection_clear()     # else a clicked word left highlighted
        self.set_and_shade_day(edate.day)
        icsfilename = icsdata.calendar
        EditEventDialog(self.root, edate, icsfilename, icsdata)

        # ANDROID - dialog may delete event, but must do last to take effect:
        # check for existence; select_clear is a synonym for selection_clear;
        #
        if Configs.clickmode == 'touch' and efld and efld.winfo_exists():
            efld.select_clear()    # ANDROID - remove selection (may be moot for readonly)
            efld.xview(0)          # ANDROID - remove scroll (or xview_scroll(-999, UNITS))

        # ANDROID - see global def
        EventDialogIsOpen = False


    def onRightClick_Event__CutCopy(self, tkevent, edate, icsdata, efld=None):     # ANDROID - +efld
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => right click (or press+hold) on Event
        open copy/cut/open menu dialog for this event;
        Cut reuses Delete code, Open reuses LeftClick code;
        
        cut/copy is run by right-click on event, and paste of
        the event is run by later right-clicks on day/daynum;

        also has Open option: equivalent to an event left-click,
        but must first cancel the diaog here, because event may be
        deleted in the Open dialog, invalidating a later cut here;

        TBD: probably should be a balloon-type text, not a dialog;
        TBD: could use drag-and-drop, but error prone (see tablets!);
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        # ANDROID - see global def
        global EventDialogIsOpen
        if EventDialogIsOpen:
            trace('Spurious Event LeftClick')
            return
        else:
            EventDialogIsOpen = True
            trace('Got Event LeftClick')

        trace('Got Event RightClick')
        self.set_and_shade_day(edate.day)
        CutCopyDialog(self, tkevent, edate, icsdata)   # [1.4] moved to class

        # ANDROID - dialog may delete event, but must do last to take effect:
        # check for existence; select_clear is a synonym for selection_clear;
        #
        if Configs.clickmode == 'touch' and efld and efld.winfo_exists():
            efld.select_clear()    # ANDROID - remove selection (may be moot for readonly)
            efld.xview(0)          # ANDROID - remove scroll (or xview_scroll(-999, UNITS))

        # ANDROID - see global def
        EventDialogIsOpen = False    # also cleared before cut/copy dialog's Open


    def onReturn_Event__Update(self, efld, icsdata):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => Enter key press on event field with focus
        update event's summary text only from current field text;

        updates summary in both gui and data structures=calendar+index
        like all updates, propogates to all windows open on this month;
        caveat: does not update any footer text (but should it?)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got Event Return')
        newsummary = efld.get()

        # data strucures
        icsdata.summary = newsummary                            # update index data (in-place!)
        icsfiletools.update_event_summary(icsdata, newsummary)  # update icalendar data (in-place!)

        # gui
        for ow in OpenMonthWindows:                       # update other gui windows?
            if icsdata.uid in ow.eventwidgets.keys():     # no need to match viewdate
                entry = ow.eventwidgets[icsdata.uid]      # set this entry in this window
                if entry != efld:
                    entry.delete(0, END)                  # else adds to current text
                    entry.insert(0, newsummary)           # has not set()


    #------------------------------------------------------------------------------------
    # Footer option: overview text display
    #------------------------------------------------------------------------------------

    def onFooterFlip(self, footervar):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => Footer toggle checked on or off: open/close text display

        this seems useful, but could require click to see extra text in dialog;
        as is, mouse-only, and not much more useful than clicked edit/view dialog;
        update: single press on tablet activates a mouse hover-in event too--keep;

        caveat: scrollbar may be difficult to reach without entering another event,
        but this is really just a convenience and a redundant display anyhow;
        caveat: this may not appear if you have limited screen space and/or many
        events in a month's days: use te daynum selection list or event clicks;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got FooterFlip:', footervar.get())
        if footervar.get():
            # toggle on: draw footer
            footerframe = Frame(self.root, relief=RIDGE, border=2)
            footertext  = ScrolledText(footerframe)

            if Configs.footerheight:
                footertext.config(height=Configs.footerheight)
            trybgconfig(footertext, Configs.footercolor)
            tryfontconfig(footertext, Configs.footerfont)

            # appears above navigation buttons (former bottom) and below days grid (top)
            if Configs.footerresize:
                footerframe.pack(side=BOTTOM, expand=YES, fill=BOTH)    # grow proportionally
                footertext.pack(side=TOP, expand=YES, fill=BOTH)
            else:
                footerframe.pack(side=BOTTOM, fill=X)                   # retain fixed size
                footertext.pack(side=TOP, expand=YES, fill=BOTH)

            self.footerframe = footerframe           # save for erase on toggle
            self.footertext  = footertext            # save for fills on enter
            self.footertext.config(state=DISABLED)   # else editable till filled [1.2]
        else:
            # toggle off: erase footer
            self.footerframe.destroy()       # or .pack()/pack_forget() to show/hide
            self.footertext = None           # but won't happen often enough to optimize


    def onEnter_Event__Footer(self, edate, icsdata):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => mouse hover-in (or single-press) on event
        show overview in footer, if currently open
        
        discarded <Leave>=erase text: some may require later scrolling;
        discarded popup version: flashed if popup appeared over mouse;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got EventEnter')
        if self.footertext:
            displaytext = ("Date: %s\nSummary: %s\n%s" %
                (edate.as_string(),
                 icsdata.summary,
                 icsdata.description))
            displaytext = fixTkBMP(displaytext)          # [2.0] Unicode replacements
            self.footertext.config(state=NORMAL)         # allow deletes/inserts [1.2]
            self.footertext.delete('1.0', END)           # delete current text (if any)
            self.footertext.insert('1.0', displaytext)   # add text at line 1, col 0
            self.footertext.config(state=DISABLED)       # restore readonly state [1.2]


    def clearfooter(self):
        """
        on month navigations, erase current footer text if open (optionally)
        """
        if self.footertext and Configs.clearfooter:      # optional: default=None/False
            self.footertext.config(state=NORMAL)         # allow changes now [1.2]
            self.footertext.delete('1.0', END)           # delete current text (if any)
            self.footertext.config(state=DISABLED)       # restore readonly state [1.2]


    #------------------------------------------------------------------------------------
    # Images option: display image for a month window's month number
    #------------------------------------------------------------------------------------

    def onImageFlip(self, imagevar):
        """
        => Images toggle checked on/off: build and display, or erase
        [2.0] parent=window for Mac slide-down, focus_force for Mac refocus
        """
        trace('Got ImageFlip:', imagevar.get())
        if imagevar.get():
            # toggle on: popup and show

            # [1.6] the PIL/Pillow requirement is no longer absolute
            """
            try:
                import PIL
            except ImportError:
                # don't fail here, or on later navigates or toggles
                imagevar.set(False)
                showerror('%s: Images not available' % PROGRAM,
                          'Please install Pillow to use the Images option.')
                return  # avoid nesting
            """

            if not self.imgfiles:
                # get image names at window's first toggle-on [1.5]
                imgdir = Configs.imgpath
                try:
                    imgs = os.listdir(imgdir)
                except:
                    imagevar.set(False)
                    showerror('%s: Images Error' % PROGRAM,
                              'Image files path is invalid:\n%s\n\n'
                              'Check your "imgpath" setting in frigcal_configs.py.' 
                              % fixTkBMP(imgdir),
                              parent=self.root)
                    self.root.focus_force()
                    return  # avoid nesting
                              
                # [1.4] skip non-files (subdirs)  
                imgs = [img for img in imgs
                            if os.path.isfile(os.path.join(imgdir, img))]

                # [1.5] skip non-image files by filename mimetype
                for img in imgs.copy():                         # yes, must .copy()!
                    filetype = mimetypes.guess_type(img)[0]
                    if filetype == None or filetype.split('/')[0] != 'image':
                        imgs.remove(img)
                
                # [1.5] issue warning if 12 images not present
                if len(imgs) != 12:
                    # console always, popup just once per window (not on each navigate)
                    # showImage indexing may eventually print console exception traceback
                    showwarning('%s: Images Error' % PROGRAM,
                                'Image files missing or extraneous.\n\n'
                                'There are not 12 images in folder:\n%s\n\n'
                                'Some months may fail to display.' 
                                % fixTkBMP(Configs.imgpath),
                                parent=self.root)
                    # no self.root.focus_force() here: obscures image popup
                self.imgfiles = imgs
                
            imgwin = Toplevel()                                 # make new window (post popup?)
            imgwin.protocol('WM_DELETE_WINDOW', lambda: None)   # quit = no-op: tied to month
            imglab = Label(imgwin)
            imglab.pack()
            self.imgwin, self.imglab = imgwin, imglab           # save for showImage(), hide, quit
            self.showImage()                                    # show first image now

            # replace red tk window icon [1.2]
            try_set_window_icon(imgwin)

            # make window non-user-resizable, as image never resized [1.4]
            imgwin.resizable(width=False, height=False)                

            # start position for all image windows [1.4]
            if Configs.initimgposition: 
                imgwin.geometry(Configs.initimgposition)        # '+X+Y' offset from top left

        else:
            # toggle off: destroy popup
            self.imgwin.destroy()
            self.imgwin = self.imglab = self.imgobj = None


    def showImage(self, prototype=PROTO):
        """
        on month navigations, and when toggled on: show photo for viewed month;
        the window sizes itself to the image's size (but never vice versa);
        """
        if self.imgwin:
            if len(self.imgfiles) != 12:
                trace('There are not 12 images in ' + Configs.imgpath)

            if prototype:
                import random
                imgfile = random.choice(self.imgfiles)
            else:
                monthnum = self.viewdate.month()               # pick by name sort order
                imgfile = sorted(self.imgfiles)[monthnum-1]    # 1..N => 0..N-1

            imgpath = os.path.join(Configs.imgpath, imgfile)

            # [1.6] use PhotoImage from PIL/Pillow if installed for all image types and Pys;
            # else use Tk/tkinter version for PNG on some Py3.4+, and GIF/PPM/PPG on all Py3.X;

            imageloaded = imagedefault = False
            try:
                imgobj = PhotoImage(file=imgpath)                  # Pillow or native version
                imageloaded = True
            except:
                try:
                    imgpath = os.path.join('icons', 'montherr.gif') 
                    imgobj = PhotoImage(file=imgpath)              # works on all pys, pillow or not
                    imagedefault = True
                except:                                            # cwd should work, but universal?
                    pass

            if imageloaded or imagedefault: 
                self.imglab.config(image=imgobj)                   # draw photo
                self.imgobj = imgobj                               # must keep a reference
                trace(imgpath, imgobj.width(), imgobj.height())    # size in pixels
                self.imgwin.title('%s %.1f - %s' % (PROGRAM, VERSION, imgfile))
                # TBD: self.root.lift()  # don't hide main month window? (lift=tkraise)

            if not imageloaded:
                # after img window configured, else popup + empty img window ([1.7] typo fix)
                msgtext = 'Image file failed to load in Python %s.\nImage: %s'
                msgtext %= (Configs.pyversion, imgpath)
                trace(msgtext)
                showerror('%s: Image not available' % PROGRAM, msgtext +
                          '\n\nPlease install Pillow to use the Images option with this image,'
                          ' or use an image type that is supported in your Python version.'
                          '\n\nAs of frigcal 1.6, PNG images work in all Pythons using Tk 8.6+'
                          ' (including standard Windows installs of Python 3.4+), and GIF/PPM/PPG'
                          ' work in all Python 3.X; all other combinations require a Pillow install.'
                          '\n\nToggle-off Images to avoid seeing this error message again.',
                          parent=self.root)
                self.root.focus_force()   # obscures image popup iff first month bad: allow
  

    #------------------------------------------------------------------------------------
    # Clone option: multiple month view windows, moved in tandem or not
    #------------------------------------------------------------------------------------

    def onClone(self):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => Clone button pressed in any open window
        make a new, independent month view window, with custom quit action;
        
        this essentially _requires_ classes with their own state (not globals);
        open this at the same date as cloner, with custom type text in title bar;
        [1.2] the popup windows get an icon via the normal month window code;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        MonthWindowClone(Toplevel(), startdate=self.viewdate, windowtype='Popup')


    def onTandemFlip(self, tandemvar):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => Tandem toggle clicked on/off in any open window     
        if checked on, main+clone windows all move on any prev/next navigation;
        toggle setting in any is propagated to all windows' GUI and navigations;

        TBD: possible alternative: use a single, global, shared tkiner IntVar,
        both here and when making a new window in make_widgets();
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got TandemFlip:', tandemvar.get())
        tandemtoggle = tandemvar.get()
        for window in OpenMonthWindows:
            window.tandemvar.set(tandemtoggle)
        

#====================================================================================
# Popup clone window: multiple month windows may be opened (and navigate separately)
#====================================================================================

class MonthWindowClone(MonthWindow):
    """
    same as its super, but just close this window on quit button;
    no need to save/backup here: main (and other?) view still open,
    and all month windows are just portals on the same calendar data;
    """
    def onQuit(self):
        """
        => popup clone window's quit button press
        silently close this month view window with no backup/save
        """
        OpenMonthWindows.remove(self)
        self.root.destroy()                      # popup's main window (only)
        if self.imgwin: self.imgwin.destroy()    # and my image window popup?

               
#====================================================================================
# Date set/increment/decrement, with rollovers, calendar module days list
#====================================================================================

class ViewDateManager:
    """
    manage the viewed day's date object and month daynumbers list;
    
    created for and embedded in each MonthWindow object;
    maps relative day indexes in GUI to/from true month day numbers;
    caveat: uses datetime module dates, not later icsfiletools.Edate;
    
    subtle: must set day to 1 on mo/yr navigations, else current date's
    day may be out range for new month when mo/yr reset by date.replace()
    (e.g, 30, for Feb);  restores prev view day later if in new month,
    else sets it to the highest day number in the new month; 
    """
    def __init___(self):
        self.currdate = None    # displayed date's Date object: with .month/.year/.day #s
        self.currdays = None    # list of displayed month's day #s: 0 if not part of month

    def relday_is_in_month(self, reldaynum):
        return self.currdays[reldaynum] != 0      # display widget index is a true day?
    def trueday_is_in_month(self, truedaynum):
        return truedaynum != 0                    # when already pulled from currdays

    def index_to_day(self, reldaynum):
        return self.currdays[reldaynum]           # true day for display label index            
    def day_to_index(self, truedaynum):
        return self.currdays.index(truedaynum)    # display label index for true day

    def month(self):
        return self.currdate.month
    def day(self):
        return self.currdate.day
    def year(self):
        return self.currdate.year
    def mdy(self):
        return (self.month(), self.day(), self.year())

    def setday(self, daynum):
        # on clicks
        self.currdate = self.currdate.replace(day=daynum)


    def get_pad_daynums(self):
        """
        fetch day numbers list from python's calendar module for currdate;
        non-month days are zero, pad with extra zeroes for maxweeks displayed;
        calhelper 6=starts on Sunday (0=Monday, but can't change GUI as is);
        """
        calhelper = calendar.Calendar(firstweekday=6)   # start on Sunday
        currdays = list(calhelper.itermonthdays(self.currdate.year, self.currdate.month))
        currdays += [0] * ((MAXWEEKS * 7) - len(currdays))
        return currdays


    def settoday(self):
        # run initially and on demand
        self.currdate = datetime.date.today()
        self.currdays = self.get_pad_daynums()

    def setdate(self, datestr):
        # TBD: could check if day is in month's range explicitly; as is,
        # .replace() generates exception + general error popup on bad day;
        trace(datestr)
        try:
            mm, dd, yyyy = datestr.split('/')       # k.i.s.s. for now
            assert len(yyyy) == 4
            self.currdate = self.currdate.replace(
                                month=int(mm), day=int(dd), year=int(yyyy))
            self.currdays = self.get_pad_daynums()
            return True
        except:
            trace(sys.exc_info())
            return False


    def nav_neutral_day(self):
        # set day=1 to avoid out-of-range on replace()
        prevday = self.currdate.day                   # save daynum to reset if possible
        self.currdate = self.currdate.replace(day=1)  # else may be out of new month's range
        return prevday

    def nav_restore_day(self, prevday):
        # restore prev day if in bounds for new month
        if prevday in self.currdays:
            self.currdate = self.currdate.replace(day=prevday)  # restore if in new month
        else:
            # set day to last (i.e., highest #) day in new month
            # TBD: or leave at 1? (later navs on prior lastday)
            for lastday in reversed(self.currdays):
                if lastday != 0:
                    self.currdate = self.currdate.replace(day=lastday)
                    break

    def setnextmonth(self):
        prevday = self.nav_neutral_day()
        currdate = self.currdate
        if currdate.month != 12:
            currdate = currdate.replace(month=currdate.month + 1)
        else:
            currdate = currdate.replace(month=1, year=currdate.year + 1)
        self.currdate = currdate
        self.currdays = self.get_pad_daynums()
        self.nav_restore_day(prevday)

    def setprevmonth(self):
        prevday = self.nav_neutral_day()
        currdate = self.currdate
        if currdate.month != 1:
            currdate = currdate.replace(month=currdate.month - 1)
        else:
            currdate = currdate.replace(month=12, year=currdate.year - 1)
        self.currdate = currdate
        self.currdays = self.get_pad_daynums()
        self.nav_restore_day(prevday)

    def setnextyear(self):
        prevday = self.nav_neutral_day()
        self.currdate = self.currdate.replace(year=self.currdate.year + 1)
        self.currdays = self.get_pad_daynums()
        self.nav_restore_day(prevday)

    def setprevyear(self):
        prevday = self.nav_neutral_day()
        self.currdate = self.currdate.replace(year=self.currdate.year - 1)
        self.currdays = self.get_pad_daynums()
        self.nav_restore_day(prevday)


#====================================================================================
# Events edits/adds dialog: in-memory updates, saved on exit
#====================================================================================

class Dialog:
    """
    common super to avoid repeating wait state code [1.4]
    """
    modal = True       # redefine in sub or self as needed
    dialogwin = None   # set me in self to dialog window object 
    root = None        # set me to month window parent (Tk or Toplevel)

    def try_grab_set(self):
        """
        workaround for grab_set modal dialog oddness on Linux only (not on Win/Mac);
        without the wait_visibility() the grab_set() fails; without the grab_set(),
        the window isn't modal;  suggested on the web: an infinite loop with a 'try'
        to catch grab_set() failures until it works -- wait_visibiity() seems better;
        
        TBD: transient() may keep the dialog above parent? (Linux modals still odd);
        [1.6] YES: without this, Linux custom modal dialog windows can be covered,
        which is bad for small dialogs like right-click popup: disabled month on top!
        not required on Windows: does right thing for modals (this is WM dependent);
        
        [2.0] same issue and fix for Mac OS X (a.k.a. darwin), and the fix here also
        solves the issue of edit dialogs posting with their right portions off-screen;
        """
        if RunningOnLinux or RunningOnMac:
            # linux and mac - no issue on Windows
            self.dialogwin.wait_visibility()       # must wait till open, else exc
            self.dialogwin.transient(self.root)    # make modals stay on top [1.6] [2.0]
        self.dialogwin.grab_set()                  # now catch all app events

    def run(self):
        """
        go modal and wait for user action
        """
        if self.modal:                          # always modal (blocking) so far
            self.dialogwin.focus_set()          # take over input focus,
            self.try_grab_set()                 # disable other windows while this is open,
            self.dialogwin.wait_window()        # and wait here until window closed/destroyed


class EventDialog(Dialog):
    """
    custom dialog for event display and/or edit;
    created and run in MonthWindow callback handlers above;
    this is an abstract superclass: its Add/Edit subclasses
    fill in differing category builder and action buttons/callbacks;
    """    
    def __init__(self, root, edate, titletype, modal=True):
        """
        subclasses fill in their differing bits with icsdata=EventData() first
        """
        self.root  = root      # my creator's window (not mine), for Dialog [1.6]
        self.edate = edate     # dialog's event's date
        self.modal = modal     # true=blocking: not currently used 
        
        # make a new window
        self.dialogwin = Toplevel(root)
        self.dialogwin.title('%s %.1f - %s Event' % (PROGRAM, VERSION, titletype))

        # replace red tk window icon [1.2]
        try_set_window_icon(self.dialogwin)

        # [1.4] route window quit/close to changes checker (formerly closed silently)
        self.dialogwin.protocol('WM_DELETE_WINDOW', self.onCancel)   # or (lambda: None)

        # [2.0] on Mac OS X, dialog appears with part off-screen - adjust post location
        if RunningOnMac:
            pass
            # no, but making the dialog transient above (as on Linux) fixed this issue
            # self.dialogwin.geometry('+%d+%d' % (scrwide / 5, scrhigh / 2))  

        self.make_widgets(edate)
        self.run()   # wait for user action [1.4]

    def onCancel(self):
        """
        => on Cancel and window close "X"
        [1.4] verify event edit Cancel/close if any input field changed
        [2.0] parent=window for Mac slide-down, focus_force for Mac refocus
        """
        if ((self.start_common_inputs == self.fetch_from_widgets() and
             self.start_custom_inputs == self.fetch_from_customs())
           or
             askyesno('Verify %s edits cancel' % PROGRAM,
                      'Inputs have changed: cancel edits anyhow?',
                      parent=self.dialogwin)
           ):
            self.dialogwin.destroy()       # no changes or verified: close window
        else:
            self.dialogwin.focus_force()   # restore active style+focus on Mac
        

    def make_widgets(self, edate):
        """
        make custom dialog for event display and/or edit
        """
        dialogwin = self.dialogwin
        icsdata = self.icsdata

        # buttons to run context-specific action and close dialog window
        # pack first = clip last! (retain on resizes)
        toolbar = Frame(dialogwin, relief=RIDGE)
        toolbar.pack(side=BOTTOM, fill=X)
        trybgconfig(toolbar, Configs.eventdialogbg)

        # differs in subclasses
        self.make_action_buttons(toolbar)
        # all contexts: close window only
        cancelbtn = Button(toolbar, text='Cancel', command=self.onCancel)  # [1.4]
        cancelbtn.pack(side=RIGHT)
        tryfontconfig(cancelbtn, Configs.controlsfont)

        # main portion of window
        formfrm = Frame(dialogwin, relief=RIDGE, border=2)
        formfrm.pack(side=TOP, expand=YES, fill=BOTH)
        trybgconfig(formfrm, Configs.eventdialogbg)

        # date known, never editable (cut/paste to move to another date)
        clickdatestr = edate.as_string()  
        self.formlabel(formfrm, 'Date:', 0, 0)                  
        datefld = Label(formfrm, text=clickdatestr, relief=RIDGE)
        datefld.grid(row=0, column=1, sticky=W)                    # left side
        trybgconfig(datefld,   Configs.eventdialogfg)              # yes, bg=fg (2 colors)
        tryfontconfig(datefld, Configs.eventdialogfont)

        # differs in subclasses
        self.formlabel(formfrm, 'Calendar:', 1, 0)
        self.make_calendar_field(formfrm)

        self.formlabel(formfrm, 'Summary:', 2, 0)
        summaryfld = Entry(formfrm)
        summaryfld.grid(row=2, column=1, sticky=EW)
        summaryfld.insert(0, fixTkBMP(icsdata.summary))            # [2.0] Unicode replace 
        trybgconfig(summaryfld,   Configs.eventdialogfg)
        tryfontconfig(summaryfld, Configs.eventdialogfont)
        self.summaryfld = summaryfld

        self.formlabel(formfrm, 'Description:', 3, 0)    
        descriptionfld = ScrolledText(formfrm)
        descriptionfld.config(height=5)                            # default initial height
        descriptionfld.grid(row=3, column=1, sticky=NSEW)          # but grows with window

        # [2.0] omit blank line if it's empty (\n added on fetch)
        if icsdata.description != '\n':
            descdisplay = fixTkBMP(icsdata.description)            # [2.0] Unicode replace 
            descriptionfld.insert(0.0, descdisplay)

        trybgconfig(descriptionfld,   Configs.eventdialogfg)
        tryfontconfig(descriptionfld, Configs.eventdialogfont)

        # [2.0] text initial height/width now configurable
        if Configs.eventdialogtextheight != None:
            descriptionfld.config(height=Configs.eventdialogtextheight)   # else 5 above (Tk=24)
        if Configs.eventdialogtextwidth != None:
            descriptionfld.config(width=Configs.eventdialogtextwidth)     # else Tk default=80
        self.descriptionfld = descriptionfld

        # category = pulldown of configs, plus entry for (possibly new) values
        # TBD: might be able to crosslink the two on a shared StringVar?
        # as is, setting optionmenu simply sets entry's text, and not vice versa
        self.formlabel(formfrm, 'Category:', 4, 0)
        categoryfrm = Frame(formfrm)
        categoryfrm.grid(row=4, column=1, sticky=W)
       
        categoryfld = Entry(categoryfrm)
        categoryfld.pack(side=LEFT)                              
        categoryfld.insert(0, fixTkBMP(icsdata.category))          # initialize to curr val, if any
        trybgconfig(categoryfld,   Configs.eventdialogfg)          # [2.0] Unicode replacement 
        tryfontconfig(categoryfld, Configs.eventdialogfont)
        self.categoryfld = categoryfld

        # str.lower for ordering, but doesn't change keys
        categories1 = sorted(Configs.category_colors.keys(), key=str.lower) or ['']
        categories2 = [fixTkBMP(x) for x in categories1]           # [2.0] Unicode replacement

        # [2.0] map back to the original later for use as a configs dict key
        # caveat: though unlikely, 'ccXcc' and 'ccYcc' may be the same fixed (punt!)
        self.categoryfixmap = dict(zip(categories2, categories1))
        categories = categories2

        def pickhandler(pick):
            categoryfld.delete(0, END)
            categoryfld.insert(0, pick)    # no need for categoryvar.get() here

        categoryvar = StringVar()          # required for init value only here 
        categorymnu = OptionMenu(categoryfrm, categoryvar, *categories, command=pickhandler)
        categorymnu.pack(side=LEFT)
        trybgconfig(categorymnu,   Configs.eventdialogfg)
        tryfontconfig(categorymnu, Configs.eventdialogfont)
        categoryvar.set('Choose...')                         # initialize to usage reminder
        
        # resizing precedence: description text highest
        formfrm.rowconfigure(3, weight=1)    
        formfrm.columnconfigure(1, weight=1)

        # [1.4] save common initial inputs dict to detect changes on Cancel
        self.start_common_inputs = self.fetch_from_widgets()
        self.start_custom_inputs = self.fetch_from_customs()
         
    def formlabel(self, frame, text, row, column, sticky=NSEW):
        label = Label(frame, text=text, relief=RIDGE)       # standardize look
        label.grid(row=row, column=column, sticky=sticky) 
        
    def fetch_from_widgets(self):
        """
        [1.4] strip extra trailing \n added to description by Text widget's
        get(), else can wind up adding one '\n' per an event's update or paste;
        could also fetch through END+'-1c', but drop any already present too;
        nit: rstrip() also drops any intended but useless blank lines at end;
        always keep one \n at end in case some ics parsers require non-blank;
        [2.0] but don't display a sole '\n' = bogus blank line (see above);
        [2.0] and map category back to non-BMP-fixed value, if in table;
        """
        # category may be empty or typed, and may be new value not in menu
        categoryfld = self.categoryfld.get()                   # get GUI field value
        if categoryfld in self.categoryfixmap:                 # [2.0] map to original
            categoryfld = self.categoryfixmap[categoryfld]     # a no-op if unfixed

        return dict(summary=     self.summaryfld.get(),
                    description= self.descriptionfld.get('1.0', END).rstrip('\n') + '\n',
                    category=    categoryfld)
        
    # subclass protocol, plus any action handlers
    def fetch_from_customs(self):             return None  # [1.4]
    def make_calendar_field(self, formframe): raise NotImplementedError
    def make_action_buttons(self, toolbar):   raise NotImplementedError


#====================================================================================
# factored event dialog subclass
#====================================================================================

class AddEventDialog(EventDialog):
    """
    dialog used to add a new event, and paste a copied event to day;
    factored differing parts to subclasses to avoid false uniformity;
    [1.3] titletype now passed as Create _or_ Paste, to differentiate;
    """
    def __init__(self, root, edate, titletype='Create', icsdata=None, initcalendar=None):
        # edate is clicked day's true date, not relative index
        # icsdata and initcalendar are not None when used for paste
        self.icsdata = icsdata or EventData(summary='Enter...')   # all else blank
        self.initcalendar = initcalendar
        EventDialog.__init__(self, root, edate, titletype)

    def make_calendar_field(self, formframe):
        # calendar unknown (Create) or changeable (Paste):
        # editable pulldown options-list of all calendars
        icsfiles1 = sorted(CalendarsTable.keys())      # iterable does *, but need list for [0]
        icsfiles2 = [fixTkBMP(x) for x in icsfiles1]   # [2.0] Unicode replacements for display 

        # [2.0] map back to the original later for use as a calendars table key 
        # caveat: though unlikely, 'ccXcc' and 'ccYcc' may be the same fixed (punt!)
        self.icsfilesfixmap = dict(zip(icsfiles2, icsfiles1))
        icsfiles = icsfiles2

        calendarvar = StringVar()
        calendarmnu = OptionMenu(formframe, calendarvar, *icsfiles)
        calendarmnu.grid(row=1, column=1, sticky=W)
        trybgconfig(calendarmnu,   Configs.eventdialogfg)
        tryfontconfig(calendarmnu, Configs.eventdialogfont)
        self.calendarvar = calendarvar              # save for Create callback
        
        # [1.5] for new adds, init to default calendar, if present:
        # use paste's, else frigcal-default, else 1st by sort order
        dfltcal = [name for name in icsfiles if name.startswith('frigcal-default-calendar')]
        calendarvar.set(self.initcalendar or (dfltcal and dfltcal[0]) or icsfiles[0])

    def make_action_buttons(self, toolbar):
        createbtn = Button(toolbar, text='Create', command=self.onAddEvent)
        createbtn.pack(side=LEFT, expand=NO)
        tryfontconfig(createbtn, Configs.controlsfont)

    def fetch_from_customs(self):
        # [1.4] verify Cancel if any inputs changed
        # there is no entry field here, so value must be in list
        return self.icsfilesfixmap[self.calendarvar.get()]   # [2.0] map to original
    
    def onAddEvent(self):
        # add new event in both gui and data structures
        # widgetdata.{.vevent, .orderby} set in add_event_data
        # each Paste creates a new event with same text data
        edate = self.edate
        newuid = icsfiletools.icalendar_unique_id()
        icsfilename = self.icsfilesfixmap[self.calendarvar.get()]   # [2.0] map to original
        widgetdata = EventData(uid=newuid,
                               calendar=icsfilename,
                               **self.fetch_from_widgets())
        trace('Adding:', widgetdata.summary)
        icsfiletools.add_event_data(edate, widgetdata)      # data structures
        self.add_event_gui(edate, widgetdata)               # then GUI: >=1 windows
        self.dialogwin.destroy()                            # and close dialog

    def add_event_gui(self, edate, widgetdata):
        """
        add new Entry to display; not static: Paste posts full dialog;
        add_event_entry both adds widget and registers event handlers;
        "ow" is a MonthWindow: non-static methods don't require calling
        through the class name, but doing so makes external more explicit;
        
        TBD: reorder now?--don't care about .orderby here (new events
        are added to end of day's list), but .calendar ordering is not
        applied until next navigation/refill, and can skew select lists;
        [1.4] this could do just ow.fill_events(), but may flash the GUI;
        """
        for ow in OpenMonthWindows:
            if ow.viewdate.month() == edate.month and ow.viewdate.year() == edate.year:
                reldaynum = ow.viewdate.day_to_index(edate.day)
                (dayframe, daynumlabel) = ow.daywidgets[reldaynum]
                MonthWindow.add_event_entry(ow, dayframe, edate, widgetdata)   # or ow.add...


#====================================================================================
# factored event dialog subclass
#====================================================================================

class EditEventDialog(EventDialog):
    """
    dialog used to view, update, and delete an existing displayed event;
    factored differing parts to subclasses to avoid false uniformity;
    """
    titletype = 'View/Edit'  # [1.3] not View/Update/Delete'
    
    def __init__(self, root, edate, icsfilename, icsdata):
        # edate is clicked event's true date
        # icsdata is clicked event's EventData
        self.icsfilename = icsfilename
        self.icsdata = icsdata
        EventDialog.__init__(self, root, edate, self.titletype)

    def make_calendar_field(self, formframe):
        # calendar known: not editable
        # must use cut/paste to move to another calendar
        icsfilename = fixTkBMP(self.icsfilename)                        # [2.0] Unicode fix
        calendarfld = Label(formframe, text=icsfilename, relief=RIDGE)
        calendarfld.grid(row=1, column=1, sticky=W)
        trybgconfig(calendarfld,   Configs.eventdialogfg)
        tryfontconfig(calendarfld, Configs.eventdialogfont)
 
    def make_action_buttons(self, toolbar):
        updatebtn = Button(toolbar, text='Update', command=self.onUpdateEvent)
        deletebtn = Button(toolbar, text='Delete', command=self.onDeleteEvent)
        updatebtn.pack(side=LEFT, expand=NO)
        deletebtn.pack(side=LEFT, expand=YES)
        tryfontconfig(updatebtn, Configs.controlsfont)
        tryfontconfig(deletebtn, Configs.controlsfont)
        
    def onUpdateEvent(self):
        # update event in both gui and data structures
        edate = self.edate
        icsdata = self.icsdata
        icsfilename = self.icsfilename
        widgetdata = EventData(calendar=icsfilename,
                               **self.fetch_from_widgets())
        icsfiletools.update_event_data(edate, icsdata, widgetdata)   # data structures
        self.update_event_gui(icsdata, widgetdata)                   # then GUI: >= 1 window
        self.dialogwin.destroy()                                     # and close dialog

    def update_event_gui(self, icsdata, widgetdata):
        """
        update displayed summary text on month display(s)
        not static, as used only by the dialog itself;
        caveat: does not update any footer text (but should it?)
        """
        for ow in OpenMonthWindows:
            if icsdata.uid in ow.eventwidgets.keys():     # no need to match viewdate
                # change summary text only
                entry = ow.eventwidgets[icsdata.uid]
                entry.delete(0, END)                      # not .config(text=x): for labels 
                entry.insert(0, widgetdata.summary)       # [2.0] already applied fixTkBMP

                # change color too if category changed (calendar not changeable)
                category = widgetdata.category            # ~white if new category unknown
                calendar = icsdata.calendar               # unless calendar is colored
                MonthWindow.colorize_event(entry, category, calendar)  # avoid redundant code!

    def onDeleteEvent(self):
        """
        delete event in both gui and data structures;
        TBD: verify this via popup too, like Cancel in 1.4?
        but doesn't discard inputs or update calendar files; 
        """
        edate = self.edate
        icsdata = self.icsdata
        icsfilename = self.icsfilename
        icsfiletools.delete_event_data(edate, icsdata)    # data structures
        self.delete_event_gui(icsdata)                    # then GUI: >=1 windows
        self.dialogwin.destroy()                          # and close dialog

    @staticmethod
    def delete_event_gui(icsdata):
        """
        delete summary text from month display(s)
        static so also callable from Cut operation without this edit dialog;
        staticmethod is optional in 3.X if class calls only, but makes explicit;
        """
        for ow in OpenMonthWindows:
            if icsdata.uid in ow.eventwidgets.keys():     # no need to match viewdate
                entry = ow.eventwidgets[icsdata.uid]      # erase this entry from gui+table             
                entry.destroy()
                del ow.eventwidgets[icsdata.uid]


#====================================================================================
# Cut/Copy/Open event right-click dialog
#====================================================================================

class CutCopyDialog(Dialog):
    """
    post modal cut/copy/open dialog on event right-click;
    events cut/copied here are global, for later pastes;
    [1.4] split out from click handler to this class;
    """
    def __init__(self, monthwindow, tkevent, edate, icsdata):
        self.root = monthwindow.root         # creator's window, for Dialog [1.6] 
        self.make_widgets(monthwindow, tkevent, edate, icsdata)
        self.run()                           # wait for user action [1.4]
    
    def make_widgets(self, monthwindow, tkevent, edate, icsdata):

        # the following use names in enclosing function scope
        def onCancel():
            # ANDROID - see global def
            global EventDialogIsOpen
            EventDialogIsOpen = False    # enable Open dialog now
            popup.destroy()
            
        def onCopy():
            global CopiedEvent
            CopiedEvent = icsdata
            popup.destroy()

        def onCut():
            global CopiedEvent
            CopiedEvent = icsdata
            icsfiletools.delete_event_data(edate, icsdata)    # delete from data structures
            EditEventDialog.delete_event_gui(icsdata)         # then delete from GUI: >=1 windows
            popup.destroy()

        popup = Toplevel()                              # new dialog window, default Tk root
        mbutton = Menubutton(popup, text='Action')      # a stand-alone pull-down
        picks = Menu(mbutton, tearoff=False)            # 'open' is just a redundant convenience
        mbutton.config(menu=picks)                      # 'open' must cancel too: dialog may delete!
        picks.add_command(label='Copy', command=onCopy)
        picks.add_command(label='Cut',  command=onCut)

        picks.add_separator()
        picks.add_command(label='Open',       # cancel this AND open view/edit dialog
                          command=lambda: (
                              onCancel(),
                              monthwindow.onLeftClick_Event__Edit(edate, icsdata)))

        picks.add_separator()
        picks.add_command(label='Cancel', command=onCancel)
        mbutton.pack(side=TOP)
        mbutton.config(bg='white', bd=4, relief=RAISED) 

        # [1.3] add summary text to give some event context
        msgtext = 'For "%s"' % fixTkBMP(icsdata.summary)               # [2.0] Unicode replace
        msg = Label(popup, text=msgtext, bg='white')
        msg.pack(side=BOTTOM)
        trybgconfig(msg, Configs.eventdialogbg)  # same as rest of dialog
        tryfontconfig(msg, Configs.daysfont)     # same as month window

        # [2.0] stretch window horizontally via min label size
        msg.config(width=max(40, len(msgtext)))
        
        # config window
        popup.title('%s %.1f - Event Actions' % (PROGRAM, VERSION))
        popup.geometry('+%d+%d' % (tkevent.x_root, tkevent.y_root))    # post popup at click spot
        trybgconfig(popup, Configs.eventdialogbg)

        # replace red tk window icon [1.2]
        try_set_window_icon(popup)
        self.dialogwin = popup   # [1.4] for run()


#====================================================================================
# Day's event selection list daynum left-click dialog [1.3]
#====================================================================================

class SelectListDialog(Dialog):
    """
    post modal select dialog on daynum left-click:
    listbox of all day's events + 'create' button;
    [1.4] split out from click handler to this class;
    """
    def __init__(self, monthwindow, clickdate):
        self.root = monthwindow.root         # creator's window, for Dialog [1.6]
        self.make_widgets(monthwindow, clickdate)
        self.run()                           # wait for user action [1.4]

    def make_widgets(self, monthwindow, clickdate):
        dialog = Toplevel()  # new window
        
        # config window: open anywhere, replace red tk icon
        dialog.title('%s %.1f - Select Event' % (PROGRAM, VERSION))
        try_set_window_icon(dialog)
        trybgconfig(dialog, Configs.eventdialogbg)

        msgtext = 'Select or create new event for %s' % clickdate.as_string()
        msg = Label(dialog, text=msgtext, bg='white')
        msg.pack(side=TOP)
        trybgconfig(msg, Configs.eventdialogbg)   # same as rest of dialog

        # button for new event as alternative (pack first = clip last on shrink)
        toolbar = Frame(dialog)
        toolbar.pack(fill=X, side=BOTTOM)
        trybgconfig(toolbar, Configs.eventdialogbg)

        # Create = same as clicking rest of day frame (if any!)
        create = Button(toolbar, text='Create', 
            command=lambda: (                              # erase select AND open create dialogs
                    dialog.destroy(),
                    monthwindow.root.update(),
                    AddEventDialog(monthwindow.root, clickdate)))
        create.pack(side=LEFT)
        tryfontconfig(create, Configs.controlsfont)

        # cancel (and other destroyers) ends wait on window
        cancel = Button(toolbar, text='Cancel', command=lambda: dialog.destroy())
        cancel.pack(side=RIGHT)
        tryfontconfig(cancel, Configs.controlsfont)

        # get events for day, ordered
        dayeventsdict = EventsTable[clickdate]             # events on this date (uid table) 
        dayeventslist = list(dayeventsdict.values())       # day's event object (all calendars)
        dayeventslist.sort(                                # mimic month window ordering
                   key=lambda d: (d.calendar, d.orderby))  # order for gui by calendar + creation 

        # create selection/action lists ([2.0] label is not a key here)
        labels, leftactions, rightactions = [], [], []
        for icsdata in dayeventslist:                      # for all ordered events in this day
            displaysummary = fixTkBMP(icsdata.summary)     # [2.0] apply Unicode replacements 
            labels.append(displaysummary)                  # add summary+callback to select list

            # list left-single callbacks (double not used)             
            leftactions.append(                            # retains state from this scope
                lambda tkevent, icsdata=icsdata: (         # save loop's current icsdata object
                    dialog.destroy(),                      # erase select AND open edit dialogs
                    monthwindow.root.update(),
                    EditEventDialog(monthwindow.root, clickdate, icsdata.calendar, icsdata)))

            # list right-single callbacks (post dialog at former listbox spot)
            rightactions.append(
                lambda tkevent, icsdata=icsdata: (
                    dialog.destroy(),
                    monthwindow.root.update(),
                    monthwindow.onRightClick_Event__CutCopy(tkevent, clickdate, icsdata)))

        # reuse PP4E component, modified ([2.0] NOTE: this binds its own mouse buttons - Mac)
        select = ScrolledList(labels, leftactions, rightactions, parent=dialog, side=TOP)
        select.listbox.config(width=60)
        trybgconfig(select.listbox,   Configs.daysbg)      # mimic day frames color, font    
        tryfontconfig(select.listbox, Configs.daysfont)
        select.listbox.config(border=2, relief=RAISED)     # mimic day frames appearance
        select.config(border=5, bg='black')                # mimic month window appearance

        # colorize events in the listbox; items have color only 
        for (index, icsdata) in enumerate(dayeventslist):
            monthwindow.colorize_listitem(
                select.listbox, index, icsdata.category, icsdata.calendar)
        
        self.dialogwin = dialog   # [1.4] for run()


#====================================================================================
# Main logic
#====================================================================================

def main(prototype=PROTO):                         # prototype now fully deprecated
    try:
        icsfiletools.init_default_ics_file()       # if none on first run (or bad path)
        icsfiletools.parse_ics_files()             # makes CalendarsTable, EventsTable
    except:
        startuperror(                              # [1.5] GUI popup, not console only
            'Error while loading calendar.\n\n'
            'Check your "icspath" setting in frigcal_configs.py first.  '
            "Then check your calendar folder's permissions, and your "
            "calendar data's validity.\n\n"
            'Python exception text follows:\n\n%s\n%s'
            % (sys.exc_info()[0], sys.exc_info()[1]))
    else:
        # [2.0] make sentinel file in cwd to signal
        # launcher to close (if run), ignore errors
        try:
            open('.frigcal-is-active', 'w').close()
        except:
            pass
        
        # the normal bit
        root = Tk()
        main = MonthWindow(root)
        
        # [2.0] on Mac, customize app-wide automatic top-of-display menu
        fixAppleMenuBar(window=root,
                        appname=PROGRAM,
                        helpaction=lambda: webbrowser.open(HELPFILE),
                        aboutaction=None,
                        quitaction=main.onQuit)    # app-wide quit: save/ask

        if RunningOnMac:
            #--------------------------------------------------------------------
            # [2.0] required on Mac OS X (only), else the checkbuttons in the
            # main window are not displayed in Aqua (blue) active-window style
            # until users click another window and click this program's window;
            #
            # this is a bug in AS's Mac Tk 8.5 -- it's not present in other Tk 
            # ports, and IDLE search dialogs have the same issue;  for reasons 
            # TBD, it's enough to use just the lift() below for frigcal when 
            # it is run from a command line, but the full bit here is required 
            # when run by mac pylaucher on a click;  ditto for pymailgui, but 
            # mergeall requires all 3 steps in both contexts (it's special?...);
            # caveat: can still lose active style on iconify and common dialogs;
            #
            # UPDATE: focus is now restored after common dialog closes by a 
            # focus_force(), and on deiconifies (unhides) by catching Dock 
            # clicks and running the heinous hack copied from mergeall below;
            #--------------------------------------------------------------------
  
            # fix tk focus loss on startup
            root.withdraw()
            root.lift()
            root.after_idle(root.deiconify)

            # fix tk focus loss on deiconify
            def onReopen():
                #print(root.state())    # always normal
                root.lift()
                root.update()
                temp = Toplevel()
                temp.lower()
                temp.destroy()
            root.createcommand('::tk::mac::ReopenApplication', onReopen)

        root.mainloop()

        # [2.0] clean up sentinel file on exit,
        # else it's deleted on next launcher run
        try:
            os.remove('.frigcal-is-active')
        except:
            pass


if __name__ == '__main__':
    main()
