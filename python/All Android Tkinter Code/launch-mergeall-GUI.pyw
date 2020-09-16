#!/usr/bin/python
"""
================================================================================
launch-mergeall-GUI.pyw:
  desktop GUI launcher (part of the mergeall system)   

-Copyright and author: © M.Lutz, 2014-2019 (http://learning-python.com) 
-License: provided freely, but with no warranties of any kind

#-------------------------------------------------------------------------------
# ANDROID VERSION, January-April 2019
# Per http://learning-python.com/mergeall-android-scripts/_README.html#toc8.
#
# Replace original file with this custom version on your phone (only).
# See "# ANDROID" for all changes applied here and in mergeall_configs.py.
# These changes are for Android only, do not impact the command-lines mode 
# of Mergeall, and might be merged into the original file in a later release.
#
# Recent changes (search here for their [date] labels to find changed code): 
#
# [Apr2119] Pydroid 3 3.0 broke webbrowser: use os.system(cmd) with a 
#           hardcoded Android activity-manager command line instead
#           (3.0's $DISPLAY breaks module, $BROWSER kills "file://").
#
# [Apr1919] Fix merge-spawn workaround to the Pydroid 3 empty sys.executable 
#           bug, to accommodate the different Python path in Pydroid 3's 3.0.
#           The fix reads a spawned 'which python' command to be path agnostic.
#           Also go back to using webbrowser for help and logfiles: it does 
#           work, but iff files use '"file://" and HTML docs use online URLs;
#           see _openbrowser.py for a demo and more details.
#
# [Apr1219] Reenable help and popup-logfile buttons, and fix them to open with
#           an os.system() spawn of an activity-manager command instead of Py's
#           webbrowser; open online version of help, for its latest changes.
#           Also use default color for "Help" - tkinter loses a custom bg.
#
# [Mar2819] Shorten label text again and further, for smaller phone displays.
#           Labels now fit >= 5.5" screens; if still too wide, set the new 
#           LABELFONT user config, or search for "# ANDROID - shorter" to edit.
#           Also for smaller displays, resplit run-dialog text (but not paths).
#
# [Mar2319] Made message text readonly to avoid keyboard popups on slow swipes.
#           This precludes copy/paste, but the on-screen keyboard is annoying.
#           Also manually split run-dialog text (but Tk still truncates paths).
#
# [Mar0819] Added folder-chooser prefills and starts as config-file options.
#           These can often avoid the tedious Android Tk folder-chooser dialog.
#-------------------------------------------------------------------------------

A portable Python 3.X/2.X tkinter/Tkinter desktop GUI, for easily launching
mergeall.py's -report and -auto (but not selective/interactive) usage modes.
For screenshots of this GUI in action, see the examples/Screenshots folder.

Usage: This is a .pyw -- it runs with no console on Windows.  Run this script
with no arguments, via icon clicks, command lines, or other.  Drag it out to
a desktop shortcut for quick access.  See folder docetc/launcher-configs for
a Windows desktop icon (attach it to a shortcut via right-click + Properties).

Uses widgets for choosing options and directory paths and viewing scrollable
mergeall stdout/stderr output, and supports saving and viewing mergeall's
output in log files.  Uses threads to stay active while waiting for mergeall
output lines.  Stays open to support multiple mergeall runs in one session --
report differences, run automatic updates, report on results, etc.  The
underlying mergeall.py was not changed: this is just a GUI shell.

This is easier than launch-mergeall-Console.py (no directory typing, and
quicker options selection), which is easier than running raw mergeall.py
command lines directly and manually from a console or shortcuts, though
mergeall.py command lines support more options (e.g., interactive mode).

As of version 1.4, this also uses threading to always remain responsive.
As of version 2.0, this also supports the mergeall auto-backups option.
As of version 3.0, this also supports mergeall's "-skipcruft" and Mac OS X.
See below for major changes made here, as well as open issues (TBDs).

--------------------------------------------------------------------------------

VERSION 3.1 CHANGES:
These were internals and command-line changes, and had no GUI impact.

VERSION 3.0 CHANGES:

This major release's changes were largely driven by a Mac OS X port,
and new usage on Linux.  Search for 'RunningOnMac' and '3.0' for Mac-ness.
Mergeall grew cruft file, symlink, and Windows long-path support in 3.0,
but most of these are not related to the GUI managed here.

App bar icon for Linux:
    Linux now gets a nice mergeall app bar (launcher) icon.  Mac icons
    remain a TBD, and Windows has always had window icons for this program.

Initial desktop logs folder for both Linux and Mac:
    The preset default for the logs folder now uses $HOME settings on these
    Unix platforms (Windows uses the user's desktop as before).

Redesign run verification dialog for Linux and Mac:
    The dialog popped up just before a run is launched was redesigned to
    make it more readable on Mac and Linux.  Its text was formerly fine
    on Windows, but fairly bunched-up elsewhere.  Also specialized the
    warning text to be less dire if backups are enabled.

Top-level window hack for Mac Tk:
    The Mac port required a top-level window hack to show buttons in Mac
    active-window style initially, using the recommended Tk 8.5 install.
    This is a complex story; see __main__ code in this file for details.

New toggle to suppress comparison lines, all platforms:
    The Mac port also inspired a new GUI toggle to suppress folder comparison
    message scrolling in the GUI (only).  This is on initially for Mac because
    the Mac Tk Text widget is VERY slow: ~30x slower than the mergeall process's
    output.  This toggle is off initially for Windows and Linux, because the GUI
    largely keeps up on these platforms, and the messages indicate progress.
    Still, the new toggle is available on these platforms too, because the GUI's
    scrolling can add a few seconds to mergeall runtime in some tests run on
    Windows, and may be a factor on slower machines; disable as desired.

    Either way, full details, including all comparison messages, are always
    available in saved log files popped up automatically at the end of a run.
    Note that this new toggle differs from 2.4's "-quiet" option and GUI toggle
    described below: "-quiet" disables output in mergeall itself before it ever
    reaches the GUI, because backup messages are arguably distracting in logs
    too; comparison messages are still useful in logs, if not the GUI.
    
    Unlike all other widgets (except the new post-run popup toggle), this toggle
    is also dynamic: setting it on/off while mergeall is running hides/shows 
    messages currently being generated.  The 'skipping' message is displayed 
    every time this toggle is turned back on, though it does not appear until 
    the next mergeall message is received.

    TBD: Mac text scrolls still seem painfully slow when there are many
    difference-report lines.  These could be also be suppressed, in addition
    to folder comparison messages, by: line.startswith(('comparing', '[', ' ')).
    This was ruled out, as it makes report-mode runs useless.  Text speed must
    be fixed by Tk's Mac developers (though one report on it went unreplied).

    UPDATE: see docetc/miscnotes/mac-weirdly-slow-tk85-text-scroll.py for a
    simple self-contained demo of the text scrolling slowness on ActiveState
    Tk 8.5.18 (the Tk recommended by python.org), Python 3.5, and OS X 10.11.
    It finishes scrolling in just 3-4 seconds on Windows, but 85 on Mac!
    
    UPDATE: recent heroic efforts at speeding Mac Text widget scrolling came
    up short.  It's simply slow in all Mac Tks tested - 8.5.9 through 8.5.18.
    The culprit seems to be update() calls required to redraw the widget after
    new text is inserted.   The code used to scroll uses normal techniques:
         statustxt.insert(END, line)    # add to Text widget
         statustxt.see(END+'-2l')       # reposition text
         statustxt.update()             # update display from within a loop
    1) Alternative scroll techniques tried had no effect on speed:
         statustxt.yview_scroll(2, 'units')
         statustxt.yview_moveto(1.0)
         statustxt.yview(END)
    2) Using update_idletasks() speeds scrolls only slightly, and all the GUI's
    controls are unresponsive while the text scrolls (an unacceptable effect):
         statustxt.update_idletasks()
    3) The after() timer loop's speed proved irrelevent, as the code mostly
    stays in the 'batch' inner loop, and doesn't rescedule after() events:
        statustxt.after(10, streamconsumer, linequeue, logfile, logpath)
    4) The update() call can be avoided by processing just 1 line per after()
    event (instead of the batch inner loop) with a very low delay count, but
    this has NO impact on scroll speed - implicit updates are also too slow:
        statustxt.after(1, streamconsumer, linequeue, logfile, logpath)
    5) This leaves disabling scrolls (the new toggle), or updating only after
    groups of lines are addded, which makes scrolling too jumpy and chaotic:
         global upcnt
         upcnt += 1
         if upcnt % 50 == 0:
             statustxt.update() 
    In the end, this is a Mac Tk bug, which hopefully is or will be addressed
    in later Tks on the Mac.  The new toggle is mergeall's best workaround.

New script to delete Mac ".*" cruft files:
    The Mac platform has a habit of creating lots of metadata files and a few
    folders, whose names all start with a ".", and which are sometimes treated
    as hidden.  These have meaning and purpose on a Mac, but are useless
    noise on other platforms.  For mergeall users on Windows and Linux whose
    archive might become infected with these files by an association with a
    Mac, a new script, "nuke-cruft-files.py," is provided to remove such files
    as a pre-step or post-step to mergeall runs that copy archives off a Mac
    See that script's extensive docstring for more details.

Disable widgets instead of erasing them, all platforms:
    Also partly for the Mac, the GUI was redesigned to enable/disable widgets
    as they fall in and out of relevance, instead of drawing/erasing them with
    pack() and pack_forget().  The latter scheme causes a noticeable flash on a
    Mac, but may have been too dramatic in general.  The "GO" button didn't
    cause flash, but enabling/disabling worked around an old text scroll issue.
    
New mode and toggle to skip system cruft files in both TO and FROM
    Inspired by the numerous ".*" files added to archives on Mac OS X, both
    mergeall and diffall grew a "-skipcruft" command line argument and mode,
    which skips known cruft files of all platforms in both FROM and TO.  The
    GUI also grew a new toggle to suport this new mode and argument. 

    When enabled, the net effect is that cruft files do not register as
    differences in report runs, and are not copied to, removed from, or replaced
    in the TO tree in update runs.  Such files thus stay on their generating
    platform only - they won't be transferred to intermediate drives and other
    computers, and won't be deleted from the generating platform by future
    merges.

    This option can be disabled, because users of a single platform may not
    care about their cruft, and some crufts may be more useful than others.
    Cruft files are defined in the mergeall_config.py file; users are
    encouraged to adjust the set of matching files as needed for their use.

Sanitize Unicode characters in message-scroll text outside Tk's BMP range
    Through 8.6, at least, Tk cannot display Unicode characers whose code
    points are outside range U+0000..U+FFFF (BMP, UCS-2).  Passing these to
    Tk raises an uncayght exception which leaves the GUI in an unpredictable
    state (usually half-drawn or hung).  To work around this, replace all
    such characters with the standard Unicode replacement character, which
    renders as a generic indicator.  This limit may be lifted in Tk 8.7.
    Update: also an issue for pathnames in Browse folder dialogs, fixed here.
    
More descriptive GUI labels and popups
    Toggle labels and ppups were given more explicit labels for clarity.

Allow editor popup to be disabled: config setting, new toggle
    The automatic popup of a text editor to view a saved mergeall log file
    can now be dsabled by a setting in mergeall_configs.py (on by default).
    The popup may seem overkill to users who require a view-only display.

    UPDATE: this is now switchable on/off by a new toggle in the GUI itself.
    The configs-file setting is retained, but used only for an intial value
    for the new toggle. The popup is normally unused, and GUI clicks are 
    easier than config edits.  This new toggle is dynamic, like the message
    scroll disabler; you can click it during a run to impact the popup. 

Configurable message text display area
    Users can now tailor the color, font, and initial size of the GUI's
    scrolled display area for mergeall messages, in mergeall_configs.py.
    The GUI's cosmetics were also polished in general along the way.

Mac changes to open dialogs (Browse for  folders TO, FROM, Logs)
    On Macs, use "message" ("title" is ignored), and add slide-down sheet
    style (versus popup window) via "parent=root" if configs file setting.
    Save dialogs seem to post titles correctly.  Mac's standard menu is
    customized here too, even though this program doesn't have one per se.

mergeall and cpall: copy unix symlinks, don't follow
    Avoid redundant data copies.  See mergeall.py and cpall.py for details.

Refocus on window after standard/common dialogs for Mac
    Run a root.focus_force() after all standard dialogs used here to force
    focus and active styling to be reset after dialog is closed.  Else, Mac
    users must click window after dialogs.  This may be AS Tk 8.5 only; has
    no effect on the initial style issue discussed earlier; and parent=root
    doesn't suffice to reset focus in the standard dialogs used here.

    TBD: should these dialogs also be made slide-down sheets on Mac like
    the open/save diaogs via parent=root, instead of modal popup windows?
    Some Mac purists may vote yea, but mergeall currently sides with variety,
    especially given that the mergeall GUI is a single-window interface.

mergeall output forced to ASCII in PyInstaller Windows exes
    A continuation of a long-running theme here, mergeall now forces stdout
    text to be ASCII when running as a frozen executable on Windows ONLY.
    See mergeall.py for details; this works around a likely PyInstaller bug.

--------------------------------------------------------------------------------

VERSION 2.4 CHANGES:
Added a toggle for the new "-quiet" script option that turns off per-file
"...backing up" log message printing in the underlying mergeall program.
These messages may make reading the log more work than it should be, and
don't add much information once backups are understood.  The new "-quiet"
toggle in the GUI is active only when backups are enabled.  Also tweaked
some GUI labels' text for clarity.  

VERSION 2.2 and 2.3 CHANGES:
These versions were optimizations and patches, and had no impact on this GUI.

VERSION 2.1 CHANGES:
This version's changes were command-line only, and had no effect on this GUI.

--------------------------------------------------------------------------------

VERSION 2.0 CHANGES:
1) Added Backups toggle and corresponding mergeall -backup command-line arg.
The new backups frame retains state but is shown/hidden when -auto is
selected/deselected, as it's applicable to -auto only here (not -report).
In the console launcher, -backup is applicable to both -auto and
selective (=[not -report]) modes.  Defaults to enabled in the GUI.

2) Moved log-file path chooser widgets down to log-file toggle button section.
The chooser retains state but is now shown/hidden when logging is toggled
on/off, as it's applicable when logging only.

3) Added "help" button that pops up the main usage doc in a web browser.
Packed in the run-mode frame's unused space.

4) The new "finished\n\n" message issued by mergeall solves the issue here
where the last output line was covered by repacking the GO button after resizes.
This works better, as it doesn't require the text display to scroll abruptly.

5) Use more descriptive text for the mode radio buttons (formerly was just
not "Report Only" and "Automatic Updates").

6) Error-check the FROM and TO paths here before trying to run mergeall, so
produces a GUI popup instead of mergeall text output message (log file path
was already being checked this way, because it required an open here).

7) Default to Desktop for log files on Windows (initial setting value only).

--------------------------------------------------------------------------------

VERSION 1.7.1 CHANGES:
None here (usage note, mergeall error message format change: see Revisions.html).

VERSION 1.7 CHANGES:
1) Minor bug fix for 2.X only -- add import of Tkinter's showerror when
using 2.X, else dialog never appears if bad log-file name.

2) Catch PermissionError (etc.) on log file open and report error in popup;
else fails silently on Windows, as ".pyw" has no console for exception text.

--------------------------------------------------------------------------------

VERSION 1.6 CHANGES: a new Python 2.X Unicode workaround, verify quits

Decoding an output line read from the spawned mergeall.py stream can fail
rarely in Python 2.X (only), if there are non-ASCII filename characters 
in the line.  This failure does not occur in 3.X.  Patched to catch the 
decode error and recover, with a notation at the front of the line in the 
GUI.  This change impacts text in the GUI display only; it does not impact
text in the log file, or the underlying mergeall process's run.  Also added
a verify dialog for the window close button to avoid accidental exits.

[Discussion] The Unicode decode failure seems a fundamental 3.X/2.X 
behavior difference.  After initial research, the most likely culprits 
appear to be:

a) The 2.X subprocess module mutates non-ASCII stream lines in transit.

b) The 2.X print statement generates either already-decoded text, or 
   wrongly-encoded bytes that do not respect the PYTHONIOENCODING setting.

In either case, this may reflect the fact that there is no notion of a 
truly binary bytes stream in 2.X -- the content of subprocess output is 
not as clearly defined as in 3.X's strict text/bytes dichotomy worldview.  

Note that setting PYTHONIOENCODING in the shell does not fix this failure.  
This environment variable is used for prints to the console, but this GUI
does only screen updates and log file writes itself, and exports this 
setting automatically to the mergeall subprocess for its prints.  Testing
verifies that os.environ settings are inherited by 2.X subprocesses too, 
even when spawned by the subprocess module.

Whatever the exact cause, this is a fundamental 2.X/3.X difference and 
another 2.X/3.X semantic incompatibility that goes well beyond syntax.  
In this case, adding an exception handler around the offending decode 
fixed the failure for all cases tested in 2.X, so this issue is closed.  
Given the other 2.X/3.X incompatibilities found and addressed in this 
project, though, it seems that writing dual-version 2.X+3.X code may be
a bit of a pipedream when it comes to realistic, practical programs.  
If in doubt, try running mergeall on Python 3.X instead of 2.X.

Also note that this patch applies only to the GUI launcher: PYTHONIOENCODING 
must still generally be set manually in your system shell when running either
the console launcher or script mergeall.py directly from a command line, if 
either may ever process and thus print non-ASCII filenames.  Else, such 
filenames may cause both scripts to abort, especially in Python 3.X.  The 
GUI launcher does not require this setting, as it automatically sets and 
propagates this variable to its mergeall.py subprocess, and never prints.

[3.0] UPDATE: for its PyIstaller frozen executable ONLY, mergeall must force
stdout text to ASCII, which isn't ideal, but is requied in this context to
avoid exceptions, and sidesteps this entire display-only issue.

--------------------------------------------------------------------------------

VERSION 1.5 CHANGES: Linux port and usage 

Pass shell=False on Linux/Unix (only) to subprocess.Popen, else starts a 
"python" interactive shell even though a full command sequence is passed. 
Linux users: see also release 1.5 notes in docs/Revisions.html for "#!"
pointers, and a possible NTFS timestamp skew issue for Windows/Linux
cross-platform syncs.

--------------------------------------------------------------------------------

VERSION 1.4 CHANGES: threads, streams, log files

1) Threading

   Add threading for the mergeall subprocess stream reader, a former TBD.
   This structure is more complex -- it trades a simple loop for two functions
   and multiple levels of loops -- but prevents the GUI from becoming blocked
   and unresponsive while waiting for a next line from the subprocess.

   This was normally not an issue: the GUI updates after each new line, and is
   used just for viewing after starting a mergeall run (and it's "GO" button is
   erased during this process to avoid overlapping runs).  However, blocked
   states are not natural in GUIs, and they can become apparent here if mergeall
   is busy copying large trees.  See book (PP4E) for more details and examples
   of GUI threading.

2) Stream Unicode decoding, take 2

   Force UTF8 encoding for prints in mergeall subprocess via PYTHONIOENCODING, 
   and use binary mode Popen stream reads + manual post-read UTF8 decoding here.
   Version 1.2 formerly made the subprocess's streams encoding match Popen's
   expectation (cp1252 on Windows) by using locale.getpreferredencoding(False);
   that works for reading the stream, but not for prints within mergeall itself.

3) 2.X log-file compatibility

   Use binary mode for the log files, writing the now-binary stream data.
   Former versions allowed for non-ASCII filenames in the log file text by
   using text mode and writing characters as UTF8, but the 2.X codecs.open()
   doesn't expand \n the same as 3.X's text-mode open() (see also next item).

4) 2.X unbuffered streams compatibility

   Temporarily dropped '-u' in mergeall spawn command-line, as it makes eolns
   (linebreak character sequences) \n in 2.X, but \r\n in 3.X.  This causes
   issues in log-file writes: without a \r\n on Windows, files are single lines.

   LATER UPDATE: the Python '-u' unbuffered flag has been reinstated.  Without
   it, mergeall output may not appear for 10 or more seconds on some machines
   and slower devices due to internal buffering.  Because this flag also makes
   line-breaks differ between Python 2.X and 3.X, though, also need to use
   special-case log-file writes to map all linebreaks to the platform's version.

   This is a complex 3.X/2.X compatibility issue, involving -u, Popen, and opens.
   Neither Popen text mode streams nor the 2.X codecs.open() will help.  The
   former can't be used because its internal encoding policy (per locale) is
   not broad enough to handle arbitrary Unicode filenames, and the latter always
   opens in binary mode, and so does no translations of linebreaks in the decoded
   text (3.X's text-mode open() does expand linebreaks by default).

   Could write binary lines in 2.X text-mode open() to expand \n on Windows,
   but that won't work in 3.X -- its text-mode open() expects Unicode strings,
   and always does encoding in addition to linebreaks.  Writing manually
   encoded text via open() in 3.X and codecs.open() in 2.X also won't work:
   2.X requires manual \r\n, which 3.X will by default expand to \r\r\n.
   3.X open() supports a 'newline' argument to turn off \n expansion, but
   this can't be used either, as it's not available in 2.X's codecs.open().
   As in, *punt*: write binary data with manual \n mapping for log files.

--------------------------------------------------------------------------------

TBD 1: No selective/interactive mode in GUI

mergeall's interactive mode is unavailable here as is, due to an outstanding
TBD regarding handling and interleaving of stdout for input() prompts in spawned
Python 3.X processes.  In practice, though, the -report and -auto modes have been
the only modes regularly used.  See launch-mergeall-Console.py for details on the
issue (the console launcher supports interactive mode, but without a log file).

TBD 2: 2.X compatibility for Unicode filenames?

This system works well on 3.X (it's main usage platform) and is largely 2.X
compatible, but the launchers may still have issues in some stream decoding
for non-ASCII filenames.  No such encoding exceptions occur on 2.X for the
raw mergall.py script, though some non-ASCII os.listdir results seem a bit
suspect in 2.X too.  More complete 2.X testing remains suggested exercise.
  --> Update: see also the 1.6 decoding change note above. <--

TBD 3: Decoupled versus single-process models?

The launchers currently use a standard decoupled model that spawns mergeall
and reads and decodes its streams.  There may be advantages to using a
single-process model that instead imports and calls mergeall's functions.
See docs\Lessons-Learned.html for more discussion on this alternative.

================================================================================
"""

