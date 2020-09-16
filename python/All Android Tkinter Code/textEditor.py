#!/usr/bin/env python3
"""
################################################################################
PyEdit: a Python/tkinter text-file editor program and component.

-Copyright and author: © M.Lutz, 2000-2019 (http://learning-python.com) 
-License: provided freely, but with no warranties of any kind
-Original version from the book Programming Python, 2nd-4th Editions (PP2E-PP4E)

#-------------------------------------------------------------------------------
# ANDROID version, Jan-Apr 2019 (search for "# ANDROID" to view all changes).
# These changes may be merged into the original code in a later release.
#
# Recent changes (search for [date] labels to see changes made):
#
# [Apr2119] Pydroid 3 3.0 broke webbrowser: use os.system(cmd) with a 
#           hardcoded Android activity-manager command line instead
#           (3.0's $DISPLAY breaks module, $BROWSER kills "file://").
#
# [Apr1919] Fix the Run-Code "Capture" workaround to the Pydroid 3 empty 
#           sys.executable bug, to accommodate the different Python path 
#           in Pydroid 3's 3.0.  The fix now reads a spawned 'which python' 
#           command to be path agnostic when hardcoding the Python path.
#           Also revert to using webbrowser for Help's user guide: it does 
#           work, but iff files use '"file://" and HTML docs use online URLs
#           (but Run-Code "Click" still uses os.system); see _openbrowser.py.
#
# [Apr1219] Reenable Help's "User Guide" button, and fix it to open with an
#           os.system() spawn of an activity-manager command instead of Py's
#           webbrowser; open online version of help, for its latest changes.
#           Also: shrink help dialog; work around its About/Versions truncated
#           text with custom scrolled-text dialogs using word wrap and sized 
#           for fit; and open default apps on Android for Run-Code's "Click".
#
# [Mar3119] An attempt to manually line-break some help-dialog text was
#           abandoned because it's impossible to get the fit right for both
#           orientations.  Pydroid 3 tkinter truncates instead of wrapping.
#
# [Mar2819] New user config for initial folder of Open/Save file-chooser dialog;
#           else, navigating to user content can be tedious in the Tk dialog.
#           Also trim some comments lines: Pydroid 3 can't handle larger files.
#
# [Feb2019] Clarify Android Tk font constraints in preset fonts pick list.
#-------------------------------------------------------------------------------

Uses the Tk text widget, plus GuiMaker menus and toolbar buttons, to implement
a full-featured text editor and code laucher that can be run as a standalone
program, and attached as a library component to other GUIs.  Also used by the
PyMailGUI and PyView programs to edit mail text and image-file notes, and by 
PyMailGUI and PyDemos in pop-up mode to display source and text files.

PROGRAM USE: 
  Run this main script (by click, command-line, IDLE Run option, etc.) to 
  start PyEdit, either with no arguments to open files in the GUI, or with one
  argument giving the pathname of a file to be opened and loaded initially:

      [[py]thon] textEditor.py [filename]

  Edit file textConfig.py to customize PyEdit appearance and behavior.  Some
  status messages are printed to the console, if PyEdit is started from one.
  You can also run this script in PyEdit's Run Code, once PyEdit is started.

LIBRARY USE:
  PyEdit can also be imported and used by other programs as GUI component
  or popup display; see its top-level classes near the end of this module. 

DISTRIBUTIONS:
  As of version 3.0, PyEdit is available both as this source, and as a frozen
  app or executable on Mac, Windows, and Linux.  The latter support opens by 
  associations, and require no Python install.  The source-code version is 
  also shipped as part of PyMailGUI 4.0.  See README.txt for more details.

TEXT POLICIES:
  PyEdit opens and saves files using a Unicode encoding that you may input
  or hardcode (see textConfig.py); reads files having any end-line format;
  and saves files using the hosting platform's end-line format (see utility
  fixeoln.py in tools/ if you need to change end-lines in a saved file).

# Android: ***ADDITIONAL DOCUMENTATION TRIMMED HERE***
# Because Pydroid 3's IDE editor cannot handle source files > roughly 256k 
# bytes (and lets the user's program die without warning!), some additional 
# comments were deleted here.  See this file's original version for text cut,
# and learning-python.com/mergeall-android-scripts/_README.html#toc85.

################################################################################
"""




#===============================================================================
# (Some) major [3.0] additions (also search for "[3.0]")
#===============================================================================


"""
--------------------------------------------------------------------------------
[3.0] General and initial Mac OS X porting notes:

PyEdit's menu items automatically show up in the top-of-screen menu bar on Mac
(as normal and expected).  Some dialog titles were tweaked here for the Mac.
Mac dialogs can also be slide-downs (via parent=win) but are not here, because
using popup windows in a multiwindow interface seems more flexible and natural.
UPDATE: parent=self is now used on Mac too, else root is lifted above subject.

Alt+<underline> menu keyboard shortcuts don't work on Mac - likely need to also
support "accelerator" options and bindings in GuiMaker.  As is, menus can be
navigated by keyboard on  Mac (ctrl+fn+F2, letter1, space, letter1), but it's
cumbersome; for now, added Undo and Redo to all toolbars for easier access.
UPDATE: menu accelerators _have_ been added, and tailored to the Mac's keys.

Mac menus remain always active and can reopen an already-open modal dialog,
which can cause havoc.  This seems paridigm skew, but duplicate modal actions
are disabled here via a decorator to avoid the issue altogether.  Mac menus also
don't have Tk tearoffs - between this and lack of Alt+* shortcuts, they seem
a bit less useful.  Mac menus also add some items "for free" that need to be
replaced (e.g., About), and have inheritance issues that may be Tk 8.5 specific.
--------------------------------------------------------------------------------
"""


# these are tedious to repeat
import sys
RunningOnMac     = sys.platform.startswith('darwin')
RunningOnWindows = sys.platform.startswith('win')           # or [:3] == 'win'
RunningOnLinux   = sys.platform.startswith('linux')


#===============================================================================


"""
[3.0] For frozen apps/exes, fix module+resource visibility.  This logic and 
its docs have now been moved off to file fixfrozenpaths.py.  Importing it
configures sys.path (but not CWD) in-place as needed for the freeze tool used, 
to grant importers access to these items.  It's a no-op for some source-code.

Also now provides a function for portably determining the install folder:
use this instead of __file__ directly, which may not work in PyInstaller 
executables (the function uses __file__ for source/app, else sys.argv[0]);.
Try the . import first: it's crucial that this gets its own version.
"""

try:
    from . import fixfrozenpaths    # get mine if I'm part of a package
except (ImportError, SystemError):
    import fixfrozenpaths           # used here only in PyEdit itself

# [3.0] data+scripts not in os.getcwd() if run from a cmdline elsewhere,
# and __file__ may not work if running as a frozen PyInstaller executable;
# use __file__ of this file for Mac apps, not module: it's in a zipfile;

INSTALLDIR = fixfrozenpaths.fetchMyInstallDir(__file__)   # absolute


#===============================================================================


def fixTkBMP(text):
    """
    [3.0] (copied from PyMailGUI) Tk <= 8.6 cannot display Unicode characters
    outside the U+0000..U+FFFF BMP (UCS-2) code-point range, and generates
    uncaught exceptions when tried (emojis kill programs!).  To address this,
    call this function to sanitize all text passed to the GUI for display.
    It replaces any non-BMP characters with the standard Unicode replacement
    character U+FFFD, which Tk displays as a highlighted question mark diamond.
    This workaround is coded to assume that Tk 8.7 will lift the BMP restriction,
    per a dev rumor.  It also assumes TkVersion has been imported from tkinter.

    There are related issues in tkinter file dialogs ("initialfile" has to be
    forced to None to avoid later errors if a filename with an emoji is chosen);
    prints to stdout (text must be forced to ascii() to avoid errors on some
    consoles); and the Mac's OpenDocument event in __main__ (either Tk, tkinter,
    or both munge filenames with emojis, requiring an odd encode+decode to open).
    """

    if TkVersion <= 8.6:
        text = ''.join((ch if ord(ch) <= 0xFFFF else '\uFFFD') for ch in text)
    return text


def isNonBMP(text):
    """
    [3.0] Return true if any character (codepoint) in text is outside Tk's BMP 
    display range.  Used by Open/Save dialogs to ignore prior saved choice for
    which this returns True , else tkinter fails in the dialog's show() calls.
    Also used by onOpen to issue a warning popup when characters are replaced.
    """

    if TkVersion <= 8.6:
        return any(ord(ch) > 0xFFFF for ch in text)
    else:
        return False   # and assume Tk 8.7 will make this better...


#===============================================================================


def try_set_window_icon(window, prog='pyedit', kind='-main'):
    """
    [3.0] For standalone windows, replace generic Tk or system icon with a
    custom icon - window icon on Windows, app bar icon on Linux, TBD on Mac
    (Mac requires app bundles to support most icon contexts; see py2app).
 
    Linux needs a gif, else requires Tk 8.6+ for pngs (or a Pillow install).
    When fetching icons from PyEdit's own folder, can get path via __file__,
    whether imported in package or run standalone, and without importing
    self; see PP4E/Gui/Tools/windows.py for more on local folder access.
    Update: see fixfrozenpaths.py for new policy: __file__  may not work.

    findicon() tries the current working dir first, then pyedit's own subdir.
    Hence, in embdedded mode, windows use a client app's icon if one exists,
    else pyedit's own; in standalone mode, windows use pyedit's own icon.
    
    'prog' and 'kind are used to build a filename for pyedit's own folder;
    'kind' can be used for a more-specific icon - popup windows use special
    'pyeditpopup.ico' when standalone to distinguish from main/quitting Tk(); 
    
    Caveat: could use PP4E.Gui.Tools.windows superclasses, but it's more
    complex to integrate with those classes' cannned APIs for quits, etc.
    Caveat: tkinter's askstring() and askinteger() don't pick up custom
    icons, but they can be patched to do so (at some peril) => see ahead.
    Caveat: tkinter's askcolor() displays no icon and cannot be patched,
    and ditto for its automatic save-as dialog's overwite warning popup.
    """
    
    def findicon(ext):
        pyeditdir = INSTALLDIR                  # not __file__ if PyInstaller exe
        iconscwd  = glob.glob('*.%s' % ext)
        namepatt  = '%s-window%s.%s' % (prog, kind, ext)
        iconhere  = os.path.join(pyeditdir, 'icons', namepatt)
        iconname  = iconscwd[0] if iconscwd else iconhere
        return iconname
    
    try:
        if RunningOnWindows:
            window.iconbitmap(findicon('ico'))            # Windows: all contexts

        elif RunningOnLinux:
            imgobj = PhotoImage(file=findicon('gif'))     # Linux: app bar, Tk 8.5+
            window.iconphoto(True, imgobj)                # use Gif for Tk 8.5-

        elif RunningOnMac or True:
            raise NotImplementedError                     # Mac (or other): neither

    except Exception as why:
        pass   # bad file or platform


#===============================================================================


"""
--------------------------------------------------------------------------------
tkinter dialog window-border patches

[3.0] The following extends two classes in the tkinter module to add custom
icons to the standard modal dialogs askstring() and askinteger().  Unlike
most common dialogs, these two always display the default Tk icon without the
code below (even if a parent is specified), and have no icon protocol support
themselves.  Caveat: these classes are semi-private ("_"), and open to future
changes that may break this code (really, hack, but there's no alternative).

Caveat: askcolor() displays no icon (even if a parent/master is passed in),
and seems unable to be patched to use a custom icon (there is no Toplevel to
use in an extended method).  This is less grievous than other ask*(): punt!

Caveat: the SaveAs dialog also posts a dialog without title or icon when the
user selects an existing file (an overwrite warning).  There seems no way to
improve this, as it's issued by Tk's common dialogs internally: also punt!
UPDATE: actually, for this the Mac app shows a slidedown with a small version 
of the PyEdit icon, along with the warning symbol imgage - this seems fine;
--------------------------------------------------------------------------------
"""

from tkinter.simpledialog import _QueryString, _QueryInteger


class PatchAskString(_QueryString):
    """
    A TopLevel (by inheritance), which interacts in its __init__.
    Extend its widget-builder method to set the window's custom
    icon per the hosting platform.  Note: this cannot extend the
    __init__ method, as that's where all user interaction occurs.
    Also note: this must return entry for initial focus to be set.
    """
    def body(self, master):                  
        entry = _QueryString.body(self, master)
        try_set_window_icon(self)
        return entry


class PatchAskInteger(_QueryInteger):
    """
    Ditto - see preceding class's docstring.
    """
    def body(self, master):
        entry = _QueryInteger.body(self, master)
        try_set_window_icon(self)
        return entry


def my_askstring(title, prompt, **kargs):
    return PatchAskString(title, prompt, **kargs).result


def my_askinteger(title, prompt, **kargs):
    return PatchAskInteger(title, prompt, **kargs).result


#===============================================================================


"""
--------------------------------------------------------------------------------
More tkinter dialog patches: pass parent arg (but allow for omission on Mac)

[3.0] Tk's common dialogs on Windows lift the root window above the subject
window when they differ, unless a parent=self argument is included.  On Mac,
this is not the case for simple dialogs like showinfo, but is for others.
This is also done for Open/Save dialogs, still coded as instance methods ahead.

On Mac, parent=self unfortunately(?) also invokes slide-down sheet style instead
of a popup window, and discards the dialog's window title, which may or may not
be preferred - hence the encapsulation here for possible future changes.
Caveat: these perhaps should be methods, but this grew from a simple fix.

Note that passing a "master=self" argument has no effect on root window lifts,
and askstring/askinteger still popup in a window (but now don't raise the root).
While we're at it, also add appname to title automatically here (not per call),
and restore parent focus botched by most dialogs in ActiveState Tk 8.5 on Mac.
--------------------------------------------------------------------------------
"""

AnyDlgParents = True   # use parent=self anywhere, to avoid root lifts?
MacDlgParents = True   # use parent=self on Mac, and accept slide-downs?


def dlgRefocus(self):
    """
    [3.0] On Mac OS X only (and using ActiveState's Tk 8.5: others TBD),
    all standard dialogs except askstring and askinteger do not restore
    focus to the parent window on close, even when the parent=self argument
    is passed; users must click to edit.  This forces focus back to parent
    with a focus_force() on self.text; neither focus_force() on self, nor
    focus_set() on self or self.text suffice in this context.  transient()
    may help (unverified), but is unsupported by most standard dialogs.
    """
    if isinstance(self, TextEditor):
        self.text.focus_force()          # TextEditor window?
    elif self != None:
        self.focus_force()               # allow generic popup too
    else:
        pass                             # allow standalones too

    
def dlgParent(self, orphan):
    """
    Allow for omissions, via parent=dlgparent(self, orphan) in any 3.X.
    Or: return dict(parent=self) and use **dlgparent(self) in py3.5+.
    Change global constants or pass orphan=True to tailor parentage.
    """
    if (not AnyDlgParents) or orphan:
        return None
    elif (not MacDlgParents) and RunningOnMac:
        return None
    else:
        return self


def callDialog(dialog, self, context, message, orphan, pargs, kargs):
    """
    Factor wrapper logic here.
    Example: Help=>About is still a popup (orphan).
    This also sanitizes (replaces) any non-BMP Unicode 
    message text for Tk, else the GUI may fail or hang.
    """
    if hasattr(self, 'appname'):
        applabel = self.appname + ' - '   # allow non-TextEditor parents
    else:                                 # also verified when refocus
        applabel = '' 

    result = dialog(                      # base tkinter or patched dialog
        applabel + context,               # title where shown: 'PyEdit - Open'
        fixTkBMP(message),                # prompt or message text (sanitized)
        *pargs,                           # any extra positional args
        parent=dlgParent(self, orphan),   # use self as parent or not
        **kargs)                          # any extra keyword args

    dlgRefocus(self)                      # else Mac OS X requires a click
    return result


# patch common dialogs: pass kwonly orphan=True to omit parent (see onHelp)

from tkinter.messagebox import showinfo, showerror, askyesno

def my_showinfo(self, context, message, *pargs, orphan=False, **kargs):
    return callDialog(showinfo, self, context, message, orphan, pargs, kargs)

def my_showerror(self, context, message, *pargs, orphan=False, **kargs):
    return callDialog(showerror, self, context, message, orphan, pargs, kargs)

def my_askyesno(self, context, message, *pargs, orphan=False, **kargs):
    return callDialog(askyesno, self, context, message, orphan, pargs, kargs)


# and patch the already-patched input dialogs by redefinition

_askstring  = my_askstring
_askinteger = my_askinteger

def my_askstring(self, context, message, *pargs, orphan=False, **kargs):
    return callDialog(_askstring, self, context, message, orphan, pargs, kargs)

def my_askinteger(self, context, message, *pargs, orphan=False, **kargs):
    return callDialog(_askinteger, self, context, message, orphan, pargs, kargs)


#===============================================================================


def modalMenuAction(method):
    """
    [3.0] A DECORATOR - easier than inserting pre+post action code.
    For Mac OS X, disable all other menu actions that may trigger
    modal dialogs if one is already in progress.  '@'-decorate all
    menu callbacks that may open modal dialogs with this no-argument
    function.  This should be a no-op outside Mac, and harmless
    (other platforms disable a window's menus during modal dialogs).
    See earlier note above for more on modal dialogs and Mac menus.
    """
    def onCall(*pargs, **kargs):                   # saves method in func scope 
        if TextEditor.modalisopen: 
            return                                 # skip call if already modal 
        else:
            TextEditor.modalisopen = True          # lock new requests out now
            try:
                res = method(*pargs, **kargs)      # original method (with self)
                return res                         # and finally runs before exit
            finally:
                TextEditor.modalisopen = False     # enable new requests again
    return onCall                                  # method name = wrapper


def allowModals():
    """
    [3.0] In two cases (onCut, onPaste), a modal menu action calls other
    modal menu actions: forcibly free modal lock so the others can run.
    Two others (save, refind) call modals immediately: don't decorate.
    """
    TextEditor.modalisopen = False


#===============================================================================


def grepThreadProducer(filenamepatt, dirname, grepkey, encoding, case, myqueue):
    """
    --------------------------------------------------------------------
    Moved from class to top-level function so it can be run by the
    multiprocessing module as a workaround for a Python 3.5/Tk 8.6
    random thread crash.  See the class's grep code for the caller.
    
    In a non-GUI parallel thread or process: queue find.find results
    list.  Could also queue matches as found, but need to keep window.
    Note that file content and file names may both fail to decode here.

    TBD: should the match here be case-insensitive per textConfig?
    [3.0] YES: recoded for new policy = case-insensitive by default,
    with a new 'Case?' GUI toggle for sensitive (either may be valid);

    TBD: could pass encoded bytes to find() to avoid filename
    decoding excs in os.walk/listdir, but which encoding to use:
    sys.getfilesystemencoding() if not None?  see also Chapter6 
    footnote issue: 3.1 fnmatch always converts bytes per Latin-1.

    [3.0] Tally and pass to consumer a few search statistics;
    it's important to show how many files were skipped due to
    Unicode errors, so the user can retry with another encoding.
    
    --------------------------------------------------------------------
    [3.0] THE TALE OF THE GREP-THREAD CRASH WORKAROUNDS...
    
    TAKE 1: speculative recodings
    
    This code occasionally crashed due to a threading bug in the
    combination of Python 3.5 and Tk 8.6 (at least), described here:
    learning-python.com/books/python-changes-2014-plus.html#s35E.

    As possible fixes, this was recoded to (1) avoid any possible
    uncaught exceptions in the non-GUI thread, and (2) explicitly
    close input files, though no evidence has ever been found to
    support either theory, and neither should have resulted in a
    hard crash (at best, these may have triggered an unrelated bug).

    The GUI consumer code (in the main class) was also recoded to
    (3) sanitize and truncate result list inserts, but this proved
    irrelevant - the crashes occur before results are pulled from
    the queue.  In the end, NONE of these three recodings were seen
    to have fixed the Tk crash (yes, argh); maybe Tk 8.7 or 8.5 will...
    
    TAKE 2: use processes instead of threads (despite the name)

    The prime suspect now appears to be Python's threading module,
    because Python's more basic _thread module is used extensively in
    the PyMailGUI program without any issues.  Hence, the grep spawn
    code has now been recoded to experiment with all the alternatives:
    threading and _thread's threads, and multiprocessing's processes.
    The latter is used by default (this can be set in textConfig.py). 

    multiprocessing has some downsides:
    - It necessitated moving the parallel task's code here (it requires
      a pickleable callable - a top-level function, or an instance of a
      top-level subclass with run()).
    - It is broken for frozen single-file executable programs (pickle
      imports fail), and required a workaround patch for this context.
      See multiprocessing_exe_patch.py and __main__ for more details.
    - It may startup more slowly (it spawns a new python program on
      Windows and forks a new process on Unix)
    - It cannot do freely-shared state quite like threads (e.g., it
      can't pass object method callables).

    OTOH, multiprocessing sidesteps thread issues completely, and
    runs *faster* where it can leverage multiple CPU cores.  On one
    multicore Windows test machine, N grep processes may run N times
    faster than threads (each gets as much CPU as a single threaded
    process), and the story is similar on Mac OS X (processes can
    consume more CPU time than threads, and finish noticably quicker).

    In addition, state is a moot point here (grep queues just a list
    of strings, not PyMailGUI's callables), and this code can easily
    revert to using threads in the future, because multiprocessing
    exports largely-compatible interfaces.

    Plus, multiprocessing works around the Tk and/or Python thread
    crash.  Such is development in the world of battery dependency.
    
    UPDATE AND CAVEAT: per later usage, it appears that Python 3.5's
    libs can still hard-crash (segfault) on very rare occasions while 
    reading a next line in some UTF-8 files (sigsegv on Mac, at least).
    This may or may not be related to the original crash, and may or 
    may not be triggered by a specific file's unusual content.  It's 
    also a dead end for this program; is it fixed in later Pythons?
    Either way, using processes is warranted by improved speed alone.
    --------------------------------------------------------------------
    """
    from PP4E.Tools.find import find

    # in py3.3+, casefold() is like lower(), but handles Unicode better
    folder = getattr(str, 'casefold', str.lower)
    if not case:
        grepkey = folder(grepkey)                         # [3.0]

    nmatch = nfile = nuerr = nierr = nxerr = nterr = 0    # [3.0]
    matches = []
    try:
        for filepath in find(pattern=filenamepatt, startdir=dirname):
            nfile += 1
            textfile = None
            try:
                textfile = open(filepath, encoding=encoding)
                for (linenum, linestr) in enumerate(textfile):
                    linestr0 = linestr                   
                    if not case:                              # queue orig case
                        linestr = folder(linestr)             # [3.0] 'a'=='A'?
                    if grepkey in linestr:
                        nmatch += 1                           # drop \n for GUI list
                        linestr0 = linestr0.rstrip('\n')
                        msg = '%s@%d  [%s]' % (filepath, linenum + 1, linestr0)
                        matches.append(msg)
            except UnicodeError as X:
                # eg: decode, bom
                nuerr += 1                                    # escape non-ASCII 
                print('Unicode error in:', ascii(filepath), type(X))
            except IOError as X:
                # eg: permission
                nierr += 1
                print('IO error in:', ascii(filepath), type(X))
            except Exception as X:
                # any others? [3.0]
                nxerr += 1
                print('Other error in:', ascii(filepath), type(X))
                print(ascii(sys.exc_info()))
            finally:
                if textfile: textfile.close()                 # always close [3.0]
    except:
        # find excs (filenames?), or any other uncaught (prints?)
        # catch and end exc, instead of propagating with finally [3.0]
        nterr += 1
        print('Uncaught error in grep task:', sys.exc_info()[0])

    print('Matches for %s: %s' % (grepkey, len(matches)))
    summary = '%d %d %d %d %d %d' % (nmatch, nfile, nuerr, nierr, nxerr, nterr)    
    matches.insert(0, summary)      # [3.0] prepend summary line
    myqueue.put(matches)            # stop consumer loop now, no active exc


#===============================================================================


"""
[3.0] Hideous workaround for multiprocessing and Windows frozen executables.

See multiprocessing_exe_patch.py here plus __main__ for all the gory details.
This code is used both as top-level script and module within package, and
the import statement form varies for these two cases in 3.X (a 3.X "feature").
"""

import multiprocessing
try:
    import multiprocessing_exe_patch          # fix multiprocessing in-place
except ImportError:
    from . import multiprocessing_exe_patch   # and when I'm part of a package




#===============================================================================
# (Mostly) original PP4E code follows (but see also "[3.0]"s ahead)
#===============================================================================


Version = '3.0'                                   # 3.0 = post PP4E
import sys, os, glob                              # platform, args, run tools
from tkinter import *                             # base widgets, constants
from tkinter.filedialog   import Open, SaveAs     # standard dialogs
from tkinter.colorchooser import askcolor
from PP4E.Gui.Tools.guimaker import *             # Frame + menu/toolbar builders


# [3.0] no longer used directly - see custom versions above
# from tkinter.simpledialog import askstring, askinteger 

# [3.0] no longer used directly - see custom versions above
# from tkinter.messagebox import showinfo, showerror, askyesno


# general configurations: from first dir on import path (sys.path)
try:
    import textConfig                        # startup font and colors
    Configs = textConfig.__dict__            # work if not on the path or bad
except:                                      # define in client app directory 
    Configs = {}


# a few global Tk constants
START     = '1.0'                   # index of first char: row=1,col=0 (vs END)
SEL_FIRST = SEL + '.first'          # map sel tag to index
SEL_LAST  = SEL + '.last'           # same as 'sel.last'

FontScale = 0                       # use bigger font on Linux, Mac OS X,
if not RunningOnWindows:            # and any other non-Windows boxes
    FontScale = 3

# ANDROID - but use smaller fonts on smaller screens
FontScale = 0


#----------------------------------------------------------------------------
# for Help button and menu About popups (now along with HTML help [3.0]);
# raw Unicode chars work because Py source encoding default is UTF-8 [3.0];
# that is, this source file needs no "# -*- coding: UTF-8 -*-" at its top;
# example: for copyright, use either \u00A9 escape or a raw © character;
#----------------------------------------------------------------------------

HelpText = """PyEdit

Version ☞ %s, June 2017 (Android 2019)

A text-editor and code-launcher program and component.
PyEdit is open source, uses Python 3.X and its tkinter
GUI toolkit, and runs on Mac OS X, Windows, Linux,
and Android.

Author and © M. Lutz 2000-2019. Originally from
the book "Programming Python, 4th Edition" (a.k.a. PP4E),
published by O'Reilly Media, Inc.

For quick access to menu actions, use the toolbar,
accelerator-key shortcuts, and menu tear-offs and
Alt-underline shortcuts where supported. For help
with dialogs, see their Help buttons. For in-depth
usage details and license, see UserGuide.html.

PyEdit Version History

● %s: Jan, 2019 (Android)
● %s: Jun, 2017 (PCs)
● 2.1: Apr, 2010
● 2.0: Jan, 2006
● 1.0: Oct, 2000

★ Version %s was released with Android patches
in January 2019, initially.

★ Version %s adds
custom icons,
non-BMP Unicode replacements,
font- and color-list configs,
dialog help and keys,
color cycling,
auto-saves,
grep search stats,
colored cursors,
menu accelerator keys,
font zoom,
line wrap modes,
toolbar fonts,
already-open checks,
case toggles for searches,
parallel grep processes,
run-code dialog and stream capture,
exe and app bundle distributions,
and full utility on Mac OS X
in addition to Windows and Linux.

★ Version 2.1 was released with PP4E. It addded
Python 3.X code,
a "grep" external-files search dialog,
verified quits if any edit windows' text is changed,
arbitrary Unicode encodings for files,
support for multiple change and font dialogs,
and upgrades to the run-code option.

★ Versions 2.0 and 1.0 appeared in PP3E and PP2E.
1.0 introduced core utility, and 2.0 added
a font-pick dialog,
unlimited undo/redo,
smarter save prompting only if text changed,
case-insensitive search,
and configuration module textConfig.py."""

# fill-in version number
HelpText = HelpText % ((Version,) * 5)

# [3.0] make help look nicer outside Windows (see also HTML help)
HelpText = HelpText.replace('\n', ' ')        # merge lines into paragraph
HelpText = HelpText.replace('  ', '\n\n')     # restore blank lines
HelpText = HelpText.replace(' ●', '\n   ● ')  # fix version bullet list (●, •, ♦)
HelpText = HelpText.replace('\n●', '\n   ● ') # the first is an oddball

# [3.0] on Windows, the hands are illegible in the system font
# used by the infobox common dialog, and no way to set font (?)
if RunningOnWindows:
    HelpText = HelpText.replace('☞', '⇨')     # ☞ beats ☛ on Mac; ★ on all

# [3.0] on Linux, specialize too-large bullets (silly, but true);
# ANDROID [Apr1219] but Linux bullets seem too small - add "False"
# (caveat: larger bullet's size can vary per run; tkinter buglet?);
#
if False and RunningOnLinux:
    HelpText = HelpText.replace('●', '•')     # else huge in info box on Linux

# yes, these render differently on Windows/Linux and Mac...
dialogHelpBullet = '•' if RunningOnMac else '●'




################################################################################
# Main class: implements editor GUI, actions (code grouped by menus);
# requires a flavor of GuiMaker to be mixed in by more specific subclasses;
# not a direct subclass of GuiMaker because that class takes multiple forms.
################################################################################