#from __future__ import print_function   # 2.X compatibility: not needed here
APPNAME = 'mergeall'
VERSION = 3.1

# [3.0] for frozen app/exes, fix module+resource visibility (sys.path)
import fixfrozenpaths

import sys
if sys.version[0] >= '3':   # Py 3.X, but allow for Py 4.X too [3.0]
    import _thread, queue
    from tkinter import *
    from tkinter.messagebox   import askokcancel, showinfo, showerror
    from tkinter.filedialog   import Directory                 # saves last dir
    from tkinter.scrolledtext import ScrolledText
else:
    import thread as _thread, Queue as queue                   # Py 2.X compatibility
    from Tkinter              import *
    from tkMessageBox         import askokcancel, showinfo, showerror    # [1.7] 
    from tkFileDialog         import Directory
    from ScrolledText         import ScrolledText

    #import codecs
    #open = codecs.open   # [1.4] log binary mode from stream, not text files

# this script isn't too platform-specific, but avoid repeating this
RunningOnMac     = sys.platform.startswith('darwin')
RunningOnWindows = sys.platform.startswith('win')
RunningOnLinux   = sys.platform.startswith('linux')

import webbrowser, subprocess, time, os

# [3.0] data+scripts not in os.getcwd() if run from a cmdline elsewhere,
# and __file__ may not work if running as a frozen PyInstaller executable;
# use __file__ of this file for Mac apps, not module: it's in a zipfile;