class TextEditor:
    """
    TextEditor methods: mix with GuiMaker menu/toolbar Frame class,
    and embed in a parent window when being used in standalone mode.
    Class-level names defined here are shared by all windows unless redef.
    """
    
    openwindows  = []            # for process-wide change-test and auto-save
    modalisopen  = False         # [3.0] process-wide modal lock, Mac OS X menus
    autosaving   = False         # [3.0] start just one auto-save timer loop
    namelessid   = 0             # [3.0] autosave filenames: init, New, not Open
    appname      = 'PyEdit'      # [3.0] for GuiMaker automatic help menu text
    openprograms = []            # [3.0] for process-wide spawnee kills at close


    # Unicode policy configurations: from pyedit's own config file;
    # imported in the class to allow overrides in subclass or self;
    # this file is both script and module: py3.X imports need help,
    # unless split importable parts off from __main__ to nested pkg
    
    if __name__ == '__main__':
        from textConfig import (               # my dir is on the path
            opensAskUser, opensEncoding,
            savesUseKnownEncoding, savesAskUser, savesEncoding)
    else:
        try:
            from .textConfig import (          # 2.1: always from this package
                opensAskUser, opensEncoding,
                savesUseKnownEncoding, savesAskUser, savesEncoding)
        except SystemError:
            from textConfig import (           # [3.0] unless multiprocessing...
                opensAskUser, opensEncoding,   # values irrelevant but must load
                savesUseKnownEncoding, savesAskUser, savesEncoding)


    # file-open common type filters
    # [3.0] these are pointless on Mac OS X (and are disabled there ahead)

    ftypes = [('All files',     '*'),                 # for file open dialog
              ('Text files',   '.txt'),               # customize in subclass
              ('Python files', '.py')]                # or set in each instance


    # dialogs that remember the last dir selected, created on first use;
    # in retrospect, probably just as easy to save last folder manually;
    # [3.0] for ease of use these are now process-global, not per-window

    openDialog = None
    saveDialog = None


    # first folder for open/save dialogs
    # tbd: set to None=omitted, so gui picks last visited (like Grep)?
    # [3.0] avoid starting in '.' source-code folder where possible
    # [3.0] this is also now used in Run Code's Sting mode, as a CWD
    
    startfiledir = os.environ.get('HOME',        # Unix (Mac, Linux)
                   os.environ.get('HOMEPATH',    # Windows (no HOME)
                   '.'))                         # else my source dir

    # ANDROID [Mar2819] - use textConfig.py user setting for first path
    # (only), if set to a valid folder (or None=internal-storage root).
    # Else, starts at Pydroid 3's app-private $HOME folder in "/data/data", 
    # and navigating to content on first use can be tedious in Android Tk.
    # '/storage/emulated/0'='/sdcard' but supports navigation to drives.
    #
    androidfiledir = Configs.get('filechooserstart', None) 
    androidfiledir = androidfiledir or '/storage/emulated/0'
    if os.path.isdir(androidfiledir):
        startfiledir = androidfiledir    


    #------------------------------------------------------
    # menu Tools=>Color List presets (+ main setting):
    # applies next one each time Color List is selected;
    # foreground/background, colorname or #RRGGBB hexstr;
    # [3.0] fg used for cursor too, else lost in dark bg;
    # users can also pick colors in GUI, but temporary;
    # [3.0] also now used for auto-color cycling on open;
    #------------------------------------------------------
    
    colors = [
        {'fg': 'white',      'bg': '#173166'},        # color pick list
        {'fg': 'black',      'bg': 'ivory'},          # ANDROID - added for fun
        {'fg': '#ffff66',    'bg': 'black'},          # first item is default
        {'fg': 'black',      'bg': 'lightcyan'},      # tailor these as desired
        {'fg': 'white',      'bg': 'darkgreen'},      # or Pick Bg/Fg chooser
        {'fg': 'white',      'bg': '#800040'},        # maroon - or so they say
        {'fg': 'black',      'bg': '#e4c0a7'},        # light mocha
        {'fg': 'white',      'bg': '#008080'},        # teal
        {'fg': 'black',      'bg': '#d0fffb'},        # three from the website
        {'fg': 'black',      'bg': '#fff5dc'},        # green?, beige?, teal?
        {'fg': 'black',      'bg': '#ddfaff'}, 
        {'fg': 'green2',     'bg': 'black'},          # 3270 terminal, anyone?
        {'fg': '#00ffff',    'bg': '#3b3b3b'},        # a touch of grey
        {'fg': 'white',      'bg': '#664e38'},        # chocolate maybe?
        {'fg': 'black',      'bg': '#f1fdfe'},        # one from pymailgui 
        {'fg': 'black',      'bg': 'wheat'},
        {'fg': '#ffffff',    'bg': '#400080'},        # it's white on purple...
        {'fg': '#ff0000',    'bg': '#000000'},        # red on black (mar/lic)
        {'fg': 'black',      'bg': '#ffb368'},        # orange, but not hurty
        {'fg': 'black',      'bg': '#ffff99'},        # a less-rude yellow
        {'fg': '#00ffff',    'bg': '#000080'},        # turquoise/midnight [sic]
        {'fg': 'black',      'bg': 'white'},          # sans colors
        {'fg': 'black',      'bg': '#00ffff'},        # black on cyan (probably)    
        {'fg': 'black',      'bg': 'aquamarine'},     # a sort of greenish
        {'fg': 'black',      'bg': '#f99b94'},        # was darker 'indian red'},
        {'fg': 'cornsilk',   'bg': '#A28264'},        # brown, and proud of it
        {'fg': 'orange',     'bg': 'navy'},
        {'fg': '#ffffff',    'bg': '#633025'},        # more browns
        {'fg': 'black',      'bg': 'beige'}]          # last is preset fg/bg
    
    if 'colorlist' in Configs:
        colors = Configs['colorlist']   # [3.0] get from textConfig file if set


    #------------------------------------------------------
    # menu Tools=>Font List presets (+ main setting):
    # applies next one each time Font List is selected;
    # (family, size, style), style can be multiple words;
    # users can also pick fonts in GUI, but temporary;
    # Tk guarantees courier, helvetica, and times;
    #------------------------------------------------------

    # ANDROID - none of the fonts marked '###' work, and courier (only) 
    # ignores bold and italic styles, in both font strings and tuples;
    # working: courier, times, helvetica (and monaco=courier, arial=helvetic);
    # added times/helvetica bold/italic and others here for demo on Android;
    # [Feb2019] updated for new findings on Android family/style constraints;

    fonts  = [
        ('courier',       4+FontScale, 'normal'),     # cross-platform, mostly
        ('courier',       6+FontScale, 'normal'),
        ('courier',       8+FontScale, 'normal'),

        ('courier',      10+FontScale, 'normal'),     # (family, size, style)
        ('courier',      10+FontScale, 'bold'),       # bold/italoc ignored
        ('courier',      10+FontScale, 'italic'),     # or Pick Font chooser
        ('courier',      12+FontScale, 'normal'),     # bigger fonts on Unix
        ('courier',      12+FontScale, 'bold'),

        ('times',        12+FontScale, 'normal'),     # 'bold italic' if 2
        ('times',        12+FontScale, 'italic'),     # tbd: show in listbox?
        ('times',        12+FontScale, 'bold'),
        ('times',        12+FontScale, 'italic bold'),

        ('helvetica',    10+FontScale, 'normal'),     # also 'underline',...
        ('helvetica',    10+FontScale, 'italic'),     
        ('helvetica',    10+FontScale, 'bold'),
        ('helvetica',    10+FontScale, 'bold italic'),

        ('arial',        10+FontScale, 'normal'),     # arial==helvetica
        ('courier',      16+FontScale, 'bold'),       # bold ignored
        ('courier',      18+FontScale, 'normal'),
        ('helvetica',    10+FontScale, 'underline'),
        ('monaco',       12+FontScale, 'normal'),     # monaco==courier, fixed-width

    ### ('menlo',        12+FontScale, 'normal'),     # mac os x font: only?
    ### ('lucinda sans', 12+FontScale, 'normal'),     # fixed-width on some
    ### ('consolas',     12+FontScale, 'normal'),     # fixed-width on some
    ### ('inconsolata',  12+FontScale, 'normal'),     # fixed-width on some

        ('courier new',  11+FontScale, 'normal'),     # where != 'courier' 
        ('courier new',  11+FontScale, 'bold'),       # differs on Mac

    ### ('tahoma',       11+FontScale, 'normal'),     # nice on all
    ### ('symbol',       11+FontScale, 'normal'),     # wacky on Windows 
    ### ('herculanum',   13+FontScale, 'normal'),     # mac+? (odin's font?)
    ### ('papyrus',      13+FontScale, 'normal'),     # mac+win (just for yucks)
    ### ('impact',       12+FontScale, 'normal')     # poster-like, win+mac
        ]

    if 'fontlist' in Configs:
        fonts = Configs['fontlist']     # [3.0] get from textConfig file if set 
    



    ############################################################################
    # General methods
    ############################################################################

    
    def __init__(self, loadFirst='', loadEncode=''):
        """
        What the TextEditor class requires, after GuiMaker.__init__.
        See top-level classes ahead for other protocol calls run.
        By the time this is called, the menu and toolbar have been
        built, and makeWidgets() has created text in the middle.
        Any self-level names defined here are local to this window.
        """
        if not isinstance(self, GuiMaker):
            raise TypeError('TextEditor needs a GuiMaker mixin')

        self.setFileName(None)
        self.lastfind   = None                      # init this window's state
        self.knownEncoding = None                   # 2.1 Unicode: till Open or Save
        self.text.focus()                           # else must click in text

       #self.openDialog = None                      # [3.0] now session-global
       #self.saveDialog = None

        # [3.0] update() is no longer required: see setAllText()
        if loadFirst:
           #self.update()                           # 2.1: else @ line 2; see book
            self.onOpen(loadFirst, loadEncode)      # this might not open a file

        # [3.0] auto-save filename ids and loop        
        TextEditor.namelessid += 1                  # autosave filenames seq#
        self.namelessid = TextEditor.namelessid     # save current count on me
        if not TextEditor.autosaving:
            self.autoSaveLoop()                     # start just one timer loop
            TextEditor.autosaving = True
                
        # [3.0] window tracking
        # auto-register every open window - both top-level and component;
        # this list is used for change-tests on quit [2.1] and auto-saves [3.0];
        TextEditor.openwindows.append(self)
        
        # [3.0] auto-deregister every window when destroyed
        def deregisterTracking(event):
            """
            called on the <Destroy> event of editor's Text widget;
            this Tk event is fired after a window's tkinter destroy()
            method is run, but neither is invoked on app-wide quit() 
            (see also docetc/examples/*/demo-tk-destroy-events.py);
            when run, self is viable, but the widget is half dead:
            this handler can't test for changes, fetch text, etc.;
            """
            print('PyEdit got <Destroy>')
            TextEditor.openwindows.remove(self)
        self.text.bind('<Destroy>', deregisterTracking)


    def start(self):
        """
        --------------------------------------------------------------------
        Run by GuiMaker.__init__, via the top-level classes ahead:
        set menu/toolbars, before accBindWidget() and makeWidgets().
        Coded as an instance method, so actions have access to a self.
        Underlines: [Alt+<menuchar1>,<key>] shortcuts on Windows/Linux.
        
        [3.0] Added menu accelerator keys; these are in addition to the
        Alt-key underline shortcuts on Windows and Linux, but underlines
        don't work on the Mac, and its menu is farther away at screen top.
        Underlines also fail on Windows/Linux in embedded Frame menus,
        and are no longer displayed in this context.
        
        Most of the magic here occurs in utility ../Tools/guimaker.py.
        In accelerators, '*'/'?' stand for platform-specific keys (e.g.,
        '*' is Command on Mac and displays as an icon; it means Control
        on Windows/Linux and displays as 'Ctrl+').  More details ahead.
        
        [3.0] Note that some menu/toolbar options handled explictly here
        also have preset Text-widget binding equivalents with automatic
        actions (e.g., ctrl|cmd-c/v for copy/paste, ctrl|cmd-z for undo),
        which are disabled by the same-key accelerators specified here.
        The built-ins update the widget's changed flag and undo stacks.

        [3.0] Reorganized menus and their underline shortcut keys to
        highlight most commonly used, and added a few more separators.
        Also reorganized and expanded the toolbar, and allow its layout
        style and font to be configured in textConfig.py; use the space.
        --------------------------------------------------------------------
        """

        #-------------------------------------------------------------------
        # Configure menubar - a GuiMaker menu-def tree:
        #
        #   [(label,
        #     [(label, underline-shortcut, handler, accelerator-shortcut?)]]
        #
        # In underlines, the value is the label character's offset. 
        # In accelerators, '*'=cmd|ctl and '?'=ctl|alt on mac|others:
        #   -on Mac, '*-f' = cmd+f, '?-f' = ctl+f, '?-*-f' = ctl+cmd+f
        #   -on Win, '*-f' = ctl+f, '?-f' = alt+f, '?-*-f' = alt+ctl+f
        # Note: built-in bindings are auto-disabled by the GuiMaker utility.
        # Caution: see top-level component classes if File menu is changed.
        #
        # Caveat: Ctl+Cmd+key triples fail when embedded in PyMailGUI - why?
        # Caveat: some accelerators override Alt-key combos; use the former.
        # Caveat: Cmd+Shift combos don't seem to work on Mac in AS TK 8.5.
        # Caveat: Cmd-equals/plus don't display in menus on Mac (use other).
        #-------------------------------------------------------------------
        
        self.menuBar = [
            ('File', 0,                                 # [3.0] reorg, add septs                                
                 [('Open...',
                       0, self.onOpen,      '*-o'),     # components accs too
                  ('New',
                       0, self.onNew,       '*-n'),     # new file, this window
                  '----',
                  ('Save',
                       0, self.onSave,      '*-s'),     # first and later saves
                  ('Save As...',
                       5, self.onSaveAs,    '?-s'),     # save under a new name
                  '----',
                  ('Quit...',
                       0, self.onQuit,      '?-q')]     # was '?-*-q', but fails
            ),
            ('Edit', 0,
                 [('Undo',
                       0, self.onUndo,      '*-u'),     # not ctrl-z: built-in
                  ('Redo',
                       0, self.onRedo,      '*-r'),     # shift-cmd-z not on mac
                  '----',
                  ('Cut',
                       0, self.onCut,       '?-c'),     # or Copy+(bkspc|fn+del)
                  ('Copy',
                       3, self.onCopy,      '*-c'),     # same as built-in copy
                  ('Paste',
                       0, self.onPaste,     '*-v'),     # like built-in paste
                  '----',
                  ('Delete',
                       0, self.onDelete,    None),      # select+(bkspc|fn+del)
                  ('Select All',
                       0, self.onSelectAll, '*-a')]
            ),
            ('Search', 0,                               # [3.0] new separators
                 [('Goto...',
                       0, self.onGoto,      '*-l'),     # goto a numbered line
                  '----',
                  ('Find...',
                       0, self.onFind,      '?-f'),     # first simple find 
                  ('Refind',
                       0, self.onRefind,    '?-g'),     # find simple again 
                  ('Change...',
                       0, self.onChange,    '*-f'),     # dialog best for finds
                  '----',
                  ('Grep...',
                       3, self.onGrep,      '*-g')]     # files search dialog
            ),
            ('View', 0,                                 # [3.0] +zoom, old Tools
                 [('Zoom In',
                       5, self.onFontPlus,  '?-i'),     # incr font size+config
                  ('Zoom Out',                          # plus: Mac shift fails
                       5, self.onFontMinus, '?-o'),     # decr font size+config
                  '----',                               # minus: Mac not shown
                  ('Font List',                         # next in presets list
                       0, self.onFontList,  'F1'),      # was '?-*-f', but fails
                  ('Pick Font...',
                       0, self.onPickFont,  'F2'),      # or choose in dialog
                  '----',
                  ('Color List',                        # next in presets list
                       0, self.onColorList, 'F3'),      # was '?-*-c' but fails
                  ('Pick Bg...',
                       5, self.onPickBg,    'F4'),      # or choose in dialog
                  ('Pick Fg...',
                       6, self.onPickFg,    'F5'),      # or choose in dialog
                  '----',
                  ('Line Wrap',                         # [3.0] toggle wrapping
                       5, self.onLineWrap,  'Escape')]
            ),            
            ('Tools', 0,                                # [3.0] reorg, shortcuts
                 [('Info...',
                       0, self.onInfo,      '*-i'),     # file information
                  '----',
                  ('Popup',
                       0, self.onPopup,     '*-p'),     # [3.0] Tk=>Tolevel
                  ('Clone',
                       0, self.onClone,     '?-p'),     # Tk=>Tk, Top=>Top
                  '----',
                  ('Run Code...',
                       0, self.onRunCode,   '*-x')]     # a simple IDE option
            )
        ]


        #-------------------------------------------------------------------
        # Configure toolbar - a GuiMaker toolbar-def tree:
        #
        #   [(label, handler {packing-in-toolbar-arg}) | spacer]
        #
        # For spacer, '<...' = pack left, and '>...' = pack right.
        # Redundant with menus and accelerator-key combos, but
        # useful, especially on tablets (tiny menus, no keyboards).
        # This could use small GIF images, but keep it simple here.
        # It's also subjective and not user-configurable (today).
        #-------------------------------------------------------------------

        # user may configure the botton's font (None=system default)
        self.toolbarFont = Configs.get('toolbarFont', None)

        # user may pick fixed or expanding spacers (e.g., '<---')
        self.toolbarFixedLayout = Configs.get('toolbarFixedLayout', False)

        # avoid redundancy (or dict(side=X))
        packLeft  = {'side': LEFT}
        packRight = {'side': RIGHT}

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # About using "portable" Unicode symbols for toolbar buttons:
        # Mac
        #   renders arrows, etc., great, though they're arguably obscure;
        #   probably, this could evolve to use totally incomprehensible GIFs...
        # Windows
        #   renders fat arrows unevenly across machines, even within same
        #   font family; abandoned arrows for ASCII characters on Windows;        
        # Linux
        #   buttons are huge and arrows renders too small: reuse Windows
        #   format to save space, and consider nuking some middle buttons;
        #   as is: uses wider init size, user can shrink to clip middles;
        #
        # UPDATE: the Linux toolbar width was resolved by using narrower 
        # Labels in guimaker, instead of Buttons; no need to make window 
        # wide, etc.  Other platforms could use Labels too, but it's not 
        # necessary: Mac Labels are spaced same, and shorter/rectangular.
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        runcode = 'Run ⚙'
        popup   = 'Pop☝' if not RunningOnLinux else 'Pop ☝'   # need a space?
        info    = '  ⅈ  ' if RunningOnMac else 'Info'           # Mac fonts rule
        
        if RunningOnWindows or RunningOnLinux:
            if True:
                bg, fg, inc, dec, pick, wrap = 'bf+-?↲'   # no spaces needed
            else: # alt
                bg, fg, inc, dec, pick, wrap = '↑↓↑↓?↲'   # but arrows too small
        else: # Mac
            if True:
                bg, fg, inc, dec, pick, wrap = ('⇧', '⇩', '⇧', '⇩', ' ? ', '⏎')
            else: # alt
                bg, fg, inc, dec, pick, wrap = [' %s ' % c for c in 'bf+-?'] + ['⏎']

        # ANDROID - make hieroglyphs a bit bigger via Mac setting + ? spaces
        bg, fg, inc, dec, pick, wrap = ('⇧', '⇩', '⇧', '⇩', '  ?  ', '⏎')


        self.toolBar = [
            # right side 
            ('Quit',   self.onQuit,      packRight),  # first=rightmost
            ('Help',   self.onHelp,      packRight),  # pack 1st=clip last
            '>---',
            (info,     self.onInfo,      packRight),  # [3.0] added info, ⅈ?
            (popup,    self.onPopup,     packRight),  # [3.0] new window, ☝?
            (runcode,  self.onRunCode,   packRight),  # [3.0] added for fun, ⚒, ⚙?
            '>---',

            # left side
            ('Save',   self.onSave,      packLeft),
            ('Open',   self.onOpen,      packLeft),   # [3.0] added open
            '<---',                                   # [3.0] toolbar spacer
            ('Cut',    self.onCut,       packLeft),   
            ('Copy',   self.onCopy,      packLeft),
            ('Paste',  self.onPaste,     packLeft),
            '<---',
            ('Undo',   self.onUndo,      packLeft),   # [3.0] added for Mac,
            ('Redo',   self.onRedo,      packLeft),   # [3.0] pre menu acc
            '<---',
            ('Find',   self.onChange,    packLeft),   # [3.0] not onRefind
            ('Grep',   self.onGrep,      packLeft),   # [3.0] added for use
            '<---',
            ('Color',  self.onColorList, packLeft),   # [3.0] added these
            (bg,       self.onPickBg,    packLeft),   # rarely used? 
            (fg,       self.onPickFg,    packLeft),
            '<---',
            ('Font',   self.onFontList,  packLeft),   # there's space...
            (inc,      self.onFontPlus,  packLeft),   # zoom in, ⇧ or ↑ 
            (dec,      self.onFontMinus, packLeft),   # zoom out, ⇩ or ↓
            (pick,     self.onPickFont,  packLeft),   # Pick, ⇳, ⇵, …, ⌨
            (wrap,     self.onLineWrap,  packLeft)    # or Wrap, ⏎, ↲

            # then right-side spacer after Run
        ]

        if RunningOnLinux:
            pass  # no need to remove middle buttons: now uses Labels instead


    def accBindWidget(self):
        """
        [3.0] Run by GuiMaker.__init__, after start(), and before making
        menus and calling makeWidgets().  Return the widget on which menu
        accelerator key events are to be bound, if GuiMaker accelerators
        used.  Returning self.master may fail: this might be an embedded
        component instance, and type may impact firing of built-in bindings;
        Text widgets work, and GuiMaker replaces same-key default bindings.
        """
        text = Text(self)      # to be configured later: see makeWidgets
        self.text = text       # don't pack it here/yet: defer for clip order 
        return text            # intercepts accelerator events when has focus


    def makeWidgets(self):
        """
        Run by GuiMaker.__init__ after start() and menu/toolbar setup,
        but before TextEditor.__init__ is called from top-level classes.
        At this point, "self" is a GuiMaker mid-window Frame object,
        between the created menu and toolbar: build text area in middle.
        """
        name = Label(self, bg='black', fg='white')   # add below menu, above tool
        name.pack(side=TOP, fill=X)                  # menu/toolbars are packed
                                                     # GuiMaker frame packs itself
        vbar = Scrollbar(self)
        hbar = Scrollbar(self, orient='horizontal')
       #text = Text(self, padx=5, wrap='none')       # original coding
        text = self.text                             # [3.0] now made earlier
        text.config(padx=5, wrap='none')             # disable line wrapping
        text.config(undo=1, autoseparators=1)        # 2.0, default is 0, 1

        vbar.pack(side=RIGHT,  fill=Y)
        hbar.pack(side=BOTTOM, fill=X)                 # pack text last: clip 1st
        text.pack(side=TOP,    fill=BOTH, expand=YES)  # else sbars clipped

        text.config(yscrollcommand=vbar.set)     # call vbar.set on text move
        text.config(xscrollcommand=hbar.set)     # ditto for hbar.set
        vbar.config(command=text.yview)          # call text.yview on scroll move
        hbar.config(command=text.xview)          # or hbar['command']=text.xview

        # 2.0: apply user configs or defaults
        startfont = Configs.get('font', self.fonts[0])          # var or list[0]
        startbg   = Configs.get('bg',   self.colors[0]['bg'])   # bg can be dark 
        startfg   = Configs.get('fg',   self.colors[0]['fg'])   # for cursor too
        text.config(font=startfont, bg=startbg, fg=startfg)

        # [3.0] cursor=fg, else can be lost in a dark bg
        text.config(insertbackground=startfg)

        # [3.0] auto add initial values to end of pick lists so selectable,
        # unless already present or added by a previously-created window
        if Configs.get('font'):
            if not startfont in self.fonts:
                self.fonts.append(startfont)         # self okay for class attr

        if Configs.get('fg') and Configs.get('bg'):
            initcols = dict(fg=startfg, bg=startbg)
            if not initcols in self.colors:          # dict '==' works in py3.X
                self.colors.append(initcols)  

        # uses tk default if unset: 24 lines x 80 chars
        if 'height' in Configs: text.config(height=Configs['height'])
        if 'width'  in Configs: text.config(width =Configs['width'])

        # [3.0] color cycling: auto set next window to next in color list;
        # this option applies to both top-level windows and components;
        if Configs.get('colorCycling', False):
            if TextEditor.namelessid > 0:            # all but first window
                self.onColorList()                   # next fg/bg from list

        # [3.0] Escape key toggles line-wrapping (at char boundaries) on and off
        # this was adapted from the Run Code output window (it's that cool)
        self.textwrapped = 0    # now a 3-state toggle, start=none

        self.text = text        # redundant but descriptive
        self.filelabel = name   # save widgets for changing


    def autoSaveLoop(self):
        """
        ------------------------------------------------------------------------
        [3.0] If configured to do so, every 5 minutes (by default) save a
        copy of the current text in every open, changed, and unsaved PyEdit
        window or widget, to the configured self-cleaning auto-save folder.

        Usage notes:
        -- By design, this DOES NOT overwrite actual files being edited,
           but saves copies in a dedicated, separate folder.  It's just a
           last-resort backup in case of outright crash or operator mistake.
           Saved files will generally be useful immediately, or not at all.
        -- Cleans up auto-save files more than one week old (by default)
           to minimize clutter/space in the save dir
        -- Auto-save applies to both top-level (main and popup) windows, and
           embedded components in client program windoes (e.g., PyMailGUI
           View/Write mail text).  All PyEdit window types are auto-saved.
        -- Time between runs and retention days are now configurable, but
           their defaults are reasonable: 5 mins is roughly just 1 paragraph,
           and catastrophic data loss is likely known immediately or soon  
        -- To disable folder cleaning but leave auto-save enabled, set the
           days-retained to a very high number (but these files are temps);
           to disable auto-saves set its folder to None.

        Coding notes:
        -- Uses either a known filename, or one generated for still-nameless
           windows.  In the former, the pathname (as much of it as possible)
           is appended to the filename to make same-named files unique in the
           auto-save folder, whether edited in the same or different sessions.
           In the latter, a window counter makes names unique in a session,
           and a process id makes them unique across sessions
        -- Uses general UTF-8 Unicode because a desired Unicode encoding
           may not yet be known or appropriate
        -- Runs just 1 auto-save timer loop per process, shared by any
           number of open windows in the session
        -- Tk's widget.after() method requires that widget not be destroyed
           before the timer expires, else no callback occurs (for proof, see
           docetc/examples/demo-poll-silent-exit-on-window-close.py)  Since
           "self" may be temporary (e.g., PyMailGUI components or popups), use
           tkinter._default_root, the implicit or explicit first-created Tk()
           that endures for the program, but fallback on "self" if it's None
           or unset ("self" is saved by tkinter callback even if its window
           is destroyed, so it can be used both for the timer handler and the
           after() widget).  See tkinter.NoDefaultRoot() for more on this story.
           This may preclude an all peer-level Tk() model: one window must be
           long-lived, and a "welcome" Tk() might open on every click on some.
        -- The ascii() calls for print() in announce() avoid exceptions when
           printing filenames with emojis on Mac OS X with no console (really)
        -- All Pyedit windows are automatically registered for auto-save on
           creation, and deregistered in their Text widgets' <Destroy> handler;
           registry is implemented as a simple global (class-level) list.
        -- Assumes CWD not changed if the save-path is relative to '.' (and
           the default is); now true, but Run Code's String mode made it iffy.
        -- TBD: this could be threaded if it ever becomes a noticable pause;
           unless you're running on a floppy drive, it's probably fine...
        ------------------------------------------------------------------------
        """
        import time
        helpfile   = 'README-autosaves.txt'                   # spared reaping
        savedir    = Configs.get('autoSaveToFolder')          # default=dir in '.'
        savemins   = Configs.get('autoSaveMinsTillRun',  5)   # 5 mins default
        retaindays = Configs.get('autoSaveDaysRetained', 7)   # 7 days default


        def savename(pathname):
            """
            Convert a known pathname of a file to a name under
            which it may be saved in the auto-save folder.  This
            adds as much of the enclosing path as possible to make
            same-named files located at different paths distinct.

            This isn't foolproof, as the name's length is limited
            per supported-platform constraints (and filesystems:
            wikipedia.org/wiki/Comparison_of_file_systems#Limits),
            but the "correct" solution of storing full folder trees
            is slow to create and prune, and lousy on usability.

            The pathname is already absolute, as recorded by PyEdit.
            It must have only legal chars because it has been used,
            be we need to replace separators, and ':' for Windows.
            Truncating dirpath on the end seems just as likely to
            distinguish the file as truncating on the front (tbd).

            Caveat: though files save correctly here, they may result
            in paths exceeding Windows' length limits in some contexts.
            Run paths through os.path.abspath() and prefix with '\\?\'
            where needed, per the mergeall and ziptools programs' fixes.
            """
            namemax  = 255  # common denominator
            filename = os.path.basename(pathname)
            dirpath  = os.path.dirname(pathname)
            dirpath  = dirpath.replace(os.sep, '_')
            dirpath  = dirpath.replace(':', '_')
            savename = '%s--AT--%s' % (filename, dirpath)
            if len(savename) > namemax:
                savename = savename[:namemax - 3] + '...'
            return savename

 
        def announce(*args):
            """
            Standard format with program name: may be embedded.
            Run all args through ascii() to avoid emoji errors. 
            """
            def isascii(text):
                try:    text.encode('ascii')
                except: return False
                else:   return True
            print('PyEdit auto-save',
                  *((arg if isascii(arg) else ascii(arg)) for arg in args))


        #--------------------------
        # autoSaveLoop starts here
        #--------------------------
        
        if not savedir:
            # None or missing: disabled - skip loop altogether
            return
        
        else:
            announce('running')

            # 1) cleanup auto-save folder items > N days old
            try:
                if os.path.exists(savedir):
                    for filename in os.listdir(savedir):
                        if filename == helpfile:
                            continue
                        pathname = os.path.join(savedir, filename)
                        modtime  = os.path.getmtime(pathname)   # epoch seconds
                        nowtime  = time.time()                  # ditto
                        dayssecs = retaindays * 24 * 60 * 60
                        if nowtime > modtime + dayssecs:
                            announce('pruning:', pathname)
                            try:
                                os.remove(pathname)
                            except Exception as why:
                                announce('skipped failed file:', why)
            except Exception as why:
                announce('reaper failed:', why)  # but continue here

            # 2) save copies of changed+unsaved files to auto-save folder
            windows = TextEditor.openwindows     # all open windows 
            changed = any(w.text_edit_modified() for w in windows)
            if not changed:
                pass   # nothing to save: go reschedule
            else:
                try:
                    if not os.path.exists(savedir):
                        os.mkdir(savedir)
                    for window in windows:
                        if window.text_edit_modified():
                            try:
                                knowname = window.getFileName()
                                if knowname:
                                    # use known file+path 
                                    filename = savename(knowname)
                                else:
                                    # create a fake name
                                    count = window.namelessid    # unique in session
                                    mypid = os.getpid()          # unique on machine 
                                    filename = '_nameless-%d-%d.txt' % (count, mypid)

                                # write to auto-save dir
                                filepath = os.path.join(savedir, filename)
                                fileobj  = open(filepath, 'w', encoding='utf8')
                                fileobj.write(window.getAllText())
                                fileobj.close()
                            except Exception as why:
                                announce('skipped file:', filename, why)
                            else:
                                announce('saved file:', filepath)
                except Exception as why:
                    announce('ended by exception:', why)    # but continue GUI

            # 3) reschedule for next run
            announce('finished')
            try:
                # use a window that endures
                import tkinter                              # app's Tk root win?
                topwin = getattr(tkinter, '_default_root', None) 
                regwin = topwin or self                     # or resort to self
                msecstimer = savemins * 60 * 1000           # N minutes of msecs
                regwin.after(msecstimer, self.autoSaveLoop) # go again in N mins
            except Exception as why:
                announce('reschedule failed:', why)         # probably never, but...
            # back to tk event loop




    ############################################################################
    # File menu commands
    ############################################################################


    def fixTkBMP_FileDialogs(self, dialogobj):
        """
        [3.0] for file Open and SaveAs dialogs, pass initialfile=None to 
        avoid tkinter errors if a prior call selected and cached a filename
        with a non-BMP Unicode character, and also pass initialdir=None if
        the prior pathname pick had such text; else, a saved file/dir name
        with emojis causes the dialog to fail on errors when run by Python;

        this disables highlighting of the prior file and/or starting in 
        the prior dir, but we avoid this in normal cases when the prior 
        choices were all BMP, and the effect spans just one call (the next 
        open/save can use a prior valid initialfile and initialdir again);
        Mac SaveAs dialogs prefill prior filename instead of highlighting,
        and uses "Untitled" if intitaldir=None, but is otherwise the same;

        this is a broad tkinter+Tk file-dialog issue: tkinter saves the 
        prior choice, and Tk supports only BMP text; fixed locally here,
        but _every_ tkinter dialog object (not func call) has the issue;
        """
        priorfile = dialogobj.options.get('initialfile', '')
        priorpath = dialogobj.options.get('initialdir', '')
     
        if isNonBMP(priorpath):
            # forget both for this call only
            return dict(initialdir=None, initialfile=None)

        elif isNonBMP(priorfile):
            # forget file for this call only, use path
            return dict(initialfile=None)

        else:
            # use both prior file and path for this call
            return dict()


    def my_askopenfilename(self):
        """
        use dialog objects that remember last result dir and file
        [3.0] add custom title text, and specialize its arg name for Mac
        [3.0] filetypes '*.*' fails on Mac: non-matches grey, unselectable
        [3.0] use parent=self so root not raised above subject window;
        this also triggers slide-down sheet style on Mac per its norms;
        [3.0] fix emojis in prior choice via fixTkBMP_FileDialogs args;  
        """
        # make dialog object first time
        if not self.openDialog:
            title = self.appname + ': Open File'
            if RunningOnMac:
                dlgargs = dict(
                    message=title,                   # Mac open ignores 'title'
                    initialdir=self.startfiledir)    # Mac fails on 'filetypes'
            else:
                dlgargs = dict(
                    title=title,                     # Windows+Linux use title
                    initialdir=self.startfiledir,    # Windows fails on 'message'
                    filetypes=self.ftypes)
            TextEditor.openDialog = Open(**dlgargs)

        # disable prior file/path name picks having emojis: kills dialog
        fixBMPargs = self.fixTkBMP_FileDialogs(self.openDialog)

        # run the dialog, restore focus
        choice = self.openDialog.show(
                     parent=self,           # don't lift root window, use Mac sheet
                     **fixBMPargs)          # avoid non-BMP Unicode failures 
        dlgRefocus(self)                    # [3.0] else Mac needs click if Cancel
        return choice                       # empty string or selected pathname 


    def my_asksaveasfilename(self):
        """
        use dialog objects that remember last result dir and file
        [3.0] add custom title text (no need to specialize arg for Mac);
        [3.0] use parent=self so root not raised above subject window;
        [3.0] fix emojis in prior choice via fixTkBMP_FileDialogs args;  
        """
        # make dialog object first time
        if not self.saveDialog:
            title = self.appname + ': Save File'          
            dlgargs = dict(
                title=title,                         # save uses title on all 3                                                   
                initialdir=self.startfiledir,        # filetypes okay on Mac:
                filetypes=self.ftypes)               # greyed out but selectable
            TextEditor.saveDialog = SaveAs(**dlgargs)

        # disable prior file/path name picks having emojis: kills dialog
        fixBMPargs = self.fixTkBMP_FileDialogs(self.saveDialog)

        # run the dialog, restore focus
        choice = self.saveDialog.show(
                     parent=self,           # don't lift root window, use Mac sheet
                     **fixBMPargs)          # avoid non-BMP Unicode failures 
        dlgRefocus(self)                    # [3.0] else Mac needs click if Cancel
        return choice                       # empty string or selected pathname 


    def findTopLevel(self):
        """
        [3.0] climb tkinter parentage chain to containing window;
        used to lift the top-level window containing TextEditor self,
        whether self is a standalone window or a nested component;
        """
        window = self.master
        while window and not isinstance(window, (Tk, Toplevel)):
            window = window.master
        return window


    @staticmethod
    def liftWindows(windows):
        """
        [3.0] lift the windows containing all the open PyEdit editor
        widgets in list 'windows' to the top of the display, and set
        focus on their text;  initially used by both Open (where
        'windows' is widgets where a file is already open) and Quit
        (where 'windows' is widgets with unsaved changes);  static,
        because also called by PyMailGUI's main list window's Quit;
        """
        for win in windows:
            toplevel = win.findTopLevel()
            if toplevel.state() == 'iconic':   # raise window if withdrawn
                toplevel.deiconify()           # then lift above others
            toplevel.lift()                    # may be > 1 changed/reopened:
            win.text.focus_set()               # the last will be activated


    @modalMenuAction
    def onOpen(self, loadFirst='', loadEncode=''):
        """
        ----------------------------------------------------------------------
        2.1: total rewrite for Unicode support; open in text mode with 
        an encoding passed in, input from the user, in textconfig, or  
        platform default, or open as binary bytes for arbitrary Unicode
        encodings as last resort and drop \r in Windows end-lines if 
        present so text displays normally; content fetches are returned
        as str, so need to  encode on saves: keep encoding used here;

        tests if file is okay ahead of time to try to avoid opens;
        this code could also load and manually decode bytes to str to
        avoid multiple open attempts (like Save ahead), but it is
        unlikely that this code will wind up trying all its cases;

        encoding behavior is configurable in the local textConfig.py:
        1) tries known type first if passed in by client (email charsets)
        2) if opensAskUser True, try user input next (prefill wih defaults)
        3) if opensEncoding nonempty, try this encoding next: 'latin-1', etc.
        4) tries sys.getdefaultencoding() platform default next
        5) uses binary mode bytes and Tk policy as the last resort

        end-lines: because the 'newline' parameter is not passed to open(),
        this code is able to read files having any end-line format (DOS \r\n
        or Unix \n), and receives its read results in universal \n format
        in text mode 'r' (binary-mode reads do not translate end-lines);

        file closes: as coded, this relies on the fact that CPython file 
        objects automatically close() themselves when garbage collected, 
        which happens here when expression temporaries are discarded;

        [3.0] add already-open test/raise, and return True if and only if
        a file was opened (else None) to avoid a bad line# error in Grep;

        [3.0] warn the user about replacements and destructive saves if the
        file content has non-BMP "emoji" chracters; Tk ~8.6 doesn't support;
        ----------------------------------------------------------------------
        """

        if self.text_edit_modified():    # 2.0
            if not my_askyesno(self, 'Open', 'Text has changed: discard changes?'):
                return

        file = loadFirst or self.my_askopenfilename()
        if not file: 
            return
        
        if not os.path.isfile(file):    # [3.0] links to files are okay too
            my_showerror(self, 'Open', 'Could not open file ' + file)
            return

        # [3.0] same-process already-open test: raise window, or let user reopen;
        # this applies to nested components too, and nameless windows are moot;
        # TBD: don't ask if (len(openwindows) == 1 and openwindow[0] == self)?
        
        match = os.path.abspath(file)
        openwindows = [w for w in TextEditor.openwindows if w.currfile == match]
        if openwindows:
            self.update()
            if my_askyesno(self, 'Open', 'File already open: reopen anyhow?'):
                # continue with duplicate open
                pass
            else:
                # raise already-open instance(s)
                self.liftWindows(openwindows)       # may be > 1 if reopened
                return                              # some callers may onQuit() now

        # try known encoding if passed and accurate (e.g., email)
        text = None     # empty file = '' = False: test for None!
        if loadEncode:
            try:
                text = open(file, 'r', encoding=loadEncode).read()
                self.knownEncoding = loadEncode
            except (UnicodeError, LookupError, IOError):         # lookup: bad name
                pass

        # try user input, prefill with next choice as default
        if text == None and self.opensAskUser:
            self.update()  # else dialog doesn't appear in rare cases
            askuser = my_askstring(self, 'Open',
                                   'Enter Unicode encoding for open',
                                   initialvalue=(self.opensEncoding or 
                                                 sys.getdefaultencoding() or ''))
            self.text.focus()  # else must click (now auto)
            if askuser:
                try:
                    text = open(file, 'r', encoding=askuser).read()
                    self.knownEncoding = askuser
                except (UnicodeError, LookupError, IOError):
                    pass
            # else return? no - more options ahead

        # try config file (or before ask user?)
        if text == None and self.opensEncoding:
            try:
                text = open(file, 'r', encoding=self.opensEncoding).read()
                self.knownEncoding = self.opensEncoding
            except (UnicodeError, LookupError, IOError):
                pass

        # try platform default (utf-8 on windows; try utf8 always?)
        if text == None:
            try:
                text = open(file, 'r', encoding=sys.getdefaultencoding()).read()
                self.knownEncoding = sys.getdefaultencoding()
            except (UnicodeError, LookupError, IOError):
                pass

        # last resort: use binary bytes and rely on Tk to decode
        if text == None:
            try:
                text = open(file, 'rb').read()         # bytes for Unicode
                text = text.replace(b'\r\n', b'\n')    # for display, saves
                self.knownEncoding = None
            except IOError:
                pass

        if text == None:
            my_showerror(self, 'Open', 'Could not decode and open file ' + file)
        else:
            self.setAllText(text)
            self.setFileName(file)
            self.text.edit_reset()             # 2.0: clear undo/redo stks
            self.text.edit_modified(0)         # 2.0: clear modified flag

            # [3.0] raise window above root, focus text
            # no longer needed if parent=self for dialogs
            """
            self.update()
            toplevel = self.findTopLevel()     # or self.liftWindows([self])
            toplevel.lift()                    # update(), else root on top
            self.text.focus_set()              # focus, else user must click
            """

            # [3.0] warn user about potential for destructive saves;
            # could user showwarning, but not used, and same on Mac;
            # could do this in setAllText, but that's only used here,
            # and for PyMailGUI's non-file raw text and View windows
            # (PyMailGUI's text-part popups will wind up coming here);
            
            if isinstance(text, str) and isNonBMP(text):   # bytes is right out!  
                self.update()   # show text first
                my_showinfo(self, 'Open', 
                    'Caution: this file contains non-BMP Unicode characters '
                    'that have been replaced for display.  Saving its text '
                    'to a file may result in loss of the characters replaced. '
                    'See the User Guide\'s "About emojis" for details.') 
                
            return True   # iff actually opened a file (else returns None)
            

    def onSave(self):
        """
        save text to file (currfile may be None if first save);
        no need for @modalMenuAcion here: onSaveAs already does,
        and would need to allowModals() to clear lock if used;
        """
        self.onSaveAs(self.currfile)


    @modalMenuAction
    def onSaveAs(self, forcefile=None):
        """
        ----------------------------------------------------------------------
        2.1: total rewrite for Unicode support: Text widget content is
        always returned as a str, so we must deal with encodings to save
        to a file here, regardless of open mode of the output file (binary
        requires bytes, and text must encode); tries the encoding used
        when opened or saved (if known), user input, config file setting,
        and platform default last; most users can use platform default; 

        retains successful encoding name here for next save, because this
        may be the first Save after New or a manual text insertion;  Save
        and SaveAs may both use last known encoding, per config file (it
        probably should be used for Save, but SaveAs usage is unclear);
        gui prompts are prefilled with the known encoding if there is one;
        
        does manual text.encode() to avoid creating file too soon; text
        mode files perform platform-specific end-line conversion: Windows
        \r is dropped if present on open() by text mode (auto) and binary
        mode (manually); if content is inserted into the widget manually,
        inserter must delete \r else duplicates here; knownEncoding=None
        before first Open or Save, after New, and if binary Open;

        encoding behavior is configurable in the local textConfig.py:
        1) if savesUseKnownEncoding > 0, try encoding from last open or save
        2) if savesAskUser True, try user input next (prefill with known?)
        3) if savesEncoding nonempty, try this encoding next: 'utf-8', etc
        4) tries sys.getdefaultencoding() as a last resort

        end-lines: because the 'newline' parameter is not passed to open(),
        this code always writes files using the hosting platform's end-line
        format (all \n are translated to os.linesep: DOS \r\n or Unix \n);
        see the utility fixeoln.py in tools/ if this is not desireable;
        ----------------------------------------------------------------------
        """

        filename = forcefile or self.my_asksaveasfilename()
        if not filename:
            return

        # get text from the Tk widget
        text = self.getAllText()      # 2.1: a str string, with \n eolns,
        encpick = None                # even if read/inserted as bytes 

        # try known encoding at latest Open or Save, if any
        if self.knownEncoding and (                                  # enc known?
           (forcefile     and self.savesUseKnownEncoding >= 1) or    # on Save?
           (not forcefile and self.savesUseKnownEncoding >= 2)):     # on SaveAs?
            try:
                text.encode(self.knownEncoding)
                encpick = self.knownEncoding
            except UnicodeError:
                pass

        # try user input, prefill with known type, else next choice
        if not encpick and self.savesAskUser:
            self.update()  # else dialog doesn't appear in rare cases
            askuser = my_askstring(self, 'Save',
                                   'Enter Unicode encoding for save',
                                   initialvalue=(self.knownEncoding or 
                                                 self.savesEncoding or 
                                                 sys.getdefaultencoding() or ''))
            self.text.focus() # else must click
            if askuser:
                try:
                    text.encode(askuser)
                    encpick = askuser
                except (UnicodeError, LookupError):    # LookupError:  bad name 
                    pass                               # UnicodeError: can't encode

        # try config file
        if not encpick and self.savesEncoding:
            try:
                text.encode(self.savesEncoding)
                encpick = self.savesEncoding
            except (UnicodeError, LookupError):
                pass

        # try platform default (utf8 on windows)
        if not encpick:
            try:
                text.encode(sys.getdefaultencoding())
                encpick = sys.getdefaultencoding()
            except (UnicodeError, LookupError):
                pass

        # open in text mode for endlines + encoding
        if not encpick:
            my_showerror(self, 'Save', 'Could not encode for file ' + filename)
        else:
            try:
                file = open(filename, 'w', encoding=encpick)
                file.write(text)
                file.close()
            except:
                my_showerror(self, 'Save', 'Could not write file ' + filename)
            else:
                self.setFileName(filename)          # may be newly created
                self.text.edit_modified(0)          # 2.0: clear modified flag
                self.knownEncoding = encpick        # 2.1: keep enc for next save
                # but don't clear undo/redo stks!
                
                # [3.0] raise window above root, focus text
                # no longer needed if parent=self for dialogs
                """
                self.update()
                toplevel = self.findTopLevel()      # or self.liftWindows([self])
                toplevel.lift()                     # update(), else root on top
                self.text.focus_set()               # focus, else user must click
                """

                return True   # iff actually saved a file (else returns None)

                
    @modalMenuAction
    def onNew(self):
        """
        start editing a new file from scratch in current window;
        onClone and onPopup make new independent edit windows instead;
        """
        if self.text_edit_modified():    # 2.0
            if not my_askyesno(self, 'New', 'Text has changed: discard changes?'):
                return

        self.setFileName(None)                    # clear text, reset state
        self.clearAllText()
        self.text.edit_reset()                    # 2.0: clear undo/redo stks
        self.text.edit_modified(0)                # 2.0: clear modified flag
        self.knownEncoding = None                 # 2.1: Unicode type unknown

        TextEditor.namelessid += 1                # [3.0] autosave filenames
        self.namelessid = TextEditor.namelessid   # my new id for text to be 


    @modalMenuAction
    def onQuit(self):
        """
        on Quit menu/toolbar select and wm border X button in toplevel windows;
        2.1: don't exit app if others changed;  2.0: don't ask if self unchanged;
        
        moved to the top-level window classes at the end since may vary per usage:
        a Quit in GUI might quit() to exit, destroy() just one Toplevel, Tk, or 
        edit frame, or not be provided at all when run as an attached component;
        check self for changes, and if might quit(), main windows should check
        other windows in the process-wide list to see if they have changed too; 
        """
        assert False, 'onQuit must be defined in window-specific sublass' 


    def text_edit_modified(self):
        """
        2.1: this now works! seems to have been a bool result type issue in tkinter;
        2.0: self.text.edit_modified() broken in Python 2.4: do manually for now; 
        """
        return self.text.edit_modified()
       #return self.tk.call((self.text._w, 'edit') + ('modified', None))




    ############################################################################
    # Edit menu commands
    ############################################################################


    @modalMenuAction
    def onUndo(self):
        """
        2.0: unlimited undos of edits, per Tk stacks
        """
        try:                                     # tk8.4 keeps undo/redo stacks
            self.text.edit_undo()                # exception if stacks empty
        except TclError:                         # menu tear-offs for quick undo
            my_showinfo(self, 'Undo', 'Nothing to undo')


    @modalMenuAction
    def onRedo(self):
        """
        2.0: unlimited redos of undone edits, per Tk stacks
        """
        try:
            self.text.edit_redo()
        except TclError:
            my_showinfo(self, 'Redo', 'Nothing to redo')


    @modalMenuAction
    def onCopy(self):
        """
        get text selected by mouse (etc.), and save it in the
        cross-app clipboard; this also happens on ctrl|command-C;
        """
        if not self.text.tag_ranges(SEL):
            my_showerror(self, 'Copy', 'No text selected')
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)


    @modalMenuAction
    def onDelete(self, strict=True):
        """
        delete selected text, without saving it to clipboard;
        if not strict, okay if nothing is selected (for paste);
        """
        if not self.text.tag_ranges(SEL):
            if strict:
                my_showerror(self, 'Delete', 'No text selected')
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)


    @modalMenuAction
    def onCut(self):
        """
        save to clipboard and delete seleted text (copy+delete);
        cut text is available both in PyEdit and other programs
        """
        if not self.text.tag_ranges(SEL):
            my_showerror(self, 'Cut', 'No text selected')
        else:
            allowModals()       # both of these are modal actions
            self.onCopy()       # reuse code: this is a combo action
            self.onDelete()


    @modalMenuAction
    def onPaste(self):
        """
        insert clipboard text at current insert cursor;
        this also generally happens on ctrl|command-V;
        
        [3.0] new paste model: delete selection so a paste
        replaces it instead of just inserting before/after,
        else user must manually delete just before paste;
        
        also do _not_ select pasted text: now that we're
        replacing selection, repastes would require a cick;
        they formerly did not, as selection was not deleted;
        prior select allowed immediate cut (rare use case);

        [3.0] need to manually insert Undo separators here,
        else consecutive Pastes, and an edit following them,
        are backed out as a unit;  see onDoChange() ahead;
        """
        try:
            text = self.selection_get(selection='CLIPBOARD')
        except TclError:
            my_showerror(self, 'Paste', 'Nothing to paste')
            return
        
        allowModals()
        self.text.config(autoseparators=0)      # [3.0] assume ctrl
        self.text.edit_separator()              # [3.0] delimit Undo change
        self.onDelete(strict=False)             # replace selected text, if any
        self.text.insert(INSERT, text)          # add at current insert cursor
        self.text.see(INSERT)
        self.text.edit_separator()              # [3.0] delimit Undo change
        self.text.config(autoseparators=1)      # [3.0] back to auto

        
        # was: select it, so can be cut
        #self.text.tag_remove(SEL, START, END)
        #self.text.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)


    def onSelectAll(self):
        """
        select entire text in widget, for copy/cut/etc.
        """
        self.text.tag_add(SEL, START, END+'-1c')   # select entire text
        self.text.mark_set(INSERT, START)          # move insert point to top
        self.text.see(INSERT)                      # scroll to top




    ############################################################################
    # Search menu commands
    ############################################################################


    @modalMenuAction
    def onGoto(self, forceline=None):
        """
        move text view, cursor, and selection to an input line number
        """
        line = forceline or my_askinteger(self, 'Goto', 'Enter line number')
        self.text.update()
        self.text.focus()
        if line is not None:
            maxindex = self.text.index(END+'-1c')
            maxline  = int(maxindex.split('.')[0])
            if line > 0 and line <= maxline:
                self.text.mark_set(INSERT, '%d.0' % line)      # goto line
                self.text.tag_remove(SEL, START, END)          # delete selects
                self.text.tag_add(SEL, INSERT, 'insert + 1l')  # select line
                self.text.see(INSERT)                          # scroll to line
            else:
                my_showerror(self, 'Goto', 'Bad line number')


    @modalMenuAction
    def onFind(self, lastkey=None, forcenocase=None):
        """
        search for a substring from current cursor, per Configs case setting;
        if found, move text view, cursor, and selection to found substring;
        [3.0] string-not-found is now an info message, not an error message;
        
        [3.0] for legacy reasons, this simple dialog still uses the textConfig
        case setting;  Change and Grep instead default to case-insensitive,
        and have new a 'Case?' toggle that allows case-sensitive to be used;
        Change reuses this method, however, so it has grown a forcenocase arg;
        """
        key = lastkey or my_askstring(self, 'Find', 'Enter search string')
        self.text.update()
        self.text.focus()
        self.lastfind = key
        if key:
            if forcenocase != None:
                nocase = forcenocase    # [3.0] toggle in Change
            else:                                                  # 2.0: nocase
                nocase = Configs.get('caseinsens', True)           # 2.0: config
                
            where = self.text.search(key, INSERT, END, nocase=nocase)
            if not where:                                          # don't wrap
                my_showinfo(self, 'Find', 'String not found')
            else:
                pastkey = where + '+%dc' % len(key)           # index past key
                self.text.tag_remove(SEL, START, END)         # remove any sel
                self.text.tag_add(SEL, where, pastkey)        # select key
                self.text.mark_set(INSERT, pastkey)           # for next find
                self.text.see(where)                          # scroll display


    def onRefind(self):
        """
        find again from last find (or start find if first time);
        no need for @modalMenuAction, as onFind already ensures,
        and would need to allowModals() to clear lock if used;
        """
        self.onFind(self.lastfind)


    def onChange(self):
        """
        -----------------------------------------------------------------------------
        non-modal find/change dialog - can use to both find, and find+replace;
        2.1: pass per-call/dialog inputs to callbacks, may be > 1 change dialog open;
        TBD: should this have a "Change All" option?  inclined to say no: dangerous!
        [3.0] binding Enter=Find doesn't work here: it would delete the selected text
              because the Text widget gets focus after each Find to speed new edits;
        [3.0] binding Escape=show/hide help fails too: can't pack in  gridded parent
        [3.0] default to case-insensitive, and add 'Case?' toggle for sensitive;
        [3.0] on Mac, set default app menubar for nonmodal dialogs, else erased;
        [3.0] add 'Top' button to goto top and re-search: for manual wrap-arounds;
        [3.0] fix undo separators so each change undone as a unit: see onDoChange();
        [3.0] lift() dialog so not hidden, focus() find text to save initial click;
        -----------------------------------------------------------------------------
        """
        new = Toplevel(self)                  # pertains to and closed with self
        try_set_window_icon(new)              # [3.0] icons (and leave resizable)
        new.title('PyEdit - Find/Change')

        # [3.0] call guimaker's Mac menubar fixer for nonmodal dialog window
        fixAppleMenuBarChild(new)

        Label(new, text='Find text?', relief=RIDGE, width=15).grid(row=0, column=0)
        Label(new, text='Change to?', relief=RIDGE, width=15).grid(row=1, column=0)
        entry1 = Entry(new, width=30)
        entry2 = Entry(new, width=30)
        entry1.grid(row=0, column=1, sticky=EW)
        entry2.grid(row=1, column=1, sticky=EW)

        # local callback handlers use names in enclosing method's scope
        # all three lift() so that dialog isn't covered by text window 
        
        def onFind():
            """
            find next occurrence of search string
            this is like Find but with a case toggle
            """
            nocase  = not caseSensVar.get()      # [3.0] pass toggle's inverse too
            findstr = entry1.get()               # [3.0] don't trigger Find popup
            if not findstr:
                my_showerror(self, 'Find/Change', 'Please enter a Find string')
            else:
                self.onFind(findstr, nocase)     # runs normal find dialog callback
            new.lift()                           # [3.0] raise above text window

        def onChange():
            """
            replace last found text and refind
            propagate the case toggle for the refind
            """
            nocase   = not caseSensVar.get()     # [3.0] pass toggle's inverse too
            findstr  = entry1.get()              # [3.0] don't trigger Find popup
            changeto = entry2.get()
            if not findstr:
                my_showerror(self, 'Find/Change', 'Please enter a Find string')
            else:
                self.onDoChange(findstr, changeto, nocase)
            new.lift()

        def onTop():
            """
            convenience: go to top of this file to search again
            deselect all so a Change has nothing to silently erase
            """
            self.onGoto(1)
            self.text.tag_remove(SEL, START, END)          # remove selection
            new.lift()
                
        Button(new, text='Find',   command=onFind ) .grid(row=0, column=2, sticky=EW)
        Button(new, text='Change', command=onChange).grid(row=1, column=2, sticky=EW)
        new.columnconfigure(1, weight=1)               # expandable entries
        
        # [3.0] add usage help hints pulldown (dialog-specific: not a popup)
        helptext = [
        'This stay-up dialog allows you to both find and change text in the',
        'PyEdit window from which the dialog was opened.  It uses two main',
        'buttons with associated input strings at the top of the dialog:',
        '',
        '%s Find (search string)' % dialogHelpBullet,
        '    Searches ahead for the next appearance of the first string,',
        '    and highlights and selects it, but does not replace it.',
        '',
        '%s Change (replacement string)' % dialogHelpBullet,
        '    Replaces the last-found and highlighted string with the second',
        '    string and searches ahead for the next occurrence of the first.',
        '',
        'Repeated Finds refind and select the string but do not replace it.',
        'Repeated Changes replace and refind the string on each new press.',
        'In all cases, searches look for a literal string, not a pattern.',
        '',
        'Searches run from current cursor location to end of file; click any',
        "text to set cursor, or 'Top' to jump to top of file to search anew.",
        '',
        "In this dialog, finds are case-insensitive ('a' ==' A') by default;",
        "turn the 'Case?' toggle on to match case exactly ('a' != 'A').",
        '',
        'The Enter (return) key does not perform any action in this dialog,',
        'because its intent is ambiguous; click Find or Change per your goals.',
        "Refind (e.g., control/Alt+g) also repeats this dialog's prior Find.",
        '',
        "Press 'Help' to open and close this help.  Tips: see the Search",
        "menu's Grep command for searching external files instead of PyEdit",
        'windows, and its Find+Refind actions (and their accelerator keys)',
        'for a simpler but limited alternative to the Find button here.'
        ]
        hlpfrm = Frame(new)
        hlpfrm.grid(row=2, columnspan=2)              # need frame to pack child
        self.addDialogHelp(hlpfrm, hlpfrm, helptext)  # see grep, Escape=Help?

        # [3.0] add Top button for manual wrap-around and re-search
        Button(hlpfrm, text='Top', command=onTop).pack(side=RIGHT, anchor=NE)
        
        # [3.0] add case-sensitivity toggle, next to new help
        caseSensVar = IntVar()
        chk = Checkbutton(new, text='Case?')
        chk.config(variable=caseSensVar)
        caseSensVar.set(0)
        chk.grid(row=2, column=2, sticky=N)

        # [3.0] save the user an initial click (focus_set is focus)
        entry1.focus_set()


    def onDoChange(self, findstr, changeto, casetoggle):
        """
        on Change in nonmodal find/change dialog: change and refind;
        
        [3.0] two undo/redo changes;  FIRST, force a new separator
        on the Tk undo stack, so that an Undo undoes just this change;
        not normally required in autoseparator mode, but in some Tks,
        an Undo undoes *all* find/change edits at once (a Tk bug?);

        SECOND, disable autoseparators temporarily here so that an
        Undo backs out the entire change as a whole;  even when auto
        separators work, users must Undo both a delete and an insert;

        note that redundant separators are simply discarded, per Tk's
        docs: see http://www.tcl.tk/man/tcl8.4/TkCmd/text.htm#M73;
        autoseparators are also odd for PyEdit's Paste and required a
        similar fix above, else Undo backs out Paste + following edits;
        """
        if self.text.tag_ranges(SEL):                      # must find first
            self.text.config(autoseparators=0)             # [3.0] assume ctrl
            self.text.edit_separator()                     # [3.0] per above
            self.text.delete(SEL_FIRST, SEL_LAST)          
            self.text.insert(INSERT, changeto)             # deletes if empty
            self.text.see(INSERT)
            self.onFind(findstr, casetoggle)               # goto next appear
            self.text.update()                             # force refresh
            self.text.edit_separator()                     # [3.0] per above           
            self.text.config(autoseparators=1)             # [3.0] back to auto


    def onGrep(self):
        """
        --------------------------------------------------------------------
        new in version 2.1: threaded external-file search;
        search matched filenames in entire directory tree for string;
        matches listbox clicks open matched file at line of occurrence;
        spans 4 windows: grep => grepping => matches list => match edit;

        search is either threaded or spawned in a process so the GUI
        remains active and is not blocked, and to allow multiple greps
        to overlap in time;  could use PP4E threadtools for threads,
        but avoid polling loop if no active grep;

        grep Unicode policy: text files content in the searched tree 
        might be in any Unicode encoding: we don't ask about each (as
        we do for opens), but allow the encoding used for the entire
        tree to be input, preset it to the platform filesystem or 
        text default, and skip files that fail to decode; in worst 
        cases, users may need to run grep N times if N encodings might
        exist;  else opens may raise exceptions, and opening in binary
        mode might fail to match encoded text against search string;

        TBD: better to issue an error if any file fails to decode? 
        but utf-16 2-bytes/char format created in Notepad may decode 
        without error per utf-8, and search strings won't be found;
        TBD: could allow input of multiple encoding names, split on 
        comma, try each one for every file, without open loadEncode?
        
        [3.0] note: latin-1 may find more than utf-8 in some cases;
        [3.0] added stats with #Unicode errors to results window;
        [3.0] code workarounds to a Python 3.5/Tk 8.6 thread crash;
        [3.0] default to case-insensitive, and add 'Case?' toggle;
        [3.0] on Mac, set default app menubar for nonmodal dialogs;
        --------------------------------------------------------------------
        """
        from PP4E.Gui.ShellGui.formrows import makeFormRow

        # nonmodal dialog: get dirnname, filenamepatt, grepkey
        popup = Toplevel()                   # stays open: not closed with self
        try_set_window_icon(popup)           # [3.0] icons (and leave resizable)
        popup.title('PyEdit - Grep')

        # [3.0] call guimaker's Mac menubar fixer for nonmodal dialog window
        fixAppleMenuBarChild(popup)

        # [3.0] implement and use folder browse button for directory root
        var1 = makeFormRow(popup, label='Directory root',   width=18, browse=True,
                           folder=True, app='PyEdit - Grep')
        var2 = makeFormRow(popup, label='Filename pattern', width=18, browse=False)
        var3 = makeFormRow(popup, label='Search string',    width=18, browse=False)
        var4 = makeFormRow(popup, label='Content encoding', width=18, browse=False)

        # prefill initial/suggested values
        #var1.set('.')                       # current dir not very useful: pyedit's
        thisfile = self.getFileName()        # use dir of window's abs filename, if any
        if thisfile != None:
            var1.set(os.path.dirname(thisfile))
        else:
            var1.set('.')                    # or '*.py*' for .pyw (.pyc error out)
        var2.set('*.py')                     # all py files in tree (but not .pyw)
        var4.set(sys.getdefaultencoding())   # for file content, not filenames

        # [3.0] add case-sesitivity toggle, off by default
        case = IntVar()
        chkb = Checkbutton(popup, text='Case?')
        chkb.config(variable=case)
        case.set(0)
        chkb.pack(side=RIGHT, anchor=N)

        def onGrepSearch():
            # vars in per-call/dialog enclosing scope, not per-editor self
            self.onDoGrep(
                var1.get(), var2.get(), var3.get(), var4.get(), case.get())

        btnfrm = Frame(popup)
        btnfrm.pack(side=TOP)
        sbtn = Button(btnfrm, text='Search', command=onGrepSearch)
        sbtn.pack(side=LEFT)
        popup.bind('<Return>', lambda event: onGrepSearch())   # [3.0] Enter=Search

        # [3.0] add usage help hints pulldown (dialog-specific: not a popup)
        helptext = [
        'This stay-up dialog performs external-file search.  On each Search click',
        'it searches all the files in the entire folder tree at "Directory root",',
        'whose names match "Filename pattern", for the provided "Search string".',
        '',
        'Searches are run in parallel processes that report their results in new',
        "popups on completion.  Searches do not block PyEdit's GUI, and multiple",
        'searches may be run at the same time.  Dialog inputs:',
        '',
        '%s Directory root' % dialogHelpBullet,
        '    The pathname of the folder tree whose files you wish to search.',
        "    Use Browse to pick a directory with your platform's file-dialog GUI,",
        '    or type or paste a directory pathname into the input field manually.',
        "    This is prefilled with the directory of the window's file, if known.",
        '',
        '%s Filename pattern' % dialogHelpBullet,
        '    The name pattern of the files you wish to search in the folder.  Use',
        '    *=any substring, ?=any character, [seq]/[!seq]=any in/not in seq, and',
        '    any other characters match literally.  Enclose any special characters',
        '    in brackets (e.g., x[?]y).  Filename case-sensitivity is per platform.',
        '    Tip: use "*.py*" to include both .py and .pyw Python source-code files;',
        '    non-text files matching the pattern (e.g., .pyc) are skipped on errors.',
        '',
        '%s Search string' % dialogHelpBullet,
        '    The string you wish to search for in all matching files in the folder.',
        '    A literal string (not pattern), matched case-insensitively by default',
        "    ('a' == 'A').  Set 'Case?' toggle on to match case exactly ('a' != 'A')." ,
        '',
        '%s Content encoding' % dialogHelpBullet,
        '    The name of the Unicode text encoding to apply when reading all files,',
        "    prefilled with your platform's default.  utf-8 is common and handles",
        '    ASCII too, but some files may require others (e.g., latin-1 or utf-16);',
        '    rerun with other encodings if Unicode errors != 0 in the results popup',
        '    and the files skipped on these errors are valid text (not binary data).',
        '',
        'Double-Click lines in the post-search popup to goto matching files/lines:',
        'each opens in a new PyEdit window that scrolls to and highlights a match.',
        'This popup displays matches as "filepath@linenumber [matchinglinetext]".',
        '',
        'When there are very many matches, a dialog is issued allowing you to skip',
        'the matches-list display, because it may stall the GUI, and even hang it in',
        'worst cases.  Skipping is recommended for pathologically-large results.',
        '',
        'Tips: this dialog\'s Enter key also starts a search, and Escape opens or',
        'closes this help display.  Run PyEdit in a console (command line) to see',
        'which files fail to decode; a latin-1 encoding is often useful on errors.',
        '',
        'Grep is useful for tracking down all occurrences of a string among a set of',
        'text files on your computer.  To search just the text in one PyEdit window',
        'instead, see the Search menu\'s Find and Change commands.  Note: Grep may',
        "not work if PyEdit is run in Python's IDLE GUI; start PyEdit in other ways."
        ]
        self.addDialogHelp(popup, btnfrm, helptext)


    def addDialogHelp(self, popup, btnfrm, helptext):
        """
        [3.0] add a Help button to the LEFT of btnfrm that opens/closes an
        embedded text widget with hints, and bind Escape on popup window to
        open it too;  factored to a common method here so reusable for
        other dialogs (currently: pickfont, find/change);  caller: make
        popup window nonresizable if possible, else help may be munged;
        """
        from tkinter.scrolledtext import ScrolledText
        
        helpopen = False
        def onFontHelp():
            # vars in per-call/dialog enclosing scope, not per-editor self
            nonlocal helpopen
            if not helpopen:
                helpfrm.pack(side=BOTTOM, fill=X, padx=20, pady=20)
            else:
                helpfrm.pack_forget()
            helpopen = not helpopen    # toggle on/off on each call

        hbtn = Button(btnfrm, text='Help', command=onFontHelp)
        hbtn.pack(side=LEFT)
        popup.bind('<Escape>', lambda event: onFontHelp())   # [3.0] Escape=Help
        
        helpfrm = Frame(popup, border=2, relief=RIDGE)
        display = ScrolledText(helpfrm,
                       height=min(20, len(helptext)),
                       width=max(len(line) for line in helptext)+1)
        display.insert(END, '\n'.join(helptext))
        display.config(state=DISABLED)            # read-only (and copy on Windows only)
        display.pack(fill=X)                      # caller makes dialog resizable or not 


    def onDoGrep(self, dirname, filenamepatt, grepkey, encoding, case):
        """
        --------------------------------------------------------------------
        on Go in grep dialog: populate scrolled list with matches, by
        spawning a non-GUI thread/process that produces matches, and
        a GUI timer loop that polls for and consumes the match result;
        
        note that multiple greps can OVERLAP in time, because each grep
        active has its own result queue, producer task, and consumer loop,
        and each grep displays its results in its own popup list window
        (but your drive may run slowly if many greps are reading at once);
        
        tbd: should the producer thread be daemonic so it dies with app?
        [3.0] give more details in the popup window than just grepkey;
        [3.0] this is now coded to spawn grep in one of a variety of 
        ways to possibly work around a Python 3.5/Tk 8.6 threading crash;
        --------------------------------------------------------------------
        """
        import threading, queue, _thread, multiprocessing   # latter patched 

        # make non-modal un-closeable dialog
        mypopup = Toplevel()                   # [3.0] not Tk, not closed with self
        try_set_window_icon(mypopup)           # [3.0] cusom icon where supported
        mypopup.title('PyEdit - Grepping')
        mypopup.protocol('WM_DELETE_WINDOW', lambda: None)  # ignore X close

        # [3.0] call guimaker's Mac menubar fixer for nonmodal dialog window
        fixAppleMenuBarChild(mypopup)

        # [3.0] more details in the busy popup
        statusfrm = Frame(mypopup)
        statusfrm.pack(padx=20, pady=20)
        status1 = 'Grep is searching for %r using %r' % (grepkey, encoding)
        status2 = 'in all files %r in tree %r' % (filenamepatt, dirname)
        Label(statusfrm, text=status1).pack()
        Label(statusfrm, text=status2).pack()

        # start the non-GUI producer thread or process [3.0]
        spawnMode = Configs.get('grepSpawnMode') or 'multiprocessing'
        print('Using', spawnMode)
        grepargs = (filenamepatt, dirname, grepkey, encoding, case)

        if spawnMode == '_thread':
            # basic thread module (used with no crashes in pymailgui)
            myqueue = queue.Queue()
            grepargs += (myqueue,)
            _thread.start_new_thread(grepThreadProducer, grepargs)
            
        elif spawnMode == 'threading':
            # enhanced thread module (original coding: crashes?)
            myqueue = queue.Queue()
            grepargs += (myqueue,)
            threading.Thread(target=grepThreadProducer, args=grepargs).start()

        elif spawnMode == 'multiprocessing':
            # thread-like processes module (slower startup, faster overall?)
            myqueue = multiprocessing.Queue()
            grepargs += (myqueue,)
            multiprocessing.Process(target=grepThreadProducer, args=grepargs).start()

        else:
            assert False, 'bad grepSpawnMode setting'

        # start the GUI consumer polling loop
        self.grepThreadConsumer(
            grepkey, filenamepatt, case, encoding, myqueue, mypopup)


    def defunct_grepThreadProducer(self,
                filenamepatt, dirname, encoding, grepkey, case, myqueue):
        """
        in a non-GUI parallel thread: queue find.find results list;
        [3.0] due to a thread crash in Python 3.5/Tk 8.6, this code
        was rewritten to use multiprocessing, and consequently moved
        to a top-level, picklable function above in this file; see that
        function for documentation removed here; a top-level class with
        a run() method works too, but needs extra code to save args; 
        """
        pass  # UNUSED: now a top-level function near the top of this file      


    def grepThreadConsumer(self, grepkey, patt, case, encoding, myqueue, mypopup):
        """
        in the main GUI thread: poll in a timer loop to watch
        the queue for a results list, and pass it on to handler;
        there may be multiple active grep threads/loops/queues;
        there may be other types of threads/checkers in process,
        especially when PyEdit is attached component (PyMailGUI);

        [3.0] Tk's widget.after() method requires that widget not be
        destroyed before the timer expires, else no callback occurs;
        since "self" is the standalone or embedded edit window from
        which the grep dialog was opened and may be closed while the
        grep searches, use the implicit or explicit first-created Tk(),
        tkinter._default_root, that endures for the program, but use
        "self" fallback if it's None (autoSaveLoop() for more details);
        """
        import queue, tkinter
        try:
            matches = myqueue.get(block=False)
        except queue.Empty:
            myargs  = (grepkey, patt, case, encoding, myqueue, mypopup)
            topwin  = getattr(tkinter, '_default_root', None) 
            regwin  = topwin or self
            regwin.after(250, self.grepThreadConsumer, *myargs)   # 4 per sec
        else:
            mypopup.destroy()     # close status window
            self.update()         # ensure it's erased now

            # notify with simple popup (Mac: slide-down in text window)
            # then show results, but no popup if no results (1=stats)
            # update: show popup anyhow, for error stats (e.g., Unicode)
            # update: but self may be destroyed/closed before the grep
            # finishes, or while grep dialog remains on screen: punt!
            
            if False:   # <= Nope
                my_showinfo(self, 'Grep', 'Grep found %d matches for: %r' %
                        (len(matches) - 1, grepkey))

            # [3.0] warn the user about a huge number of matches; the 
            # results list load is not threaded, and can easily hang 
            # the GUI, if not kill it outright due to memory issues;

            if True or len(matches) > 1:    # <= do always: no initial popup
                proceed = True
                if len(matches) > 2500:
                    proceed = my_askyesno(None, 'Grep: Many Matches Warning',
                              'There are %s matches.  A large number of '
                              'matches may take some time to display, and a very '
                              'large number may hang the GUI altogether.\n\n'
                              'Continue to the match results list?' % 
                              format(len(matches) - 1, ','))
                    self.update()
                if proceed:
                    print('Matches list open', flush=True)
                    self.grepMatchesList(matches, grepkey, patt, case, encoding)


    def grepMatchesList(self, matches, grepkey, patt, case, encoding):
        """
        --------------------------------------------------------------------
        populate list after successful matches, open files on clicks;
        we already know file Unicode encoding from the search: use 
        it here when filename clicked, so the open doesn't ask user;

        [3.0] give number matches and file failures in a label too;
        these are now passed as matches[0] from the producer thread,
        else they show up only in the console (when there is one);
        
        [3.0] need to replace any non-BMP Unicode characters in lines
        for display in Tks ~8.6 (though 8.7 may support emojis); also
        truncate any weirdly-long lines to ensure they don't trigger
        a known Tk crash (see the producer code above for details:
        it's unlikely that the code in this consumer is a factor, as
        the crash occurs _before_ the producer queues its results);

        [3.0] avoid a bad line# error message if file was already open
        and user declined to reopen it, by checking return value of an
        explicit onOpen() call after constructor run;  also close the
        new edit window in this event: we could scroll to the line in
        the existing and lifted window, but the user may not want this,
        there may be > 1, and onOpen()'s result is just boolean (tbd);

        [3.0] tries to avoid a brief empty-window "flash" that appears
        _only_ for the PyInstaller frozen executable of PyMailGUI on 
        Windows (not for PyEdit's own exe, or source or Mac app), but 
        the withdraw/deiconify doesn't seem to help, even if update()
        immediately after, for reasons tbd; punt -- likely a Tk issue;
        --------------------------------------------------------------------
        """
        from PP4E.Gui.Tour.scrolledlist import ScrolledList

        # [3.0] grab stats from first item in matches list
        summary, matches = matches[0], matches[1:]                  # or x, *y
        searchstats = tuple(int(num) for num in summary.split())
        assert searchstats[0] == len(matches)

        # catch list double-click: parse match line, open editor
        class ScrolledFilenames(ScrolledList):
            def runCommand(self, selection):  
                file, line = selection.split('  [', 1)[0].split('@')
                editor = TextEditorMainPopup(
                     winTitle='Grep match popup'          # parent=None=Tk root
                     )                                    # not closed with self
                opened = editor.onOpen(file, encoding)
                if opened:
                    editor.onGoto(int(line))        # goto line in new window
                    editor.text.focus_force()       # no, really  
                else:
                    editor.onQuit()   # close new edit window: it's bogus now

        # new non-modal window
        popup = Toplevel()           # [3.0] not Tk(), not closed with self
        popup.withdraw()             # [3.0] avoid flash (Win PyMailGUI exes only)
        try_set_window_icon(popup)   # [3.0] custom icon where supported
        popup.title('PyEdit - Grep matches: %r (%s)' % (grepkey, encoding))

        # [3.0] make window larger initially (esp. on Mac)
        screenwide = popup.winfo_screenwidth()    # full screen size, in pixels
        screenhigh = popup.winfo_screenheight()
        popup.geometry('%dx%d' % (screenwide * 0.75, screenhigh * 0.50))
        #popup.geometry('%dx%d' % (min(screenwide, 900), min(screenhigh, 300)))

        # [3.0] call guimaker's Mac menubar fixer for nonmodal dialog window
        fixAppleMenuBarChild(popup)

        # [3.0] show search-stats label 
        infotemplate = ('Stats: key=%r, patt=%s, case=%d, encoding=%s, '
            'matches=%d, files=%d, errors=(Unicode=%d, IO=%d, other=%d, find=%d)')
        infotext = infotemplate % ((grepkey, patt, case, encoding) + searchstats)
        Label(popup, text=infotext, bg='black', fg='white').pack(fill=X)

        # [3.0] sanitize Unicode, truncate pathologically-long lines
        # [3.0] add horizontal scroll and configurable list font
        matches = [fixTkBMP(match) for match in matches]
        matches = [match[:500]     for match in matches]
        ScrolledFilenames(parent=popup,
                          options=matches,
                          horizscroll=True,
                          listfont=Configs.get('grepMatchesFont', None))

        popup.deiconify()   # show window now
        popup.lift()        # raise on screen now (former notify popup dropped)




    ############################################################################
    # View menu commands [3.0]
    ############################################################################


    def currentFont(self):
        """
        return Python font spec (family, size, style) of current text font;
        much magic here - need to parse out tcl parts and strip '{}' if present:
        
        'courier 12 bold' => ['courier', '12', 'bold']
        'courier 12 {bold italic}' => ['courier', '12', 'bold italic']
        'courier 12 {}' => ['courier', '12', '']
        '{courier new} 12 {bold italic}' => ['courier new', '12', 'bold italic']

        result tuple contains all strings: convert size to int as needed;
        result also padded with default values to make length=3 always
        (if config-file fonts omit the size and/or style parts they work,
        but fonstr here gets just 1 or 2 parts; onPickFont() sets all 3);
        """
        import re
        fontstr = self.text.config()['font'][-1]                    # at end of config val 
        tclsubs = re.findall(r'(?:\{[^\}]*\})|(?:[^ ]+)', fontstr)  # '{non-}}' or 'nonblank'
        pyparts = [sub.strip('{}') for sub in tclsubs]              # drop '{}' if present

        # pad with default size/styles if missing (family is required)
        if len(pyparts) == 1:
            pyparts.append(0)      # omitted size: 0=default for family
        if len(pyparts) == 2:
            pyparts.append('')     # omitted styles: ''=default=normal+roman
            
        return pyparts  # (family, size, style), all strings


    def fontResize(self, incr=None, actual=None):
        """
        increment or set the current font size and reconfigure
        """
        try:
            family, size, style = self.currentFont()
            resize = int(size) + incr if incr else actual
            self.text.config(font=(family, resize, style))
        except:
            my_showerror(self, 'Font', 'Cannot resize current font')


    def onFontPlus(self):
        """
        Zoom In: increment the current font size and reconfigure
        """
        self.fontResize(+1)


    def onFontMinus(self):
        """
        Zoom Out: decrement the current font size and reconfigure
        """
        self.fontResize(-1)

        
    def onFontList(self):
        """
        pick next font spec in configurable list
        """
        self.text.config(font=self.fonts[0])       # resizes the text area as needed
        self.fonts.append(self.fonts.pop(0))       # [3.0] don't skip [0] initially


    def onColorList(self):
        """
        pick next color pair in configurable list
        """
        self.text.config(fg=self.colors[0]['fg'],
                         bg=self.colors[0]['bg'])
        # [3.0] cursor=fg, else lost in dark bg
        self.text.config(insertbackground=self.colors[0]['fg'])
        self.colors.append(self.colors.pop(0))     # move current front to end


    @modalMenuAction
    def onPickFg(self):
        """
        open platform's color-select dialog to pick arbitrary fg
        """
        self.pickColor('fg')                       # added on 10/02/00


    @modalMenuAction
    def onPickBg(self):
        """
        open platform's color-select dialog to pick arbitrary bg
        """
        self.pickColor('bg')                       # this is too easy?


    def pickColor(self, part):
        """
        set foreground or background color per user input
        [3.0] pass parent to avoid raising root on Windows;
        this does not invoke a slide-down on Mac OS X here;
        """
        names = dict(bg='Background', fg='Foreground')
        partname = names[part]
        prompt = 'PyEdit - Pick %s' % partname     # [3.0] custom prompt

        # platform-specific dialog
        (triple, hexstr) = askcolor(parent=self,   # don't raise Tk root  
                                    title=prompt) 
        dlgRefocus(self)                           # [3.0] else Mac needs click
                
        if hexstr:
            self.text.config(**{part: hexstr})
            # [3.0] cursor=fg, else lost in dark bg
            if part == 'fg':
                self.text.config(insertbackground=hexstr)


    def onPickFont(self):
        """
        2.0: open new non-modal custom dialog to pick arbitrary font for self
        2.1: pass per-dialog inputs to callback, may be > 1 font dialog open
        [3.0] total rewrite to provide help and meaningful prefills
        [3.0] note: there is a new font dialog in Tk 8.6+, but can't assume;
        [3.0] on Mac, set default app menubar for nonmodal dialogs, else erased;
        [3.0] caveat: dialog not updated if zoom in/out, but unclear if should;
        [3.0] hide while build, else flash on Windows (due to currentFont()?);
        """
        from PP4E.Gui.ShellGui.formrows import makeFormRow
        
        popup = Toplevel(self)          # pertains to and closed with self
        popup.withdraw()                # [3.0] hide to avoid flash
        try_set_window_icon(popup)      # [3.0] icons where supported
        popup.title('PyEdit - Font')
        popup.resizable(width=False, height=False)  # [3.0] nonresizable: help

        # [3.0] call guimaker's Mac menubar fixer for nonmodal dialog window
        fixAppleMenuBarChild(popup)

        var1 = makeFormRow(popup, label='Family', browse=False, width=18)
        var2 = makeFormRow(popup, label='Size',   browse=False, width=18)
        var3 = makeFormRow(popup, label='Styles', browse=False, width=18)
        
        # [3.0] prefill with current font: see also preset pick-list's examples
        family, size, style = self.currentFont()
        var1.set(family)
        var2.set(size)
        var3.set(style)

        def onFontApply():
            # vars in per-call/dialog enclosing scope, not per-editor self
            self.onDoFont(popup, var1.get(), var2.get(), var3.get())
                          
        btnfrm = Frame(popup)
        btnfrm.pack(side=TOP)
        abtn = Button(btnfrm, text='Apply', command=onFontApply)
        abtn.pack(side=LEFT)
        popup.bind('<Return>', lambda event: onFontApply())   # [3.0] Enter=Apply

        # [3.0] add usage help hints pulldown (dialog-specific: not a popup)
        helptext = [
        'This dialog sets the font of the text displayed by the window that opened it.',
        'Its input fields are prefilled with the font parameters currently being used.',
        'Enter Family, optional Size, and a space-separated list of zero or more Styles:',
        '',
        '%s Family' % dialogHelpBullet,
        '    Use courier, times, helvetica, arial, consolas, calibri, inconsolata, menlo,...',
        '    Some family names may render differently or map to a default on some platforms.',
        '    Courier, helvetica, and times are guaranteed to be present on every platform.',
        '    For fixed-width text like program code, try menlo or monaco on Macs, consolas',
        '    on Windows, inconsolata on Linux, or courier on all three.  A font.families()',
        '    in a running Python/tkinter program lists all available font families.', 
        '',
        '%s Size' % dialogHelpBullet,
        '    Use 9, 12, 18, 20, 0, -30,...',
        '    Where N=points, -N=pixels, 0=platform default, and empty=0.',
        '',
        '%s Styles' % dialogHelpBullet,
        '    Use any of (bold or normal), (italic or roman), underline, or overstrike.',
        '    Default values are normal (i.e., nonbold) and roman (i.e., nonitalic).',
        '',
        'Example inputs (do not input quotes added here for clarity only):',
        '',
        '    ["arial, "9", ""]',
        '    ["courier", "12", "bold"]',
        '    ["monaco", "12", "normal"]',
        '    ["times", "0", "normal italic"]',
        '    ["courier new", "-20", "bold roman underline"]',
        '',
        "Click Apply to apply the font parameters you have entered to the edit window text.",
        'The Enter key also applies the font, and Escape opens or closes this help.  This',
        'dialog stays open on screen to allow you to experiment with alternative settings.',
        '',
        "Save fonts in your program's config files to use them as presets in later runs.",
        "See also the View menu's Font List to cycle through your preset fonts on request,",
        "and its Zoom In/Out to increment and decrement the current font's size quickly.",
        "To set the Run Code output window's font, see its textConfig.py setting."
        ]
        self.addDialogHelp(popup, btnfrm, helptext)   # see grep, Escape=Help
        popup.deiconify()                             # [3.0] unhide flash-free


    def onDoFont(self, popup, family, size, style):
        """
        on Apply in nonmodal font input dialog: configure text;
        self is the same edit window here, for open pick-font dialogs;
        size seems the only required part (style default=normal+roman);
        """
        if size == '':
            size = '0'   # use default size if omitted [3.0]
        try:  
            self.text.config(font=(family, int(size), style))
        except:
            my_showerror(self, 'Font', 'Bad font specification')
            popup.focus_force()   # [3.0] raise, refocus on Mac


    def onLineWrap(self):
        """
        [3.0] toggle line wrapping in the edit window's text on or off;
        it's off by default with a horizontal scroll bar; when toggled
        on here, use character boundaries only - 'word' boundaries seem
        too much formatting; Run Code's output window similarly toggles,
        but must set up an Escape binding manually (it has no menu);

        UPDATE: this is now a 3-state toggle, that cycles through none,
        char-wrapping, and word-wrapping.  Word wrapping seems prone to
        errors (your file may be one massive line!), but also may be
        useful when viewing unstructured prose with very long lines.
        Run Code still does just off and char: it is structured text.
        """
        wrapmodes = ['none', 'char', 'word']          # Tk's options
        self.textwrapped += 1                         # starts at 0=none
        nextmode = wrapmodes[self.textwrapped % 3]    # remainder of div
        self.text.config(wrap=nextmode)               # none->char->word




    ############################################################################
    # Tools menu commands
    ############################################################################


    @modalMenuAction
    def onInfo(self):
        """
        pop-up dialog giving text statistics and cursor location;
        caveat (2.1): Tk insert position column counts a tab as one 
        character: translate to next multiple of 8 to match visual?
        note: 3.X len(text) is chars (Unicode codepoints), not bytes;
        [3.0] new format; add font, color, modified, Unicode encoding;
        """ 
        text  = self.getAllText()                  # added on 5/3/00 in 15 mins
        chars = len(text)                          # words uses a simple guess:
        lines = len(text.split('\n'))              # any separated by whitespace
        words = len(text.split())                  # 3.x: bytes is really chars:

        chars = format(chars, ',d')                # str is unicode code points
        lines = format(lines, ',d')                # [3.0]: comma-separate Ks
        words = format(words, ',d')
        
        index = self.text.index(INSERT)            # Tk insert location: 'line.col'
        line, col = index.split('.')               # ('line', 'col')
        line, col = (int(x) for x in (line, col))  # (line, col), Tk col 0 => 1
        col += 1                 
        where = tuple(format(x, ',d') for x in (line, col))
        
        font   = self.currentFont()                 # [3.0]: font, also onPickFont
        colors = self.text.cget('bg'), self.text.cget('fg')

        my_showinfo(self, 'Information',
                 '—Current Location—\n' +
                 'line:  \t%s\ncolumn:\t%s\n\n' % where +
                 '—Text Statistics—\n' +
                 'lines:\t%s\nchars:\t%s\nwords:\t%s\n\n' % (lines, chars, words) +
                 '—Unsaved Changes—\n' +
                 '%s\n\n' % bool(self.isModified()) +
                 '—File Encoding—\n' +
                 '%s\n\n' % self.knownEncoding +
                 '—Display Font—\n' +
                 '%s, %s, %s\n\n' % tuple(font) + 
                 '—Display Color—\n' +
                 'bg: %s, fg: %s' % colors)


    def onPopup(self):
        """
        [3.0] added to allow main Tk windows(s) to create transitory
        Toplevel windows that can be closed individually without closing
        other windows, and are not closed with the spawning self window;
        else Clone for a main Tk can make only other Tk windows that all
        close whenever any one of them is closed; in sum:

        -File->New opens a new file in the same window
        -Tools->Clone makes a new window of same type as opener (Tk or Toplevel)
        -Tools->Popup (new) makes a new transient (Toplevel) window

        naturally, users can also simply click their PyEdit shortcut or alias
        again, which creates a truly-independent window, session, and process;
        caveat: Popup is the same as Clone for Toplevel popup windows;
        """
        TextEditorMainPopup(winTitle='Popup')     # parent=None=Tk root (not self)


    def onClone(self, makewindow=True):                  
        """
        open a new edit window without changing one already open (onNew);
        inherits quit and other behavior of the window that it clones;
        2.1: subclass must redefine/replace this if makes its own popup, 
        else this creates a bogus extra window here which will be empty;
        e.g., TextEditorMainPopup redefines to pass makewindow=False, but
        main windows make a new Toplevel with parent=implicit Tk app root;
        either way, child of default Tk not self, so not closed with self;
        """
        if not makewindow:
             new = None                 # assume class makes its own window
        else:
             new = Toplevel()           # a new edit window in same process
        myclass = self.__class__        # instance's (lowest) class object
        myclass(new)                    # attach/run instance of my class


    def onRunCode(self):
        """
        -------------------------------------------------------------------------
        [3.0]: Open new non-modal custom dialog to run code text in window self.
        This replaces the former multiple-popup interface, and adds a new option
        for capturing the code's standard streams in the PyEdit GUI interface,
        by spawning a thread to poll for the code's output and post on receipt,
        and allowing the GUI user to enter input to be sent to code on request.

        The new Capture mode uses Python's subprocess to tap into the code's
        streams (multiprocessing, used for grep, is for passing data instead).
        This and other custom dialogs have no Cancel: simply close the window.
        See the dialog's help text below for more on this command's utility.
        -------------------------------------------------------------------------
        """
        popup = Toplevel(self)            # pertains to and closed with self
        try_set_window_icon(popup)        # icons where supported
        popup.title('PyEdit - Run Code')
       #popup.resizable(width=False, height=False)  # need resizes for cmd args
        fixAppleMenuBarChild(popup)       # Mac menubar fixer for dialogs

        argsfrm = Frame(popup)
        argsfrm.pack(side=TOP, fill=X)
        Label(argsfrm, text='Command-line arguments?', relief=RIDGE).pack(side=LEFT)
        cmdargs = Entry(argsfrm, width=30)
        cmdargs.pack(side=RIGHT, expand=YES, fill=X)

        radiofrm = Frame(popup, relief=GROOVE, border=3)
        radiofrm.pack(fill=X, padx=5, pady=5)
        Label(radiofrm, text='Run Mode:').pack(side=TOP, anchor=W)

        # sans propr String: in-process is too dangerous
        # Keep is special only on Windows: popup info if used elsewhere
        # Console requires Python config for Windows/Linux frozen exec (on Py!)
        modevar = StringVar()
        modes = ['Console ⚕', 'Click', 'Click+Keep', 'Capture ⚕']     
        for mode in modes:
            Radiobutton(radiofrm,
                        text=mode,
                        variable=modevar,
                        value=mode, pady=3).pack(side=TOP, anchor=NW)
        modevar.set(modes[-1])

        def onRun():
            self.onDoRunCode(popup, cmdargs.get(), modevar.get())                          

        btnfrm = Frame(popup)
        btnfrm.pack(side=TOP)
        Button(btnfrm, text=' Run ', command=onRun).pack(side=LEFT)
        popup.bind('<Return>', lambda event: onRun())   # Enter=Run

        # [3.0] add usage help hints pulldown (dialog-specific: not a popup)
        helptext = [
        "This dialog launches Python (or other) code.  It assumes that the text in the",
        "window you open it from is either a Python program or other launchable content,",
        "and runs the code with optional command-line arguments in a selected run mode.",
        "",
        "Run Code turns PyEdit into an edit+run development tool.  It is not a full IDE,",
        "but can be used to test and run programs and other content you code in PyEdit,",
        "without resorting to shell command lines or other external tools.",
        "",
        "USAGE",
        "",
        "This dialog window stays open to allow you to run edited code multiple times.",
        "Select a run mode from its list; Capture mode is generally recommended for most",
        "Python code.  All run modes run your code from its file, and prompt you when a",
        "Save is required for new files or changes.",
        "",
        "Enter command-line arguments, if used by the code, at the top of this window,",
        "and click Run (or press Enter) to launch the code in the associated edit window.",
        "Run Code supports shell syntax for arguments, and quotes or escapes the names of",
        "your file and the Python executable (if used) as required for the host platform.",
        "Depending on the run mode used, any console IO interaction will occur in either",
        "a system console window or PyEdit's own GUI, per the run-mode details below.",
        "",
        "RUN MODES",
        "",
        "All run modes start the code's file in a new process so PyEdit is not paused or",
        "shut down early.  They differ in their assumptions about the code's type, and",
        "in their handling of the code's console IO streams:",
        "",
        "%s Console (Python)" % dialogHelpBullet,
        "",
        "    On all platforms, this mode assumes the window's text is Python code, and",
        "    routes its console IO (if any) to the console window used to start PyEdit",
        "    (if any).  It runs the code with either the Python running PyEdit, or one",
        "    you've installed locally and set in your textConfig.py configurations file.",
        "    Because this mode pops up no additional windows, it may work well for GUIs.",
        "",
        "    Limitations: although this mode can be used to start many types of programs,",
        "    it does not work well for code that uses console IO streams when no console",
        "    exists (e.g., print() and input() go nowhere when PyEdit is launched by icon",
        "    click).  This mode is also unavailable when PyEdit is a frozen Windows or",
        "    Linux executable, unless your textConfig.py sets an installed Python's path.",
        "    Import-path settings in your textConfig.py are ignored; use PYTHONPATH where",
        "    available (e.g., when PyEdit is launched from a console on Mac OS X), or use",
        "    Capture mode below for more control over streams and paths.",
        "",
        "%s Click (any code)" % dialogHelpBullet,
        "",
        "    On all platforms, this mode assumes the window's text is Python code or any",
        "    other launchable content, and runs the code's file as though its icon was",
        "    clicked in the platform's file-explorer GUI.  This mode can be used for both",
        "    Python programs and non-Python code being edited (e.g., HTML files may open",
        "    in a web browser).  For Python code, it uses whatever Python you associate",
        "    with the file or its type, and on Windows may open console windows to serve",
        "    as the code's standard streams.",
        "",        
        "    Limitations: this mode is platform-specific.  Because it does not connect to",
        "    the code's IO streams explicitly, it can fail for code that uses them on",
        "    some platforms.  This mode will also fail if no program has been associated",
        "    to open the code's file on your computer; for Python code this must normally",
        "    be a Python which you have installed locally.  Unlike Console and Capture,",
        "    this mode also cannot pass command-line arguments to Python code scripts on",
        "    some platforms (e.g., Mac), though no-argument scripts work more portably.",
        "    This mode ignores Python and import-path settings in your textConfig.py;",
        "    set your associations to change your Python, and set PYTHONPATH where used.",
        "",
        "%s Click+Keep (any code, Windows only)" % dialogHelpBullet,
        "",
        "    On Windows, this mode is the same as Click, but opens a new Command Prompt",
        "    window for the code's console IO, which remains open after the code exits so",
        "    no closing input() call is required in Python code.  On Unix (Mac, Linux),",
        "    this mode is not available; use one of the other modes to launch your code.",
        "",
        "%s Capture (☚ recommended, Python)" % dialogHelpBullet,
        "",
        "    On all platforms, this mode assumes the window's text is Python code, and",
        "    connects the code's console IO to PyEdit's GUI.  The code's standard output",
        "    (e.g., print()) plus any standard error (e.g., exceptions) are scrolled by",
        "    PyEdit in a per-run window.  Standard input (e.g., for input()) is provided",
        "    for the code as needed: type an input line at the top of the run's window",
        "    and press Enter or Send.  This mode works for all code on all platforms; it",
        "    is ideal when PyEdit is started without a console window (e.g., by a click)",
        "    and is recommended unless no console IO is used or a console is present.",
        "",
        "    Normal spawned-program exit disables the input line at the top of the run's",
        "    window, and closing the run's window forcibly kills the spawned program if",
        "    it is still running.  Kills allow you to shutdown programs that are looping",
        "    or no longer pertinent, and avoid programs becoming hung waiting for input.",
        "    Capture mode also kills any still-running spawned programs when PyEdit itself",
        "    is closed, to avoid pipe errors; launch longer-lived programs in other ways.",
        "",
        "    Limitations: none, though this mode may require configurations when PyEdit",
        "    is a frozen app or executable.  It runs code with either a Python given in",
        "    your textConfig.py, or else the Python used to run PyEdit.  It also uses the",
        "    module import-path settings in your textConfig.py to allow locally-installed",
        "    libraries to be used when PyEdit is a frozen product; if no such setting is",
        "    given in this context, imports might be limited to Python's standard library",
        "    modules.  This mode may also scroll output slower than a console on some",
        "    platforms; its output window may be extraneous but harmless for GUIs; and",
        "    it supports but does not hide passwords input via Python's getpass module.",  
        "",
        "    Tips: in the run's output window, use Ctrl/Command+C to copy selected text;",
        "    Ctrl/Command+A or Click/Shift+Click to select all text (e.g., to paste into",
        "    a full PyEdit Popup window); and the Escape (Esc) key to toggle output-text",
        "    line-wrapping on and off.  See README.txt for more package-related notes.",
        "",
        "CONFIGURATION",
        "",
        "Both Console and Capture modes allow you to configure the Python used to run",
        "your code, by setting its path in your textConfig.py file.  The Python 3.X (and",
        "its standard library) that is running PyEdit is used by default, but any other",
        "separately-installed Python may be used — including a Python 2.X.  Click modes",
        "instead use your computer's file/type associations to choose a Python.",
        "",
        "Capture mode also allows you to extend the module-import path to include your",
        "local code or installs folders, though this is not required to use modules in",
        "either your main script's folder or Python's standard library, even for PyEdit",
        "apps and executables.  For more details, see the documentation in textConfig.py.",
        "",
        "EXAMPLES",
        "",
        "For precoded examples you can try in Run Code, see the files and README.txt in",
        "PyEdit's install folder docetc/examples/RunCode-examples."
        ]
        self.addDialogHelp(popup, btnfrm, helptext)   # see grep, Escape=Help
        

        
    def onDoRunCode(self, popup, cmdargs, runmode):
        """
        -------------------------------------------------------------------------
        [3.0] On Run in RunCode dialog: launch this window's text as code.  
        Run as clicked program, spawned process with or without console, 
        or spawned process with standard streams (console IO) capture.
        
        The latter--Capture mode--is preferred.  It uses a reader thread with
        an after() timer output-polling loop to avoid blocking the GUI, and 
        each run gets its own popup whose close will kill the code if running.
        This isn't the sole mode, because scrolling is slow on Macs in the Tk
        used for development, and Click mode has valid use cases (e.g., HTML).  
        See the the onRunCode() GUI builder above for additional details.

        Subtlety: the PyEdit launcher script "Launch_PyEdit.pyw" shipped
        with PyMailGUI uses a wait() call to stay open until PyEdit exits.
        This is required to keep PyEdit's streams usable for any code PyEdit
        runs here.  Else, the code's grandparent (launcher) stdin stream
        reports EOFError (or OSError) immediately in terminals on Unix, for
        code using input in modes String, Streamless, and Console.  This is
        not an issue for Capture mode which works without wait() too (yet
        another reason to prefer it), or when textEditor.py is run directly,
        though closing PyMailGUI's launcher can trigger the issue too (rare!). 

        Update: the original string mode ("String" in this version) has been
        withdrawn from the GUI.  It leads to issues when the GUI is unblocked
        while code runs, and can cause PyEdit to be closed without save prompts
        if the code spawned is either a GUI that quits or any code that exits.  
        Generally, spawned code must be run in a separate process to insulate 
        PyEdit from the code's errors and exits; the three remaining Run Code
        modes do so, at the minor expense of requiring code to be saved in files.
        Most of String mode's original code was moved to a doc file: see ahead.
        A prior Streamless mode has also been cut; use Console on Windows.

        -------------------------------------------------------------------------
        About the input() replacements:

        [See also above: String mode has now been withdrawn.  Capture modes uses
        a proxy script; it was originally designed to replace the built-in input()
        with a version that flushes its prompt as described here, but has since
        grown to perform additional tasks; see notes ahead at Capture mode's code.]

        1) String mode requires an input() replacement, because the builtin
        version releases control to the GUI while waiting for input.  This 
        has to do with Python's input hook function (PyOS_InputHook), which
        oddly is coded to trigger Tk's event loop too when tkinter is used.
        The net effect is that Tk Guis are normally blocked for paused or 
        long-running actions--but NOT for an input() that is waiting for text.
      
        This isn't a concern for sys.stdin.realine() (which is blocking) or 
        other run modes (which run in separate processes).  It matters for 
        String mode, because the CWD is reset while the target code runs.
        This can make auto-save misroute CWD-based save files if its after() 
        events can fire during a paused input(), and can break Help's image
        and HTML paths if its button remains active.  To fix, we could either
        save directories at start-up instead of fetching as needed, or replace
        the built-in input() with one that is blocking; the latter was used.

        Note that this is not an issue for sys.stdin.readline() calls in code
        run by String mode: the GUI is blocked until input is entered in the 
        console--as normal.  Also note that all other Run Code run modes are 
        immune to this issue, because they run code in a separate process (and
        are probably preferred for that reason; String mode is a legacy tool).

        2) Capture mode also defines a custom input() replacement, via code in 
        file subprocproxy.py.  This replacement is not to force blocking, but 
        is required to force input() to flush its prompt with a newline before 
        reading; else prompts would appear _after_ user input is required.

        -------------------------------------------------------------------------
        About the (*now withdrawn*) String mode:
        
        1) On further testing, input() redefinition does _not suffice to keep 
        the GUI blocked in all cases.  This is true even if the custom version
        is injected into the builtin scope.  The source of the GUI event-loop
        restart may be any, but GUI code that runs a nested mainloop() call 
        suffices to wreak havoc.  Hence, String mode is prone to odd behavior 
        when it should wait for the run code to exit but does not.  This 
        merits a punt for now; other modes are recommended.

        2) String mode code also uses PyEdit's GUI event loop and root widget.
        Building more widgets may add to PyEdit's root, and a widgets.quit()
        may shut down PyEdit (without a prompt for unsaved changes!).  Don't
        do this.  String mode, if used at all, should be for non-GUI programs.
        [String mode was later withdrawn for this reason: it's too dangerous.]
        
        -------------------------------------------------------------------------
        Console mode alternatives

        In Console mode, explored starting new console/terminal windows in this
        mode on _all_ platforms, and _never_ if all 3 standard streams are TTYs
        (if their .isatty() is True).  It seems overkill to open a new console
        window on Windows with Start if one is already present, and the code's
        streams are inoperative on Unix in this mode when no terminal exists.

        This was abandoned, because it makes for behavior that seems uneven
        (a new console might appear or not, depending on how PyEdit was run),
        and there seems no usable way to open a new terminal on Unix to run a
        Python script with command-line arguments, leaving this per-platform.
        "open -a Terminal stuff.py" is almost there on Mac, but script cmd args
        fail; "gnome-terminal" may work on some Linux, but may not work on all.
        Capture mode works the same and everywhere => it's the recommended mode.

        Console mode could also fallback on using Capture-like Popen calls but
        not catpuring streams, but this was deemed moot: use Capture mode if
        there is no Python executable present or configured.

        -------------------------------------------------------------------------
        Frozen app and executable notes
        
        Frozen apps/executables throw a monkey-wrench into the RunCode design,
        because they ship with a fixed set of frozen library models (for both
        Mac apps and Windows/Linux exes), and may ship with no Python executable
        at all (for Windows/Linux exes).  Moreover, one of the features of
        frozen programs the that they never require a separate Python install.
        Requiring a Python install may be reasonable for running code, but it's
        a bit much for casual users.  How to run arbitrary user Python code?

        This was resolved by forced-inclusion of all (or most?) standard libs
        in the freezes for basic use, and allowing the textConfig.py file to 
        specify both a Python executable when one is preferred or required, and
        import-path settings to pick up different or locally-installed items.

        For exes on Windows and Linux, the Capture mode's proxy script also
        must be frozen, because there may be no standalone Python executable.
        In this case only, a Python executable _must_ be configured for modes
        that require one for running user code -- namely, Console mode only.
        For capture mode, _both_ the .py and frozen versions of the proxy are
        shipped: the former is used when textConfig.py names an installed
        Python, and the (more limited) frozen proxy is used otherwise.

        -------------------------------------------------------------------------
        Killing spawned scripts: 

        As a new feature, Capture now forcibly kills spawned programs when 
        their run window is closed by the user so the programs don't live on
        indefinitely.  This is important when the program is waiting on input
        from PyEdit, but is especially useful for code stuck in an infinite loop.
        It's also platform-specific and complex.  This is especially so when 
        using subprocess's shell=True (a kill may kill the shell parent, not its 
        proxy-command child), but this setting is required for other reasons here 
        (e.g., allowing arbitrary command-line args without parsing).

        On Mac:
           Popen's kill() does the trick, without manually-formed process groups.

        On Windows:
           Kills require running a "taskkill /f /t" command to force-kill the
           shell process by its pid, and all processes it started (including the
           proxy).  Setting shell=False with a cmd string sufficed in some 
           contexts but not all (e.g., frozen Windows executables), and the Popen
           CREATE_NEW_PROCESS_GROUP is not required to make this work.

           taskkill causes momentary console popups in frozen Windows PyEdits only,
           unless this command is run with subprocess.Popen() and shell=True as
           done here.  This forces use of STARTF_USESHOWWINDOW and SW_HIDE; passing
           Popen creationflags=CREATE_NO_WINDOWS (0x08000000) may work too (untried).
           os.system() did popups; os.popen() broke kills; os.spawnv() was untried.
           
           Windows process groups may be a cleaner solution for kills (and are
           used for Linux), but did not work at all despite multiple tries for the
           use case here - a stack that may include python, subprocess, cmd.exe,
           and Windows APIs, and can go bad anyhere along the way.

        On Linux:
           Kills require special code to create a process group at launch and 
           kill the entire group on window close, else only the shell is killed,
           not the proxy child it launches.  Using an "exec " cmd prefix to 
           replace the shell with its child also works, but only for source-code
           proxies (not frozen).  Neither of these are required on Mac, for 
           reasons that remain a suggested exercise (automatic groups?)
              
        A portable and alternative (but unverified) fix requires the 3rd-party
        psutil package to walk and kill child processes, and was not used here.
        Windows and Linux frozen PyInstaller proxies additionally must arrange
        for pruning of their temporary folders on non-normal exit; see ahead.
 
        In the end, Python's subprocess module is really two very-different
        and platform-specific interfaces.  While it helps with stream captures,
        it also adds an extra layer of wrapper code which may obscure platform
        interfaces too much, and is hardly a replacement for all prior art. 

        UPDATE: still-running spawned programs also have to be killed when 
        PyEdit closes, or they die horrible SIGPIPE deaths; see onCloseWindow.

        -------------------------------------------------------------------------
        Prior version comments follow (most are still relevant):
        
        run Python code being edited--not an IDE, but handy;
        tries to run in file's dir, not cwd (may be PP4E root);
        inputs and adds command-line arguments for script files;

        code's stdin/out/err = editor's start window, if any:
        run with a console window to see code's print outputs;
        but parallelmode uses Start to open a DOS box for I/O;
        module search path will include '.' dir where started;
        in non-file mode, code's Tk root may be PyEdit's window;
        subprocess or multiprocessing modules may work here too;

        2.1: fixed to use base file name after chdir, not path;
        2.1: use StartArgs to allow args in file mode on Windows;
        2.1: run an update() after 1st dialog else 2nd dialog 
        sometimes does not appear in rare cases (at this writing);

        [3.0] notes: launchmodes adds sys.executable py to cmdline
        in filemode launches; its objects' args are label+cmdline;        
        verified on Mac OS X - run from Terminal to see prints;
        -------------------------------------------------------------------------
        """


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # onDoRunCode() starts here (on a "Run" in Run Code popup)
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        
        import _thread, queue, subprocess, traceback, shlex, shutil
        from PP4E.launchmodes import Spawn, StartAny, Fork
        from PP4E.launchmodes import quoteCmdlineItem
        from tkinter.scrolledtext import ScrolledText


        if runmode == 'String':                             # run text string
            #-----------------------------------------------------------------
            # DEFUNCT: String mode has been withdrawn - stub example only.
            # in-process: locks PyEdit, IO=PyEdit console, GUI root=PyEdit's;
            #
            # redefines built-in input() for the code run, because builtin 
            # version reactivates Tk event loop (it is not truly blocking):
            # this can misroute auto-saves and break Help icon and html file;
            #
            # see above for other issues: GUI code's mainloop() can also 
            # unblock GUI, and a double quit can close PyEdit silently (!); 
            #-----------------------------------------------------------------
            
            # moved to: doecetc/examples/Assorted-demos/trimmed-string-mode-code.py
            assert False, 'too dangerous: GUI may unblock, code may exit!'



        # -------------------------------------------------------------------
        # try parallel modes: these require a file, but do not block PyEdit
        # 
        # QUOTE (or escape) python-exe and edited-file paths for use in
        # command lines; shlex does not work on Windows, but for string-based
        # cmdlines its split() isn't needed and its 3.3+ quote() applies to
        # non-inputs here only; on Windows, quote python and file (naively)
        # to allow for spaces and specials, but not embedded quotes (if these
        # are legal at all); some modes do not need to quote python (Click
        # doesn't use it, Console doesn't add it to cmd), but must still
        # quote filename to allow nested spaces and specials;  UPDATE: all
        # quote code moved to PP4E.launchmodes.quoteCmdlineItem() for reuse;
        # -------------------------------------------------------------------

        # edited file: now always an absolute+normalized pathname
        thefile = self.getFileName()

        # is file usable?
        if thefile == None or not os.path.exists(thefile):
            my_showinfo(self, 'Run Code', 'File missing: you must Save before Run')
            return
        
        if self.text_edit_modified():                 # 2.0: changed test
            # [3.0] error -> info
            my_showinfo(self, 'Run Code', 'Text changed: you must Save before Run')
            return

        # user's preferred Python: overrides PyEdit's Python if set+valid
        userpython = Configs.get('RunCode_PYTHONEXECUTABLE', None)
        if userpython and not os.path.isfile(userpython):
            userpython = None

        # a python, when present/needed
        #
        # ANDROID - sys.executable is empty in Pydroid 3: Popen fails if not set here
        #
        # ANDROID [Apr1919]: Pydroid 3's 3.0 release moved its Python from the
        # first of the following paths to the second, breaking this workaround:
        #    /data/user/0/ru.iiec.pydroid3/files/arm-linux-androideabi/bin/python
        #    /data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/bin/python
        # to allow for both paths--and be platform agnostic in general--read the
        # result of a 'which python' shell command instead of using literal strs;
        #
        # note: this sets the py exe path globally and intentionally: this fixes
        # the Pydroid 3 bug for spawnees that spawn commands or scripts too;
        #
        sys.executable = os.popen('which python').read().rstrip()  # path to Python exe      
        pickpython = userpython or sys.executable     # user's version or mine/me

        # quote for shell commands per notes above
        quotethefile = quoteCmdlineItem(thefile)      # quote for cmd as needed 
        quotepython  = quoteCmdlineItem(pickpython)   # enclosing spaces+specials

        # no python for source code: must use fozen proxy exe?
        noPythonExe = (                     
            hasattr(sys, 'frozen')     and     # frozen exe PyEdit package?
            sys.frozen != 'macosx_app' and     # not Mac app (has a python)? 
            userpython == None)                # and no user python config?



        if runmode == 'Console ⚕':
            #-----------------------------------------------------------------
            # parallel: IO to Pyedit console (if any) on both Windows+Unix;
            # works if Pyedit run from cmdline, or no IO used (e.g., GUI);
            # chdir() may not be required on all platforms: just in case;
            #
            # NOT AVAILABLE ON WINDOWS OR LINUX FOR FROZEN EXECUTABLES,
            # unless user has set a Python install path in textConfig.py:
            # there may be no python exe, and target cannot be frozen here;
            # could mimic Capture mode and just not connect streams to the 
            # GUI, but that's too much effort for a less-convenient mode;
            #
            # a former "Steamless" mode that used os.P_DETACH was deleted
            # here, because it was redundant with Console mode on Windows;
            #-----------------------------------------------------------------

            # or remove from options list (tbd)
            if noPythonExe:
                my_showinfo(popup, 'Run Code',
                    'Sorry — Console mode is not available in frozen PyEdits '
                    'on Windows and Linux unless you give an installed Python '
                    'in your textConfig.py file.  Try running your code with '
                    'one of the other listed modes.')
                return

            mycwd = os.getcwd()                             # cwd may be root
            dirname, filename = os.path.split(thefile)  
            os.chdir(dirname or mycwd)                      # cd for filenames

            label  = '[PyEdit: Run Code]'                   # separate output
            thecmd = quotethefile + ' ' + cmdargs           # 2.1: not theFile
            # now uses subrocess to avoid cmdline splits
            try:                                            # 2.1: support args
                Spawn(label,                                # run in parallel
                      thecmd,                               # user's py or mine
                      python=pickpython)()
            finally:
                os.chdir(mycwd)                             # go back to my dir



        elif runmode == 'Click':
            #-----------------------------------------------------------------
            # parallel: IO to nowhere explicitly, run as if clicked in a
            # file-explorer on host platform, per file/type association;
            # may fails if no assoc prog, or standard input is required;
            #
            # this opens non-Python files too, and doesn't use an explicit
            # Python executable itself - opens per file/type associations;
            # arguably stretches Run Code paradigm, but handy for html, etc.
            #
            # caveat: Mac's "open" command run here does not pass arguments
            # to a Python script (they go to the PythonLauncher app instead),
            # Click is still useful for other apps and no-arg Python scripts;
            #-----------------------------------------------------------------

            #
            # ANDROID [Apr1219]: do something marginally useful on Android;
            # spawns an "am" activity-manager command line (see onUserGuide),
            # which uses Android default apps that are less general than other
            # platforms' filename associations, but we can't do any better
            # (the 'xdg-open' Linux command used otherwise won't work at all);
            #
            # ANDROID [Apr1919]: webbrowser.open() would spawn the same command
            # to open the URL (via subprocess.Popen) but has no advantage here; 
            #
            # ANDROID [Apr2119]: Pydroid 3 3.0 broke webbrowser AND changed 
            # $BROWSER to skip all "file://" - keep os.system, hardcode cmd;
            # 
            brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
            url = 'file://' + thefile
            cmd = brw % url
            os.system(cmd)    # not os.environ['BROWSER']
            
            # other platforms code...
            """
            mycwd = os.getcwd()                             # cwd may be root
            dirname, filename = os.path.split(thefile)  
            os.chdir(dirname or mycwd)                      # cd for files

            label  = '[PyEdit: Run Code]'                   # separate output
            # quoting and cmdline now handled in StartAny
            try:
                StartAny(label,
                         thefile,
                         cmdargs)()                         # noPy used here
            finally:
                os.chdir(mycwd)                             # go back to my dir
            """



        elif runmode == 'Click+Keep':
            #-----------------------------------------------------------------
            # parallel: IO to new console on Windows, Pyedit console on Unix;
            # on Windows, the new console stays up after the program exits,
            # which spares the user from adding a closing input() call;
            # on Unix, works the same as Console mode if used (see above);
            #
            # NOW AVAILABLE ON WINDOWS ONLY: same as Console mode on Unix,
            # and Unix terminal popup equivalent has proved elusive (above);
            # we could change Console to do Keep on Windows iff all 3 std
            # streams are not .isatty(), but Keep is not needed for GUIs;
            # this mode was formerly called "Popup" (old docs warning...);
            #-----------------------------------------------------------------

            # or remove from options list (tbd)
            if not RunningOnWindows:                        # Mac/Linux: punt
                my_showinfo(popup, 'Run Code',
                    'Sorry — Click+Keep mode is not available outside Windows.  '
                    'Try running your code with one of the other listed modes.')
                return

            mycwd = os.getcwd()                             # cwd may be root
            dirname, filename = os.path.split(thefile)  
            os.chdir(dirname or mycwd)                      # cd for files

            label  = '[PyEdit: Run Code]'                   # separate output
            # quoting and cmdline now handled in StartArgs
            try:
                if RunningOnWindows:                        # 2.1: support args
                    StartAny(label,
                             thefile,
                             cmdargs,
                             keep=True)()                   # noPy used here
                else:
                    # unused: placeholder for mac/linux equivalents tbd
                    thecmd = quotethefile + ' ' + cmdargs   # 2.1: not theFile
                    Fork(label,                          
                         thecmd,
                         python=pickpython)()               # user's py or mine
            finally:
                os.chdir(mycwd)                             # go back to my dir



        elif runmode == 'Capture ⚕': 
            #-----------------------------------------------------------------
            # [3.0] spawn code file as a parallel process and connect to its 
            # streams in PyEdit's GUI; scroll its stdout+stderr output in a
            # per-un window, and send stdin input to it on user request;
            #
            # PREFERRED: works everywhere for all code, console window or not;
            # only downside is an extra output window for GUIs with no output,
            # but this window still displays Python error messages, if any;
            #
            # this uses an output reader thread and polling loop for scrolling
            # output here; for code, it uses a proxy script to force input() 
            # to flush its prompts before reading, encode output to UTF8 and
            # binary form, extend import paths, send PyEdit the process's temp
            # dir in PyInstaller executable mode, and compile and exec() the
            # target code: see subprocproxy.py for the other half of the story;
            #
            # the proxy is run as source-code for source and mac app formats,
            # and always if the user gives a python executable path in configs,
            # but must also be frozen for Windows and Linux exe distributions,
            # because there is no python executable to be found in the exe; 
            # see build-app-exe/windows/build.py for more notes on this case;
            #
            # the proxy app/exe also "bakes in" most (all?) of Python's std
            # lib for use by the code; users can instead config a python exe 
            # (and hence std libs): see include-full-stdlib.py in same folder;
            #
            # tbd: input line is saved for context; clear it on send instead?
            # tbd: font is in textConfig, but change with general text font?  
            # tbd: this pops up a new RunCode window per Run click to retain 
            # prior cmdline args; or keep/lift just one per PyEdit window?
            #
            #-----------------------------------------------------------------
            # USE IN EMBEDDED CONTEXTS
            #
            # INITIAL POLICY: Capture will not be fully functional whenever
            # PyEdit is being used as an embedded component widget by another 
            # program (e.g., PyMailGUI), except for source-code distributions.
            # Instead, we issue a message pointing users to the full PyEdit 
            # download site.  This is largely due to implementation issues (it
            # seems odd to bake all stdlibs into an email client for a coding 
            # tool), but also for security (mixing code and email is a bad
            # idea).  Capture works fully in all _PyEdit_ standalone packages
            # (source, app, exes) as well as source-code form PyMailGUIs, but 
            # has minimal stdlibs/utility in PyMailGUI frozen app and exes.
            #
            # TBD TEMP: we could allow Run Code if the user has configured a 
            # Python exe; this may run into PYTHONPATH/HOME issues in PyMailGUI
            # app, and seems a bit too tricky for a rarely-used feature.
            #
            # FINAL POLICY: we now disable Run Code and issue a popup when 
            # PyEdit is an imported embedded component, in **all** run modes: 
            # source, frozen app, frozen exe.  Although Run Code works in 
            # source-code PyMailGUIs, and has only reduced stdlib support in
            # the Mac app PyMailGUI, running code in other programs like email
            # clients seems largely academic, if not invalid.  The last straw 
            # was the need to kill still-running programs on PyEdit quit: this
            # would add an extra exit task to embedders (along the lines of 
            # current unsaved-changes handling) that's not worth the effort. 
            #-----------------------------------------------------------------

            if __name__ != '__main__':
                # not standalone (main) in source, app, or exe contexts
                my_showinfo(popup, 'Run Code',
                    'Sorry — PyEdit\'s Run-Code Capture mode is not available '
                    'in this program.  To use Capture mode in its complete '
                    'form, get the full standalone PyEdit program at:\n\n'
                    '    http://learning-python.com/pyedit')
                return   # run code not supported here

            """
            delete me soon.....................................................
            # if not source code and not own PyEdit frozen app or exe
            # --or-- source code but part of a frozen Mac app (PyMailGUI);
            # __name__ == '__main__' won't help: ok if embed in source; 
            # sys.executable won't help: may be an app bundle python;

            if (RunningOnMac and 
                not hasattr(sys, 'frozen') and 
                '.app' + os.sep in os.getcwd()):
                runcodewarn_mac()                 # e.g., PyMailGUI Mac app
                # but continue
                
            elif (hasattr(sys, 'frozen') and 
                  not any('pyedit' in arg.lower() for arg in sys.argv[0:2])):
                if RunningOnMac:
                    runcodewarn_mac()             # other Mac app embedders?
                    # but continue
                elif RunningOnWindows or RunningOnLinux:
                    runcodepunt_winlin()          # PyMailGUI Windows/Linux exes
                    return                        # run code not supported here
            ...................................................................
            """


            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # Capture mode utilities (some are enclosing-scope closures)
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


            # forced encoding for all three streams in spawnee
            StreamEncoding = 'UTF8'  


            def streamreader(stream, linequeue, EOF):
                """
                -------------------------------------------------------------
                In a parallel thread - read the subprocess's stdout/stderr 
                stream, and post its lines to a queue for the GUI to fetch 
                and display on timer-event callbacks; this way, the GUI is
                not blocked waiting for the spawned program's output lines.
                The thread exits on subproc stdout stream close (real eof),
                which is assumed to occur on both normal and forced exits.
                Stdout/stderr streams are binary: line reads work anyhow.
                -------------------------------------------------------------
                """
                for line in stream:           # may block this thread (only)
                    linequeue.put(line)       # place on queue for GUI timer loop
                linequeue.put(EOF)            # subproc exit: write sentinel, exit


            def streamconsumer(linequeue, EOF, textdisplay, inputline, inputsend):
                """
                -------------------------------------------------------------
                In the main GUI thread - run a timer-based loop to poll for, 
                fetch, and scroll lines from the shared thread queue until 
                the reader thread sends the EOF-signal sentinel on the queue.

                This timer loop runs only until a single program run finishes.
                it ends when the stream reader sends EOF, or the output window
                is closed; after() silently does nothing on destroyed windows
                (docetc/examples/*/demo-poll-silent-exit-on-window-close.py).

                Processes lines in batches for speed; this helps everywhere,
                but scrolling is still weirdly slow with AS's Mac Tk 8.5!
                Avoiding update() till N lines have been received may help,
                but makes scrolling jerky, and precludes interactive code.                
 
                Batches may also make it appear as if others are paused when
                running multiple programs - the latest's scrolls hog the cpu.
                Stdout/stderr streams are binary: decode + fix eolns for GUI.
                --------------------------------------------------------------
                """
                line = None
                while line != '[EOF]':
                    # process the next batch of posted lines
                    try:
                        queued = linequeue.get(block=False) 
                    except queue.Empty:
                        # nothing posted: go reschedule and wait
                        break

                    if queued is EOF:
                        # subproc exited: end loop, leave text window open
                        inputline.config(state=DISABLED)
                        inputsend.config(state=DISABLED)    # else broken-pipe errors
                        inputline.unbind("<Return>")        # need unbind: has focus       
                        line = '[EOF]'                      # display this line last
                    else:
                        # binary stream line: manually decode and fix eolns
                        try:
                            line = queued.decode(StreamEncoding)
                            line = line.replace('\r', '')   
                        except UnicodeDecodeError:
                            line = '(UNDECODABLE LINE)\n'

                    # process next line: add to PyEdit window, force GUI update
                    try:
                        line = fixTkBMP(line)               # sanitize Unicode for gui
                        textdisplay.config(state=NORMAL)    # allow changes temporarily
                        textdisplay.insert(END, line)       # add to end of text widget
                        textdisplay.see(END+'-2l')          # scroll to new end of text
                        textdisplay.config(state=DISABLED)  # '-2l' = before auto \n at end
                        textdisplay.update()                # run gui events now: else dead

                    except Exception as why:
                        print('Run Code shutdown:', why)    # stdout window was closed?
                        print('This may be normal if your output window was closed early')
                        line = '[EOF]'                      # exit timer loop, retain window?
                    # back to top of batch while loop

                if line == '[EOF]':
                    try:
                        textdisplay.focus_set()   # focus for scrolls, Escape
                    except:
                        pass   # ignore if window was closed: reported above
                else:
                    # reschedule and wait: check queue 10 times per second (msecs)
                    myargs = (linequeue, EOF, textdisplay, inputline, inputsend)
                    textdisplay.after(100, streamconsumer, *myargs)  # no-op if closed


            def onSendinput():
                """
                -------------------------------------------------------------
                Provide stdin in a user-activated field (e.g., on prompts).
                This may seem a bit clumsy, but it's simple and adequate.
                Stdin stream is now binary too: encode to bytes before send.
                -------------------------------------------------------------
                """
                inputtext = inputline.get()                    # yes, it's in scope
                inputtext = inputtext.encode(StreamEncoding)   # to subproc's encoding
                linesep   = os.linesep.encode(StreamEncoding)  # to b'\n' or b'\r\n'
                subproc.stdin.write(inputtext + linesep)       # flush() is required
                subproc.stdin.flush()                          # (in text-mode only?)


            def onCloseWindow():
                """
                -------------------------------------------------------------
                If user closes window while subproc still running, forcibly 
                kill the subproc so we don't leave a hung process waiting for
                input or stuck in a loop.  Allows user to kill the latter.
                A closure: most names here are per-run enclosing-scope state.

                We could just subproc.stdin.close() but that won't stop a
                spawned output-only or no-output program.  subprocess reaps
                zombies on del, but also force the issue here/now.  See above
                for the Windows hack here, the launch code below for more on 
                the Linux process group fix, and subprocproxy.py for more on
                subprocTempdir prune here.  TBD: should this verify kills?

                Now also run for still-open windows on PyEdit quit(), or else
                running spawnees die badly on SIGPIPE errors if they do any
                stream input or output.  No portable fix exists.  <Destroy>
                is not fired when quit(): use a class-global closure list.
                Run Code is disabled if PyEdit embedded: importers ignore.
                -------------------------------------------------------------
                """
                # kill program if still running
                if subproc.poll() == None:               # in scope: this Run
                    # still running
                    try:

                        if RunningOnWindows:
                            # subproc.kill() won't handle all cases here:
                            # run a tree+force taskkill for shell+children;
                            # force /f is required, but skips norm shutdown; 
                            # running the taskkill with os.system() pops up a
                            # console for frozen PyEdits, but Popen(shell=True)
                            # never does; Windows process groups didn't work;
                            #
                            killer = 'taskkill /pid %d /t /f' % subproc.pid
                            subprocess.Popen(killer, shell=True)

                        elif RunningOnLinux:
                            # send kill signal manually to all in the process
                            # group formed when the shell process was started;
                            # see the launch code ahead for more on this fix;
                            #
                            import signal
                            os.killpg(os.getpgid(subproc.pid), signal.SIGTERM)
                        
                        elif RunningOnMac:
                            # simple unix case: kill the proxy cmd, not the shell;
                            # stops proxy now, in any state: looping, paused, etc.
                            #
                            subproc.kill()
                            
                    except Exception as why:
                        print('Process kill exception', why)

                # reap zombies on window close
                if subproc.poll() != None:
                    subproc.wait(timeout=1)

                # prune frozen proxy temp dir if used and lingers
                if (subprocTempdir and                    # in scope: this Run
                    os.path.exists(subprocTempdir)):
                    try:
                        shutil.rmtree(subprocTempdir)
                    except Exception as why:
                        #showinfo('exc', str(why))
                        print('\t\tCannot prune %s [%s]' % (subprocTempdir, why))

                # close run window, whether spawnee exited normally or was killed
                stdoutwindow.destroy()

                # don't test on PyEdit quit: remove this run's function/closure
                TextEditor.openprograms.remove(onCloseWindow)


            def fixPyInstallerTkEnvVars(userpython):
                """
                -------------------------------------------------------------
                When PyEdit (not the subproc proxy) is run as a PyInstaller
                frozen executable on Windows or Linux, its TCL/TK_LIBRARY env
                variables get set by a PyInstaller runtime hook.  Back these
                out here from the environ passed to the subproc when using a
                user-configured Python, else Tcl/Tk will load versions from
                PyEdit's temp folder, not those in the user's chosen Python.
                It's too late to address these once the proxy is launched.
                For a GUI spawnee, these may be set anew by the host Python.
                -------------------------------------------------------------
                """
                if (userpython != None and          # user-configured Python
                    hasattr(sys, 'frozen') and      # a frozen PyEdit running
                    sys.frozen != 'macosx_app'):    # but not a Mac app bindle
                    
                    # always fix so tk is loaded from user's python
                    # but iff a PyInstaller dir: user might set too;
                    # proxy is being run as source, not frozen exe;
                    # example setting value: "...\Temp\_MEI27802\tk";
                    
                    copyenv = os.environ.copy()
                    for key in ('TCL_LIBRARY', 'TK_LIBRARY'):
                        if key in os.environ:
                            if (os.sep + '_MEI') in os.environ[key]:
                                del copyenv[key]
                    return copyenv
                else:
                    # no harm in keeping vars (if set) in any other cases;
                    # proxy may be run as source (including app) or frozen exe
                    return os.environ
                    

            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # Capture mode logic (sets enclosing-scope state used in closures above)
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


            #-------------------------------------------------------------------
            # __BUILD__a new non-modal window for run's console streams.
            #
            # this window displays stdout+stderr output and provides stdin 
            # input; it's per-run and not automatically closed by new runs,
            # though closing it will automatically kill still-running code;
            #-------------------------------------------------------------------
            
            stdoutwindow = Toplevel(self)                   # child of self: closes
            if noPythonExe:                                 # frozen proxy subproc?
                stdoutwindow.withdraw()                     # hide till get line #1
                self.text.update()                          # and unpress Run button
                
            try_set_window_icon(stdoutwindow)               # icons where supported
            stdoutwindow.title('PyEdit - Run Code: Streams')
            fixAppleMenuBarChild(stdoutwindow)              # dialog menubar fixer

            # stdin input line entry
            inputfrm = Frame(stdoutwindow)
            inputfrm.pack(side=TOP, fill=X)
            Label(inputfrm, text='Input Line?', relief=RIDGE).pack(side=LEFT)
            inputline = Entry(inputfrm)
            inputline.pack(side=LEFT, expand=YES, fill=X)
            
            inputsend = Button(inputfrm, text='Send', command=onSendinput)
            inputsend.pack(side=RIGHT, fill=Y)
            inputline.bind('<Return>', lambda event: onSendinput())

            # double-scrolled stdout+stderr display 
            area = Frame(stdoutwindow)                   # or a PyEdit component?
            vbar = Scrollbar(area)
            hbar = Scrollbar(area, orient='horizontal')
            text = Text(area, wrap='none')               # disable line wrapping
            text.config(undo=1, autoseparators=1)        # 2.0, default is 0, 1

            # pack last=clip first (clip sbars last)
            area.pack(expand=YES,  fill=BOTH)
            vbar.pack(side=RIGHT,  fill=Y)
            hbar.pack(side=BOTTOM, fill=X)
            text.pack(side=TOP,    fill=BOTH, expand=YES)

            # cross-link sbars and text
            text.config(yscrollcommand=vbar.set)     # call vbar.set on text move
            text.config(xscrollcommand=hbar.set)
            vbar.config(command=text.yview)          # call text.yview on scroll move
            hbar.config(command=text.xview)          # or hbar['command']=text.xview
            textdisplay = text                       # prior name, used from here on 

            # config style and clicks: select text, wrapping toggle
            textdisplay.config(relief=RIDGE, border=3)
            textdisplay.config(width=100)                   # chars, else dflt=80
            
            textdisplay.config(state=DISABLED)              # read/copy-only text
            textdisplay.bind('<Button-1>', 
                  lambda event: textdisplay.focus_set())    # click to copy on Mac

            textwrapped = False
            def toggleLineWrapping():
                nonlocal textwrapped                        # uses scope (not self)
                if not textwrapped:
                    textdisplay.config(wrap='char')         # no 'word' boundaries
                else:
                    textdisplay.config(wrap='none')         # turn wrapping back off
                textwrapped = not textwrapped
            textdisplay.bind('<Escape>',                    # <KeyPress-w><Button-1>?
                  lambda event: toggleLineWrapping())       # use same as edit window

            # config output font if set                     # default reasonable
            if Configs.get('runcodefont'):
                textdisplay.config(font=Configs['runcodefont'])

            # config output colors if set                   # default b/w suffices
            if Configs.get('runcodebg'):                    # uncolored may be best
                textdisplay.config(bg=Configs['runcodebg'])
            if Configs.get('runcodefg'):
                textdisplay.config(fg=Configs['runcodefg'])


            #-------------------------------------------------------------------
            # __LAUNCH__ the proxy to launch the edited program.
            #
            # pass cmdargs as entered: user must quote/escape as needed;
            # manually quote items we add to str (only seqs auto-quote);
            # proxy (app or exe) has all python standard libs baked in;
            #
            # for output streams, use binary mode + manual decode here,
            # and force prints in the spawnee to encode per UTF8 Unicode;
            # that supports non-ascii text, and avoids read decode errors;
            # also replace any non-BMP characters received for the GUI;
            #-------------------------------------------------------------------
            
            extras = {}
            if noPythonExe:
                # frozen proxy: run frozen exe directly (but not for Mac app);
                # python '-u' not available; no userpython or shipped py exe;
                # PyEdit is not an embedded dir here: proxy will be in '.'
                # with PyEdit exe unless PyEdit run from cmd line elsewhere;
                # stdout+stderr stream should be binary-mode, UTF8 Unicode,
                # and unbuffered, but it's not - see subprocproxy workaround;
                
                proxy  = 'subprocproxy'       # omitting .exe okay on Windows
                mydir  = INSTALLDIR           # not via __file__ if frozen
                proxy  = os.path.join(mydir, proxy)
                proxy  = quoteCmdlineItem(proxy)
                cmdstr = proxy + ' ' + quotethefile + ' ' + cmdargs
                os.environ['PYTHONUNBUFFERED'] = 'True'   # -u equiv (iff env?)
                os.environ['PYTHONIOENCODING'] = StreamEncoding
                extras = dict(env=os.environ)

            else:
                # source proxy: run script's source with python executable;
                # use python set in textConfig, else python running PyEdit;
                # this branch is also used for frozen Mac apps, and when a 
                # Python executable is set in textConfigs.py: use .py source;
                # proxy script file is not in '.' if PyEdit is embedded;
                # stdout+stderr stream is binary-mode, UTF8 Unicode, unbuffered;

                proxy  = 'subprocproxy.py'
                mydir  = INSTALLDIR           # uses dir(__file__) here
                proxy  = os.path.join(mydir, proxy)
                proxy  = quoteCmdlineItem(proxy)
                cmdstr = ' '.join([quotepython, '-u', proxy, quotethefile])
                cmdstr = cmdstr + ' ' + cmdargs
                os.environ['PYTHONIOENCODING'] = StreamEncoding   # Unicode?
                extras = dict(env=fixPyInstallerTkEnvVars(os.environ))

                if RunningOnMac and hasattr(sys, 'frozen') and userpython:

                    # force py2app Mac app bundle to support user-configured
                    # Python executable paths; without this, these 2 env vars
                    # inherit bundle settings, and libs are always those of
                    # the bundle's Python, not the Python set in textConfig.py;
                    # the source-code package doesn't have this issue on Macs;
                    # this saves any user paths, though PYTHONPATH isn't loaded
                    # if PyEdit is started by clicks anyhow (use textConfig.py);

                    def debugpaths(debug=False):
                        if debug:
                            my_showinfo(self, 'Debugging',
                                os.environ.get('PYTHONPATH', 'X') + '\n\n' +
                                os.environ.get('PYTHONHOME', 'X'))

                    debugpaths()
                    if 'PYTHONPATH' in os.environ:
                        alldirs = os.environ['PYTHONPATH'].split(os.pathsep)
                        alldirs = [d for d in alldirs if d != mydir]
                        if not alldirs:
                            del os.environ['PYTHONPATH']   # empty fails
                        else:
                            os.environ['PYTHONPATH'] = os.pathsep.join(alldirs)
                    if 'PYTHONHOME' in os.environ:
                        del os.environ['PYTHONHOME']       # or .pop(key, None)
                    debugpaths()

            # on Linux, launches and kills require special handling here: 
            # frozen proxies need a './' in case '.' is not on PATH, and 
            # must form a process group so that the proxy is killed along
            # with its shell on later window close; without process groups,
            # the later os.kill() kills the shell, not its proxy cmd child;
            # we must use shell=True to finesse cmdline-args parsing issues;
 
            # other ideas: prefixing the cmd with 'exec ' replaces the shell 
            # with its child such that a later subproc.kill() kills the child,
            # but this works only for a source-code proxy, not when it's frozen;
            # Mac doesn't require './' (it runs the proxy as source) or process
            # groups (a subproc.kill() kills the child);  Windows happily runs
            # programs in '.', and uses a taskkill command instead of .kill();
            # Popen(start_new_session=True) runs setsid() auto in python3.2+:
            
            if RunningOnLinux:
                # frozen proxy in frozen pyedit's dir?
                if cmdstr.startswith('subprocproxy '): 
                    cmdstr = './' + cmdstr               # in case '.' not on path

                # create a process group for shell+cmd
                extras.update(preexec_fn=os.setsid)      # so os.kill() kills cmd

            # this needs to: use strings to avoid arg splits on Windows, quote
            # all args it adds to cmd strings (only sequences auto-quote args),
            # use shell=True to avoid spurious cmd prompts for frozen executables
            # on Windows, use shell=True for strings to pass args to the script
            # on Unix, and allow the script to be forcibly killed everywhere;
            # see note "Killing spawned scripts" above for more background;

            # all 3 streams use binary mode now: must encode for stdin too;
            # proxy now does cwd: formerly rundir = os.path.dirname(thefile);
            # neither shell=True nor env=os.environ export login env on Mac;
            # debug: my_showinfo(self, 'xxx', cmdstr)

            subproc = subprocess.Popen(
                  cmdstr,                       # not seq: pass args as given
                  shell=True,                   # avoid popup for win exe, etc.
                  universal_newlines=False,     # binary streams, manual decode/eoln
                  stdout=subprocess.PIPE,       # capture sub's stdout here
                  stdin=subprocess.PIPE,        # provide sub's stdin here
                  stderr=subprocess.STDOUT,     # route sub's stderr to its stdout
                  **extras)                     # any special-case kw args needed

            # read and save the subproc's temp folder name for prune on kill;
            # only when proxy run a frozen PyInstaller exe: not Mac or source;
            # caveat: this can gobble line1 of a non-py error message, which
            # we could force to output or queue, but this should not occur;

            if noPythonExe:
                subprocTempdir = subproc.stdout.readline()    # get line #1
                subprocTempdir = subprocTempdir.decode(StreamEncoding).rstrip()
                stdoutwindow.deiconify()    # show window now (else temp pause) 
            else:
                subprocTempdir = None
            

            #-------------------------------------------------------------------
            # __MONITOR__ the spawnee: read and process code's streams.
            #
            # start reader thread + timer-based poller for subproc's stdout/err;
            # provide stdin text when the user interacts in respose to prompts;
            # kill a still-running subproc on run-window close, or PyEdit quit;
            #-------------------------------------------------------------------
            
            EOF = None                   # stream lines read will never be this
            linequeue = queue.Queue()    # infinite-size shared queue of objects

            stdoutwindow.protocol('WM_DELETE_WINDOW', onCloseWindow)
            TextEditor.openprograms.append(onCloseWindow)

            _thread.start_new_thread(streamreader, (subproc.stdout, linequeue, EOF))
            streamconsumer(linequeue, EOF, textdisplay, inputline, inputsend)

            # back to Tk event loop, with after() timer polling loop started




    ############################################################################
    # Help menu commands (just one for now)
    ############################################################################


    #@modalMenuAction - no more, but my popups are
    def onHelp(self):
        """
        ------------------------------------------------------------------
        display my help text in a simple info dialog;  this could
        popup HTML via py's webbrowser module, but that seems overkill
        for PyEdit's intuitive actions;  caveat: showinfo() formats the
        text better on some platforms than others (Linux seems worst);
        this becomes "About" under "Help" on Mac and Linux because of
        GuiMaker's logic (Help content follows complex rules on Macs);

        [3.0] This now pops up a custom dialog that allows users to pick
        either About--the original showinfo text box, or User Guide--the
        new HTML doc auto-opened in a web browser.  Ideally, these would
        be separate menu entries, but the dialog is the easiest way to
        work with GuiMaker's Help logic unchanged (any more, at least).

        [3.0] Now splits up the original help text into two halves: About
        and Versions.  The combo was too long for an info box on Linux
        (and small screens?), and info boxes can't be adjusted.  Versions
        is still not short, but what would you expect from PP4E's author?

        [3.0] Subtle: the About and Versions info boxes are children of 
        the Help dialog (not self TextEditor) so Help gets active focus 
        on close.  This makes it only partly modal on Mac, but acceptably.
        ------------------------------------------------------------------
        """

        def androidTextDisplay(title, helptext):
            """
            # ANDROID [Apr1219] - work around truncated common-dialog text bug, 
            # by using a word-wrapped scrolled-text widget instead of showinfo;
            # also set font for fit on smaller (~5.5") phones with large defaults; 
            """
            from tkinter.scrolledtext import ScrolledText
            popup = Toplevel()
            popup.title('PyEdit %s - %s' % (Version, title))
            ok = Button(popup, text='OK', command=popup.destroy)
            ok.pack(side=BOTTOM)                      # pack first=clip last
            text = ScrolledText(popup, wrap='word')   # wrap on word boundaries
            text.pack(expand=YES, fill=BOTH)
            text.insert(END, helptext)
            text.config(font='courier 5 normal')      # else some phones default larger
            text.config(width=48, height=24)          # start small for fit: chars, lines
            text.config(state=DISABLED)               # make read-only: avoid os-keyboard

        @modalMenuAction
        def onAbout():
            """
            display text in a modal popup
            original version help, half1 (force popup on Mac, not slide-down)
            """
            # ANDROID [Apr1219] - use custom dialog to avoid truncation
            androidTextDisplay('About', HelpText_About)

            # other platforms legacy code...
            """
            orphan = RunningOnMac
            my_showinfo(popup, 'About', HelpText_About, orphan=orphan)
            """

        @modalMenuAction
        def onVersions():
            """
            display text in a model popup  
            original version help, half2 (force popup on Mac, not slide-down)
            """
            # ANDROID [Apr1219] - use custom dialog to avoid truncation
            androidTextDisplay('Versions', HelpText_Versions)

            # other platforms legacy code...
            """
            orphan = RunningOnMac
            my_showinfo(popup, 'Versions', HelpText_Versions, orphan=orphan)
            """

        def onReadme():
            """
            display text file in an independent PyEdit window
            don't close with help dialog: user may edit in this window,
            and closing with help would silently ignore unsaved changes;
            """
            myreadme = os.path.join(mysourcedir, 'README.txt')
            TextEditorMainPopup(
                    parent=None,               # parent = None = Tk root:
                    loadFirst=myreadme,        # not auto-closed with Help popup 
                    winTitle=None,             # no label: a full edit window
                    loadEncode='UTF-8')        # has Unicode copyright

        def onUserGuide():
            """
            display html file in a web browser
            """
            #
            # ANDROID [Apr1219]: webbrowser fails on Android (for reasons TBD), 
            # so spawn a shell command using the $BROWSER preset in Pydroid 3:
            # "am start --user 0 -a android.intent.action.VIEW -d %s"; Android
            # uses online version to pick up latest changes (others should too);
            #
            # ANDROID [Apr1919]: webbrowser _does_ work, but requires local file
            # URLs to start with "file://" and does not open a web browser for
            # local HTML files (they open in text editors); use the online URL
            # to ensure a web browser, and either os.system or webbrowser.open;
            #
            # ANDROID [Apr2119]: Pydroid 3 3.9 broke webbrowser and changed 
            # $BROWSER - use os.system again, with hardcoded command line; 
            #
            myuserguide = ('https://www.learning-python.com'
                               '/pyedit-products/unzipped/UserGuide.html')
            brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
            cmd = brw % myuserguide
            os.system(cmd)

            # other platforms code...
            """
            import webbrowser
            myuserguide = os.path.join(mysourcedir, 'UserGuide.html')
            if os.path.exists(myuserguide):
                webbrowser.open('file:' + myuserguide)
            else:
                # could fail for same reason as image load below
                my_showinfo(self, 'User Guide',
                            'Sorry - cannot find user guide HTML file')
            """

        # get source dir from __file__, whether embedded or standalone;
        # update: uses __file__ fails for source-code and Mac apps, but
        # sys.argv[0] scheme required for frozen PyInstaller executables;
        mysourcedir = INSTALLDIR

        # split help text into About + Versions: too long on Linux
        chop = HelpText.find('PyEdit Version History')
        HelpText_About, HelpText_Versions = HelpText[:chop].strip(), HelpText[chop:]

        # build a simple non-modal dialog
        popup = Toplevel(self, bg='white')   # close with parent? (tbd)
        try_set_window_icon(popup)           # Windows+Linux icon image
        fixAppleMenuBarChild(popup)          # Mac menubar fixer for dialogs
        popup.title('PyEdit %s - Help' % Version)
        popup.appname = 'PyEdit'             # for callDialog (non-TextEditor)

        dlgfont = 'helvetica'
        tagline = ' PyEdit \u2014 Edit text. Run code. Have fun.'
        # 
        # ANDROID [Apr1219] - smaller font for fit, was 18
        #
        Label(popup, text=tagline, bg='white',
                     font=(dlgfont, 10, 'bold italic'), bd=15).pack()
        
        # display icon image: gif works on all py 3.Xs
        imgpath = os.path.join(mysourcedir, 'icons', 'pyedit-window-main.gif')
        try:
            gifimg = PhotoImage(file=imgpath)
            imglab = Label(popup, image=gifimg, bg='white')
            imglab.pack(expand=NO, side=LEFT)
            popup._save_pyedit_help_img = gifimg      # else erased if no more refs

        except Exception as why:
            # --the following is now moot, because String mode was withdrawn--
            # unlikely, but image load can fail if cwd is reset temporarily when
            # a paused input() [fixed] or GUI-code mainloop() [unfixable] restarts 
            # the GUI during the exec() in Run-Code's String mode (rare but true!)
            print('PyEdit image load failed:', why)   # continue without the image

        # help content/format buttons
        # 
        # ANDROID [Apr1219] - smaller font for fit, was 14
        #
        btnfont = (dlgfont, 8, 'bold')
        Button(popup, text='About',
               font=btnfont, bg='white',
               command=onAbout).pack(padx=10, pady=10)

        Button(popup, text='Versions',
               font=btnfont, bg='white',
               command=onVersions).pack(padx=10, pady=10)

        Button(popup, text='Readme',
               font=btnfont, bg='white',
               command=onReadme).pack(padx=10, pady=10)

        # ANDROID [Apr1219] - most colored buttons also lose their bg on presses,
        # though only the user-guide button does here: use a label+bind instead;
        #
        uglab = Label(popup, text='User Guide',
                      font=btnfont, bg='white',
                      relief=SOLID,
                      width=12, height=2)    # forge button (but a bit larger...)
        uglab.pack(padx=10, pady=10)
        uglab.bind('<Button-1>', lambda event: onUserGuide()) 

        # other platforms code...
        """
        Button(popup, text='User Guide',
               #state=DISABLED,           # ANDROID - webbrowser failed initially
               font=btnfont, bg='white',
               command=onUserGuide).pack(padx=10, pady=10) 
        """

        Button(popup, text='Close Help',
               command=popup.destroy).pack(padx=10, pady=10, side=BOTTOM)




    ############################################################################
    # Utilities, useful outside this class too
    ############################################################################


    # Access text content
    
    def isEmpty(self):
        return not self.getAllText()

    def getAllText(self):
        return self.text.get(START, END+'-1c')    # extract text as str string

    def setAllText(self, text):
        """
        ----------------------------------------------------------------
        Caller: call self.update() first if just packed, else the
        initial position may be at line 2, not line 1 (2.1; Tk bug?).

        [3.0] UPDATE: Yes, this is/was a Tk 8.5 bug, until at least
        late 2015: http://core.tcl.tk/tk/tktview/1739605.  The best 
        workaround is to either not call see() at all and assume that
        the view is at the top, or call Text.see() twice in succession
        as done here (see ../docetc's demo-tk-line1-scroll-bug.py for
        a minimal proof).  Later Tks may also help, but iff installed.
 
        Hence, callers *no longer must call update()* to fix the see()
        line #1 issue for just-packed PyEdit windows.  And they probably
        shouldn't - doing so can cause a visible flash even if windows
        withdraw() and deiconify() to hide during builds, and may even
        trigger an unrelated initial sizing bug in Tk 8.5 that ignores
        config() but is officially outside the scope of this docstring. 
        ----------------------------------------------------------------
        """
        if isinstance(text, str):                 # [3.0] sanitize to display
            text = fixTkBMP(text)                
        self.text.delete(START, END)              # store text string in widget
        self.text.insert(END, text)               # or START; text=bytes or str
        self.text.mark_set(INSERT, START)         # move insert point to top
        self.text.see(INSERT)                     # scroll to top, insert set
        self.text.see(INSERT)                     # no, really: see note above

    def clearAllText(self):
        self.text.delete(START, END)              # clear text in widget



    # Access filename and text's Unicode encoding
    
    def getFileName(self):
        return self.currfile
    
    def setFileName(self, name):                  # see also: onGoto(linenum)
        """
        [3.0] absolutize + normalize file's pathname
        for matches against the open-file list, etc.;
        this also drops odd '/' from GUI on Windows;
        """
        if name != None:                          # abspath() runs normpath()
            name = os.path.abspath(name)          # else mixed slashes on Win
        # for saves, already-open test, run-code
        self.currfile = name
        # [3.0] gui: sanitize Unicode text
        self.filelabel.config(text=fixTkBMP(str(name)))   # may be None

    def setKnownEncoding(self, encoding='utf-8'): # 2.1: for saves if inserted
        self.knownEncoding = encoding             # else saves use config, ask?



    # Change colors and font
    
    def setBg(self, color):
        self.text.config(bg=color)                # to set manually from code

    def setFg(self, color):                       # caveat: not used everywhere
        self.text.config(fg=color)                # 'black', '#RRGGBB' hexstring
        self.text.config(insertbackground=color)  # [3.0] cursor=fg, for dark bg

    def setFont(self, font):
        self.text.config(font=font)               # ('family', size, 'style')



    # Change window size
    
    def setHeight(self, lines):                   # default = 24h x 80w
        self.text.config(height=lines)            # may also be from textConfig.py

    def setWidth(self, chars):
         self.text.config(width=chars)



    # Access Tk's text-modified flag and undo stack
    
    def clearModified(self):
        self.text.edit_modified(0)                # clear modified flag

    def isModified(self):
        return self.text_edit_modified()          # changed since last reset?

    def clearUndoStack(self):
        self.text.edit_reset()                    # discard any changes made
        
    @staticmethod
    def anyWindowsModified():
        """
        [3.0] return list of open windows that have unsaved
        changes; this list is Boolean False if it is empty;
        it spans all PyEdit window types: pop-up or component;
        client programs may use this prior to an app quit,
        and may call it through the class name with no self;
        """
        return [w for w in TextEditor.openwindows if w.text_edit_modified()]



    # Forced scroll to top or bottom

    def seeTop(self):
        """
        [3.0] Tk still has a bug that opens with line 2 at the
        top for set text; only update() fixes this, not seeTop(),
        but update() unfortunately can also cause a brief flash.
        """
        self.text.see(START)           # scroll to line 1, column 0
        self.text.see(START)           # if just packed: see setAllText
       #self.text.yview_moveto(0.0)    # alternative, but not see() fix


    def seeEnd(self):
        self.text.see(END)             # scroll to end of current text
        self.text.see(END)             # if just packed: see setAllText
       #self.text.yview_moveto(1.0)    # alternative, but not see() fix




################################################################################
# Ready-to-use, top-level editor classes
# Each mixes in a GuiMaker Frame subclass which builds menu and toolbars.
#
# These classes are common use cases, but other configurations are possible.
# Call TextEditorMain().mainloop() to start PyEdit as a standalone program.
# Redefine/extend onQuit in a subclass to catch exit or destroy (see PyView).
# Caveat: could use windows.py for icons, but quit protocol is custom here.
################################################################################


"""
#
# Android: ***ADDITIONAL DOCUMENTATION TRIMMED HERE***
# Because Pydroid 3's IDE editor cannot handle source files > roughly 256k 
# bytes (and lets the user's program die without warning!), some additional 
# comments were deleted here.  See this file's original version for text cut,
# and learning-python.com/mergeall-android-scripts/_README.html#toc85.
#

--------------------------------------------------------------------------------

2.1: Quit protocol notes

--------------------------------------------------------------------------------

[3.0] Top-level class updates and notes

--------------------------------------------------------------------------------
"""



#*******************************************************************************
# When text editor owns the window: main
#*******************************************************************************

class TextEditorMain(TextEditor, GuiMakerWindowMenu):
    """
    ----------------------------------------------------------------------------
    Main PyEdit top-level windows that quit() to exit entire app on a Quit
    in GUI, build a menu on a window, and check for changes in all other
    top-level windows on close.  Generally used for PyEdit's main window.
    onQuit is run for Quit in toolbar or File menu, as well as window border X,
    and will also be called from application menu and Dock Quit on Mac OS X.

    Builds on a passed-in parent, which must be a window - a Tk (explicit, or
    default=None) or Toplevel - and probably should be a Tk so the window isn't
    silently destroyed and closed with a transient parent.  All non-popup main
    PyEdit windows check all other PyEdit windows open in the process for changes
    on a Quit in the GUI, since a quit() here will exit the entire app.  Editor
    Frame need not occupy entire window (see PyView), but its Quit ends program.

    Tk roots have no parent themselves - they are parent to widgets built here,
    though a Clone of this window creates a Toplevel to serve as its container.
    UPDATE: Quits also kill any still-running Run-Code spawnees: see onQuit(). 
    ----------------------------------------------------------------------------
    """
    
    def __init__(self, parent=None, loadFirst='', loadEncode=''):
        """
        editor fills entire parent window
        """
        GuiMaker.__init__(self, parent)              # use main window menus
        
        try_set_window_icon(self.master)             # [3.0] set (some) icons
        wintype   = ' ✍' #if RunningOnMac else ''    # [3.0] distinguish (or ✐)
        fulltitle = 'PyEdit %s - Main' + wintype     # use diff icon on Win/Lin
        self.master.title(fulltitle % Version)       # title on parent win
        self.master.iconname('PyEdit')

        # set wm X or red-dot close callback if full window
        self.master.protocol('WM_DELETE_WINDOW', self.onQuit)

        # [3.0] do this _after_ borders: may trigger unicode popup 
        TextEditor.__init__(self, loadFirst, loadEncode) # GuiMaker frame packs self

        # [3.0] +track for change-test and auto-save in __init__ and <Destroy>
        

    @modalMenuAction
    def onQuit(self):
        """
        on Quit requested in GUI: quit app
        quit() ends the entire program regardless of widget type
        there's no need to clear tracking lists here: exiting
        
        [3.0] on Mac this may also be triggered from app-menu
        or Dock when any window may be on top: rewritten to not
        treat self specially when asking about checking changes;

        [3.0] run Run-Code closures to kill any still-running spawnees
        so they don't die badly later on output or input pipe errors;
        for all still-open run windows: a no-op if spawnee not running;
        no need to close programs when embedded: Run Code is disabled;
        caveat: this could warn the user and ask, but it's documented;
        """
        doquit = False

        # check all windows for unsaved changes
        allwins = TextEditor.openwindows
        changed = [w for w in allwins if w.text_edit_modified()]
        if not changed:
            # none changed: close silently
            doquit = True

        else:
            if len(allwins) == 1:
                # just me open: specialize the message
                verify = ("This window's text is changed and unsaved.\n\n"
                          'Quit and discard its changes?')
            else:
                # [3.0] ask about all, new message format
                numchange = len(changed)
                verify = ('%s window%s ha%s unsaved changes.\n\n'
                          'Quit and discard %s changes?')                     
                verify %= ((numchange,) +
                       [('', 's', 'its'), ('s', 've', 'all')][numchange > 1]) 

            if my_askyesno(self, 'Quit', verify):
                # quit without saving (but auto-saves remain)
                doquit = True
            else:
                # [3.0] lift changed windows for convenience
                self.liftWindows(changed)

        if doquit:
            # [3.0] run Run-Code closures to kill any still-running spawnees
            for onCloseWindow in TextEditor.openprograms.copy():
                onCloseWindow()   # runs a closure, changes list in-place

            # and close all PyEdit windows, without triggerring <Destroys>s
            GuiMaker.quit(self)