MYDIR = fixfrozenpaths.fetchMyInstallDir(__file__)   # absolute

# [3.0] new doc, in this script's folder - but not necessarily '.' (cwd)
HELPFILE = os.path.join(MYDIR, 'UserGuide.html')

# [3.0] Mac OS X is pickier about file URLs
if RunningOnMac:
    HELPFILE = 'file:' + HELPFILE

# ANDROID [Apr1219] - open latest online version of user guide (all platforms should)
HELPURL = 'https://learning-python.com/mergeall-products/unzipped/UserGuide.html'

# [3.0] part of PP4E's guimaker module, copied here to avoid dependency
from guimaker_pp4e import fixAppleMenuBar

# [3.0] user configs: scrolled messages text area, log-file popup;
# for GUI settings, None = use Tk defaults: 24 lines high, 80 chars wide;
try:
    from mergeall_configs import (
        LOGEDITORPOPUP,
        DEFAULTLOGDIR,
        MACSLIDEDOWN,
        TEXTAREAHEIGHT, TEXTAREAWIDTH, TEXTAREAFONT, TEXTAREACOLOR,

        # ANDROID [Mar0819]
        DEFAULTFROMDIR, DEFAULTTODIR,                # entry prefills: see usage ahead
        BROWSELOGDIR, BROWSEFROMDIR, BROWSETODIR,    # chooser-dialog starts: ditto

        # ANDROID [Mar2819]
        LABELFONT,                                   # font if labels too wide to fit
        HEADERFONT)                                  # custom font for section headers