#*******************************************************************************
# When text editor owns the window: popup
#*******************************************************************************

class TextEditorMainPopup(TextEditor, GuiMakerWindowMenu):
    """
    ----------------------------------------------------------------------------
    Popup PyEdit top-level windows that destroy() to close only self on a Quit
    in the GUI, close with their parent (usually the app root), build a menu on
    a window, and do not check for changes in any other windows on close.
    onQuit is run for Quit in toolbar or File menu, as well as window border X,
    but not from application-menu or Dock Quit when run on Mac OS X.
    
    Makes and builds on new Toplevel window, which is itself a child to another
    parent - the root Tk (for None), an explicit Tk, or other passed-in window
    or widget.  Adds to edit-windows list so will be checked for changes if any
    PyEdit main window quits, and included in auto-saves.

    The new window's parent should generally be the program's Tk root (e.g., a
    main PyEdit window's parent - which is automatic if parent is None), so it
    won't be silently closed by a transient parent's closure while being tracked
    for changes or auto-saves.  This won't cause errors (<Destroy> events now
    update tracking lists), but any unsaved changes would be ignored on close.
    This is bad enough that a "note" is issued here if parent isn't a Tk; this
    is okay iff the client program has its own change tests (e.g., PyMailGUI),
    but not otherwse (e.g., Help initially made README popups dialog chldren).

    [3.0] Note: client programs run on Mac OS X that create TextEditorMainPopup
    windows but are not themselves GuiMakerWindowMenu clients should also call
    guimaker.fixAppleMenuBar() with their app root window's help and quit info.
    That function saves and reapplies the app's info to PyEdit popups, so that
    its application menu's help and quit apply to the whole app as usual.
    ----------------------------------------------------------------------------
    """
    
    def __init__(self, parent=None, loadFirst='', winTitle='', loadEncode=''):
        """
        create and fill own popup editor window
        """            
        self.popup = Toplevel(parent)                     # None: parent=Tk root
        GuiMaker.__init__(self, self.popup)               # use main window menus
        assert self.master == self.popup

        try_set_window_icon(self.popup, kind='-popup')    # [3.0] set (some) icons
        winTitle  = winTitle or 'Popup'                   # [3.0] '' if popup Clone
        wintype   = ' ☝' #if RunningOnMac else ''         # [3.0] distinguish (or ⚐, ⇧)
        fulltitle = 'PyEdit %s - %s' + wintype            # use diff icon on Win/Lin
        self.popup.title(fulltitle % (Version, winTitle))
        self.popup.iconname('PyEdit')
        self.popup.protocol('WM_DELETE_WINDOW', self.onQuit)

        # [3.0] do this _after_ borders: may trigger unicode popup
        TextEditor.__init__(self, loadFirst, loadEncode)  # a frame in a new popup

        # [3.0] should tracking be selectable by args? (tbd)
        if not isinstance(self.popup.master, Tk):
            print("PyEdit note: tracked window's parent is not Tk")
            
        # [3.0] +track for change-test and auto-save in __init__ and <Destroy>


    @modalMenuAction
    def onQuit(self):
        """
        on Quit request in GUI: destroy window
        [3.0] called for window's file-menu or toolbar Quit (only)
        """
        # check this window's unsaved changes only
        close = not self.text_edit_modified()
        if not close:
            close = my_askyesno(self, 'Quit',
                             "This window's text is changed and unsaved.\n\n"
                             'Quit and discard its changes?')
        if close:
            # close this window only (plus its child widgets/windows)
            # <Destroy> removes self from openwindows list
            self.popup.destroy()
            

    def onClone(self):
        TextEditor.onClone(self, makewindow=False)    # I make my own pop-up!



#*******************************************************************************
# When editor embedded in another window: with File/Quit
#*******************************************************************************

class TextEditorComponent(TextEditor, GuiMakerFrameMenu):
    """
    ------------------------------------------------------------------------
    Attached PyEdit component frames with full menu/toolbar options,
    which run a destroy() on a Quit in the GUI to erase self only.
    A Quit in the GUI verifies if any changes in self (only) here.
    Does not intercept window manager border X: doesn't own window.
    TBD: decorate borders if parent is a Tk or Toplevel (e.g., Clone)?

    [3.0] Allow components to be change-tested and auto-saved: add
    self to the openwindows list managed by __init__ and <Destroy>;

    [3.0] Clients: use TextEditor.anyWindowsModified() to check for
    changes in any window on app quit, and instance.isModified()
    to check for changes in a single window on container window close;
    clients can also run the onSave() method directly as desired;
    ------------------------------------------------------------------------
    """
    
    def __init__(self, parent=None, loadFirst='', loadEncode=''):     
        """
        embedded, Frame-based menus
        """
        GuiMaker.__init__(self, parent)                   # all menus, buttons on
        TextEditor.__init__(self, loadFirst, loadEncode)  # GuiMaker must init 1st

        # [3.0] +track for change-test and auto-save in __init__ and <Destroy>


    @modalMenuAction
    def onQuit(self):
        """
        on Quit request in GUI: destroy Frame
        """
        # check this component's unsaved changes only
        close = not self.text_edit_modified()
        if not close:
            close = my_askyesno(self, 'Quit',
                             'Text is changed and unsaved.\n\n'
                             'Quit and discard its changes?')
        if close:
            # erase self Frame but do not quit enclosing app
            # <Destroy> removes self from openwindows list
            self.destroy()