except Exception as why:
    # if any fail, all default (brutal, but simple)
    LOGEDITORPOPUP = True   # default: initial value for log-file popup toggle 
    DEFAULTLOGDIR  = None   # default: Desktop folder?, per running platform
    MACSLIDEDOWN   = False  # default: popup, not sheet, for folder dialogs
    TEXTAREAHEIGHT = 20     # initial number lines in message scroll widget
    TEXTAREAWIDTH  = None   # initial number characters per line, wrapped
    TEXTAREAFONT   = None   # scrolled messages font, None=Tk default font
    TEXTAREACOLOR  = None   # scrolled messages color(s), None=Tk default font

    # ANDROID [Mar0819]
    DEFAULTFROMDIR = None   # default: always Browse in GUI (entry prefill)
    DEFAULTTODIR   = None   # ditto
    BROWSELOGDIR   = None   # default: use tkinter start default (chooser dialog)
    BROWSEFROMDIR  = None   # ditto
    BROWSETODIR    = None   # ditto

    # ANDROID [Mar2819]
    LABELFONT      = None   # default to system default: best on most devices 
    HEADERFONT     = None   # default to small preset in code ahead

    print('Error in config file: %s' % why)   # to console, if any


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
    Use here: filenames in mergeall messages scrolled text (rare, but true).
    """
    if TkVersion <= 8.6:
        text = ''.join((ch if ord(ch) <= 0xFFFF else '\uFFFD') for ch in text)
    return text


def isNonBMP(text):
    """
    [3.0] Return true if any char (codepoint) in text is outside Tk's BMP range.
    Used by folder dialogs to force initialfile=None when True for prior choice.
    """
    if TkVersion <= 8.6:
        return any(ord(ch) > 0xFFFF for ch in text)
    else:
        return False   # and assume Tk 8.7 will make this better...


def refocusWindow():
    """
    [3.0] Call after (most) standard dialogs to reset focus on the main
    window, else focus and active style are lost when dialog is closed.
    This may be a bug in ActiveState Tk 8.5 (TBD), but the fix is simple.
    """
    root.focus_force()   # else Mac requires a user click after dialogs



####################################################################################
# GUI BUILDER
####################################################################################



# font for headers in controls sections;
# could be user-configurable too, but seems arguably-better hardwired;
# [2.4] not just 'bold': if used as family name, Tk falls back on arial!
# [3.0] smaller font on Linux, else looks almost cartoonish;

HDRFONT = 'arial 14 bold'         # ('family', size, 'style? style?...')
if RunningOnLinux:
    HDRFONT = 'arial 12 bold'     # smaller is better on Linux (not Mac, Windows)   

# ANDROID - go smaller (arial==helvetica, which supports bold in font str or tuple);
# [Mar2819] also allow user to give header font in config file, along with label font;
#
HDRFONT = HEADERFONT or 'arial 6 bold'    # use small default if None


def makewidgets(root):
    """
    build the gui window, setup Browse/GO/other event handlers
    """
    # used on GO
    global dirents                                                    # folders
    global modevar, logvar, bkpvar                                    # settings
    global quietvar, cmpmsgsvar, cruftvar, logpopupvar                # more settings
    global gobutton, statustxt                                        # widgets


    #---------------------------------------------------------------------------
    # Event handlers (less ongobutton: ahead)
    #---------------------------------------------------------------------------

    # some use names in the enclosing func (which are actually globals)
    
    # one open dialog for entire run, saved in scope (closure) 
    opendirdlg = Directory() 

    def onbrowse(field, label):
        title = 'Choose mergeall %s folder' % label
        if RunningOnMac:                              # [3.0] specialize on Mac
            if MACSLIDEDOWN:
                # Mac: message (title ignored), slidedown window, custom text
                title = 'Choose mergeall %s folder' % label
                dlgkargs = dict(message=title, parent=root)
            else:
                # Mac: message (title ignored), popup window, standard text
                title = 'mergeall: Choose %s Folder' % label
                dlgkargs = dict(message=title)
        else:
            # Windows+Linux: the usual modal popup, standard text
            title = 'mergeall: Choose %s folder' % label
            dlgkargs = dict(title=title)

        # check prior pathname choice for emojis: kills dialog
        prior = opendirdlg.options.get('initialdir', '')
        if isNonBMP(prior):
            dlgkargs.update(dict(initialdir=None))   # for this call only

        # ANDROID [Mar0819] - use config starts if set because the Android tkinter
        # chooser GUI is tedious+slow (like its Linux cousin, but worse on phones);
        # Android uses different settings for entry prefills and dialogs starts;
        # 
        starts = dict(FROM=BROWSEFROMDIR, TO=BROWSETODIR, Logs=BROWSELOGDIR)
        if starts[label] and os.path.isdir(starts[label]):
            dlgkargs['initialdir'] = starts[label]
        else:
            pass                                   # use tkinter's default 
            # or: dlgkargs['initialdir'] ='/'      # dlgkargs.update() is overkill here
            # dlgkargs['initialdir'] = None        # this leaves None and kills isNonBMP

        chosendir = opendirdlg.show(**dlgkargs)
        if chosendir:
            field.delete('0', END)
            field.insert(END, fixTkBMP(chosendir))
        refocusWindow()   # [3.0] else requires click on Mac

    def onquit():
        answer = askokcancel('%s: Verify Exit' % APPNAME, 'Really quit mergeall now?')
        if answer:
            win.quit()              # win in enclosing scope; or sys.exit()
        else:
            refocusWindow()         # [3.0] else requires click on Mac

    def onmodetoggle():
        if modevar.get().startswith('REPORT'):          # hide/show backups frame [2.0]
            # [3.0] bkpfrm.pack_forget()                # -backup applies to -auto updates only
            bkpbtn.config(state=DISABLED)               # enabled/disable widgets [3.0]
            quietbtn.config(state=DISABLED)
            cruftbtn.config(text='Skip cruft items in FROM and TO?')   # ANDROID - shorter
                                 #'do not report as differences?')     # ANDROID
        else:
            # [3.0] bkpfrm.pack(expand=YES, fill=X)
            bkpbtn.config(state=NORMAL)
            quietbtn.config(state=NORMAL)
            cruftbtn.config(text='Skip cruft items in FROM and TO?')    # ANDROID - shorter
                                 #'do not copy, replace, or delete?')   # ANDROID

    def onlogtoggle():
        if logvar.get():                                # show/hide log-file path chooser [2.0]
            # [3.0] logdirfrm.pack(expand=YES, fill=X)  # chooser applies only if logging
            logbtn.config(state=NORMAL)
            logent.config(state=NORMAL)
            logpopupbtn.config(state=NORMAL)            # [3.0] ditto for log-popup toggle
            #logpopupbtn.config(state=DISABLED)         # ANDROID - webbrowser failed initially 
        else:
            # [3.0] logdirfrm.pack_forget()
            logbtn.config(state=DISABLED)
            logent.config(state=DISABLED)
            logpopupbtn.config(state=DISABLED) 

    def onbkptoggle():
        if bkpvar.get():                             # show/hide -quiet toggle button [2.4]
            # [3.0] quietbtn.pack(anchor=NW)         # -quiet applies only if doing backups,
            quietbtn.config(state=NORMAL)            # and whether saving to log file or not
        else:
            # [3.0] quietbtn.pack_forget()
            # quietvar.set(False)                    # keep prior setting, disabled=moot [3.0]
            quietbtn.config(state=DISABLED)

    def onhelp():
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
        # ANDROID [Apr2119]: Pydroid 3 3.0 broke webbrowser and changed 
        # $BROWSER - use os.system() with a hardcoded command-line string;
        #
        brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
        cmd = brw % HELPURL
        os.system(cmd)          # was os.environ['BROWSER'], webbrowser.open(HELPURL)

        # other platforms code...
        """
        webbrowser.open(HELPFILE)                    # popup local file in web browser
        """


    #---------------------------------------------------------------------------
    # Build the GUI (link to handlers)
    #---------------------------------------------------------------------------


    #
    # MAIN WINDOW
    #
    
    win = root                                    # [3.0] allow for TopLevel() or Tk()
    win.title('mergeall %.1f' % VERSION)          # set main window title, [1.6] version
    win.protocol('WM_DELETE_WINDOW', onquit)      # [1.6] catch/verify window close

    # replace red (no, blue...) tk icon?
    iconfolder = os.path.join(MYDIR, 'icons')
    try:
        if RunningOnWindows:
            # try Windows window icon
            icnpath = os.path.join(iconfolder, 'mergeall.ico')
            win.iconbitmap(icnpath)

        elif RunningOnLinux:
            # try Linux app-bar icon [3.0]
            icnpath = os.path.join(iconfolder, 'mergeall.gif')
            imgobj = PhotoImage(file=icnpath)
            win.iconphoto(True, imgobj)

        elif RunningOnMac or True:
            # Mac OS X: neither of the above works (yet?) [3.0]
            # Macs require apps for most icon contexts
            raise NotImplementedError
        
    except Exception as why:
        # punt: bad file/call or platform (Mac OS X TBD)
        pass

    # [3.0] on Mac, customize app-wide automatic top-of-display menu
    fixAppleMenuBar(root, 'mergeall',
                    helpaction=onhelp, aboutaction=None, quitaction=onquit)

    ctrlfrm = Frame(win)
    ctrlfrm.pack(expand=NO, fill=BOTH, side=TOP)

    
    #
    # MAIN TO/FROM DIRECTORY CHOOSERS
    #
    
    dirsfrm = Frame(ctrlfrm, relief=GROOVE, border=3)
    dirsfrm.pack(fill=X)
    Label(dirsfrm, text='Main Folders', font=HDRFONT).pack()   # [2.4] font

    rowsfrm = Frame(dirsfrm)
    rowsfrm.pack(expand=YES, fill=X)
    rowsfrm.columnconfigure(1, weight=1)

    dirents = {}
    for (row, key) in enumerate(('FROM', 'TO')):
        rowsfrm.rowconfigure(row, weight=1)
        Label(rowsfrm, 
              font=LABELFONT,                 # ANDROID - configurable [Mar2819]
              text=key + ' folder:').grid(row=row, column=0, sticky=E)

        dirent = Entry(rowsfrm)
        dirent.insert(END, 'enter or browse...')
        dirent.grid(row=row, column=1, sticky=EW)

        handler = lambda dirent=dirent, key=key: onbrowse(dirent, key)   # current!
        Button(rowsfrm, text='Browse...',
               command=handler).grid(row=row, column=2)
        dirents[key] = dirent

    # ANDROID [Mar0819] - prefill to avoid tedious Android/phone chooser dialog
    for (key, prefill) in [('FROM', DEFAULTFROMDIR), ('TO', DEFAULTTODIR)]:
        if prefill and os.path.isdir(prefill):
            dirents[key].delete('0', END)
            dirents[key].insert(END, prefill)


    #
    # RUN MODE RADIO BUTTONS: -report or -auto
    #
    
    radiofrm = Frame(ctrlfrm, relief=GROOVE, border=3)
    radiofrm.pack(fill=X)
    Label(radiofrm, text='Run Mode', font=HDRFONT).pack()

    # help button: use empty space in run mode frame [2.0]
    # ANDROID [Apr1219]: use default color to avoid loss, was [relief=FLAT, bg='white')]
    #
    helpbtn = Button(radiofrm, text='Help', command=onhelp)
    helpbtn.pack(side=RIGHT, anchor=NE)
    #helpbtn.config(state=DISABLED)                 # ANDROID - webbrowser failed initially
 
    modevar = StringVar()
    modes = ['REPORT: show differences only',       # ANDROID - shorter
             'UPDATE: make TO the same as FROM']    # ANDROID - shorter
    for mode in modes:
        Radiobutton(radiofrm,
                    text=mode,
                    font=LABELFONT,                 # ANDROID - configurable [Mar2819]
                    variable=modevar,
                    value=mode,
                    command=onmodetoggle).pack(side=TOP, anchor=NW)
    modevar.set(modes[0])

    # [3.0] skip cruft files in FROM and TO - don't copy/remove/replace or report 
    cruftvar = BooleanVar()                                
    cruftvar.set(True)
    cruftbtn = Checkbutton(radiofrm, 
                           text='Skip cruft items in FROM and TO?',   # ANDROID - shorter
                                #'do not report as differences?',     # ANDROID
                           font=LABELFONT,                            # ANDROID - configurable [Mar2819]
                           variable=cruftvar)
    cruftbtn.pack(side=LEFT)


    #
    # MESSAGE TOGGLES + LOG DIRECTORY CHOOSER
    #
    
    msgfrm = Frame(ctrlfrm, relief=GROOVE, border=3)
    msgfrm.pack(fill=X)
    Label(msgfrm, text='Messages', font=HDRFONT).pack()

    logfrm = Frame(msgfrm)
    logfrm.pack(side=TOP, fill=X)
    logvar = BooleanVar()                                  # Intvar works too
    logvar.set(True)                                       # else default=off (eibti)
    Checkbutton(logfrm,
                text='Save logfile to folder? ',           # ANDROID - shorter
                font=LABELFONT,                            # ANDROID - configurable [Mar2819]
                variable=logvar,
                command=onlogtoggle).pack(side=LEFT)

    # log-file dir chooser by toggle, unhide/hide when toggled on/off [2.0]
    key = 'Logs'
    logdirfrm = Frame(logfrm)
    logdirfrm.pack(expand=YES, fill=X)
    handler = lambda: onbrowse(logent, key)     # last, not current (!) [see above]
    logbtn = Button(logdirfrm, text='Browse...', command=handler)
    logbtn.pack(side=RIGHT)

    logent = Entry(logdirfrm)
    logent.insert(END, 'enter or browse...')    # ANDROID - shorter
    logent.pack(side=LEFT, expand=YES, fill=X)
    dirents[key] = logent
    
    # [3.0] logdirfrm.pack_forget()   # till logs toggled on (now enabled/disabled)
    logbtn.config(state=NORMAL)       # till logs toggled on (initially are)
    logent.config(state=NORMAL)

    # fill initial/default logs folder value  
    if DEFAULTLOGDIR and os.path.exists(DEFAULTLOGDIR):
        # [3.0] allow user-configs file to give initial default 
        defaultlogs = DEFAULTLOGDIR
    else:
        try:
            # [2.0] try user's Desktop on Windows (has HOMEPATH but no HOME)
            defaultlogs = r'C:\Users\%s\Desktop' % os.environ['username']
            assert os.path.exists(defaultlogs)
        except:
            try:
                # [3.0] try same on Linux and Mac OS X (TBD: or Documents?)
                defaultlogs = os.path.join(os.environ['HOME'], 'Desktop')
                assert os.path.exists(defaultlogs)
            except:
                # ANDROID - try internal-storage docs folder (on some phones);
                # [Mar0819] don't use /sdcard/Documents as a prefill (made by 
                # MS Office apps); create the preset if it doesn't exist; but
                # still use DEFAULTLOGDIR as the prefill instead, if it's set;
                #
                try:
                    defaultlogs = '/sdcard/Admin-Mergeall'   # was '/sdcard/Documents'
                    if not os.path.exists(defaultlogs):      # make now if needed
                        os.mkdir(defaultlogs)
                    assert os.path.isdir(defaultlogs)        # exists + is a folder
                except:
                    defaultlogs = None

    if defaultlogs:
        # may be unset or fail on some Unix and Windows =>  empty, Browse
        logent.delete('0', END)
        logent.insert(END, defaultlogs)

    # [3.0] allow comparison messages to be suppressed (mostly for Mac speed);
    # this toggle (only) is dynamic: can change effect while output scrolling; 
    cmpmsgsvar = BooleanVar()
    if RunningOnMac:
        cmpmsgsvar.set(True)               # initial=suppress on Mac OS X
    else:
        cmpmsgsvar.set(False)              # off on Windws/Linux: fast GUI
    Checkbutton(msgfrm,
                text='Hide comparison messages?',     # ANDROID - shorter [Mar2819]
                font=LABELFONT,                       # ANDROID - configurable [Mar2819]
                variable=cmpmsgsvar).pack(side=LEFT, anchor=NW)

    # [3.0] allow log-file popup editor to be suppressed in the GUI per run;
    # the configs-file entry added previously now gives an initial value only;
    logpopupvar = BooleanVar()
    logpopupvar.set(LOGEDITORPOPUP)
    logpopupbtn = Checkbutton(msgfrm,
                text='Popup logfile?',         # ANDROID - shorter [Mar2819]
                font=LABELFONT,                # ANDROID - configurable [Mar2819]
                variable=logpopupvar)
    logpopupbtn.pack(side=RIGHT, anchor=NE)
    #logpopupvar.set(False)                    # ANDROID - webbrowser failed initially 
    #logpopupbtn.config(state=DISABLED)        # ANDROID - webbrowser failed initially
    

    #
    # BACKUP TOGGLES
    #
    
    # enable/disable when '-auto' run mode selected/deselected [2.0] [3.0]
    bkpfrm = Frame(ctrlfrm, relief=GROOVE, border=3)
    bkpfrm.pack(fill=X)
    Label(bkpfrm, text='Backups', font=HDRFONT).pack()
    
    bkpvar = BooleanVar()
    bkpbtn = Checkbutton(bkpfrm,
                text='Save TO items replaced or deleted, note adds?',   # ANDROID - shorter [Mar2819]
                font=LABELFONT,                                         # ANDROID - configurable [Mar2819]
                variable=bkpvar,
                command=onbkptoggle)
    bkpbtn.pack(anchor=NW)
    bkpvar.set(True)                 # initial=on: do backups

    # [3.0] bkpfrm.pack_forget()     # till -auto selected
    bkpbtn.config(state=DISABLED)    # till -auto selected
    
    # [2.4] support -quiet mode: omit "...backing up" per-file log messages
    quietvar = BooleanVar() 
    quietbtn = Checkbutton(bkpfrm,
                           text='Disable per-item backup messages?',    # ANDROID - shorter [Mar2819]
                           font=LABELFONT,                              # ANDROID - configurable [Mar2819]
                           variable=quietvar)
    quietbtn.pack(anchor=NW)
    quietvar.set(True)                # init=suppress (though good for errors+feedback)
    
    # [3.0] quietbtn.pack_forget()    # only if backups selected, but will be initially
    quietbtn.config(state=DISABLED)   # till -auto AND -backups selected  
  

    #
    # MESSAGES SCROLLED TEXT + 'GO' BUTTON
    #
    
    # 'go' always hidden during run to prevent overlapping run launches
    statustxt = ScrolledText(win)
    statustxt.config(state=DISABLED)  # ANDROID [Mar2319]: readonly text to avoid keyboard
    
    # [3.0] user configs: size, font, color (no border - color sets off better)
    try:
        if TEXTAREAHEIGHT: statustxt.config(height=TEXTAREAHEIGHT)
        if TEXTAREAWIDTH:  statustxt.config(width=TEXTAREAWIDTH)
        if TEXTAREAFONT:   statustxt.config(font=TEXTAREAFONT)
        if TEXTAREACOLOR:
            if isinstance(TEXTAREACOLOR, str):
                statustxt.config(bg=TEXTAREACOLOR)
            elif isinstance(TEXTAREACOLOR, tuple):
                statustxt.config(bg=TEXTAREACOLOR[0])
                statustxt.config(fg=TEXTAREACOLOR[1])
            else:
                print('Bad color value in config file')
    except Exception as why:
        print('Bad config setting: %s' % why)
    
    gobutton = Button(win, text='GO: run mergeall', font=HDRFONT,
                      command=ongobutton)
    gobutton.pack(side=BOTTOM)
    statustxt.pack(side=TOP, expand=YES, fill=BOTH)    # pack last=clip first



####################################################################################
# ON "GO": SPAWN MERGEALL PROCESS
####################################################################################



# [1.4] how spawned mergeall subprocess's text is written and decoded here
STREAM_ENCODE = 'utf8'

EOF_SENTINEL = []            # stream lines read will never be a list
linequeue = queue.Queue()    # infinite-size shared queue of objects



def ongobutton():
    """
    on GO button press: fetch gui values, confirm run, launch mergeall
    """
    # set in makewidgets
    global dirents                                         # folders
    global modevar, logvar, bkpvar, quietvar, cruftvar     # settings
    global gobutton, statustxt                             # widgets

    # [3.0] for comparison message suppresssion
    global firstcompareline
    firstcompareline = True               # reset before each run
    
    # get inputs from GUI
    fromdir = dirents['FROM'].get()       # directory fields
    todir   = dirents['TO'].get()
    logdir  = dirents['Logs'].get()
    mode    = modevar.get()               # runmode radiobtn
    dolog   = logvar.get()                # logfile checkbtn
    dobkp   = bkpvar.get()                # backups checkbtn
    quiet   = quietvar.get()              # quiet mode checkbtn [2.4]
    docruft = cruftvar.get()              # skip cruft files [3.0]
    
    # config run    
    modearg = '-report' if mode.startswith('REPORT') else '-auto'
    if dobkp and modearg != '-report':
        modearg += ' -backup'             # [2.0] backup replacements/removals
        if quiet:
            modearg += ' -quiet'          # [2.4] no per-file backup log messages

    if docruft:
        modearg += ' -skipcruft'          # [3.0] ignore cruft files in FROM and TO

    if not dolog:
        logpath = logfile = None
    else:
        datestamp = time.strftime('date%y%m%d-time%H%M%S')
        logpath   = logdir + os.sep + 'mergeall-%s.txt' % (datestamp)

    # confirm run
    if modearg.startswith('-report'):
        runtype = 'REPORT-ONLY RUN'
        warning = 'This run will not change your data.'
    else:
        runtype = 'AUTO-UPDATE RUN'
        warningbase = (
            # ANDROID [Mar2319] - manually line break for fit (but Tk still truncates paths)
            #
            # '*WARNING*: by design, this may change your TO folder tree in-place, '
            # 'by adding, replacing, and deleting files and folders as needed '
            # 'to make TO the same as FROM.')
            #
            '*CAUTION*: by design, this run may change\n'
            'your TO folder tree in-place, by adding,\n'
            'replacing, and deleting files and folders\n'
            'as needed to make TO the same as FROM.')

        warningmore = (
            # ANDROID [Mar2319] - manually line break for fit (but Tk still truncates paths)
            #
            # '  Because backups are disabled, any such changes '
            # 'will be permanent and irrevocable.')
            #
            '\nBecause backups are disabled, any such\n'
            'changes cannot be undone.')
        warning = warningbase + ('' if dobkp else warningmore)
        
    confirm = askokcancel('%s: Confirm Run' % APPNAME,
            'About to run:\n'
            'mergeall.py %s\n\n'
            'FROM:\n%s\n\n'
            'TO:  \n%s\n\n'
            'Logging output to:\n%s\n\n'
            '%s\n\n'
            'Start this %s?' %
                          (modearg, fromdir, todir, logpath, warning, runtype))

    notruntitle = '%s: Not Run' % APPNAME
    if not confirm:
        showinfo(notruntitle,  'The mergeall run was cancelled.')
    elif not os.path.exists(fromdir):
        showerror(notruntitle, 'Please select a valid mergeall FROM folder.')      # [2.0] popup
    elif not os.path.exists(todir):
        showerror(notruntitle, 'Please select a valid mergeall TO folder.')        # [2.0] popup
    elif dolog and not os.path.exists(logdir):
        showerror(notruntitle, 'Please select a valid mergeall log file folder.')  # or sooner?
    else:
        # [1.4] log uses binary mode for now-binary data from stream
        if dolog:
            try:
                logfile = open(logpath, 'wb')
            except:
                # [1.7] catch PermissionError and show popup (else silent for .pyw)
                showerror(notruntitle, 'Please select a writeable log file folder.')
                return

        # proceed with mergeall
        # [3.0] gobutton.pack_forget()     # hide/erase button
        gobutton.config(state=DISABLED)    # keep but disable
        statustxt.config(state=NORMAL)     # ANDROID [Mar2319]: enable text for changes during run
        statustxt.delete('1.0', END)       # clear last run text
        

        # [1.4] force UTF8 prints in mergeall, use binary streams + manual decode here;
        # this setting is inherited by the spawned mergeall subprocess for its prints;
        os.environ['PYTHONIOENCODING'] = STREAM_ENCODE

        # config mergeall command (sequences: auto-quoted by subprocess)
        extras = {}
        if hasattr(sys, 'frozen') and (RunningOnWindows or RunningOnLinux):
            # pyinstaller exe [3.0]
            # run frozen executable directly, not script through python
            
            freezename = 'mergeall.exe' if RunningOnWindows else 'mergeall'
            mergeallpath = os.path.join(MYDIR, freezename)
            os.environ['PYTHONUNBUFFERED'] = 'True'           # -u equiv (iff env?)
            cmdseq = [mergeallpath,                           # frozen executable
                      fromdir,                                # '/' ok on Windows
                      todir] + modearg.split()                # 'a b?' -> ['a', 'b'?]
            
            if RunningOnWindows:
                # else spawn hangs unless launcher uses --console (with popup!)
                # startupinfo, env=os.environ, and creationflags are irrelevant
                extras.update(stdin=subprocess.DEVNULL)

        else:
            # py2app Mac app or source (original code)
            # relative script path works whether run here or via desktop shortcut
            # [3.0] but not in os.getcwd() if run from a cmdline elsewhere

            # ANDROID - hardcode sys.executable, else empty in Pydroid 3: kills Popen
            #
            # ANDROID [Apr1919]: Pydroid 3's 3.0 release moved its Python from the
            # first of the following paths to the second, breaking this workaround:
            #    /data/user/0/ru.iiec.pydroid3/files/arm-linux-androideabi/bin/python
            #    /data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/bin/python
            # to allow for both paths--and be platform agnostic in general--read the
            # result of a 'which python' shell command instead of using literal strs;
            #
            sys.executable = os.popen('which python').read().rstrip()  # path to Python exe

            scriptname = 'mergeall.py'
            mergeallpath = os.path.join(MYDIR, scriptname)      
            cmdseq = [sys.executable, '-u',                   # [1.4] need -u unbufferred
                      mergeallpath,                           # script file (app or source)
                      fromdir,                                # '/' ok on Windows
                      todir] + modearg.split()                # 'a b?' -> ['a', 'b'?]

        # [1.5] shell should be True on Windows so that it uses filename associations,
        # but False on Linux so that it doesn't just start a "python" interactive shell
        doshell = RunningOnWindows
        
        # spawn mergeall
        # use subprocess: os.popen/spawnv not enough, popen2 is 2.X only;
        subproc = subprocess.Popen(
                      cmdseq,                     # a string cmd may fail on Unix
                      shell=doshell,              # [1.5] see note above, platform specific
                      universal_newlines=False,   # [1.4] binary mode, manual decode/eoln
                      stdout=subprocess.PIPE,     # capture sub's stdout here
                      stderr=subprocess.STDOUT,   # route sub's stderr to its stdout
                      **extras)

        # read and process mergeall's output: reader thread + timer-based poller
        _thread.start_new_thread(streamreader, (subproc.stdout, linequeue))
        streamconsumer(linequeue, logfile, logpath)

        # returns here immediately: a thread and timer-event loop are now running

    # [3.0] for all cases, else requires click on Mac
    refocusWindow()



####################################################################################
# MERGEALL PROCESS HANDLER: THREAD + POLLER
####################################################################################



def streamreader(stream, linequeue):
    """
    [1.4] In a parallel thread - read the mergeall subprocess's stdout/stderr
    stream, and post its lines to a queue for the GUI to read and display
    on timer event callbacks; this way, the GUI isn't blocked/paused during
    long-running copies or other actions in the spawned mergeall script;
    """
    for line in stream:             # read stdout+stderr lines: may block this thread
        linequeue.put(line)         # place on queue to be picked up by GUI thread
    linequeue.put(EOF_SENTINEL)     # write sentinel at eof and exit: subprocess ended



def streamconsumer(linequeue, logfile, logpath):
    """
    [1.4] In the main GUI thread - run a timer-based loop to poll for, read,
    and display and log stream lines from the shared thread queue until the
    reader thread sends the end-signal sentinel value on the queue.  The main
    GUI thread running this code thus remains active between mergeall output
    lines.  A nested loop is also used here to process lines in batches so the
    GUI's response to lines is quick, but it calls update() to remain active.
    
    At this point we have 2 threads and a process (connected by queue and stream)
    and 3 or 4 loops going at once -- the main GUI thread runs a timer event loop
    to poll the queue, and runs the nested line-batch loop here; the spawned
    stream-reader thread runs a blockable reading loop and posts lines to the
    queue; and the spawned mergeall process runs its own file-processing loops
    to create output lines eventually displayed in the GUI here.
    """
    global statustxt, gobutton           # widgets
    global firstcompareline              # state 
    global cmpmsgsvar, logpopupvar       # settings


    def trydecode(binline, stream_encode):
        """
        [1.6] line decode can fail in Python 2.X due to a TBD library
        incompatibility issue; see 1.6 note near top of this script;

        if uncaught, GUI is dead but unclosed, and the error message does
        not appear in GUI -- because the error occurs here in GUI instead 
        of subproc, its text goes to console here (if any), not to subproc 
        stream queue, and the subproc is apparently terminated in 2.X;

        also note that "line" text here is used for the GUI display only:
        it doesn't show up in the binary log file, and this has no impact 
        on the underlying mergeall process, which proceeds unaffected;

        [3.0] changed the error message to be a str instead of a bytes;
        the latter would surely fail later in the caller under python 3.X,
        but the decode here probably only ever failed on python 2.X, where
        a bytes result works because bytes is really just a synonym for str;
        """
        try:
            line = binline.decode(stream_encode)        # [1.4] manual decode here, match subproc
        except UnicodeDecodeError:
           #line = b'(UNDECODABLE LINE): ' + binline    # [1.6] don't let this kill the GUI in 2.X
            line = '(UNDECODABLE LINE: see log file)\n' # [3.0] use str, but drop the content
        return line


    try:
        binline = linequeue.get(block=False)       # check the queue
    except queue.Empty:
        pass                                       # nothing posted yet: reschedule and wait
    else:
        # process a batch of 1 or more objects
        while True:
            
            if binline != EOF_SENTINEL:                
                # process the next line string: GUI + logfile
                
                eoln = os.linesep                         # local line-end: \r\n Windows, \n Unix
                line = trydecode(binline, STREAM_ENCODE)  # [1.4] manual decode here, match subproc [1.6] 
                line = line.replace(eoln, '\n')           # [1.4] and fix any Windows eolns for tk

                # [3.0] sanitize Unicode in line to be displayed in GUI
                line = fixTkBMP(line)
                
                # [3.0] allow comparison messages to be suppressed in the GUI, dynamically
                anycompare = ('comparing', '"comparing', "'comparing")   # ascii() in Windows exe!
                if line.startswith(anycompare):                          # in line content?
                    if cmpmsgsvar.get():                                 # suppress toggle on?
                        if firstcompareline:
                            # show first line only for top-level dirs, plus message
                            firstcompareline = False
                            statustxt.insert(END, line)
                            statustxt.insert(END, 'Folder comparison messages '
                                                  'are being suppressed in the GUI...\n')
                            statustxt.see(END+'-2l')      # scroll to new end of text
                        else:
                            # skip all other compare lines in GUI (only)
                            pass
                    else:
                        # show comparison line, reset to show message if toggled on+off
                        firstcompareline = True           # reshow msg if toggled again
                        statustxt.insert(END, line)       # add to end of text widget
                        statustxt.see(END+'-2l')          # scroll to new end of text
                else:
                    # show all other lines normally, don't reset for message 
                    statustxt.insert(END, line)           # add to end of text widget
                    statustxt.see(END+'-2l')              # scroll to new end of text
                                                          # '-2l' = before empty auto \n at end
                                                          
                # force GUI to show/respond now (else dead during batch)
                statustxt.update() 

                # write binary stream line to binary logfile
                if logfile:                                    # also save to log file? [1.4]: binary
                    eoln = os.linesep.encode()                 # must be bytes in 3.X (no-op in 2.X)
                    binline = binline.replace(b'\r\n', b'\n')  # [1.4] got just \n from '-u' in 2.X only
                    binline = binline.replace(b'\n', eoln)     # replaces are no-op in 3.X and unix 
                    logfile.write(binline)

                # read next line if any, else goto reschedule and wait
                if linequeue.empty():
                    break
                else:
                    binline = linequeue.get(block=False)   # back to top of loop
                
            else:
                # reader thread posted eof sentinel and exited: close out the run
                showinfo('%s: Finished' % APPNAME,
                    'The mergeall run has finished.' +
                    ('' if not logfile else
                       ('\nSee its log file in the popup window.' if logpopupvar.get() else
                        '\nSee its log file in the logs folder.')))
                refocusWindow()   # [3.0] else requires click on Mac
            
                # if logging: close logfile, show in editor if toggled on [3.0]
                if logfile:
                    logfile.close()                  
                    if logpopupvar.get():
                        # [3.0] Mac OS X is pickier about file URLs
                        if RunningOnMac:
                            logpath = 'file:' + logpath
 
                        #
                        # ANDROID [Apr1219] - webbrowser fails on Android (for reasons TBD), 
                        # so spawn a shell command using the $BROWSER preset in Pydroid 3:
                        # "am start --user 0 -a android.intent.action.VIEW -d %s";
                        # safe to assume logpath is accessible (else can't write anyhow);
                        #
                        # ANDROID [Apr1919] - webbrowser _does_ work, but requires local file
                        # URLs to start with "file://"; prefix as required, and use either 
                        # os.system or webbrowser.open to display the logfile in the GUI;
                        #
                        # ANDROID [Apr2119]: Pydroid 3 3.0 broke webbrowser and changed 
                        # $BROWSER to skip "file://" - use os.system() +  hardcoded command;
                        #
                        brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
                        url = 'file://' + logpath
                        cmd = brw % url
                        os.system(cmd)          # _not_ os.environ['BROWSER'], webbrowser.open()

                        # other platforms code...
                        """
                        # webbrowser opens text files in Notepad on Windows,
                        # gedit on Linux, and TextEdit on Mac OS X (but YMMV)
                        webbrowser.open(logpath)      # assume never raises exc
                        """

                # [3.0] reenable new runs now
                gobutton.config(state=NORMAL)
                statustxt.config(state=DISABLED)    # ANDROID [Mar2319]: back to readonly to avoid keyboard

                # [3.0] the following had odd text scrolls after vertical resizes
                # statustxt.pack_forget()
                # gobutton.pack(side=BOTTOM)                        # unhide button
                # statustxt.pack(side=TOP, expand=YES, fill=BOTH)   # pack last=clip first
 
                # exit the timer events loop: back to waiting on user
                return

        # end batch while loop
        
    # reschedule and wait: check queue 10 times per second (msecs)
    statustxt.after(100, streamconsumer, linequeue, logfile, logpath)



####################################################################################
# MAIN/TOP-LEVEL LOGIC
####################################################################################



if __name__ == '__main__':

    if not RunningOnMac:                     # Windows and Linux: normal
        root = Tk()                          # 'root' is used elsewhere
        makewidgets(root)
        root.mainloop()
       
    else:
        
        #----------------------------------------------------------------------------
        # [3.0] Mac OS X hack: a partial workaround for a bug in the recommended AS
        # Mac Tk 8.5 for Python 3.5.  Hide/unhide main window so it shows its radio
        # and check buttons in Aqua's active-window style (default blue) immediately.
        # This code fixes style at initial opening only; style can be lost on popups
        # and minimize/restore -- click this window, and possibly others first, to
        # reset style as needed.  More: docetc/miscnotes/mac-main-hack-notes.txt.
        #
        # This may be fixed in Tk 8.6, which may be supported by py.org's Python 3.X
        # someday, and is supported by homebrew's Python distribution (to be tested).
        # Unlike frigcal and pymailgui, a lift() is not enough here, whether clicked
        # to open in the mac python launcher, or run from a 'python3' command line.
        #
        # Update: root.force_focus() is now used to restore window active state after
        # dialogs, but doesn't help for deiconifies caught via <Map> or <Visibility>
        # events, and has no impact here on initial state in all codings attempted.
        # 
        # Update: the following don't help even if they do a focus_force (why?):
        # root.bind('<Map>', onUnhide) + root.after(2000, refocusWindow),
        # root.createcommand('::tk::mac::onShow', onShow),
        # root.createcommand('::tk::mac::ReopenApplication', onReopen)
        #
        # UPDATE: losing focus in deiconifies in AS Tk 8.5 was finally fixed by the
        # hideous workaround below, which creates and then immediately destroys a 
        # new but lowered (and hence invisible) top-level window on the Mac 
        # reopen-app even (i.e., Doc and app icon clicks).  The widgets flash off
        # and on momentarily (and the temp window may flash if mergeall is not at
        # fullscreen), but otherwise are active styled.  Tk 8.6 status tbd... 
        #----------------------------------------------------------------------------

        root = Tk()
        makewidgets(root)

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
        

        """
        # an alternative open workaround: a bogus Tk root, iconified after 2 seconds:
        root = Tk()
        root.protocol('WM_DELEsTE_WINDOW', lambda: None)
        Label(root, text='Welcome to mergeall', width=25, height=5).pack()
        makewidgets(Toplevel())
        root.after(2000, root.iconify)
        root.mainloop()
        """

        """
        # a 15-line AppleScript alternative omitted here for space (and humanity...)
        """