#*******************************************************************************
# When editor embedded in another window: without File/Quit
#*******************************************************************************

class TextEditorComponentMinimal(TextEditor, GuiMakerFrameMenu):
    """
    ------------------------------------------------------------------------
    Attached PyEdit component Frames without Quit and File menu options.
    On startup, removes Quit from toolbar, and either deletes File menu 
    or disables all its items (at the cost of maintenance work); menu and
    toolbar structures are per-instance data: changes do not impact others.
    
    Quit in GUI never occurs, because it is removed from available options;
    instead, a <Destroy> event is used to deregister from tracking lists,
    and clients should xall a change-test method on container and app quit. 
    TBD: decorate borders if parent is a Tk or Toplevel (e.g., Clone)?
    
    [3.0] Allow components to be change-tested and auto-saved: add
    self to the openwindows list managed by __init__ and <Destroy>;
    see ahead for change-test methods available.

    [3.0] Uses client method call to prompt for save if text changed.
    Note that these windows are tracked for changes on PyEdit root 
    window quits, but are part of other windows when used in another
    program with its own root - clients call change-testing manually.
    ------------------------------------------------------------------------
    """
    
    def __init__(self, parent=None, loadFirst='', deleteFile=True, loadEncode=''):
        """
        embedded, Frame-based menus, no File/Quit
        """
        self.deleteFile = deleteFile
        GuiMaker.__init__(self, parent)                  # GuiMaker Frame packs self
        TextEditor.__init__(self, loadFirst, loadEncode) # TextEditor adds middle

        # [3.0] +track for change-test and auto-save in __init__ and <Destroy>


    def checkForLastChanceSavePrompt(self):
        """
        [3.0] optionally called at container's close to prompt for save
        if component text has been changed and not saved to a file;
        we can't veto the close here - this is just a chance to save;

        OTHER OPTIONS:
        -- On container window close, call instance.isModified()
           to check for changes in a single window, and cancel close 
        -- On enclosing app quit, call TextEditor.anyWindowsModified()
           to check for changes in any PyEdit window, and cancel quit
        -- Clients can also run instance.onSave() directly as desired
           to prompt the user for a save
        
        clients should ensure that component will not be closed without
        some change-testing (e.g., use the Tk root for its container's
        parent, not a transient window); <Destroy> cannot check or fetch;  
        """
        if self.text_edit_modified():
            if my_askyesno(self, 'Component close',
                        'Text changed: save its changes now?'):
                self.onSave()   # an automatic Save button press

        
    def start(self):
        """
        extend start() setup method to remove Quit/File
        """
        TextEditor.start(self)                         # GuiMaker start call
        for i in range(len(self.toolBar)):             # delete quit in toolbar
            if self.toolBar[i][0] == 'Quit':           # delete file menu items,
                del self.toolBar[i]                    # or just disable file
                break
        if self.deleteFile:
            for i in range(len(self.menuBar)):
                if self.menuBar[i][0] == 'File':
                    del self.menuBar[i]
                    break
        else:
            for (name, key, items) in self.menuBar:
                if name == 'File':                     # CAUTION: this may break
                    items.append([1,2,4,5,6])          # if file menu is changed




################################################################################
# standalone program run
################################################################################


def testPopup():
    # see also PyView and PyMailGUI for component tests
    root = Tk()
    TextEditorMainPopup(root)
    TextEditorMainPopup(root)
    Button(root, text='More', command=TextEditorMainPopup).pack(fill=X)
    Button(root, text='Quit', command=root.quit).pack(fill=X)
    root.mainloop()


def main():
    """
    --------------------------------------------------------------------------
    Standalone launch: may be typed or clicked, and associated with files.
    No need for heroics to set Mac active-window style here: it's all menus.

    [3.0] Magic no more: this formerly used the implicit/automatic Tk() root,
    because 'parent' defaulted to None, which triggered a default Tk() in
    GuiMaker.  That seems too implicit (especially given that parentage is
    crucial to window closures), so changed to make the root obvious here.
    Because popups pass no explicit parent, root here will be parent to all.

    [3.0] For Mac py2app app-bundle distribution only, manually catch the
    OpenDocument apple event.  This event is delivered both when an associated
    text file is clicked, and when a file is dropped onto the app's icon.  The
    file's name would normally become a command-line arg processed as usual
    (and does for Windows exes created by PyInstaller,) but py2app's argv
    emulation is currently broken (the workaround here dates back to 2012),
    and the event is better: supports drag-and-drop, Open With, and clicks.
    --------------------------------------------------------------------------
    """
    import time
    
    try:                                              
        fname = sys.argv[1]                           # arg = optional filename
    except IndexError:                                # Mac app uses doc events 
        fname = None

    if RunningOnMac and fname and fname.startswith('-psn_'):
        #------------------------------------------------------------------
        # [3.0] on Mac, ignore a ProcessSerialNumber in argv that _may_
        # be passed when a file is opened by Finder via Launch Services;
        # apps cannot use argv in this context, but must instead respond
        # to Mac OpenDoc events on clicks, drops, and Open-Withs -- see
        # the special handler code below; we still allow a valid argv
        # filename, as pyedit might be run from a command-line too;
        #
        # without this check, pyedit would on rare occasion fail to launch
        # for specific files _only_, when the app was not yet running _only_,
        # due to argv[1] == '-psn_0_3834792' (e.g.) causing onOpen() errors
        # and hung error popups;  offending files opened in pyedit otherwise, 
        # copy or rename didn't help, and a TextEdit Save removed the issue;
        #
        # this seemed to happen for files opened in MS-Word inadvertently, 
        # and possibly after a system restart; for one file that triggered 
        # the bogus arg, MS-Word left behind Mac extended attributes...
        #
        # $ ls -l@ Whitepaper.html 
        # -rwxrwxrwx@ 1 blue  wheel  90072 May 30 18:46 Whitepaper.html
	#         com.apple.quarantine	   29 
        # $ xattr Whitepaper.html 
        # com.apple.quarantine
        # $ xattr -p com.apple.quarantine Whitepaper.html 
        # 0002;5928a690;Microsoft Word;
        #
        # all of which is now an obscure moot point given the argv fix;
        #------------------------------------------------------------------
        fname = None

    if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
        # and to be sure, never use _any_ argv as a filename in Mac App mode;
        # this probably subsumes the prior check, but it's an afterthought;
        fname = None
        
    # make main window on Tk root (pack optional)
    root = Tk()
    text = TextEditorMain(root, loadFirst=fname)      # Tk(TextEditor+GuiMaker) 
    text.pack(expand=YES, fill=BOTH)
    startupTime = time.time()                         # epoch seconds

    # [3.0] catch doc-open events in Mac app mode
    if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':

        def openAllDocs(*args):
            """
            ---------------------------------------------------------------
            Catch Mac OpenDoc events -- received on doc clicks, Open With,
            and drag-and-drop -- and open files in the root (if received 
            at startup time) or new popup window(s) (all other receipts).

            OpenDoc events args can be > 1 if many selected and clicked
            as a group, and may come in here either just after the app
            is started, arbitrarily long after it's started, or never if
            the user clicks the app instead of a doc (Open/ReopenApp).
            This event has meaning only on Mac in frozen-app mode: for
            source code, the Python Launcher is the app, not this code.
            
            Open file in first (root) window if and only if event received 
            just after app start, else use popups with parent = Tk root so
            not auto closed with other Toplevels.  This code seems a wacky 
            heuristic, but is unavoidable: we don't want to open docs in a 
            formerly-opened root, but the user may have clicked _either_ 
            the app or a file initially, and only event-receipt time can 
            differentiate.  If PyEdit is embedded, the root is elsewhere 
            and PyEdit is not __main__, so this code is unused/irrelevant.
            
            Windows has no such requirement: either it or PyInstaller's
            bootstrap code spawns a new PyEdit process for each doc open,
            which is less functional (there is no shared state) but simple.
            Note: this is not called with no args if the app itself is
            clicked once it's already open (see the Reopen handler below).

            Also note that app startup sends either either OpenDoc if
            started via a file click or drop -XOR- OpenApp otherwise, and
            OpenDoc can be sent both at app startup and on later doc opens,
            whether the main window is in use or not.  Tk programs seem
            to register event handlers soon enough to catch either event,
            but don't use the main window for a doc _except_ at startup
            (even if user clears with File->New... and adds text or not).

            UPDATE: just like Grep matches, close a new popup window
            if the file is already open and the user opts to not reopen.
            This is debatable, but leaving an empty window under the auto
            raised window(s) where the file is already open seems odd: 
            it was usually closed manually anyhow, and a new popup can 
            always be made quickly on Macs with a new app/Dock click.

            NOTE: it's critical to _not_ open a filename in sys.argv[1]
            in app mode, as Finder/Launch Services may pass anything,
            including a '-psn_*' ProcessSerialNumber; use events instead,
            and ignore psn in argv (it is not also passed here);
                        
            NOTE: very rarely, this failed to open a first file in the 
            newly-launched app's main window for "Open With" (but not for 
            drag-and-drop); increased the delay time to 1.0 (not 0.5) to 
            compensate.  This has not been seen again, and may reflect a
            system or Tk bug, or have been a symptom of the prior note's 
            issue before it was fixed (TBD).

            SUBTLETY: this does an odd encode + decode to fix filenames 
            containing non-BMP Unicode emoji characters.  Either Tk or 
            Python's tkinter munge emojis such that os.path.isfile() in 
            onOpen() returns False, thereby causing such files to fail 
            for any Finder-based open (e.g., drag-and-drop).  Filenames
            are trashed when received here, but seem to contain encoded 
            bytes in a Python decoded str - which is why the encode/decode
            fixes all cases tested.  If this workaround ever fails, such 
            files can still be opened in PyEdit via a File->Open, per the
            popup; their name's emojis are replaced for display either way.
            Examples: docetc/examples/Assorted-demos/non-BMP-emoji-*.txt.
            Absolute pathnames received on this event look like this:
            '/.../Non-BMP-Emojis/Non-BMP-Emoji-both-\xf0\x9f\x98\x8a.txt'
            ---------------------------------------------------------------
            """
            print('PyEdit caught openDoc:', ascii(args), flush=True)
                    
            # may be > one if many selected and clicked
            for arg in args:
                if not os.path.isfile(arg):
                     # fix raw emoji bytes passed in str from tkinter and/or Tk
                     try:
                         arg = arg.encode('latin1').decode('utf8')
                         assert os.path.isfile(arg)   # okay now?
                     except:
                         my_showerror(root, 'OpenDoc', 
                            'OpenDoc failed for "%s"\n\n'
                            'Try opening manually with PyEdit\'s File->Open' % arg)
                         continue   # skip: onOpen() would fail too

                if (len(text.openwindows) == 1 and        # just 1 window open?
                    text.getFileName() == None and        # no file in it (yet)?
                    time.time() < (startupTime + 1.0)):   # just after startup?

                    # file 1, at startup: in already-created root window
                    try:
                        text.onOpen(arg)
                    except Exception as why:
                        # onOpen() should catch all excs: just in case
                        print('OpenDoc root failure:', ascii(why), flush=True)
                        my_showerror(root, 'OpenDoc', 'OpenDoc failed for "%s"' % arg)

                else:
                    # files 2..N: in popup windows, parent=None=Tk root (no self)
                    # not just: TextEditorMainPopup(loadFirst=arg)

                    popup = TextEditorMainPopup() 
                    try:
                        opened = popup.onOpen(arg)
                    except Exception as why:
                        # onOpen() should catch all excs: just in case
                        opened = False
                        print('OpenDoc popup failure:', ascii(why), flush=True)
                        my_showerror(popup, 'OpenDoc', 'OpenDoc failed for "%s"' % arg)

                    if not opened:        # already open + user declined reopen?
                        popup.onQuit()    # auto close empty/covered edit window

        assert RunningOnMac
        root.createcommand('::tk::mac::OpenDocument', openAllDocs)


    # [3.0] catch app-reopen events in all Mac modes
    if RunningOnMac:
        
        def reopenApp():
            """
            ----------------------------------------------------------------
            Respond to the ReopenApplication event when running as either
            a frozen Mac app or source code.  This event is called if the
            app or its Dock entry (of the frozen app, or the Python Launcher
            for source code) is clicked while the app is already running.

            Apple defines a complex protocol for app action (lifting, etc.);
            here, we just open a new empty popup window in response, instead
            of no-op.  The app exits in full if its main window is closed,
            so we'll never receive another reopen event after that point.
            ----------------------------------------------------------------
            """
            print('PyEdit caught reopenApp', flush=True)
            TextEditorMainPopup()                    

        def openApp():
            """
            ----------------------------------------------------------------
            When an app starts, it receives OpenApp (if the app itself was
            clicked) XOR OpenDoc (if the app was started because a doc was
            clicked, drag-and-dropped, or Open-With'ed).  Ignore OpenApp,
            as the normal __main__ logic has already created a root window, 
            but catch OpenDoc above to open a file in the root window when
            that event is received at startup time (else in a new popoup).
            ----------------------------------------------------------------
            """
            print('PyEdit caught openApp', flush=True)   # stub for now

        # PP4E.Gui.Tools.guimaker also binds onQuit to tk::mac::Quit            
        root.createcommand('::tk::mac::ReopenApplication', reopenApp)
        root.createcommand('::tk::mac::OpenApplication', openApp)       
    
    # now it's the user's turn
    root.mainloop() 


if __name__ == '__main__':                            # when run as a script

    #---------------------------------------------------------------
    # [3.0] Add support for using multiprocessing (MP) in Grep.
    # Used for single-file PyInstaller frozen binaries on Windows: 
    # - On Windows calling this function must be called here.
    # - On Linux and OS X (and if not frozen) it does nothing.
    # This is required only in the frozen program's main, which
    # is run in the process that spawns the MP child process.
    # See also multiprocessing_exe_patch.py, imported above.
    # PyEdit lib clients must do this in __main__ too (PyMailGUI).
    #---------------------------------------------------------------
    multiprocessing.freeze_support()
    
    # or testPopup()
    main()                                            # run .pyw for no DOS box
